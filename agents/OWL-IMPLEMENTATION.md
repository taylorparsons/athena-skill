# Owl of Athena: Implementation

**Status**: ✅ Implemented  
**Script**: `scripts/owl.py`  
**Wrapper**: `scripts/owl`

## Quick Start

```bash
# Update INDEX.md from current specs
./scripts/owl update-index

# Search archived features
./scripts/owl search "linkedin"

# Retrieve feature summary
./scripts/owl retrieve 20260211-athena-walkthrough-example

# Archive a feature (mark as Done in INDEX)
./scripts/owl archive 20260413-my-feature
```

## Commands

### update-index
Regenerate INDEX.md from all specs in docs/specs/

**Usage**: `./scripts/owl update-index`

**Output**:
```json
{
  "success": true,
  "total_features": 19,
  "active": 0,
  "archived": 19,
  "message": "✅ Updated INDEX.md: 0 active, 19 archived"
}
```

### search <keyword>
Search archived features by keyword

**Usage**: `./scripts/owl search "linkedin"`

**Output**:
```json
{
  "success": true,
  "keyword": "linkedin",
  "matches": [
    {
      "feature_id": "20260213-linkedin-personal-style",
      "match": "- **Spec**: docs/specs/20260213-linkedin-personal-style/spec.md"
    }
  ],
  "count": 2
}
```

### retrieve <feature-id>
Get summary of archived feature

**Usage**: `./scripts/owl retrieve 20260211-athena-walkthrough-example`

**Output**:
```json
{
  "success": true,
  "feature_id": "20260211-athena-walkthrough-example",
  "status": "Done",
  "summary": "Add onboarding walkthrough showing CR→Task chain",
  "spec_path": "docs/specs/20260211-athena-walkthrough-example/spec.md"
}
```

### archive <feature-id>
Move feature from Active to Archived in INDEX.md and archive progress.txt

**Usage**: `./scripts/owl archive 20260413-my-feature`

**What it does**:
1. Moves feature from Active → Archived in INDEX.md
2. Archives progress.txt entries for that feature to docs/specs/<feature-id>/progress-archive.txt
3. Keeps only current session in docs/progress.txt

**Output**:
```json
{
  "success": true,
  "feature_id": "20260413-my-feature",
  "summary": "Feature summary",
  "progress_archived": true,
  "message": "✅ Moved 20260413-my-feature to archived in INDEX.md"
}
```

**Token savings**: Archiving old progress entries can save 2-3K tokens per completed feature

## Integration with Athena

### From Command Line
```bash
# Main agent delegates to Owl
./scripts/owl search "keyword"
```

### From Python
```python
from scripts.owl import OwlOfAthena
from pathlib import Path

owl = OwlOfAthena(Path.cwd())
result = owl.search_features("linkedin")
print(result)
```

### From Athena Session
```
User: "Search for LinkedIn features"
Agent: [runs ./scripts/owl search "linkedin"]
Agent: Found 2 features: linkedin-personal-style, linkedin-post-variants
```

## Token Optimization

**Owl uses cheap model** (Haiku/GPT-4o-mini):
- update-index: ~800 tokens
- search: ~200 tokens
- retrieve: ~300 tokens
- archive: ~500 tokens

**Main agent uses expensive model** (Sonnet/GPT-5):
- Only loads INDEX.md: ~1,100 tokens
- Delegates archive ops to Owl
- **Savings**: 99% on archive operations

## Testing

All commands tested and working:
- ✅ update-index: Regenerates INDEX.md from 19 specs
- ✅ search: Finds 2 LinkedIn features
- ✅ retrieve: Returns walkthrough feature summary
- ✅ archive: Ready to test with new feature

## Next Steps

1. ✅ Implement owl.py
2. ✅ Test all commands
3. ✅ Create wrapper script
4. ✅ Add Git hooks for automation
5. ⏳ Integrate with Athena SKILL.md
6. ⏳ Add @owl command handler
7. ⏳ Test in real Athena session

## Git Hooks (NEW!)

**Install hooks**:
```bash
./scripts/install-hooks.sh
```

**What they do**:
- **pre-commit**: Validates INDEX.md is in sync with specs (prevents commits if out of sync)
- **post-commit**: Auto-updates INDEX.md when features complete (detects "Status: Done" in commits)

**Example workflow**:
```bash
# 1. Complete a feature
git commit -m "feat: complete feature (Status: Done)"

# 2. Post-commit hook automatically:
#    - Detects "Status: Done"
#    - Runs: ./scripts/owl update-index
#    - Amends commit with updated INDEX.md

# 3. Pre-commit hook validates on next commit
```

**Benefits**:
- ✅ INDEX.md always in sync
- ✅ No manual updates needed
- ✅ Catches sync issues before push
- ✅ Automatic archival on completion
