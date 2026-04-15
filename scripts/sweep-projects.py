#!/usr/bin/env python3
"""
sweep-projects.py — Weekly token-optimization sweeper for Athena projects.

Usage:
    python3 ~/.claude/skills/athena/scripts/sweep-projects.py [OPTIONS] [BASE_DIR...]

Options:
    --dry-run    Report issues without running auto-fixes
    --fix        Run safe auto-fixes (update-index, prune-done, write-memory)
    --verbose    Show all checks, not just issues
    --sync       Copy this script to ~/.claude/skills/athena/scripts/ and exit

BASE_DIR defaults to $HOME and /Volumes (if it exists).
"""

import re
import shutil
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path
from typing import List

SKILL_DIR = Path(__file__).parent.parent.resolve()
DEFAULT_LOG = Path.home() / ".claude" / "logs" / "athena-sweep.log"

BINARY_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".pdf", ".webp", ".ico"}
PROGRESS_LINE_THRESHOLD = 200
PROGRESS_ARCHIVE_LINE_THRESHOLD = 500
REQUESTS_LINE_THRESHOLD = 150
LARGE_FILE_KB = 100
INDEX_STALE_DAYS = 7
MIN_SPECS_FOR_INDEX = 3

# Token cost constants (mirror owl.py)
TOKENS_PER_SPEC = 500
TOKENS_PER_LINE = 10


# ── Project discovery (verbatim from migrate-all-projects.py) ─────────────────

def find_athena_projects(base_dirs: List[Path]) -> List[Path]:
    """Return all project roots that contain docs/requests.md."""
    projects = []

    for base in base_dirs:
        if not base.exists():
            continue
        try:
            result = subprocess.run(
                ["find", str(base), "-name", "requests.md",
                 "-path", "*/docs/requests.md",
                 "-not", "-path", "*/.git/*",
                 "-not", "-path", "*/node_modules/*",
                 "-not", "-path", "*/__pycache__/*"],
                capture_output=True, text=True, timeout=60
            )
        except subprocess.TimeoutExpired:
            print(f"  ⚠️  Search timed out in {base}, skipping")
            continue

        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            requests_file = Path(line)
            project_root = requests_file.parent.parent
            resolved = project_root.resolve()
            if resolved == SKILL_DIR.resolve():
                continue
            try:
                resolved.relative_to(SKILL_DIR)
                continue  # inside the skill dir
            except ValueError:
                pass
            projects.append(project_root.resolve())

    return sorted(set(projects))


# ── Status helpers (derived from owl.py) ──────────────────────────────────────

def _get_spec_status(spec_dir: Path) -> str:
    """Return 'Active' or 'Done'. Ground truth is tasks.md, fallback is spec.md."""
    tasks = spec_dir / "tasks.md"
    if tasks.exists():
        content = tasks.read_text()
        for section in ("## NEXT", "## IN PROGRESS"):
            if section in content:
                idx = content.index(section) + len(section)
                next_section = content.find("##", idx)
                block = content[idx:next_section] if next_section != -1 else content[idx:]
                real_lines = [l.strip() for l in block.splitlines()
                              if l.strip() and not l.startswith("#")]
                if real_lines:
                    return "Active"
        return "Done"
    spec = spec_dir / "spec.md"
    if spec.exists():
        m = re.search(r"^\*\*Status:\*\*\s*(\w+)", spec.read_text(), re.MULTILINE)
        if m:
            return m.group(1)
    return "Done"


# ── Check functions ────────────────────────────────────────────────────────────

def check_missing_index(root: Path) -> List[dict]:
    specs_dir = root / "docs" / "specs"
    index = root / "docs" / "athena-index.md"
    if index.exists() or not specs_dir.exists():
        return []
    count = sum(1 for d in specs_dir.iterdir() if d.is_dir() and (d / "spec.md").exists())
    if count < MIN_SPECS_FOR_INDEX:
        return []
    return [{"rule": "missing_index",
             "message": f"athena-index.md missing ({count} specs present)",
             "token_cost": count * TOKENS_PER_SPEC,
             "fix_cmd": ["./scripts/owl", "update-index"], "auto_fixable": True}]


def check_stale_index(root: Path) -> List[dict]:
    index = root / "docs" / "athena-index.md"
    if not index.exists():
        return []
    m = re.search(r"\*\*Last updated\*\*:\s*(\d{4}-\d{2}-\d{2})", index.read_text())
    if not m:
        return []
    last = date.fromisoformat(m.group(1))
    days = (date.today() - last).days
    if days <= INDEX_STALE_DAYS:
        return []
    return [{"rule": "stale_index",
             "message": f"athena-index.md stale ({days} days)",
             "token_cost": 0,
             "fix_cmd": ["./scripts/owl", "update-index"], "auto_fixable": True}]


