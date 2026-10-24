"""Exact definition-level audit of a specified abstract-menu bridge.

No SPE claim, no oracle or LP dependency, and no finite-test proof of a universal game statement.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from pathlib import Path
import json


def audit(k):
    topics = tuple(frozenset(((i - 1) % k, i, (i + 1) % k)) for i in range(k))

    def payoff(action, profile):
        return sum((F(1, sum(customer in topics[v] for v in profile))
                    for customer in topics[action]), F(0))

    optimum = max(len(set().union(*(topics[a] for a in profile)))
                  for profile in combinations_with_replacement(range(k), 3))
    assert optimum == 9
    threshold = F(optimum, 6)
    menus = []
    for root in range(k):
        profile = (root, (root - 1) % k, (root + 1) % k)
        values = tuple(payoff(a, profile) for a in profile)
        assert values == (F(4, 3), F(11, 6), F(11, 6))
        assert values[0] < threshold < min(values[1:])
        final_values = tuple(payoff(a, profile[:2] + (a,)) for a in range(k))
        far = (root + 3) % k
        assert topics[far].isdisjoint(topics[profile[0]] | topics[profile[1]])
        assert final_values[far] == max(final_values) == 3 > values[-1]
        menus.append({"root": root, "profile": profile,
                      "utilities": [str(v) for v in values],
                      "profitable_last_action": far,
                      "profitable_last_utility": str(final_values[far]),
                      "all_last_actions_checked": k})
    return {"k": k, "players": 3, "optimum": optimum,
            "threshold": str(threshold), "menus": menus}


if __name__ == "__main__":
    result = {"claim": "abstract root-tail threshold bridge fails; not an SPE counterexample",
              "method": "Fraction and direct set unions; no SPE oracle",
              "cases": [audit(k) for k in (9, 10, 11, 12)]}
    target = Path(__file__).with_name("opt_threshold_cycle_audit.json")
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"cases": len(result["cases"]),
                      "menus": sum(len(c["menus"]) for c in result["cases"]),
                      "all_checks": True}))
