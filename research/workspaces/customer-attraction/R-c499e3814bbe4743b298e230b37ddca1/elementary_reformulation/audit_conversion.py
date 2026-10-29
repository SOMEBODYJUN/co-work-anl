"""Definition-level audits for the pure-mathematics handoff.

Fixed fixtures test the conversion, not the CAG half conjecture. Fractions
are exact. No LP, random search or package-specific SPE solver is used.
"""
from fractions import Fraction as F
from itertools import product
import json


def submasks(mask):
    q = mask
    while True:
        yield q
        if not q:
            return
        q = (q - 1) & mask


def coverage(mu, mask):
    return sum((v for b, v in mu.items() if b & mask), F(0))


def harmonic(k):
    return sum((F(1, j) for j in range(1, k + 1)), F(0))


def potential(mu, q):
    return sum((v * harmonic(sum(q[a] for a in range(len(q)) if b >> a & 1))
                for b, v in mu.items()), F(0))


def direct_pay(mu, leaf, a):
    # Explicit unit-customer clones, independent of the potential formula.
    clients = [b for b, v in mu.items() for _ in range(int(v))]
    return sum((F(1, sum(bool(b >> c & 1) for c in leaf))
                for b in clients if b >> a & 1), F(0))


def leaf_from(h, policy, n):
    while len(h) < n:
        h = h + (policy(h),)
    return h


def q_of(leaf, p):
    return tuple(leaf.count(a) for a in range(p))


def atom_pay(b, q, a):
    return F(1, sum(q[c] for c in range(len(q)) if b >> c & 1)) if b >> a & 1 else F(0)


def check_tree(mu, p, n, policy):
    gains = []
    for t in range(n):
        for h in product(range(p), repeat=t):
            a = policy(h)
            leaf = leaf_from(h, policy, n)
            q = q_of(leaf, p)
            q_minus = tuple(q[c] - int(c == a) for c in range(p))
            actual = direct_pay(mu, leaf, a)
            assert actual == potential(mu, q) - potential(mu, q_minus)
            assert actual == sum((v * atom_pay(b, q, a) for b, v in mu.items()), F(0))
            for alt in range(p):
                other_leaf = leaf_from(h + (alt,), policy, n)
                other_q = q_of(other_leaf, p)
                matrix_gain = sum((v * (atom_pay(b, q, a) - atom_pay(b, other_q, alt))
                                   for b, v in mu.items()), F(0))
                gain = actual - direct_pay(mu, other_leaf, alt)
                assert matrix_gain == gain
                gains.append(gain)
    root = leaf_from((), policy, n)
    actual_mask = sum(1 << a for a in set(root))
    W = coverage(mu, actual_mask)
    opt = max(coverage(mu, j) for j in range(1, 1 << p) if j.bit_count() <= n)
    for j in range(1, 1 << p):
        if j.bit_count() <= n:
            d_dot_mu = sum((v * (2 * bool(b & actual_mask) - bool(b & j))
                           for b, v in mu.items()), F(0))
            assert d_dot_mu == 2 * W - coverage(mu, j)
    return gains, W, opt


def invert_coverage(f, p):
    full = (1 << p) - 1
    return {b: sum(((-1) ** (b.bit_count() - d.bit_count())
                    * (f[full] - f[full ^ d]) for d in submasks(b)), F(0))
            for b in range(1, full + 1)}


def main():
    all_a = lambda h: 0
    fresh = lambda h: 0 if not h else 1 - h[0]
    g1, w1, o1 = check_tree({1: 2, 2: 1}, 2, 2, all_a)
    g2, w2, o2 = check_tree({1: 1, 2: 1}, 2, 2, all_a)
    gf, wf, of = check_tree({1: 1, 2: 1}, 2, 2, fresh)
    assert min(g1) >= 0 and min(g2) < 0 and min(gf) >= 0
    assert (w1, o1, wf, of) == (2, 3, 2, 2)

    # A complete history-dependent policy with duplicate coverage labels.
    # On (0,1) and (1,0), which have equal counts, its actions differ.
    policy = lambda h: (len(h) + sum((i + 1) * a for i, a in enumerate(h))) % 2
    assert policy((0, 1)) != policy((1, 0))
    tested_gains = 0
    for n in (3, 6):
        mu = {3: n, 4: 1, 7: 2}
        no_core = {3: n, 4: 1}
        gains, W, opt = check_tree(mu, 3, n, policy)
        reduced, W0, opt0 = check_tree(no_core, 3, n, policy)
        assert gains == reduced and min(gains) >= 0
        assert W - W0 == opt - opt0 == 2
        assert 2 * W0 - opt0 == 2 * W - opt - 2
        tested_gains += len(gains)
        f = {a: coverage(mu, a) for a in range(8)}
        recovered = invert_coverage(f, 3)
        assert all(recovered[b] == mu.get(b, 0) for b in recovered)

        # The class-lift representative follows the prescribed original
        # label for its class; it is not a globally fixed representative.
        quotient = {}
        lifts = {(): ()}
        for t in range(n):
            for H in product(range(2), repeat=t):
                h = lifts[H]
                chosen = policy(h)
                quotient[H] = 0
                lifts[H + (0,)] = h + (chosen,)
                lifts[H + (1,)] = h + (2,)
        qg, qW, qopt = check_tree({1: n, 2: 1, 3: 2}, 2, n,
                                 lambda h: quotient[h])
        assert min(qg) >= 0 and (qW, qopt) == (W, opt)
        for H, h in lifts.items():
            assert tuple(0 if a in (0, 1) else 1 for a in h) == H

    # The rank-two uniform matroid function is monotone submodular but
    # its unique coverage atom at {1,2,3} is negative.
    f = {a: F(min(a.bit_count(), 2)) for a in range(8)}
    for a, b in product(range(8), repeat=2):
        assert f[a] + f[b] >= f[a | b] + f[a & b]
        if a & b == a:
            assert f[a] <= f[b]
    recovered = invert_coverage(f, 3)
    assert recovered[7] == -1
    assert all(recovered[b] == (0 if b.bit_count() == 1 else 1)
               for b in range(1, 7))

    print(json.dumps({
        "status": "passed",
        "purpose": "exact conversion and boundary auditing, not half search",
        "matrix_vs_unit_client_history_comparisons": tested_gains,
        "history_dependent_equal_count_actions_preserved": True,
        "dynamic_quotient_and_all_history_IC": "passed",
        "all_catalog_core_deletion": "passed",
        "submodular_noncoverage_full_atom": str(recovered[7]),
        "same_nerve_fixture_efficiency": ["3/2", "1"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
