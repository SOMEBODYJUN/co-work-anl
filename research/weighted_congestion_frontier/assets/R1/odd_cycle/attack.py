#!/usr/bin/env python3
"""Independent literal-cost attack of the odd ring, using exact Fractions.

Each count-state represents every labelled state with those group counts.
The default fixture is the m=3, degree-10 candidate supplied for attack.
"""
from fractions import Fraction as F
from itertools import product
from math import prod
import argparse
import json


def candidate():
    t = F(1, 6)
    return dict(
        u=(F(1), t**4, t**2),
        v=(t**5, t**3, t),
        n=(1944, 1, 1),
        k=(2, 10, 10),
        deg=(10, 10, 10),
        q=(F(1), F(1, 1250000), F(3, 50000000)),
        p=(F(9, 100), F(13), F(9, 10)),
    )


def normalized(g):
    m = len(g['u'])
    x = tuple(g['v'][i] / g['u'][i] for i in range(m))
    t = tuple(g['v'][i] / g['u'][(i+1) % m] for i in range(m))
    return x, t


def coefficients(g):
    m = len(g['u'])
    return (
        tuple(g['q'][i] / g['u'][i]**g['k'][i] for i in range(m)),
        tuple(g['p'][i] / g['u'][(i+1) % m]**g['deg'][i] for i in range(m)),
    )


def literal_light_costs(g, h, z, i, bit):
    """z[i] counts bit-0 lights. Deviating light is present after its move."""
    m = len(h)
    nxt = (i+1) % m
    a, b = coefficients(g)
    count = z[i] if bit == 0 else g['n'][i] - z[i]
    assert count > 0
    other_count = g['n'][i] - count
    current = (
        a[i] * (count*g['v'][i] + g['u'][i]*(bit == h[i]))**g['k'][i]
        + b[i] * (g['v'][i] + g['u'][nxt]*(1-bit == h[nxt]))**g['deg'][i]
    )
    deviation = (
        a[i] * ((other_count+1)*g['v'][i] + g['u'][i]*(1-bit == h[i]))**g['k'][i]
        + b[i] * (g['v'][i] + g['u'][nxt]*(bit == h[nxt]))**g['deg'][i]
    )
    return current, deviation


def literal_hub_costs(g, h, z, i):
    m = len(h)
    prev = (i-1) % m
    a, b = coefficients(g)
    same = z[i] if h[i] == 0 else g['n'][i] - z[i]
    # A previous light uses side bit (1 - its own bit).
    collision = z[prev] if h[i] == 1 else g['n'][prev] - z[prev]
    current = (
        a[i] * (g['u'][i] + same*g['v'][i])**g['k'][i]
        + b[prev] * (
            collision*(g['u'][i]+g['v'][prev])**g['deg'][prev]
            + (g['n'][prev]-collision)*g['u'][i]**g['deg'][prev]
        )
    )
    deviation = (
        a[i] * (g['u'][i] + (g['n'][i]-same)*g['v'][i])**g['k'][i]
        + b[prev] * (
            (g['n'][prev]-collision)*(g['u'][i]+g['v'][prev])**g['deg'][prev]
            + collision*g['u'][i]**g['deg'][prev]
        )
    )
    return current, deviation


def sufficient_certificate(g, alpha):
    m = len(g['u'])
    x, t = normalized(g)
    n, k, deg, q, p = (g[key] for key in ('n', 'k', 'deg', 'q', 'p'))
    N = tuple((1+x[i])**k[i] - alpha*(n[i]*x[i])**k[i] for i in range(m))
    M = tuple(alpha*(1+n[i]*x[i])**k[i] - 1 for i in range(m))
    P = tuple(alpha*(1+t[i])**deg[i] - t[i]**deg[i] for i in range(m))
    Q = tuple((1+t[i])**deg[i] - alpha for i in range(m))
    light = tuple(q[i]*N[i] - p[i]*P[i] for i in range(m))
    hub = tuple(n[(i-1) % m]*p[(i-1) % m]*Q[(i-1) % m] - q[i]*M[i] for i in range(m))
    R = tuple(n[i]*N[i]*Q[i] / (P[i]*M[(i+1) % m]) for i in range(m))
    return dict(
        alpha=alpha,
        weight_cycle=prod(x) == prod(t),
        N=N, M=M, P=P, Q=Q,
        light_slack=light, hub_slack=hub,
        coefficient_cycle=prod(R),
        certified=(m % 2 == 1 and all(z > 0 for z in light+hub)),
    )


