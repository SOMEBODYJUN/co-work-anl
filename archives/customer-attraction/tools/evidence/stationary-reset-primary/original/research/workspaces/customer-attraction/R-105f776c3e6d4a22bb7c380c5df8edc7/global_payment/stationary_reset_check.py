#!/usr/bin/env python3
"""Exact test of the incidence-stationarity reward-exchange candidate.

Uses the pre-existing 36-client aggregate-theta SPE, reconstructed from unit
customer sets and its full history rule. No canonical implementation imports.
"""
from fractions import Fraction as F
from itertools import combinations, product
import json

K = 6
M = 3
clients = []
for x in range(3):
    for y in range(3, 6):
        clients.append(frozenset((x, y)))
for X in combinations(range(3), 2):
    for Y in combinations(range(3, 6), 2):
        clients.extend([frozenset(X + Y)] * 3)
assert len(clients) == 36

def action(h):
    if not h:
        return 0
    if len(h) == 1:
        return 3 if h[0] < 3 else 0
    group = range(3) if h[1] < 3 else range(3, 6)
    return min(a for a in group if a not in h)

def finish(h):
    z = tuple(h)
    while len(z) < M:
        z += (action(z),)
    return z

def payoff(z, i):
    a = z[i]
    return sum((F(1, sum(t in c for t in z)) for c in clients if a in c), F(0))

def welfare(z):
    return sum(any(t in c for t in z) for c in clients)

checks = 0
for d in range(M):
    for h in product(range(K), repeat=d):
        prescribed = payoff(finish(h), d)
        for a in range(K):
            assert prescribed >= payoff(finish(h + (a,)), d)
            checks += 1

p = (F(1, 4), F(1, 4), F(0), F(1, 4), F(1, 4), F(0))
leaves = [finish((a,)) for a in range(K)]
P = [[F(z.count(t), M) for t in range(K)] for z in leaves]
stationary = tuple(sum((p[a] * P[a][t] for a in range(K)), F(0)) for t in range(K))
assert stationary == p
D = sum((p[a] * payoff(leaves[a], 0) for a in range(K)), F(0))
U = sum((p[a] * F(welfare(leaves[a]), M) for a in range(K)), F(0))
assert D == 10 and U == F(34, 3) and D < U
for c in clients:
    incidence_root = sum((p[a] * (a in c) for a in range(K)), F(0))
    incidence_random_player = sum((p[a] * F(sum(t in c for t in leaves[a]), M)
                                    for a in range(K)), F(0))
    assert incidence_root == incidence_random_player

print(json.dumps({
    'full_ordered_histories': 1 + K + K*K,
    'IC_comparisons_including_self': checks,
    'p': list(map(str, p)),
    'stationarity': list(map(str, stationary)),
    'expected_root_payoff': str(D),
    'expected_uniform_terminal_player_payoff': str(U),
    'gap': str(U-D),
    'status': 'Stationarity preserves incidence marginals, not reward exchangeability; Q-CAG-HALF remains OPEN.'
}, indent=2))