def check_large_progress(root: Path) -> List[dict]:
    f = root / "docs" / "progress.txt"
    if not f.exists():
        return []
    lines = len(f.read_text().splitlines())
    if lines <= PROGRESS_LINE_THRESHOLD:
        return []
    return [{"rule": "large_progress",
             "message": f"progress.txt: {lines} lines",
             "token_cost": lines * TOKENS_PER_LINE,
             "fix_cmd": ["./scripts/owl", "prune-done"], "auto_fixable": True}]


def check_large_archive(root: Path) -> List[dict]:
    f = root / "docs" / "progress-archive.txt"
    if not f.exists():
        return []
    lines = len(f.read_text().splitlines())
    if lines <= PROGRESS_ARCHIVE_LINE_THRESHOLD:
        return []
    return [{"rule": "large_archive",
             "message": f"progress-archive.txt: {lines} lines — manual truncation recommended",
             "token_cost": 0, "fix_cmd": None, "auto_fixable": False}]


def check_unarchived_done_specs(root: Path) -> List[dict]:
    specs_dir = root / "docs" / "specs"
    index = root / "docs" / "athena-index.md"
    if not specs_dir.exists():
        return []
    archived_ids = set()
    if index.exists():
        in_archived = False
        for line in index.read_text().splitlines():
            if line.startswith("## Archived"):
                in_archived = True
            elif line.startswith("## ") and in_archived:
                in_archived = False
            elif in_archived and line.startswith("### "):
                archived_ids.add(line[4:].strip())
    unindexed = [
        d.name for d in specs_dir.iterdir()
        if d.is_dir() and _get_spec_status(d) == "Done" and d.name not in archived_ids
    ]
    if not unindexed:
        return []
    preview = ", ".join(unindexed[:3]) + ("..." if len(unindexed) > 3 else "")
    return [{"rule": "unarchived_done",
             "message": f"{len(unindexed)} done spec(s) not archived: {preview}",
             "token_cost": len(unindexed) * TOKENS_PER_SPEC,
             "fix_cmd": None, "auto_fixable": False}]


