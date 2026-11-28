"""Verify a completed replay against Git objects; call from the fresh clone with its venv."""
import argparse
import csv
import hashlib
from importlib import metadata
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from zipfile import ZipFile, ZIP_DEFLATED

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

COMMIT = "1580e869769a9410b88d040acf08bab394c6f9d2"
WORK = Path("work/boss 1")
TASK = WORK / "research/tasks"
PROOF = TASK / "fresh_restore"
LOGS = PROOF / "logs"
COMPUTE = WORK / "compute"
SKIP_KEYS = {"executed_at", "elapsed_seconds", "wall_seconds"}
PLANS = ["research/models/compute-initial.json", "research/models/compute-china-activity.json",
         "research/models/compute-audited-history.json", "research/tasks/bank_research/compute_jobs.json"]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def save(name, value):
    (PROOF / name).write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def git(*args):
    return subprocess.check_output(["git", *map(str, args)])


def before(path):
    return git("show", f"{COMMIT}:{path}")


def walk(value, where, omit):
    if isinstance(value, dict):
        clean = {}
        for key, v in value.items():
            path = f"{where}/{key}"
            if key in SKIP_KEYS:
                omit[path] = v
            else:
                clean[key] = walk(v, path, omit)
        return clean
    if isinstance(value, list):
        return [walk(v, f"{where}/{i}", omit) for i, v in enumerate(value)]
    return value


def canonical_sha(value):
    return digest(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode())


def model_snapshot(model, result):
    if model == "early-warning":
        return {"data_sha256": result["data_sha256"],
                "split_rows": {k: v["rows"] for k, v in result["splits"].items()},
                "test_episodes": result["baseline"]["distinct_country_episodes"],
                "baseline_brier": result["baseline"]["brier"],
                "models": {name: {s: {k: estimation[s][k] for k in
                             ["brier", "roc_auc", "detected_episodes", "missed_episodes",
                              "false_alarm_fraction_negative_periods"]} for s in ["raw_test", "calibrated_test"]}
                           for name, estimation in result["models"].items()}}
    if model == "bridge":
        return {k: result[k] for k in ["n_test", "bridge_mae", "lag_baseline_mae"]}
    if model == "nowcast":
        return {k: result[k] for k in ["target_period", "previous_estimate", "updated_estimate", "news_impact",
                                       "news_reconciliation_error", "converged", "em_iterations"]}
    return {"scenarios": len(result["results"]), "unit": result["unit"]}


