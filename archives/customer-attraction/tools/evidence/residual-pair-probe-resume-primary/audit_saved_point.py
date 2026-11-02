"""One independent exact audit of the frozen five-player saved point.

Does not import either original probe, run a random batch, or certify float
outputs by tolerance. SciPy only proposes static primal/dual candidates;
Fraction verifies every inequality and equal objective values afterwards.
"""
from __future__ import annotations

from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement, product
from math import lcm
from pathlib import Path
import hashlib
import json
import platform

import numpy as np
import scipy
from scipy.optimize import linprog


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "original/pair_probe_r5b0.json"
saved = json.loads(SOURCE.read_text())
instance = saved["best"]["instance"]
k, r = instance["k"], instance["r"]
weights = tuple(instance["weights"])
prefix = tuple(instance["prefix"])
assert k == 7 and r == 5 and not prefix
assert len(weights) == (1 << k) - 1
assert all(type(w) is int and w >= 0 for w in weights)
types = tuple((mask, w) for mask, w in enumerate(weights, 1) if w)
scale = lcm(*range(1, r + len(prefix) + 1))


def counts(actions):
    return tuple(actions.count(a) for a in range(k))


def multisets(n):
    return tuple(counts(a) for a in combinations_with_replacement(range(k), n))


def add(q, a):
    return q[:a] + (q[a] + 1,) + q[a + 1:]


def load(mask, q):
    return sum(q[a] for a in range(k) if (mask >> a) & 1)


background = counts(prefix)
terminals = multisets(r)


