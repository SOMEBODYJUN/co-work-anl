"""Definition-level audit of the converging-path lemma, all strict suffixes."""
import json
import random
from collections import Counter
from fractions import Fraction as F

OPTIONS=((0,1),(0,2),(1,3))  # X:AB, Z:AC, T:BD


def audit(gamma,r,p,Q,K,c,d,x,z,t):
    q=(r,p,r,Q);frozen=(r*gamma,K,c,d);weights=(x,z,t)
    def totals(s):
        W=list(frozen)
        for w,u in zip(weights,s):W[u]+=w
        return W
    def box(s):return all(v*gamma<=w<=(v+1)*gamma for w,v in zip(totals(s),q))
    def improve(s,i):
        u=s[i];v=next(k for k in OPTIONS[i] if k!=u);W=totals(s)
        return (W[u]-weights[i])*q[v]>W[v]*q[u]
    def potential(s):
        W=totals(s);ss=[v*v for v in frozen]
        for v,u in zip(weights,s):ss[u]+=v*v
        return sum(F(v*v-vv,2*h) for v,vv,h in zip(W,ss,q))
    s=[1,2,3]
    assert box(s)
    if c>r*gamma:s[1]=0
    assert box(s) and not improve(s,1)
    if improve(s,2):
        branch='T';s[2]=1;allowed=(0,1,2)
        assert K+x+t<=(p+1)*gamma
    elif improve(s,0):
        branch='X';s[0]=0;allowed=(1,2) if c>r*gamma else (2,)
    else:
        assert not any(improve(s,i) for i in range(3))
        return 'NE',1
    s=tuple(s);seen={s};stack=[s]
    while stack:
        u=stack.pop();assert box(u)
        assert all(not improve(u,i) for i in range(3) if i not in allowed)
        count=0
        for i in allowed:
            if improve(u,i):
                count+=1;v=list(u);v[i]=next(k for k in OPTIONS[i] if k!=u[i]);v=tuple(v)
                assert box(v) and potential(v)<potential(u)
                if v not in seen:seen.add(v);stack.append(v)
        if not count:assert not any(improve(u,i) for i in range(3))
    assert len(seen)<=8
    return branch,len(seen)


if __name__=='__main__':
    rng=random.Random(6347);counts=Counter();triples=set();ns=0;maximum=0
    for _ in range(10000):
        Q=rng.randint(1,9);p=rng.randint(1,Q);r=rng.randint(1,p);a=rng.randint(4,80)
        x,z,t=[rng.randint(1,a-1) for _ in range(3)]
        K=rng.randint(p*a,(p+1)*a)-x
        c=rng.randint(r*a,(r+1)*a)-z
        d=rng.randint(Q*a,(Q+1)*a)-t
        b,n=audit(a,r,p,Q,K,c,d,x,z,t)
        counts[b]+=1;triples.add((r,p,Q));ns+=n;maximum=max(maximum,n)
    print(json.dumps({'cases':10000,'seed':6347,'q_triples':len(triples),'branches':dict(counts),'all_suffix_states':ns,'max_suffix_states':maximum}),flush=True)
