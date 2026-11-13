#!/usr/bin/env python3
"""Unit tests for owl.py script-gated KB commands (token-diet layout).

Run: python3 -m unittest discover -s scripts/tests -v
"""
import re
import shutil
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from owl import TASK_ID_RE, OwlOfAthena  # noqa: E402


def make_feature(specs_dir: Path, feature_id: str, status: str = "Active",
                 next_tasks=None, in_progress=None, summary="Test feature summary.",
                 with_tasks: bool = True, blank_line_summary: bool = False):
    """Write a feature spec (+ tasks.md unless with_tasks=False).

    blank_line_summary writes the `## Summary` heading followed by a blank line,
    the other legal Markdown shape; both shapes must yield the same summary.
    with_tasks=False models a pre-migration feature whose task truth is still
    docs/progress.txt.
    """
    fdir = specs_dir / feature_id
    fdir.mkdir(parents=True)
    if status == "Active" and next_tasks is None and in_progress is None:
        next_tasks = ["T-001: pending task. (Implements: FR-001)"]
    summary_block = f"## Summary\n\n{summary}" if blank_line_summary else f"## Summary\n- {summary}"
    (fdir / "spec.md").write_text(
        f"# Feature Spec: {feature_id}\n\nStatus: {status}\n\n"
        f"{summary_block}\n\n## Requirements\n\n"
        "Functional requirements:\n"
        "- FR-001: Do the thing. (Sources: CR-20260101-1200; D-20260101-1201)\n",
        encoding="utf-8")
    if not with_tasks:
        return fdir
    next_lines = "\n".join(f"- {t}" for t in (next_tasks or []))
    prog_lines = "\n".join(f"- {t}" for t in (in_progress or ["(none)"]))
    (fdir / "tasks.md").write_text(
        f"# Tasks: {feature_id}\n\n## NEXT\n{next_lines}\n\n"
        f"## IN PROGRESS\n{prog_lines}\n\n## DONE\n- [2026-01-01 12:00] T-000: done task. (Implements: FR-001)\n",
        encoding="utf-8")
    return fdir


class OwlTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="owl-test-"))
        self.docs = self.tmp / "docs"
        self.specs = self.docs / "specs"
        self.specs.mkdir(parents=True)
        self.owl = OwlOfAthena(self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)


class TestAppendCommands(OwlTestCase):
    def test_add_request_creates_log_and_returns_id(self):
        result = self.owl.add_request("Please build X", source="chat")
        self.assertTrue(result.get("success"))
        self.assertTrue(result["id"].startswith("CR-"))
        content = (self.docs / "requests.md").read_text()
        self.assertIn("# Customer Requests (append-only)", content)
        self.assertIn(f"## {result['id']}", content)
        self.assertIn("Please build X", content)

    def test_add_request_empty_text_errors(self):
        self.assertIn("error", self.owl.add_request("   "))

    def test_add_request_id_collision_bumps_minute(self):
        first = self.owl.add_request("first")
        second = self.owl.add_request("second")
        self.assertNotEqual(first["id"], second["id"])

    def test_add_decision_requires_cr(self):
        self.assertIn("error", self.owl.add_decision("some decision", cr=""))
        self.assertIn("error", self.owl.add_decision("some decision", cr="X-1"))

    def test_add_decision_appends_entry(self):
        result = self.owl.add_decision("Chose option A.", cr="CR-20260101-1200",
                                       prd="Section 2")
        self.assertTrue(result.get("success"))
        content = (self.docs / "decisions.md").read_text()
        self.assertIn(f"## {result['id']}", content)
        self.assertIn("Inputs: CR-20260101-1200", content)
        self.assertIn("PRD: Section 2", content)
        self.assertIn("Chose option A.", content)

    def test_add_note_requires_existing_feature(self):
        self.assertIn("error", self.owl.add_note("nope", "notes"))
        self.assertIn("error", self.owl.add_note("", "notes"))

    def test_add_note_creates_and_appends(self):
        make_feature(self.specs, "20260101-feat")
        result = self.owl.add_note("20260101-feat", "Ran tests -> pass",
                                   goal="Ship it", skills="athena")
        self.assertTrue(result.get("success"))
        content = (self.specs / "20260101-feat" / "notes.md").read_text()
        self.assertIn("# Session Notes: 20260101-feat (append-only)", content)
        self.assertIn(f"## {result['id']}", content)
        self.assertIn("Goal: Ship it", content)
        self.assertIn("Skills: athena", content)
        self.assertIn("Ran tests -> pass", content)


