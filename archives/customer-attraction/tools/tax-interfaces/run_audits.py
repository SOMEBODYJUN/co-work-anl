#!/usr/bin/env python3
"""Replay the three tax-interface counterexamples without solver dependencies."""
from argparse import ArgumentParser
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ARCHIVE = HERE.parents[1]


def main():
    if not __debug__:
        raise SystemExit("Run without -O: the preserved audits use assertions.")
    started = datetime.now(timezone.utc).isoformat()
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=False)

    def execute(name, script, *extra):
        proc = subprocess.run([sys.executable, str(HERE / script), *map(str, extra)],
                              capture_output=True, text=True, check=True)
        if name == "root_original":
            (out / (name + ".stdout.txt")).write_text(proc.stdout)
        if proc.stderr:
            (out / (name + ".stderr.txt")).write_text(proc.stderr)
        return proc.stdout

    # Verify that the preserved root JSON and both embedded-table implementations
    # actually refer to the same unit-customer membership instance.
    spec = importlib.util.spec_from_file_location("root_original", HERE / "root_tax_original.py")
    original = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(original)
    root_input = json.loads((ARCHIVE / "evidence/tax-interfaces/inputs/root_tax_failure.json").read_text())
    groups = Counter()
    for row in root_input["customers"]:
        membership = "".join(root_input["topics"][i] for i in row["topics"])
        groups[membership] += row["multiplicity"]
    assert root_input["players"] == 4 and root_input["topics"] == list("ABCDEF")
    assert dict(groups) == original.GROUPS

    original_text = execute("root_original", "root_tax_original.py")
    assert "Verified all 259 ordered decision histories and 1295 deviations." in original_text
    bridge = json.loads(execute("bridge", "audits/customer_attraction_tax_bridge.py"))
    (out / "bridge.json").write_text(json.dumps(bridge, ensure_ascii=False, indent=2) + "\n")
    general = json.loads(execute("general", "audits/customer_attraction_general_tax.py"))
    (out / "general.json").write_text(json.dumps(general, ensure_ascii=False, indent=2) + "\n")
    root = json.loads(execute("root_independent", "audits/customer_attraction_root_tax_upload_independent.py",
                              "--output-dir", out / "root_independent"))
    assert root["input_groups"] == dict(groups)
    assert bridge["first_step_bridge_violation"] == "1/2"
    assert bridge["total_tax_is_equality"] is True
    small = general["nine_unit_customer_example"]
    large = general["ninety_six_unit_customer_companion"]
    assert small["total_tax_gap"] == "1/20" and large["total_tax_gap"] == "4/11"
    assert small["root_checked_histories"] == 1093
    assert large["root_checked_histories"] is None
    assert (root["W"], root["OPT4"], root["tau"], root["RT_gap"]) == (38, 61, "45/2", "1/2")
    assert root["profitable_deviations"] == 0
    assert root["static_safety"]["v4"] == "9"
    assert Fraction(root["static_safety"]["W_minus_4v4"]) == 2

    dependencies = sorted(HERE.rglob("*.py")) + sorted((ARCHIVE / "evidence/tax-interfaces/inputs").glob("*.json"))
    summary = {
        "status": "PASS",
        "scope": "Three explicit tax-interface counterexamples; not a general or six-provider half-coverage verdict.",
        "arithmetic": "fractions.Fraction; deterministic; no seed, float tolerance or external solver",
        "python_version": platform.python_version(),
        "run_started_utc": started,
        "git_base_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ARCHIVE, text=True).strip(),
        "bridge": {"nodes": bridge["verified_decision_histories"],
                   "nonself_deviations": bridge["verified_actual_continuation_deviations"], "gap": "1/2"},
        "background": {"small_gap": "1/20", "large_gap": "4/11",
                       "subgame_nodes_each": small["subgame_checked_histories"],
                       "small_root_nodes": small["root_checked_histories"],
                       "large_root_enumerated": False},
        "root": {"nodes": root["nodes"], "nonself_deviations": root["deviations"],
                 "gap": "1/2", "v4": "9", "negative_control_rejected": bool(root["negative_control_profitable_deviations"])},
        "sha256": {str(p.relative_to(ARCHIVE)): hashlib.sha256(p.read_bytes()).hexdigest() for p in dependencies},
    }
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
