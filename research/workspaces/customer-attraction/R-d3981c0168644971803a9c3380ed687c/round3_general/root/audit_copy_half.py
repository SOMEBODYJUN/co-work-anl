"""Root's independent unit-customer replay of the copy-half counterexample.

Input is only the six disjoint blocks, five coverage sets and specified A-child.
No author implementation, game package or equilibrium solver is imported.
All other children are explicitly completed by finite backward induction here.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json

blocks = {}
cursor = 0
for name, count in (("core", 6), ("private_A", 12), ("X", 8),
                    ("Y1", 2), ("Y2", 2), ("Z", 5)):
    blocks[name] = frozenset(range(cursor, cursor + count))
    cursor += count
topics = (blocks["core"] | blocks["private_A"], blocks["X"],
          blocks["Y1"] | blocks["Y2"] | blocks["Z"],
          blocks["core"] | blocks["X"] | blocks["Y1"],
          blocks["core"] | blocks["X"] | blocks["Y2"])
names = ("A", "E", "D", "F1", "F2")
assert cursor == 35 and len(set(topics)) == 5
policy = {}


def pay(z, role):
    return sum((F(1, sum(x in topics[a] for a in z))
                for x in topics[z[role]]), F())


def welfare(z):
    return len(frozenset().union(*(topics[a] for a in z)))


@lru_cache(None)
def complete(h):
    if len(h) == 3:
        return h
    children = [complete(h + (a,)) for a in range(5)]
    if not h:
        action = 0
    elif h == (0,):
        action = 1
    elif len(h) == 2 and h[0] == 0:
        action = (3, 2, 3, 4, 3)[h[1]]
    else:
        action = max(range(5), key=lambda a: (pay(children[a], len(h)), -a))
    policy[h] = action
    return children[action]


z = complete(())
checks = 0
minimum = None
for h, action in policy.items():
    eq = pay(complete(h), len(h))
    for a in range(5):
        slack = eq - pay(complete(h + (a,)), len(h))
        assert slack >= 0, (h, action, a, slack)
        minimum = slack if minimum is None else min(minimum, slack)
        checks += 1
assert z == (0, 1, 2)
profits = tuple(pay(z, i) for i in range(3))
assert profits == (F(18), F(8), F(9))
optimum = max(welfare(zz) for zz in product(range(5), repeat=3))
copy_z = complete((0, 0))
copy_profit = pay(copy_z, 1)
assert copy_z == (0, 0, 3) and copy_profit == 8 < profits[0] / 2
assert profits[0] > 2 * profits[1]
assert welfare(z) == optimum == 35
summary = {
    "status": "passed_root_independent_definition_level_replay",
    "unit_customers": cursor, "topics": list(names),
    "topic_sizes": list(map(len, topics)), "players": 3,
    "decision_histories": len(policy), "IC_checks_including_self": checks,
    "minimum_IC_slack": str(minimum), "actual": list(z),
    "payoffs": list(map(str, profits)), "welfare": welfare(z),
    "OPT": optimum, "copy_leaf": list(copy_z),
    "copy_profit": str(copy_profit), "half_earlier_profit": str(profits[0] / 2),
    "scope": "Refutes copy-half protection and earlier<=2*later; not HALF, STATIC-2 or prefix coupon cap2.",
    "complete_policy": [{"history": list(h), "action": a}
                        for h, a in sorted(policy.items(), key=lambda item: (len(item[0]), item[0]))],
}
output = Path(__file__).with_name("copy_half_independent_audit.json")
output.write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps({k: v for k, v in summary.items() if k != "complete_policy"}, indent=2))
