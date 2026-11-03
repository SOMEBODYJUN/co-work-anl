"""Independent audit of raw query-2 multiplicities and a complete action table.

Does not import any discovery/audit implementation.  Every multiplicity is
expanded into distinct unit clients.  Fractions and integer counters are exact.
"""

from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ACTOR = HERE.parent
raw = json.loads((ACTOR / "round5_coupling/stationary_348_diagnostic.json").read_text())
candidate = next(row for row in raw["results"] if row["query"] == 2)
unit_clients = tuple(mask for row in candidate["unit_customers"]
                     for mask in [row["mask"]] * row["multiplicity"])
assert len(unit_clients) == 6286
old = json.loads((ACTOR / "representation/high_insertion_2cycle_348_exact.json").read_text())
actions = {tuple(row["history"]): row["action"] for row in old["certificate"]["actions"]}
m, k = 3, 6
expected_nodes = {h for depth in range(m) for h in product(range(k), repeat=depth)}
assert set(actions) == expected_nodes
assert all(a in range(k) for a in actions.values())


def finish(history):
    history = tuple(history)
    while len(history) < m:
        history += (actions[history],)
    return history


@lru_cache(None)
def summary(terminal):
    own_counters = [Counter() for _ in range(m)]
    extra_counters = [Counter() for _ in range(k)]
    covered = 0
    for mask in unit_clients:
        load = sum(bool(mask & (1 << a)) for a in terminal)
        if load:
            covered += 1
            for i, a in enumerate(terminal):
                if mask & (1 << a):
                    own_counters[i][load] += 1
        for a in range(k):
            if mask & (1 << a):
                extra_counters[a][load + 1] += 1
    own = tuple(sum((F(v, d) for d, v in c.items()), F(0)) for c in own_counters)
    extra = tuple(sum((F(v, d) for d, v in c.items()), F(0)) for c in extra_counters)
    assert sum(own) == covered
    return own, extra, covered


def rank(matrix):
    mat = [list(row) for row in matrix]
    lead = 0
    for column in range(len(mat[0])):
        pivot = next((i for i in range(lead, len(mat)) if mat[i][column]), None)
        if pivot is None:
            continue
        mat[lead], mat[pivot] = mat[pivot], mat[lead]
        scale = mat[lead][column]
        mat[lead] = [x / scale for x in mat[lead]]
        for i in range(len(mat)):
            if i != lead and mat[i][column]:
                factor = mat[i][column]
                mat[i] = [x - factor * y for x, y in zip(mat[i], mat[lead])]
        lead += 1
        if lead == len(mat):
            break
    return lead


comparisons = []
for h in sorted(expected_nodes, key=lambda h: (len(h), h)):
    actual = finish(h)
    own = summary(actual)[0][len(h)]
    for a in range(k):
        deviating = finish(h + (a,))
        difference = own - summary(deviating)[0][len(h)]
        assert difference >= 0, (h, a, difference)
        comparisons.append({"history": h, "alternate": a, "margin": difference})

paths = [finish((a,)) for a in range(k)]
d = [summary(z)[0][0] for z in paths]
u = max(d)
K = [[summary(paths[b])[1][a] for b in range(k)] for a in range(k)]
P = [[F(z.count(a), m) for a in range(k)] for z in paths]
p = [F(1, 4), F(1, 4), F(0), F(1, 4), F(1, 4), F(0)]
assert all(sum(p[b] * P[b][a] for b in range(k)) == p[a] for a in range(k))
stationary_rank = rank([[P[b][a] - F(a == b) for b in range(k)] for a in range(k)])
assert stationary_rank == k - 1
prices = [sum(K[a][b] * p[b] for b in range(k)) for a in range(k)]
C = sum(p[a] * prices[a] for a in range(k))
D = sum(p[a] * d[a] for a in range(k))
Ubar = sum(p[b] * sum(summary(paths[b])[0]) / m for b in range(k))
T, Gamma = F(0), F(0)
for mask in unit_clients:
    loads = [sum(bool(mask & (1 << a)) for a in z) for z in paths]
    T += sum((p[b] * F(1, n + 1) if n else F(0)
              for b, n in enumerate(loads)), F(0)) / m
    Gamma += sum((p[b] * p[c] * F((loads[b] - loads[c])**2,
                                  (1 + loads[b]) * (1 + loads[c]))
                  for b in range(k) for c in range(k)), F(0)) / (2 * m)
assert C == Ubar - T + Gamma
assert D - C == D - Ubar + T - Gamma
assert prices[2] - u == F(123, 4)
pure_maxima = [max(K[a][b] for a in range(k)) for b in range(k)]
safe = [b for b in range(k) if pure_maxima[b] <= u]
W = summary(finish(()))[2]
OPT = max(summary(z)[2] for z in product(range(k), repeat=m))


def encode(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): encode(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [encode(v) for v in x]
    return x


output = {"status": "pass", "unit_clients": len(unit_clients),
          "complete_ordered_nodes": len(expected_nodes),
          "all_comparisons_including_same_action": len(comparisons),
          "genuine_comparisons": sum(row["alternate"] != actions[tuple(row["history"])]
                                     for row in comparisons),
          "minimum_margin": min(row["margin"] for row in comparisons),
          "forced_paths": paths, "root_d": d, "root_u": u,
          "K": K, "P_full_slot": P, "p": p, "stationarity_rank": stationary_rank,
          "Kp": prices, "stationary_query_2_overload": prices[2] - u,
          "D": D, "C": C, "D_minus_C": D - C,
          "Ubar": Ubar, "T": T, "Gamma": Gamma,
          "pure_column_maxima": pure_maxima, "safe_pure_columns": safe,
          "actual_W": W, "OPT_3": OPT,
          "half_margin_2W_minus_OPT": 2 * W - OPT,
          "all_exact_SPE_comparisons": comparisons}
target = HERE / "stationary_query2_independent_audit.json"
target.write_text(json.dumps(encode(output), indent=2) + "\n", encoding="utf-8")
print(json.dumps(encode({key: output[key] for key in (
    "status", "unit_clients", "complete_ordered_nodes", "all_comparisons_including_same_action",
    "root_u", "Kp", "D", "C", "D_minus_C", "Ubar", "T", "Gamma",
    "pure_column_maxima", "safe_pure_columns", "actual_W", "OPT_3")})))
