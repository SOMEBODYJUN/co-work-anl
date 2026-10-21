"""Independent raw-unit-customer Fraction audit; no LP/model/author imports.

Generic-Q cases use its cap in place of v, which audits the algebra and upper
rounding bound. Exact minimax is separately certified on sharp disjoint families
and the two-singleton mixed game. Universal results use analytic proofs.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement
import json,random
from pathlib import Path


def all_counts(p,n):
    for tup in combinations_with_replacement(range(p),n):
        yield tuple(tup.count(a) for a in range(p))


def load(mask,b):return sum(q for a,q in enumerate(b) if mask>>a&1)
def value(clients,a,b):return sum((F(1,1+load(mask,b)) for mask in clients if mask>>a&1),F())
def coverage(clients,T):return sum(any(mask>>a&1 for a in T) for mask in clients)


def check(clients,p,n,Q,T,cap):
    C=[i for i,mask in enumerate(clients) if any(mask>>a&1 for a in T)]
    Cset=set(C);O=len(C);d=[sum(bool(mask>>a&1) for a in T) for mask in clients]
    L=[sum((prob*load(mask,b) for b,prob in Q),F()) for mask in clients]
    g=[sum((F(1,1+L[i]) for i,mask in enumerate(clients) if mask>>a&1),F()) for a in range(p)]
    expected=[sum((prob*value(clients,a,b) for b,prob in Q),F()) for a in range(p)]
    assert max(expected)==cap
    delta=[cap-x for x in expected];J=[x-y for x,y in zip(expected,g)]
    j=[]
    for i,mask in enumerate(clients):
        jx=sum((prob*(load(mask,b)-L[i])**2/((1+L[i])**2*(1+load(mask,b))) for b,prob in Q),F())
        assert jx==sum((prob*F(1,1+load(mask,b)) for b,prob in Q),F())-1/(1+L[i])
        j.append(jx)
    assert all(J[a]==sum((j[i] for i,mask in enumerate(clients) if mask>>a&1),F()) for a in range(p))
    Rov=sum((F(d[i]-1,1+L[i]) for i in C),F())
    Rout=sum((L[i]/(1+L[i]) for i in range(len(clients)) if i not in Cset),F())
    q=[sum((prob*b[a] for b,prob in Q),F())/max(1,n-1) for a in range(p)]
    D=(2*n-1)*cap-O
    assert D==Rov+Rout+sum((delta[a]+J[a] for a in T),F())+(n-1)*sum((q[a]*(delta[a]+J[a]) for a in range(p)),F())
    JC=sum((j[i] for i in C),F());FC=sum((prob*sum((F(1,1+load(clients[i],b)) for i in C),F()) for b,prob in Q),F())
    assert FC<=n*cap and JC+Rout<=D
    supportcap=min(max(value(clients,a,b) for a in range(p)) for b,prob in Q if prob)
    residual=supportcap-cap-Rout-JC/2
    assert residual<=0 or 4*residual**2<=JC*FC
    return L,g,D


def main():
    rng=random.Random(20261021);generic=0;sharp_backgrounds=0
    for n in range(1,5):
        for p in range(1,6):
            for _ in range(4):
                clients=[rng.randrange(1,1<<p) for _ in range(rng.randrange(0,16))]
                B=list(all_counts(p,n-1));weights=[rng.randrange(1,8) for b in B];den=sum(weights)
                Q=[(b,F(w,den)) for b,w in zip(B,weights)]
                T=max(combinations_with_replacement(range(p),n),key=lambda t:coverage(clients,t))
                cap=max(sum((prob*value(clients,a,b) for b,prob in Q),F()) for a in range(p))
                check(clients,p,n,Q,T,cap);generic+=1
    for n in range(1,8):
        p=n;clients=[1]*n+[1<<a for a in range(1,n)];T=tuple(range(n));B0=(n-1,)+(0,)*(n-1)
        L,g,D=check(clients,p,n,[(B0,F(1))],T,F(1));assert D==0
        query=[F(n,2*n-1)]+[F(1,2*n-1)]*(n-1)
        for b in all_counts(p,n-1):
            left=sum((query[a]*value(clients,a,b) for a in range(p)),F())-1
            right=(sum((b[a]*(1-g[a]) for a in range(p)),F())+sum((F((load(mask,b)-L[i])**2,(1+L[i])*(1+load(mask,b))) for i,mask in enumerate(clients)),F()))/(2*n-1)
            assert left==right and left>=0
            assert (left==0)==all(load(mask,b)==L[i] for i,mask in enumerate(clients))
            sharp_backgrounds+=1
    # Exact mixed minimax: both pure queries get 3/4 against the fair Q;
    # the fair query gets 3/4 against both pure backgrounds.
    mixed_clients=[1,2];Q=[((1,0),F(1,2)),((0,1),F(1,2))]
    for b,_ in Q:assert sum((F(1,2)*value(mixed_clients,a,b) for a in range(2)),F())==F(3,4)
    check(mixed_clients,2,2,Q,(0,1),F(3,4))
    result={'status':'passed','seed':20261021,'generic_cap_identity_and_rounding_cases':generic,
            'sharp_disjoint_minimax_families':7,'sharp_background_identity_cases':sharp_backgrounds,
            'mixed_minimax_cases':1,'universal_proof_by_finite_search':False,'Q_CAG_HALF':'OPEN'}
    Path(__file__).with_name('security_slack_review.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
