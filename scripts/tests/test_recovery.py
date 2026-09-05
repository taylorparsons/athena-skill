"""Recovery snapshots must be read-only and distinguish recorded from live state."""
import subprocess
from unittest.mock import patch

from test_owl import OwlTestCase, make_feature


class TestRecovery(OwlTestCase):
    def test_latest_note_does_not_inherit_authority(self):
        make_feature(self.specs, "20260101-active")
        self.owl.add_note("20260101-active", "- Authorization: Old push request\n- Verification: Old pass")
        self.owl.add_note("20260101-active", "- Pending processes: session 42; recheck")
        output = "\n".join(self.owl._recovery_fields("20260101-active"))
        self.assertIn("Authorization: unknown", output)
        self.assertIn("Verification: unknown", output)
        self.assertIn("Pending processes: session 42; recheck", output)
        self.assertNotIn("Old push", output)

    def test_unknown_and_bounded_fields(self):
        self.assertIn("Authorization: unknown", "\n".join(self.owl._recovery_fields("")))
        make_feature(self.specs, "20260101-active")
        self.owl.add_note("20260101-active", "- Verification: " + "x" * 900)
        output = "\n".join(self.owl._recovery_fields("20260101-active"))
        self.assertIn("[truncated]", output)
        self.assertNotIn("x" * 501, output)

    def test_git_snapshot_preserves_index_and_worktree(self):
        def git(*args):
            return subprocess.run(["git", *args], cwd=self.tmp, check=True,
                                  capture_output=True, text=True).stdout.strip()
        git("init")
        file = self.tmp / "sample.txt"
        file.write_text("baseline")
        git("add", "sample.txt")
        git("-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-m", "baseline")
        revision = git("rev-parse", "HEAD")
        file.write_text("staged")
        git("add", "sample.txt")
        file.write_text("working")
        before = (self.tmp / ".git/index").read_bytes()
        output = self.owl.context_block()
        self.assertIn(revision, output)
        self.assertIn("MM sample.txt", output)
        self.assertEqual(before, (self.tmp / ".git/index").read_bytes())
        self.assertEqual("working", file.read_text())
        self.assertEqual("staged", git("show", ":sample.txt"))

    def test_git_unavailable_and_timeout(self):
        self.assertIn("unavailable", "\n".join(self.owl._git_recovery_state()))
        for error in (FileNotFoundError(), subprocess.TimeoutExpired("git", 10)):
            with patch("owl.subprocess.run", side_effect=error):
                self.assertIn("unavailable", "\n".join(self.owl._git_recovery_state()))

    def test_git_status_preserves_unstaged_column(self):
        results = [subprocess.CompletedProcess([], 0, value) for value in
                   ("main\n", "a" * 40 + "\n", " M sample.txt\n")]
        with patch("owl.subprocess.run", side_effect=results):
            lines = self.owl._git_recovery_state()
        self.assertIn("   M sample.txt", lines)

    def test_clean_git_state(self):
        results = [subprocess.CompletedProcess([], 0, value) for value in
                   ("main\n", "a" * 40 + "\n", "")]
        with patch("owl.subprocess.run", side_effect=results):
            self.assertIn("  clean", self.owl._git_recovery_state())

    def test_git_status_is_bounded(self):
        results = [subprocess.CompletedProcess([], 0, value) for value in
                   ("main", "a" * 40, "\n".join(f"?? file{i}" for i in range(25)))]
        with patch("owl.subprocess.run", side_effect=results):
            output = "\n".join(self.owl._git_recovery_state())
        self.assertIn("5 more paths", output)
        self.assertNotIn("file20", output)