class TestContext(OwlTestCase):
    def test_context_new_layout(self):
        make_feature(self.specs, "20260101-active", status="Active",
                     next_tasks=["T-002: next thing. (Implements: FR-001)"],
                     in_progress=["T-001: current thing. (Implements: FR-001)"])
        make_feature(self.specs, "20251201-done", status="Done")
        self.owl.add_note("20260101-active", "session note", goal="The goal line")
        self.owl.add_request("Latest customer ask")
        self.owl.add_decision("A decision", cr="CR-20260101-1200")

        block = self.owl.context_block()
        self.assertIn("Active feature: 20260101-active", block)
        self.assertIn("Goal: The goal line", block)
        self.assertIn("T-001: current thing", block)
        self.assertIn("T-002: next thing", block)
        self.assertIn("Latest customer ask", block)
        self.assertIn("Recent requests: CR-", block)
        self.assertIn("Recent decisions: D-", block)
        self.assertNotIn("20251201-done", block)

    def test_context_goal_falls_back_to_spec_summary(self):
        make_feature(self.specs, "20260101-active", summary="Spec summary goal.")
        block = self.owl.context_block()
        self.assertIn("Goal: Spec summary goal.", block)

    def test_context_no_active_feature(self):
        block = self.owl.context_block()
        self.assertIn("Active feature: (none)", block)

    def test_context_multiple_active_picks_latest_note(self):
        make_feature(self.specs, "20260101-older")
        make_feature(self.specs, "20260102-newer")
        (self.specs / "20260101-older" / "notes.md").write_text(
            "# Session Notes\n\n## S-20260101-1000\nGoal: old\n\nx\n")
        (self.specs / "20260102-newer" / "notes.md").write_text(
            "# Session Notes\n\n## S-20260601-1000\nGoal: new\n\nx\n")
        block = self.owl.context_block()
        self.assertIn("Active feature: 20260102-newer", block)
        self.assertIn("Other active features: 20260101-older", block)

    LEGACY_PROGRESS = ("Session: 2026-01-05 10:00\nFeature: 20260101-active\n"
                       "Goal: Legacy goal\n\nIN PROGRESS\n- legacy task one\n\n"
                       "NEXT\n- legacy task two\n")

    def test_context_legacy_layout_reads_progress(self):
        """No tasks.md for the feature: progress.txt is still task truth."""
        make_feature(self.specs, "20260101-active", with_tasks=False)
        (self.docs / "progress.txt").write_text(self.LEGACY_PROGRESS, encoding="utf-8")
        block = self.owl.context_block()
        self.assertIn("Goal: Legacy goal", block)
        self.assertIn("legacy task one", block)
        self.assertIn("legacy task two", block)

    def test_context_prefers_feature_tasks_over_progress(self):
        """Defect 1: a repo may keep progress.txt as phase evidence AND have a
        migrated feature. tasks.md wins; progress.txt must not blank out NEXT."""
        make_feature(self.specs, "20260101-active",
                     next_tasks=["T-002: next thing. (Implements: FR-001)"],
                     in_progress=["T-001: current thing. (Implements: FR-001)"])
        (self.docs / "progress.txt").write_text(self.LEGACY_PROGRESS, encoding="utf-8")
        block = self.owl.context_block()
        self.assertIn("T-002: next thing", block)
        self.assertIn("T-001: current thing", block)
        self.assertNotIn("legacy task one", block)
        self.assertNotIn("legacy task two", block)
        # Precedence, not removal: the fallback source stays on disk untouched.
        self.assertTrue((self.docs / "progress.txt").exists())

    def test_context_progress_without_session_block_does_not_blank_tasks(self):
        """The live repo shape: progress.txt holds phase evidence but no
        `Session:` block, so the legacy parse is empty and must not win."""
        make_feature(self.specs, "20260101-active",
                     next_tasks=["T-1423: blocking spike. (Implements: FR-1408)"])
        (self.docs / "progress.txt").write_text(
            "## Phase 4 evidence [2026-01-05]\n- p95 latency 1.8s\n", encoding="utf-8")
        block = self.owl.context_block()
        self.assertIn("Active feature: 20260101-active", block)
        self.assertIn("T-1423: blocking spike", block)

    def test_context_ignores_indented_task_detail_bullets(self):
        """A task's indented detail lines are not tasks. Counting them turned
        `NEXT (top 5)` into five fragments of one task's prose."""
        fdir = self.specs / "20260101-active"
        fdir.mkdir(parents=True)
        (fdir / "spec.md").write_text("# Spec\n\nStatus: Active\n\n## Summary\n\nS.\n",
                                      encoding="utf-8")
        (fdir / "tasks.md").write_text(
            "# Tasks\n\n## NEXT\n\n"
            "- T-1423: BLOCKING spike (Implements: FR-1408)\n"
            "  - Gate order: no other task starts until this passes.\n"
            "  - Baseline: an unattended reboot plus normal warm-up.\n"
            "- T-1424: Second real task (Implements: FR-1409)\n", encoding="utf-8")
        ctx = self.owl._active_context()
        self.assertEqual(ctx["next_tasks"],
                         ["T-1423: BLOCKING spike (Implements: FR-1408)",
                          "T-1424: Second real task (Implements: FR-1409)"])

    def test_status_active_requires_a_top_level_task(self):
        """A NEXT section holding only indented detail is not an active task."""
        self.assertEqual(
            self.owl._extract_status_from_tasks("## NEXT\n\n  - detail only\n"), "Done")
        self.assertEqual(
            self.owl._extract_status_from_tasks("## NEXT\n\n- T-001: real\n"), "Active")

    def test_context_mixed_repo_falls_back_per_feature(self):
        """Precedence is evaluated per feature, not once for the whole repo."""
        make_feature(self.specs, "20260101-active", with_tasks=False)
        make_feature(self.specs, "20260102-migrated",
                     next_tasks=["T-003: migrated task. (Implements: FR-001)"])
        (self.docs / "progress.txt").write_text(self.LEGACY_PROGRESS, encoding="utf-8")
        # progress.txt names the unmigrated feature, so its tasks are the source.
        self.assertIn("legacy task two", self.owl.context_block())


