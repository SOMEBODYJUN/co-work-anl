#!/usr/bin/env python3
"""Finite exact audit of the polynomial step-DAG all-in bound, not a proof."""
import argparse
from fractions import Fraction as Q
import hashlib
import json
import random
import sys


def poly(coeff, x):
    return sum((a*x**k for k, a in enumerate(coeff)), Q(0))


def audit(q, edges, weights, degree, shape, rng):
    m = len(weights)
    assert sum(weights) < 1
    assert all(0 <= u < v < m for u, v in edges)
    out = [sum((weights[v] for u, v in edges if u == j), Q(0)) for j in range(m)]
    assert all(out[v] < weights[v] for v in range(m))
    h = []
    for v in range(m):
        h.append((1+sum((h[u] for u, j in edges if j == v), Q(0)))/q)
    assert sum(h) == q-1
    anchors, amplitudes = [Q(1)]+[1+w for w in weights], [Q(1)]+h
    polynomials = []
    for r, (anchor, amplitude) in enumerate(zip(anchors, amplitudes)):
        raw = [Q(0)]*(degree+1)
        if shape == 0:
            raw[0 if r == 0 else degree] = 1
        elif shape == 1:
            raw[degree] = 1
        elif shape == 2:
            raw[0] = 1
        else:
            raw = [Q(rng.randint(0,4), rng.randint(1,3)) for _ in range(degree+1)]
            if not any(raw):
                raw[0] = 1
        norm = poly(raw, anchor)
        polynomials.append([amplitude*a/norm for a in raw])
    # Resource indices: A_r=2r, B_r=2r+1, r=0 root anchor, r=v+1 satellites.
    strategies = [(frozenset(2*r for r in range(m+1)),
                   frozenset(2*r+1 for r in range(m+1)))]
    for v in range(m):
        parents = [u for u, j in edges if j == v]
        strategies.append((frozenset([0, 2*(v+1)+1]+[2*(u+1) for u in parents]),
                           frozenset([1, 2*(v+1)]+[2*(u+1)+1 for u in parents])))
    full_weights = [Q(1)]+weights
    state = [0]+[1]*m

    def costs(profile, player):
        return sum((poly(polynomials[e//2], sum(
                    (full_weights[j] for j in range(m+1)
                     if e in strategies[j][profile[j]]), Q(0)))
                    for e in strategies[player][profile[player]]), Q(0))

    current = [costs(state, i) for i in range(m+1)]
    assert current[0] == q
    literal_deviations = []
    bound = q/(1+(q-1)*(1+1/(q*(q-1)))**(-degree))
    delta = [weights[v]-out[v] for v in range(m)]
    T = sum((h[v]*weights[v] for v in range(m)), Q(0))
    gap_moment = sum((h[v]*delta[v] for v in range(m)), Q(0))
    W = sum(weights)
    assert gap_moment == W-(q-1)*T
    assert gap_moment <= W/q < 1/q
    assert all(h[v] >= 1/q for v in range(m))
    for i in range(m+1):
        moved = list(state)
        moved[i] = 1-state[i]
        after = costs(moved, i)
        assert after > 0
        factor = bound if i == 0 else 1+1/q
        assert current[i] <= factor*after
        if i == 0:
            assert after >= 1+(q-1)*(1+1/(q*(q-1)))**(-degree)
        literal_deviations.append({'player':i, 'before':str(current[i]),
                                   'after':str(after), 'bound':str(factor)})
    return {'q':str(q), 'degree':degree, 'shape':shape,
            'weights':list(map(str,weights)), 'edges':list(map(list,edges)),
            'h':list(map(str,h)),
            'polynomials':[[str(a) for a in coeff] for coeff in polynomials],
            'strategies':[[sorted(s) for s in family] for family in strategies],
            'all_in_state':state, 'gap_moment':str(gap_moment),
            'deviations':literal_deviations}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', help='Create a new record exclusively; never overwrite.')
    parser.add_argument('--check', help='Recompute and compare an existing record.')
    args = parser.parse_args()
    if args.output and args.check:
        parser.error('--output and --check are mutually exclusive')
    rng = random.Random(524170)
    families = [(Q(2), [], [Q(999,2000)]*2),
                (Q(3), [], [Q(1,12)]*6),
                (Q(3), [], [Q(999,6000)]*6),
                (Q(3), [(0,4),(1,4),(2,4)], [Q(1,2**(v+2)) for v in range(5)]),
                (Q(4), [(v,10) for v in range(4)],
                 [Q(1,2**(v+2)) for v in range(11)])]
    cases = [audit(q, edges, weights, d, shape, rng)
             for q, edges, weights in families for d in [0,1,2,4,16,32]
             for shape in range(7)]
    result = {'finite_evidence_only':True, 'python':sys.version.split()[0],
              'seed':524170, 'arithmetic':'fractions.Fraction',
              'source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest(),
              'cases':cases, 'games':len(cases),
              'literal_deviations':sum(len(c['deviations']) for c in cases)}
    if args.output:
        with open(args.output,'x',encoding='utf-8') as target:
            json.dump(result,target,ensure_ascii=False,indent=2)
            target.write('\n')
    elif args.check:
        with open(args.check,encoding='utf-8') as source:
            assert json.load(source) == result
    else:
        print(json.dumps(result,ensure_ascii=False,indent=2))
    if args.output or args.check:
        print(json.dumps({k:result[k] for k in ['finite_evidence_only','games',
              'literal_deviations','source_sha256']}))


if __name__ == '__main__':
    main()
