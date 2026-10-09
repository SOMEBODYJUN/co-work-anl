"""Definition-level audit of a failed local coverage-opportunity SPE bridge.

This script expands every integer multiplicity into distinct unit customers and
checks every ordered decision history without importing the canonical model,
SPE solver, or certificate verifier. It proves the supplied finite certificate,
not a universal welfare bound. Default execution prints a report; --output may
freeze a new report and refuses to overwrite existing evidence.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "examples/customer_attraction/coverage_opportunity_failure.json"
CERTIFICATE = ROOT / "evidence/certificates/customer_attraction/coverage_opportunity_failure.json"


def audit():
    obj = json.loads(INPUT.read_text())
    cert = json.loads(CERTIFICATE.read_text())
    labels = obj["topics"]
    topic_count, players = len(labels), obj["players"]
    customers = []
    for row in obj["customers"]:
        assert isinstance(row["multiplicity"], int) and row["multiplicity"] > 0
        customers.extend([frozenset(row["topics"])] * row["multiplicity"])
    actions = {tuple(row["history"]): row["action"] for row in cert["actions"]}
    assert len(actions) == len(cert["actions"])
    required = {h for d in range(players) for h in product(range(topic_count), repeat=d)}
    assert set(actions) == required
    assert all(a in range(topic_count) for a in actions.values())

    def terminal(prefix):
        history = tuple(prefix)
        while len(history) < players:
            history += (actions[history],)
        return history

    def utilities(history):
        assert len(history) == players
        out = [Fraction(0)] * players
        for likes in customers:
            attracted = [i for i, a in enumerate(history) if a in likes]
            if attracted:
                for i in attracted:
                    out[i] += Fraction(1, len(attracted))
        return tuple(out)

    def covered(history):
        return {x for x, likes in enumerate(customers) if any(a in likes for a in history)}

    checked_comparisons = 0
    for history, action in actions.items():
        actual = utilities(terminal(history))[len(history)]
        assert terminal(history)[len(history)] == action
        for alternative in range(topic_count):
            deviation = utilities(terminal(history + (alternative,)))[len(history)]
            assert actual >= deviation, (history, action, alternative, actual, deviation)
            checked_comparisons += 1

    actual_path = terminal(())
    actual_counts = tuple(actual_path.count(a) for a in range(topic_count))
    assert actual_counts == tuple(cert["terminal_counts"])
    actual_u = utilities(actual_path)
    actual_w = len(covered(actual_path))
    assert sum(actual_u) == actual_w

    def F(prefix, remaining):
        C = covered(prefix)
        return max(len(C | covered(support))
                   for size in range(min(remaining, topic_count) + 1)
                   for support in combinations(range(topic_count), size))

    opportunities = []
    for i, action in enumerate(actual_path):
        prefix = actual_path[:i]
        before = F(prefix, players - i)
        after = F(prefix + (action,), players - i - 1)
        opportunities.append({"history": [labels[a] for a in prefix],
                              "action": labels[action], "F_before": before,
                              "F_after": after, "delta": before - after,
                              "current_utility": str(actual_u[i]),
                              "local_bridge_holds": before - after <= actual_u[i]})
    optimum = F((), players)
    assert actual_path == (0, 0, 1)
    assert actual_u == (Fraction(5, 2), Fraction(5, 2), Fraction(3))
    assert (actual_w, optimum) == (8, 11)
    assert opportunities[1]["delta"] == 3 > actual_u[1]
    assert sum(row["delta"] for row in opportunities) == optimum - actual_w

    second_table = []
    root_table = []
    third_best = []
    for a in range(topic_count):
        values = [utilities(terminal((a, b)))[1] for b in range(topic_count)]
        second_table.append({"first": labels[a], "second_payoffs": [str(v) for v in values],
                             "chosen_second": labels[actions[(a,)]]})
        root_table.append({"first": labels[a],
                           "first_utility": str(utilities(terminal((a,)))[0])})
        for b in range(topic_count):
            values = [utilities((a, b, c))[2] for c in range(topic_count)]
            third_best.append({"history": [labels[a], labels[b]],
                               "payoffs": [str(v) for v in values],
                               "chosen": labels[actions[(a, b)]]})
    return {"claim": "CA-COVERAGE-OPPORTUNITY-NO",
            "scope": "one complete ordered-history pure SPE; action-specific local bridge is false",
            "universal_half_coverage_proved": False,
            "half_coverage_refuted": False,
            "unit_customers": len(customers), "decision_nodes": len(actions),
            "checked_comparisons_including_chosen_actions": checked_comparisons,
            "actual_path": [labels[a] for a in actual_path],
            "utilities": [str(v) for v in actual_u], "welfare": actual_w,
            "optimum": optimum, "opportunities": opportunities,
            "second_node_payoffs": second_table, "root_payoffs": root_table,
            "third_node_payoffs": third_best,
            "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
            "input_sha256": sha256(INPUT.read_bytes()).hexdigest(),
            "certificate_sha256": sha256(CERTIFICATE.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = audit()
    if args.output:
        if args.output.exists():
            raise FileExistsError("refusing to overwrite a frozen audit")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
