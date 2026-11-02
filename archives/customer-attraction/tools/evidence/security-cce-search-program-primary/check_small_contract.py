"""Small deterministic interface check; never calls the original main/random search.

The ordered-history and ordered-player LP constructions below do not import a
repository model, solver, certificate checker, or previous CCE audit.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib
import importlib.util
import json
import platform
import sys

import numpy as np
import scipy
from scipy.optimize import linprog

BASE = Path(__file__).resolve().parent
SOURCE = BASE / "original/search_cce.py"
spec = importlib.util.spec_from_file_location("original_search_cce", SOURCE)
source = importlib.util.module_from_spec(spec)
spec.loader.exec_module(source)


def check_case(name, k, m, weights, expected_cce):
    masks = list(range(1, 1 << k))
    r = np.array([weights.get(t, 0) for t in masks], dtype=float)
    d = source.data(k, m)
    _, profiles, counts, ix, uc, wc, g = d

    def welfare(z):
        return sum(v for t, v in weights.items() if any(t >> a & 1 for a in z))

    def utility(z, i):
        return sum((F(v, sum(t >> b & 1 for b in z))
                    for t, v in weights.items() if t >> z[i] & 1), F(0))

    # Exact, fully ordered recursion: different histories have separate caches.
    @lru_cache(None)
    def credible(h):
        if len(h) == m:
            return (h,)
        ch = [credible(h + (a,)) for a in range(k)]
        floor = max(min(utility(z, len(h)) for z in zs) for zs in ch)
        return tuple(z for zs in ch for z in zs if utility(z, len(h)) >= floor)

    credible_root = credible(())
    exact_counts = sorted({tuple(z.count(a) for a in range(k)) for z in credible_root})
    exact_target = min((ix[q] for q in exact_counts), key=lambda j: (welfare(profiles[j]), j))
    target, constraints, sigma = source.solve_spe(r, d, k, m)
    assert target == exact_target
    histories = [h for size in range(m) for h in product(range(k), repeat=size)]
    assert set(sigma) == set(histories)
    assert len(constraints) == k * len(histories)

    def finish(h):
        while len(h) < m:
            h += (sigma[h],)
        return h

    actual = finish(())
    assert tuple(actual.count(a) for a in range(k)) == counts[target]
    slacks = []
    exact_rows = []
    # Original expand appends each edge only after expanding its child.
    def rows(h):
        if len(h) == m:
            return
        actual_z = finish(h)
        for b in range(k):
            child_z = finish(h + (b,))
            rows(h + (b,))
            row = []
            for t in masks:
                za = sum(t >> a & 1 for a in actual_z)
                zb = sum(t >> a & 1 for a in child_z)
                left = F(1, za) if t >> sigma[h] & 1 else F(0)
                right = F(1, zb) if t >> b & 1 else F(0)
                row.append(left - right)
            exact_rows.append(row)
    rows(())
    assert np.allclose(constraints, np.array(exact_rows, dtype=float), atol=1e-14, rtol=0)
    for h in histories:
        z = finish(h)
        for b in range(k):
            slacks.append(utility(z, len(h)) - utility(finish(h + (b,)), len(h)))
    assert min(slacks) >= 0

    # Tensor check uses actual individual payoff differences on every ordered
    # terminal profile, independently of the occupancy aggregate formula.
    ordered = list(product(range(k), repeat=m))
    ordered_g = []
    for z in ordered:
        q = tuple(z.count(a) for a in range(k))
        j = ix[q]
        row = []
        assert abs(welfare(z) - wc[j] @ r) < 1e-12
        for a in range(k):
            agg = sum((utility(z, i) - utility(z[:i] + (a,) + z[i + 1:], i)
                       for i in range(m)), F(0))
            assert abs(float(agg) - g[j, a] @ r) < 1e-12
        for i in range(m):
            for a in range(k):
                row.append(float(utility(z, i) - utility(z[:i] + (a,) + z[i + 1:], i)))
        ordered_g.append(row)
    full = linprog([welfare(z) for z in ordered],
                   A_ub=-np.array(ordered_g).T, b_ub=np.zeros(m * k),
                   A_eq=np.ones((1, len(ordered))), b_eq=[1],
                   bounds=(0, None), method="highs")
    assert full.success
    val, y, lam = source.cce(r, d)
    assert abs(val - float(expected_cce)) < 1e-10
    assert abs(full.fun - val) < 1e-10
    assert min(y) >= -1e-12 and min(lam) >= -1e-12
    assert abs(sum(lam) - 1) < 1e-10
    dual_columns = wc @ r - (g @ r) @ y
    assert abs(min(dual_columns) - val) < 1e-10
    assert min((g @ r).T @ lam) >= -1e-10
    return {"name": name, "k": k, "m": m, "integer_weights": weights,
            "ordered_histories": len(histories), "constraints_with_self": len(slacks),
            "ordered_terminal_profiles": len(ordered), "occupancy_columns": len(profiles),
            "credible_root_count_outcomes": len(exact_counts),
            "target_sorted_representative": list(profiles[target]),
            "actual_ordered_path": list(actual), "minimum_exact_SPE_slack": str(min(slacks)),
            "SPE_welfare": welfare(actual), "expected_CCE": str(expected_cce),
            "source_occupancy_LP": val, "independent_individual_ordered_LP": full.fun,
            "minimum_dual_column": float(min(dual_columns)), "checked": True}


def main():
    cases = [check_case("three_disjoint_singletons", 3, 3, {1: 1, 2: 1, 4: 1}, F(21, 10)),
             check_case("zero_customers", 2, 3, {}, F(0)),
             check_case("one_player_two_topics", 2, 1, {1: 1, 2: 2}, F(2)),
             check_case("empty_and_duplicate_topics", 3, 3, {6: 1}, F(1)),
             check_case("one_topic", 1, 2, {1: 3}, F(3))]
    report = {"source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              "python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
              "original_main_calls": 0, "random_search_calls": 0, "original_data_calls": 5,
              "original_solve_spe_calls": 5, "original_cce_LP_calls": 5,
              "independent_ordered_individual_LP_calls": 5,
              "new_exact_counterexample_claim": False, "cases": cases}
    output = BASE / "small-contract-check.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"checked_cases": len(cases), "report": str(output.relative_to(BASE))}))


if __name__ == "__main__":
    main()
