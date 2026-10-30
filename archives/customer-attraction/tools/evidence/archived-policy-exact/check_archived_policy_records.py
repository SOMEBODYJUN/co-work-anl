#!/usr/bin/env python3
"""Independent exact count-state recurrence for archived-policy records.

This checker does not import the archived solver, cone code, or price code.
It reconstructs finite pure-SPE outcome sets from the customer definition
using exact Fraction arithmetic and directly checks the saved selected tree.
"""
from __future__ import annotations

import hashlib
import json
from functools import lru_cache
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
READ = ROOT / "cleanup/workspaces/Boss3/customer-structure/archived-policy-read"
REPORT = READ / "archived_tstar_attack.json"
FILES = {
    "coverage_opportunity_failure.json": READ / "comparisons/coverage_opportunity_failure.json",
    "worst_pne_welfare_failure.json": READ / "comparisons/worst_pne_welfare_failure.json",
    "worst_cce_welfare_failure.json": READ / "comparisons/worst_cce_welfare_failure.json",
    "portfolio_matching_failure.json": READ / "comparisons/portfolio_matching_failure.json",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def payoffs(counts, customers, p):
    out = [Fraction(0) for _ in range(p)]
    for topics, multiplicity in customers:
        attracted = sum(counts[t] for t in topics)
        if attracted:
            share = Fraction(multiplicity, attracted)
            for topic in topics:
                if counts[topic]:
                    out[topic] += share
    return tuple(out)


def solve_exact(instance):
    """Return all pure-SPE terminal count vectors by count-state induction."""
    p, m, customers = instance["p"], instance["m"], instance["customers"]
    payoff_cache = {}

    def utility(counts):
        if counts not in payoff_cache:
            payoff_cache[counts] = payoffs(counts, customers, p)
        return payoff_cache[counts]

    @lru_cache(None)
    def outcomes(counts):
        if sum(counts) == m:
            return frozenset((counts,))
        children = []
        for action in range(p):
            child = list(counts)
            child[action] += 1
            children.append(outcomes(tuple(child)))
        threshold = max(
            min(utility(terminal)[action] for terminal in child)
            for action, child in enumerate(children)
        )
        result = frozenset(
            terminal
            for action, child in enumerate(children)
            for terminal in child
            if utility(terminal)[action] >= threshold
        )
        assert result
        return result

    root = outcomes((0,) * p)
    seen = set()

    def visit(counts):
        if counts in seen:
            return
        seen.add(counts)
        if sum(counts) < m:
            for action in range(p):
                child = list(counts)
                child[action] += 1
                visit(tuple(child))

    visit((0,) * p)
    return root, outcomes.cache_info().currsize, sum(sum(c) == m for c in seen), utility


def terminal_for_policy(actions, p, m, history=()):
    history = tuple(history)
    if len(history) == m:
        return tuple(history.count(action) for action in range(p))
    return terminal_for_policy(actions, p, m, history + (actions[history],))


def verify_selected(selected):
    instance = selected["instance"]
    p, m = len(instance["topics"]), int(instance["players"])
    customers = [
        (tuple(c["topics"]), int(c["multiplicity"])) for c in instance["customers"]
    ]
    actions = {
        tuple(row["history"]): int(row["action"])
        for row in selected["certificate"]["actions"]
    }
    assert len(actions) == sum(p**depth for depth in range(m))
    cache = {}

    def utility(counts):
        if counts not in cache:
            cache[counts] = payoffs(counts, customers, p)
        return cache[counts]

    comparisons = 0
    for history in actions:
        if len(history) == m:
            continue
        action = actions[history]
        chosen = utility(terminal_for_policy(actions, p, m, history))[action]
        for alternative in range(p):
            deviated = terminal_for_policy(actions, p, m, history + (alternative,))
            assert chosen >= utility(deviated)[alternative], (history, action, alternative)
            comparisons += 1
    terminal = terminal_for_policy(actions, p, m)
    assert list(terminal) == selected["certificate"]["terminal_counts"]
    assert sum(utility(terminal)) == selected["W"]
    return {
        "histories": len(actions),
        "comparisons": comparisons,
        "terminal_counts": list(terminal),
        "welfare": str(sum(utility(terminal))),
        "physical_topics": len({tuple(c["topics"]) for c in instance["customers"]}),
    }


def main():
    report = json.loads(REPORT.read_text())
    expected = {
        "coverage_opportunity_failure.json": {"p": 5, "m": 3, "roots": 8, "rows": [77, 84, 88, 84, 88, 88, 80, 80]},
        "worst_pne_welfare_failure.json": {"p": 4, "m": 3, "roots": 2, "rows": [40, 39]},
        "worst_cce_welfare_failure.json": {"p": 5, "m": 3, "roots": 7, "rows": [76, 84, 81, 84, 84, 88, 84]},
        "portfolio_matching_failure.json": {"p": 5, "m": 2, "roots": 5, "rows": [24, 24, 24, 24, 24]},
    }
    games = {}
    for name, path in FILES.items():
        data = json.loads(path.read_text())
        customers = [(tuple(c["topics"]), int(c["multiplicity"])) for c in data["customers"]]
        instance = {"p": len(data["topics"]), "m": int(data["players"]), "customers": customers}
        root, states, terminal_states, _ = solve_exact(instance)
        records = [row for row in report["records"] if row["source"] == name]
        exp = expected[name]
        assert len(records) == exp["roots"]
        assert [row["rows"] for row in records] == exp["rows"]
        assert all(tuple(row["root"]) in root for row in records)
        games[name] = {
            "p": instance["p"],
            "m": instance["m"],
            "customers": sum(multiplicity for _, multiplicity in customers),
            "count_states": states,
            "terminal_count_states": terminal_states,
            "root_outcomes": len(root),
            "saved_records": len(records),
            "saved_rows": [row["rows"] for row in records],
            "saved_roots": [row["root"] for row in records],
            "input_sha256": sha(path),
        }
    result = {
        "status": "exact-finite-count-state-and-selected-certificate-verified",
        "report_sha256": sha(REPORT),
        "source_sha256": {name: sha(path) for name, path in FILES.items()},
        "games": games,
        "selected_certificate": verify_selected(report["selected"]),
        "saved_record_count": len(report["records"]),
        "saved_best_float": report["best_float"],
        "universal_result": report["universal_result"],
        "claims_not_made": [
            "No floating LP upper bound is certified.",
            "No exact proof is given for omitted duals or unsaved policies.",
            "Archived LP row counts remain metadata, not a general theorem.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