def check_large_files(root: Path) -> List[dict]:
    docs = root / "docs"
    if not docs.exists():
        return []
    issues = []
    for f in docs.rglob("*"):
        if not f.is_file() or f.suffix in BINARY_EXTENSIONS:
            continue
        kb = f.stat().st_size / 1024
        if kb > LARGE_FILE_KB:
            issues.append({"rule": "large_file",
                           "message": f"Large file: {f.relative_to(root)} ({kb:.0f} KB)",
                           "token_cost": int(f.stat().st_size // 4),
                           "fix_cmd": None, "auto_fixable": False})
    return issues


def check_binary_files(root: Path) -> List[dict]:
    docs = root / "docs"
    if not docs.exists():
        return []
    issues = []
    for f in docs.rglob("*"):
        if f.is_file() and f.suffix in BINARY_EXTENSIONS:
            kb = f.stat().st_size / 1024
            issues.append({"rule": "binary_file",
                           "message": f"Binary in docs/: {f.relative_to(root)} ({kb:.0f} KB)",
                           "token_cost": 0, "fix_cmd": None, "auto_fixable": False})
    return issues


def check_log_no_archive(root: Path) -> List[dict]:
    issues = []
    for name in ("requests.md", "decisions.md"):
        f = root / "docs" / name
        if not f.exists():
            continue
        content = f.read_text()
        lines = len(content.splitlines())
        if lines > REQUESTS_LINE_THRESHOLD and "## Archive" not in content:
            issues.append({"rule": "log_no_archive",
                           "message": f"{name}: {lines} lines, no ## Archive section",
                           "token_cost": lines * TOKENS_PER_LINE,
                           "fix_cmd": None, "auto_fixable": False})
    return issues


CHECKERS = [
    check_missing_index, check_stale_index, check_large_progress, check_large_archive,
    check_unarchived_done_specs, check_large_files, check_binary_files, check_log_no_archive,
]


# ── Core sweep ────────────────────────────────────────────────────────────────

def sweep_project(root: Path, dry_run: bool, fix: bool) -> dict:
    result = {"path": str(root), "issues": [], "fixed": [], "errors": []}
    for checker in CHECKERS:
        try:
            result["issues"].extend(checker(root))
        except Exception as e:
            result["errors"].append(f"{checker.__name__}: {e}")

    result["token_cost"] = sum(i["token_cost"] for i in result["issues"])

    if fix and not dry_run and (root / "scripts" / "owl").exists():
        seen: set = set()
        for issue in result["issues"]:
            if not issue["auto_fixable"] or not issue["fix_cmd"]:
                continue
            key = tuple(issue["fix_cmd"])
            if key in seen:
                continue
            seen.add(key)
            try:
                proc = subprocess.run(issue["fix_cmd"], cwd=str(root),
                                      capture_output=True, text=True, timeout=30)
                if proc.returncode == 0:
                    result["fixed"].append(" ".join(issue["fix_cmd"]))
                else:
                    result["errors"].append(
                        f"{' '.join(issue['fix_cmd'])}: {proc.stderr.strip()}")
            except Exception as e:
                result["errors"].append(f"{' '.join(issue['fix_cmd'])}: {e}")
        if result["fixed"]:
            try:
                subprocess.run(["./scripts/owl", "write-memory"], cwd=str(root),
                               capture_output=True, text=True, timeout=15)
                result["fixed"].append("./scripts/owl write-memory")
            except Exception:
                pass
    return result


# ── Output ────────────────────────────────────────────────────────────────────

def print_result(r: dict, verbose: bool) -> None:
    if not r["issues"] and not r["errors"] and not verbose:
        return
    print(f"── {r['path']}")
    for i in r["issues"]:
        tok = f" (~{i['token_cost']:,} tokens)" if i["token_cost"] else ""
        print(f"  ⚠️  {i['message']}{tok}")
    if not r["issues"] and verbose:
        print("  ✅ Clean")
    for f in r["fixed"]:
        print(f"  → fixed: {f}")
    for e in r["errors"]:
        print(f"  ❌ {e}")
    print()


def print_summary(results: list, fix: bool) -> None:
    total = len(results)
    clean = sum(1 for r in results if not r["issues"])
    fixed = sum(1 for r in results if r["fixed"])
    tokens = sum(r["token_cost"] for r in results)
    top = sorted(results, key=lambda r: r["token_cost"], reverse=True)[:5]
    top = [t for t in top if t["token_cost"] > 0]
    print("═" * 50)
    print(f"  Projects scanned:          {total}")
    print(f"  Clean:                     {clean}")
    print(f"  Issues found:              {total - clean}")
    if fix:
        print(f"  Auto-fixed:                {fixed}")
    print(f"  Tokens potentially wasted: ~{tokens:,}")
    if top:
        print("  Largest offenders:")
        for t in top:
            print(f"    {t['path']}  {t['token_cost']:,} tokens")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    args = sys.argv[1:]

    if "--sync" in args:
        dst = Path.home() / ".claude" / "skills" / "athena" / "scripts" / "sweep-projects.py"
        if dst.parent.exists():
            shutil.copy2(Path(__file__).resolve(), dst)
            print(f"✅ Synced to {dst}")
        else:
            print(f"❌ Destination dir not found: {dst.parent}")
        return

    dry_run = "--dry-run" in args
    fix = "--fix" in args
    verbose = "--verbose" in args
    args = [a for a in args if a not in ("--dry-run", "--fix", "--verbose")]

    base_dirs = [Path(a) for a in args] if args else [Path.home()]
    if not args and Path("/Volumes").exists():
        base_dirs.append(Path("/Volumes"))

    # Tee stdout to log file
    log_path = DEFAULT_LOG
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_fh = log_path.open("a", encoding="utf-8")

    class Tee:
        def __init__(self, fh):
            self._fh = fh
            self._out = sys.__stdout__

        def write(self, s):
            self._out.write(s)
            self._fh.write(s)

        def flush(self):
            self._out.flush()
            self._fh.flush()

    orig_stdout = sys.stdout
    sys.stdout = Tee(log_fh)

    print(f"\n{'=' * 60}")
    print(f"  Athena Sweep — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Mode: {'dry-run' if dry_run else ('fix' if fix else 'report-only')}")
    print()

    projects = find_athena_projects(base_dirs)
    if not projects:
        print("  No Athena projects found.")
        sys.stdout = orig_stdout
        log_fh.close()
        return

    print(f"  Found {len(projects)} project(s)\n")
    results = [sweep_project(p, dry_run=dry_run, fix=fix) for p in projects]
    for r in results:
        print_result(r, verbose)
    print_summary(results, fix)
    sys.stdout = orig_stdout
    log_fh.close()


if __name__ == "__main__":
    main()
