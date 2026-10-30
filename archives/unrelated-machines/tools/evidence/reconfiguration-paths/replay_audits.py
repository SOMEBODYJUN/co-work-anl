"""Replay retained original exact audits without altering frozen evidence.

This runner is new curation code, not a historical source or theorem proof.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys


BASE = Path(__file__).resolve().parent
ROOT = BASE / "original"


def differences(old, new, path=""):
    if type(old) is not type(new):
        return [{"path": path, "old": old, "new": new}]
    if isinstance(old, dict):
        result = []
        for key in sorted(set(old) | set(new)):
            here = path + "/" + key
            if key not in old or key not in new:
                result.append({"path": here, "old": old.get(key), "new": new.get(key)})
            else:
                result.extend(differences(old[key], new[key], here))
        return result
    if isinstance(old, list):
        if len(old) != len(new):
            return [{"path": path + "/length", "old": len(old), "new": len(new)}]
        return [entry for i, (a, b) in enumerate(zip(old, new))
                for entry in differences(a, b, path + "/" + str(i))]
    return [] if old == new else [{"path": path, "old": old, "new": new}]


def read_report(name):
    return json.loads((ROOT / "evidence/runs/unrelated_machines" / name).read_text())


def expected():
    first = read_report("pruned_first_move_transient_peak_audit.json")["results"]
    active = read_report("permanent_buffer_activation_audit.json")
    held = read_report("held_cycle_assigned_max_path_audit.json")
    return {
        "held_cycle_buffer_path": held["canonical"]["result"],
        "held_cycle_buffer_path_independent": held["independent"]["result"],
        "permanent_buffer_activation": active["canonical"]["result"],
        "permanent_buffer_activation_independent": active["independent"]["result"],
        "pruned_first_move_transient_peak": first["canonical"],
        "pruned_first_move_independent": first["independent"],
        "pruned_first_move_full_input": first["full_input_integration"],
        "lst_support_release_and_threshold_group": read_report("lst_support_release_and_threshold_group_audit.json"),
        "lst_support_release_optimal": read_report("lst_support_release_optimal_audit.json"),
        "bundle_peeling_path_audit": read_report("bundle_peeling_path_audit.json"),
        "bundle_peeling_profile_independent": read_report("bundle_peeling_profile_independent.json"),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    target = args.output_dir.resolve()
    if target == BASE or BASE in target.parents:
        raise SystemExit("Choose a new output directory outside the evidence tree.")
    if target.exists() and any(target.iterdir()):
        raise SystemExit("Output directory must be empty; retained outputs are never overwritten.")
    target.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, old in expected().items():
        command = [sys.executable, str(ROOT / "tests/audits/unrelated_machines" / (name + ".py"))]
        if name == "pruned_first_move_full_input":
            command.append(str(ROOT / "tests/audits/unrelated_machines/pruned_first_move_transient_peak.py"))
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        (target / (name + ".stdout.txt")).write_text(result.stdout)
        (target / (name + ".stderr.txt")).write_text(result.stderr)
        row = {"name": name, "command": command, "cwd": str(ROOT),
               "returncode": result.returncode, "stderr_bytes": len(result.stderr),
               "stdout_sha256": hashlib.sha256(result.stdout.encode()).hexdigest()}
        try:
            row["differences"] = differences(old, json.loads(result.stdout))
        except json.JSONDecodeError as error:
            row["json_error"] = str(error)
        rows.append(row)
        print(name, result.returncode, "differences", len(row.get("differences", [])))
    (target / "results.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n")
    return int(any(r["returncode"] or r.get("json_error") or r.get("differences") for r in rows))


if __name__ == "__main__":
    raise SystemExit(main())
