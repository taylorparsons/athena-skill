#!/bin/bash
# install-owl.sh — Install the scripts/owl delegation wrapper into any Athena project.
#
# Usage (from project root):
#   bash ~/.claude/skills/athena/scripts/install-owl.sh
#
# What it does:
#   1. Creates scripts/ if missing
#   2. Writes scripts/owl as a thin wrapper that delegates to owl.py
#   3. Makes it executable
#
# The wrapper delegates ALL commands to owl.py so prune-done, update-index,
# write-memory, archive, retrieve, and search all use the single authoritative
# Python implementation in the Athena skill.

set -e

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="$REPO_ROOT/scripts/owl"

mkdir -p "$REPO_ROOT/scripts"

cat > "$TARGET" << 'WRAPPER'
#!/bin/bash
# owl - Athena archive management helper
# Delegates to ~/.claude/skills/athena/scripts/owl.py when available.
# Falls back to a minimal bash write-memory for environments without the skill.
#
# Commands: prune-done, update-index, write-memory, archive, retrieve, search, trim-progress

set -e

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
SKILL_OWL="$HOME/.claude/skills/athena/scripts/owl.py"

# Primary path: delegate everything to the global owl.py
if [ -f "$SKILL_OWL" ]; then
    exec python3 "$SKILL_OWL" --repo "$REPO_ROOT" "$@"
fi

# ── Fallback (skill not installed) ───────────────────────────────────────────
# Only write-memory is implemented here. prune-done and update-index require
# owl.py and will warn instead of silently doing nothing.

DOCS_DIR="$REPO_ROOT/docs"
MEMORY_DIR="$HOME/.claude/projects/$(echo "$REPO_ROOT" | sed 's/[^a-zA-Z0-9._-]/-/g')/memory"
mkdir -p "$MEMORY_DIR"

write_memory() {
  if [ ! -f "$DOCS_DIR/decisions.md" ] && [ ! -f "$DOCS_DIR/progress.txt" ] && [ ! -f "$DOCS_DIR/requests.md" ]; then
    return 0
  fi

  if [ -f "$DOCS_DIR/progress.txt" ]; then
    head_lines=$(head -n 50 "$DOCS_DIR/progress.txt")
    cat > "$MEMORY_DIR/project_status.md" << 'EOF'
---
name: Current Project Status
description: Active project status and recent progress
type: project
---

# Recent Progress

EOF
    echo "$head_lines" >> "$MEMORY_DIR/project_status.md"
  fi

  if [ -f "$DOCS_DIR/decisions.md" ]; then
    sed '/^## Archive/,$d' "$DOCS_DIR/decisions.md" | head -n 100 > "$MEMORY_DIR/active_decisions_raw.txt" 2>/dev/null || true
    if [ -s "$MEMORY_DIR/active_decisions_raw.txt" ]; then
      cat > "$MEMORY_DIR/active_decisions.md" << 'EOF'
---
name: Active Project Decisions
description: Key architectural and product decisions made in this project
type: project
---

# Active Decisions

EOF
      cat "$MEMORY_DIR/active_decisions_raw.txt" >> "$MEMORY_DIR/active_decisions.md"
      rm -f "$MEMORY_DIR/active_decisions_raw.txt"
    fi
  fi

  if [ -f "$DOCS_DIR/requests.md" ]; then
    sed '/^## Archive/,$d' "$DOCS_DIR/requests.md" | head -n 100 > "$MEMORY_DIR/active_requests_raw.txt" 2>/dev/null || true
    if [ -s "$MEMORY_DIR/active_requests_raw.txt" ]; then
      cat > "$MEMORY_DIR/active_requests.md" << 'EOF'
---
name: Active Customer Requests
description: Current feature requests and customer needs from ATHENA requests.md
type: project
---

# Active Requests

EOF
      cat "$MEMORY_DIR/active_requests_raw.txt" >> "$MEMORY_DIR/active_requests.md"
      rm -f "$MEMORY_DIR/active_requests_raw.txt"
    fi
  fi
}

case "${1:-write-memory}" in
  write-memory)
    write_memory
    ;;
  prune-done|update-index)
    echo "⚠️  owl.py not found at $SKILL_OWL — install the Athena skill to enable $1" >&2
    exit 0
    ;;
  *)
    echo "Usage: owl {write-memory|prune-done|update-index|archive|retrieve|search}" >&2
    echo "Note: install ~/.claude/skills/athena to enable all commands" >&2
    exit 1
    ;;
esac
WRAPPER

chmod +x "$TARGET"
echo "✅ Installed $TARGET (delegates to owl.py)"

# Write project .claude/settings.json with correct hook commands
SETTINGS_DIR="$REPO_ROOT/.claude"
SETTINGS_FILE="$SETTINGS_DIR/settings.json"
mkdir -p "$SETTINGS_DIR"

cat > "$SETTINGS_FILE" << 'SETTINGS'
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "cd \"$(git rev-parse --show-toplevel)\" && ./scripts/owl prune-done | jq -r '.message // .' && ./scripts/owl update-index | jq -r '.message // .' && ./scripts/owl write-memory | jq -r '.message // .'; true"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "cd \"$(git rev-parse --show-toplevel)\" && ./scripts/owl prune-done | jq -r '.message // .' && ./scripts/owl update-index | jq -r '.message // .'; true"
          }
        ]
      }
    ]
  }
}
SETTINGS

echo "✅ Wrote $SETTINGS_FILE (SessionStart + Stop hooks)"

# Quick smoke test
if python3 "$SKILL_DIR/scripts/owl.py" --repo "$REPO_ROOT" write-memory 2>/dev/null | jq -r '.message // .' 2>/dev/null; then
    echo "✅ owl.py smoke test passed"
else
    echo "⚠️  owl.py returned non-zero — check that docs/ exists in $REPO_ROOT"
fi