class TestSummaryExtraction(OwlTestCase):
    """Defect 2: `## Summary` followed by a blank line yielded an empty summary.

    Measured on this repo before the fix: 16/16 blank-line specs had an empty
    index summary, 9/9 same-line specs had a populated one. Both shapes are
    correct Markdown, so both must extract the same text.
    """

    TEXT = "Replace Home Assistant with a purpose-built Claire runtime."

    def test_blank_line_and_inline_summary_agree(self):
        inline = f"# Spec\n\n## Summary\n{self.TEXT}\n\n## Requirements\n"
        blank = f"# Spec\n\n## Summary\n\n{self.TEXT}\n\n## Requirements\n"
        bullet = f"# Spec\n\n## Summary\n- {self.TEXT}\n\n## Requirements\n"
        self.assertEqual(self.owl._extract_summary(inline), self.TEXT)
        self.assertEqual(self.owl._extract_summary(blank), self.TEXT)
        self.assertEqual(self.owl._extract_summary(bullet), self.TEXT)

    def test_summary_collects_wrapped_paragraph_as_one_line(self):
        spec = ("# Spec\n\n## Summary\n\nReplace Home Assistant with a\n"
                "purpose-built Claire runtime.\n\nTrailing paragraph.\n\n## Requirements\n")
        summary = self.owl._extract_summary(spec)
        self.assertEqual(summary, "Replace Home Assistant with a purpose-built Claire runtime.")
        self.assertNotIn("\n", summary)  # the index stores one summary per line
        self.assertNotIn("Trailing paragraph", summary)

    def test_summary_stops_at_next_heading_or_rule(self):
        self.assertEqual(
            self.owl._extract_summary("## Summary\n\n---\n\n## Requirements\n"),
            "No summary available")
        self.assertEqual(
            self.owl._extract_summary("## Summary\n\n## Requirements\n\nbody\n"),
            "No summary available")

    def test_summary_absent_returns_placeholder(self):
        self.assertEqual(self.owl._extract_summary("# Spec\n\n## Requirements\n"),
                         "No summary available")

    def test_update_index_populates_blank_line_summaries(self):
        make_feature(self.specs, "20260101-blank", blank_line_summary=True,
                     summary="Blank-line shape summary.")
        make_feature(self.specs, "20260102-inline", summary="Inline shape summary.")
        self.owl.update_index()
        index = (self.docs / "athena-index.md").read_text()
        self.assertIn("- **Summary**: Blank-line shape summary.", index)
        self.assertIn("- **Summary**: Inline shape summary.", index)


