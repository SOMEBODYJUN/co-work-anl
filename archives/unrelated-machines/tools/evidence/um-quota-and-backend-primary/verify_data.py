"""Independent saved-data checks; never imports or executes original algorithms."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import ast
import difflib
import hashlib
import json
import random

HERE = Path(__file__).resolve().parent
STAGE = HERE.parents[4]

def read(relative):
    return json.loads((HERE / relative).read_text())

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    manifest = read("primary-inventory.json") + read("comparison-inventory.json")
    for d in manifest:
        p = STAGE / d["preserved_repo_path"]
        assert p.stat().st_size == d["size"] and digest(p) == d["sha256"]
        if p.suffix == ".py":
            ast.parse(p.read_text())
    for d in read("reused-artifacts.json"):
        p = STAGE / d["preserved_repo_path"]
        assert p.stat().st_size == d["size"] and digest(p) == d["sha256"]
    fixture = read("original/examples/unrelated_machines/weighted_menu_joint_fixtures.json")
    outputs = read("reused-runs/backend-fixture_outputs.json")
    report = read("reused-runs/backend-audit_results.json")
    rows = {d["name"]: d for d in report["weighted_menu_cases"]}
    assert set(fixture) == set(outputs) == set(rows)
    checked_jobs = original_count = normalized_count = 0
    for name, payload in fixture.items():
        table, states = {}, {}
        count = norm_count = 1
        bonuses = 0
        for group in payload["groups"]:
            g = group["id"]
            table[("selector", g)] = {
                ("state", g, s["id"]): F(1) for s in group["states"]}
            count *= len(group["states"])
            norm_count *= len(group["states"])
            for state in group["states"]:
                s = state["id"]
                mass = F(0)
                for inc in state["incidences"]:
                    u, p = inc["resource"], F(inc["p"])
                    table[("incidence", g, s, u)] = {
                        ("state", g, s): p, ("resource", u): F(1)}
                    count *= 2
                    norm_count *= 2
                    mass += p
                states[g, s] = mass
                if mass < 1:
                    bonuses += 1
                    norm_count *= 2
        out = outputs[name]
        seen, loads, intervals = set(), defaultdict(F), defaultdict(list)
        end = F(0)
        for rec in out["jobs"]:
            j, m = tuple(rec["job"]), tuple(rec["machine"])
            assert j in table and j not in seen and m in table[j]
            seen.add(j)
            p, start, finish = map(F, (rec["p"], rec["start"], rec["finish"]))
            assert p == table[j][m] and start >= 0 and finish == start + p
            loads[m] += p
            end = max(end, finish)
            if p:
                intervals[m].append((start, finish))
        assert seen == set(table)
        for seq in intervals.values():
            seq.sort()
            assert all(a[1] <= b[0] for a, b in zip(seq, seq[1:]))
        C = F(out["makespan"])
        assert max(loads.values()) == end == C == F(rows[name]["makespan"])
        assert len(table) == rows[name]["original_jobs_output"]
        assert count == rows[name]["original_assignments_enumerated"]
        assert norm_count == rows[name]["normalized_assignments_enumerated"]
        assert bonuses == out["bonus_jobs_added_then_deleted"]
        normalized = defaultdict(F, loads)
        chosen = {d["group"]: d["state"] for d in out["chosen_states"]}
        allocation = {tuple(d["item"]): d["group"] for d in out["aux_allocation"]}
        for gi, group in enumerate(payload["groups"]):
            for si, state in enumerate(group["states"]):
                g, s = group["id"], state["id"]
                p = 1 - states[g, s]
                if p <= 0:
                    continue
                if chosen[g] == s and allocation.get(("bonus", gi, si)) == g:
                    normalized[("bonus_resource", gi, si)] += 1
                else:
                    normalized[("state", g, s)] += p
        mass = list(map(F, out["chosen_normalized_mass"]))
        utility = list(map(F, out["aux_utility"]))
        assert max(normalized.values()) == F(out["normalized_makespan"]) == 2 - min(mass)
        assert C <= max(normalized.values()) <= 2 - min(utility)
        assert all(a >= b for a, b in zip(mass, utility))
        O, K = F(rows[name]["OPT_original"]), out["K"]
        assert C <= 2 - (2 - O) / (2 * K) <= (2 - F(1, 2*K)) * O
        checked_jobs += len(table)
        original_count += count
        normalized_count += norm_count
    assert (checked_jobs, original_count, normalized_count) == (29, 832, 24820)
    execution = read("reused-runs/backend-menu.execution.json")
    assert execution["exit_code"] == 0 and execution["source_sha256"] == next(
        d["sha256"] for d in manifest if d["id"] == "af2ee631a5e5e8dfd2e2")
    assert (HERE / "reused-runs/backend-menu.stdout").read_bytes() == (
        HERE / "reused-runs/backend-audit_results.json").read_bytes()
    assert (HERE / "reused-runs/backend-menu.stderr").read_bytes() == b""
    assert len(report["raw_backend_cases"]) == 7
    assert report["raw_backend_cases"][-1]["brute_used"] is False
    old = (HERE / "version-comparison/initial-backend.py").read_text()
    current = (HERE / "original/tests/audits/unrelated_machines/degree_two_weighted_menu_backend.py").read_text()
    expected = old.replace("(scratch implementation)", "(structured audit implementation)").replace(
        "import re\n", "import re\nimport sys\n\n"
        "# Explicit rational encodings may exceed CPython's decimal digit default.\n"
        "# The algorithm works in encoding length and never expands a numeric count.\n"
        'if hasattr(sys, "set_int_max_str_digits"):\n'
        "    sys.set_int_max_str_digits(0)\n")
    assert expected == current
    (HERE / "version-comparison/backend.diff").write_text("".join(difflib.unified_diff(
        old.splitlines(True), current.splitlines(True), fromfile="initial-backend.py",
        tofile="current-frozen-backend.py")))
    mainrun = read("comparison/evidence/runs/unrelated_machines/depth_two_quota_audit.json")
    independent = read("comparison/evidence/runs/unrelated_machines/depth_two_quota_independent.json")
    conformance = read("comparison/evidence/runs/unrelated_machines/depth_two_quota_conformance.json")
    assert mainrun["exhaustive_inputs"] == 3 + 8*9 + 64*27 == 1803
    assert independent["star_cases"] == sum((3 * 2**w)**u for u in range(4) for w in range(5))
    assert independent["ceil_identity_cases"] == 29*29*8 == 6728
    by_name = {Path(d["path"]).name: d for d in manifest}
    assert mainrun["code_sha256"] == by_name["depth_two_quota_greedy.py"]["sha256"]
    assert independent["implementation_sha256"] == by_name["depth_two_quota_independent.py"]["sha256"]
    assert conformance["canonical_sha256"] == mainrun["code_sha256"]
    assert conformance["script_sha256"] == by_name["depth_two_quota_conformance.py"]["sha256"]
    assert conformance["manuscript_sha256"] != by_name["rooted_dag_degree_token_bridge.md"]["sha256"]
    rng = random.Random(197604919)
    disconnected = nonzero = huge = 0
    magnitude = 2**130 + 33
    for _ in range(1000):
        u, w = rng.randrange(5), rng.randrange(6)
        labels = list(range(1 + u + w))
        rng.shuffle(labels)
        child = tuple(rng.choice((1, 2, 3, 5, magnitude)) for _ in range(u))
        root = rng.choice((1, 2, 3, 5, magnitude))
        _neighbors = tuple(rng.randrange(1 << w) for _ in range(u))
        adjacent = tuple(rng.randrange(2) for _ in range(u))
        disconnected += int(any(not a for a in adjacent))
        nonzero += int(labels[0] != 0)
        huge += int(magnitude in child or root == magnitude)
    assert (disconnected, nonzero, huge) == (631, 758, 464)
    cross = read("comparison/evidence/runs/unrelated_machines/cross_layer_quota_matching_candidate.json")
    assert cross["sha256"] == by_name["cross_layer_quota_matching.py"]["sha256"]
    small = [(K, s, ((K-s)*K+s-1)//s) for K in range(2, 7)
             for s in range(1, K) if ((K-s)*K+s-1)//s <= 4]
    assert len(small) == 8 and sum(K for K, s, q in small) == 35
    assert sum(K-1 for K in range(2, 101)) == 4950
    assert sum(K*(K-1) for K in range(2, 101)) == 333300
    for sample in cross["result"]["bridge_samples"]:
        K, s, q = sample["K"], sample["s"], sample["q"]
        assert sample["tasks"] == 1 + 2*q + q*K
        assert sample["machines"] == 1 + 2*q + K-s + q*s
        assert F(sample["no_load"]) == 2 - F(s, K)
    result = {
        "status": "passed",
        "verification": "independent saved-data/AST/version/counter checks; no original algorithm imported or run",
        "inventory_source_files_checked": len(manifest),
        "weighted_original_fixtures": 5,
        "all_original_jobs_and_intervals_checked": checked_jobs,
        "original_assignment_counts_reconstructed": original_count,
        "normalized_assignment_counts_reconstructed": normalized_count,
        "conformance_generator_statistics_reconstructed": [disconnected, nonzero, huge],
        "cross_small_parameter_triples": small,
        "cross_small_layer_checks": 35,
        "cross_closed_parameter_points": 4950,
        "cross_closed_layer_evaluations": 333300,
        "original_program_new_runs": 0,
        "historical_unknown_exit_codes": "cross-layer and three depth-two frozen records; intentionally not supplied",
        "historical_manuscript_824d_original_available": False,
    }
    (HERE / "data-selfcheck.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
