#!/usr/bin/env python3
"""Independent literal-index audit of the second, K=0 AB projection.

Uses only standard library; imports no discovery/author verification code.
Enumerates every six-multiset of the sixteen (t,f,b,c) customer words.
Every off/all/query_equal sum is evaluated directly on its ordered indices.
Read-only with respect to six_lift. Prints its exact report to stdout.
"""
from pathlib import Path
from itertools import product, combinations_with_replacement
from fractions import Fraction as F
import json
import time

def main():
    start = time.time()
    here = Path(__file__).resolve().parents[2] / 'six_lift'
    cert = json.loads((here / 'joint_full_AB_extension.json').read_text())
    weights = cert['integer_row_weights']
    saved = json.loads((here / 'AB_projected_row_joint.json').read_text())
    patterns = list(product((0, 1), repeat=4))
    allvisible = list(product((0, 1), repeat=6))
    maxima = {}
    count = 0
    for p in range(3):
        actuals = sorted({(v[0], sum(v[:4]), sum(v[:5]))
                          for v in allvisible if sum(v[:2]) == p})
        for ix in combinations_with_replacement(range(16), 6):
            es = [patterns[k] for k in ix]
            d = sum(e[0] for e in es)
            shares, D, D1, PA, PG, H = [], [], [], [], [], []
            for t, f, b, c in es:
                z = p + t + f + b + c
                shares.append(tuple(60*x//z if x else 0 for x in (t, f, b, c)))
                D.append(60//(p+t+f+b+1))
                D1.append(60//(p+t+3))
                PA.append(60//(p+t+f+1))
                PG.append(60//((p+t+f+1)*(p+t+f+2)))
                H.append(shares[-1][2]+shares[-1][3]+b*PG[-1])
            raw = -weights['source'] * sum(s[0] for s in shares)
            raw += weights['floorfamily:1:3:off'] * sum(
                shares[i][1]-es[j][3]*D1[i]
                for i in range(6) for j in range(6) if i != j)
            raw += weights['floorfamily:3:1:off'] * sum(
                shares[i][3]-es[j][1]*D[i]
                for i in range(6) for j in range(6) if i != j)
            raw += weights['floorfamily:3:2:off'] * sum(
                shares[i][3]-es[j][2]*D[i]
                for i in range(6) for j in range(6) if i != j)
            raw += weights['floorfamily:3:3:all'] * sum(
                shares[i][3]-es[j][3]*D[i]
                for i in range(6) for j in range(6))
            raw += weights['pairfamily:2:3:query_equal'] * sum(
                H[i]-(es[j][2]+es[j][3])*PA[i]+es[j][2]*es[j][3]*PG[i]
                for i in range(6) for j in range(6) if i != j)
            nf = sum(e[1] for e in es)
            nb = sum(e[2] for e in es)
            nc = sum(e[3] for e in es)
            nbc = sum(e[2]*e[3] for e in es)
            for a, pf, ell in actuals:
                value = raw-weights['fixedfloor:actual:1:3']*(60//(a+5))*nc
                value -= sum(weights[f'fixedfloor:actual:5:{q}']*nq*(60//(ell+1))
                             for q, nq in [(1, nf), (2, nb), (3, nc)])
                value += weights['fixedpair:actual:2:3'] * (
                    -(60//(pf+1))*(nb+nc)+(60//((pf+1)*(pf+2)))*nbc)
                key = p, a, pf, ell, d
                maxima[key] = max(maxima.get(key, value), value)
            count += 1
    lookup = {}
    for v in allvisible:
        z, p, pf, ell = sum(v), sum(v[:2]), sum(v[:4]), sum(v[:5])
        def sh(x):
            return 60*x//z if x else 0
        H = sh(v[4])+sh(v[5])+(60//((pf+1)*(pf+2)))*v[4]
        constant = 6*(weights['source']*sh(v[2])
                      + weights['fixedfloor:actual:1:3']*sh(v[1])
                      + sum(weights[f'fixedfloor:actual:5:{q}'] for q in (1, 2, 3))*sh(v[5])
                      + weights['fixedpair:actual:2:3']*H)
        for d in range(7):
            lookup[''.join(map(str, v)), d] = constant+maxima[p, v[0], pf, ell, d]
    assert all(lookup[r['actual_bits'], r['d']] == r['coefficient']
               for r in saved['coefficients'])
    point = json.loads((here / 'joint_AB_input.json').read_text())
    upper = sum(F(x['weight'])*lookup[x['actual_bits'], x['d']]
                for x in point['support'])
    assert upper == F(cert['exact_upper_bound']) < 0
    assert cert['K_integer_coefficient'] == saved['K_integer_coefficient'] == 0
    print(json.dumps(dict(independent_literal_index_audit=True, histograms=count,
                          conditional_states=len(maxima), visible_coefficients=len(lookup),
                          K_coefficient=0, upper=str(upper),
                          seconds=time.time()-start), indent=2))

if __name__ == '__main__':
    main()
