"""New exact reconstruction, not the missing historical integer audit.

Read the written all-even-degree proof for the universal result.  This file
checks the literal signed witnesses and the FULL degree-d Walsh Gram for
d=1,2,3.  No optimization solver, sampled vectors, or eigenvalue tolerance.
"""
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import hashlib
import json


def base_weights():
    weights = [0] * 16
    weights[0] = 18
    for j in range(4):
        weights[1 << j] = -5
    for i, j in combinations(range(4), 2):
        weights[(1 << i) | (1 << j)] = 1 if (i, j) == (2, 3) else 5
    return weights


def walsh_transform(values):
    result = list(values)
    stride = 1
    while stride < len(result):
        for start in range(0, len(result), 2 * stride):
            for j in range(start, start + stride):
                a, b = result[j], result[j + stride]
                result[j], result[j + stride] = a + b, a - b
        stride *= 2
    return result


def exact_positive_definite(matrix):
    """Exact Schur elimination; all pivots must be positive."""
    a = [[Fraction(x) for x in row] for row in matrix]
    pivots = []
    for i in range(len(a)):
        pivot = a[i][i]
        assert pivot > 0, (i, pivot)
        pivots.append(str(pivot))
        for j in range(i + 1, len(a)):
            for k in range(i + 1, len(a)):
                a[j][k] -= a[j][i] * a[i][k] / pivot
    return pivots


def lift_check(d):
    p, m = 4 * d, 2 * d
    blocks = [((1 << d) - 1) << (j * d) for j in range(4)]
    base = base_weights()
    weights = [
        base[sum(((b & block).bit_count() % 2) << j
                 for j, block in enumerate(blocks))]
        for b in range(1 << p)
    ]
    factor = 1 << (4 * (d - 1))
    moments = walsh_transform(weights)
    assert moments[0] == 24 * factor
    block_unions = [
        sum(blocks[j] for j in range(4) if s >> j & 1)
        for s in range(16)
    ]
    subgroup = set(block_unions)
    assert all(v == 0 for e, v in enumerate(moments) if e not in subgroup)
    visible = [a for a in range(1 << p) if a.bit_count() <= d]
    cosets = defaultdict(list)
    for a in visible:
        representative = min(a ^ s for s in block_unions)
        cosets[representative].append(a)
    for a in visible:
        for b in visible:
            if (a ^ b) not in subgroup:
                assert moments[a ^ b] == 0
    pivots = []
    for indices in cosets.values():
        gram = [[moments[a ^ b] for b in indices] for a in indices]
        pivots.extend(exact_positive_definite(gram))
    integer_value = 0
    for b, mass in enumerate(weights):
        ys = [(b & block).bit_count() % 2 for block in blocks]
        z = ys[0] + ys[1] - ys[2] - ys[3]
        assert z * (z - 1) >= 0
        integer_value += mass * z * (z - 1)
    assert integer_value == -4 * factor
    return {
        "d": d, "m": m, "labels": p, "literal_types": len(weights),
        "lift_factor": factor, "signed_total": moments[0],
        "all_degree_d_walsh_indices": len(visible),
        "full_gram_entries": len(visible) ** 2,
        "coset_count": len(cosets),
        "coset_size_histogram": dict(sorted(Counter(map(len, cosets.values())).items())),
        "all_exact_pivots_positive": True,
        "minimum_exact_pivot": str(min(map(Fraction, pivots))),
        "integer_row_value": integer_value,
        "integer_row_at_empty": 0,
    }


def main():
    base = base_weights()
    total = sum(base)
    c = [sum(w for b, w in enumerate(base) if b >> j & 1) for j in range(4)]
    jmat = [[sum(w for b, w in enumerate(base)
                 if b >> i & 1 and b >> j & 1) for j in range(4)]
            for i in range(4)]
    moment = [[total] + c] + [[c[i]] + jmat[i] for i in range(4)]
    pivots = exact_positive_definite(moment)
    assert total == 24 and c == [10, 10, 6, 6]
    inverse_c = [2, 2, -2, -2]
    assert [sum(row[j] * inverse_c[j] for j in range(4)) for row in jmat] == c
    assert sum(c[i] * inverse_c[i] for i in range(4)) == 16
    projection_cells = []
    for size in (0, 1, 2):
        for inds in combinations(range(4), size):
            support = sum(1 << i for i in inds)
            cells = defaultdict(int)
            for b, mass in enumerate(base):
                cells[b & support] += mass
            assert min(cells.values()) >= 0
            projection_cells.extend(cells.values())
    visible = [s for s in range(16) if s.bit_count() <= 2]
    parity = {s: sum(w for b, w in enumerate(base)
                     if (s & b).bit_count() % 2) for s in visible}
    triangle_count = 0
    for e in visible:
        for f in visible:
            if (e ^ f) in parity:
                assert parity[e] + parity[f] >= parity[e ^ f]
                triangle_count += 1
    result = {
        "identity": "new Boss2 exact reconstruction; not a historical replay",
        "scope": "literal base and FULL degree-d Grams for d=1,2,3 only",
        "base_weights": base, "base_total": total, "base_first_moments": c,
        "base_intersection_matrix": jmat,
        "base_affine_moment_exact_pivots": pivots,
        "base_projections_through_two_bits": 11,
        "base_minimum_projection_cell": min(projection_cells),
        "base_all_visible_ordered_triangles": triangle_count,
        "lifts": [lift_check(d) for d in (1, 2, 3)],
        "universal_claim_depends_on_written_coset_proof": True,
        "original_integer_audit_available": False,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output = Path(__file__).resolve().parent / "replay/integer-square-reconstruction.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"report": str(output), "lifts": result["lifts"]}, indent=2))


if __name__ == "__main__":
    main()