def compare_models():
    plan = read(PROOF / "replay_plan.json")
    source_plans = [(name, json.loads(before(WORK / name))) for name in PLANS]
    headers = {k: v for k, v in plan.items() if k != "jobs"}
    specs = {j["id"]: (p, j) for p, contents in source_plans for j in contents["jobs"]}
    assert all({k: v for k, v in p.items() if k != "jobs"} == headers for _, p in source_plans)
    assert len(plan["jobs"]) == len(specs) == 11
    frozen = json.loads(before(COMPUTE / "ledger.json"))
    after = read(Path(".fresh-restore-runtime/ledger-replayed.json"))
    base_n = len(frozen["runs"])
    assert after["runs"][:base_n] == frozen["runs"] and after["sessions"][:-1] == frozen["sessions"]
    assert len(after["runs"]) == base_n + len(plan["jobs"]) and len(after["sessions"]) == len(frozen["sessions"]) + 1
    original = {r["id"]: r for r in frozen["runs"]}
    fresh = {r["id"]: r for r in after["runs"][base_n:]}
    assert not set(fresh).intersection(original)
    rows = []
    for job in plan["jobs"]:
        old_id = job["id"].removeprefix("fresh-")
        plan_path, old_job = specs[old_id]
        assert job == {**old_job, "id": "fresh-" + old_id}
        prior, new = original[old_id], fresh[job["id"]]
        assert prior["status"] == new["status"] == "complete" and new["wall_seconds"] > 0
        assert all(prior[k] == new[k] for k in ["fingerprint", "input_sha256", "code_sha256", "environment_sha256", "versions"])
        frozen_path, fresh_path = COMPUTE / prior["output"], COMPUTE / new["output"]
        a, b = before(frozen_path), fresh_path.read_bytes()
        assert digest(a) == prior["output_sha256"] and digest(b) == new["output_sha256"]
        omitted_a, omitted_b = {}, {}
        old_value = walk(json.loads(a), "", omitted_a)
        new_value = walk(json.loads(b), "", omitted_b)
        assert omitted_a.keys() == omitted_b.keys()
        new_result = json.loads(b)["result"]
        inputs = {job["input"]: digest(Path(job["input"]).read_bytes())}
        input_value = read(Path(job["input"]))
        external_reference = None
        if input_value.get("csv"):
            csv_path = Path(input_value["csv"])
            if csv_path.is_absolute():
                external_reference = str(csv_path)
                csv_path = Path(job["input"]).parent / csv_path.name
            inputs[str(csv_path)] = digest(csv_path.read_bytes())
            assert new_result["data_sha256"] == inputs[str(csv_path)]
        assert inputs[job["input"]] == new["input_sha256"]
        assert all(digest(before(path)) == sha for path, sha in inputs.items())
        rows.append({
            "original_id": old_id, "fresh_id": job["id"], "method": job["method"], "original_plan": plan_path,
            "input_kind": new_result["input_kind"], "clone_input_hashes": inputs, "source_spec_external_csv": external_reference, "code_sha256": new["code_sha256"],
            "environment_sha256": new["environment_sha256"], "fingerprint": new["fingerprint"],
            "original_output": str(frozen_path.relative_to(WORK)), "new_output_in_clone": str(fresh_path.relative_to(WORK)),
            "archived_as": "compute/" + new["output"], "frozen_file_sha256": digest(a), "replay_file_sha256": digest(b),
            "byte_equal": a == b, "frozen_normalized_sha256": canonical_sha(old_value),
            "replay_normalized_sha256": canonical_sha(new_value),
            "exact_including_numeric_types_after_timing_removal": canonical_sha(old_value) == canonical_sha(new_value),
            "omitted_timing_fields": {p: {"frozen": omitted_a[p], "replay": omitted_b[p]} for p in omitted_a},
            "core_results": model_snapshot(job["method"], new_result), "runner_wall_seconds": new["wall_seconds"]})
    portable_plan = read(PROOF / "portable-jst-plan.json")
    orig_spec = read(WORK / "research/models/jst_audited_20261127/experiment.json")
    portable_spec = read(PROOF / "portable-jst-experiment.json")
    panel = WORK / "research/models/jst_audited_20261127/panel.csv"
    assert portable_spec == {**orig_spec, "csv": str(panel)}
    assert panel.resolve().is_relative_to(Path.cwd().resolve())
    extended = read(Path(".fresh-restore-runtime/ledger-portable.json"))
    assert extended["runs"][:-1] == after["runs"] and extended["sessions"][:-1] == after["sessions"]
    prow = extended["runs"][-1]
    reference_row = original["historical-warning-audit-v2"]
    assert prow["id"] == portable_plan["jobs"][0]["id"] and prow["status"] == "complete"
    assert all(prow[k] == reference_row[k] for k in ["code_sha256", "environment_sha256", "versions"])
    assert prow["input_sha256"] == digest((PROOF / "portable-jst-experiment.json").read_bytes())
    a = before(COMPUTE / reference_row["output"])
    b = (COMPUTE / prow["output"]).read_bytes()
    oa, ob = {}, {}
    sha_a = canonical_sha(walk(json.loads(a), "", oa))
    sha_b = canonical_sha(walk(json.loads(b), "", ob))
    assert json.loads(b)["result"]["data_sha256"] == digest(panel.read_bytes()) == digest(before(panel))
    assert digest(b) == prow["output_sha256"] and sha_a == sha_b
    portable = {"original_problem": "Frozen experiment has literal source-checkout absolute CSV pathname. Original fresh-* run resolved outside clone. It is excluded as evidence of self-contained input.",
                "original_csv_literal": orig_spec["csv"], "corrected_csv": str(panel),
                "only_semantic_experiment_edit": "csv path", "data_sha256": digest(panel.read_bytes()),
                "job": prow, "session": extended["sessions"][-1], "full_output_sha256": digest(b),
                "frozen_normalized_sha256": sha_a, "replay_normalized_sha256": sha_b,
                "removed_timing_fields": {p: {"frozen": oa[p], "replay": ob[p]} for p in oa},
                "budget_after": read(LOGS / "portable-plan-after.json"), "archived_as": "compute/" + prow["output"],
                "local_input_and_exact_result": sha_a == sha_b}
    return {"algorithm": "Recursively remove only executed_at, elapsed_seconds and wall_seconds, including within arrays. Sort JSON object keys and compare exact serialized values, including floating-point values and numerical types; no tolerance.",
            "portable_corrected_jst": portable, "original_plan_sha256": {k: digest(before(WORK / k)) for k in PLANS},
            "replay_plan_sha256": digest((PROOF / "replay_plan.json").read_bytes()), "headers": headers,
            "source_ledger_original_records_unchanged": True, "new_ledger_records": len(fresh), "old_ledger_records": base_n,
            "batch_session": after["sessions"][-1], "budget_before": read(LOGS / "compute-plan-before.json"),
            "budget_after": read(LOGS / "compute-plan-after.json"), "jobs": rows}


