"""Exact finite binomial audit; no general SDP or whole-family matrix generation."""

import argparse
from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path
import json


OUT = Path('raw_sh3_inclusion_entry_cut_binomial_audit.json')


def binomial_case(q, m, a, b, delta):
    assert q > 0 and q % 4 == 0 and m >= 100*q
    n = comb(m, q)
    c = comb(m-q, q)
    k = comb(2*q, q)
    g = comb(m, 2*q)
    assert n*c == g*k
    h = sum(comb(q, j)*comb(m-q, q-j) for j in range(q//4, q+1))
    tiny = sum(comb(q, j)**2 for j in range(q//4))
    s1, s2 = q**a, q**b
    d1, d2 = c//(k*s1), k//s2
    assert d1 >= 1 and d2 >= 1

    hbound = Fraction(8, 49)**(q//4)
    mbound = (q+1)*(2*q+1)*Fraction(256, 729)**(q//4)
    floorbound = Fraction(4, 99)**q
    assert Fraction(h, c) < hbound
    assert Fraction(tiny, k) <= mbound
    assert Fraction(k, c) <= floorbound
    assert k*(2*q+1) >= 4**q
    lhs = delta*d1*(delta*d2-tiny)
    certificate = lhs > h
    if q == 64:
        assert certificate
    return {
        'q': q, 'm': m, 'scale_exponents': [a,b],
        'delta': str(delta), 'd1': str(d1), 'd2': str(d2),
        'H': str(h), 'M': str(tiny),
        'strict_reverse_cut': certificate,
        'exact_cut_margin_over_C': str((lhs-h)/c),
        'H_over_C': str(Fraction(h,c)), 'M_over_K': str(Fraction(tiny,k)),
        'all_four_binomial_bounds_verified': True,
        'original_counts': {
            'machines': str(2*n+g), 'jobs': str(1+n*d1+g*d2),
            'finite_entries': str(n+n*d1*(1+c)+g*d2*(1+k)),
        },
    }


def small_complete_original_matrix():
    """A small general inclusion matrix, outside m>=100q asymptotic scope."""
    m, q = 6, 2
    subsets = tuple(combinations(range(m), q))
    blocks = tuple(combinations(range(m), 2*q))
    n, c, k = len(subsets), comb(m-q,q), comb(2*q,q)
    d1, d2 = c//k, k
    machines = [('U',s) for s in subsets]+[('B',w) for w in blocks]+[('Z',t) for t in subsets]
    eligible_b = {s:tuple(w for w in blocks if set(s) <= set(w)) for s in subsets}
    eligible_t = {w:tuple(t for t in subsets if set(t) <= set(w)) for w in blocks}
    jobs = {('h',):{('U',s):Fraction(1) for s in subsets}}
    for s in subsets:
        for j in range(d1):
            endpoints = {('U',s):Fraction(1,d1)}
            endpoints.update({('B',w):Fraction(1) for w in eligible_b[s]})
            jobs[('f',s,j)] = endpoints
    for w in blocks:
        for ell in range(d2):
            endpoints = {('B',w):Fraction(1,d2)}
            endpoints.update({('Z',t):Fraction(1) for t in eligible_t[w]})
            jobs[('e',w,ell)] = endpoints
    assert len(machines) == 45 and len(jobs) == 106
    assert sum(map(len,jobs.values())) == 750

    a_u, a_b = Fraction(1,n), Fraction(k*d1,n*c)
    configs = {v:[] for v in machines}
    for s in subsets:
        configs[('U',s)] = [(1-a_u,tuple(('f',s,j) for j in range(d1))),
                            (a_u,(('h',),))]
    for w in blocks:
        configs[('B',w)].append((1-a_b,tuple(('e',w,l) for l in range(d2))))
        for s in subsets:
            if set(s) <= set(w):
                for j in range(d1):
                    configs[('B',w)].append((Fraction(1,n*c),(('f',s,j),)))
    for t in subsets:
        configs[('Z',t)].append((1-Fraction(d1*d2,n),()))
        for w in blocks:
            if set(t) <= set(w):
                for ell in range(d2):
                    configs[('Z',t)].append((a_b/k,(('e',w,ell),)))
    cover = {job:Fraction(0) for job in jobs}
    first = {(job,v):Fraction(0) for job,ends in jobs.items() for v in ends}
    count = 0
    for v, row in configs.items():
        assert sum(prob for prob,_ in row) == 1
        for prob, config in row:
            assert prob >= 0 and len(set(config)) == len(config)
            assert sum(jobs[job][v] for job in config) <= 1
            for job in config:
                cover[job] += prob
                first[(job,v)] += prob
            count += 1
    assert all(value == 1 for value in cover.values())
    for job,ends in jobs.items():
        for v in ends:
            if job[0] == 'h':
                expected = a_u
            elif job[0] == 'f':
                expected = 1-a_u if v[0] == 'U' else Fraction(1,n*c)
            else:
                expected = 1-a_b if v[0] == 'B' else a_b/k
            assert first[(job,v)] == expected

    s = subsets[0]
    w = eligible_b[s][0]
    t = eligible_t[w][0]
    assignment = {('h',):('U',s)}
    for job in jobs:
        if job[0] == 'f':
            assignment[job] = ('B',w) if job == ('f',s,0) else ('U',job[1])
        elif job[0] == 'e':
            assignment[job] = ('Z',t) if job == ('e',w,0) else ('B',job[1])
    assert set(assignment) == set(jobs)
    loads = {v:Fraction(0) for v in machines}
    for job,v in assignment.items():
        loads[v] += jobs[job][v]
    expected_peak = max(Fraction(1),2-Fraction(1,d1),2-Fraction(1,d2))
    assert max(loads.values()) == expected_peak == Fraction(11,6)
    return {'scope':'small matrix/config/path audit, not asymptotic cut instance',
            'q':q,'m':m,'machines':len(machines),'original_jobs':len(jobs),
            'finite_entries':sum(map(len,jobs.values())),
            'explicit_CONFIG1_support':count,'all_original_cover_equalities':len(cover),
            'all_finite_endpoint_marginals':len(first),
            'complete_path_assignment_jobs':len(assignment),'actual_path_peak':str(expected_peak)}


def main():
    cases = [binomial_case(q,m,a,b,delta)
             for q in (4,8,16,32,64)
             for m in (100*q,104*q)
             for a,b in ((0,0),(1,1),(2,2))
             for delta in (Fraction(1),Fraction(1,2),Fraction(1,4),Fraction(1,8))]
    toy = small_complete_original_matrix()
    result = {'scope':'exact finite binomial formulas plus separate small complete original matrix',
              'binomial_cases':len(cases),'strict_reverse_cut_cases':sum(x['strict_reverse_cut'] for x in cases),
              'cases':cases,'small_complete_matrix':toy,
              'not_run':['general SDP solver','full m>=100q matrix materialization',
                         'all complete assignments','unknown source-solution decoder']}
    OUT.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'binomial_cases':len(cases),
                      'strict_reverse_cut_cases':result['strict_reverse_cut_cases'],
                      'small_complete_matrix':toy,'output':str(OUT)},sort_keys=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    OUT = parser.parse_args().output
    if OUT.exists():
        parser.error('refusing to overwrite an existing output')
    main()
