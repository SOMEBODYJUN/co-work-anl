"""Exact finite regression for the general occupation-reserve algebra.
The proof is in occupation_reserve_review.md; finite tests do not prove its
quantifiers. No SPE, model, solver, or previous audit output is imported.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json


def evaluate(b, dist):
    # Each record is (root-membership a, future load k, probability p).
    assert sum(p for a,k,p in dist)==1
    en=sum(p*k for a,k,p in dist)
    ea=sum(p*a for a,k,p in dist)
    ef=sum(p/(1+b+a+k) for a,k,p in dist)
    V=sum(p*k/(1+b+a+k) for a,k,p in dist)
    D=sum((p/(b+1+k) for a,k,p in dist if a),F(0))
    G=ea*ef
    I=en*ef-V
    pair=F(0); tail_square=F(0)
    for a,k,p in dist:
        for aa,kk,pp in dist:
            den=(1+b+a+k)*(1+b+aa+kk)
            dn=k-kk; da=a-aa
            pair+=F(1,2)*p*pp*dn*(dn+da)/den
            if dn:tail_square+=F(1,2)*p*pp*(dn*dn-da*da)/den
    p0={k:sum((p for a,kk,p in dist if a==0 and kk==k),F(0)) for a,k,p in dist}
    grouped_tax=sum((p*(1-p0[k])/((b+1+k)*(b+2+k)) for a,k,p in dist if a),F(0))
    assert I==pair
    assert I-(G-D)==grouped_tax+tail_square
    return dict(I=I,G=G,D=D,V=V,n_qKp=en*ef,reserve_after_gap=I-G+D,grouped_tax=grouped_tax,nonzero_load_square=tail_square)

integer_cases=0; minimum_I=None; minimum_strong=None
for b in range(5):
    for n in range(1,7):
        states=[(a,k) for a in [0,1] for k in range(n+1)]
        distributions=[]
        for a,k in states: distributions.append([(a,k,F(1))])
        for (a,k),(aa,kk) in combinations(states,2):
            for t in [F(1,5),F(1,2),F(4,5)]:
                distributions.append([(a,k,t),(aa,kk,1-t)])
        # Two deterministic full-support distributions per domain.
        for weights in [list(range(1,len(states)+1)),list(range(len(states),0,-1))]:
            total=sum(weights)
            distributions.append([(a,k,F(w,total)) for (a,k),w in zip(states,weights)])
        for dist in distributions:
            r=evaluate(F(b),dist)
            assert r['I']>=0 and r['reserve_after_gap']>=0
            assert r['grouped_tax']>=0 and r['nonzero_load_square']>=0
            integer_cases+=1
            minimum_I=r['I'] if minimum_I is None else min(minimum_I,r['I'])
            minimum_strong=r['reserve_after_gap'] if minimum_strong is None else min(minimum_strong,r['reserve_after_gap'])

# These enlarged-model scalar examples show why the integer-load sign step
# may not be used on arbitrary fractional future-player masses.
fractional_I=evaluate(F(0),[(0,F(1,2),F(1,2)),(1,F(0),F(1,2))])
assert fractional_I['I']==F(-1,48)
fractional_strong=evaluate(F(0),[(0,F(0),F(9,10)),(1,F(1,4),F(1,10))])
assert fractional_strong['reserve_after_gap']==F(-7,3600)
result=dict(status='PASS',scope='Finite Fraction checks of exact general formulas and integer-load boundary only; not SPE or half evidence',integer_distribution_cases=integer_cases,minimum_I=str(minimum_I),minimum_strengthened_reserve=str(minimum_strong),fractional_I_boundary={k:str(v) for k,v in fractional_I.items()},fractional_strengthening_boundary={k:str(v) for k,v in fractional_strong.items()})
Path(__file__).with_name('occupation_reserve_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
