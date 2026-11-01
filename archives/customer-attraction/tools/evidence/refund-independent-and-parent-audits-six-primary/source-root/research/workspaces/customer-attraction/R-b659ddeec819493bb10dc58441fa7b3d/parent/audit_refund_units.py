"""Root audit from raw policy; no game solver or author audit imports."""
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parents[1]
source = root / "refund/prefixed_refund_counterexample.json"
raw = source.read_bytes()
data = json.loads(raw)
customers = [mask for mask, count in data["rows"] for _ in range(count)]
topics = [{x for x, mask in enumerate(customers) if mask & (1 << a)}
          for a in range(7)]
policy = {tuple(row["history"]): row["action"] for row in data["actions"]}
histories = [h for depth in range(3) for h in product(range(7), repeat=depth)]
assert set(policy) == set(histories)
assert len({frozenset(t) for t in topics}) == 7

def terminal(history):
    while len(history) < 3:
        history += (policy[history],)
    return history

def coverage(profile):
    return set().union(*(topics[a] for a in profile)) if profile else set()

def utility(profile, role, domain=None):
    selected = topics[profile[role]]
    if domain is not None:
        selected = selected & domain
    return sum((Fraction(1, sum(x in topics[a] for a in profile))
                for x in selected), Fraction())

slacks = []
root_values = []
for history in histories:
    i = len(history)
    chosen = utility(terminal(history), i)
    for action in range(7):
        deviation = utility(terminal(history + (action,)), i)
        assert chosen >= deviation, (history, action, chosen, deviation)
        slacks.append(chosen - deviation)
        if not history:
            root_values.append(str(deviation))

actual = terminal(())
C = coverage(actual)
profits = [utility(actual, i) for i in range(3)]
assert sum(profits) == len(C)
all_profiles = list(product(range(7), repeat=3))
opt = max(len(coverage(p)) for p in all_profiles)
optimal_profiles = [p for p in all_profiles if len(coverage(p)) == opt]
optimal_sets = {frozenset(coverage(p)) for p in optimal_profiles}
assert len(optimal_sets) == 1
O = set(next(iter(optimal_sets)))
D = O - C
f = [max(len(coverage(p) & D) for p in product(range(7), repeat=r))
     for r in range(4)]
outside = [utility(actual, i, C - O) for i in range(3)]
reserve_slacks = [profits[i] + outside[i] - (f[3-i] - f[2-i])
                  for i in range(3)]
assert len(customers) == 179
assert actual == (6, 0, 1)
assert profits == [34, 35, 38]
assert len(C) == 107 and opt == 111
assert f == [0, 36, 72, 72]
assert outside == [34, 0, 34]
assert reserve_slacks == [68, -1, 36]
assert len(D) - len(C - O) == opt - len(C) == 4

result = {
    "claim": "per-position once-only outside-optimum refund reserve; universal and existential-optimum versions",
    "status": "refuted by complete root SPE; Q-CAG-HALF unaffected",
    "source_sha256": hashlib.sha256(raw).hexdigest(),
    "unit_customers": len(customers), "distinct_topics": len(topics),
    "ordered_histories": len(histories), "all_action_comparisons": len(slacks),
    "min_IC_slack": str(min(slacks)), "root_true_query_profits": root_values,
    "actual": actual, "profits": list(map(str, profits)), "W": len(C),
    "optimal_ordered_profiles": optimal_profiles,
    "optimal_union_count": len(optimal_sets), "OPT": opt,
    "missing": len(D), "outside_optimum": len(C - O),
    "f_D": f, "outside_role_profits": list(map(str, outside)),
    "per_role_reserve_slacks": list(map(str, reserve_slacks)),
    "half_slack": 2*len(C)-opt,
}
destination = root / "parent/refund_unit_audit.json"
destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(result, ensure_ascii=False, indent=2))
