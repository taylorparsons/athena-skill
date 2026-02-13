#!/usr/bin/env python3
"""Deterministic terminal snake simulator with replay and optional interactive play."""

from __future__ import annotations

import argparse
import json
import random
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

Direction = Tuple[int, int]
DIR_MAP = {
    "U": (0, -1),
    "W": (0, -1),
    "UP": (0, -1),
    "D": (0, 1),
    "S": (0, 1),
    "DOWN": (0, 1),
    "L": (-1, 0),
    "A": (-1, 0),
    "LEFT": (-1, 0),
    "R": (1, 0),
    "RIGHT": (1, 0),
}

DIR_LABELS = {
    (1, 0): "R",
    (-1, 0): "L",
    (0, -1): "U",
    (0, 1): "D",
}

Opp = {
    (0, -1): (0, 1),
    (0, 1): (0, -1),
    (-1, 0): (1, 0),
    (1, 0): (-1, 0),
}


@dataclass
class Step:
    tick: int
    direction: str
    head: Tuple[int, int]
    food: Tuple[int, int]
    score: int
    length: int
    alive: bool
    collision: str | None
    board: List[str]


def direction_to_label(direction: Direction) -> str:
    return DIR_LABELS.get(direction, "R")


def parse_moves(path: Path) -> List[str]:
    if not path.exists():
        return []
    raw = path.read_text(encoding="utf-8").strip().splitlines()
    return [line.strip().upper() for line in raw if line.strip()]


def next_food(rng: random.Random, width: int, height: int, occupied):
    for _ in range(200):
        x = rng.randint(1, width - 2)
        y = rng.randint(1, height - 2)
        if (x, y) not in occupied:
            return x, y
    raise RuntimeError("Cannot place food")


def draw_board(width: int, height: int, snake: Sequence[Tuple[int, int]], food: Tuple[int, int]):
    occupied = set(snake)
    rows = []
    for y in range(height):
        row = []
        for x in range(width):
            if x in (0, width - 1) or y in (0, height - 1):
                row.append("#")
            elif (x, y) == food:
                row.append("*")
            elif (x, y) == snake[0]:
                row.append("H")
            elif (x, y) in occupied:
                row.append("S")
            else:
                row.append(" ")
        rows.append("".join(row))
    return rows


def step_once(width: int, height: int, rng: random.Random, snake: List[Tuple[int, int]],
              food: Tuple[int, int], score: int, direction: Direction, next_move: str | None):
    proposed = direction
    if next_move:
        candidate = DIR_MAP.get(next_move, direction)
        if candidate and candidate != Opp.get(direction):
            proposed = candidate

    head_x, head_y = snake[0]
    dx, dy = proposed
    new_head = (head_x + dx, head_y + dy)
    alive = True
    collision = None

    x, y = new_head
    if x <= 0 or x >= width - 1 or y <= 0 or y >= height - 1:
        alive = False
        collision = "wall"
    elif new_head in snake:
        alive = False
        collision = "self"

    if alive:
        snake.insert(0, new_head)
        if new_head == food:
            score += 1
            food = next_food(rng, width, height, set(snake))
        else:
            snake.pop()

    board = draw_board(width, height, snake, food)
    return snake, food, score, proposed, alive, collision, new_head, board


