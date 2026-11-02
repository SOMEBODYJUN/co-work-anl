"""Root's independent sparse-row audit of the two-pivot repair.

No discovery code, author checker, JSON witness, scipy or canonical game solver
is imported. All graph continuations and payoff rows are reconstructed here.
"""
from fractions import Fraction as F
from itertools import product
import json


def add(*parts):
    out = {}
    for scale, row in parts:
        for v, x in row.items():
            out[v] = out.get(v, F(0)) + scale * x
    return {v: x for v, x in out.items() if x}


def vertex(path, topic):
    q = tuple(path.count(a) for a in range(6))
    assert q[topic] > 0
    return {(q, topic): F(1)}


def action(h):
    if not h:
        return 0
    if len(h) == 1:
        return 3 if h[0] < 3 else 0
    group = range(3) if h[1] < 3 else range(3, 6)
    return next(a for a in group if a not in h)


def terminal(h):
    while len(h) < 3:
        h += (action(h),)
    return h


def payoff(v, mask):
    q, a = v
    return (F(1, sum(q[b] for b in range(6) if mask >> b & 1))
            if mask >> a & 1 else F(0))


def circuit(a, b):
    return add((2, vertex((a, a, b), a)),
               (2, vertex((a, b, b), b)),
               (-1, vertex((a, b, b), a)),
               (-3, vertex((b, b, b), b)))


def main():
    # The four membership cases prove the arbitrary-r,s identity directly.
    general_checks = 0
    for r in range(1, 33):
        for s in range(1, r + 1):
            for ina, inb in product((0, 1), repeat=2):
                def u(a_count, b_count, player):
                    included = ina if player == 0 else inb
                    return F(included, a_count * ina + b_count * inb) if included else F(0)
                lhs = r*s*u(r, s, 0) + r*(r-s)*u(s, r, 1)
                rhs = s*s*u(s, r, 0) + (r-s)*inb
                assert lhs == rhs
                general_checks += 1

    incentives = []
    for h, b in (((2, 4), 1), ((4, 2), 3), ((4, 4), 2)):
        incentives.append(add((1, vertex(terminal(h), action(h))),
                              (-1, vertex(terminal(h + (b,)), b))))

    specifications = (
        ((0, 2, 4), (0, 3, 4), 0, 2, 1),
        ((1, 2, 4), (2, 2, 4), 2, 2, 1),
        ((1, 2, 4), (2, 4, 4), 4, 2, 1),
        ((3, 3, 4), (0, 3, 4), 3, 1, 2),
        ((3, 4, 4), (0, 3, 4), 4, 1, 2),
    )
    dilutions = []
    dilution_checks = 0
    for source, target, a, factor, mult in specifications:
        row = add((factor, vertex(target, a)), (-1, vertex(source, a)))
        ratios = []
        for mask in range(1, 64):
            assert sum(x * payoff(v, mask) for v, x in row.items()) >= 0
            if mask >> a & 1:
                ratios.append(payoff(next(iter(vertex(source, a))), mask) /
                              payoff(next(iter(vertex(target, a))), mask))
            dilution_checks += 1
        assert max(ratios) == factor
        dilutions.append((mult, row))

    root = terminal(())
    assert root == (0, 3, 4)
    target = add(*[(2, vertex(root, a)) for a in root],
                 *[(-1, vertex((1, 2, 4), a)) for a in (1, 2, 4)])
    rhs = add(*[(1, row) for row in incentives], *dilutions,
              (-1, circuit(2, 4)), (1, circuit(3, 4)))
    assert target == rhs
    all_vertices = {(tuple(h.count(a) for a in range(6)), b)
                    for h in product(range(6), repeat=3) for b in set(h)}
    assert len(all_vertices) == 126
    for mask in range(1, 64):
        for pair in ((2, 4), (3, 4)):
            assert sum(x * payoff(v, mask) for v, x in circuit(*pair).items()) == 0
    report = {
        'status': 'independent root reconstruction passed',
        'arbitrary_r_s_identity_proof': 'four membership cases in companion review',
        'finite_r_s_regression_checks': general_checks,
        'genuine_ordered_incentive_rows': len(incentives),
        'sharp_dilution_type_checks': dilution_checks,
        'sparse_vector_identity_over_vertices': len(all_vertices),
        'target': '2C_034-C_124',
        'scope': 'specified strategy and comparison only; general half remains OPEN',
    }
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
