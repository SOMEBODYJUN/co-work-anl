#!/usr/bin/env python3
"""Read an existing construction certificate; do not run/import its constructor."""
from __future__ import annotations

from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import platform
import sys


ROOT = Path(__file__).resolve().parent
EXPECTED = {
    "source/single_home_cascade_query_separation.py": "c52eb5be01a64e7d13f1e80a7ad1cb5711ed187f0a8ad1000269847d004d59cd",
    "source/single_home_cascade_query_separation_review.md": "3f92aec8afd506dd6ed879311cbb4b48e6482f8e1bd0e4673a62f8b6798bc934",
    "inputs/home_cascade_query_patterns.json": "cfb25856400d6d0ee6b6cea9cb100d8545c97fe2025643f8a62260763fc69573",
    "frozen/single_home_cascade_query_patterns_v2.json": "846ec8efc0e0b3ea2f92e71a548ea4b62aaef60f40c2d74ed2ef8cd001dcf286",
}


def must(value: bool, context: str) -> None:
    if not value:
        raise ValueError(context)


def main() -> None:
    hashes = {}
    for name, expected in EXPECTED.items():
        actual = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        must(actual == expected, "source-byte identity: " + name)
        hashes[name] = actual
    raw = json.loads((ROOT / "inputs/home_cascade_query_patterns.json").read_text())
    run = json.loads((ROOT / "frozen/single_home_cascade_query_patterns_v2.json").read_text())
    must(run["input_sha256"] == hashes["inputs/home_cascade_query_patterns.json"], "run input hash")
    must(run["script_sha256"] == hashes["source/single_home_cascade_query_separation.py"], "run script hash")
    must(run["all_checks_passed"] is True, "historical run success flag")
    machines = raw["machines"]
    jobs = raw["unit_jobs"] + raw["home_jobs"]
    table = {j["id"]: {m: Fraction(v) for m, v in j["processing"].items()} for j in jobs}
    home = {j["id"]: j["home"] for j in raw["home_jobs"]}
    small = {j: table[j][h] for j, h in home.items()}
    u_set = {j["id"] for j in raw["unit_jobs"]}
    q_set = set(raw["queries"])
    n = run["normal_form"]
    must(n["original_machine_count"] == len(machines) == 14, "machine count")
    must(n["original_job_count"] == len(jobs) == 14, "job count")
    must(set(raw["sigma0"]) == set(raw["sigma1"]) == set(table), "input complete schedules")
    must(all(raw["sigma0"][j] == h for j, h in home.items()), "strong home initial schedule")
    d_set = {j for j in home if table[j][raw["sigma1"][j]] == 1}
    z_set = {j for j in home if table[j][raw["sigma1"][j]] == 0}
    must(set(n["D"]) == d_set and set(n["Z"]) == z_set, "D/Z identity")
    must(q_set <= d_set, "queries are strict1 unit exports")
    weights = {j: Fraction(raw.get("nonquery_unit_weights", {}).get(j, "0")) for j in d_set - q_set}
    a_q = {q: set(n["A_q"][q]) for q in q_set}
    union = set()
    for q, support in a_q.items():
        must(support == set(raw["expected_A_q"][q]), "manual support for " + q)
        must(support <= d_set - q_set and not support & union, "support disjointness")
        union |= support
        must(sum((weights[j] for j in support), Fraction()) == Fraction(n["c_q"][q]), "support fee")
    must(set(n["dropped_D"]) == d_set - union - q_set == set(raw["expected_dropped_D"]), "unused D")
    total_fee = sum(weights.values(), Fraction())
    must(total_fee == Fraction(n["sigma1_nonquery_unit_fee_W"]) == 100, "W")
    must(sum((Fraction(c) for c in n["c_q"].values()), Fraction()) == Fraction(n["constructed_full_query_fee"]) == 58, "full family fee")
    # Verify stored paths as finite original edges; no augmenting-path search.
    seen_vertices = set()
    for d, edges in n["augmenting_paths_M1_edges"].items():
        must(d in d_set and edges[0]["job"] == d, "path root")
        vertices = set()
        for index, edge in enumerate(edges):
            j, m = edge["job"], edge["machine"]
            must(j in table and raw["sigma1"][j] == m and table[j][m] == 1, "stored M1 edge")
            vertices.update({("job", j), ("machine", m)})
            if index:
                must(j in u_set and raw["sigma0"][j] == edges[index - 1]["machine"], "stored M0 link")
        must(len(vertices) == 2 * len(edges) and not vertices & seen_vertices, "stored disjoint simple paths")
        seen_vertices |= vertices
        must(edges[-1]["machine"] == n["augmenting_endpoints"][d], "stored endpoint")
    must(set(n["augmenting_paths_M1_edges"]) == d_set, "all D paths")
    must(len(set(n["augmenting_endpoints"].values())) == len(d_set), "endpoint injection")
    must(n["augmenting_endpoints"]["f5"] == raw["expected_endpoints"]["f5"] == "W1", "U-chain endpoint")
    counts = {"schedules": 0, "original_job_assignments": 0, "machine_loads": 0, "jobs_by_machine_entries": 0}

    def check_schedule(record: dict) -> Fraction:
        sigma = record["schedule"]
        must(set(sigma) == set(table), "complete original jobs")
        loads = {m: Fraction() for m in machines}
        actual_jobs = {m: [] for m in machines}
        for job in jobs:
            j = job["id"]
            m = sigma[j]
            must(m in table[j], "legal original endpoint")
            loads[m] += table[j][m]
            actual_jobs[m].append({"job": j, "processing_time": str(table[j][m])})
            counts["original_job_assignments"] += 1
        must(set(record["loads"]) == set(machines), "all original machines")
        for m in machines:
            must(loads[m] == Fraction(record["loads"][m]), "exact load on " + m)
            must(actual_jobs[m] == record["jobs_by_machine"][m], "per-machine original identity on " + m)
            counts["machine_loads"] += 1
            counts["jobs_by_machine_entries"] += len(actual_jobs[m])
        peak = max(loads.values())
        must(peak == Fraction(record["peak"]), "stored peak")
        must(record["peak_machines"] == [m for m in machines if loads[m] == peak], "peak machines")
        must(record["all_original_jobs_checked"] is True and record["all_original_machine_loads_checked"] is True, "historical complete-schedule flags")
        counts["schedules"] += 1
        return peak

    for key in ("sigma0", "sigma1"):
        must(n[key]["schedule"] == raw[key], "stored input schedule identity")
        must(check_schedule(n[key]) <= 1, "strict witness")
    table_summary = []
    must(len(run["patterns"]) == len(raw["audit_patterns"]) == run["pattern_count_explicitly_requested"] == 8, "eight explicit patterns")
    for record, requested in zip(run["patterns"], raw["audit_patterns"], strict=True):
        s = set(record["subset"])
        must(record["subset"] == requested["subset"] and s <= q_set, "original explicit query request")
        peak = check_schedule(record)
        selected = s | set().union(*(a_q[q] for q in s)) if s else set()
        sigma = record["schedule"]
        exported = {j for j in home if table[j][sigma[j]] == 1}
        must(exported == selected == set(record["unit_exports"]), "actual original unit exports")
        must(exported - q_set == set(record["nonquery_unit_exports"]), "actual nonquery exports")
        for j in home:
            expected = raw["sigma1"][j] if j in z_set | selected else home[j]
            must(sigma[j] == expected, "home/unit/zero contract on " + j)
        must(all(sigma[j] in (raw["sigma0"][j], raw["sigma1"][j]) for j in u_set), "original U endpoints")
        moved_u = [j["id"] for j in raw["unit_jobs"] if sigma[j["id"]] != raw["sigma0"][j["id"]]]
        must(moved_u == record["unit_only_jobs_moved_from_sigma0"], "actual U moves")
        delta = max((sum((small[q] for q in q_set - s if home[q] == m), Fraction()) for m in machines), default=Fraction())
        fee = sum((weights[j] for j in exported - q_set), Fraction())
        additive = sum((Fraction(n["c_q"][q]) for q in s), Fraction())
        must(peak <= 1 + delta and delta == Fraction(record["delta_remaining_queries"]), "residual query bound")
        must(Fraction(record["load_bound"]) == 1 + delta, "stored bound")
        must(fee == additive == Fraction(record["actual_nonquery_fee"]) == Fraction(record["additive_fee"]), "exact constructed fee")
        for key, value in (("expected_peak", peak), ("expected_delta", delta), ("expected_fee", fee)):
            must(value == Fraction(requested[key]) == Fraction(record["manual_expectations_checked"][key]), "manual expected value")
        must(record["load_bound_checked"] is True and record["fee_additivity_checked"] is True, "historical pattern check flags")
        if not s or s == q_set:
            must(peak <= 1, "strict endpoint pattern")
        table_summary.append({"subset": record["subset"], "peak": str(peak), "delta": str(delta), "fee": str(fee)})
    actual_subsets = {frozenset(r["subset"]) for r in run["patterns"]}
    fixture_cube = {frozenset(x) for size in range(len(q_set) + 1) for x in itertools.combinations(q_set, size)}
    must(actual_subsets == fixture_cube, "this three-query fixture lists its full cube")
    report = {
        "scope": "Read-only independent arithmetic/identity verification of one previously successful frozen output; constructor not imported or executed; no general theorem or optimality test.",
        "all_checks_passed": True,
        "python_version_this_check": platform.python_version(),
        "historical_run_python_version": run["python_version"],
        "historical_invocation": run["invocation"],
        "source_sha256": hashes,
        "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "counts": counts,
        "patterns": table_summary,
        "all_eight_subsets_of_this_fixture_checked": True,
        "general_boolean_cube_enumeration_claimed": False,
    }
    encoded = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if len(sys.argv) == 2:
        with Path(sys.argv[1]).open("x") as output:
            output.write(encoded)
    else:
        sys.stdout.write(encoded)


if __name__ == "__main__":
    main()
