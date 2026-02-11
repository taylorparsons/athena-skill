#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def _run(repo: Path, args: list[str]) -> str:
    result = subprocess.run(
        args,
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError((result.stderr or "").strip() or f"command failed: {' '.join(args)}")
    return result.stdout


def _git(repo: Path, args: list[str]) -> str:
    return _run(repo, ["git", *args])


def _git_root(repo: Path) -> Path:
    out = _git(repo, ["rev-parse", "--show-toplevel"]).strip()
    return Path(out)


def _is_git_repo(repo: Path) -> bool:
    try:
        _git(repo, ["rev-parse", "--is-inside-work-tree"])
        return True
    except Exception:
        return False


def _commit_subject(task: str, summary: str, feature: str) -> str:
    s = summary.strip().replace("\n", " ")
    return f"{task}: {s} (Feature: {feature})"


def _commit_body(feature: str, cr: str | None, decisions: str | None) -> str:
    lines: list[str] = []
    if cr:
        lines.append(f"Input: {cr}")
    if decisions:
        lines.append(f"Decisions: {decisions}")
    lines.append(f"Feature: {feature}")
    lines.append(f"Spec: docs/specs/{feature}/spec.md")
    lines.append(f"Tasks: docs/specs/{feature}/tasks.md")
    lines.append("Progress: docs/progress.txt")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Stage and create a local git commit with RALPH traceability pointers. Never pushes.",
    )
    parser.add_argument("--repo", default=".", help="Path inside the git repo (default: .).")
    parser.add_argument("--feature", required=True, help="FEATURE_ID (e.g., 20260129-peas-guardrails).")
    parser.add_argument("--task", required=True, help="Task ID (e.g., T-001).")
    parser.add_argument("--summary", required=True, help="Short summary for the commit subject.")
    parser.add_argument("--cr", help="Customer request ID (e.g., CR-YYYYMMDD-HHMM).")
    parser.add_argument("--decisions", help="Comma-separated decision IDs (e.g., D-...,D-...).")
    parser.add_argument(
        "--paths",
        nargs="*",
        help="Optional paths to stage (default: stage all changes with git add -A).",
    )
    parser.add_argument(
        "--allow-empty",
        action="store_true",
        help="Allow empty commits (default: false).",
    )
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    if not _is_git_repo(repo):
        raise RuntimeError("not a git repository (no commits made)")

    root = _git_root(repo)

    stage_args = ["add", "-A"] if not args.paths else ["add", "--", *args.paths]
    _git(root, stage_args)

    subject = _commit_subject(task=args.task, summary=args.summary, feature=args.feature)
    body = _commit_body(feature=args.feature, cr=args.cr, decisions=args.decisions)

    commit_args = ["commit", "-m", subject, "-m", body]
    if args.allow_empty:
        commit_args.insert(1, "--allow-empty")
    _git(root, commit_args)

    sha = _git(root, ["rev-parse", "HEAD"]).strip()
    print(f"[OK] Committed {sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
