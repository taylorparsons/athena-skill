#!/usr/bin/env python3
"""Create deterministic kebab-case slugs from lines in input.txt."""

from __future__ import annotations

import re
from pathlib import Path


def to_slug(value: str) -> str:
    value = value.strip().lower()
    # Normalize any run of non-alphanumeric characters to a single dash.
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def main() -> None:
    src = Path("input.txt")
    dest = Path("output.txt")
    text = src.read_text(encoding="utf-8").splitlines()
    slugs = sorted({to_slug(line) for line in text if to_slug(line)})
    dest.write_text("\n".join(slugs) + ("\n" if slugs else ""), encoding="utf-8")


if __name__ == "__main__":
    main()