def run_replay(width: int, height: int, seed: int, moves: List[str], max_ticks: int):
    rng = random.Random(seed)
    snake = [(width // 2, height // 2), (width // 2 - 1, height // 2)]
    direction: Direction = (1, 0)
    food = next_food(rng, width, height, set(snake))
    score = 0

    steps = []
    alive = True
    collision = None
    board = draw_board(width, height, snake, food)

    for tick in range(1, max_ticks + 1):
        move = moves[tick - 1] if tick - 1 < len(moves) else None
        snake, food, score, direction, alive, collision, head, board = step_once(
            width, height, rng, snake, food, score, direction, move
        )

        steps.append(
            Step(
                tick=tick,
                direction=direction_to_label(direction),
                head=head,
                food=food,
                score=score,
                length=len(snake),
                alive=alive,
                collision=collision,
                board=board,
            ).__dict__
        )

        if not alive:
            break

    summary = {
        "width": width,
        "height": height,
        "seed": seed,
        "total_steps": len(steps),
        "moves_used": len(moves),
        "score": score,
        "length": len(snake),
        "alive": alive,
        "collision": collision,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "final_head": snake[0] if snake else None,
        "board": "\n".join(board),
    }
    return summary, steps


def run_play(width: int, height: int, seed: int, max_ticks: int, frame_delay_ms: int):
    import curses

    def key_to_direction(key: int) -> str | None:
        mapping: Dict[int, str] = {
            curses.KEY_UP: "U",
            curses.KEY_DOWN: "D",
            curses.KEY_LEFT: "L",
            curses.KEY_RIGHT: "R",
            ord("w"): "U",
            ord("W"): "W",
            ord("s"): "D",
            ord("S"): "S",
            ord("a"): "L",
            ord("A"): "A",
            ord("d"): "R",
            ord("D"): "RIGHT",
        }
        return mapping.get(key)

    rng = random.Random(seed)
    snake = [(width // 2, height // 2), (width // 2 - 1, height // 2)]
    direction: Direction = (1, 0)
    food = next_food(rng, width, height, set(snake))
    score = 0
    steps = []

    def game_loop(screen):
        nonlocal snake
        nonlocal food
        nonlocal score
        nonlocal direction
        screen.nodelay(True)
        curses.curs_set(0)
        alive = True
        collision = None
        board = draw_board(width, height, snake, food)
        end_reason = "in_progress"

        for tick in range(1, max_ticks + 1):
            start_ms = time.time() * 1000
            key = screen.getch()
            if key in (ord("q"), ord("Q")):
                end_reason = "quit"
                break

            move = key_to_direction(key)
            snake, food, score, direction, alive, collision, head, board = step_once(
                width, height, rng, snake, food, score, direction, move
            )

            screen.clear()
            for y, row in enumerate(board):
                screen.addstr(y, 0, row)
            screen.addstr(
                height,
                0,
                f"tick:{tick} score:{score} len:{len(snake)} "
                f"dir:{direction_to_label(direction)} alive:{alive} collision:{collision or '-'}",
            )
            screen.addstr(
                height + 1,
                0,
                "controls: W/A/S/D or arrows, Q to quit",
            )
            screen.refresh()

            steps.append(
                Step(
                    tick=tick,
                    direction=direction_to_label(direction),
                    head=head,
                    food=food,
                    score=score,
                    length=len(snake),
                    alive=alive,
                    collision=collision,
                    board=board,
                ).__dict__
            )

            if not alive:
                end_reason = collision
                break

            elapsed_ms = int((time.time() * 1000) - start_ms)
            delay = max(0, frame_delay_ms - elapsed_ms)
            if delay > 0:
                curses.napms(delay)

        if not alive:
            screen.addstr(
                height + 2, 0, f"Game over ({end_reason}). Press any key to continue."
            )
        elif end_reason == "quit":
            screen.addstr(height + 2, 0, "Stopped by user. Press any key to continue.")
        elif end_reason == "in_progress":
            screen.addstr(height + 2, 0, "Stopped by tick limit. Press any key to continue.")
        screen.refresh()
        screen.nodelay(False)
        screen.getch()

        return {
            "summary": {
                "width": width,
                "height": height,
                "seed": seed,
                "total_steps": len(steps),
                "moves_used": 0,
                "score": score,
                "length": len(snake),
                "alive": alive,
                "collision": collision if collision else end_reason,
                "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "final_head": snake[0] if snake else None,
                "board": "\n".join(board),
            },
            "steps": steps,
        }

    return curses.wrapper(game_loop)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", type=int, default=30)
    parser.add_argument("--height", type=int, default=16)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-ticks", type=int, default=80)
    parser.add_argument("--moves-file", default="moves.txt")
    parser.add_argument("--frame-delay-ms", type=int, default=0)
    parser.add_argument("--output", default="game-metrics.json")
    parser.add_argument("--play", action="store_true", help="Open interactive terminal game")
    args = parser.parse_args()

    if args.play:
        result = run_play(
            width=args.width,
            height=args.height,
            seed=args.seed,
            max_ticks=args.max_ticks,
            frame_delay_ms=args.frame_delay_ms,
        )
        summary = result["summary"]
        steps = result["steps"]
    else:
        moves = parse_moves(Path(args.moves_file))
        summary, steps = run_replay(
            width=args.width,
            height=args.height,
            seed=args.seed,
            moves=moves,
            max_ticks=args.max_ticks,
        )

    data = {
        "meta": {
            "command": {
                "width": args.width,
                "height": args.height,
                "seed": args.seed,
                "max_ticks": args.max_ticks,
                "moves_file": args.moves_file,
                "play": args.play,
            }
        },
        "summary": summary,
        "steps": steps,
    }
    Path(args.output).write_text(json.dumps(data, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
