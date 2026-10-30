"""Independent replay of a four-player full-SPE prefix-balance counterexample.

Every multiplicity is expanded into distinct unit customers. All ordered
histories and all six choices are replayed directly with Fraction. This script
imports no canonical model, SPE solver, cone code, or certificate verifier.
Default execution only prints; --output freezes a new report without overwriting.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "examples/customer_attraction/prefix_balance_failure.json"
CERT = ROOT / "evidence/certificates/customer_attraction/prefix_balance_failure.json"


def audit():
    obj = json.loads(INPUT.read_text()); cert = json.loads(CERT.read_text())
    labels = obj["topics"]; p = len(labels); n = obj["players"]
    customers = []
    for row in obj["customers"]:
        assert type(row["multiplicity"]) is int and row["multiplicity"] > 0
        likes = frozenset(row["topics"])
        assert all(type(a) is int and a in range(p) for a in likes)
        customers.extend([likes] * row["multiplicity"])
    actions = {tuple(row["history"]): row["action"] for row in cert["actions"]}
    required = {h for t in range(n) for h in product(range(p), repeat=t)}
    assert len(actions) == len(cert["actions"]) and set(actions) == required
    assert all(type(a) is int and a in range(p) for a in actions.values())

    def terminal(history):
        h = tuple(history)
        while len(h) < n:
            h += (actions[h],)
        return h

    def utility(history, position):
        assert len(history) == n
        own = history[position]
        return sum((F(1, sum(a in likes for a in history))
                    for likes in customers if own in likes), F(0))

    def coverage(history):
        return frozenset(x for x, likes in enumerate(customers)
                         if any(a in likes for a in history))

    comparisons = ties = 0; minimum_positive_slack = None
    for h, a in actions.items():
        actual = utility(terminal(h), len(h))
        assert terminal(h)[len(h)] == a
        for alternative in range(p):
            deviated = utility(terminal(h + (alternative,)), len(h))
            assert actual >= deviated, (h, a, alternative, actual, deviated)
            comparisons += 1
            ties += actual == deviated
            if actual > deviated:
                slack = actual - deviated
                minimum_positive_slack = (slack if minimum_positive_slack is None
                                          else min(slack, minimum_positive_slack))

    # Independently check that the JSON expands the compact strategy in the text.
    assert (labels, n) == (["L0", "A", "B", "L1", "L2", "L3"], 4)
    assert actions[()] == 1
    for h in product(range(p), repeat=1):
        assert actions[h] == (1 if h == (2,) else 2)
    for h in product(range(p), repeat=2):
        assert actions[h] == (1 if h == (2, 2) else 2)
    priority = (2, 1, 0, 3, 4, 5)
    for h in product(range(p), repeat=3):
        assert actions[h] == max(priority, key=lambda a: utility(h + (a,), 3))

    path = terminal(())
    actual_u = tuple(utility(path, i) for i in range(n))
    W = len(coverage(path)); assert sum(actual_u) == W
    assert tuple(path.count(a) for a in range(p)) == tuple(cert["terminal_counts"])

    def completions(prefix, remaining):
        candidates = [(len(coverage(tuple(prefix) + support)), support)
                      for size in range(min(remaining, p) + 1)
                      for support in combinations(range(p), size)]
        maximum = max(v for v, _ in candidates)
        return maximum, [s for v, s in candidates if v == maximum]

    optimum, optimal_supports = completions((), n)
    Fs, Bs, witnesses = [], [], []
    for t in range(n + 1):
        f, supports = completions(path[:t], n - t)
        Fs.append(f); Bs.append(sum(actual_u[:t], F(0)) + f - optimum)
        witnesses.append([labels[a] for a in supports[0]])
    deltas = [Fs[t - 1] - Fs[t] for t in range(1, n + 1)]
    assert sum(deltas) == optimum - W
    assert Bs[-1] == 2 * W - optimum

    before_last = path[:-1]
    background = [sum(a in likes for a in before_last) for likes in customers]
    tax = sum((F(b, b + 1) for b in background), F(0))
    tax_margin = W + tax - optimum
    assert path == (1, 2, 2, 2)
    assert actual_u == (F(15, 4), F(41, 12), F(41, 12), F(41, 12))
    assert (len(customers), W, optimum) == (22, 14, 22)
    assert optimal_supports == [(0, 3, 4, 5)]
    assert Fs == [22, 18, 18, 16, 14]
    assert Bs == [F(0), F(-1, 4), F(19, 6), F(55, 12), F(6)]
    assert (tax, tax_margin) == (F(109, 12), F(13, 12))
    assert F(W, optimum) == F(7, 11) > F(1, 2)

    third_table, second_table, root_table = [], [], []
    for a in range(p):
        third_row = []
        second_row = []
        for b in range(p):
            h = (a, b)
            options = [utility(terminal(h + (c,)), 2) for c in range(p)]
            chosen = utility(terminal(h), 2)
            assert chosen == max(options)
            third_row.append(str(chosen))
            second_row.append(str(utility(terminal(h), 1)))
        third_table.append(third_row); second_table.append(second_row)
        root_table.append(str(utility(terminal((a,)), 0)))

    return {"claim": "CA-PREFIX-BALANCE-NO",
            "scope": "one complete ordered-history pure SPE; every-prefix balance is false",
            "half_coverage_refuted": False, "root_total_tax_refuted": False,
            "unit_customers": len(customers), "decision_nodes": len(actions),
            "checked_comparisons_including_chosen_actions": comparisons,
            "ties_including_chosen_actions": ties,
            "minimum_positive_slack": str(minimum_positive_slack),
            "actual_path": [labels[a] for a in path],
            "utilities": [str(v) for v in actual_u], "welfare": W, "optimum": optimum,
            "optimal_supports": [[labels[a] for a in s] for s in optimal_supports],
            "F_by_prefix": Fs, "B_by_prefix": [str(v) for v in Bs],
            "completion_witness_by_prefix": witnesses, "opportunity_losses": deltas,
            "root_prefix_tax": str(tax), "root_tax_margin": str(tax_margin),
            "half_coverage_margin": 2 * W - optimum,
            "welfare_over_optimum": str(F(W, optimum)),
            "third_selected_equals_maximum_payoff_table": third_table,
            "second_action_payoff_table": second_table, "root_action_payoffs": root_table,
            "input_sha256": sha256(INPUT.read_bytes()).hexdigest(),
            "certificate_sha256": sha256(CERT.read_bytes()).hexdigest(),
            "audit_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
            "all_checks_passed": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(); report = audit()
    encoded = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(encoded)
    print(encoded, end="")

if __name__ == "__main__":
    main()
