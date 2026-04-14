#!/usr/bin/env python3
"""
patch-claude-settings.py — Fix Owl hooks and CLAUDE.md for existing Athena installs

Patches applied
---------------
1. settings.json — SessionStart hook
   Early installs used `type: "agent"` which is unsupported by Claude Code and causes
   a "SessionStart hook error" on every session start. Replaced with `type: "command"`.

2. ~/.claude/CLAUDE.md — owl-of-athena skill entry
   Adds the owl-of-athena skill entry if missing. The entry scopes Owl to mid-session
   dispatches only (archive, search, stale index). The SessionStart shell hook handles
   the pre-Athena run automatically, so the CLAUDE.md entry must NOT trigger Owl at
   session start (that would cause a redundant second run after Athena has loaded).

This script is idempotent: safe to run multiple times.

Usage
-----
    python3 scripts/patch-claude-settings.py [--settings PATH] [--claude-md PATH] [--dry-run]

Options
-------
    --settings PATH    Path to settings.json  (default: ~/.claude/settings.json)
    --claude-md PATH   Path to CLAUDE.md      (default: ~/.claude/CLAUDE.md)
    --dry-run          Print what would change without writing any file
"""

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

# --- settings.json patch ---

CORRECT_COMMAND = (
    'REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null) && '
    '[ -f "$REPO_ROOT/scripts/owl" ] && '
    'cd "$REPO_ROOT" && '
    './scripts/owl prune-done && '
    './scripts/owl update-index && '
    './scripts/owl write-memory; true'
)

CORRECT_HOOK = {
    "type": "command",
    "command": CORRECT_COMMAND,
}


def is_broken_owl_hook(hook: dict) -> bool:
    return (
        hook.get("type") == "agent"
        and "owl" in hook.get("prompt", "").lower()
    )


def is_correct_owl_hook(hook: dict) -> bool:
    return (
        hook.get("type") == "command"
        and "owl" in hook.get("command", "").lower()
    )


def patch_settings(settings: dict) -> tuple[dict, list[str]]:
    changes = []
    hooks = settings.get("hooks", {})
    session_start = hooks.get("SessionStart", [])

    for entry in session_start:
        inner_hooks = entry.get("hooks", [])
        for i, hook in enumerate(inner_hooks):
            if is_broken_owl_hook(hook):
                inner_hooks[i] = CORRECT_HOOK
                changes.append("settings.json: replaced type:agent Owl hook with type:command in SessionStart")
            elif is_correct_owl_hook(hook):
                changes.append("settings.json: SessionStart Owl hook already correct — no change needed")

    return settings, changes


# --- CLAUDE.md patch ---

OWL_SECTION_MARKER = "### owl-of-athena"

OWL_SECTION = """\
### owl-of-athena
**Path:** `.claude/agents/owl-of-athena.md` (sub-agent, dispatched via Agent tool)
**Trigger:** Dispatch mid-session when: a feature is fully done (archive it), the user asks about archived features, or athena-index.md appears stale. Never load archived specs directly — use Owl. Note: `prune-done` and `update-index` run automatically via the `SessionStart` shell hook before Athena loads — do not dispatch Owl for these at session start.
"""

# Insert after the athena skill entry (before verification-before-completion or end of skills)
INSERT_AFTER = "### verification-before-completion"
INSERT_AFTER_ATHENA = "### athena"


def patch_claude_md(content: str) -> tuple[str, list[str]]:
    changes = []

    if OWL_SECTION_MARKER in content:
        # Already present — check if it has the old "At the start of every session" trigger
        if "At the start of every session" in content:
            old_trigger = (
                "**Trigger:** At the start of every session — dispatch Owl to run "
                "`update-index` and `prune-done` before any other work. Also dispatch when: "
                "a feature is fully done (archive it), the user asks about archived features, "
                "or athena-index.md appears stale. Never load archived specs directly — use Owl."
            )
            new_trigger = (
                "**Trigger:** Dispatch mid-session when: a feature is fully done (archive it), "
                "the user asks about archived features, or athena-index.md appears stale. Never load "
                "archived specs directly — use Owl. Note: `prune-done` and `update-index` run "
                "automatically via the `SessionStart` shell hook before Athena loads — do not "
                "dispatch Owl for these at session start."
            )
            if old_trigger in content:
                content = content.replace(old_trigger, new_trigger)
                changes.append("CLAUDE.md: updated owl-of-athena trigger to mid-session-only")
            else:
                changes.append("CLAUDE.md: owl-of-athena entry already correct — no change needed")
        else:
            changes.append("CLAUDE.md: owl-of-athena entry already correct — no change needed")
        return content, changes

    # Not present — insert before ### verification-before-completion if found,
    # otherwise append to end of Available Skills section
    if INSERT_AFTER in content:
        content = content.replace(
            INSERT_AFTER,
            OWL_SECTION + "\n" + INSERT_AFTER,
        )
        changes.append("CLAUDE.md: added owl-of-athena skill entry")
    else:
        content = content.rstrip() + "\n\n" + OWL_SECTION
        changes.append("CLAUDE.md: appended owl-of-athena skill entry")

    return content, changes


# --- main ---

def write_with_backup(path: Path, content: str, dry_run: bool) -> None:
    if dry_run:
        return
    backup = path.with_suffix(f".bak.{datetime.now().strftime('%Y%m%d%H%M%S')}")
    shutil.copy2(path, backup)
    print(f"  Backup: {backup}")
    path.write_text(content, encoding="utf-8")
    print(f"  Written: {path}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--settings",
        default=str(Path.home() / ".claude" / "settings.json"),
        help="Path to Claude Code settings.json",
    )
    parser.add_argument(
        "--claude-md",
        default=str(Path.home() / ".claude" / "CLAUDE.md"),
        help="Path to CLAUDE.md",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print changes without writing files",
    )
    args = parser.parse_args()
    prefix = "[dry-run] " if args.dry_run else ""
    any_writes = False

    # --- Patch settings.json ---
    settings_path = Path(args.settings)
    if not settings_path.exists():
        print(f"settings.json not found at {settings_path} — skipping")
    else:
        with settings_path.open() as f:
            try:
                settings = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error: {settings_path} is not valid JSON: {e}")
                return 1

        patched_settings, s_changes = patch_settings(settings)

        for msg in s_changes:
            print(f"{prefix}{msg}")

        if any("Replaced" in c for c in s_changes):
            any_writes = True
            if not args.dry_run:
                backup = settings_path.with_suffix(
                    f".bak.{datetime.now().strftime('%Y%m%d%H%M%S')}"
                )
                shutil.copy2(settings_path, backup)
                print(f"  Backup: {backup}")
                with settings_path.open("w") as f:
                    json.dump(patched_settings, f, indent=2, ensure_ascii=False)
                    f.write("\n")
                print(f"  Written: {settings_path}")

        if not s_changes:
            print("settings.json: no Owl SessionStart hook found — skipping")

    # --- Patch CLAUDE.md ---
    claude_md_path = Path(args.claude_md)
    if not claude_md_path.exists():
        print(f"CLAUDE.md not found at {claude_md_path} — skipping")
    else:
        original = claude_md_path.read_text(encoding="utf-8")
        patched_md, md_changes = patch_claude_md(original)

        for msg in md_changes:
            print(f"{prefix}{msg}")

        if patched_md != original:
            any_writes = True
            write_with_backup(claude_md_path, patched_md, args.dry_run)

    if any_writes and not args.dry_run:
        print("\nRestart Claude Code for changes to take effect.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
