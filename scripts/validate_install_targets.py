#!/usr/bin/env python3
"""Validate installable skill targets in this repository."""

from __future__ import annotations

from pathlib import Path
import re
import sys


EXPECTED_TARGETS = {
    "skills/athena": "athena",
}

REQUIRED_FILES = {
    "skills/athena": (
        "agents/openai.yaml",
        "assets/athena-warrior-icon.svg",
    ),
}

EXPECTED_INTERFACE_BINDINGS = {
    "skills/athena": {
        "icon_small": "./assets/athena-warrior-icon.svg",
        "icon_large": "./assets/athena-warrior-icon.svg",
    }
}

FRONTMATTER_DELIM = "---"


def parse_frontmatter(skill_md: Path) -> dict[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != FRONTMATTER_DELIM:
        raise ValueError("missing opening YAML frontmatter delimiter '---'")

    end = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == FRONTMATTER_DELIM:
            end = idx
            break
    if end is None:
        raise ValueError("missing closing YAML frontmatter delimiter '---'")

    data: dict[str, str] = {}
    key_re = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$")
    for line in lines[1:end]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = key_re.match(line)
        if not match:
            raise ValueError(f"invalid frontmatter line: {line!r}")
        key, value = match.group(1), match.group(2).strip()
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]
        data[key] = value
    return data


def _strip_yaml_scalar(raw_value: str) -> str:
    value = raw_value.strip()
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def parse_interface_block(openai_yaml: Path) -> dict[str, str]:
    text = openai_yaml.read_text(encoding="utf-8")
    fields: dict[str, str] = {}
    in_interface = False

    key_re = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$")
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped == "interface:":
            in_interface = True
            continue

        if not in_interface:
            continue

        if not line.startswith((" ", "\t")):
            break

        match = key_re.match(line)
        if not match:
            continue

        key, value = match.group(1), _strip_yaml_scalar(match.group(2))
        fields[key] = value

    return fields


def validate_required_files(target_dir: Path, rel_path: str) -> list[str]:
    errors: list[str] = []
    for rel_file in REQUIRED_FILES.get(rel_path, ()):
        if not (target_dir / rel_file).is_file():
            errors.append(f"{rel_path}: missing required file '{rel_file}'")
    return errors


def validate_interface_bindings(target_dir: Path, rel_path: str) -> list[str]:
    errors: list[str] = []
    expected_bindings = EXPECTED_INTERFACE_BINDINGS.get(rel_path, {})
    if not expected_bindings:
        return errors

    openai_yaml = target_dir / "agents/openai.yaml"
    if not openai_yaml.is_file():
        return errors

    interface_fields = parse_interface_block(openai_yaml)
    for key, expected_value in expected_bindings.items():
        actual_value = interface_fields.get(key)
        if actual_value != expected_value:
            errors.append(
                f"{rel_path}: agents/openai.yaml interface.{key} must be "
                f"'{expected_value}', got '{actual_value or ''}'"
            )

    return errors


def validate_target(repo_root: Path, rel_path: str, expected_name: str) -> list[str]:
    errors: list[str] = []
    target_dir = repo_root / rel_path

    if not target_dir.is_dir():
        return [f"{rel_path}: target directory does not exist"]

    skill_files = sorted(target_dir.rglob("SKILL.md"))
    if len(skill_files) != 1:
        return [
            f"{rel_path}: expected exactly 1 SKILL.md, found {len(skill_files)}"
        ]

    top_skill = target_dir / "SKILL.md"
    if skill_files[0] != top_skill:
        errors.append(
            f"{rel_path}: SKILL.md must be at target root ({top_skill}), "
            f"found at {skill_files[0]}"
        )
        return errors

    try:
        frontmatter = parse_frontmatter(top_skill)
    except ValueError as exc:
        return [f"{rel_path}: invalid SKILL.md frontmatter: {exc}"]

    required = {"name", "description"}
    keys = set(frontmatter.keys())
    missing = sorted(required - keys)
    extras = sorted(keys - required)

    if missing:
        errors.append(f"{rel_path}: missing frontmatter keys: {', '.join(missing)}")
    if extras:
        errors.append(f"{rel_path}: unsupported frontmatter keys: {', '.join(extras)}")

    name_value = frontmatter.get("name", "")
    if name_value != expected_name:
        errors.append(
            f"{rel_path}: frontmatter name must be '{expected_name}', got '{name_value}'"
        )

    description = frontmatter.get("description", "").strip()
    if not description:
        errors.append(f"{rel_path}: frontmatter description must be non-empty")

    errors.extend(validate_required_files(target_dir, rel_path))
    errors.extend(validate_interface_bindings(target_dir, rel_path))

    return errors


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    all_errors: list[str] = []

    for rel_path, expected_name in EXPECTED_TARGETS.items():
        errors = validate_target(repo_root, rel_path, expected_name)
        if errors:
            all_errors.extend(errors)
        else:
            print(f"OK: {rel_path} -> {expected_name}")

    if all_errors:
        print("Validation failed:", file=sys.stderr)
        for error in all_errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("All install targets validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
