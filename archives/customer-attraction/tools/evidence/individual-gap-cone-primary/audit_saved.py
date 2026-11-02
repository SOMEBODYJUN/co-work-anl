"""Audit the three saved policies and all 350 records; no discovery imports.

Only Python's standard library is used.  This checks the supplied complete
ordered action maps directly, rather than asking an outcome-set solver for a
replacement policy.  Run with a fresh --out path to keep events separate.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import lru_cache
import hashlib
from itertools import combinations, product
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "original/research/workspaces/customer-attraction/R-a5cc2a7008c548ec9b48d8386b872229/global_proof"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_case(m, p):
    best_path = SOURCE / f"gap_n{m}p{p}_best.json"
    run_path = SOURCE / f"gap_n{m}p{p}_run.json"
    best = json.loads(best_path.read_text())
    run = json.loads(run_path.read_text())
    assert set(best) == {"scope", "parameters", "gap_over_ui", "threshold", "a", "u", "W", "OPT", "instance", "strategy", "canonical_verified", "cone_sha256"}
    assert set(run) == {"scope", "parameters", "best_exact_gap_over_ui", "accepted_exact_improvements", "distinct_complete_policies", "elapsed", "records"}
    assert best["parameters"] == run["parameters"]
    assert best["parameters"]["players"] == m and best["parameters"]["topics"] == p
    assert best["threshold"] == m
    assert best["canonical_verified"] is True  # An old claim, checked below independently.
    instance = best["instance"]
    assert set(instance) == {"topics", "customers", "players"}
    assert instance["players"] == m and instance["topics"] == list(map(str, range(p)))
    customers = []
    for item in instance["customers"]:
        assert set(item) == {"topics", "multiplicity"}
        topics = tuple(item["topics"])
        number = item["multiplicity"]
        assert topics == tuple(sorted(set(topics)))
        assert all(type(a) is int and 0 <= a < p for a in topics)
        assert type(number) is int and number > 0
        customers.append((topics, number))

    strategy = best["strategy"]
    assert set(strategy) == {"terminal_counts", "actions"}
    actions = {}
    for entry in strategy["actions"]:
        assert set(entry) == {"history", "action"}
        h, a = tuple(entry["history"]), entry["action"]
        assert h not in actions
        assert all(type(t) is int and 0 <= t < p for t in h)
        assert type(a) is int and 0 <= a < p
        actions[h] = a
    expected = {h for depth in range(m) for h in product(range(p), repeat=depth)}
    assert set(actions) == expected

    @lru_cache(None)
    def terminal(h):
        if len(h) == m:
            return tuple(h.count(a) for a in range(p))
        return terminal(h + (actions[h],))

    @lru_cache(None)
    def utility(q, a):
        return sum((F(number, sum(q[t] for t in topics))
                    for topics, number in customers if a in topics), F(0))

    root_q = terminal(())
    assert list(root_q) == strategy["terminal_counts"]
    root_path = ()
    while len(root_path) < m:
        root_path += (actions[root_path],)
    payoff = [utility(root_q, a) for a in root_path]
    welfare = sum(number for topics, number in customers if any(root_q[a] for a in topics))
    assert sum(payoff) == welfare
    covers = [(sum(number for topics, number in customers if set(topics).intersection(J)), J)
              for J in combinations(range(p), min(m, p))]
    optimum = max(value for value, J in covers)
    optimal_supports = [list(J) for value, J in covers if value == optimum]
    tested_a = best["a"]
    assert type(tested_a) is int and 0 <= tested_a < p and root_q[tested_a] > 0
    tested_u = utility(root_q, tested_a)
    exact_gap = F(optimum - welfare) / tested_u
    assert F(best["u"]) == tested_u and best["W"] == welfare and best["OPT"] == optimum
    assert F(best["gap_over_ui"]) == exact_gap == F(run["best_exact_gap_over_ui"])

    margins = Counter()
    by_depth = {d: Counter() for d in range(m)}
    for h, chosen in actions.items():
        own = utility(terminal(h), chosen)
        for alternative in range(p):
            if alternative == chosen:
                continue
            delta = own - utility(terminal(h + (alternative,)), alternative)
            assert delta >= 0, (h, chosen, alternative, delta)
            margins[delta] += 1
            by_depth[len(h)][delta] += 1

    # Engine records actions in depth-first order; the certificate serializes
    # breadth by depth.  Rebuild the actual hashed ordering, without Engine.
    discovery_order = []

    def preorder(h):
        if len(h) == m:
            return
        discovery_order.append((h, actions[h]))
        for a in range(p):
            preorder(h + (a,))

    preorder(())
    action_hash = hashlib.sha256(repr(discovery_order).encode()).hexdigest()
    assert action_hash == best["cone_sha256"]

    groups = defaultdict(list)
    for a in range(p):
        signature = tuple(i for i, (topics, _) in enumerate(customers) if a in topics)
        groups[signature].append(a)
    coverage_classes = [{"labels": labels, "customer_type_indices": list(sig),
                         "size": sum(customers[i][1] for i in sig)}
                        for sig, labels in groups.items()]

    records = run["records"]
    hashes = set()
    groups_by_policy = defaultdict(list)
    for index, rec in enumerate(records):
        assert set(rec) == {"step", "a", "proposal_gap_over_ui", "threshold", "portfolio", "cone_rows", "cone_sha256"}
        assert type(rec["step"]) is int and 0 <= rec["step"] < run["parameters"]["steps"]
        assert type(rec["a"]) is int and 0 <= rec["a"] < p
        assert rec["threshold"] == m
        assert math.isfinite(rec["proposal_gap_over_ui"])
        J = rec["portfolio"]
        assert J == sorted(set(J)) and len(J) == min(m, p)
        assert all(type(a) is int and 0 <= a < p for a in J)
        assert type(rec["cone_rows"]) is int and rec["cone_rows"] > 0
        sha = rec["cone_sha256"]
        assert len(sha) == 64 and all(ch in "0123456789abcdef" for ch in sha)
        hashes.add(sha)
        groups_by_policy[sha].append(index)
    assert len(hashes) == run["distinct_complete_policies"]
    for indices in groups_by_policy.values():
        chosen_records = [records[i] for i in indices]
        assert len({r["step"] for r in chosen_records}) == 1
        assert len({r["a"] for r in chosen_records}) == 1
        assert len({r["cone_rows"] for r in chosen_records}) == 1
        assert 1 <= len(chosen_records) <= 2
        assert len({tuple(r["portfolio"]) for r in chosen_records}) == len(chosen_records)
    assert action_hash in hashes
    assert all(actions[h] == 0 for h in actions)
    assert len(actions) == sum(p ** d for d in range(m))
    assert sum(margins.values()) == len(actions) * (p - 1)
    return {
        "players": m, "topics": p, "primary_files": {
            best_path.name: {"size": best_path.stat().st_size, "sha256": digest(best_path)},
            run_path.name: {"size": run_path.stat().st_size, "sha256": digest(run_path)}},
        "customers": instance["customers"], "customer_total": sum(n for _, n in customers),
        "coverage_classes": coverage_classes, "all_prescribed_actions": [0],
        "root_history": list(root_path), "root_counts": list(root_q),
        "root_payoffs": list(map(str, payoff)), "W": welfare, "OPT": optimum,
        "optimal_supports": optimal_supports, "tested_topic": tested_a,
        "tested_payoff": str(tested_u), "gap_over_ui": str(exact_gap),
        "half_margin": 2 * welfare - optimum, "bridge_margin": str(m * tested_u - (optimum - welfare)),
        "checked_histories": len(actions), "checked_proper_deviations": sum(margins.values()),
        "zero_proper_deviations": margins[F(0)],
        "strict_proper_deviations": sum(v for k, v in margins.items() if k > 0),
        "minimum_margin": str(min(margins)),
        "margin_histogram": {str(k): v for k, v in sorted(margins.items())},
        "depth_checks": {str(d): {"proper": sum(hist.values()), "zero": hist[F(0)],
                                      "strict": sum(v for k, v in hist.items() if k > 0)}
                         for d, hist in by_depth.items()},
        "discovery_action_hash_matches": action_hash,
        "saved_run": {"parameters": run["parameters"], "elapsed_literal": run["elapsed"],
                      "accepted_exact_improvements_field": run["accepted_exact_improvements"],
                      "distinct_policies": len(hashes), "records": len(records),
                      "observed_steps": sorted({r["step"] for r in records}),
                      "observed_max_step": max(r["step"] for r in records),
                      "topics_tested": sorted({r["a"] for r in records}),
                      "comparison_supports_seen": len({tuple(r["portfolio"]) for r in records}),
                      "proposal_min": min(r["proposal_gap_over_ui"] for r in records),
                      "proposal_max": max(r["proposal_gap_over_ui"] for r in records),
                      "cone_rows_min": min(r["cone_rows"] for r in records),
                      "cone_rows_max": max(r["cone_rows"] for r in records),
                      "completion_marker_present": False,
                      "records_fully_consumed": records},
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise FileExistsError(args.out)
    for source in json.loads((HERE / "source-manifest.json").read_text()):
        p = HERE / source["preserved_path"]
        assert p.stat().st_size == source["size"] and digest(p) == source["sha256"]
    cases = [audit_case(4, 6), audit_case(5, 7), audit_case(6, 7)]
    report = {"scope": "fixed supplied policies and saved records; no discovery replay or universal gap upper bound",
              "original_main_executions": 0, "engine_calls": 0, "solver_calls": 0,
              "canonical_verifier_calls": 0, "new_definition_audit_executions": 1,
              "total_histories": sum(c["checked_histories"] for c in cases),
              "total_proper_deviations": sum(c["checked_proper_deviations"] for c in cases),
              "total_saved_records": sum(c["saved_run"]["records"] for c in cases), "cases": cases}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "cases"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
