#!/usr/bin/env python3
"""Exact independent single-row CONFIG decomposition and finite hull audit.

One incoming job has time 1, k outgoing jobs each time 1/k, threshold
1+s/k with integers k>=1 and 0<=s<k. q is incoming marginal, and t_j is
the outgoing job's other-end/down marginal, so its local marginal is 1-t_j.
Input JSON: {"k":4,"s":1,"q":"1/2","t":[...],"c":[...optional lift...]}.
No-input mode audits a small exact grid against all original configurations;
SciPy only locates supports, which are then solved and verified over Fraction.
Every infeasible point has an exact separator checked at every original vertex.
"""
from bisect import bisect_right
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import argparse
import json
import sys

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

VERSION = "independent-uniform-incoming-row-config-v2"


def ceil(x):
    return -(-x.numerator // x.denominator)


def cube_distribution(marginals):
    boundaries = sorted({F(0), F(1), *marginals})
    answer = []
    for left, right in zip(boundaries, boundaries[1:]):
        if left == right:
            continue
        midpoint = (left + right) / 2
        subset = tuple(i for i, z in enumerate(marginals) if z > midpoint)
        answer.append((right - left, subset))
    return answer


def uniform_rank_distribution(marginals, rank):
    """Explicit rank<=rank uniform-matroid decomposition, O(k) outcomes."""
    if any(z < 0 or z > 1 for z in marginals):
        raise ValueError("uniform-rank coordinate outside [0,1]")
    total = sum(marginals, F(0))
    integer_total = ceil(total)
    if integer_total > rank:
        raise ValueError("uniform-rank sum exceeds rank")
    if integer_total == 0:
        return [(F(1), ())]
    real_count = len(marginals)
    lengths = list(marginals)
    deficit = integer_total - total
    if deficit:
        lengths.append(deficit)  # At most one dummy coordinate, length<1.
    prefix = [F(0)]
    for z in lengths:
        prefix.append(prefix[-1] + z)
    assert prefix[-1] == integer_total
    boundaries = sorted({F(0), F(1), *(z - (z.numerator // z.denominator) for z in prefix)})
    answer = []
    for left, right in zip(boundaries, boundaries[1:]):
        if left == right:
            continue
        midpoint = (left + right) / 2
        chosen = []
        for j in range(integer_total):
            point = midpoint + j
            item = bisect_right(prefix, point) - 1
            assert 0 <= item < len(lengths)
            if item < real_count:
                chosen.append(item)
        if len(set(chosen)) != len(chosen) or len(chosen) > rank:
            raise RuntimeError("shifted grid failed a uniform-rank configuration")
        answer.append((right - left, tuple(sorted(chosen))))
    # Verify the constructive decomposition without invoking a polytope theorem.
    assert sum((weight for weight, subset in answer), F(0)) == 1
    actual = [sum((weight for weight, subset in answer if i in subset), F(0))
              for i in range(real_count)]
    assert actual == list(marginals)
    return answer


def validate_result(k, s, q, t, configurations):
    threshold = F(1) + F(s, k)
    assert sum((row["weight"] for row in configurations), F(0)) == 1
    actual_q = F(0)
    actual_local = [F(0)] * k
    for row in configurations:
        weight, incoming, outgoing = row["weight"], row["incoming"], row["outgoing"]
        assert weight > 0 and incoming in (0, 1)
        assert len(set(outgoing)) == len(outgoing)
        assert all(0 <= i < k for i in outgoing)
        load = F(incoming) + F(len(outgoing), k)
        assert load <= threshold and row["load"] == load
        actual_q += weight * incoming
        for i in outgoing:
            actual_local[i] += weight
    assert actual_q == q and actual_local == [1 - z for z in t]


def decompose(k, s, q, t, lift=None):
    if type(k) is not int or k < 1 or type(s) is not int or not 0 <= s < k:
        raise ValueError("integers k>=1 and 0<=s<k required")
    q, t = F(q), tuple(F(z) for z in t)
    if len(t) != k or not 0 <= q <= 1 or any(z < 0 or z > 1 for z in t):
        raise ValueError("one down marginal per outgoing job, all coordinates in [0,1]")
    lower = [max(F(0), q - z) for z in t]
    if sum(lower, F(0)) > s * q:
        raise ValueError("positive-part row condition is infeasible")
    if lift is None:
        raw = lower
    else:
        raw = [F(z) for z in lift]
        if len(raw) != k or any(z < lo for z, lo in zip(raw, lower)) or sum(raw, F(0)) > s * q:
            raise ValueError("provided lift violates its lower/sum constraints")
    # Lower/sum-only lifts need not initially be co-occurrence probabilities.
    joint = [min(z, q, 1 - down) for z, down in zip(raw, t)]
    assert all(z >= lo for z, lo in zip(joint, lower)) and sum(joint, F(0)) <= s * q
    support = defaultdict(F)
    if q:
        conditional = [z / q for z in joint]
        for weight, subset in uniform_rank_distribution(conditional, s):
            support[1, subset] += q * weight
    if q < 1:
        conditional = [(1 - down - z) / (1 - q) for z, down in zip(joint, t)]
        assert all(0 <= z <= 1 for z in conditional)
        for weight, subset in cube_distribution(conditional):
            support[0, subset] += (1 - q) * weight
    configurations = [{"weight": weight, "incoming": incoming, "outgoing": list(subset),
                       "load": F(incoming) + F(len(subset), k)}
                      for (incoming, subset), weight in sorted(support.items()) if weight]
    validate_result(k, s, q, t, configurations)
    return {"k": k, "s": s, "threshold": F(1) + F(s, k), "q": q, "t": t,
            "raw_lift": raw, "cooccurrence_lift": joint, "configurations": configurations}


def original_configurations(k, s):
    # Independent direct physical load enumeration, not the candidate formula.
    threshold = F(1) + F(s, k)
    answer = []
    for bits in product((0, 1), repeat=k + 1):
        load = F(bits[0]) + F(sum(bits[1:]), k)
        if load <= threshold:
            answer.append(bits)
    return answer


def exact_affine_support(vertices, indices, target):
    """Solve the floating oracle's selected support exactly by elimination."""
    n = len(indices)
    rows = [[F(1)] * n + [F(1)]]
    rows += [[F(vertices[j][i]) for j in indices] + [target[i]]
             for i in range(len(target))]
    pivot_row, pivots = 0, []
    for column in range(n):
        pivot = next((i for i in range(pivot_row, len(rows)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        factor = rows[pivot_row][column]
        rows[pivot_row] = [z / factor for z in rows[pivot_row]]
        for i in range(len(rows)):
            if i != pivot_row and rows[i][column]:
                factor = rows[i][column]
                rows[i] = [a - factor * b for a, b in zip(rows[i], rows[pivot_row])]
        pivots.append((pivot_row, column))
        pivot_row += 1
    assert all(any(row[:n]) or not row[-1] for row in rows)
    weight = [F(0)] * n
    for i, column in pivots:
        weight[column] = rows[i][-1]
    assert all(z >= 0 for z in weight) and sum(weight, F(0)) == 1
    assert all(sum((w * vertices[j][i] for w, j in zip(weight, indices)), F(0)) == target[i]
               for i in range(len(target)))
    return weight


def audit():
    import numpy as np
    from scipy.optimize import linprog
    grid = (F(0), F(1, 2), F(1))
    counts = {"grid_points": 0, "exact_feasible_hull_supports": 0,
              "exact_infeasible_vertex_separators": 0, "boundary_constructive_cases": 0}
    max_support = 0
    for k in range(1, 5):
        for s in range(k):
            vertices = original_configurations(k, s)
            matrix = np.array([[1] * len(vertices)] +
                              [[v[i] for v in vertices] for i in range(k + 1)], dtype=float)
            for coordinates in product(grid, repeat=k + 1):
                q, t = coordinates[0], coordinates[1:]
                target = (q,) + tuple(1 - z for z in t)
                valid = sum((max(F(0), q - z) for z in t), F(0)) <= s * q
                result = linprog(np.zeros(len(vertices)), A_eq=matrix,
                                 b_eq=np.array([1] + [float(z) for z in target]),
                                 bounds=(0, None), method="highs")
                if valid:
                    assert result.success
                    support = [i for i, weight in enumerate(result.x) if weight > 1e-10]
                    exact_affine_support(vertices, support, target)
                    constructed = decompose(k, s, q, t)
                    max_support = max(max_support, len(constructed["configurations"]))
                    counts["exact_feasible_hull_supports"] += 1
                else:
                    assert result.status == 2
                    indices = [i for i, z in enumerate(t) if q > z]
                    # Exact valid inequality on every enumerated original vertex:
                    # (|S|-s)*incoming + sum_{S}outgoing <= |S|.
                    assert all((len(indices) - s) * v[0] + sum(v[i + 1] for i in indices)
                               <= len(indices) for v in vertices)
                    assert (len(indices) - s) * q + sum((target[i + 1] for i in indices), F(0)) > len(indices)
                    counts["exact_infeasible_vertex_separators"] += 1
                counts["grid_points"] += 1
    # Arbitrary feasible lower/sum lift that needs clipping before interpretation.
    record = decompose(4, 2, F(1, 3), [1] * 4, [F(2, 3), 0, 0, 0])
    assert record["cooccurrence_lift"] == [0] * 4
    counts["boundary_constructive_cases"] += 1
    decompose(4, 2, F(1, 2), [F(3, 4)] * 4,
              [F(1, 4), F(1, 8), F(1, 4), F(1, 8)])
    counts["boundary_constructive_cases"] += 1
    huge = 10**5000 + 151
    for k, s, q, t in [(1, 0, F(0), [F(0)]), (1, 0, F(1), [F(1)]),
                       (5, 2, F(1), [F(3, 5)] * 5),
                       (5, 2, F(1), [F(0), F(1), F(3, 4), F(3, 4), F(1, 2)]),
                       (5, 2, F(0), [F(1), F(0), F(2, 3), F(1, 3), F(1, 5)]),
                       (5, 2, F(1, huge), [1 - F(1, huge)] * 5),
                       (3, 0, F(2, 7), [F(2, 7), F(5, 7), F(1)])]:
        decompose(k, s, q, t)
        counts["boundary_constructive_cases"] += 1
    return {"version": VERSION, "code_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
            "counts": counts, "maximum_constructed_support_on_grid": max_support,
            "over_4300_decimal_digits_denominator": True,
            "scope": "Single-row finite audit; all original configurations enumerated only for k<=4. "
                     "SciPy provides candidate supports/infeasibility flags; positive supports and "
                     "negative separating inequalities are certified over Fraction. The general theorem "
                     "rests on the explicit constructive proof, not these tests."}


def jsonable(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): jsonable(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [jsonable(v) for v in x]
    return x


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.input:
        data = json.loads(args.input.read_text())
        payload = decompose(data["k"], data["s"], data["q"], data["t"], data.get("c"))
    else:
        payload = audit()
    text = json.dumps(jsonable(payload), indent=2, ensure_ascii=False) + "\n"
    if args.output:
        with args.output.open("x") as handle:
            handle.write(text)
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
