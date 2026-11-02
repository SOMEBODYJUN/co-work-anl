from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

CLIENTS = [{1} for _ in range(4)] + [{2}, {3}, {0, 2, 3}, {0, 2, 3}]


def utility(s, player):
    return sum((F(1, sum(a in c for a in s)) for c in CLIENTS if s[player] in c), F(0))


def potential(s):
    return sum((sum((F(1, j) for j in range(1, sum(a in c for a in s) + 1)), F(0))
                for c in CLIENTS), F(0))


pne = []
for s in product(range(4), repeat=3):
    for i in range(3):
        assert utility(s, i) == potential(s) - potential(s[:i] + s[i+1:])
    if all(utility(s, i) >= utility(s[:i] + (a,) + s[i+1:], i)
           for i in range(3) for a in range(4)):
        pne.append({"profile": s, "welfare": str(sum(utility(s, i) for i in range(3))),
                    "potential": str(potential(s))})
assert sorted(set(tuple(sorted(r["profile"])) for r in pne)) == [(1, 1, 2), (1, 1, 3), (1, 2, 3)]
assert all(F(r["potential"]) == 9 for r in pne)
assert potential((0, 1, 1)) == 8
report = {"static_ordered_profiles": 64, "static_comparisons": 64 * 12,
          "spe_profile": (0, 1, 1), "spe_potential": "8", "minimum_pne_potential": "9", "all_pne": pne}
Path(__file__).with_suffix(".json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
