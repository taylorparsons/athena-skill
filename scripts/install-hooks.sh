#!/bin/bash
# Install Owl Git Hooks
# Usage: ./scripts/install-hooks.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
HOOKS_DIR="$REPO_ROOT/.git/hooks"

echo "🦉 Installing Owl of Athena Git Hooks..."
echo ""

# Check if .git exists
if [ ! -d "$REPO_ROOT/.git" ]; then
    echo "❌ Error: Not a git repository"
    exit 1
fi

# Install post-commit hook
if [ -f "$SCRIPT_DIR/hooks/post-commit" ]; then
    cp "$SCRIPT_DIR/hooks/post-commit" "$HOOKS_DIR/post-commit"
    chmod +x "$HOOKS_DIR/post-commit"
    echo "✅ Installed: post-commit (auto-update athena-index.md)"
else
    echo "⚠️  Skipped: post-commit hook not found"
fi

# Install pre-commit hook
if [ -f "$SCRIPT_DIR/hooks/pre-commit" ]; then
    cp "$SCRIPT_DIR/hooks/pre-commit" "$HOOKS_DIR/pre-commit"
    chmod +x "$HOOKS_DIR/pre-commit"
    echo "✅ Installed: pre-commit (validate athena-index.md sync)"
else
    echo "⚠️  Skipped: pre-commit hook not found"
fi

echo ""
echo "🎉 Owl hooks installed!"
echo ""
echo "What they do:"
echo "  • pre-commit: Validates athena-index.md is in sync with specs"
echo "  • post-commit: Auto-updates athena-index.md when features complete"
echo ""
echo "To uninstall:"
echo "  rm .git/hooks/post-commit .git/hooks/pre-commit"
