"""Finite exact cross-check of the separate universal two-node proof.

No LP, source solver, or complete-strategy model is imported. Enumerating
H=0,...,5 is a finite supplement, never the proof for arbitrary marginals.
Edge order is own1, own2, cross1, cross2.
"""

from fractions import Fraction as F
from itertools import product
import json


ODD = tuple(mask for mask in range(16) if mask.bit_count() % 2)


def compositions(total):
    for a in range(total + 1):
        for b in range(total - a + 1):
            for c in range(total - a - b + 1):
                yield tuple(map(F, (a, b, c, total - a - b - c)))


def distance(H, values, mask):
    return sum((H - x if mask >> i & 1 else x
                for i, x in enumerate(values)), F())


def evaluate(first, second):
    a, b, c, d = first
    A, B, C, E = second
    H = sum(first, F())
    assert sum(second, F()) == H
    own = (b + c, B + C)
    q = (c + d, C + E)
    v = (b + d, B + E)
    ell = tuple(abs(q[i] - v[1 - i]) for i in range(2))
    upper = tuple(min(q[i] + v[1 - i], 2 * H - q[i] - v[1 - i])
                  for i in range(2))
    capacity = tuple(upper[i] - ell[i] for i in range(2))
    values = own + ell
    distances = {mask: distance(H, values, mask) for mask in ODD}
    violated = [mask for mask, val in distances.items() if val < H]
    rho = max(F(), H - min(distances.values()))
    g = (sum(own) - sum(ell)) / 2
    exact = (sum(own) - sum(ell) - rho) / 2
    six = min(b + c, B + C, b + B, c + C,
              b + c + d - E, B + C + E - d)
    assert exact == six == min(g, *own)
    assert g == min(q[0], v[1]) + min(q[1], v[0]) - d - E
    odd_bounds = {
        mask: sum((own[i] for i in range(2) if not mask >> i & 1), F())
        - sum((ell[i] for i in range(2) if mask >> (i + 2) & 1), F())
        + F(mask.bit_count() - 1, 2) * H
        for mask in ODD
    }
    assert odd_bounds[1] == own[1] and odd_bounds[2] == own[0]
    assert all(value >= g for mask, value in odd_bounds.items()
               if mask not in (1, 2))
    if rho:
        assert len(violated) == 1
        larger_index = 0 if own[0] > own[1] else 1
        assert violated == [1 << larger_index]
        assert rho == 2 * (g - min(own))
        for i in range(2):
            assert capacity[i] == 2 * min(q[i], v[1 - i],
                                          H - q[i], H - v[1 - i])
            assert capacity[i] >= rho
            repaired = list(values)
            repaired[i + 2] += rho
            assert ell[i] <= repaired[i + 2] <= upper[i]
            assert all(distance(H, repaired, mask) >= H for mask in ODD)
    else:
        assert not violated
    return {"H": str(H), "own": list(map(str, own)),
            "ell": list(map(str, ell)), "g": str(g), "rho": str(rho),
            "exact": str(exact), "cross_capacity": list(map(str, capacity)),
            "violating_odd_masks": violated,
            "odd_distances": {str(k): str(v) for k, v in distances.items()}}


def main():
    count = positive = 0
    by_H = []
    for H in range(6):
        margins = list(compositions(H))
        local_positive = 0
        for first, second in product(margins, repeat=2):
            result = evaluate(first, second)
            local_positive += F(result["rho"]) > 0
            count += 1
        positive += local_positive
        by_H.append({"H": H, "four_state_marginals": len(margins),
                     "ordered_pairs": len(margins) ** 2,
                     "positive_deficit_pairs": local_positive})
    assert count == 4878 and positive == 312
    example = evaluate(tuple(map(F, (0, 1, 1, 0))),
                       tuple(map(F, (1, 0, 0, 1))))
    assert example["violating_odd_masks"] == [1]
    assert example["odd_distances"]["1"] == "0"
    assert example["odd_distances"]["2"] == "4"
    print(json.dumps({
        "scope": "Finite Fraction cross-check only; universal transport and support claims use the separate analytic proof; no SPE or half claim",
        "edge_order": ["own1", "own2", "cross1", "cross2"],
        "H_range": [0, 5], "ordered_margin_pairs": count,
        "positive_deficit_pairs": positive, "by_H": by_H,
        "six_facets_equal_cycle_formula": True,
        "other_six_odd_bounds_at_least_free_bound": True,
        "positive_deficit_unique_larger_own_singleton": True,
        "either_cross_alone_has_capacity_and_repairs_all_odd_sets": True,
        "own_index_counterexample": {
            "first_00_01_10_11": [0, 1, 1, 0],
            "second_00_01_10_11": [1, 0, 0, 1], **example,
        },
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
