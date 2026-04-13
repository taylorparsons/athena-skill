#!/usr/bin/env python3
"""
Owl of Athena: Archive Management Agent
Lightweight agent for INDEX.md maintenance and archive operations
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
        self.index_path = self.docs_dir / "INDEX.md"
        self.specs_dir = self.docs_dir / "specs"
    
    def archive_feature(self, feature_id: str) -> Dict:
        """Move feature from Active to Archived in INDEX.md"""
        if not self.index_path.exists():
            return {"error": "INDEX.md not found"}
        
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
        
        # Update INDEX.md (move from Active to Archived)
        updated_content = self._move_to_archived(content, feature_id, summary)
        self.index_path.write_text(updated_content)
        
        return {
            "success": True,
            "feature_id": feature_id,
            "summary": summary,
            "message": f"✅ Moved {feature_id} to archived in INDEX.md"
        }
    
    def retrieve_feature(self, feature_id: str) -> Dict:
        """Retrieve archived feature summary"""
        # Check INDEX.md for feature
        if not self.index_path.exists():
            return {"error": "INDEX.md not found"}
        
        content = self.index_path.read_text()
        
        # Find feature in INDEX
        feature_info = self._find_in_index(content, feature_id)
        if not feature_info:
            return {"error": f"Feature {feature_id} not found in INDEX.md"}
        
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
            return {"error": "INDEX.md not found"}
        
        content = self.index_path.read_text()
        matches = []
        
        # Search in INDEX.md
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
    
    def update_index(self) -> Dict:
        """Regenerate INDEX.md from current specs"""
        features = []
        
        # Scan all features in docs/specs/
        for feature_dir in sorted(self.specs_dir.iterdir()):
            if not feature_dir.is_dir():
                continue
            
            spec_file = feature_dir / "spec.md"
            if not spec_file.exists():
                continue
            
            spec_content = spec_file.read_text()
            status = self._extract_status(spec_content)
            summary = self._extract_summary(spec_content)
            
            features.append({
                'id': feature_dir.name,
                'status': status,
                'summary': summary,
                'spec_path': f"docs/specs/{feature_dir.name}/spec.md"
            })
        
        # Generate new INDEX.md
        index_content = self._generate_index(features)
        self.index_path.write_text(index_content)
        
        active_count = sum(1 for f in features if f['status'] == 'Active')
        archived_count = len(features) - active_count
        
        return {
            "success": True,
            "total_features": len(features),
            "active": active_count,
            "archived": archived_count,
            "message": f"✅ Updated INDEX.md: {active_count} active, {archived_count} archived"
        }
    
    def _extract_status(self, spec_content: str) -> str:
        """Extract status from spec.md"""
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
        """Find feature in INDEX.md"""
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
        """Move feature from Active to Archived section"""
        # Simple implementation: just update the status line
        # In production, would do more sophisticated section moving
        return content.replace(
            f"### {feature_id}",
            f"### {feature_id}\n- **Status**: Done ({datetime.now().strftime('%Y-%m-%d')})"
        )
    
    def _generate_index(self, features: List[Dict]) -> str:
        """Generate INDEX.md content"""
        active = [f for f in features if f['status'] == 'Active']
        archived = [f for f in features if f['status'] != 'Active']
        
        content = f"""# Athena Feature Index

**Purpose**: Lightweight index to reduce token overhead by loading only active features.  
**Last updated**: {datetime.now().strftime('%Y-%m-%d')}

## How to Use This Index

**For Athena agents**: Load this INDEX.md first. Only load specs marked as "Active" below. Skip "Archived" features unless explicitly requested by user.

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

**Without INDEX.md**:
- Load all {len(features)} specs = ~{total_tokens:,} tokens

**With INDEX.md**:
- Load INDEX.md only = ~{index_tokens} tokens
- Load {len(active)} active specs = ~{len(active) * 300} tokens
- **Total**: ~{index_tokens + len(active) * 300} tokens
- **Savings**: ~{savings}% reduction

**Usage Pattern**:
1. Athena loads INDEX.md first
2. Identifies active features (currently: {len(active)})
3. Skips {len(archived)} archived features
4. If user asks about archived feature, load on-demand
"""
        
        return content


def main():
    """CLI interface for Owl of Athena"""
    if len(sys.argv) < 2:
        print("Usage: owl.py <command> [args]")
        print("Commands:")
        print("  archive <feature-id>   - Move feature to archived")
        print("  retrieve <feature-id>  - Get feature summary")
        print("  search <keyword>       - Search archived features")
        print("  update-index           - Regenerate INDEX.md")
        sys.exit(1)
    
    repo_root = Path.cwd()
    owl = OwlOfAthena(repo_root)
    
    command = sys.argv[1]
    
    if command == "archive" and len(sys.argv) > 2:
        result = owl.archive_feature(sys.argv[2])
    elif command == "retrieve" and len(sys.argv) > 2:
        result = owl.retrieve_feature(sys.argv[2])
    elif command == "search" and len(sys.argv) > 2:
        result = owl.search_features(sys.argv[2])
    elif command == "update-index":
        result = owl.update_index()
    else:
        result = {"error": "Invalid command or missing arguments"}
    
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
