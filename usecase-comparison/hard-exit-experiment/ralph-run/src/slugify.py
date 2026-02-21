#!/usr/bin/env python3
"""Iteration 2: deterministic kebab-case slugifier with report."""

from __future__ import annotations

import json
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path


def normalize_slug(value: str):
    raw = value.strip()
    if not raw:
        return None, "empty-line", False

    unicode_normalized = any(ord(ch) > 127 for ch in raw)
    normalized = unicodedata.normalize("NFKD", raw)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    ascii_text = ascii_text.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text).strip("-")

    if not slug:
        return None, "no-usable-chars", unicode_normalized

    return slug, None, unicode_normalized


def main() -> None:
    src = Path("input.txt")
    output = Path("output.txt")
    report = Path("report.json")

    lines = src.read_text(encoding="utf-8").splitlines()
    invalid_lines = []
    valid_slugs = []
    unicode_normalized_count = 0

    for idx, line in enumerate(lines, start=1):
        slug, reason, used_unicode = normalize_slug(line)
        if slug is None:
            invalid_lines.append({"line_number": idx, "raw": line, "reason": reason})
            continue

        if used_unicode:
            unicode_normalized_count += 1

        valid_slugs.append(slug)

    output_lines = sorted(set(valid_slugs))
    output.write_text("\n".join(output_lines) + ("\n" if output_lines else ""), encoding="utf-8")

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_file": str(src),
        "total_lines": len(lines),
        "valid_lines": len(valid_slugs),
        "invalid_lines": invalid_lines,
        "output_count": len(output_lines),
        "unique_count": len(output_lines),
        "duplicates_removed": len(valid_slugs) - len(output_lines),
        "unicode_normalized_count": unicode_normalized_count,
    }
    report.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
