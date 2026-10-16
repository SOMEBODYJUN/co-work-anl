#!/usr/bin/env python3
"""固定槽图族的最小Hamming跨槽修复：独立整数全枚举。"""
from itertools import product, permutations
from math import factorial
import json
import platform


def loads_scaled(m, sigma):
    loads = [0] * m
    for j, i in enumerate(sigma):
        loads[i] += m + 1 if j == 0 else 1
    return loads


def audit(m):
    n = m * m
    optimal = []
    enumerated = 0
    for sigma in product(range(m), repeat=n):
        enumerated += 1
        if max(loads_scaled(m, sigma)) <= m + 1:
            optimal.append(sigma)
    expected_optimal = m * factorial(n - 1) // (factorial(m + 1) ** (m - 1))
    assert len(optimal) == expected_optimal
    slot_schedules = []
    for block_permutations in product(list(permutations(range(m))), repeat=m):
        sigma = tuple(i for block in block_permutations for i in block)
        assert all(sigma.count(i) == m for i in range(m))
        slot_schedules.append(sigma)
    assert len(slot_schedules) == factorial(m) ** m
    minima_same = set()
    minima_move = set()
    constructed_distances = set()
    for sigma in slot_schedules:
        same_big = []
        moved_big = []
        for target in optimal:
            distance = sum(a != b for a, b in zip(sigma, target))
            (same_big if sigma[0] == target[0] else moved_big).append(distance)
        minima_same.add(min(same_big))
        if moved_big:
            minima_move.add(min(moved_big))
        source = sigma[0]
        small = [j for j in range(1, n) if sigma[j] == source]
        destinations = [i for i in range(m) if i != source]
        target = list(sigma)
        for j, i in zip(small, destinations):
            target[j] = i
        assert loads_scaled(m, target) == [m + 1] * m
        constructed_distances.add(sum(a != b for a, b in zip(sigma, target)))
    assert minima_same == constructed_distances == {m - 1}
    assert minima_move == ({m + 1} if m > 1 else set())
    return {
        "m": m, "n": n, "all_assignments": enumerated,
        "optimal_assignments": len(optimal), "slot_supported_assignments": len(slot_schedules),
        "all_slot_to_optimal_pairs_examined": len(slot_schedules) * len(optimal),
        "same_big_minimum_Hamming_values": sorted(minima_same),
        "moved_big_minimum_Hamming_values": sorted(minima_move),
        "constructed_optimal_repair_Hamming_values": sorted(constructed_distances),
    }


if __name__ == "__main__":
    print(json.dumps({
        "title": "固定槽图族的最小Hamming修复独立全枚举",
        "python": platform.python_version(),
        "arithmetic": "exact integers, processing times scaled by m+1",
        "records": [audit(m) for m in [1, 2, 3]],
        "scope": "Complete finite enumeration for m<=3; general proof requires the two big-job-location cases.",
    }, ensure_ascii=False, indent=2))
