#!/usr/bin/env python3
"""Render terminal frames from game-metrics.json to MP4 via ffmpeg."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

BLACK = (0, 0, 0)
WALL = (120, 120, 120)
FOOD = (255, 0, 0)
HEAD = (0, 255, 0)
BODY = (0, 180, 0)

def p3_header(width: int, height: int):
    return f"P3\n{width} {height}\n255\n"


def board_to_rgb(board: list[str], scale: int) -> str:
    h = len(board)
    w = len(board[0]) if h else 0
    out_lines = []
    for row in board:
        pixels = []
        for ch in row:
            if ch == '#':
                rgb = WALL
            elif ch == '*':
                rgb = FOOD
            elif ch == 'H':
                rgb = HEAD
            elif ch == 'S':
                rgb = BODY
            else:
                rgb = BLACK
            px = f"{rgb[0]} {rgb[1]} {rgb[2]}"
            pixels.append((px + ' ') * scale)
        row_scaled = ''.join(pixels).rstrip()
        out_lines.extend([row_scaled] * scale)
    return '\n'.join(out_lines)


def write_ppm(frame_data: Sequence[str], out_path: Path, scale: int) -> None:
    raw_h = len(frame_data)
    raw_w = len(frame_data[0]) if raw_h else 0
    with out_path.open('w', encoding='utf-8') as f:
        f.write(p3_header(raw_w * scale, raw_h * scale))
        f.write(board_to_rgb(frame_data, scale))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("metrics")
    parser.add_argument("--scale", type=int, default=16)
    parser.add_argument("--fps", type=int, default=4)
    parser.add_argument("--out", default="artifacts")
    parser.add_argument("--video", default="artifacts/video.mp4")
    args = parser.parse_args()

    data = json.loads(Path(args.metrics).read_text(encoding='utf-8'))
    steps = data.get('steps', [])

    outdir = Path(args.out)
    ppm_dir = outdir / "frames"
    ppm_dir.mkdir(parents=True, exist_ok=True)

    for idx, step in enumerate(steps):
        board_value = step.get('board', [])
        if isinstance(board_value, list):
            board = [str(row) for row in board_value]
        else:
            board = board_value.splitlines()
        write_ppm(board, ppm_dir / f"{idx:06d}.ppm", args.scale)

    import subprocess
    subprocess.run([
        'ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(args.fps),
        '-i', str(ppm_dir / '%06d.ppm'), '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
        args.video
    ], check=True)


if __name__ == '__main__':
    main()