def check_environment():
    locks = ["requirements-methods-lock.txt", "requirements-research.txt"]
    pins = {}
    for path in map(Path, locks):
        for line in path.read_text().splitlines():
            if "==" in line:
                dist, version = line.strip().split("==")
                pins[canonicalize_name(dist)] = version
    installed = {canonicalize_name(d.metadata["Name"]): d.version for d in metadata.distributions()}
    extras = {k: v for k, v in installed.items() if k not in pins}
    extra_deps = []
    for d in metadata.distributions():
        for name in d.requires or []:
            requirement = Requirement(name)
            if canonicalize_name(requirement.name) in extras and (not requirement.marker or requirement.marker.evaluate()):
                extra_deps.append({"package": d.metadata["Name"], "version": d.version, "requires": name})
    cfg = Path(".venv-methods/pyvenv.cfg").read_text().splitlines()
    assert Path(sys.prefix).resolve() == Path(".venv-methods").resolve()
    assert "include-system-site-packages = false" in cfg
    return {"python": sys.version, "node": subprocess.check_output(["node", "--version"], text=True).strip(),
            "platform": f"{platform.system()} {platform.machine()}", "location": "local task container",
            "codespaces": os.environ.get("CODESPACES") == "true",
            "visible_cpus_nproc": int(subprocess.check_output(["nproc"])),
            "affinity_cpus": len(os.sched_getaffinity(0)), "isolated_venv": ".venv-methods",
            "include_system_site_packages": False,
            "original_requirements_sha256": {f: digest(before(f)) for f in locks},
            "exact_project_pin_count": len(pins), "matched_project_pin_count": sum(installed.get(k) == v for k, v in pins.items()),
            "project_exact_pins_vs_installed": {k: {"pinned": v, "installed": installed.get(k)} for k, v in sorted(pins.items())},
            "additional_installed_distributions": extras, "active_requirements_for_extras": extra_deps,
            "full_resolved_constraints": "resolved-environment.txt", "resolved_file_sha256": digest((PROOF / "resolved-environment.txt").read_bytes()),
            "verifications": {"doctor": read(LOGS / "doctor.json"), "pip_check": (LOGS / "pip-check.log").read_text().strip()},
            "historical_environment_fingerprint_scope": "Python, NumPy, pandas, SciPy, statsmodels, scikit-learn, joblib and threadpoolctl. The old ledger did not independently record cloudpickle or pip."}