class TestIndexFieldParsing(OwlTestCase):
    """Defect 3: `_find_in_index` searched for `Status:`, but `update-index`
    emits `- **Status**: `, so the literal never matched its own output."""

    def test_retrieve_after_update_index_roundtrip(self):
        make_feature(self.specs, "20260101-active", blank_line_summary=True,
                     summary="Round-trip summary.")
        self.owl.update_index()
        result = self.owl.retrieve_feature("20260101-active")
        self.assertTrue(result.get("success"))
        self.assertEqual(result["status"], "Active")
        self.assertEqual(result["summary"], "Round-trip summary.")

    def test_index_field_tolerates_emphasis_variants(self):
        for line, expected in (("- **Status**: Active", "Active"),
                               ("Status: Active", "Active"),
                               ("- Status: Active", "Active"),
                               ("* _Status_: Active", "Active"),
                               ("- **Status**:", "")):
            self.assertEqual(self.owl._index_field(line, "Status"), expected, line)
        self.assertIsNone(self.owl._index_field("- **Spec**: docs/x.md", "Status"))
        self.assertIsNone(self.owl._index_field("Statuses are fine", "Status"))

    def test_find_in_index_stops_at_next_feature(self):
        index = ("### 20260101-a\n- **Status**: Active\n"
                 "- **Spec**: docs/specs/20260101-a/spec.md\n- **Summary**: A.\n\n"
                 "### 20260102-b\n- **Status**: Done\n"
                 "- **Spec**: docs/specs/20260102-b/spec.md\n- **Summary**: B.\n")
        info = self.owl._find_in_index(index, "20260101-a")
        self.assertEqual(info["status"], "Active")
        self.assertEqual(info["summary"], "A.")

    def test_retrieve_missing_feature_errors(self):
        (self.docs / "athena-index.md").write_text("# Athena Feature Index\n", encoding="utf-8")
        self.assertIn("error", self.owl.retrieve_feature("20260101-nope"))


