"""Definition-level Fraction audit. No canonical model, BI, LP, or SPE solver."""

from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


def decomposition(customers, background, root, tail):
    r = len(tail) + 1
    g = lambda topic: sum((F(1, background[i] + r - 1)
                           for i, customer in enumerate(customers)
                           if topic in customer), F())
    root_u = F()
    tail_u = [F() for _ in tail]
    credit = debt = F()
    debt_alt = F()
    for i, customer in enumerate(customers):
        a = root in customer
        n = sum(topic in customer for topic in tail)
        b = background[i]
        if a:
            root_u += F(1, b + 1 + n)
        if n:
            for j, topic in enumerate(tail):
                if topic in customer:
                    tail_u[j] += F(1, b + a + n)
        p = F(n, r - 1)
        if a and n < r - 1:
            credit += (1 - p) * (F(1, b + n + 1) - F(1, b + r - 1))
        elif not a and n:
            debt += p * (F(1, b + n) - F(1, b + r - 1))
            debt_alt += F(n * (r - 1 - n),
                          (r - 1) * (b + n) * (b + r - 1))
    mean = sum(tail_u, F()) / (r - 1)
    drift = g(root) - sum((g(topic) for topic in tail), F()) / (r - 1)
    assert credit >= 0 and debt >= 0
    assert debt == debt_alt
    assert root_u - mean == drift + credit - debt
    return {"root": str(root_u), "tail_mean": str(mean),
            "g_drift": str(drift), "C": str(credit), "D": str(debt)}


def full_policy_audit(customers, topic_count, players, policy):
    def completion(history):
        while len(history) < players:
            history += (policy(history),)
        return history

    def utility(terminal, position):
        return sum((F(1, sum(topic in c for topic in terminal))
                    for c in customers if terminal[position] in c), F())

    nodes = comparisons = 0
    for depth in range(players):
        for history in product(range(topic_count), repeat=depth):
            nodes += 1
            actual = completion(history)
            actual_u = utility(actual, depth)
            for action in range(topic_count):
                comparisons += 1
                alternate = completion(history + (action,))
                assert actual_u >= utility(alternate, depth), (history, action)
    actual = completion(())
    return {"nodes": nodes, "comparisons": comparisons,
            "actual": actual,
            "payoffs": [str(utility(actual, i)) for i in range(players)]}


def main():
    scalar_checks = 0
    for r in range(2, 11):
        for b in range(9):
            for a in (0, 1):
                for n in range(r):
                    customer = set(range(1, n + 1))
                    if a:
                        customer.add(0)
                    decomposition([customer], [b], 0, list(range(1, r)))
                    scalar_checks += 1

    triangle = [{0, 1}, {0, 2}, {1, 2}]

    def triangle_policy(history):
        if not history:
            return 0
        if len(history) == 1:
            return min(set(range(3)) - set(history))
        return min(set(range(3)) - set(history))

    triangle_report = full_policy_audit(triangle, 3, 3, triangle_policy)
    triangle_report["decomposition"] = decomposition(triangle, [0] * 3, 0, [1, 2])
    assert triangle_report["decomposition"] == {
        "root": "1", "tail_mean": "1", "g_drift": "0", "C": "0", "D": "0"}

    repo = Path(__file__).resolve().parents[5]
    data = json.loads((repo / "examples/customer_attraction/aggregate_theta_failure.json").read_text())
    aggregate = [set(customer["topics"])
                 for customer in data["customers"]
                 for _ in range(customer.get("multiplicity", 1))]

    def aggregate_policy(history):
        if not history:
            return 0
        if len(history) == 1:
            return 3 if history[0] < 3 else 0
        group = range(3) if history[1] < 3 else range(3, 6)
        return min(set(group) - set(history))

    aggregate_report = full_policy_audit(aggregate, 6, 3, aggregate_policy)
    aggregate_report["source"] = "examples/customer_attraction/aggregate_theta_failure.json"
    aggregate_report["decomposition"] = decomposition(aggregate, [0] * 36, 0, [3, 4])
    assert aggregate_report["decomposition"] == {
        "root": "10", "tail_mean": "12", "g_drift": "0", "C": "1/2", "D": "5/2"}
    report = {"claim_status": "exact identity and conditional no-go; no half counterexample",
              "scalar_checks": scalar_checks,
              "triangle_full_spe": triangle_report,
              "existing_aggregate_theta_full_spe": aggregate_report}
    target = Path(__file__).with_name("tail_disagreement_audit.json")
    target.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
