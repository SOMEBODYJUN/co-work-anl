"""Independent unit-customer audit of one prescribed-kernel counterexample.

No game solver, StrategyCone, search routine, or shared payoff helper is used.
The fixed full strategy is checked at every ordered history by actually running
every deviating branch. Stationarity and its uniqueness are checked separately.
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
source_path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "weak_stationary_kernel_candidate.json"
source = json.loads(source_path.read_text())
instance = source["instance"]
p = len(instance["topics"])
m = instance["players"]
customers = tuple(frozenset(row["topics"])
                  for row in instance["customers"]
                  for _ in range(row["multiplicity"]))
actions = {tuple(row["history"]): row["action"] for row in source["actions"]}
histories = tuple(h for n in range(m) for h in product(range(p), repeat=n))
assert set(actions) == set(histories)
assert len(actions) == len(source["actions"])


def finish(prefix):
    history = tuple(prefix)
    while len(history) < m:
        history += (actions[history],)
    return history


def payoff(path, player):
    selected = path[player]
    return sum((F(1, sum(a in interested for a in path))
                for interested in customers if selected in interested), F(0))


def cover(path):
    return sum(any(a in interested for a in path) for interested in customers)


def static_query(background, selected):
    return sum((F(1, 1+sum(a in interested for a in background))
                for interested in customers if selected in interested), F(0))


def rank(matrix):
    rows = [list(map(F, row)) for row in matrix]
    rank_value = 0
    for col in range(len(rows[0])):
        pivot = next((j for j in range(rank_value, len(rows)) if rows[j][col]), None)
        if pivot is None:
            continue
        rows[rank_value], rows[pivot] = rows[pivot], rows[rank_value]
        pivot_value = rows[rank_value][col]
        rows[rank_value] = [v/pivot_value for v in rows[rank_value]]
        for j in range(rank_value+1, len(rows)):
            multiplier = rows[j][col]
            rows[j] = [v-multiplier*w for v, w in zip(rows[j], rows[rank_value])]
        rank_value += 1
    return rank_value


slacks = []
strict_nodes = 0
for h in histories:
    on_path = finish(h)
    actual = payoff(on_path, len(h))
    node_slacks = []
    for alternative in range(p):
        deviated = finish(h+(alternative,))
        slack = actual-payoff(deviated, len(h))
        assert slack >= 0, (h, alternative, on_path, deviated, slack)
        slacks.append(slack)
        if alternative != actions[h]:
            node_slacks.append(slack)
    strict_nodes += all(slack > 0 for slack in node_slacks)

path = finish(())
payoffs = tuple(payoff(path, i) for i in range(m))
welfare = cover(path)
assert sum(payoffs) == welfare
assert sorted(path) == [1, 2, 3, 4]
assert payoffs == (5, 5, 5, 5)
assert welfare == 20
optimum = max(cover(z) for z in product(range(p), repeat=m))
assert optimum == 23

tails = tuple(finish((a,))[1:] for a in range(p))
tail_counts = tuple(tuple(t.count(b) for b in range(p)) for t in tails)
assert tail_counts == tuple(map(tuple, source["root_followers"]))
kernel = tuple(tuple(F(c, m-1) for c in q) for q in tail_counts)
pi = tuple(map(F, source["stationary_distribution"]))
assert sum(pi) == 1 and all(v >= 0 for v in pi)
assert all(sum(pi[a]*kernel[a][b] for a in range(p)) == pi[b] for b in range(p))
stationarity_rank = rank([[kernel[a][b]-(a == b) for a in range(p)] for b in range(p)])
assert stationarity_rank == p-1
query_values = tuple(sum(pi[a]*static_query(tails[a], t) for a in range(p))
                     for t in range(p))
cap = max(query_values)
threshold = F(2*welfare, 2*m-1)
assert query_values == (F(25, 8), F(23, 4), F(39, 8), F(19, 4), F(43, 8))
assert cap == F(23, 4) and cap-threshold == F(1, 28)
assert F(2*m-1, 2)*cap/welfare == F(source["scaled_cap_to_welfare"]) == F(161, 160)
alternative_background = path[:-1]
alternative_values = tuple(static_query(alternative_background, t) for t in range(p))
assert max(alternative_values) == 5 < threshold


def serializable(obj):
    if isinstance(obj, F):
        return str(obj)
    if isinstance(obj, dict):
        return {k: serializable(v) for k, v in obj.items()}
    if isinstance(obj, (tuple, list)):
        return [serializable(v) for v in obj]
    return obj


report = {
    "identity": "verified failure only of root-stationary cap <= W/(m-1/2)",
    "main_half_coverage_claim": "OPEN; this instance satisfies 2W=40 >= OPT4=23",
    "method": "independent distinct unit customers; execute all ordered deviations; Fraction",
    "unit_customers": len(customers), "players": m, "topics": p,
    "checked_ordered_histories": len(histories),
    "checked_deviations_including_own_action": len(slacks),
    "nontrivial_deviations": len(histories)*(p-1),
    "strict_best_action_nodes": strict_nodes,
    "minimum_deviation_slack": min(slacks),
    "actual_ordered_path": path, "actual_payoffs": payoffs,
    "welfare": welfare, "optimum": optimum,
    "root_deviation_ordered_paths": [finish((a,)) for a in range(p)],
    "root_deviation_payoffs": [payoff(finish((a,)), 0) for a in range(p)],
    "kernel": kernel, "stationary_distribution": pi,
    "stationarity_rank": stationarity_rank,
    "unique_stationary_distribution": True,
    "root_follower_backgrounds": tails,
    "query_values": query_values, "cap": cap,
    "threshold_W_over_m_minus_half": threshold,
    "strict_cap_excess": cap-threshold,
    "scaled_cap_to_welfare": F(2*m-1, 2)*cap/welfare,
    "alternative_actual_last_prefix": alternative_background,
    "alternative_actual_last_prefix_query_values": alternative_values,
    "alternative_actual_last_prefix_cap": max(alternative_values),
}
target = HERE / ("weak_stationary_kernel_simple_audit.json" if "simple" in source_path.name
                 else "weak_stationary_kernel_audit.json")
target.write_text(json.dumps(serializable(report), indent=2) + "\n")
print(json.dumps(serializable(report), indent=2))
