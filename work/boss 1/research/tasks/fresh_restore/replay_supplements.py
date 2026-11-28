"""Run the standalone research and household programs from the frozen clone's root."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

FROZEN = "1580e869769a9410b88d040acf08bab394c6f9d2"
WORK = Path("work/boss 1")
RESEARCH = WORK / "research"
TASKS = RESEARCH / "tasks"
PROOF = TASKS / "fresh_restore"
LOGS = PROOF / "logs"
PYTHON = Path(".venv-methods/bin/python")
HOUSEHOLD = TASKS / "household_engine"
TEMP = Path(".fresh-restore-runtime")
runs = []


def sha(data):
    return hashlib.sha256(data).hexdigest()


def frozen_bytes(path):
    return subprocess.check_output(["git", "show", f"{FROZEN}:{path}"])


def stat(path):
    if not path.exists():
        return None
    st = path.stat()
    return {"sha256": sha(path.read_bytes()), "bytes": st.st_size, "mtime_ns": st.st_mtime_ns}


def run(label, command, inputs, outputs):
    """Map each output to the tracked path which supplies its reference bytes."""
    argv = [str(x) for x in command]
    before = {str(path): stat(path) for path in outputs}
    inputs_info = {
        str(path): {"frozen_sha256": sha(frozen_bytes(path)), "replay_sha256": sha(path.read_bytes())}
        for path in inputs
    }
    start = datetime.now(timezone.utc).isoformat()
    clock = time.monotonic()
    completed = subprocess.run(argv, capture_output=True, check=False)
    seconds = time.monotonic() - clock
    (LOGS / (label + ".stdout")).write_bytes(completed.stdout)
    (LOGS / (label + ".stderr")).write_bytes(completed.stderr)
    files = {}
    for path, reference in outputs.items():
        original = sha(frozen_bytes(reference))
        after = stat(path)
        prior = before[str(path)]
        files[str(path)] = {
            "frozen_reference": str(reference), "frozen_sha256": original,
            "before": prior, "after": after,
            "rewritten_or_created": after is not None and (
                prior is None or after["mtime_ns"] != prior["mtime_ns"]
            ),
            "byte_equal_to_frozen": after is not None and after["sha256"] == original,
        }
    success = (completed.returncode == 0
               and all(row["frozen_sha256"] == row["replay_sha256"] for row in inputs_info.values())
               and all(row["rewritten_or_created"] and row["byte_equal_to_frozen"] for row in files.values()))
    item = {"name": label, "argv_from_clone_root": argv, "started_utc": start, "wall_seconds": seconds,
            "exit_code": completed.returncode, "stdout": f"logs/{label}.stdout",
            "stderr": f"logs/{label}.stderr", "input_and_code": inputs_info, "output_files": files,
            "all_checks_pass": success}
    runs.append(item)
    (PROOF / "supplementary-runs.json").write_text(json.dumps(runs, ensure_ascii=False, indent=2) + "\n")
    print(f"{label}: exit={completed.returncode} regenerated={sum(r['rewritten_or_created'] for r in files.values())}"
          f"/{len(files)} frozen_bytes={sum(r['byte_equal_to_frozen'] for r in files.values())}/{len(files)}",
          flush=True)


def script(label, folder, program, input_names, output_names, executable=PYTHON):
    source = folder / program
    inputs = [source, *(folder / name for name in input_names)]
    outputs = {folder / name: folder / name for name in output_names}
    run(label, [executable, source], inputs, outputs)


def main():
    current = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    if current != FROZEN:
        raise SystemExit(f"Expected {FROZEN}, found {current}")
    LOGS.mkdir(parents=True, exist_ok=True)
    TEMP.mkdir(exist_ok=True)
    script("property-fiscal", TASKS / "property_fiscal", "recompute.py",
           ["property_releases.csv", "fiscal_releases.csv", "supplemental.csv", "cities_price_202610.csv"],
           ["results.json"])
    bank = TASKS / "bank_research"
    bank_inputs = ["icbc_h1_input.json", "lanzhou_h1_input.json", "icbc_q3_input.json", "lanzhou_q3_input.json"]
    run("bank-accounts", [PYTHON, bank / "bank_accounts.py"],
        [bank / "bank_accounts.py", bank / "statement_extract.csv", Path("cncrisis/models.py")],
        {bank / name: bank / name for name in [*bank_inputs, "compute_jobs.json", "capital_and_liquidity_results.json"]})
    history = TASKS / "history_framework_review"
    run("history-framework", [PYTHON, history / "recompute.py"],
        [history / "recompute.py", history / "official_inputs.json", Path("research/models/jst_example/JSTdatasetR6.dta"),
         WORK / "compute/outputs/historical-warning-v1-cdc109f9a414.json"],
        {history / name: history / name for name in ["event_scan.csv", "named_paths.csv", "results.json"]})
    models = RESEARCH / "models"
    for name in ["household_observations", "equity_real_return"]:
        script(name, models, name + ".py", [name + "_input.json"], [name + ".json"])
    script("build-examples", HOUSEHOLD, "build_examples.js", ["engine.js"],
           ["scenarios.json", "synthetic_household.json", "loan_input.json"], "node")
    script("household-node-regressions", HOUSEHOLD, "checks.js",
           ["engine.js", "scenarios.json", "synthetic_household.json"],
           ["checks.json", "sample_summary.json", "legacy_cash_stress.json", "synthetic_strategy_results.csv",
            "sample_baseline_severe_months.json"], "node")
    run("contract-python", [PYTHON, HOUSEHOLD / "compare_python.py"],
        [HOUSEHOLD / "compare_python.py", HOUSEHOLD / "engine.js", HOUSEHOLD / "loan_input.json",
         Path("vendor/numpy-financial/_financial.py"), Path("cncrisis/methods.py")],
        {HOUSEHOLD / name: HOUSEHOLD / name for name in ["loan_work_reference.json", "python_reference_checks.json"]})
    html_sources = ["build.py", "ui.html", "engine.js", "ui.js", "synthetic_household.json"]
    build = HOUSEHOLD / "build.py"
    run("build-example-html", [PYTHON, build], [HOUSEHOLD / name for name in html_sources + ["scenarios.json"]],
        {HOUSEHOLD / "calculator.html": HOUSEHOLD / "calculator.html"})
    formal = WORK / "formal"
    rebuilt = TEMP / "calculator.html"
    run("build-formal-html", [PYTHON, build, "--scenarios", formal / "scenarios.json", "--output", rebuilt],
        [*(HOUSEHOLD / name for name in html_sources), formal / "scenarios.json"],
        {rebuilt: formal / "calculator.html"})
    return 0 if all(row["all_checks_pass"] for row in runs) else 1


if __name__ == "__main__":
    sys.exit(main())
