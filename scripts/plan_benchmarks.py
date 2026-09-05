#!/usr/bin/env python3
"""Print an unrun Athena comparison matrix. No models, network or file writes."""
import argparse
import json
import re
from pathlib import Path

BASELINE = "f71b8fc1ef1f57dfe3c78b7e25861c0da1361965"
CANDIDATE = "1dd6243f74d1e356511792e76932f7ae4d9aa7c2"
CONFIG_FIELDS = ("label", "model_id", "harness", "reasoning", "tools_permissions_id",
                 "budget", "fixture_id", "installation_profile", "cache_policy")


def build_plan(suite, configurations, repetitions=1, baseline=BASELINE, candidate=CANDIDATE):
    if not isinstance(repetitions, int) or not 1 <= repetitions <= 100:
        raise ValueError("repetitions must be an integer from 1 to 100")
    if any(not re.fullmatch(r"[0-9a-f]{40}", sha) for sha in (baseline, candidate)):
        raise ValueError("arm revisions must be full 40-character commit SHAs")
    if baseline == candidate:
        raise ValueError("baseline and candidate must differ")
    if not isinstance(configurations, list) or not configurations:
        raise ValueError("provide a nonempty configuration list")
    labels = set()
    for config in configurations:
        if not isinstance(config, dict):
            raise ValueError("each configuration must be an object")
        for key in CONFIG_FIELDS:
            value = config.get(key)
            if not isinstance(value, str) or not value.strip() or "REPLACE_" in value:
                raise ValueError(f"configuration needs a concrete {key}")
        if config["label"] in labels:
            raise ValueError("configuration labels must be unique")
        labels.add(config["label"])
    cases = suite["cases"]
    if len({case["id"] for case in cases}) != len(cases) or not cases:
        raise ValueError("case IDs must be unique and nonempty")
    runs = []
    for repetition in range(1, repetitions + 1):
        for config_index, config in enumerate(configurations):
            for case_index, case in enumerate(sorted(cases, key=lambda c: c["priority"])):
                arms = [("baseline", baseline), ("candidate", candidate)]
                if (repetition + config_index + case_index) % 2 == 0:
                    arms.reverse()
                for arm, revision in arms:
                    runs.append({"run_id": f"run-{len(runs)+1:04d}", "status": "unrun",
                                 "repetition": repetition, "case_id": case["id"],
                                 "arm": arm, "arm_commit": revision,
                                 "configuration": dict(config), "prompt": case["prompt"],
                                 "case_spec": f"references/benchmark-cases.json#{case['id']}"})
    return {"suite": suite["suite"], "status": "unrun", "suite_commit": None,
            "instructions": "Record the suite commit before execution. This plan is not a model run.",
            "run_count": len(runs), "runs": runs}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--repetitions", type=int, default=1)
    parser.add_argument("--baseline", default=BASELINE)
    parser.add_argument("--candidate", default=CANDIDATE)
    args = parser.parse_args()
    try:
        suite = json.loads((Path(__file__).resolve().parents[1] /
                            "references/benchmark-cases.json").read_text())
        plan = build_plan(suite, json.loads(args.config.read_text()), args.repetitions,
                          args.baseline, args.candidate)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.error(str(exc))
    print(json.dumps(plan, indent=2))


if __name__ == "__main__":
    main()