class TestQueryCommands(OwlTestCase):
    def test_show_cr_and_d(self):
        cr = self.owl.add_request("The request body")["id"]
        d = self.owl.add_decision("The decision body", cr=cr)["id"]
        self.owl.add_request("Another entry")
        shown = self.owl.show_entry(cr)
        self.assertIn("The request body", shown)
        self.assertNotIn("Another entry", shown)
        self.assertIn("The decision body", self.owl.show_entry(d))

    def test_show_fr(self):
        make_feature(self.specs, "20260101-feat")
        shown = self.owl.show_entry("FR-001")
        self.assertIn("[20260101-feat]", shown)
        self.assertIn("FR-001: Do the thing.", shown)

    def test_show_not_found_and_unsupported(self):
        self.assertIn("not found", self.owl.show_entry("CR-19990101-0000"))
        self.assertIn("unsupported", self.owl.show_entry("Q-123"))

    def test_why_chain(self):
        make_feature(self.specs, "20260101-feat",
                     next_tasks=["T-002: build it. (Implements: FR-001)"])
        out = self.owl.why("FR-001")
        self.assertIn("[20260101-feat]", out)
        self.assertIn("FR-001: Do the thing.", out)
        self.assertIn("CR-20260101-1200", out)
        self.assertIn("T-002: build it.", out)

    def test_why_not_found(self):
        self.assertIn("not found", self.owl.why("FR-999"))

    def test_why_resolves_reformatted_four_digit_traceability(self):
        """Defect 4: the plain `- FR-1408: ... (Sources: ...)` shape, four-digit
        FR and task IDs, and the `(Implements: ...)` tag on the task header line."""
        fdir = self.specs / "20260725-ha-free-claire"
        fdir.mkdir(parents=True)
        (fdir / "spec.md").write_text(
            "# Feature Spec\n\nStatus: Active\n\n## Summary\n\nHA-free runtime.\n\n"
            "Functional requirements:\n"
            "- FR-1408: Memory safety. The blocking spike T-1423 must pass. "
            "(Sources: CR-20260725-1328; D-20260726-1128)\n", encoding="utf-8")
        (fdir / "tasks.md").write_text(
            "# Tasks\n\n## NEXT\n\n"
            "- T-1423: BLOCKING feasibility spike (Implements: FR-1407, FR-1408)\n"
            "  - Gate order: no other task starts until this passes.\n", encoding="utf-8")
        out = self.owl.why("FR-1408")
        self.assertIn("[20260725-ha-free-claire]", out)
        self.assertIn("FR-1408: Memory safety.", out)
        self.assertIn("CR-20260725-1328", out)
        self.assertIn("D-20260726-1128", out)
        self.assertIn("T-1423: BLOCKING feasibility spike", out)
        self.assertNotIn("FR-1407:", out)  # a neighbour ID must not be pulled in

    def test_task_id_regex_accepts_more_than_three_digits(self):
        """A fixed \\d{3} width matched no modern task ID, so the commit lookup
        silently lost its per-task narrowing."""
        self.assertEqual(re.findall(TASK_ID_RE, "T-001 T-1423 T-14231 FR-1408"),
                         ["T-001", "T-1423", "T-14231"])


class TestMigrate(OwlTestCase):
    def test_migrate_splits_blocks(self):
        make_feature(self.specs, "20260101-feat")
        (self.docs / "progress.txt").write_text(
            "Session: 2026-01-05 10:00\nFeature: 20260101-feat\nGoal: g\n\n"
            "DONE\n- something\n"
            "Session: 2026-01-06 11:00\nFeature: 20250101-gone\nGoal: g2\n\n"
            "NOTES\n- orphan\n", encoding="utf-8")
        result = self.owl.migrate()
        self.assertTrue(result.get("success"))
        self.assertEqual(result["sessions_migrated"], 1)
        self.assertEqual(result["sessions_to_legacy"], 1)
        self.assertFalse((self.docs / "progress.txt").exists())
        notes = (self.specs / "20260101-feat" / "notes.md").read_text()
        self.assertIn("## S-20260105-1000", notes)
        self.assertIn("- something", notes)
        legacy = (self.docs / "audit" / "progress-legacy.txt").read_text()
        self.assertIn("20250101-gone", legacy)
        self.assertIn("- orphan", legacy)

    def test_migrate_idempotent(self):
        result = self.owl.migrate()
        self.assertTrue(result.get("skipped"))

    def test_prune_done_graceful_without_progress(self):
        result = self.owl.prune_done()
        self.assertTrue(result.get("success"))
        self.assertTrue(result.get("skipped"))


