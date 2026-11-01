"""New n=4 exact audit; neither imports nor runs the frozen LP program.

Rebuilds the source strategy recipe, compares its floating leaf selector with
exact seed maximization, then checks the rational reconstruction on every
count state AND every ordered history.  NumPy is used only for reproducing
the frozen float selector, never for certificate inequalities.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib
import json
import platform

import numpy as np


BASE = Path(__file__).resolve().parent
N, K = 4, 6
MASKS = tuple(range(1, 1 << K))
PRIORITY = (1, 0, 2, 3, 4, 5)
raw_bytes = (BASE / "original/structured_packing_4.json").read_bytes()
raw = json.loads(raw_bytes)
assert raw["n"] == N


def frac(value):
    # This proposes a new exact value, and does not equate floats to rationals.
    return F(str(value)).limit_denominator(10**6)


def compositions(total, length):
    if length == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for tail in compositions(total - first, length - 1):
                yield (first,) + tail


def add(q, action):
    return tuple(value + (index == action) for index, value in enumerate(q))


@lru_cache(None)
def payoff(q, action):
    return tuple(F(1, max(1, sum(q[b] for b in range(K) if mask >> b & 1)))
                 if mask >> action & 1 else F(0) for mask in MASKS)


def dot(row, point):
    return sum((a * b for a, b in zip(row, point)), F(0))


seed = {mask: F(0) for mask in MASKS}
for j in range(N):
    leaf = 1 << (j + 2)
    seed[leaf] = seed[leaf + 2] = F(N - 2)
    seed[leaf + (1 if j < N - 1 else 3)] = F(1 if j < N - 1 else N - 1)
seed_vector = tuple(seed[m] for m in MASKS)
float_masks = np.array([[int(m >> a & 1) for a in range(K)] for m in MASKS], dtype=float)
float_seed = np.array([float(v) for v in seed_vector])


def float_value(q, action):
    matrix = (float_masks / np.maximum(1, float_masks @ np.array(q))[:, None]).T
    return float(matrix[action] @ float_seed)


states = [q for size in range(N) for q in compositions(size, K)]
moves = {}
float_moves = {}
leaf_ties = 0
for q in states:
    if sum(q) < N - 1:
        moves[q] = float_moves[q] = 0 if q[1] == sum(q) else 1
    else:
        values = {a: dot(payoff(add(q, a), a), seed_vector) for a in range(K)}
        moves[q] = max(PRIORITY, key=values.__getitem__)
        float_moves[q] = max(PRIORITY, key=lambda a: float_value(add(q, a), a))
        leaf_ties += sum(v == max(values.values()) for v in values.values()) > 1
selector_differences = [list(q) for q in states if moves[q] != float_moves[q]]
assert not selector_differences, selector_differences


@lru_cache(None)
def finish(q):
    return q if sum(q) == N else finish(add(q, moves[q]))


rows = {}
for q in states:
    a = moves[q]
    chosen = payoff(finish(add(q, a)), a)
    for deviation in range(K):
        alternative = payoff(finish(add(q, deviation)), deviation)
        rows[q, deviation] = tuple(x - y for x, y in zip(chosen, alternative))
seed_slacks = [dot(row, seed_vector) for row in rows.values()]
assert min(seed_slacks) >= 0
root = (0,) * K
terminal = finish(root)
u = payoff(terminal, moves[root])
blocks = {a: tuple(F(not (m & 1) and bool(m >> a & 1)
                    and sum(bool(m >> b & 1) for b in range(2, K)) == 1)
                   for m in MASKS) for a in range(2, K)}
weights = {m: F(0) for m in MASKS}
for mask, value in raw["w"]:
    assert mask in weights and value > 0
    weights[mask] = frac(value)
w = tuple(weights[m] for m in MASKS)
t = frac(raw["ratio"])
slacks = {key: dot(row, w) for key, row in rows.items()}
assert min(slacks.values()) >= 0
assert dot(u, w) == 1
block_values = {a: dot(e, w) for a, e in blocks.items()}
assert min(block_values.values()) == t

# Reconstruct the omitted equality multiplier y and ALL 63 reduced costs.
dual_ic, dual_pack = {}, {}
for key, value in raw["dual"]:
    coefficient = -frac(value)
    assert coefficient >= 0
    if key[0] == "pack":
        assert key[1] + 2 not in dual_pack
        dual_pack[key[1] + 2] = coefficient
    else:
        label = (tuple(key[0]), key[1])
        assert label in rows and label not in dual_ic
        dual_ic[label] = coefficient
assert sum(dual_pack.values(), F(0)) == 1
y = t
residual = tuple(y * u[i]
                 - sum((v * rows[key][i] for key, v in dual_ic.items()), F(0))
                 - sum((v * blocks[a][i] for a, v in dual_pack.items()), F(0))
                 for i in range(len(MASKS)))
assert min(residual) >= 0
assert dot(residual, w) == 0
assert all(v * slacks[key] == 0 for key, v in dual_ic.items())
assert all(v * (block_values[a] - t) == 0 for a, v in dual_pack.items())


def counts(history):
    return tuple(history.count(a) for a in range(K))


def complete(history):
    result = tuple(history)
    while len(result) < N:
        result += (moves[counts(result)],)
    return result


def utility(history, actor):
    return dot(payoff(counts(history), history[actor]), w)


# This separate ordered-history loop is deliberately uncompressed.
history_total = ordered_rows = 0
ordered_slacks = []
for depth in range(N):
    for history in product(range(K), repeat=depth):
        history_total += 1
        chosen = utility(complete(history), depth)
        for action in range(K):
            alternative = utility(complete(history + (action,)), depth)
            slack = chosen - alternative
            assert slack == slacks[counts(history), action]
            ordered_slacks.append(slack)
            ordered_rows += 1
assert min(ordered_slacks) >= 0
actual = complete(())


def coverage(history):
    selected = set(history)
    return sum((weights[m] for m in MASKS if any(m >> a & 1 for a in selected)), F(0))


all_profiles = list(product(range(K), repeat=N))
opt = max(map(coverage, all_profiles))
welfare = coverage(actual)
best_after_root_A = max(coverage((0,) + tail) for tail in product(range(K), repeat=N - 1))
denominator = 1
from math import lcm
for value in w:
    denominator = lcm(denominator, value.denominator)
assert sum(utility(actual, i) for i in range(N)) == welfare
result = {
    "status": "NEW exact certificate for this fixed n=4 strategy cone; not an all-strategy bound",
    "inputs": [{"path": str(path.relative_to(BASE)), "bytes": len(path.read_bytes()),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
               for path in (BASE / "original").iterdir() if path.is_file()],
    "environment": {"python": platform.python_version(), "numpy": np.__version__},
    "rationalization_rule": "Fraction(str(float)).limit_denominator(1000000), followed by exact checks",
    "n": N, "catalog_size": K, "nonempty_type_columns": len(MASKS),
    "seed": [[m, str(seed[m])] for m in MASKS if seed[m]],
    "leaf_priority": list(PRIORITY), "last_count_states_with_exact_ties": leaf_ties,
    "float_and_exact_seed_selector_differences": selector_differences,
    "count_states": len(states), "count_ic_rows_including_self": len(rows),
    "terminal_count_vectors": len(list(compositions(N, K))),
    "ordered_histories": history_total, "ordered_ic_rows_including_self": ordered_rows,
    "ordered_terminal_profiles_for_OPT": len(all_profiles),
    "minimum_seed_IC": str(min(seed_slacks)), "minimum_exact_IC": str(min(slacks.values())),
    "minimum_ordered_IC": str(min(ordered_slacks)),
    "exact_optimum": str(t), "root_normalization": str(dot(u, w)),
    "primal": [[m, str(weights[m])] for m in MASKS if weights[m]],
    "block_sizes": [[a, str(v)] for a, v in block_values.items()],
    "reconstructed_equality_multiplier": str(y),
    "dual_ic": [[list(q), a, str(v)] for (q, a), v in dual_ic.items()],
    "dual_pack": [[a, str(v)] for a, v in dual_pack.items()],
    "dual_nonnegative_residual_all_columns": [[m, str(residual[m - 1])] for m in MASKS],
    "dual_min_residual": str(min(residual)),
    "dual_zero_residual_count": sum(v == 0 for v in residual),
    "complementarity_all_exact": True,
    "actual_actions": list(actual), "actual_terminal_counts": list(terminal),
    "actual_utilities": [str(utility(actual, i)) for i in range(N)],
    "welfare": str(welfare), "OPT4": str(opt), "OPT4_over_W": str(opt / welfare),
    "best_coverage_after_root_A": str(best_after_root_A),
    "root_coverage_opportunity_loss": str(opt - best_after_root_A),
    "root_opportunity_loss_over_root_utility": str((opt - best_after_root_A) / dot(u, w)),
    "integer_unit_customer_scaling": denominator,
    "integer_types": [[m, int(weights[m] * denominator)] for m in MASKS if weights[m]],
    "integer_total_clients": int(sum(w) * denominator),
    "moves_all_count_states": [[list(q), moves[q]] for q in states],
    "count_IC_slack_histogram": dict(sorted(Counter(str(v) for v in slacks.values()).items())),
    "source_float_ratio": raw["ratio"],
    "source_float_primal_and_exact_proposals": [[m, value, str(weights[m]),
         str(F(str(value)) - weights[m])] for m, value in raw["w"]],
    "source_float_dual_and_exact_proposals": [[key, value, str(frac(value)),
         str(F(str(value)) - frac(value))] for key, value in raw["dual"]],
}
output = BASE / "exact-audit.json"
output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({key: result[key] for key in (
    "status", "count_states", "count_ic_rows_including_self", "ordered_histories",
    "ordered_ic_rows_including_self", "minimum_exact_IC", "exact_optimum",
    "dual_min_residual", "welfare", "OPT4", "integer_total_clients")}, ensure_ascii=False))
