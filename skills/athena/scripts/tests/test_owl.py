#!/usr/bin/env python3
"""Unit tests for owl.py script-gated KB commands (token-diet layout).

Run: python3 -m unittest discover -s scripts/tests -v
"""
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from owl import OwlOfAthena  # noqa: E402


def make_feature(specs_dir: Path, feature_id: str, status: str = "Active",
                 next_tasks=None, in_progress=None, summary="Test feature summary."):
    fdir = specs_dir / feature_id
    fdir.mkdir(parents=True)
    if status == "Active" and next_tasks is None and in_progress is None:
        next_tasks = ["T-001: pending task. (Implements: FR-001)"]
    (fdir / "spec.md").write_text(
        f"# Feature Spec: {feature_id}\n\nStatus: {status}\n\n"
        f"## Summary\n- {summary}\n\n## Requirements\n\n"
        "Functional requirements:\n"
        "- FR-001: Do the thing. (Sources: CR-20260101-1200; D-20260101-1201)\n",
        encoding="utf-8")
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

    def test_context_legacy_layout_reads_progress(self):
        make_feature(self.specs, "20260101-active")
        (self.docs / "progress.txt").write_text(
            "Session: 2026-01-05 10:00\nFeature: 20260101-active\n"
            "Goal: Legacy goal\n\nIN PROGRESS\n- legacy task one\n\n"
            "NEXT\n- legacy task two\n", encoding="utf-8")
        block = self.owl.context_block()
        self.assertIn("Goal: Legacy goal", block)
        self.assertIn("legacy task one", block)
        self.assertIn("legacy task two", block)


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


if __name__ == "__main__":
    unittest.main()
