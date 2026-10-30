#!/usr/bin/env python3
"""Exact literal-state and reduction checks; no numerical proof inference."""
from fractions import Fraction as Q
from itertools import product
from math import comb
from pathlib import Path
import json
import random

SEED = 20261014


def value(poly, x):
    ans = Q(0)
    for c in reversed(poly):
        ans = ans * x + c
    return ans


def shift(poly, h):
    return [sum((poly[j] * comb(j, k) * h ** (j-k)
                 for j in range(k, len(poly))), Q(0))
            for k in range(len(poly))]


def scale(poly, w):
    return [c * w ** j for j, c in enumerate(poly)]


def tests(n, w, F, G, alpha):
    return (value(F, 1) + n*value(G, 1+w)
            - alpha*(value(F, 1+n*w) + n*value(G, 1)),
            value(F, 1+w) + value(G, w)
            - alpha*(value(F, n*w) + value(G, 1+w)))


def membership(n, state, player):
    if player == 0:
        return {(state[0], j) for j in range(n+1)}
    return {(state[player], 0), (1-state[player], player)}


def literal_costs(n, w, F, G, state):
    actions = [membership(n, state, i) for i in range(n+1)]
    loads = {(c, j): sum((Q(1) if i == 0 else w
                         for i in range(n+1) if (c, j) in actions[i]), Q(0))
             for c in (0, 1) for j in range(n+1)}
    return [sum((value(F if j == 0 else G, loads[c, j])
                 for c, j in actions[i]), Q(0)) for i in range(n+1)]


def margins(n, w, F, G, m, alpha):
    u, v, z = value(G, 1), value(G, 1+w), value(G, w)
    h = lambda j: value(F, 1+j*w)+(n-j)*v+j*u
    out = [h(m)-alpha*h(n-m)]
    if m:
        out.append(value(F, 1+m*w)+z-alpha*(value(F, (n-m+1)*w)+v))
    if m < n:
        out.append(value(F, (n-m)*w)+v-alpha*(value(F, 1+(m+1)*w)+z))
    return out


def monomial_reduce(n, w, F, G, alpha, d):
    assert all(x > 0 for x in tests(n, w, F, G, alpha))
    swapped = w > 1
    if swapped:
        assert n == 1
        F, G, w = scale(G, w), scale(F, w), 1/w
        assert all(x > 0 for x in tests(n, w, F, G, alpha))
    assert 0 < w <= 1
    E = (1+w)**d
    u, v, z = value(G, 1), value(G, 1+w), value(G, w)
    assert v > 0
    lam = (u/v-1/E)/(1-1/E)
    assert 0 <= lam <= 1
    constant, beta = v*lam, v*(1-lam)/E
    endpoint = [constant]+[Q(0)]*(d-1)+[beta]
    assert value(endpoint, 1) == u
    assert value(endpoint, 1+w) == v
    assert value(endpoint, w) >= z
    pure = [Q(0)]*d+[beta]
    assert beta > 0 and all(x > 0 for x in tests(n, w, F, pure, alpha))
    good = []
    for k in range(len(F)):
        t, p, r = (1+n*w)**k, (1+w)**k, (n*w)**k
        score = n*(E-alpha)*(p-alpha*r)-(alpha*E-w**d)*(alpha*t-1)
        if F[k] and score > 0:
            good.append(k)
    assert good and min(good) >= 1
    k = min(good)
    low = (alpha*(1+n*w)**k-1)/(n*(E-alpha))
    high = ((1+w)**k-alpha*(n*w)**k)/(alpha*E-w**d)
    assert 0 < low < high < 1
    beta_out = (low+high)/2
    ff, gg = [Q(0)]*k+[Q(1)], [Q(0)]*d+[beta_out]
    assert all(x > 0 for x in tests(n, w, ff, gg, alpha))
    return swapped


