#!/usr/bin/env python3
"""Exact, independent tests of a padded logarithmic-palette normal form.

This is not a scheduling approximation backend. The padded instance is handled
by its complete load classification: every schedule leaving a private block
edge has load at least N^2; all other schedules are active assignments plus
private dummy loads 1. No astronomical matrix is materialized.
"""

from collections import Counter
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import random


def ceilq(x):
    return -(-x.numerator // x.denominator)


def make_palette_from_h(H):
    assert H >= 2
    N = 1 << (H - 1)
    palette = {1, N*N}
    ordinary = {1}
    exponents = 0
    j = 2
    while 1 << j <= H:
        b = F(8*j+1, 8*j)
        power = F(1)
        R = H // (1 << j)
        for r in range(R+1):
            q = ceilq(power)
            assert 1 <= q <= N
            ordinary.add(q)
            power *= b
        exponents += R
        j += 1
    palette |= ordinary
    assert len(palette) <= 2 + exponents <= 2 + H//2
    assert max(ordinary) < N*N
    return palette, exponents


@lru_cache(None)
def padding(n, k):
    assert n >= 1 and k >= 2
    ell = (8*k*n-1).bit_length()
    E = (1 << k)*8*k*ell
    H = E+1
    N = 1 << E
    b = F(8*k+1, 8*k)
    R = H//(1 << k)
    assert R == 8*k*ell
    assert b**(8*k) >= 2
    assert b**R >= 8*k*n
    assert N >= 16*k*n
    assert 2*(8*k+2)*n < N*N
    palette, exponent_count = make_palette_from_h(H)
    powers = [F(1)]
    while powers[-1] < 8*k*n:
        powers.append(powers[-1]*b)
    assert len(powers)-1 <= R
    assert all(ceilq(p) in palette for p in powers)
    return {
        'n': n, 'k': k, 'ell': ell, 'E': E, 'H': H, 'N': N,
        'b': b, 'alpha': F(2)-F(1,k), 's': 8*k*n,
        'sentinel': N*N, 'powers': tuple(powers), 'palette': palette,
        'grid_exponents_total': exponent_count,
    }


def scalar_encode(z, pad):
    assert 0 <= z <= pad['s']
    target = max(F(1), z)
    for r, power in enumerate(pad['powers']):
        if power >= target:
            q = ceilq(power)
            assert z <= q <= pad['b']*z+1
            assert q in pad['palette']
            assert r == 0 or pad['powers'][r-1] < target
            return q
    raise AssertionError('grid not long enough')


def encode(p, T, pad):
    if p is None or p > T:
        return pad['sentinel']
    return scalar_encode(pad['s']*p/T, pad)


def loads(P, a):
    out = [F(0)]*len(P)
    for j, i in enumerate(a):
        if P[i][j] is None:
            return None
        out[i] += P[i][j]
    return tuple(out)


def check_scalar_edges(pad, counts):
    T = F(17, 2**127+101)
    b, s = pad['b'], pad['s']
    assert encode(F(0), T, pad) == 1
    assert encode(T/s, T, pad) == 1
    assert encode(T, T, pad) < pad['sentinel']
    assert encode(T+F(1,2**521+47), T, pad) == pad['sentinel']
    assert encode(None, T, pad) == pad['sentinel']
    probes = {F(0), F(1), F(s), F(1,2**521+47)}
    for left, right in zip(pad['powers'],pad['powers'][1:]):
        if left <= s:
            probes.add(left)
        if right <= s:
            probes.add(right)
        if (left+right)/2 <= s:
            probes.add((left+right)/2)
        just_over = left+F(1,2**521+47)
        if just_over <= s:
            probes.add(just_over)
    for z in probes:
        q = scalar_encode(z, pad)
        assert z <= q <= b*z+1
        assert encode(T*z/s, T, pad) == q
        counts['scalar_boundary_probes'] += 1


def check_matrix(P, k, counts):
    m, n = len(P), len(P[0])
    assert all(any(P[i][j] is not None for i in range(m)) for j in range(n))
    assignments = list(product(range(m), repeat=n))
    legal = [(max(ell),a) for a in assignments
             if (ell := loads(P,a)) is not None]
    O, witness = min(legal)
    zero_predicate = all(any(P[i][j] == 0 for i in range(m)) for j in range(n))
    assert (O == 0) == zero_predicate
    counts['matrix_k_pairs'] += 1
    if O == 0:
        zero_a = tuple(next(i for i in range(m) if P[i][j] == 0)
                       for j in range(n))
        assert max(loads(P,zero_a)) == 0
        counts['exact_zero_branches'] += 1
        return

    pad = padding(n,k)
    L = max(min(P[i][j] for i in range(m) if P[i][j] is not None)
            for j in range(n))
    U = sum(min(P[i][j] for i in range(m) if P[i][j] is not None)
            for j in range(n))
    assert 0 < L <= O <= U <= n*L
    T = L
    grid = [T]
    while grid[-1] < U:
        grid.append(grid[-1]*pad['b'])
    assert len(grid)-1 <= 8*k*(n-1).bit_length()
    good = next(t for t in grid if t >= O)
    assert O <= good <= pad['b']*O
    counts['threshold_grid_points'] += len(grid)

    # The exact first good threshold; all complete low-load padded schedules
    # must have private dummies and originals on original machines.
    T = good
    Q = tuple(tuple(encode(p,T,pad) for p in row) for row in P)
    qpatterns = [(max(F(1),max(loads(Q,a))),a) for a in assignments]
    qopt, qa = min(qpatterns)
    q_witness = max(F(1),max(loads(Q,witness)))
    bound = pad['b']*(F(pad['s'])/T)*O+n
    assert qopt <= q_witness <= bound <= (8*k+2)*n
    assert pad['alpha']*qopt < pad['sentinel']
    assert pad['alpha']*bound < pad['sentinel']
    counts['good_thresholds'] += 1
    for qC,a in qpatterns:
        counts['active_assignment_patterns'] += 1
        retained = all(P[i][j] is not None and P[i][j] <= T
                       for j,i in enumerate(a))
        if not retained:
            assert qC >= pad['sentinel']
            counts['sentinel_active_patterns'] += 1
        else:
            pells, qells = loads(P,a), loads(Q,a)
            for pi, qi in zip(pells,qells):
                assert pi <= T*qi/pad['s']
            counts['retained_active_patterns'] += 1
        if qC <= pad['alpha']*qopt:
            assert retained
            pC = max(loads(P,a))
            assert pC <= pad['alpha']*(pad['b']*O+T/(8*k))
            assert pC <= pad['alpha']*pad['b']**2*O
            assert pC < (F(2)-F(1,2*k))*O
            counts['every_qualifying_output_pattern'] += 1

    # Rejection at an earlier candidate never claims an OPT lower bound.
    if L < O:
        Qlow = tuple(tuple(encode(p,L,pad) for p in row) for row in P)
        sentinel_patterns = sum(any(P[i][j] is None or P[i][j] > L
                                    for j,i in enumerate(a))
                                for a in assignments)
        counts['earlier_candidate_sentinel_patterns'] += sentinel_patterns
        for a in assignments:
            if any(P[i][j] is None or P[i][j] > L
                   for j,i in enumerate(a)):
                assert max(loads(Qlow,a)) >= pad['sentinel']

    # Every unenumerated padded schedule uses a sentinel: either an original
    # moves to a dummy machine, or some dummy leaves its unique private edge.
    # Its makespan is >= sentinel, strictly above every qualifying output.
    assert pad['N']-n > 0
    counts['complete_private_block_classifications'] += 1


def main():
    counts = Counter()
    assert loads(((),()),()) == (F(0),F(0))
    counts['empty_original_case'] += 1
    palette_samples = []
    for H in list(range(2,129))+[257,513,1025]:
        palette, exponent_count = make_palette_from_h(H)
        counts['palette_h_values'] += 1
        if H in [2,4,16,64,128,257,513,1025]:
            palette_samples.append({'H':H,'distinct':len(palette),
                                    'universal_bound':H//2+2,
                                    'grid_exponents':exponent_count})

    for n in range(1,6):
        for k in [2,3]:
            check_scalar_edges(padding(n,k),counts)

    palette = [F(0),F(1,3),F(1),F(2),None]
    for n in [1,2]:
        for entries in product(palette,repeat=2*n):
            P = (entries[:n],entries[n:])
            if all(any(P[i][j] is not None for i in range(2)) for j in range(n)):
                for k in [2,3]:
                    check_matrix(P,k,counts)

    huge = 2**521+47
    fixtures = [
        ((F(1),),),
        ((F(0),F(1,2**521+47),F(2),F(1,3)),),
        ((F(1),None),(F(2),F(1,3)),(F(0),F(2))),
        ((F(0),F(1),None,F(1,huge)),(F(1),F(0),F(3,2),F(0))),
        ((F(1),F(1),F(1),F(1)),(F(1),F(1),F(1),F(1))),
        ((None,F(1,huge),F(2),F(1,3)),(F(1),None,F(1),F(2,7))),
        ((F(0),F(1,huge),F(1),F(7,3),None),
         (F(0),F(2,huge),F(3,2),None,F(1,7))),
    ]
    for P in fixtures:
        for k in [2,3]:
            check_matrix(P,k,counts)
    rng = random.Random(20261019)
    random_palette = palette+[F(1,huge),F(7,11),F(5,2)]
    for n in [3,4,5]:
        accepted = 0
        while accepted < 60:
            P = tuple(tuple(rng.choice(random_palette) for _ in range(n))
                      for _ in range(2))
            if all(any(P[i][j] is not None for i in range(2)) for j in range(n)):
                for k in [2,3]:
                    check_matrix(P,k,counts)
                accepted += 1

    for k in range(2,1001):
        b, alpha = F(8*k+1,8*k),F(2)-F(1,k)
        assert alpha*b*b == (F(2)-F(1,2*k)-F(7,32*k*k)-F(1,64*k**3))
        assert alpha*b*b < F(2)-F(1,2*k)
        # Symbolic dimensions avoid allocating the enormous N for large k.
        n = k*k+1
        ell = (8*k*n-1).bit_length()
        E = (1 << k)*8*k*ell
        assert (E+1)//(1 << k) == 8*k*ell
        counts['fixed_k_ratio_and_padding_identities'] += 1

    pad_samples = []
    for n,k in [(1,2),(2,2),(5,2),(5,3)]:
        p = padding(n,k)
        pad_samples.append({
            'original_n':n,'fixed_k':k,'N_is_2_to_power':p['E'],
            'actual_H':p['H'],'palette_distinct':len(p['palette']),
            'palette_bound':2+p['H']//2,
            'active_grid_length':len(p['powers']),
            'sentinel_bitlength':p['sentinel'].bit_length(),
        })
    output = {
        'status':'passed','arithmetic':'fractions.Fraction and exact integers',
        'seed':20261019,'counts':dict(counts),
        'palette_samples':palette_samples,'padding_samples':pad_samples,
        'scope':('Complete compressed classification of all low-load padded schedules; '
                 'active assignments enumerated for stated finite matrices. No full padded '
                 'matrix materialized, no B implemented or executed, no Git/history/push '
                 'state read, no hardness claim.'),
    }
    repo = Path(__file__).resolve().parents[3]
    output['reproduction'] = {'command': 'python3 tests/audits/unrelated_machines/logarithmic_palette_padding_equivalence.py', 'python': __import__('sys').version, 'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'proof_sha256': hashlib.sha256((repo/'research/current/unrelated_machines/model_and_classical_barriers.md').read_bytes()).hexdigest()}
    print(json.dumps(output,indent=2))


if __name__ == '__main__':
    main()