def enumerate_count_states(g, alpha):
    """Exact full-state check, including every individual type of deviation.

    Positive latency and own positive weight make every deviation cost positive.
    Group symmetry is exact: no state is sampled or discarded.
    """
    m = len(g['u'])
    # Cache literal costs only by variables on which a player's costs depend.
    L = {}
    H = {}
    for i in range(m):
        prev, nxt = (i-1) % m, (i+1) % m
        for hi, hn, zi, bit in product((0, 1), (0, 1), range(g['n'][i]+1), (0, 1)):
            if (zi if bit == 0 else g['n'][i]-zi) == 0:
                continue
            h, z = [0]*m, [0]*m
            h[i], h[nxt], z[i] = hi, hn, zi
            c, d = literal_light_costs(g, h, z, i, bit)
            L[i, hi, hn, zi, bit] = c / d
        for hi, zi, zp in product((0, 1), range(g['n'][i]+1), range(g['n'][prev]+1)):
            h, z = [0]*m, [0]*m
            h[i], z[i], z[prev] = hi, zi, zp
            c, d = literal_hub_costs(g, h, z, i)
            H[i, hi, zi, zp] = c / d
    best = None
    argmin = None
    states = 0
    approximate_equilibria = []
    certificate_witnesses = {'light': 0, 'hub': 0}
    for h in product((0, 1), repeat=m):
        for z in product(*(range(n+1) for n in g['n'])):
            states += 1
            moves = [(H[i, h[i], z[i], z[(i-1) % m]], 'H', i, h[i]) for i in range(m)]
            for i in range(m):
                for bit in (0, 1):
                    key = (i, h[i], h[(i+1) % m], z[i], bit)
                    if key in L:
                        moves.append((L[key], 'L', i, bit))
            maximum = max(moves, key=lambda y: y[0])
            if best is None or maximum[0] < best:
                best, argmin = maximum[0], (h, z, maximum)
            if maximum[0] <= alpha:
                approximate_equilibria.append((h, z))
            # Verify the proposed all-state proof's witness, independently.
            light_witness = next((i for i in range(m)
                                  if (z[i] if h[i] == 0 else g['n'][i]-z[i]) > 0), None)
            if light_witness is not None:
                i = light_witness
                assert L[i, h[i], h[(i+1) % m], z[i], h[i]] > alpha
                certificate_witnesses['light'] += 1
            else:
                hub_witness = next(i for i in range(m) if h[i] == h[(i-1) % m])
                assert H[hub_witness, h[hub_witness], z[hub_witness], z[(hub_witness-1) % m]] > alpha
                certificate_witnesses['hub'] += 1
    return dict(count_states=states, represented_labelled_states='2^'+str(m+sum(g['n'])),
                alpha_pne_count=len(approximate_equilibria),
                alpha_pne=approximate_equilibria,
                exact_best_factor=best, exact_best_factor_decimal=float(best),
                minimizing_count_state=argmin, certificate_witnesses=certificate_witnesses)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--enumerate', action='store_true', help='exhaust all 62240 count states')
    args = parser.parse_args()
    g = candidate()
    result = dict(game=g, coefficients=coefficients(g), certificate=sufficient_certificate(g, F(2)))
    if args.enumerate:
        result['exhaustive'] = enumerate_count_states(g, F(2))
    print(json.dumps(result, indent=2, default=lambda y: str(y)))


if __name__ == '__main__':
    main()
