#!/usr/bin/env python3
"""
Owl of Athena: Archive Management Agent
Lightweight agent for athena-index.md maintenance and archive operations
"""

import json
import sys
from pathlib import Path
from datetime import datetime
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
            return {"error": "progress.txt not found"}

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
            for i, line in enumerate(lines):
                if feature_id in line:
                    context = '\n'.join(lines[max(0, i - 2):i + 3]).lower()
                    if any(w in context for w in ['shipped', 'done', '✅', 'complete']):
                        return True
            return False  # feature_id in PRD but not marked shipped

        return True  # no PRD — trust tasks.md + spec.md


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

    parsed, _ = parser.parse_known_args()
    repo_root = Path(parsed.repo).resolve() if parsed.repo else Path.cwd()
    remaining = parsed.args

    if not remaining:
        print("Usage: owl.py [--repo PATH] <command> [args]")
        print("Commands:")
        print("  archive <feature-id>   - Move feature to archived")
        print("  retrieve <feature-id>  - Get feature summary")
        print("  search <keyword>       - Search archived features")
        print("  update-index           - Regenerate athena-index.md from specs (reads tasks.md)")
        print("  prune-done             - Remove closed feature sessions from progress.txt")
        print("  trim-progress          - Archive old progress.txt sessions (legacy)")
        sys.exit(1)

    owl = OwlOfAthena(repo_root)
    command = remaining[0]
    
    if command == "archive" and len(remaining) > 1:
        result = owl.archive_feature(remaining[1])
    elif command == "retrieve" and len(remaining) > 1:
        result = owl.retrieve_feature(remaining[1])
    elif command == "search" and len(remaining) > 1:
        result = owl.search_features(remaining[1])
    elif command == "update-index":
        result = owl.update_index()
    elif command == "prune-done":
        result = owl.prune_done()
    elif command == "trim-progress":
        result = owl.trim_progress()
    else:
        result = {"error": "Invalid command or missing arguments"}
    
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
