from fractions import Fraction as F
from itertools import combinations, permutations, product
from math import prod
import json


def transpose(a):
    return [list(c) for c in zip(*a)]


def multiply(a, b):
    bt = transpose(b)
    return [[sum((x * y for x, y in zip(row, col)), F(0)) for col in bt] for row in a]


def gram(f, diagonal):
    return multiply(transpose(f), [[d * x for x in row] for d, row in zip(diagonal, f)])


def determinant(a):
    n = len(a)
    value = F(0)
    for p in permutations(range(n)):
        inversions = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        value += (-1) ** inversions * prod(a[i][p[i]] for i in range(n))
    return value


def psd(a):
    n = len(a)
    for k in range(1, n + 1):
        for indexes in combinations(range(n), k):
            minor = [[a[i][j] for j in indexes] for i in indexes]
            if determinant(minor) < 0:
                return False
    return True


def main():
    full_rank = [
        [[F(1), F(0)], [F(0), F(1)]],
        [[F(1), F(2)], [F(3), F(5)]],
        [[F(1), F(0), F(1)], [F(0), F(1), F(2)]],
        [[F(1), F(2), F(3)], [F(4), F(5), F(7)]],
    ]
    cases = 0
    changes_of_basis = 0
    for f in full_rank:
        assert any(determinant([[row[j] for j in cols] for row in f]) != 0
                   for cols in combinations(range(len(f[0])), 2))
        for weights in [(F(1, 2), F(1, 2)), (F(1, 3), F(2, 3))]:
            for loads in product((F(0), F(1, 2), F(1), F(2)), repeat=2):
                for delta in [F(0), F(1, 2), F(1), F(3, 2)]:
                    diagonal = [(1 + delta - load) * w for load, w in zip(loads, weights)]
                    k = gram(f, diagonal)
                    atomwise = all(load <= 1 + delta for load in loads)
                    assert psd(k) == atomwise
                    cases += 1
                    r = len(f[0])
                    g = [[F(2 if i == 0 else 3 if i == j else 0) if i == j else F(0)
                          for j in range(r)] for i in range(r)]
                    # Add one nonzero off-diagonal entry; diagonal remains invertible.
                    g[0][-1] += 1
                    assert determinant(g) != 0
                    fp = multiply(f, g)
                    kp = gram(fp, diagonal)
                    assert kp == multiply(transpose(g), multiply(k, g))
                    assert psd(kp) == atomwise
                    changes_of_basis += 1

    low = [[F(1)], [F(1)]]
    assert gram(low, [F(1, 2), F(-1, 2)]) == [[F(0)]]
    assert psd(gram(low, [F(1, 2), F(-1, 2)]))
    identity = full_rank[0]
    k = gram(identity, [F(1, 2), F(-1, 2)])
    absolute = [[k[i][j] + (F(1, 2) if i == j else 0) for j in range(2)] for i in range(2)]
    assert psd(absolute)
    scale = [[F(1), F(0)], [F(0), F(2)]]
    kp = gram(multiply(identity, scale), [F(1, 2), F(-1, 2)])
    absolutep = [[kp[i][j] + (F(1, 2) if i == j else 0) for j in range(2)] for i in range(2)]
    assert not psd(absolutep)

    canonical_sharp = 0
    for n in range(5):
        for degrees in product(range(1, 5), repeat=n):
            nleaves = prod(degrees)
            for a in [F(0), F(1, 4 * nleaves), F(1, 2 * max(1, nleaves - 1))]:
                u = (1 - 2 * a * (nleaves - 1)) / nleaves
                v = (1 + 2 * a) / nleaves
                assert u >= 0
                assert u + (nleaves - 1) * v == 1
                cumulative = 1
                for d in degrees:
                    cumulative *= d
                    descendants = nleaves // cumulative
                    chosen = u + (descendants - 1) * v
                    independent = (1 + 2 * a) / cumulative - 2 * a
                    assert chosen == independent
                    if d > 1:
                        other = descendants * v
                        assert other - chosen == 2 * a
                canonical_sharp += 1
    print(json.dumps({
        "canonical_sha256": "a17bde448cd58ab9b637a6050837153006423cf8097b078621bcb302031ff02b",
        "full_row_rank_relative_gram_equivalences": cases,
        "invertible_basis_congruence_checks": changes_of_basis,
        "rank_omission_counterexample": True,
        "absolute_identity_basis_counterexample": True,
        "canonical_uniform_other_leaves_equals_independent_path_law": canonical_sharp,
        "status": "all exact finite audits passed"
    }, indent=2))


if __name__ == "__main__":
    main()
