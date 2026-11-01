"""Enumerate all complete two-active-player strategies from the saved input.

No canonical model, utility function, outcome solver, or verifier is imported.
Customer multiplicities are expanded into distinct unit customers.  Every
four-topic policy has one root action and four last-player replies: 4^5=1024.
"""
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def audit(data, base):
    labels = data["instance"]["topics"]
    k = len(labels)
    customers = [frozenset(t["topics"]) for t in data["instance"]["customers"]
                 for _ in range(t["multiplicity"])]
    old_load = [sum(base[a] for a in interests) for interests in customers]

    def payoff(first, last, player):
        chosen = (first, last)[player]
        return sum((Fraction(1, old_load[x] + int(first in interests) + int(last in interests))
                    for x, interests in enumerate(customers) if chosen in interests), Fraction(0))

    last_values = [[payoff(a, b, 1) for b in range(k)] for a in range(k)]
    last_brs = [tuple(b for b in range(k) if last_values[a][b] == max(last_values[a]))
                for a in range(k)]
    outcomes = set()
    policies = []
    checked_policies = 0
    for first in range(k):
        for replies in product(range(k), repeat=k):
            checked_policies += 1
            if any(replies[a] not in last_brs[a] for a in range(k)):
                continue
            first_values = [payoff(a, replies[a], 0) for a in range(k)]
            if first_values[first] != max(first_values):
                continue
            last = replies[first]
            counts = tuple(base[a] + int(a == first) + int(a == last) for a in range(k))
            profit = payoff(first, last, 0) + payoff(first, last, 1)
            outcomes.add(counts)
            policies.append((profit, counts, first, replies))
    policies.sort()
    minimum, target, first, replies = policies[0]
    candidates = [p for p in policies if p[0] == minimum and p[1] == target]
    _, _, first, replies = candidates[0]
    comparisons = []
    for a in range(k):
        for b in range(k):
            comparisons.append({"history": [a], "action": b,
                                "gap": last_values[a][replies[a]] - last_values[a][b]})
    values = [payoff(a, replies[a], 0) for a in range(k)]
    for a in range(k):
        comparisons.append({"history": [], "action": a, "gap": values[first] - values[a]})
    if any(row["gap"] < 0 for row in comparisons):
        raise AssertionError("Constructed complete policy violates an SPE comparison")
    return {"base": base, "unit_customers": len(customers), "remaining_players": 2,
            "all_complete_policies_tested": checked_policies, "valid_policies": len(policies),
            "outcomes": sorted(outcomes), "minimum_remaining_profit": minimum,
            "lexicographic_minimum_target": target,
            "last_payoff_table": last_values, "last_best_replies": last_brs,
            "minimum_witness": {"first_action": first, "last_replies": replies,
                                "actual_active_path": [first, replies[first]],
                                "active_payoffs": [payoff(first, replies[first], 0), payoff(first, replies[first], 1)],
                                "first_action_payoffs_under_these_replies": values,
                                "complete_policy_comparisons_including_self": comparisons}}


def main():
    data = json.loads((HERE / "original/background_nonmonotone.json").read_text())
    if data["r"] != 2:
        raise ValueError("Independent full-policy enumeration is specifically for this r=2 saved witness")
    base = tuple(data["base"])
    added = tuple(base[a] + int(a == data["add"]) for a in range(len(base)))
    original, modified = audit(data, base), audit(data, added)
    for result, key in ((original, "original"), (modified, "added")):
        assert str(result["minimum_remaining_profit"]) == data[key][0]
        assert list(result["lexicographic_minimum_target"]) == data[key][1]
    report = {"status": "PASS", "scope": "all 1024 complete two-player strategies at each of two legal backgrounds",
              "original": original, "added": modified,
              "strict_increase": modified["minimum_remaining_profit"] > original["minimum_remaining_profit"]}
    output = HERE / "replay/independent-full-policy-check.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2,
                                default=lambda x: str(x) if isinstance(x, Fraction) else x) + "\n")
    print(json.dumps({"status": report["status"], "minimum_original": str(original["minimum_remaining_profit"]),
                      "minimum_added": str(modified["minimum_remaining_profit"]),
                      "valid_policies": [original["valid_policies"], modified["valid_policies"]]}))


if __name__ == "__main__":
    main()
