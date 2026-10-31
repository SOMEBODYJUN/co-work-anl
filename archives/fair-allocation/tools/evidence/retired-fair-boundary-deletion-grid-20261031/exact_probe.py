"""Deterministic exact probes for fair-allocation topic reselection.

Only integer arithmetic is used. The chore probe enumerates item-type count
allocations, not labelled copies; this quotient is exact because copies of a
type have identical costs for all agents. No random search is used.
"""
import itertools
import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def compositions(total, n=4):
    if n == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, n - 1):
            yield (first,) + rest


def chore_counts(a, b, c):
    rows = list(itertools.product(compositions(a), compositions(b), compositions(c)))
    return np.asarray(rows, dtype=np.int64).transpose(0, 2, 1)


def efx_mask(counts, middle, large):
    costs = np.asarray([[large, 1, middle]] * 2 + [[large, middle, 1]] * 2,
                       dtype=np.int64)
    good = np.ones(len(counts), dtype=bool)
    for i in range(4):
        bundle_costs = counts @ costs[i]
        owned = counts[:, i, :]
        smallest = np.min(np.where(owned > 0, costs[i], 10**9), axis=1)
        trim = np.where(np.sum(owned, axis=1) > 0,
                        bundle_costs[:, i] - smallest, 0)
        good &= trim <= np.min(bundle_costs, axis=1)
    return good


def partitions(total, minpart=1):
    if total == 0:
        yield ()
    for first in range(minpart, total + 1):
        for rest in partitions(total - first, first):
            yield (first,) + rest


def multipartite_coloring(parts, n):
    parts = sorted(parts, reverse=True)
    bundles = [[] for _ in range(n)]
    if sum(parts) < n:
        j = 0
        for p, size in enumerate(parts):
            for v in range(size):
                bundles[j].append((p, v))
                j += 1
        return bundles
    if parts[0] >= n:
        for v in range(parts[0]):
            bundles[v % n].append((0, v))
        return bundles
    chosen = []
    for size in parts:
        chosen.append(size)
        if sum(chosen) >= n:
            break
    counts = [(size + 1) // 2 for size in chosen]
    assert sum(counts) <= n
    remaining = n - sum(counts)
    for p, size in enumerate(chosen):
        add = min(remaining, size - counts[p])
        counts[p] += add
        remaining -= add
    assert remaining == 0
    j = 0
    for p, (size, colors) in enumerate(zip(chosen, counts)):
        for v in range(size):
            bundles[j + v % colors].append((p, v))
        j += colors
    return bundles


def validate(parts, n, bundles):
    parts = sorted(parts, reverse=True)
    assert len(bundles) == n
    sizes = [len(b) for b in bundles]
    assert max(sizes) - min(sizes) <= 1
    colored = set()
    for b in bundles:
        assert len({p for p, _ in b}) <= 1
        for vertex in b:
            assert vertex not in colored
            colored.add(vertex)
    for p, size in enumerate(parts):
        for v in range(size):
            if (p, v) not in colored:
                for b in bundles:
                    assert any(q != p for q, _ in b)


def run():
    report = {"date": "2026-10-20", "seed": None,
              "arithmetic": "int64 exact, entries at most 50 and 13 chores"}
    counts = chore_counts(3, 5, 5)
    base = efx_mask(counts, 7, 20)
    assert len(counts) == math.comb(6, 3) * math.comb(8, 3)**2 == 62720
    assert not np.any(base)
    report["he_tao_reproduction"] = {
        "agents": 4, "type_multiplicities": [3, 5, 5],
        "costs": [[20, 1, 7], [20, 1, 7], [20, 7, 1], [20, 7, 1]],
        "allocation_types": len(counts), "efx_types": int(base.sum())}
    grid = []
    for middle in range(2, 13):
        for large in range(middle + 1, 51):
            mask = efx_mask(counts, middle, large)
            grid.append({"middle": middle, "large": large,
                         "efx_types": int(mask.sum())})
    report["fixed_13_grid"] = {"middle_range": [2, 12], "large_range": "middle+1..50",
                               "points": len(grid),
                               "nonexistence_points": sum(x["efx_types"] == 0 for x in grid)}
    smaller = []
    for a, b, c in itertools.product(range(4), range(6), range(6)):
        if a + b + c > 12 or a + b + c == 0:
            continue
        arr = chore_counts(a, b, c)
        mask = efx_mask(arr, 7, 20)
        smaller.append({"multiplicities": [a, b, c], "allocation_types": len(arr),
                        "efx_types": int(mask.sum())})
    report["deletion_minimal_probe"] = {
        "scope": "all nonempty coordinatewise subinstances of (3,5,5), total<=12, costs fixed (1,7,20)",
        "instances": len(smaller),
        "nonexistence_instances": [x for x in smaller if x["efx_types"] == 0]}
    checked = 0
    for total in range(1, 31):
        for parts in partitions(total):
            for n in range(1, 13):
                bundles = multipartite_coloring(parts, n)
                validate(parts, n, bundles)
                checked += 1
    report["multipartite_lemma_check"] = {
        "all_integer_partitions_of_total": [1, 30], "agents": [1, 12],
        "cases": checked, "failures": 0}
    (HERE / "probe_results.json").write_text(json.dumps(report, indent=2))
    (HERE / "trivalued_grid.json").write_text(json.dumps(grid, indent=2))
    (HERE / "deletion_subinstances.json").write_text(json.dumps(smaller, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    run()