def run():
    rng = random.Random(SEED)
    cases = []
    for n in range(1, 7):
        for w in map(Q, ('1/8', '1/2', '1', '2', '4')):
            for _ in range(3):
                d = rng.randrange(1, 9)
                F = [Q(rng.choice((0, 0, 1, 2)), rng.choice((1, 2, 4)))
                     for _ in range(d+1)]
                G = [Q(rng.choice((0, 0, 1, 2)), rng.choice((1, 2, 4)))
                     for _ in range(d+1)]
                cases.append((n, w, F, G, d))
    for n in range(1, 5):
        for w in (Q(1, 2), Q(1), Q(2)):
            for F, G in (([Q(0)], [Q(0)]), ([Q(0)], [Q(1)]),
                         ([Q(0)], [Q(0), Q(1)]), ([Q(0), Q(1)], [Q(0)])):
                cases.append((n, w, F, G, 1))
    # Explicit high-factor family, plus translated and mixed polynomial tests.
    w, d = Q(1, 32), 128
    G = [Q(0)]*d+[Q(1, 2)/(1+w)**d]
    for n in (4, 5, 6):
        for F in ([Q(0), Q(0), Q(1)], shift([Q(0), Q(0), Q(1)], Q(1, 64))):
            cases.append((n, w, F, G, d))
    stats = dict(seed=SEED, cases=len(cases), literal_states=0,
                 literal_deviations=0, orbit_alpha_checks=0,
                 high_factor_reductions=0, translated_nonzero=0,
                 direct_polynomial_reductions=0, exchanged_players=0)
    alphas = (Q(1), Q(11, 8), Q(3, 2), Q(2), Q(5, 2))
    for n, w, F, G, d in cases:
        for state in product((0, 1), repeat=n+1):
            costs = literal_costs(n, w, F, G, state)
            m = sum(state[i] == state[0] for i in range(1, n+1))
            for alpha in alphas:
                expected = margins(n, w, F, G, m, alpha)
                for i in range(n+1):
                    target = list(state)
                    target[i] = 1-target[i]
                    after = literal_costs(n, w, F, G, target)[i]
                    index = 0 if i == 0 else (1 if state[i] == state[0] else len(expected)-1)
                    assert costs[i]-alpha*after == expected[index]
            stats['literal_states'] += 1
            stats['literal_deviations'] += n+1
        for alpha in alphas:
            stats['orbit_alpha_checks'] += 1
            u, v, z = value(G, 1), value(G, 1+w), value(G, w)
            I = [m for m in range(n+1)
                 if (m == 0 or value(F, 1+m*w)+z <= alpha*(value(F, (n-m+1)*w)+v))
                 and (m == n or value(F, (n-m)*w)+v <= alpha*(value(F, 1+(m+1)*w)+z))]
            assert I and I == list(range(min(I), max(I)+1))
            no_pne = all(max(margins(n, w, F, G, m, alpha)) > 0 for m in range(n+1))
            if no_pne:
                assert not set(I).intersection(n-m for m in I)
            # alpha >= rho is certified without an irrational comparison.
            if no_pne and 2*alpha*(alpha-1) >= 1:
                b = max(I)
                if 2*b < n:
                    Fprime, nprime = shift(F, b*w), n-2*b
                    wprime, Gprime = w, G
                else:
                    a = min(I)
                    assert 2*a > n and 2*a-n == 1
                    r = n-a
                    Fprime, nprime = scale(shift(F, r*w), w), 1
                    wprime, Gprime = 1/w, scale(G, w)
                assert all(x > 0 for x in tests(nprime, wprime, Fprime, Gprime, alpha))
                monomial_reduce(nprime, wprime, Fprime, Gprime, alpha, d)
                stats['high_factor_reductions'] += 1
                stats['translated_nonzero'] += b > 0
            # Check translation identities at every legal endpoint, including
            # nonzero shifts that the finite no-PNE samples need not attain.
            h = lambda j: value(F, 1+j*w)+(n-j)*v+j*u
            for b in range((n-1)//2+1):
                np, fp = n-2*b, shift(F, b*w)
                hm, lm = tests(np, w, fp, G, alpha)
                assert hm == h(b)-alpha*h(n-b)+(alpha-1)*b*(u+v)
                assert lm == margins(n, w, F, G, b+1, alpha)[1]
            for a in range(n//2+1, n+1):
                r, np = n-a, 2*a-n
                fp = shift(F, r*w)
                A, B, C = value(fp, 1), value(fp, 1+np*w), value(fp, w)
                assert B+np*u-alpha*(A+np*v) == h(a)-alpha*h(n-a)+(alpha-1)*r*(u+v)
                assert C+v-alpha*(B+z) == margins(n, w, F, G, a-1, alpha)[-1]
                if np == 1:
                    hm, lm = tests(1, 1/w, scale(fp, w), scale(G, w), alpha)
                    assert hm == C+v-alpha*(B+z)
                    assert lm == B+u-alpha*(A+v)
    # The player-exchange branch is tested with explicit legal polynomial tests.
    for F, G, w, alpha in (([Q(0), Q(1)], [Q(0), Q(0), Q(1, 2)], Q(1, 5), Q(101, 100)),):
        # Only invoke the certificate interface when strict; otherwise retain its
        # exact failed boundary rather than inventing a successful witness.
        if all(x > 0 for x in tests(3, w, F, G, alpha)):
            stats['direct_polynomial_reductions'] += 1
            monomial_reduce(3, w, F, G, alpha, 2)
    # Deterministic direct test search includes every positive-degree mixture.
    for n in (1, 2, 4):
        for w in (Q(1, 8), Q(1, 4), Q(1, 2)):
            for k in (1, 2):
                for q in (Q(1, 4), Q(1, 2), Q(1)):
                    d = 32
                    F = [Q(0)]*k+[Q(1)]
                    G = [Q(1, 1000)]+[Q(0)]*(d-1)+[q/(1+w)**d]
                    alpha = Q(101, 100)
                    if all(x > 0 for x in tests(n, w, F, G, alpha)):
                        monomial_reduce(n, w, F, G, alpha, d)
                        stats['direct_polynomial_reductions'] += 1
                        if n == 1:
                            swapped = monomial_reduce(1, 1/w, scale(G, w), scale(F, w), alpha, d)
                            assert swapped
                            stats['exchanged_players'] += 1
    Path(__file__).with_name('results.json').write_text(json.dumps(stats, indent=2)+'\n')
    print(json.dumps(stats, sort_keys=True))


if __name__ == '__main__':
    run()
