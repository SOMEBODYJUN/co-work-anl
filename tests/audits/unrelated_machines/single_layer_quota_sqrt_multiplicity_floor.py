#!/usr/bin/env python3
from fractions import Fraction
from itertools import combinations, product

def nu(A, U, t):
    opts=[]
    for mask in A:
        bits=[i for i in range(U) if mask>>i & 1]
        bundles=[]
        for c in combinations(bits,t):
            z=0
            for i in c: z |= 1<<i
            bundles.append(z)
        opts.append(bundles)
    dp={0:0}
    for choices in opts:
        nxt=dict(dp)
        for used,count in dp.items():
            for b in choices:
                if used & b: continue
                nm=used|b
                nxt[nm]=max(nxt.get(nm,-1),count+1)
        dp=nxt
    return max(dp.values(),default=0)

def check_family(A,U,K):
    q=len(A)
    Delta=max(sum((m>>u)&1 for m in A) for u in range(U))
    b=max(min(Fraction(t,K),Fraction(nu(A,U,t),q)) for t in range(1,K+1))
    B=max(min(Fraction(t,K),Fraction(K-t+1,K-t+1+t*Delta)) for t in range(1,K+1))
    assert b>=B,(A,U,K,Delta,b,B)

def main():
    cases=0
    for U,K in ((3,2),(4,2),(5,2),(4,3),(5,3)):
        masks=[m for m in range(1<<U) if m.bit_count()>=K]
        for A in product(masks,repeat=3):
            check_family(A,U,K); cases+=1
    for Delta in range(1,9):
        for K in range(1,9):
            g=2; U=g*K; A=[]
            for j in range(g):
                block=((1<<K)-1)<<(j*K); A.extend([block]*Delta)
            q=len(A)
            got=max(min(Fraction(t,K),Fraction(nu(tuple(A),U,t),q)) for t in range(1,K+1))
            expected=max(min(Fraction(t,K),Fraction(K//t,Delta)) for t in range(1,K+1))
            assert got==expected,(Delta,K,got,expected)
    print(f'ok: {cases} exhaustive systems; group formulas checked')

if __name__=='__main__': main()
