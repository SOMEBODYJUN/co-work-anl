#!/usr/bin/env python3
"""Independent rational reconstruction of the statement-only token-lift point."""
from fractions import Fraction as F
from itertools import combinations
import json


def mm(a, b):
    return [[sum((x * y for x, y in zip(row, col)), F(0))
             for col in zip(*b)] for row in a]


def transpose(a):
    return [list(row) for row in zip(*a)]


def gram_psd_rank(a):
    """Exact symmetric Schur elimination, including zero-diagonal checks."""
    a = [row[:] for row in a]
    rank = 0
    while a:
        for i in range(len(a)):
            assert a[i][i] >= 0, ('negative diagonal', rank, i, a[i][i])
        piv = next((i for i in range(len(a)) if a[i][i] > 0), None)
        if piv is None:
            assert all(x == 0 for row in a for x in row), 'zero diagonal/offdiag obstruction'
            return rank
        if piv:
            a[0], a[piv] = a[piv], a[0]
            for row in a:
                row[0], row[piv] = row[piv], row[0]
        d = a[0][0]
        b = [[a[i][j] - a[i][0] * a[0][j] / d
              for j in range(1, len(a))] for i in range(1, len(a))]
        a = b
        rank += 1
    return rank


subsets = [sum(1 << i for i in s) for s in combinations(range(10), 4)]
nu = {s: F(1, 210) for s in subsets}
beta = {}
for s in subsets:
    first = (s & 31).bit_count()
    beta[s] = F(1, 8) if first in (0, 4) else F(-1, 400) if first == 2 else F(0)
assert sum(beta.values()) == 1
delta = F(1, 100)
Y = 1 << 10


def expectation(weights, mask):
    return sum((wt for s, wt in weights.items() if (s & mask) == mask), F(0))


def moment(mask):
    if mask & Y:
        return delta * expectation(beta, mask ^ Y)
    return expectation(nu, mask)


basis = [0] + [1 << i for i in range(11)]
basis += [(1 << i) | (1 << j) for i, j in combinations(range(11), 2)]
assert len(basis) == 67
gram = [[moment(s | t) for t in basis] for s in basis]
rank = gram_psd_rank(gram)
assert rank == 55

# Full sum X=4 moment checks against every Boolean monomial of degree <=3.
tests = [0]
for size in range(1, 4):
    tests.extend(sum(1 << i for i in s) for s in combinations(range(11), size))
for t in tests:
    assert sum((moment(t | (1 << i)) for i in range(10)), F(0)) == 4 * moment(t)

pairs = list(combinations(range(10), 2))
pm = [(1 << i) | (1 << j) for i, j in pairs]
A = [[expectation(nu, e | f) for f in pm] for e in pm]
R = [[F(int(i in e)) for e in pairs] for i in range(10)]
RtR = mm(transpose(R), R)
Ainv = [[14 * F(i == j) - F(4, 3) * RtR[i][j] + F(1, 4)
         for j in range(45)] for i in range(45)]
assert mm(Ainv, A) == [[F(i == j) for j in range(45)] for i in range(45)]
C = [[expectation(beta, e | (1 << i)) for i in range(10)] for e in pm]
D = [[expectation(beta, (1 << i) | (1 << j)) for j in range(10)] for i in range(10)]
E = mm(mm(transpose(C), Ainv), C)
assert mm(R, C) == [[3 * x for x in row] for row in D]
vecs = {'constant': [1] * 10, 'half_sign': [1] * 5 + [-1] * 5,
        'within_half': [1, -1] + [0] * 8}
expected_d = {'constant': F(8, 5), 'half_sign': F(2), 'within_half': F(1, 20)}
expected_e = {'constant': F(4932, 125), 'half_sign': F(15), 'within_half': F(453, 1000)}
eigenvalues = {}
for name, v in vecs.items():
    for mat, lam in ((D, expected_d[name]), (E, expected_e[name])):
        assert [sum((mat[i][j] * v[j] for j in range(10)), F(0))
                for i in range(10)] == [lam * vi for vi in v]
    schur = expected_d[name] - delta * expected_e[name]
    assert schur > 0
    eigenvalues[name] = {'D': str(expected_d[name]), 'E': str(expected_e[name]),
                         'D_minus_delta_E': str(schur)}

block = [[4 * F(i == j) * moment(Y | (1 << i))
          - moment(Y | (1 << i) | (1 << j)) for j in range(10)] for i in range(10)]
s = vecs['half_sign']
assert [sum((block[i][j] * s[j] for j in range(10)), F(0))
        for i in range(10)] == [F(-2, 5) * delta * si for si in s]
negative_block_norm = sum((s[i] * block[i][j] * s[j]
                           for i in range(10) for j in range(10)), F(0))
assert negative_block_norm == -4 * delta


def lifted_y_two(a, i, b, j):
    if a == b:
        return delta * expectation(beta, 1 << i) / 4 if i == j else F(0)
    if i == j:
        return F(0)
    return delta * expectation(beta, (1 << i) | (1 << j)) / 12


qterms = [(1 if a == 0 else -1, a, i, s[i]) for a in range(2) for i in range(10)]
qnorm = sum((ca * sa * cb * sb * lifted_y_two(a, i, b, j)
             for ca, a, i, sa in qterms for cb, b, j, sb in qterms), F(0))
assert qnorm == F(-1, 150)

print(json.dumps({'independent_exact_first': True, 'author_proof_or_code_read': False,
                  'signed_subsets': len(subsets), 'sum_beta': str(sum(beta.values())),
                  'aggregate_m2_dimension': len(basis), 'aggregate_m2_exact_psd_rank': rank,
                  'sum_X_eq_4_monomial_checks': len(tests),
                  'pure_X_pair_basis_dimension': 45, 'A_inverse_verified': True,
                  'Schur_eigenvalues': eigenvalues, 'Schur_multiplicities': [1, 1, 8],
                  'formal_lift_Q_square': str(qnorm),
                  'necessary_block_half_sign_eigenvalue': str(-2 * delta / 5),
                  'necessary_block_half_sign_quadratic': str(negative_block_norm)}, indent=2))