def household():
    folder = TASK / "household_engine"
    with (folder / "synthetic_strategy_results.csv").open() as f:
        rows = list(csv.DictReader(f))
    strategies = {row["strategy"] for row in rows}
    scenarios = {row["scenario"] for row in rows}
    by_strategy = {key: [r for r in rows if r["strategy"] == key] for key in strategies}
    assert all({r["scenario"] for r in group} == scenarios and len(group) == len(scenarios) for group in by_strategy.values())
    common = {k for k, group in by_strategy.items() if all(r["feasible"] == "true" for r in group)}
    assert all((r["commonFeasible"] == "true") == (r["strategy"] in common) for r in rows)
    assert all(len({r["trajectory"] for r in group}) == 1 for group in by_strategy.values())
    shared_paths = {r["trajectory"] for r in rows if r["strategy"] in common}
    pareto = {r["strategy"] for r in rows if r["pareto"] == "true"}
    assert pareto <= common
    ref = read(folder / "python_reference_checks.json")
    tests = read(folder / "checks.json")
    return {
        "source": "Freshly generated 1,500-row strategy CSV, grouped independently by strategy and scenario. Distinct trajectory IDs are the engine's full-path groupings.",
        "data_kinds": sorted({r["inputKind"] for r in rows}), "policies": len(strategies), "rows": len(rows),
        "scenarios": sorted(scenarios), "common_feasible_policies": len(common), "distinct_common_feasible_trajectories": len(shared_paths),
        "distinct_all_trajectories": len({r["trajectory"] for r in rows}), "pareto_policies": len(pareto),
        "node_checks": tests["checks"], "node_failures": tests["failures"], "numpy_financial": ref["numpy_financial_distribution"],
        "contract_lengths": [r["compared_periods"] for r in ref["comparisons"]],
        "total_contract_periods": sum(r["compared_periods"] for r in ref["comparisons"]),
        "max_absolute_error_cny": max(v for r in ref["comparisons"] for v in r["max_abs_error_cny"].values()),
        "baseline_severe_first_cash_failure_month": next(int(r["firstFailure"]) for r in rows if r["strategy"] == "S000" and r["scenario"] == "severe"),
        "legacy_cash_sensitivity": read(folder / "legacy_cash_stress.json"), "independent_decimal_sale_cash": ref["decimal_sale_cash"],
        "rebuilt_formal_html_sha256": digest(Path(".fresh-restore-runtime/calculator.html").read_bytes())}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--formal-peer", type=Path, help="Path to the matching source checkout, read-only")
    args = parser.parse_args()
    assert git("rev-parse", "HEAD").decode().strip() == COMMIT
    branch = git("branch", "--show-current").decode().strip()
    origin = git("remote", "get-url", "origin").decode().strip()
    assert branch == "work/cn-crisis" and origin == "https://github.com/SOMEBODYJUN/co-work-anl.git"
    formal = {}
    for name in ["report.md", "judgments.json", "scenarios.json", "calculator.html"]:
        path = WORK / "formal" / name
        hashes = {"frozen_object": digest(before(path)), "fresh_worktree": digest(path.read_bytes())}
        if args.formal_peer:
            hashes["source_worktree"] = digest((args.formal_peer / path).read_bytes())
        hashes["match"] = len(set(hashes.values())) == 1
        formal["formal/" + name] = hashes
    state = read(WORK / "research_state.json")
    start = read(LOGS / "session-start.json")
    status = read(LOGS / "status-before.json")
    assert status == read(LOGS / "status-after.json")
    stage_hashes = [{"stage": key, "path": p, "expected_sha256": sha,
                     "observed_sha256": digest((WORK / p).read_bytes())}
                    for key in status["completed_stages"] for p, sha in state["stages"][key]["files"].items()]
    reset_state = {"runtime": state["runtime"], "branch": branch, "origin": origin, "actor_session": start["actor"],
                   "run_id_session": start["run_id"], "cycle_session": start["cycle"],
                   "completed_stages": status["completed_stages"], "remaining_stages": status["remaining_stages"],
                   "state_identical_to_frozen": before(WORK / "research_state.json") == (WORK / "research_state.json").read_bytes(),
                   "state_sha256": digest((WORK / "research_state.json").read_bytes()), "registered_artifact_checks": stage_hashes,
                   "status_during_fresh_ledger": read(LOGS / "status-with-replay-ledger.json")["remaining_stages"],
                   "active_ledger_restored_sha256": digest((COMPUTE / "ledger.json").read_bytes()),
                   "nodes": len(status["graph"]["nodes"]), "edges": len(status["graph"]["edges"]),
                   "unresolved_nodes": status["graph"]["unresolved"], "unresolved_edges": status["graph"]["unresolved_edges"],
                   "session_complete": start["complete"], "review": status["review"], "release": status["release"], "formal": formal}
    environment = check_environment()
    models = compare_models()
    family = household()
    subs = read(PROOF / "supplementary-runs.json")
    files = [f for r in subs for f in r["output_files"].values()]
    topics = {"property": read(TASK / "property_fiscal/results.json"),
              "bank_q3_static_cet1_buffer_headroom_rmb_million": {b["bank"]: b["static_cet1_headroom_to_2027_public_buffer"]
                for b in read(TASK / "bank_research/capital_and_liquidity_results.json")["banks"] if b["bank"].endswith("q3")},
              "history": read(TASK / "history_framework_review/results.json")["sample_sensitivity"],
              "household_observations": read(WORK / "research/models/household_observations.json")["household"],
              "equity_cny": read(WORK / "research/models/equity_real_return.json")}
    okay = {
        "identity_state": reset_state["state_identical_to_frozen"] and start["actor"] == "boss 1"
                          and start["run_id"] == "35440ff34fc845dbaa2b3d94cf6d2c00" and start["cycle"] == 1,
        "stages_graph": len(status["completed_stages"]) == 17 and not reset_state["unresolved_nodes"] and not reset_state["unresolved_edges"]
                        and all(s["expected_sha256"] == s["observed_sha256"] for s in stage_hashes),
        "source_artifacts": all(v["match"] for v in formal.values()),
        "environment_recovered": environment["matched_project_pin_count"] == environment["exact_project_pin_count"] == 38
                                 and environment["verifications"]["doctor"]["vendor_integrity"] == "pass",
        "stock_inputs_all_clone_local": all(not r["source_spec_external_csv"] for r in models["jobs"]),
        "after_path_repair_clone_local": models["portable_corrected_jst"]["local_input_and_exact_result"],
        "fresh_jobs_exact": all(r["exact_including_numeric_types_after_timing_removal"] for r in models["jobs"]),
        "supplements": len(subs) == 10 and len(files) == 24 and all(r["all_checks_pass"] for r in subs),
        "household": (family["policies"], family["rows"], family["common_feasible_policies"], family["distinct_common_feasible_trajectories"],
                      family["distinct_all_trajectories"], family["pareto_policies"], family["node_checks"], family["node_failures"],
                      family["total_contract_periods"]) == (500,1500,134,105,416,6,26,0,146),
        "formal_rebuild": family["rebuilt_formal_html_sha256"] == "9b4e215c09195bdf0ddcda0713f513b3899c7ced87596e67818a975f398d666b"}
    save("environment.json", environment)
    save("comparisons.json", {"frozen_commit": COMMIT, "recovered": reset_state, "runner": models,
                              "supplementary_core_results": topics, "household": family, "checks": okay})
    with ZipFile(PROOF / "raw_evidence.zip", "w", compression=ZIP_DEFLATED) as z:
        for p in sorted(LOGS.iterdir()):
            if p.is_file():
                z.write(p, "logs/" + p.name)
        for item in models["jobs"]:
            z.write(WORK / item["new_output_in_clone"], item["archived_as"])
        correction = models["portable_corrected_jst"]
        z.write(COMPUTE / correction["job"]["output"], correction["archived_as"])
        z.write(Path(".fresh-restore-runtime/ledger-portable.json"), "ledger/replayed-with-portable-jst.json")
        z.writestr("ledger/frozen.json", before(COMPUTE / "ledger.json"))
        z.write(Path(".fresh-restore-runtime/ledger-replayed.json"), "ledger/replayed.json")
        z.write(Path(".venv-methods/pyvenv.cfg"), "environment/pyvenv.cfg")
    print(json.dumps({"checks": okay, "stage_file_checks": len(stage_hashes), "standalone_output_files": len(files),
                      "runner_new_rows": models["new_ledger_records"], "runner_byte_identical": sum(r["byte_equal"] for r in models["jobs"]),
                      "resolved_environment": environment["additional_installed_distributions"], "household": family}, ensure_ascii=False, indent=2))
    return 0 if all(okay.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
