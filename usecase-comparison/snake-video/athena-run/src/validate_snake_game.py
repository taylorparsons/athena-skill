#!/usr/bin/env python3
"""Basic validator for snake-metrics output."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def fail(msg: str) -> int:
    print(msg)
    return 1


def main() -> int:
    if len(sys.argv) < 2:
        return fail('Usage: validate_snake_game.py <game-metrics.json>')
    path = Path(sys.argv[1])
    if not path.exists():
        return fail(f'Missing metrics file: {path}')

    data = json.loads(path.read_text(encoding='utf-8'))
    summary = data.get('summary', {})
    steps = data.get('steps', [])
    if not steps:
        return fail('No steps in output')

    for idx, s in enumerate(steps):
        board_value = s.get("board", [])
        if isinstance(board_value, list):
            board = board_value
        else:
            board = board_value.splitlines()
        if not board or len(board) != summary['height']:
            return fail(f'step {idx}: board height mismatch')
        if any(len(row) != summary['width'] for row in board):
            return fail(f'step {idx}: board width mismatch')

    if summary['length'] < 1:
        return fail('invalid final length')

    if summary['score'] < 0:
        return fail('invalid score')

    print('validate_snake_game: OK')
    return 0


if __name__ == '__main__':
    sys.exit(main())
