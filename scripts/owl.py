#!/usr/bin/env python3
"""
Owl of Athena: Archive Management Agent
Lightweight agent for athena-index.md maintenance and archive operations
"""

import json
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class OwlOfAthena:
    """Archive management agent for Athena"""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.docs_dir = repo_root / "docs"
        self.index_path = self.docs_dir / "athena-index.md"
        self.specs_dir = self.docs_dir / "specs"
    
    def archive_feature(self, feature_id: str) -> Dict:
        """Move feature from Active to Archived in athena-index.md and archive progress"""
        if not self.index_path.exists():
            return {"error": "athena-index.md not found"}
        
        # Read current INDEX
        content = self.index_path.read_text()
        
        # Check if feature exists in specs
        feature_path = self.specs_dir / feature_id
        if not feature_path.exists():
            return {"error": f"Feature {feature_id} not found in docs/specs/"}
        
        # Get feature metadata
        spec_file = feature_path / "spec.md"
        if not spec_file.exists():
            return {"error": f"spec.md not found for {feature_id}"}
        
        spec_content = spec_file.read_text()
        summary = self._extract_summary(spec_content)
        
        # Archive progress.txt entries for this feature
        progress_archived = self._archive_progress_entries(feature_id)
        
        # Update athena-index.md (move from Active to Archived)
        updated_content = self._move_to_archived(content, feature_id, summary)
        self.index_path.write_text(updated_content)
        
        return {
            "success": True,
            "feature_id": feature_id,
            "summary": summary,
            "progress_archived": progress_archived,
            "message": f"✅ Moved {feature_id} to archived in athena-index.md"
        }
    
    def _archive_progress_entries(self, feature_id: str) -> bool:
        """Archive progress.txt entries for completed feature"""
        progress_file = self.docs_dir / "progress.txt"
        if not progress_file.exists():
            return False
        
        content = progress_file.read_text()
        lines = content.split('\n')
        
        # Find entries related to this feature
        feature_lines = []
        current_session_lines = []
        in_feature_session = False
        
        for i, line in enumerate(lines):
            # Check if this session is for our feature
            if f"Feature: {feature_id}" in line:
                in_feature_session = True
            
            # Check for new session start
            if line.startswith("Session:") and i > 0:
                in_feature_session = False
            
            if in_feature_session:
                feature_lines.append(line)
            else:
                # Keep only the last session (current work)
                if line.startswith("Session:"):
                    current_session_lines = [line]
                elif current_session_lines:
                    current_session_lines.append(line)
        
        # If we found feature-specific entries, archive them
        if feature_lines:
            archive_file = self.docs_dir / "progress-archive.txt"
            feature_content = '\n'.join(feature_lines)
            if archive_file.exists():
                archive_file.write_text(archive_file.read_text() + '\n\n' + feature_content)
            else:
                archive_file.write_text(feature_content)
            
            # Update progress.txt to only keep current session
            if current_session_lines:
                progress_file.write_text('\n'.join(current_session_lines))
            
            return True
        
        return False
    
    def retrieve_feature(self, feature_id: str) -> Dict:
        """Retrieve archived feature summary"""
        # Check athena-index.md for feature
        if not self.index_path.exists():
            return {"error": "athena-index.md not found"}
        
        content = self.index_path.read_text()
        
        # Find feature in INDEX
        feature_info = self._find_in_index(content, feature_id)
        if not feature_info:
            return {"error": f"Feature {feature_id} not found in athena-index.md"}
        
        # Load spec if user needs more detail
        spec_file = self.specs_dir / feature_id / "spec.md"
        if spec_file.exists():
            spec_content = spec_file.read_text()
            summary = self._extract_summary(spec_content)
        else:
            summary = feature_info.get("summary", "No summary available")
        
        return {
            "success": True,
            "feature_id": feature_id,
            "status": feature_info.get("status", "Unknown"),
            "summary": summary,
            "spec_path": f"docs/specs/{feature_id}/spec.md"
        }
    
    def search_features(self, keyword: str) -> Dict:
        """Search archived features by keyword"""
        if not self.index_path.exists():
            return {"error": "athena-index.md not found"}
        
        content = self.index_path.read_text()
        matches = []
        
        # Search in athena-index.md
        lines = content.split('\n')
        current_feature = None
        
        for line in lines:
            if line.startswith('### '):
                current_feature = line.replace('### ', '').strip()
            elif keyword.lower() in line.lower() and current_feature:
                if current_feature not in [m['feature_id'] for m in matches]:
                    matches.append({
                        'feature_id': current_feature,
                        'match': line.strip()
                    })
        
        return {
            "success": True,
            "keyword": keyword,
            "matches": matches,
            "count": len(matches)
        }
    
    def trim_progress(self) -> Dict:
        """Keep only current session in progress.txt, archive the rest"""
        progress_file = self.docs_dir / "progress.txt"
        if not progress_file.exists():
            return {"error": "progress.txt not found"}
        
        content = progress_file.read_text()
        lines = content.split('\n')
        
        # Find the last session
        last_session_start = -1
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].startswith("Session:"):
                last_session_start = i
                break
        
        if last_session_start == -1:
            return {"error": "No session found in progress.txt"}
        
        # Archive old sessions
        old_sessions = '\n'.join(lines[:last_session_start])
        current_session = '\n'.join(lines[last_session_start:])
        
        if old_sessions.strip():
            # Save to archive
            archive_file = self.docs_dir / "progress-archive.txt"
            if archive_file.exists():
                archive_file.write_text(archive_file.read_text() + '\n\n' + old_sessions)
            else:
                archive_file.write_text(old_sessions)
            
            # Update progress.txt with only current session
            progress_file.write_text(current_session)
            
            old_lines = len(lines[:last_session_start])
            new_lines = len(lines[last_session_start:])
            tokens_saved = old_lines * 10  # Rough estimate
            
            return {
                "success": True,
                "old_sessions_archived": old_lines,
                "current_session_lines": new_lines,
                "tokens_saved": tokens_saved,
                "message": f"✅ Archived {old_lines} lines, kept {new_lines} lines"
            }
        
        return {
            "success": True,
            "message": "✅ progress.txt already minimal (only current session)"
        }

    def update_index(self) -> Dict:
        """Regenerate athena-index.md from current specs"""
        features = []
        
        # Scan all features in docs/specs/
        for feature_dir in sorted(self.specs_dir.iterdir()):
            if not feature_dir.is_dir():
                continue
            
            spec_file = feature_dir / "spec.md"
            if not spec_file.exists():
                continue
            
            spec_content = spec_file.read_text()
            status = self._extract_status(feature_dir)
            summary = self._extract_summary(spec_content)
            
            features.append({
                'id': feature_dir.name,
                'status': status,
                'summary': summary,
                'spec_path': f"docs/specs/{feature_dir.name}/spec.md"
            })
        
        # Generate new athena-index.md
        index_content = self._generate_index(features)
        self.index_path.write_text(index_content)
        
        active_count = sum(1 for f in features if f['status'] == 'Active')
        archived_count = len(features) - active_count
        
        return {
            "success": True,
            "total_features": len(features),
            "active": active_count,
            "archived": archived_count,
            "message": f"✅ Updated athena-index.md: {active_count} active, {archived_count} archived"
        }
    
    def _extract_status(self, feature_dir: Path) -> str:
        """Determine feature status: check tasks.md first, fall back to spec.md"""
        tasks_file = feature_dir / "tasks.md"
        if tasks_file.exists():
            return self._extract_status_from_tasks(tasks_file.read_text())
        spec_file = feature_dir / "spec.md"
        if spec_file.exists():
            return self._extract_status_from_spec(spec_file.read_text())
        return 'Done'

    def _extract_status_from_tasks(self, tasks_content: str) -> str:
        """Active if any real task exists under NEXT or IN PROGRESS sections"""
        in_active_section = False
        for line in tasks_content.split('\n'):
            if line.startswith('## NEXT') or line.startswith('## IN PROGRESS'):
                in_active_section = True
            elif line.startswith('## '):
                in_active_section = False
            elif in_active_section and line.strip().startswith('- '):
                task_text = line.strip()[2:].strip()
                if task_text and task_text.lower() not in ('(none)', 'none', ''):
                    return 'Active'
        return 'Done'

    def _extract_status_from_spec(self, spec_content: str) -> str:
        """Fall back: read Status: field from spec.md"""
        for line in spec_content.split('\n'):
            if 'Status:' in line or '**Status:**' in line:
                status = line.split('Status:')[-1].strip()
                status = status.replace('**', '').replace('*', '').strip()
                return 'Active' if status.lower() in ['active', 'in progress'] else 'Done'
        return 'Done'
    
    def _extract_summary(self, spec_content: str) -> str:
        """Extract summary from spec.md"""
        lines = spec_content.split('\n')
        for i, line in enumerate(lines):
            if '## Summary' in line and i + 1 < len(lines):
                summary = lines[i + 1].strip()
                if summary.startswith('-'):
                    summary = summary[1:].strip()
                return summary[:200]  # Limit length
        return "No summary available"
    
    def _find_in_index(self, content: str, feature_id: str) -> Optional[Dict]:
        """Find feature in athena-index.md"""
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if f"### {feature_id}" in line:
                # Extract info from next few lines
                info = {'feature_id': feature_id}
                for j in range(i + 1, min(i + 5, len(lines))):
                    if 'Status:' in lines[j]:
                        info['status'] = lines[j].split('Status:')[-1].strip()
                    if 'Summary:' in lines[j]:
                        info['summary'] = lines[j].split('Summary:')[-1].strip()
                return info
        return None
    
    def _move_to_archived(self, content: str, feature_id: str, summary: str) -> str:
        """Move feature from Active to Archived section by regenerating the index"""
        # Regenerate the full index from specs — this correctly places features
        # based on their actual Status field rather than doing brittle string surgery
        self.update_index()
        return self.index_path.read_text()
    
    def _generate_index(self, features: List[Dict]) -> str:
        """Generate athena-index.md content"""
        active = [f for f in features if f['status'] == 'Active']
        archived = [f for f in features if f['status'] != 'Active']
        
        content = f"""# Athena Feature Index

**Purpose**: Lightweight index to reduce token overhead by loading only active features.  
**Last updated**: {datetime.now().strftime('%Y-%m-%d')}

## How to Use This Index

**For Athena agents**: Load this athena-index.md first. Only load specs marked as "Active" below. Skip "Archived" features unless explicitly requested by user.

**For humans**: This index shows all features. Archived features are complete and should not be modified.

---

## Active Features (Load these during sessions)

"""
        
        if active:
            for f in active:
                content += f"""### {f['id']}
- **Status**: Active
- **Spec**: {f['spec_path']}
- **Summary**: {f['summary']}

"""
        else:
            content += "*No active features currently. All features are archived.*\n\n"
        
        content += """---

## Archived Features (Skip unless explicitly requested)

"""
        
        for f in archived:
            content += f"""### {f['id']}
- **Status**: Done
- **Spec**: {f['spec_path']}
- **Summary**: {f['summary']}

"""
        
        # Add token optimization section
        total_tokens = len(archived) * 500  # Rough estimate
        index_tokens = 1100
        savings = int((1 - index_tokens / total_tokens) * 100) if total_tokens > 0 else 0
        
        content += f"""---

## Token Optimization

**Without athena-index.md**:
- Load all {len(features)} specs = ~{total_tokens:,} tokens

**With athena-index.md**:
- Load athena-index.md only = ~{index_tokens} tokens
- Load {len(active)} active specs = ~{len(active) * 300} tokens
- **Total**: ~{index_tokens + len(active) * 300} tokens
- **Savings**: ~{savings}% reduction

**Usage Pattern**:
1. Athena loads athena-index.md first
2. Identifies active features (currently: {len(active)})
3. Skips {len(archived)} archived features
4. If user asks about archived feature, load on-demand
"""
        
        return content

    def prune_done(self) -> Dict:
        """Remove session blocks for fully-closed features from progress.txt.

        A feature is fully closed when ALL of:
          1. tasks.md has no items under NEXT or IN PROGRESS
          2. spec.md has Status: Done
          3. PRD.md marks the feature as shipped
        """
        progress_file = self.docs_dir / "progress.txt"
        prd_file = self.docs_dir / "PRD.md"
        if not progress_file.exists():
            return {"success": True, "skipped": True,
                    "message": "✅ progress.txt retired — per-feature notes need no pruning"}

        prd_content = prd_file.read_text() if prd_file.exists() else ""
        content = progress_file.read_text()

        # Split into session blocks (each starts with "Session:")
        blocks = []
        current = []
        for line in content.split('\n'):
            if line.startswith('Session:') and current:
                blocks.append('\n'.join(current))
                current = [line]
            else:
                current.append(line)
        if current:
            blocks.append('\n'.join(current))

        kept = []
        pruned = []
        pruned_features = []

        for block in blocks:
            feature_id = self._extract_feature_id(block)
            if feature_id and self._is_fully_closed(feature_id, prd_content):
                pruned_features.append(feature_id)
                pruned.append(block)
            else:
                kept.append(block)

        # Archive pruned blocks before removing from progress.txt
        if pruned:
            archive_file = self.docs_dir / "progress-archive.txt"
            archive_content = '\n\n'.join(pruned)
            if archive_file.exists():
                archive_file.write_text(archive_file.read_text() + '\n\n' + archive_content)
            else:
                archive_file.write_text(archive_content)

        progress_file.write_text('\n'.join(kept))
        return {
            "success": True,
            "pruned_features": list(dict.fromkeys(pruned_features)),  # deduplicate
            "blocks_removed": len(blocks) - len(kept),
            "message": f"✅ Pruned {len(blocks) - len(kept)} session block(s) for {len(set(pruned_features))} closed feature(s)"
        }

    def _extract_feature_id(self, block: str) -> Optional[str]:
        """Extract Feature: <id> from a session block"""
        for line in block.split('\n'):
            if line.startswith('Feature:'):
                return line.split('Feature:')[-1].strip()
        return None

    def _is_fully_closed(self, feature_id: str, prd_content: str) -> bool:
        """True if feature is Done in tasks.md, spec.md, AND PRD.md"""
        feature_dir = self.specs_dir / feature_id
        if not feature_dir.exists():
            return False

        # 1. tasks.md check (ground truth)
        if self._extract_status(feature_dir) == 'Active':
            return False

        # 2. spec.md check
        spec_file = feature_dir / "spec.md"
        if spec_file.exists():
            if self._extract_status_from_spec(spec_file.read_text()) != 'Done':
                return False

        # 3. PRD.md check — feature-id appears near a shipped/done indicator
        if prd_content:
            lines = prd_content.split('\n')
            found_in_prd = False
            for i, line in enumerate(lines):
                if feature_id in line:
                    found_in_prd = True
                    context = '\n'.join(lines[max(0, i - 2):i + 3]).lower()
                    if any(w in context for w in ['shipped', 'done', '✅', 'complete']):
                        return True
            if found_in_prd:
                return False  # found in PRD but not yet marked shipped

        return True  # not in PRD (or no PRD) — trust tasks.md + spec.md

    # --- Memory bridge helpers ---

    def _parse_progress(self, progress_file: Path) -> Dict:
        """Parse the most recent session block from progress.txt.

        Returns dict with keys: feature_id, goal, in_progress (list), next_tasks (list).
        """
        content = progress_file.read_text(encoding="utf-8")
        lines = content.split("\n")

        # Locate last session block
        last_session_start = -1
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].startswith("Session:"):
                last_session_start = i
                break

        if last_session_start == -1:
            return {}

        result: Dict = {"feature_id": "", "goal": "", "in_progress": [], "next_tasks": []}
        section = None

        for line in lines[last_session_start:]:
            stripped = line.strip()
            if line.startswith("Feature:"):
                result["feature_id"] = line.split("Feature:", 1)[-1].strip()
            elif line.startswith("Goal:"):
                result["goal"] = line.split("Goal:", 1)[-1].strip()
            elif stripped == "IN PROGRESS":
                section = "in_progress"
                continue
            elif stripped == "NEXT":
                section = "next_tasks"
                continue
            elif stripped in ("DONE", "NOTES") or (line.startswith("Session:") and line != lines[last_session_start]):
                section = None
                continue
            if section in ("in_progress", "next_tasks") and stripped.startswith("- "):
                task_text = stripped[2:].strip()
                if task_text and task_text.lower() not in ("(none)", "none"):
                    result[section].append(task_text)

        return result

    def _extract_active_features(self) -> List[str]:
        """Return list of active feature IDs from athena-index.md."""
        if not self.index_path.exists():
            return []
        active: List[str] = []
        in_active_section = False
        for line in self.index_path.read_text(encoding="utf-8").split("\n"):
            if line.startswith("## Active Features"):
                in_active_section = True
                continue
            if line.startswith("## ") and in_active_section:
                break
            if in_active_section and line.startswith("### "):
                fid = line.replace("### ", "").strip()
                if fid:
                    active.append(fid)
        return active

    def _upsert_memory_index(self, memory_index: Path, entry_filename: str,
                              entry_title: str, entry_hook: str) -> None:
        """Idempotently add or replace an entry in MEMORY.md."""
        new_line = f"- [{entry_title}]({entry_filename}) — {entry_hook}"
        if not memory_index.exists():
            memory_index.write_text(f"# Memory Index\n\n{new_line}\n", encoding="utf-8")
            return
        existing = memory_index.read_text(encoding="utf-8")
        lines = existing.split("\n")
        updated = []
        found = False
        for line in lines:
            if f"]({entry_filename})" in line:
                updated.append(new_line)
                found = True
            else:
                updated.append(line)
        if found:
            memory_index.write_text("\n".join(updated), encoding="utf-8")
        else:
            memory_index.write_text(existing.rstrip("\n") + "\n" + new_line + "\n", encoding="utf-8")

    def write_memory(self) -> Dict:
        """Write project_athena_active.md to Claude Code memory dir.

        Memory path: ~/.claude/projects/<encoded-repo-path>/memory/
        Encoded = repo absolute path with all '/' replaced by '-'.

        Idempotent: skips write if memory file is newer than progress.txt.
        Silently skips if memory dir does not exist (not initialized).
        """
        progress_file = self.docs_dir / "progress.txt"

        # Compute memory directory
        encoded = str(self.repo_root.resolve()).replace("/", "-")
        memory_dir = Path.home() / ".claude" / "projects" / encoded / "memory"

        if not memory_dir.exists():
            return {"success": True, "skipped": True,
                    "message": "memory not initialized — skipping"}

        memory_file = memory_dir / "project_athena_active.md"
        memory_index = memory_dir / "MEMORY.md"

        # Legacy layout only: skip if memory is already newer than progress.txt.
        # In the notes-based layout the sources are many small files, so we
        # always rewrite (cheap and idempotent).
        if (progress_file.exists() and memory_file.exists()
                and memory_file.stat().st_mtime > progress_file.stat().st_mtime):
            return {"success": True, "skipped": True,
                    "message": "memory file is newer than progress.txt — no update needed"}

        context = self._active_context()
        active_features = context["active_features"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        feature_id = context.get("feature_id", "")
        goal = context.get("goal", "")
        in_progress = context.get("in_progress", [])
        next_tasks = context.get("next_tasks", [])

        def fmt(items: List[str]) -> str:
            return "\n".join(f"  - {t}" for t in items) if items else "  (none)"

        feature_line = (f"Active feature: {feature_id}. Goal: {goal}."
                        if feature_id else "No active feature.")

        content = f"""---
name: Athena Active Context
description: Current active feature, goal, and task state — written by Owl at session start
type: project
---

{feature_line}

**Why:** {goal if goal else 'See the active feature docs for session context.'}
**How to apply:** Use this context directly — do not read athena-index.md or the docs/ logs. Load only the active spec(s) listed below; access requests/decisions via ./scripts/owl.

**Active features:**
{fmt(active_features)}
**IN PROGRESS:**
{fmt(in_progress)}
**NEXT:**
{fmt(next_tasks)}
**Last updated:** {timestamp}
"""
        memory_file.write_text(content, encoding="utf-8")
        self._upsert_memory_index(
            memory_index,
            entry_filename="project_athena_active.md",
            entry_title="Athena Active Context",
            entry_hook="active feature, goal, and task state for the current session",
        )

        return {
            "success": True,
            "memory_file": str(memory_file),
            "feature_id": feature_id or "(none)",
            "active_features": len(active_features),
            "message": f"✅ Wrote memory: {feature_id or 'no active feature'}, {len(active_features)} active feature(s)"
        }

    # --- Script-gated KB access (token-diet layout) ---
    #
    # New layout: task truth in docs/specs/<id>/tasks.md, session notes in
    # docs/specs/<id>/notes.md, no docs/progress.txt. All commands fall back
    # to progress.txt when the repo has not run `owl migrate` yet.

    def _scan_active_features(self) -> List[str]:
        """Active feature IDs derived directly from specs (index may be stale)."""
        if not self.specs_dir.exists():
            return []
        return [d.name for d in sorted(self.specs_dir.iterdir())
                if d.is_dir() and (d / "spec.md").exists()
                and self._extract_status(d) == 'Active']

    def _parse_tasks(self, tasks_file: Path) -> Dict:
        """Parse IN PROGRESS / NEXT task lists from a tasks.md file."""
        result: Dict = {"in_progress": [], "next_tasks": []}
        if not tasks_file.exists():
            return result
        section = None
        for line in tasks_file.read_text(encoding="utf-8").split("\n"):
            if line.startswith("## IN PROGRESS"):
                section = "in_progress"
                continue
            if line.startswith("## NEXT"):
                section = "next_tasks"
                continue
            if line.startswith("## "):
                section = None
                continue
            stripped = line.strip()
            if section and stripped.startswith("- "):
                task = stripped[2:].strip()
                if task and task.lower() not in ("(none)", "none"):
                    result[section].append(task)
        return result

    def _latest_note_meta(self, feature_id: str) -> Dict:
        """Timestamp + Goal of the latest session block in a feature's notes.md."""
        result = {"timestamp": "", "goal": ""}
        notes = self.specs_dir / feature_id / "notes.md"
        if not notes.exists():
            return result
        lines = notes.read_text(encoding="utf-8").split("\n")
        last = -1
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].startswith("## S-"):
                last = i
                break
        if last == -1:
            return result
        result["timestamp"] = lines[last][len("## S-"):].strip()
        for line in lines[last:]:
            if line.startswith("Goal:"):
                result["goal"] = line.split("Goal:", 1)[-1].strip()
                break
        return result

    def _current_feature(self, active: List[str]) -> str:
        """Most recently worked active feature (newest note, then tasks.md mtime)."""
        if not active:
            return ""
        if len(active) == 1:
            return active[0]

        def sort_key(fid: str):
            ts = self._latest_note_meta(fid)["timestamp"]  # S-IDs sort lexically
            tasks = self.specs_dir / fid / "tasks.md"
            mtime = tasks.stat().st_mtime if tasks.exists() else 0
            return (ts, mtime)

        return sorted(active, key=sort_key, reverse=True)[0]

    def _active_context(self) -> Dict:
        """Shared context source for `context` and `write-memory` (both layouts)."""
        progress_file = self.docs_dir / "progress.txt"
        active = self._scan_active_features()
        ctx: Dict = {"active_features": active, "feature_id": "", "goal": "",
                     "in_progress": [], "next_tasks": []}

        if progress_file.exists():  # legacy layout
            legacy = self._parse_progress(progress_file)
            ctx["feature_id"] = legacy.get("feature_id") or self._current_feature(active)
            ctx["goal"] = legacy.get("goal", "")
            ctx["in_progress"] = legacy.get("in_progress", [])
            ctx["next_tasks"] = legacy.get("next_tasks", [])
            return ctx

        feature = self._current_feature(active)
        ctx["feature_id"] = feature
        if feature:
            meta = self._latest_note_meta(feature)
            spec_file = self.specs_dir / feature / "spec.md"
            spec_summary = (self._extract_summary(spec_file.read_text())
                            if spec_file.exists() else "")
            ctx["goal"] = meta["goal"] or spec_summary
            tasks = self._parse_tasks(self.specs_dir / feature / "tasks.md")
            ctx["in_progress"] = tasks["in_progress"]
            ctx["next_tasks"] = tasks["next_tasks"]
        return ctx

    def _recent_entry_ids(self, log_file: Path, prefix: str, count: int = 3) -> List[str]:
        """Last N entry IDs (## CR-... / ## D-... headings) from a log."""
        if not log_file.exists():
            return []
        ids = [line[3:].strip() for line in log_file.read_text(encoding="utf-8").split("\n")
               if line.startswith(f"## {prefix}")]
        return ids[-count:]

    def _latest_request_verbatim(self, max_chars: int = 500) -> str:
        """Verbatim body of the newest CR entry, truncated."""
        req = self.docs_dir / "requests.md"
        if not req.exists():
            return ""
        lines = req.read_text(encoding="utf-8").split("\n")
        last = -1
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].startswith("## CR-"):
                last = i
                break
        if last == -1:
            return ""
        body: List[str] = []
        in_verbatim = False
        for line in lines[last:]:
            low = line.strip().lower()
            if "request (verbatim)" in low:
                in_verbatim = True
                continue
            if in_verbatim:
                if line.startswith("### ") or low.startswith("notes:"):
                    break
                body.append(line)
        text = "\n".join(body).strip()
        return text[:max_chars] + ("…" if len(text) > max_chars else "")

    def _recovery_fields(self, feature_id: str) -> List[str]:
        """Latest note only: recorded state is not current authority or live process state."""
        fields = {"Authorization": "unknown", "Pending processes": "unknown",
                  "Verification": "unknown"}
        source = "none"
        if feature_id:
            notes = self.specs_dir / feature_id / "notes.md"
            if notes.exists():
                in_note = False
                for line in notes.read_text(encoding="utf-8").splitlines():
                    if line.startswith("## "):
                        in_note = line.startswith("## S-")
                        source = line[3:].strip() if in_note else "none"
                        fields = dict.fromkeys(fields, "unknown")
                    elif in_note:
                        for label in fields:
                            prefix = f"- {label}:"
                            if line.startswith(prefix):
                                value = line[len(prefix):].strip() or "unknown"
                                fields[label] = value[:500] + (" [truncated]" if len(value) > 500 else "")
        return [f"Recorded recovery state (note: {source}; revalidate before acting):"] + [
            f"  {key}: {value}" for key, value in fields.items()]

    def _git_recovery_state(self) -> List[str]:
        """Read-only Git snapshot; avoid optional index locks on status."""
        def git(*args):
            result = subprocess.run(
                ["git", "--no-optional-locks", *args], cwd=self.repo_root,
                capture_output=True, text=True, timeout=10)
            if result.returncode:
                raise RuntimeError("Git state unavailable")
            return result.stdout.rstrip("\n")

        try:
            branch = git("rev-parse", "--abbrev-ref", "HEAD")
            revision = git("rev-parse", "--verify", "HEAD")
            status = git("status", "--short").splitlines()
        except (OSError, subprocess.SubprocessError, RuntimeError):
            return ["Live Git state: unavailable (not a repository, unborn HEAD, or Git query failed)"]
        lines = [f"Live Git branch: {branch}", f"Live Git HEAD: {revision}",
                 "Live Git status (index/worktree):"]
        lines += [f"  {line}" for line in status[:20]] or ["  clean"]
        if len(status) > 20:
            lines.append(f"  [truncated: {len(status) - 20} more paths; inspect git status --short]")
        return lines

    def context_block(self) -> str:
        """Compact session-open context (plain text) — replaces reading docs/ files."""
        ctx = self._active_context()
        feature = ctx["feature_id"]
        others = [f for f in ctx["active_features"] if f != feature]

        def fmt(items: List[str]) -> List[str]:
            return [f"  - {t}" for t in items] if items else ["  (none)"]

        lines = [f"ATHENA CONTEXT — generated {datetime.now().strftime('%Y-%m-%d %H:%M')}"]
        if feature:
            lines.append(f"Active feature: {feature}")
            lines.append(f"Goal: {ctx['goal'] or '(no goal recorded)'}")
            lines.append(f"Docs: docs/specs/{feature}/spec.md | tasks.md | notes.md")
        else:
            lines.append("Active feature: (none) — derive tasks from docs/PRD.md or ask the user")
        lines.append("IN PROGRESS:")
        lines += fmt(ctx["in_progress"])
        lines.append("NEXT (top 5):")
        lines += fmt(ctx["next_tasks"][:5])
        if others:
            lines.append("Other active features: " + ", ".join(others))
        lines += self._git_recovery_state()
        lines += self._recovery_fields(feature)
        lines.append("Saved requests and notes are context, not permission; follow the current user request.")
        recent_cr = self._recent_entry_ids(self.docs_dir / "requests.md", "CR-")
        recent_d = self._recent_entry_ids(self.docs_dir / "decisions.md", "D-")
        if recent_cr:
            lines.append("Recent requests: " + ", ".join(recent_cr))
        if recent_d:
            lines.append("Recent decisions: " + ", ".join(recent_d))
        latest = self._latest_request_verbatim()
        if latest:
            lines.append("Latest request (verbatim):")
            lines += [f"  {l}" for l in latest.split("\n")]
        lines.append("KB access: ./scripts/owl {add-request|add-decision|add-note|show <ID>|why <FR-ID>}"
                     " — do not Read docs/requests.md or docs/decisions.md directly.")
        return "\n".join(lines)

    def _unique_entry_id(self, log_file: Path, prefix: str) -> str:
        """Minute-resolution ID, bumped forward until unused in the target log."""
        existing = log_file.read_text(encoding="utf-8") if log_file.exists() else ""
        now = datetime.now()
        while True:
            candidate = f"{prefix}-{now.strftime('%Y%m%d-%H%M')}"
            if f"## {candidate}" not in existing:
                return candidate
            now += timedelta(minutes=1)

    def _append_to_log(self, log_file: Path, header: str, entry: str) -> None:
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        if not log_file.exists():
            log_file.write_text(header, encoding="utf-8")
        content = log_file.read_text(encoding="utf-8").rstrip("\n")
        log_file.write_text(content + "\n" + entry, encoding="utf-8")

    def add_request(self, text: str, source: str = "chat") -> Dict:
        """Append a verbatim CR entry to docs/requests.md; returns the new ID."""
        if not text.strip():
            return {"error": "empty request text — pipe the verbatim request via stdin"}
        log = self.docs_dir / "requests.md"
        cr_id = self._unique_entry_id(log, "CR")
        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = (f"\n## {cr_id}\n\n### Metadata\n- **Date:** {ts}\n- **Source:** {source}\n\n"
                 f"### Request (verbatim):\n{text.strip()}\n")
        self._append_to_log(log, "# Customer Requests (append-only)\n", entry)
        return {"success": True, "id": cr_id,
                "message": f"✅ Appended {cr_id} to docs/requests.md"}

    def add_decision(self, text: str, cr: str, prd: str = "") -> Dict:
        """Append a D entry to docs/decisions.md; returns the new ID."""
        if not text.strip():
            return {"error": "empty decision text — pipe the decision via stdin"}
        if not cr or not cr.startswith("CR-"):
            return {"error": "--cr CR-YYYYMMDD-HHMM is required (comma-separate multiples)"}
        log = self.docs_dir / "decisions.md"
        d_id = self._unique_entry_id(log, "D")
        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = (f"\n## {d_id}\nDate: {ts}\nInputs: {cr}\nPRD: {prd or '(n/a)'}\n\n"
                 f"{text.strip()}\n")
        self._append_to_log(log, "# Decisions (append-only)\n", entry)
        return {"success": True, "id": d_id,
                "message": f"✅ Appended {d_id} to docs/decisions.md"}

    def add_note(self, feature_id: str, text: str, goal: str = "", agent: str = "",
                 model: str = "", skills: str = "") -> Dict:
        """Append a timestamped session block to docs/specs/<id>/notes.md."""
        if not feature_id:
            return {"error": "--feature <feature-id> is required"}
        if not text.strip():
            return {"error": "empty note text — pipe session notes via stdin"}
        feature_dir = self.specs_dir / feature_id
        if not feature_dir.is_dir():
            return {"error": f"Feature {feature_id} not found in docs/specs/"}
        notes = feature_dir / "notes.md"
        if not notes.exists():
            notes.write_text(f"# Session Notes: {feature_id} (append-only)\n",
                             encoding="utf-8")
        s_id = f"S-{datetime.now().strftime('%Y%m%d-%H%M')}"
        header = [f"\n## {s_id}"]
        for label, value in (("Agent", agent), ("Model", model),
                             ("Skills", skills), ("Goal", goal)):
            if value:
                header.append(f"{label}: {value}")
        entry = "\n".join(header) + "\n\n" + text.strip() + "\n"
        content = notes.read_text(encoding="utf-8").rstrip("\n")
        notes.write_text(content + "\n" + entry, encoding="utf-8")
        return {"success": True, "id": s_id,
                "file": f"docs/specs/{feature_id}/notes.md",
                "message": f"✅ Appended {s_id} to docs/specs/{feature_id}/notes.md"}

    def _extract_log_entry(self, log_file: Path, entry_id: str) -> str:
        """One entry block (## <id> … next ## heading) from an append-only log."""
        if not log_file.exists():
            return ""
        lines = log_file.read_text(encoding="utf-8").split("\n")
        block: List[str] = []
        capturing = False
        for line in lines:
            if line.startswith(f"## {entry_id}"):
                capturing = True
            elif capturing and line.startswith("## "):
                break
            if capturing:
                block.append(line)
        return "\n".join(block).strip()

    def show_entry(self, entry_id: str) -> str:
        """Print exactly one KB entry: CR/D from logs, FR from spec files."""
        if entry_id.startswith("CR-"):
            block = self._extract_log_entry(self.docs_dir / "requests.md", entry_id)
            return block or f"(not found: {entry_id} in docs/requests.md)"
        if entry_id.startswith("D-"):
            block = self._extract_log_entry(self.docs_dir / "decisions.md", entry_id)
            return block or f"(not found: {entry_id} in docs/decisions.md)"
        if entry_id.startswith("FR-"):
            matches: List[str] = []
            for spec in sorted(self.specs_dir.glob("*/spec.md")):
                for line in spec.read_text(encoding="utf-8").split("\n"):
                    if re.search(rf"\b{re.escape(entry_id)}\b", line):
                        matches.append(f"[{spec.parent.name}] {line.strip()}")
            return "\n".join(matches) or f"(not found: {entry_id} in docs/specs/*/spec.md)"
        return f"(unsupported ID: {entry_id} — expected CR-…, D-…, or FR-…)"

    def why(self, fr_id: str) -> str:
        """Traceability chain: FR line → Sources IDs → implementing tasks → commits."""
        if not fr_id.startswith("FR-"):
            return f"(unsupported ID: {fr_id} — expected FR-…)"
        out: List[str] = []
        for spec in sorted(self.specs_dir.glob("*/spec.md")):
            fid = spec.parent.name
            fr_lines = [l.strip() for l in spec.read_text(encoding="utf-8").split("\n")
                        if re.search(rf"\b{re.escape(fr_id)}\b:", l)]
            if not fr_lines:
                continue
            out.append(f"[{fid}]")
            source_ids: List[str] = []
            for line in fr_lines:
                out.append(f"  {line}")
                source_ids += re.findall(r"(?:CR|D)-\d{8}-\d{4}", line)
            if source_ids:
                out.append("  Sources (full text via `owl show <ID>`): "
                           + ", ".join(dict.fromkeys(source_ids)))
            task_ids: List[str] = []
            tasks_file = spec.parent / "tasks.md"
            if tasks_file.exists():
                for line in tasks_file.read_text(encoding="utf-8").split("\n"):
                    if fr_id in line and "Implements" in line:
                        out.append(f"  {line.strip()}")
                        task_ids += re.findall(r"\bT-\d{3}\b", line)
            # Task IDs repeat across features (every feature has a T-001), so
            # commits must match both the task ID and the feature ID.
            greps = [["--all-match", f"--grep={t}", f"--grep={fid}"]
                     for t in list(dict.fromkeys(task_ids))[:5]] + [[f"--grep={fid}"]]
            for grep_args in greps:
                try:
                    result = subprocess.run(
                        ["git", "log", "--oneline", "-5"] + grep_args,
                        capture_output=True, text=True, cwd=self.repo_root, timeout=10)
                    for commit in result.stdout.strip().split("\n"):
                        if commit and f"  commit {commit}" not in out:
                            out.append(f"  commit {commit}")
                except (subprocess.SubprocessError, OSError):
                    break
        if not out:
            return f"(not found: {fr_id} in docs/specs/*/spec.md)"
        if not any(l.startswith("  commit") for l in out):
            out.append("  (no commits found)")
        return "\n".join(out)

    def migrate(self) -> Dict:
        """Convert progress.txt to per-feature notes.md + docs/audit/progress-legacy.txt."""
        progress_file = self.docs_dir / "progress.txt"
        if not progress_file.exists():
            return {"success": True, "skipped": True,
                    "message": "no progress.txt — already migrated"}

        content = progress_file.read_text(encoding="utf-8")
        blocks: List[str] = []
        current: List[str] = []
        for line in content.split("\n"):
            if line.startswith("Session:") and current:
                blocks.append("\n".join(current))
                current = [line]
            else:
                current.append(line)
        if current:
            blocks.append("\n".join(current))

        migrated = 0
        legacy = 0
        for block in blocks:
            if not block.strip():
                continue
            feature_id = self._extract_feature_id(block)
            if feature_id and (self.specs_dir / feature_id).exists():
                notes = self.specs_dir / feature_id / "notes.md"
                if not notes.exists():
                    notes.write_text(f"# Session Notes: {feature_id} (append-only)\n",
                                     encoding="utf-8")
                converted = self._session_block_to_note(block)
                existing = notes.read_text(encoding="utf-8").rstrip("\n")
                notes.write_text(existing + "\n\n" + converted + "\n", encoding="utf-8")
                migrated += 1
            else:
                audit_dir = self.docs_dir / "audit"
                audit_dir.mkdir(parents=True, exist_ok=True)
                legacy_file = audit_dir / "progress-legacy.txt"
                existing = (legacy_file.read_text(encoding="utf-8").rstrip("\n") + "\n\n"
                            if legacy_file.exists() else "")
                legacy_file.write_text(existing + block.strip() + "\n", encoding="utf-8")
                legacy += 1

        progress_file.unlink()
        return {
            "success": True,
            "sessions_migrated": migrated,
            "sessions_to_legacy": legacy,
            "message": (f"✅ Migrated {migrated} session block(s) to per-feature notes.md, "
                        f"{legacy} block(s) to docs/audit/progress-legacy.txt; "
                        "removed docs/progress.txt")
        }

    def prune_prd(self) -> Dict:
        """Archive PRD link ceremony and closed backlog lines to docs/audit/prd-archive.md.

        Moves: (1) Metadata `- **Inputs:**` / `- **Decisions:**` link lists,
        (2) backlog lines marked Shipped/Implemented/Planned that do not cite
        an active feature. Requirements (Goals/FRs) are never touched.
        """
        prd_file = self.docs_dir / "PRD.md"
        if not prd_file.exists():
            return {"error": "PRD.md not found"}

        active = self._scan_active_features()
        lines = prd_file.read_text(encoding="utf-8").split("\n")
        kept: List[str] = []
        archived: List[str] = []
        in_backlog = False

        for line in lines:
            stripped = line.strip()
            if (stripped.startswith("- **Inputs:**") or stripped.startswith("- **Decisions:**")) \
                    and stripped.count("](") >= 3:
                label = "Inputs" if stripped.startswith("- **Inputs:**") else "Decisions"
                archived.append(line)
                kept.append(f"- **{label}:** see docs/audit/prd-archive.md")
                continue
            if line.startswith("## "):
                in_backlog = line.startswith("## Next / backlog")
            if in_backlog and re.match(r"-\s*(Shipped|Implemented|Planned)", stripped):
                if not any(feature in line for feature in active):
                    archived.append(line)
                    continue
            kept.append(line)

        if not archived:
            return {"success": True, "skipped": True,
                    "message": "✅ PRD already lean — nothing to prune"}

        archive_file = self.docs_dir / "audit" / "prd-archive.md"
        archive_file.parent.mkdir(parents=True, exist_ok=True)
        existing = (archive_file.read_text(encoding="utf-8").rstrip("\n") + "\n"
                    if archive_file.exists()
                    else "# PRD Archive (pruned by owl prune-prd)\n")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        archive_file.write_text(
            existing + f"\n## Pruned {timestamp}\n" + "\n".join(archived) + "\n",
            encoding="utf-8")
        prd_file.write_text("\n".join(kept), encoding="utf-8")
        saved = sum(len(l) + 1 for l in archived)
        return {
            "success": True,
            "lines_archived": len(archived),
            "bytes_archived": saved,
            "message": (f"✅ Pruned {len(archived)} PRD line(s) (~{saved} B) "
                        "to docs/audit/prd-archive.md")
        }

    def _session_block_to_note(self, block: str) -> str:
        """Rewrite a progress.txt session block as a notes.md `## S-…` entry."""
        lines = block.strip().split("\n")
        first = lines[0]
        match = re.match(r"Session:\s*(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2})", first)
        if match:
            y, mo, d, h, mi = match.groups()
            heading = f"## S-{y}{mo}{d}-{h}{mi}"
            rest = lines[1:]
        else:
            heading = f"## S-migrated"
            rest = lines
        return heading + "\n" + "\n".join(rest)


