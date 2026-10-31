"""Exact unit-customer check of the supplied complete five-player policy.

This is a definition-level supplementary audit, not a SPE solver or blind review.
It preserves every node/action inequality and every background comparison count.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parent.parent
INSTANCE = BASE / "comparison/background_step_instance.json"
CERTIFICATE = BASE / "comparison/background_step_certificate.json"
instance = json.loads(INSTANCE.read_text())
certificate = json.loads(CERTIFICATE.read_text())
n = instance["players"]
k = len(instance["topics"])
assert n == 5 and instance["topics"] == ["A", "B", "C"]
customers = [frozenset(row["topics"]) for row in instance["customers"]
             for _ in range(row["multiplicity"])]
assert len(customers) == 12
histories = [h for depth in range(n) for h in product(range(k), repeat=depth)]
rows = certificate["actions"]
assert len(rows) == len(histories) == 121
policy = {tuple(row["history"]): row["action"] for row in rows}
assert len(policy) == len(rows) and set(policy) == set(histories)
assert all(type(a) is int and 0 <= a < k for a in policy.values())


def terminal(history):
    while len(history) < n:
        history = history + (policy[history],)
    return history


def payoff(terminal_path, player):
    action = terminal_path[player]
    return sum((Fraction(1, sum(a in accepts for a in terminal_path))
                for accepts in customers if action in accepts), Fraction(0))


comparisons = []
for h in histories:
    prescribed_terminal = terminal(h)
    actual = payoff(prescribed_terminal, len(h))
    for action in range(k):
        alternative_terminal = terminal(h + (action,))
        alternative = payoff(alternative_terminal, len(h))
        assert actual >= alternative, (h, action, actual, alternative)
        comparisons.append({"history": list(h), "prescribed_action": policy[h],
                            "tested_action": action,
                            "prescribed_terminal": list(prescribed_terminal),
                            "alternative_terminal": list(alternative_terminal),
                            "prescribed_payoff": str(actual),
                            "alternative_payoff": str(alternative),
                            "margin": str(actual - alternative)})


def comparison_table(background):
    remaining = n - sum(background)
    values = []
    for a in range(remaining + 1):
        for b in range(remaining - a + 1):
            counts = (a, b, remaining - a - b)
            val = Fraction(0)
            for accepts in customers:
                prior = sum(background[j] for j in accepts)
                future = sum(counts[j] for j in accepts)
                if future:
                    val += Fraction(future, prior + future)
            values.append({"counts": counts, "remaining_profit": str(val)})
    maximum = max(Fraction(row["remaining_profit"]) for row in values)
    return {"background": list(background), "remaining_players": remaining,
            "maximum": str(maximum),
            "maximizers": [row["counts"] for row in values
                           if Fraction(row["remaining_profit"]) == maximum],
            "all_count_values": values}


f4 = comparison_table((0, 0, 1))
f3 = comparison_table((1, 0, 1))
assert f4["maximum"] == "11" and f3["maximum"] == "41/6"
path = terminal(())
assert path == (2, 0, 0, 0, 0)
profits = [str(payoff(path, i)) for i in range(n)]
assert profits == ["3", "2", "2", "2", "2"]
assert [path.count(i) for i in range(k)] == certificate["terminal_counts"]
margins = [Fraction(row["margin"]) for row in comparisons]
out = {"status": "PASS", "audit": "unit expansion of complete supplied policy",
       "not_a_solver_or_blind_review": True,
       "inputs": [{"path": str(p.relative_to(BASE)),
                   "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                  for p in [INSTANCE, CERTIFICATE]],
       "unit_customers": len(customers), "players": n, "topics": k,
       "ordered_histories": len(histories),
       "action_comparisons_including_chosen": len(comparisons),
       "nonchosen_action_comparisons": len(histories) * (k - 1),
       "zero_margins_including_chosen": sum(x == 0 for x in margins),
       "positive_margins": sum(x > 0 for x in margins),
       "minimum_positive_margin": str(min(x for x in margins if x > 0)),
       "policy_digits_breadth_then_lexicographic": "".join(str(policy[h]) for h in histories),
       "actual_path": list(path), "actual_profits": profits,
       "F4_C": f4, "F3_CA": f3, "all_node_action_inequalities": comparisons,
       "scope": "A complete finite proof certificate for this five-player policy; no arbitrary-instance or arbitrary-m extrapolation."}
output = Path(__file__).with_name("background-unit-check.json")
output.write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps({key: out[key] for key in ["status", "unit_customers", "ordered_histories",
      "action_comparisons_including_chosen", "nonchosen_action_comparisons",
      "zero_margins_including_chosen", "positive_margins", "minimum_positive_margin",
      "policy_digits_breadth_then_lexicographic", "actual_path", "actual_profits"]}))
