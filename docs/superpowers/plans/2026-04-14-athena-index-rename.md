# Athena Index Rename Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rename `docs/INDEX.md` to `docs/athena-index.md` across all functional code, hooks, and documentation to prevent filename collisions in mature repos.

**Architecture:** Single constant change in `owl.py` drives all functional behavior. Git hooks get surgical path + message updates. All other changes are string replacements in documentation files. Append-only logs and `progress-archive.txt` are never touched.

**Tech Stack:** Python 3, bash, markdown

**ATHENA traceability:**
- Input: CR-20260414-1100
- Decision: D-20260414-1100
- Spec: docs/specs/20260414-athena-index-rename/spec.md
- Tasks: docs/specs/20260414-athena-index-rename/tasks.md

---

### Task 1: Rename the file and update owl.py constant (T-001, T-002)

**Files:**
- Rename: `docs/INDEX.md` → `docs/athena-index.md`
- Modify: `scripts/owl.py:19`

- [ ] **Step 1: Rename the file**

```bash
git mv docs/INDEX.md docs/athena-index.md
```

- [ ] **Step 2: Update the constant in owl.py**

In `scripts/owl.py`, change line 19:

```python
# Before
self.index_path = self.docs_dir / "INDEX.md"

# After
self.index_path = self.docs_dir / "athena-index.md"
```

- [ ] **Step 3: Verify owl.py uses the new path**

```bash
python3 scripts/owl.py update-index
```

Expected output:
```json
{
  "success": true,
  "total_features": 19,
  "active": 0,
  "archived": 19,
  "message": "✅ Updated INDEX.md: 0 active, 19 archived"
}
```

Then confirm the file was created at the right path:

```bash
ls docs/athena-index.md
```

Expected: file exists. `docs/INDEX.md` must NOT exist.

- [ ] **Step 4: Verify prune-done also works**

```bash
python3 scripts/owl.py prune-done
```

Expected:
```json
{
  "success": true,
  "pruned_features": [],
  "blocks_removed": 0,
  "message": "✅ Pruned 0 session block(s) for 0 closed feature(s)"
}
```

- [ ] **Step 5: Commit**

```bash
git add docs/athena-index.md scripts/owl.py
git commit -m "T-001,T-002: rename INDEX.md to athena-index.md, update owl.py constant (Feature: 20260414-athena-index-rename)

Input: CR-20260414-1100
Decision: D-20260414-1100
Spec: docs/specs/20260414-athena-index-rename/spec.md"
```

---

### Task 2: Update pre-commit hook (T-003)

**Files:**
- Modify: `scripts/hooks/pre-commit`

- [ ] **Step 1: Update the INDEX_FILE variable**

In `scripts/hooks/pre-commit`, change:

```bash
# Before
INDEX_FILE="$REPO_ROOT/docs/INDEX.md"

# After
INDEX_FILE="$REPO_ROOT/docs/athena-index.md"
```

- [ ] **Step 2: Update output messages**

```bash
# Before
echo "⚠️  Owl: INDEX.md out of sync!"
echo "   INDEX.md lists: $INDEX_COUNT features"
echo "   Then: git add docs/INDEX.md"
echo "✅ Owl: INDEX.md in sync ($INDEX_COUNT features)"

# After
echo "⚠️  Owl: athena-index.md out of sync!"
echo "   athena-index.md lists: $INDEX_COUNT features"
echo "   Then: git add docs/athena-index.md"
echo "✅ Owl: athena-index.md in sync ($INDEX_COUNT features)"
```

- [ ] **Step 3: Verify hook runs cleanly**

```bash
bash scripts/hooks/pre-commit
```

Expected: `✅ Owl: athena-index.md in sync (19 features)`
Exit code: 0

- [ ] **Step 4: Commit**

```bash
git add scripts/hooks/pre-commit
git commit -m "T-003: update pre-commit hook for athena-index.md (Feature: 20260414-athena-index-rename)

Input: CR-20260414-1100
Spec: docs/specs/20260414-athena-index-rename/spec.md"
```

---

### Task 3: Update post-commit hook (T-004)

**Files:**
- Modify: `scripts/hooks/post-commit`

- [ ] **Step 1: Update git diff and git add paths**

In `scripts/hooks/post-commit`, change:

```bash
# Before
echo "🦉 Owl: Detected feature completion, updating INDEX.md..."
echo "🦉 Owl: Regenerating INDEX.md..."
if ! git diff --quiet docs/INDEX.md 2>/dev/null; then
    echo "🦉 Owl: INDEX.md updated, staging changes..."
    git add docs/INDEX.md
    ...
    echo "✅ INDEX.md automatically updated"
else
    echo "✅ INDEX.md already up to date"
fi

# After
echo "🦉 Owl: Detected feature completion, updating athena-index.md..."
echo "🦉 Owl: Regenerating athena-index.md..."
if ! git diff --quiet docs/athena-index.md 2>/dev/null; then
    echo "🦉 Owl: athena-index.md updated, staging changes..."
    git add docs/athena-index.md
    ...
    echo "✅ athena-index.md automatically updated"
else
    echo "✅ athena-index.md already up to date"
fi
```