def _parse_cli_flags(argv: List[str]):
    """Split a command's argv tail into ({--flag: value}, [positionals])."""
    flags: Dict = {}
    positionals: List[str] = []
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg.startswith("--"):
            key = arg[2:]
            if i + 1 < len(argv) and not argv[i + 1].startswith("--"):
                flags[key] = argv[i + 1]
                i += 2
            else:
                flags[key] = True
                i += 1
        else:
            positionals.append(arg)
            i += 1
    return flags, positionals


def _read_stdin_text(flags: Dict) -> str:
    """Entry body from --text or piped stdin (never blocks on a TTY)."""
    if isinstance(flags.get("text"), str):
        return flags["text"]
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return ""


def main():
    """CLI interface for Owl of Athena"""
    import argparse as _argparse

    parser = _argparse.ArgumentParser(
        prog="owl.py",
        description="Owl of Athena: archive management for the ATHENA traceability system",
        add_help=False,
    )
    parser.add_argument(
        "--repo",
        default=None,
        help="Repo root path (default: current working directory). "
             "Supported for compatibility with older wrapper scripts.",
    )
    # Capture the rest as positional args so legacy callers still work
    parser.add_argument("args", nargs="*")

    parsed, unknown = parser.parse_known_args()
    repo_root = Path(parsed.repo).resolve() if parsed.repo else Path.cwd()
    remaining = parsed.args + unknown

    if not remaining:
        print("Usage: owl.py [--repo PATH] <command> [args]")
        print("Session:")
        print("  context                          - Print compact session-open context (plain text)")
        print("  write-memory                     - Write Claude Code memory file with active context")
        print("Append (body via stdin or --text):")
        print("  add-request [--source s]         - Append verbatim CR entry, returns ID")
        print("  add-decision --cr CR-... [--prd section]")
        print("  add-note --feature <id> [--goal g] [--agent a] [--model m] [--skills s]")
        print("Query:")
        print("  show <CR-...|D-...|FR-...>       - Print exactly one entry")
        print("  why <FR-...>                     - Print traceability chain incl. commits")
        print("  retrieve <feature-id>            - Get feature summary")
        print("  search <keyword>                 - Search archived features")
        print("Maintenance:")
        print("  archive <feature-id>             - Move feature to archived")
        print("  update-index                     - Regenerate athena-index.md from specs")
        print("  migrate                          - Convert progress.txt to per-feature notes.md")
        print("  prune-prd                        - Archive PRD link lists + closed backlog lines")
        print("  prune-done                       - Legacy: prune closed sessions from progress.txt")
        print("  trim-progress                    - Legacy: archive old progress.txt sessions")
        sys.exit(1)

    owl = OwlOfAthena(repo_root)
    command = remaining[0]
    flags, positionals = _parse_cli_flags(remaining[1:])

    # Plain-text commands (agent-facing output, not JSON)
    if command == "context":
        print(owl.context_block())
        return
    if command == "show" and positionals:
        print(owl.show_entry(positionals[0]))
        return
    if command == "why" and positionals:
        print(owl.why(positionals[0]))
        return

    if command == "archive" and positionals:
        result = owl.archive_feature(positionals[0])
    elif command == "retrieve" and positionals:
        result = owl.retrieve_feature(positionals[0])
    elif command == "search" and positionals:
        result = owl.search_features(positionals[0])
    elif command == "add-request":
        result = owl.add_request(_read_stdin_text(flags),
                                 source=flags.get("source", "chat"))
    elif command == "add-decision":
        result = owl.add_decision(_read_stdin_text(flags),
                                  cr=str(flags.get("cr", "")),
                                  prd=str(flags.get("prd", "") or ""))
    elif command == "add-note":
        result = owl.add_note(str(flags.get("feature", "")),
                              _read_stdin_text(flags),
                              goal=str(flags.get("goal", "") or ""),
                              agent=str(flags.get("agent", "") or ""),
                              model=str(flags.get("model", "") or ""),
                              skills=str(flags.get("skills", "") or ""))
    elif command == "migrate":
        result = owl.migrate()
    elif command == "prune-prd":
        result = owl.prune_prd()
    elif command == "update-index":
        result = owl.update_index()
    elif command == "prune-done":
        result = owl.prune_done()
    elif command == "trim-progress":
        result = owl.trim_progress()
    elif command == "write-memory":
        result = owl.write_memory()
    else:
        result = {"error": "Invalid command or missing arguments"}

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