def integer_pay(q, a):
    # Only consumed for occupied labels; absent-label zero convention is harmless.
    # All positive denominators divide scale.
    answer = 0
    for mask, w in types:
        if (mask >> a) & 1:
            den = load(mask, background) + load(mask, q)
            if den:
                assert scale % den == 0
                answer += w * (scale // den)
    return answer


pay = {q: tuple(integer_pay(q, a) for a in range(k)) for q in terminals}
total = {q: sum(q[a] * pay[q][a] for a in range(k)) for q in terminals}


@lru_cache(None)
def outcomes(q):
    if sum(q) == r:
        return frozenset((q,))
    children = [outcomes(add(q, a)) for a in range(k)]
    threshold = max(min(pay[z][a] for z in child) for a, child in enumerate(children))
    return frozenset(z for a, child in enumerate(children) for z in child
                     if pay[z][a] >= threshold)


root = (0,) * k
root_outcomes = outcomes(root)
assert len(root_outcomes) == instance["root_outcomes"] == 1
target = next(iter(root_outcomes))
assert target == tuple(instance["terminal"])

# Construct a fresh complete ordered strategy, not merely an on-path list.
# Each unchosen child minimizes this mover's payoff among that child's
# implementable outcomes; each occurrence is expanded separately in the tree.
policy = {}


def implement(h, target_here):
    q = counts(h)
    if len(h) == r:
        assert q == target_here
        return
    children = [outcomes(add(q, a)) for a in range(k)]
    threshold = max(min(pay[z][a] for z in child) for a, child in enumerate(children))
    chosen = next(a for a, child in enumerate(children)
                  if target_here in child and pay[target_here][a] >= threshold)
    policy[h] = chosen
    for a, child in enumerate(children):
        child_target = target_here if a == chosen else min(child, key=lambda z: (pay[z][a], z))
        implement(h + (a,), child_target)


implement((), target)
assert len(policy) == sum(k ** j for j in range(r))


@lru_cache(None)
def finish(h):
    if len(h) == r:
        return h
    return finish(h + (policy[h],))


def exact_utility(a, actions):
    answer = F(0)
    for mask, w in types:
        if (mask >> a) & 1:
            den = sum((mask >> b) & 1 for b in prefix + actions)
            assert den > 0
            answer += F(w, den)
    return answer


path = finish(())
assert path == tuple(instance["ordered_path"])
all_slacks, nonself_slacks = [], []
for depth in range(r):
    for h in product(range(k), repeat=depth):
        a = policy[h]
        obey = exact_utility(a, finish(h))
        for b in range(k):
            slack = obey - exact_utility(b, finish(h + (b,)))
            assert slack >= 0
            all_slacks.append(slack)
            if b != a:
                nonself_slacks.append(slack)

path_payoffs = tuple(exact_utility(a, path) for a in path)
assert [float(x) for x in path_payoffs] == instance["path_payoffs"]
assert sum(path_payoffs) == F(str(instance["tail_total"]))


def rational_static_game(j):
    """Exact security at the j-th selected path prefix; both sides saved."""
    remaining = r - j
    bg = counts(prefix + path[:j])
    rivals = multisets(remaining - 1)
    matrix = tuple(tuple(sum((F(w, 1 + load(mask, bg) + load(mask, q))
                              for mask, w in types if (mask >> a) & 1), F(0))
                         for a in range(k)) for q in rivals)
    array = np.array([[float(x) for x in row] for row in matrix])
    result = linprog(np.r_[np.zeros(k), -1.],
                     A_ub=np.c_[-array, np.ones(len(rivals))],
                     b_ub=np.zeros(len(rivals)),
                     A_eq=[np.r_[np.ones(k), 0.]], b_eq=[1.],
                     bounds=[(0, None)] * k + [(None, None)], method="highs")
    assert result.success, result.message
    p = tuple(F(float(x)).limit_denominator(10 ** 7) for x in result.x[:k])
    dual = tuple(F(float(x)).limit_denominator(10 ** 7) for x in -result.ineqlin.marginals)
    assert min(p) >= 0 and sum(p) == 1
    assert min(dual) >= 0 and sum(dual) == 1
    query_guarantees = tuple(sum((row[a] * p[a] for a in range(k)), F(0)) for row in matrix)
    pure_caps = tuple(sum((dual[i] * matrix[i][a] for i in range(len(rivals))), F(0))
                      for a in range(k))
    value = min(query_guarantees)
    assert max(pure_caps) == value
    assert all(x >= value for x in query_guarantees)
    assert all(x <= value for x in pure_caps)
    return {
        "step": j, "remaining": remaining, "prefix": list(prefix + path[:j]),
        "rival_count": len(rivals), "value": str(value),
        "primal_p": [str(x) for x in p],
        "dual_support": [{"count": list(q), "probability": str(x)}
                         for q, x in zip(rivals, dual) if x],
        "primal_all_row_min": str(min(query_guarantees)),
        "dual_all_label_max": str(max(pure_caps)),
        "original_saved_float": saved["best"]["values"][j],
        "original_float_error": str(F.from_float(saved["best"]["values"][j]) - value),
        "proposal_solver_status": int(result.status),
    }, value


static_audits, values = zip(*(rational_static_game(j) for j in range(r)))
pair_values = [path_payoffs[j] + path_payoffs[j + 1] + (r - j - 2) * values[j + 2]
               - (r - j) * values[j] for j in range(r - 2)]
assert pair_values[saved["best"]["step"]] == 0
coverage = {q: sum(w for mask, w in types if load(mask, q)) for q in terminals}
opt = max(coverage.values())
report = {
    "status": "exact finite saved-point audit; no random batch or universal PAIR proof",
    "input_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "runtime": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
    "dimensions": {"labels": k, "players": r, "unit_customers": sum(weights),
                   "nonzero_types": len(types), "terminal_counts": len(terminals),
                   "visited_count_states": outcomes.cache_info().currsize,
                   "full_ordered_decisions": len(policy),
                   "all_action_comparisons": len(all_slacks), "nonself_comparisons": len(nonself_slacks)},
    "nonzero_weights": {str(mask): w for mask, w in types},
    "root_outcomes": [list(q) for q in sorted(root_outcomes)],
    "recovered_path": list(path), "path_payoffs": [str(x) for x in path_payoffs],
    "remaining_total": str(sum(path_payoffs)), "root_coverage": coverage[target],
    "minimum_exact_IC_slack": str(min(all_slacks)),
    "minimum_exact_nonself_IC_slack": str(min(nonself_slacks)),
    "static_games": list(static_audits), "exact_pair_balances": [str(x) for x in pair_values],
    "OPT_5": opt, "one_optimal_count": list(next(q for q in terminals if coverage[q] == opt)),
    "twice_W_minus_OPT_5": 2 * coverage[target] - opt,
    "original_helper_main_runs": 0, "original_pair_main_runs": 0, "random_samples_run": 0,
}
(HERE / "exact-saved-point-audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
strategy = {"status": "new independently reconstructed complete strategy; not present in frozen JSON",
            "k": k, "r": r, "ordered_history_actions": [
                {"history": list(h), "action": policy[h]} for h in sorted(policy, key=lambda h: (len(h), h))]}
(HERE / "new-complete-strategy.json").write_text(json.dumps(strategy, separators=(",", ":")) + "\n")
print(json.dumps({key: report[key] for key in ("status", "dimensions", "recovered_path", "path_payoffs",
                                             "remaining_total", "exact_pair_balances", "OPT_5")},
                 ensure_ascii=False, indent=2))