class TestPrunePrd(OwlTestCase):
    PRD = (
        "# PRD: Test\n\n## Metadata\n"
        "- **Status:** Active\n"
        "- **Inputs:** [CR-1](r.md#a), [CR-2](r.md#b), [CR-3](r.md#c), [CR-4](r.md#d)\n"
        "- **Decisions:** [D-1](d.md#a), [D-2](d.md#b), [D-3](d.md#c)\n\n"
        "## Functional requirements\n"
        "- FR-T-001: Keep me. (Sources: CR-1)\n\n"
        "## Next / backlog\n"
        "- Shipped (v1, CR-1): `docs/specs/20250101-old-feat/spec.md`.\n"
        "- Implemented in: `docs/specs/20250102-older/spec.md`.\n"
        "- Planned in: `docs/specs/20260101-live/spec.md`.\n"
        "- Open item: do something later.\n"
    )

    def test_prune_prd_archives_and_points(self):
        make_feature(self.specs, "20260101-live")  # active feature cited by one backlog line
        (self.docs / "PRD.md").write_text(self.PRD, encoding="utf-8")
        result = self.owl.prune_prd()
        self.assertTrue(result.get("success"))
        self.assertEqual(result["lines_archived"], 4)  # 2 metadata lists + 2 closed backlog lines
        prd = (self.docs / "PRD.md").read_text()
        self.assertIn("- **Inputs:** see docs/audit/prd-archive.md", prd)
        self.assertIn("- **Decisions:** see docs/audit/prd-archive.md", prd)
        self.assertIn("FR-T-001: Keep me.", prd)
        self.assertIn("Planned in: `docs/specs/20260101-live/spec.md`", prd)
        self.assertIn("Open item: do something later.", prd)
        self.assertNotIn("20250101-old-feat", prd)
        archive = (self.docs / "audit" / "prd-archive.md").read_text()
        self.assertIn("[CR-1](r.md#a)", archive)
        self.assertIn("20250101-old-feat", archive)
        self.assertIn("20250102-older", archive)

    def test_prune_prd_idempotent(self):
        make_feature(self.specs, "20260101-live")
        (self.docs / "PRD.md").write_text(self.PRD, encoding="utf-8")
        self.owl.prune_prd()
        second = self.owl.prune_prd()
        self.assertTrue(second.get("skipped"))

    def test_prune_prd_missing_and_lean(self):
        self.assertIn("error", self.owl.prune_prd())
        (self.docs / "PRD.md").write_text("# PRD\n\n## Goals\n- g1\n", encoding="utf-8")
        result = self.owl.prune_prd()
        self.assertTrue(result.get("skipped"))


