"""Independent residual-profit optimization; no repository solver imported.
Finite enumeration checks an independent all-n elimination proof, not SPE by sampling.
"""
from fractions import Fraction as F
from pathlib import Path
import json


def vectors(total, width):
    if width == 1:
        yield (total,)
    else:
        for k in range(total + 1):
            for tail in vectors(total-k, width-1):
                yield (k,) + tail


def one(n):
    x=n-2
    groups=[]
    for j in range(n-1):
        groups += [((j+2,),x),((0,j+2),1),((1,j+2),x)]
    groups += [((n+1,),x),((1,n+1),x),((0,1,n+1),n-1)]
    def value(q):
        answer=F(0)
        for likes,multiplicity in groups:
            load=sum(q[a] for a in likes)
            background=int(0 in likes)
            if load:
                answer += F(multiplicity*load,background+load)
        return answer
    maximum=F(-1); best=None; checked=0
    for q in vectors(n-1,n+2):
        v=value(q); checked+=1
        if v>maximum: maximum,best=v,q
    expected=2*(n-1)*(n-2)+F(7*n-13,6)
    target=(0,1)+(1,)*(n-3)+(0,0)+(1,)
    assert len(target)==n+2 and sum(target)==n-1
    assert value(target)==maximum==expected
    u=F(n*n-1,n)
    optimum=2*n*n-2*n-2
    slack=2*u+maximum-optimum
    assert slack==F(23-5*n,6)-F(2,n)
    if n>=5: assert slack<0
    return dict(n=n,groups=len(groups),customers=sum(v for _,v in groups),
                residual_count_vectors=checked,F_tail=str(maximum),maximizer=list(best),
                root_u=str(u),OPT=optimum,Bellman_half_slack=str(slack),
                minimum_required_coefficient=str(F(optimum-maximum,u)))


def main():
    result={'status':'PASS','scope':'finite residual-profit exact checks only; all-n proof in review',
            'runs':[one(n) for n in range(4,9)]}
    out=Path(__file__).with_name('profit_bellman_family_independent_audit.json')
    with out.open('x') as f: json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(result))

if __name__=='__main__': main()
