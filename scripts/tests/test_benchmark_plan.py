"""Check offline matrix construction, not model performance."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from plan_benchmarks import BASELINE, CONFIG_FIELDS, build_plan


class TestBenchmarkPlan(unittest.TestCase):
    def setUp(self):
        self.suite = json.loads((Path(__file__).resolve().parents[2] /
                                "references/benchmark-cases.json").read_text())
        self.configs = [dict.fromkeys(CONFIG_FIELDS, "synthetic-test-setting") for _ in range(3)]
        for index, config in enumerate(self.configs):
            config["label"] = f"synthetic-{index}"

    def test_screen_and_repeated_matrix(self):
        for repetitions, expected in ((1, 48), (3, 144)):
            plan = build_plan(self.suite, self.configs, repetitions)
            self.assertEqual(expected, plan["run_count"])
            self.assertEqual(expected, len({run["run_id"] for run in plan["runs"]}))
            self.assertTrue(all(run["status"] == "unrun" for run in plan["runs"]))
            for config in self.configs:
                for case in self.suite["cases"]:
                    matches = [r for r in plan["runs"] if r["configuration"] == config
                               and r["case_id"] == case["id"]]
                    self.assertEqual(2 * repetitions, len(matches))

    def test_paired_settings_and_alternating_order(self):
        runs = build_plan(self.suite, self.configs)["runs"]
        for i in range(0, len(runs), 2):
            a, b = runs[i:i+2]
            self.assertEqual(a["configuration"], b["configuration"])
            self.assertEqual(a["prompt"], b["prompt"])
            self.assertEqual({"baseline", "candidate"}, {a["arm"], b["arm"]})
        self.assertNotEqual(runs[0]["arm"], runs[2]["arm"])

    def test_rejects_unconfigured_or_duplicate_models(self):
        self.configs[0]["model_id"] = "REPLACE_EXACT_MODEL_ID"
        with self.assertRaises(ValueError):
            build_plan(self.suite, self.configs)
        with self.assertRaises(ValueError):
            build_plan(self.suite, [self.configs[1], self.configs[1]])

    def test_rejects_invalid_revisions_and_repetitions(self):
        for kwargs in ({"candidate": BASELINE}, {"baseline": "main"}, {"repetitions": 0}):
            with self.assertRaises(ValueError):
                build_plan(self.suite, self.configs, **kwargs)