class TestArchiveLogs(OwlTestCase):
    """archive-logs / archive-specs: lean hot path, nothing lost, lookups keep working."""

    TODAY = datetime(2026, 10, 29)

    def write_logs(self):
        # An old entry whose body holds a pasted single-# heading and a stray ## one.
        (self.docs / "requests.md").write_text(
            "# Customer Requests (append-only)\n\n"
            "## CR-20260801-0900\n\n### Request:\nold ask\n\n# Codex brief\nnot an entry\n\n"
            "## CR-20260805-1000\n\nsecond old ask\n\n"
            "## CR-20261020-1000\n\nrecent ask\n", encoding="utf-8")
        (self.docs / "decisions.md").write_text(
            "# Decisions (append-only)\n\n"
            "## D-20260801-0901\nold decision\n\n"
            "## D-20261020-1001\nrecent decision\n", encoding="utf-8")

    def test_old_entries_move_to_month_shards_and_recent_stay(self):
        self.write_logs()
        result = self.owl.archive_logs(keep_days=30, keep_last=1, today=self.TODAY)
        self.assertTrue(result["success"])
        live = (self.docs / "requests.md").read_text()
        self.assertIn("## CR-20261020-1000", live)
        self.assertNotIn("CR-20260801-0900", live)
        self.assertTrue(live.startswith("# Customer Requests (append-only)"))
        shard = (self.docs / "audit" / "requests-2026-08.md").read_text()
        self.assertIn("## CR-20260801-0900", shard)
        self.assertIn("# Codex brief", shard)
        self.assertIn("## CR-20260805-1000", shard)
        self.assertIn("recent decision", (self.docs / "decisions.md").read_text())

    def test_keep_last_protects_newest_entries_even_if_old(self):
        self.write_logs()
        self.owl.archive_logs(keep_days=1, keep_last=2, today=datetime(2027, 6, 1))
        live = (self.docs / "requests.md").read_text()
        self.assertIn("CR-20260805-1000", live)
        self.assertIn("CR-20261020-1000", live)
        self.assertNotIn("CR-20260801-0900", live)

    def test_show_and_validator_still_find_archived_entries(self):
        self.write_logs()
        self.owl.archive_logs(keep_days=30, keep_last=1, today=self.TODAY)
        shown = self.owl.show_entry("CR-20260801-0900")
        self.assertIn("old ask", shown)
        self.assertIn("[archived: docs/audit/requests-2026-08.md]", shown)
        self.assertIn("old decision", self.owl.show_entry("D-20260801-0901"))
        self.assertIn("not found", self.owl.show_entry("CR-20250101-0000"))

    def test_second_run_is_a_no_op_and_dry_run_writes_nothing(self):
        self.write_logs()
        before = (self.docs / "requests.md").read_text()
        dry = self.owl.archive_logs(keep_days=30, keep_last=1, dry_run=True, today=self.TODAY)
        self.assertEqual(dry["logs"]["requests"]["archived"], 2)
        self.assertEqual((self.docs / "requests.md").read_text(), before)
        self.assertFalse((self.docs / "audit").exists())
        self.owl.archive_logs(keep_days=30, keep_last=1, today=self.TODAY)
        shard = (self.docs / "audit" / "requests-2026-08.md").read_text()
        again = self.owl.archive_logs(keep_days=30, keep_last=1, today=self.TODAY)
        self.assertEqual(again["logs"]["requests"]["archived"], 0)
        self.assertEqual((self.docs / "audit" / "requests-2026-08.md").read_text(), shard)

    def test_no_entry_is_lost_or_duplicated(self):
        self.write_logs()
        self.owl.archive_logs(keep_days=30, keep_last=1, today=self.TODAY)
        text = (self.docs / "requests.md").read_text() + (
            self.docs / "audit" / "requests-2026-08.md").read_text()
        for entry_id in ("CR-20260801-0900", "CR-20260805-1000", "CR-20261020-1000"):
            self.assertEqual(text.count(f"## {entry_id}"), 1, entry_id)

    def test_appending_after_archive_still_works(self):
        self.write_logs()
        self.owl.archive_logs(keep_days=30, keep_last=1, today=self.TODAY)
        added = self.owl.add_request("new ask after archive")
        self.assertIn(f"## {added['id']}", (self.docs / "requests.md").read_text())

    def test_validator_accepts_ids_that_moved_to_shards(self):
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
        from validate_traceability_links import validate_repo
        self.write_logs()
        make_feature(self.specs, "20260101-live")
        (self.specs / "20260101-live" / "spec.md").write_text(
            "# Spec\n\nStatus: Active\n\n- FR-001: x. (Sources: CR-20260801-0900; D-20260801-0901)\n",
            encoding="utf-8")
        (self.docs / "PRD.md").write_text("# PRD\n", encoding="utf-8")
        (self.specs / "20260101-live" / "tasks.md").write_text(
            "# Tasks\nSpec: docs/specs/20260101-live/spec.md\n## NEXT\n- T-1: x. (Implements: FR-001)\n",
            encoding="utf-8")
        self.owl.archive_logs(keep_days=30, keep_last=1, today=self.TODAY)
        errors = [e for e in validate_repo(self.tmp) if "unknown" in e]
        self.assertEqual(errors, [])


