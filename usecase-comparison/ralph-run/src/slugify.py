#!/usr/bin/env python3
"""Iteration 2: deterministic kebab-case conversion."""

from __future__ import annotations

import re
from pathlib import Path


def to_slug(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def main() -> None:
    src = Path("input.txt")
    dest = Path("output.txt")
    text = src.read_text(encoding="utf-8").splitlines()
    slugs = sorted({to_slug(line) for line in text if to_slug(line)})
    dest.write_text("\n".join(slugs), encoding="utf-8")


if __name__ == "__main__":
    main()
