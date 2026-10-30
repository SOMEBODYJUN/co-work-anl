"""New runner for four retained original checks; no generic LP backend.

The heterogeneous-macro script is imported only for its corrected boundary
function. Its historical 10,000-round random audit is not rerun here.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys


BASE = Path(__file__).resolve().parent
ROOT = BASE / "original"
SCRIPTS = ROOT / "tests/audits/unrelated_machines"
REPORTS = ROOT / "evidence/runs/unrelated_machines"


def differences(old, new, path=""):
    if type(old) is not type(new):
        return [{"path": path, "old": old, "new": new}]
    if isinstance(old, dict):
        result = []
        for key in sorted(set(old) | set(new)):
            if key not in old or key not in new:
                result.append({"path": path + "/" + key,
                               "old": old.get(key), "new": new.get(key)})
            else:
                result.extend(differences(old[key], new[key], path + "/" + key))
        return result
    if isinstance(old, list):
        if len(old) != len(new):
            return [{"path": path + "/length", "old": len(old), "new": len(new)}]
        return [d for i, (a, b) in enumerate(zip(old, new))
                for d in differences(a, b, path + "/" + str(i))]
    return [] if old == new else [{"path": path, "old": old, "new": new}]


def jobs():
    result = []
    for name, report in [
        ("threshold_cover_recovery", "threshold_cover_recovery_audit.json"),
        ("threshold_cover_recovery_independent", "threshold_cover_recovery_independent_audit.json"),
        ("c2_prefix_full_load_independent", "c2_prefix_full_load_independent_audit.json"),
    ]:
        result.append((name, [sys.executable, str(SCRIPTS / (name + ".py"))],
                       report, "original script main"))
    macro = SCRIPTS / "heterogeneous_macro_uniform_residual.py"
    program = (
        "import importlib.util,json,hashlib;from pathlib import Path;"
        f"p=Path({str(macro)!r});"
        "s=importlib.util.spec_from_file_location('macro_boundary',p);"
        "m=importlib.util.module_from_spec(s);s.loader.exec_module(m);"
        "r={'boundary':m.audit_less_macro_boundary(),"
        "'code_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),"
        "'scope':'corrected cardinality fixture only; earlier random audit unchanged'};"
        "print(json.dumps(r,indent=2))"
    )
    result.append(("heterogeneous_macro_boundary", [sys.executable, "-c", program],
                   "heterogeneous_macro_boundary_repair_audit.json",
                   "original corrected boundary function only; random audit not run"))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    target = args.output_dir.resolve()
    if target.exists() and any(target.iterdir()):
        raise SystemExit("Choose an empty output directory; retained outputs are not overwritten.")
    if target == ROOT or ROOT in target.parents:
        raise SystemExit("Original evidence is immutable.")
    target.mkdir(parents=True, exist_ok=True)

    def run(job):
        name, command, report, mode = job
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
        (target / (name + ".stdout.txt")).write_text(result.stdout)
        (target / (name + ".stderr.txt")).write_text(result.stderr)
        row = {"name": name, "command": command, "mode": mode,
               "cwd": str(ROOT), "returncode": result.returncode,
               "stdout_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(),
               "stderr_bytes": len(result.stderr), "expected_report": report}
        try:
            expected = json.loads((REPORTS / report).read_text())
            row["differences"] = differences(expected, json.loads(result.stdout))
        except json.JSONDecodeError as error:
            row["json_error"] = str(error)
        return row

    with ThreadPoolExecutor(max_workers=3) as pool:
        rows = list(pool.map(run, jobs()))
    (target / "results.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n")
    for row in rows:
        print(row["name"], row["returncode"], "differences", len(row.get("differences", [])))
    return int(any(r["returncode"] or r.get("json_error") or r.get("differences") for r in rows))


if __name__ == "__main__":
    raise SystemExit(main())
