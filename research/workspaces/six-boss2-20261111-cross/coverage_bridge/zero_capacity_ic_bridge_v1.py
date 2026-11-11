#!/usr/bin/env python3
"""Convert seed credit using genuine terminal ICs against six optimal labels.

No parameter LP is used. The common IC multipliers are exact minima over the
already exhaustive discrete visible types of the frozen rows.
"""
from fractions import Fraction as F
import json
from pathlib import Path

import zero_capacity_rows_v1 as base

HERE=Path(__file__).resolve().parent


def possible_a4(p,d):
    extra=d-1-p
    return [a4 for a4 in (0,1) if 0<=extra-a4<=1]


def enhanced2(p,d,a6,n,lam):
    total=F(0)
    # One B_j bit is shared by all five choices of i. Minimize it only after
    # that inner sum. C_i has positive query coefficient and may be dropped.
    for y,nj in ((0,6-n),(1,n)):
        if not nj:continue
        candidates=[]
        for bj in (0,1):
            term=F(0)
            for x,count in ((1,n-y),(0,5-n+y)):
                if not count:continue
                val=base.L2(p,d,0,x,y,0,bj,a6,n)+lam*F(n,6*(p+x+bj+1))
                term+=count*val
            candidates.append(term)
        total+=F(nj,30)*min(candidates)
    return total


def enhanced13(p,d,a6,n,a4,lam):
    # Z's true background is actual first four plus its forced R predecessor.
    return base.orbit_average(13,p,d,a6,n)+lam*F(n,6*(p+a4+2))


def main():
    data=json.loads((HERE/'mainline_zero_capacity_v1.json').read_text())
    c2=[]
    for r in data['cut2_complete_visible_table']:
        delta=F(r['L'][1])-F(r['L'][0])
        c2.append((delta*(r['p']+r['x']+r['Bj']+1),r))
    lam2,witness2=min(c2,key=lambda x:x[0])
    c13=[]
    for r in data['cut13_complete_visible_table']:
        delta=F(r['L'][1])-F(r['L'][0])
        for a4 in possible_a4(r['p'],r['d']):c13.append((delta*(r['p']+a4+1),dict(r,A4=a4)))
    lam13,witness13=min(c13,key=lambda x:x[0])
    assert lam2>0 and lam13>0
    out={'scope':'fixed common terminal-IC multipliers and finite local coverage conversion; not SPE counterexamples',
         'lambda2':str(lam2),'lambda2_limiting_signature':witness2,
         'lambda13':str(lam13),'lambda13_limiting_signature':witness13,
         'enhanced_coverage':{},'two_signature_obstruction':{}}
    for row,lam in ((2,lam2),(13,lam13)):
        def val(p,d,a6,n,a4):
            return enhanced2(p,d,a6,n,lam) if row==2 else enhanced13(p,d,a6,n,a4,lam)
        misses=[val(0,1,0,n,0) for n in range(1,7)];A=min(misses)
        cases=[]
        for p in range(4):
            for extra in range(3):
                d=p+extra+1
                for a4 in possible_a4(p,d):
                    for a6 in (0,1):
                        for n in range(7):
                            v=val(p,d,a6,n,a4)
                            signature={'p':p,'d':d,'A4':a4,'A6':a6,'n':n}
                            if d-1+a6>0:cases.append((A*int(n>0)-v,signature,v))
        B,worst,worstval=max(cases,key=lambda x:x[0])
        out['enhanced_coverage'][str(row)]={'miss_credits':list(map(str,misses)),
            'A':str(A),'B':str(B),'worst_tax_signature':worst,'worst_average':str(worstval)}
        # Both signatures lie inside the finite local projection domain.
        # They are not claimed to jointly realize a complete SPE.
        U=base.orbit_average(row,0,1,0,1)
        C=base.orbit_average(row,0,2,0,1)
        scale=base.SCALE[row]
        Unew=val(0,1,0,1,0);Cnew=val(0,2,0,1,1)
        out['two_signature_obstruction'][str(row)]={
            'uncovered_signature':'actual=000000, one optimal membership, old replies/seed projected to zero',
            'covered_signature':'actual=000100, one optimal membership, old replies/seed projected to zero',
            'raw_required_half_multiplier_upper':str(U),
            'raw_required_half_multiplier_lower':str(scale-C),
            'after_ic_required_half_multiplier_upper':str(Unew),
            'after_ic_required_half_multiplier_lower':str(scale-Cnew),
            'raw_intervals_disjoint':U<scale-C,'after_ic_intervals_disjoint':Unew<scale-Cnew}
    (HERE/'zero_capacity_ic_bridge_v1.json').write_text(json.dumps(out,indent=2)+'\n')
    print(out)


if __name__=='__main__':main()
