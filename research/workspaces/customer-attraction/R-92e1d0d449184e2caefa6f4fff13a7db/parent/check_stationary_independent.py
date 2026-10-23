"""Independent exact checks; no imports from the discovery or canonical solver."""
from fractions import Fraction as Q
from random import Random
import json


def payoff(b, inside, count):
    if not inside and not count:
        return Q(0), Q(0)
    return Q(inside, b+inside+count), Q(count, b+inside+count)


def loss(r, b, a, t):
    return Q(a*t*(r-a-t), (r-1)*(a+t)*(b+r-a)*(b+t))

rng=Random(9221)
counts={'pair_checks':0,'mixture_checks':0,'partial_checks':0,'derivative_checks':0,'sharp_multiplicative':0}
for r in range(2,42):
    n=r-1
    for b in (0,1,3,19):
        candidates=[loss(r,b,a,t) for a in range(1,n+1) for t in range(1,n+1)]
        sharp=max([Q(0),*candidates])
        factor=Q(n)+Q(n*n//4,b+1)
        best_ratio=Q(n)
        for a in range(1,n+1):
            for t in range(1,n+1):
                prob=Q(t,a+t)
                rin,bin_=payoff(b,1,n-a)
                rout,bout=payoff(b,0,t)
                R=prob*rin+(1-prob)*rout
                B=prob*bin_+(1-prob)*bout
                assert R-B/n == -loss(r,b,a,t)
                assert R-B/n>=-sharp
                assert B<=factor*R
                best_ratio=max(best_ratio,B/R)
                counts['pair_checks']+=1
        assert best_ratio==factor
        counts['sharp_multiplicative']+=1
        if b==0:
            D=(r+1)**2//4
            assert sharp==Q(1-Q(r,D),n)
        for repeat in range(5):
            terms=[]
            raw=[rng.randrange(1,10) for _ in range(4)]
            total=sum(raw)
            for wt in raw:
                a=rng.randrange(1,n+1);t=rng.randrange(1,n+1)
                terms.append((Q(wt,total)*Q(t,a+t),1,n-a))
                terms.append((Q(wt,total)*Q(a,a+t),0,t))
            assert sum(p for p,I,K in terms)==1
            assert sum(p*(K-n*I) for p,I,K in terms)==0
            R=sum(p*payoff(b,I,K)[0] for p,I,K in terms)
            B=sum(p*payoff(b,I,K)[1] for p,I,K in terms)
            assert R-B/n>=-sharp and B<=factor*R
            counts['mixture_checks']+=1
            partial=[(p,I,rng.randrange(K+1)) for p,I,K in terms]
            Rp=sum(p*payoff(b,I,K)[0] for p,I,K in partial)
            Bp=sum(p*payoff(b,I,K)[1] for p,I,K in partial)
            assert Rp>=R and Bp<=B
            assert Rp-Bp/n>=-sharp and Bp<=factor*Rp
            counts['partial_checks']+=1
        for ell in range(1,r-1):
            q=r-ell
            for t in range(1,q):
                # Finite difference clearing positive denominators.
                d=b*(b+ell); z=2*b+ell
                # Derivative numerator of t(q-t)/[(b+t)(b+t+ell)].
                first=(q-2*t)*(t*t+z*t+d)-(q*t-t*t)*(2*t+z)
                second=-(r+2*b)*t*t-2*d*t+q*d
                assert first==second
                counts['derivative_checks']+=1
print(json.dumps({'status':'passed','seed':9221,'scope':'r=2..41, b=0,1,3,19; exact rational checks only','checks':counts},ensure_ascii=False,indent=2))
