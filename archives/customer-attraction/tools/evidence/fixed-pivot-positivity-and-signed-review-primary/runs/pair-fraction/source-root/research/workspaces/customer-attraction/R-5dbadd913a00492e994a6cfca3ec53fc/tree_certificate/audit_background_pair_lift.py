"""Definition-level Fraction audit; finite regression is not the general proof.

No equilibrium solver, search generator, or external numerical package is used.
Every count vector here includes a common arbitrary background, possibly with
positive counts on the active a,b,c labels themselves.
"""
from fractions import Fraction as Q
from itertools import product
import json


def resource_u(active, counts, membership):
    if not membership[active]:
        return Q(0)
    load = sum(n * membership[c] for c, n in enumerate(counts))
    assert counts[active] > 0 and load > 0
    return Q(1, load)


def add_active(z, a, r, b, s):
    q = list(z)
    q[a] += r
    q[b] += s
    return tuple(q)


def background_pay(z, q, membership):
    # Only evaluate U_c when z_c>0, which implies q_c>0.
    return sum((n * resource_u(c, q, membership)
                for c, n in enumerate(z) if n), Q(0))


def error(z, a, b, r, s, membership):
    q = add_active(z, a, r, b, s)
    qp = add_active(z, a, s, b, r)
    return (r*s*resource_u(a, q, membership)
            + r*(r-s)*resource_u(b, qp, membership)
            - s*s*resource_u(a, qp, membership)
            - (r-s)*membership[b])


def audit():
    # Direct four-cell formulas across many independent integer parameters.
    four_cell_checks = 0
    for r in range(1, 16):
        for s in range(1, r+1):
            for d in range(31):
                for alpha, beta in product((0, 1), repeat=2):
                    z = (0, 0, d)
                    membership = (alpha, beta, 1)
                    e = error(z, 0, 1, r, s, membership)
                    h = r-s
                    if not alpha and not beta:
                        expected = Q(0)
                    elif alpha and not beta:
                        expected = Q(s*h*d, (d+r)*(d+s))
                    elif not alpha and beta:
                        expected = -Q(h*d, d+r)
                    else:
                        expected = -Q(h*d, d+r+s)
                    assert e == expected
                    q = add_active(z, 0, r, 1, s)
                    qp = add_active(z, 0, s, 1, r)
                    bq = background_pay(z, q, membership)
                    bqp = background_pay(z, qp, membership)
                    rent = Q(d, d+r+s*alpha) if beta else Q(0)
                    residue = Q(s*h*d, (d+r)*(d+s)) if alpha and not beta else Q(0)
                    assert e+h*rent == residue >= 0
                    assert e+h*bq >= 0 and e+h*bqp >= 0
                    four_cell_checks += 1

    # Explicit arbitrary-label backgrounds include positive z_a,z_b,z_c.
    difference_checks = 0
    flow_checks = 0
    for z in product(range(3), repeat=4):
        for membership in product((0, 1), repeat=4):
            d = sum(zc*mc for zc, mc in zip(z, membership))
            for r, s in ((1, 1), (2, 1), (3, 1), (3, 2), (5, 2)):
                b = 3
                es = [error(z, a, b, r, s, membership) for a in range(3)]
                k = Q(s*(r-s)*d, (d+r)*(d+s+r*membership[b]))
                for a, c in product(range(3), repeat=2):
                    assert es[a]-es[c] == k*(membership[a]-membership[c])
                    difference_checks += 1
                # Arbitrarily repeated directed cycle. Length does not matter.
                cycle = ((0, 1, 7), (1, 2, 7), (2, 0, 7))
                assert sum((w*(es[a]-es[c]) for a,c,w in cycle), Q(0)) == 0
                flow_checks += 1

    kernel_checks = 0
    for d in range(1001):
        k0 = Q(d, (d+2)*(d+1))
        k1 = Q(d, (d+2)*(d+3))
        assert 0 <= k0 <= Q(1, 6) and 0 <= k1 <= Q(1, 10)
        kernel_checks += 2
    return {
        'exact': True,
        'four_cell_and_rent_checks': four_cell_checks,
        'shared_pivot_difference_checks': difference_checks,
        'balanced_flow_checks': flow_checks,
        'kernel_bound_checks': kernel_checks,
        'scope': 'Finite implementation regression for general lemmas L1-L2; no SPE or half theorem is asserted.'
    }


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2))
