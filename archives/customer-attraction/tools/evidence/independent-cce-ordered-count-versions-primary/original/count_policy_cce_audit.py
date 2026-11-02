"""Literal-client independent check of the simpler count-dependent SPE witness."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

CLIENTS = [{1} for _ in range(4)] + [{2}, {3}, {0, 2, 3}, {0, 2, 3}]
LAST = {(0, 0): 1, (0, 1): 1, (0, 2): 1, (0, 3): 1,
        (1, 1): 2, (1, 2): 3, (1, 3): 2, (2, 2): 1,
        (2, 3): 1, (3, 3): 1}


def action(h):
    return 0 if not h else (1 if len(h) == 1 else LAST[tuple(sorted(h))])


def outcome(h):
    while len(h) < 3:
        h = h + (action(h),)
    return h


def u(s, i):
    return sum((F(1, sum(a in c for a in s)) for c in CLIENTS if s[i] in c), F(0))


rows = []
for t in range(3):
    for h in product(range(4), repeat=t):
        selected = u(outcome(h), t)
        alternatives = [u(outcome(h + (a,)), t) for a in range(4)]
        assert selected >= max(alternatives), (h, selected, alternatives)
        rows.append({"history": h, "action": action(h), "outcome": outcome(h),
                     "payoff": str(selected), "alternative_payoffs": list(map(str, alternatives))})
report = {"clients": [sorted(c) for c in CLIENTS], "strategy_type": "count-dependent",
          "actual_outcome": outcome(()), "actual_payoffs": [str(u(outcome(()), i)) for i in range(3)],
          "comparisons": 4 * len(rows), "all_spe_rows": rows}
target = Path(__file__).with_suffix(".json")
target.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({k: v for k, v in report.items() if k != "all_spe_rows"}, indent=2))