class TestArchiveSpecs(OwlTestCase):
    FULL = (
        "# Feature Spec: 20260101-done\n\nStatus: Done\n\n## Summary\n\nShipped the thing.\n\n"
        "## Design\n\n" + "Long design prose line.\n" * 200 +
        "\n## Requirements\n\n"
        "- FR-001: Do it. (Sources: CR-20260101-1200)\n\n"
        "### Notes\n\n" + "More history.\n" * 100 +
        "\n1. Given a, when b, then c. (Verifies: FR-001)\n")

    def make_done(self, fid="20260101-done"):
        fdir = make_feature(self.specs, fid, status="Done")
        (fdir / "spec.md").write_text(self.FULL.replace("20260101-done", fid), encoding="utf-8")
        return fdir

    def test_done_spec_is_condensed_and_full_text_kept(self):
        fdir = self.make_done()
        result = self.owl.archive_specs()
        self.assertEqual(result["specs"][0]["feature_id"], "20260101-done")
        condensed = (fdir / "spec.md").read_text()
        self.assertLess(len(condensed), 700)
        for kept in ("# Feature Spec", "Status: Done", "Shipped the thing.",
                     "- FR-001: Do it.", "Verifies: FR-001",
                     "Archived-Full: docs/audit/specs/20260101-done.md"):
            self.assertIn(kept, condensed)
        self.assertNotIn("Long design prose", condensed)
        full = (self.docs / "audit" / "specs" / "20260101-done.md").read_text()
        self.assertEqual(full, self.FULL)

    def test_active_spec_is_never_condensed(self):
        make_feature(self.specs, "20260102-live")
        before = (self.specs / "20260102-live" / "spec.md").read_text()
        self.owl.archive_specs()
        self.assertEqual((self.specs / "20260102-live" / "spec.md").read_text(), before)

    def test_condensed_spec_keeps_index_summary_status_and_fr_lookup(self):
        self.make_done()
        before = self.owl.update_index()
        self.owl.archive_specs()
        after = self.owl.update_index()
        self.assertEqual(after["archived"], before["archived"])
        self.assertEqual(self.owl.retrieve_feature("20260101-done")["summary"],
                         "Shipped the thing.")
        self.assertIn("FR-001: Do it.", self.owl.show_entry("FR-001"))

    def test_second_run_skips_and_restore_round_trips(self):
        fdir = self.make_done()
        self.owl.archive_specs()
        again = self.owl.archive_specs()
        self.assertEqual(again["specs"], [])
        self.assertTrue(self.owl.restore_spec("20260101-done")["success"])
        self.assertEqual((fdir / "spec.md").read_text(), self.FULL)
        self.assertFalse((self.docs / "audit" / "specs" / "20260101-done.md").exists())
        self.assertIn("error", self.owl.restore_spec("20260101-done"))

    def test_dry_run_writes_nothing(self):
        fdir = self.make_done()
        result = self.owl.archive_specs(dry_run=True)
        self.assertGreater(result["specs"][0]["bytes_saved"], 0)
        self.assertEqual((fdir / "spec.md").read_text(), self.FULL)
        self.assertFalse((self.docs / "audit").exists())

    def test_archive_command_condenses_unless_keep_spec(self):
        self.docs.joinpath("athena-index.md").write_text("# Index\n", encoding="utf-8")
        fdir = self.make_done()
        kept = self.owl.archive_feature("20260101-done", keep_spec=True)
        self.assertFalse(kept["spec_condensed"])
        self.assertEqual((fdir / "spec.md").read_text(), self.FULL)
        done = self.owl.archive_feature("20260101-done")
        self.assertTrue(done["spec_condensed"])
        self.assertIn("Archived-Full:", (fdir / "spec.md").read_text())


if __name__ == "__main__":
    unittest.main()
