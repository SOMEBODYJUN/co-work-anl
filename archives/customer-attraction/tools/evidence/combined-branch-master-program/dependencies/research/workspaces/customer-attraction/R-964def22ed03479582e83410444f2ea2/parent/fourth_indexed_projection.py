#!/usr/bin/env python3
"""Full six-index, two-follower projection at the actual fourth source.

Uses only exact integers. The five raw rows are real source IC, actual last
pair comparisons, two families of terminal IC, and off-branch pair comparisons.
This is a necessary inequality, not a half-coverage certificate or SPE solver.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import math

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'work.py').exists())
OLD = ROOT / 'research/workspaces/customer-attraction/R-d1fe1e0c444e40d68b6813bf88db8fba'
WEIGHTS = (83667573, 9398368, 1172672, 2396329, 3365058)
PATTERNS = tuple(product((0, 1), repeat=3))


def compositions(total, length):
    if length == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for rest in compositions(total - first, length - 1):
                yield (first,) + rest


HISTS = tuple(tuple(a + b for a, b in product(compositions(6-d, 4), compositions(d, 4)))
              for d in range(7))


def sh60(num, den):
    if not num:
        return 0
    assert den and 60 % den == 0
    return num * (60 // den)


def compact_rows(a, hist):
    """Each entry is 60 times the corresponding customer coefficient."""
    p = sum(a[:3])
    pa = p + a[3]
    whole = sum(a)
    ua = sh60(a[3], whole)
    ha = sh60(a[4] + a[5], whole) + sh60(a[4], (pa+1)*(pa+2))
    nb = sum(n*b for n, (t,b,c) in zip(hist, PATTERNS))
    nc = sum(n*c for n, (t,b,c) in zip(hist, PATTERNS))
    nbc = sum(n*b*c for n, (t,b,c) in zip(hist, PATTERNS))
    source = 6*ua
    fixedpair = 6*ha
    last_b = last_c = pair = 0
    for n, (t,b,c) in zip(hist, PATTERNS):
        if not n:
            continue
        source -= n*sh60(t, p+t+b+c)
        fixedpair += n*(-sh60(b+c, pa+1) + sh60(b*c, (pa+1)*(pa+2)))
        den = p+t+b+1
        last_b += n*sh60(5*c-nb+b, den)
        last_c += n*sh60(6*c-nc, den)
        hi = sh60(b+c, p+t+b+c) + sh60(b, (p+t+1)*(p+t+2))
        pair += n*(5*hi-sh60(nb-b+nc-c, p+t+1)
                   +sh60(nbc-b*c, (p+t+1)*(p+t+2)))
    return source, fixedpair, last_b, last_c, pair


def literal_rows(a, hist):
    """Definition-level independent implementation, using labeled i,j sums."""
    menu = tuple(z for n,z in zip(hist, PATTERNS) for _ in range(n))
    assert len(menu) == 6
    p = sum(a[:3])
    pa = sum(a[:4])
    s = sum(a)
    u4 = F(a[3], s) if a[3] else F()
    ha = (F(a[4]+a[5], s) if a[4]+a[5] else F()) + F(a[4], (pa+1)*(pa+2))
    def own_t(z):
        t,b,c=z
        return F(t,p+t+b+c) if t else F()
    def own_c(z):
        t,b,c=z
        return F(c,p+t+b+c) if c else F()
    def hi(z):
        t,b,c=z
        return (F(b+c,p+t+b+c) if b+c else F())+F(b,(p+t+1)*(p+t+2))
    rows = [6*u4-sum(map(own_t,menu)),
            sum(ha-F(b+c,pa+1)+F(b*c,(pa+1)*(pa+2)) for t,b,c in menu), F(), F(), F()]
    for i,(t,b,c) in enumerate(menu):
        for j,(_,bj,cj) in enumerate(menu):
            if i != j:
                rows[2] += own_c(menu[i])-F(bj,p+t+b+1)
                rows[4] += hi(menu[i])-F(bj+cj,p+t+1)+F(bj*cj,(p+t+1)*(p+t+2))
            rows[3] += own_c(menu[i])-F(cj,p+t+b+1)
    scaled = tuple(60*r for r in rows)
    assert all(r.denominator == 1 for r in scaled)
    return tuple(map(int, scaled))


def coefficient(a,d):
    return max(sum(w*r for w,r in zip(WEIGHTS,compact_rows(a,h))) for h in HISTS[d])


def run():
    assert sum(map(len,HISTS)) == math.comb(13,7) == 1716
    # Actual coordinates only affect the two additive constants and pa.
    # Reconstruct raw i,j rows for every histogram, all p=0..3 and both a4.
    raw_checked = 0
    for p in range(4):
        for a4 in (0,1):
            a = (1,)*p+(0,)*(3-p)+(a4,1,1)
            for family in HISTS:
                for h in family:
                    assert compact_rows(a,h)==literal_rows(a,h),(a,h)
                    raw_checked += 1
    coeff = [{'actual_bits':''.join(map(str,a)), 'd':d,
              'coefficient':str(coefficient(a,d))}
             for a in product((0,1), repeat=6) for d in range(7)]
    lookup = {(r['actual_bits'],r['d']):int(r['coefficient']) for r in coeff}
    point = json.loads((OLD/'parent/joint_system.json').read_text())['certificate']
    value = sum(F(z['weight'])*lookup[z['actual_bits'],z['d']] for z in point['support'])
    assert value < 0
    report = {
        'status':'exact necessary projection and strict separation verified; no half proof',
        'scope':'m=6; actual fourth source; six arbitrary comparison indices; all customer types',
        'scale':60, 'integer_weights':list(WEIGHTS), 'K_coefficient':0,
        'histogram_states':1716, 'raw_row_identity_cases':raw_checked,
        'customer_types':448, 'minimum_and_maximum_histograms_per_d':[len(h) for h in HISTS],
        'separated_point':'R-d1fe1e0c444e40d68b6813bf88db8fba/parent/joint_system.json',
        'exact_separation':str(value), 'normalized_separation':str(value/(60*WEIGHTS[0])),
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'coefficients':coeff,
    }
    target=HERE/'fourth_indexed_projection.json'
    target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='coefficients'},indent=2),flush=True)


if __name__=='__main__':run()