- [ ] **Step 2: Verify hook is valid bash**

```bash
bash -n scripts/hooks/post-commit
```

Expected: no output, exit code 0.

- [ ] **Step 3: Commit**

```bash
git add scripts/hooks/post-commit
git commit -m "T-004: update post-commit hook for athena-index.md (Feature: 20260414-athena-index-rename)

Input: CR-20260414-1100
Spec: docs/specs/20260414-athena-index-rename/spec.md"
```

---

### Task 4: Update install-hooks.sh and patch-claude-settings.py (T-005, T-006)

**Files:**
- Modify: `scripts/install-hooks.sh`
- Modify: `scripts/patch-claude-settings.py`

- [ ] **Step 1: Update install-hooks.sh messages**

In `scripts/install-hooks.sh`, replace every `INDEX.md` with `athena-index.md` in the echo output lines:

```bash
# Lines to update (4 occurrences):
echo "✅ Installed: post-commit (auto-update athena-index.md)"
echo "✅ Installed: pre-commit (validate athena-index.md sync)"
echo "  • pre-commit: Validates athena-index.md is in sync with specs"
echo "  • post-commit: Auto-updates athena-index.md when features complete"
```

- [ ] **Step 2: Update patch-claude-settings.py trigger strings**

In `scripts/patch-claude-settings.py`, update the `OWL_SECTION` string (the CLAUDE.md content block). Change every `INDEX.md` occurrence to `athena-index.md` within the string constants. The relevant lines are in `OWL_SECTION` around:

```python
# Before (within the OWL_SECTION string)
"or INDEX.md appears stale."
"INDEX.md appears stale. Never load"

# After
"or athena-index.md appears stale."
"athena-index.md appears stale. Never load"
```

- [ ] **Step 3: Verify patch script is valid Python**

```bash
python3 -c "import scripts.patch_claude_settings" 2>/dev/null || python3 scripts/patch-claude-settings.py --dry-run
```

Expected: reports current install state cleanly, no syntax errors.

- [ ] **Step 4: Commit**

```bash
git add scripts/install-hooks.sh scripts/patch-claude-settings.py
git commit -m "T-005,T-006: update install-hooks.sh and patch script for athena-index.md (Feature: 20260414-athena-index-rename)

Input: CR-20260414-1100
Spec: docs/specs/20260414-athena-index-rename/spec.md"
```

---

### Task 5: Update SKILL.md files (T-007)

**Files:**
- Modify: `SKILL.md`
- Modify: `skills/athena/SKILL.md`

- [ ] **Step 1: Update root SKILL.md**

In `SKILL.md`, replace all occurrences of `INDEX.md` with `athena-index.md`. Key lines to verify after:

```markdown
- `docs/athena-index.md` (load first - identifies active vs archived features)
**Token optimization**: athena-index.md lists all features...
| athena-index.md appears stale | `"Run update-index"` |
```

- [ ] **Step 2: Update skills/athena/SKILL.md**

Same replacements in `skills/athena/SKILL.md`. Verify same three lines updated.

- [ ] **Step 3: Verify no INDEX.md remains in either SKILL.md**

```bash
grep "INDEX\.md" SKILL.md skills/athena/SKILL.md
```

Expected: no output.

- [ ] **Step 4: Commit**

```bash
git add SKILL.md skills/athena/SKILL.md
git commit -m "T-007: update SKILL.md files for athena-index.md (Feature: 20260414-athena-index-rename)

Input: CR-20260414-1100
Spec: docs/specs/20260414-athena-index-rename/spec.md"
```

---

### Task 6: Update agent files (T-008, T-009)

**Files:**
- Modify: `agents/owl-of-athena.md`
- Modify: `.claude/agents/owl-of-athena.md`
- Modify: `agents/OWL-IMPLEMENTATION.md`

- [ ] **Step 1: Update agents/owl-of-athena.md**

Replace all `INDEX.md` with `athena-index.md`. Key occurrences:

```markdown
**Purpose**: Manage athena-index.md and archived features
### 1. athena-index.md Maintenance
- Update athena-index.md when features complete
- Keep athena-index.md under 1K tokens
```

- [ ] **Step 2: Update .claude/agents/owl-of-athena.md**

Replace all `INDEX.md` with `athena-index.md`. Key lines:

```markdown
description: ...Handles athena-index.md maintenance...
- `./scripts/owl archive <feature-id>` — move feature to archived in athena-index.md
- `./scripts/owl update-index` — regenerate athena-index.md from all specs...
```

- [ ] **Step 3: Update agents/OWL-IMPLEMENTATION.md**

Replace all `INDEX.md` with `athena-index.md` throughout the file.

- [ ] **Step 4: Verify no INDEX.md remains**

```bash
grep "INDEX\.md" agents/owl-of-athena.md .claude/agents/owl-of-athena.md agents/OWL-IMPLEMENTATION.md
```

Expected: no output.

- [ ] **Step 5: Commit**

```bash
git add agents/owl-of-athena.md .claude/agents/owl-of-athena.md agents/OWL-IMPLEMENTATION.md
git commit -m "T-008,T-009: update agent files for athena-index.md (Feature: 20260414-athena-index-rename)

Input: CR-20260414-1100
Spec: docs/specs/20260414-athena-index-rename/spec.md"
```

---

### Task 7: Update README.md and INDEX-TEST-RESULTS.md (T-010, T-011)

**Files:**
- Modify: `docs/INDEX-TEST-RESULTS.md`
- Modify: `README.md`

- [ ] **Step 1: Update docs/INDEX-TEST-RESULTS.md**

Replace all `INDEX.md` with `athena-index.md` throughout the file. Verify:

```bash
grep "INDEX\.md" docs/INDEX-TEST-RESULTS.md
```

Expected: no output.

- [ ] **Step 2: Replace all INDEX.md references in README.md**

Replace all `INDEX.md` with `athena-index.md` in `README.md`.

- [ ] **Step 3: Add single-prompt fast path to existing-project bootstrap**

In `README.md`, find the "Step 3 — Bootstrap an existing project" section. It currently opens with:

```markdown
### Step 3 — Bootstrap an existing project (first time only)

If your project already has ATHENA docs but no `INDEX.md`, generate it once:
```

Replace with:

```markdown
### Step 3 — Bootstrap an existing project (first time only)

If your project already has ATHENA docs but no `athena-index.md`, you have two options:

**Fast path — paste this prompt into Claude Code:**

```
Bootstrap Owl of Athena in this project. Run ./scripts/owl update-index to generate docs/athena-index.md, run ./scripts/install-hooks.sh to install git hooks, run ./scripts/owl prune-done to clean progress.txt, then commit the results.
```

**Manual path:**
```

Then keep the existing numbered steps below it, updated to reference `athena-index.md`.

- [ ] **Step 4: Verify no INDEX.md remains in README.md**

```bash
grep "INDEX\.md" README.md
```

Expected: no output.

- [ ] **Step 5: Commit**

```bash
git add docs/INDEX-TEST-RESULTS.md README.md
git commit -m "T-010,T-011: update README and test results for athena-index.md, add single-prompt bootstrap (Feature: 20260414-athena-index-rename)

Input: CR-20260414-1100
Spec: docs/specs/20260414-athena-index-rename/spec.md"
```

---

### Task 8: Update progress.txt and ATHENA artifacts, final commit (T-012, T-013)

**Files:**
- Modify: `docs/progress.txt`
- Modify: `docs/specs/20260414-athena-index-rename/tasks.md`

- [ ] **Step 1: Update progress.txt active references**

In `docs/progress.txt`, replace any remaining `INDEX.md` references in the current session block (the top session — do NOT touch the `---` separator or anything below it).

- [ ] **Step 2: Final verification — no functional INDEX.md references remain**

```bash
grep -r "INDEX\.md" scripts/ SKILL.md skills/athena/SKILL.md agents/ .claude/agents/ README.md docs/INDEX-TEST-RESULTS.md docs/progress.txt
```

Expected: no output.

- [ ] **Step 3: Confirm docs/athena-index.md exists and docs/INDEX.md does not**

```bash
ls docs/athena-index.md && ! ls docs/INDEX.md 2>/dev/null && echo "✅ rename complete"
```

Expected: `✅ rename complete`

- [ ] **Step 4: Mark tasks done in tasks.md**

In `docs/specs/20260414-athena-index-rename/tasks.md`, move all tasks to DONE with timestamp.

- [ ] **Step 5: Final traceable commit**

```bash
git add docs/progress.txt docs/specs/20260414-athena-index-rename/tasks.md
git commit -m "T-012,T-013: update progress.txt, mark feature done (Feature: 20260414-athena-index-rename)

Input: CR-20260414-1100
Decision: D-20260414-1100
Spec: docs/specs/20260414-athena-index-rename/spec.md
Tasks: docs/specs/20260414-athena-index-rename/tasks.md
Progress: docs/progress.txt"
```
