#!/usr/bin/env python3
"""Independent Exact-only reconstruction; finite checks, not a general proof.
No author proof or other reviews were read before this file was frozen.
"""
from fractions import Fraction as F
from itertools import product, combinations
from collections import deque
import random, json, hashlib, platform
from pathlib import Path

class Flow:
    def __init__(self): self.g=[]
    def node(self): self.g.append([]); return len(self.g)-1
    def edge(self,u,v,c):
        e=[v,c,len(self.g[v])]; f=[u,0,len(self.g[u])]
        self.g[u].append(e); self.g[v].append(f); return e
    def run(self,s,t):
        total=0
        while True:
            dist=[-1]*len(self.g); dist[s]=0; q=deque([s])
            while q:
                u=q.popleft()
                for v,c,r in self.g[u]:
                    if c and dist[v]<0: dist[v]=dist[u]+1; q.append(v)
            if dist[t]<0: return total
            cur=[0]*len(self.g)
            def dfs(u,c):
                if u==t: return c
                while cur[u]<len(self.g[u]):
                    e=self.g[u][cur[u]]; v,cap,rev=e
                    if cap and dist[v]==dist[u]+1:
                        f=dfs(v,min(c,cap))
                        if f: e[1]-=f; self.g[v][rev][1]+=f; return f
                    cur[u]+=1
                return 0
            while True:
                f=dfs(s,10**9)
                if not f: break
                total+=f

def threshold(P,b,T):
    m=len(P); n=len(P[0]) if m else 0
    chosen={j:next(i for i in range(m) if P[i][j]==0) for j in range(n) if any(P[i][j]==0 for i in range(m))}
    rem=[j for j in range(n) if j not in chosen]
    f=Flow(); src=f.node(); sink=f.node(); job={j:f.node() for j in rem}; refs=[]
    for j in rem: f.edge(src,job[j],1)
    N=len(rem)
    for i,row in enumerate(P):
        small=sorted([(row[j],j) for j in rem if row[j] is not None and 0<row[j]<b])
        units=[j for j in rem if row[j]==b]
        assert len(small)<=2
        def capnode(c):
            u=f.node(); f.edge(u,sink,min(N,max(0,c))); return u
        def attach(j,u): refs.append((j,i,f.edge(job[j],u,1)))
        if T<b:
            small=[x for x in small if x[0]<=T]
            cap=2 if len(small)==2 and sum(x[0] for x in small)<=T else 1
            u=capnode(cap)
            for p,j in small: attach(j,u)
            continue
        ell=T//b; a=T-ell*b
        if len(small)==0:
            u=capnode(ell)
            for j in units: attach(j,u)
        elif len(small)==1:
            p,j=small[0]; u=capnode(ell)
            for k in units: attach(k,u)
            attach(j,capnode(1) if p<=a else u)
        else:
            (p,x),(q,y)=small
            if p+q<=a:
                u=capnode(ell)
                for j in units: attach(j,u)
                attach(x,capnode(1)); attach(y,capnode(1))
            elif q<=a:
                r=capnode(ell+1); u=f.node(); f.edge(u,r,min(N,ell))
                for j in units: attach(j,u)
                attach(x,r); attach(y,r)
            elif p<=a or p+q<=b+a:
                u=capnode(ell)
                for j in units: attach(j,u)
                attach(y,u); attach(x,capnode(1))
            else:
                u=capnode(ell)
                for j in units+[x,y]: attach(j,u)
    if f.run(src,sink)!=N: return None
    for j,i,e in refs:
        if e[1]==0:
            assert j not in chosen
            chosen[j]=i
    assert len(chosen)==n
    sig=[chosen[j] for j in range(n)]; loads=[F(0) for _ in range(m)]
    for j,i in enumerate(sig): assert P[i][j] is not None; loads[i]+=P[i][j]
    return sig, max(loads,default=F(0)), loads

def candidate_values(P,b):
    n=len(P[0]) if P else 0; sums={F(0)}
    for row in P:
        sm=[p for p in row if p is not None and 0<p<b]
        sums.update(sm)
        if len(sm)==2: sums.add(sum(sm))
    return sorted({ell*b+s for ell in range(n+1) for s in sums if ell*b+s<=n*b})

def approximation(P,b):
    cand=candidate_values(P,b)
    for T in cand:
        if T>=b: break
        out=threshold(P,b,T)
        if out is not None: return out
    for T in cand:
        if T<b: continue
        out=threshold(P,b,T)
        if out is not None: return out
    raise AssertionError('legal input must succeed')

def oracle(P):
    m=len(P); n=len(P[0]) if m else 0; best=None
    ends=[[i for i in range(m) if P[i][j] is not None] for j in range(n)]
    for sig in product(*ends):
        loads=[F(0)]*m
        for j,i in enumerate(sig): loads[i]+=P[i][j]
        C=max(loads,default=F(0))
        if best is None or C<best: best=C
    return best

def local_family_check():
    count=0
    b=F(1)
    for ell in range(1,5):
      for a8 in range(8):
       a=F(a8,8); T=ell+a
       for p8 in range(1,8):
        for q8 in range(p8,8):
         p,q=F(p8,8),F(q8,8)
         for u in range(ell+2):
          for sx,sy in product([0,1],repeat=2):
           load=u+sx*p+sy*q
           if p+q<=a: allowed=u<=ell
           elif q<=a: allowed=u<=ell and u+sx+sy<=ell+1
           elif p<=a or p+q<=1+a: allowed=u+sy<=ell
           else: allowed=u+sx+sy<=ell
           assert load>T or allowed, ('misses feasible',ell,a,p,q,u,sx,sy)
           assert not allowed or load<=T+F(1,2), ('overload',ell,a,p,q,u,sx,sy)
           count+=1
    return count

def reduce_3dm(q,triples):
    if q<1 or any(not any(t[z]==v for t in triples) for z in range(3) for v in range(q)):
        return [[F(1),F(1)]]
    jobs=[('x',x) for x in range(q)]+[('y',y) for y in range(q)]
    for z in range(q): jobs += [('u',z)]*(sum(t[2]==z for t in triples)-1)
    P=[]
    for x,y,z in triples:
        P.append([F(1,2) if (kind=='x' and a==x) or (kind=='y' and a==y) else F(1) if kind=='u' and a==z else None for kind,a in jobs])
    return P

def main():
    rng=random.Random(73119); b=F(1); checks=0; families=0
    for _ in range(300):
        m=rng.randrange(1,5); n=rng.randrange(0,6); P=[]
        for i in range(m):
            row=[b if rng.randrange(3)==0 else None for j in range(n)]
            for j in rng.sample(range(n),rng.randrange(min(2,n)+1)): row[j]=F(rng.choice([1,2,3,4,5,6,7]),8)
            for j in range(n):
                if rng.randrange(18)==0: row[j]=F(0)
            P.append(row)
        for j in range(n):
            if all(P[i][j] is None for i in range(m)): P[rng.randrange(m)][j]=b
        opt=oracle(P)
        out=approximation(P,b); assert out[1]<=F(3,2)*opt
        for T in sorted(set([F(t,8) for t in range(0,25)]+candidate_values(P,b))):
            got=threshold(P,b,T)
            if T<b: assert (got is not None)==(opt<=T)
            elif opt<=T: assert got is not None
            if got is not None: assert got[1]<=T+(F(0) if T<b else b/2)
            checks+=1
        families+=1
    # All q=2 source subsets, excluding no-edge handled by legal constant NO.
    dm=0
    universe=list(product(range(2),repeat=3))
    for mask in range(1<<len(universe)):
        ts=[t for j,t in enumerate(universe) if mask>>j&1]
        yes=any(all(len({t[c] for t in pair})==2 for c in range(3)) for pair in combinations(ts,2))
        P=reduce_3dm(2,ts); opt=oracle(P)
        assert (opt<=1)==yes
        assert yes or opt>=F(3,2)
        assert all(sum(p is not None and 0<p<1 for p in row)<=2 for row in P)
        dm+=1
    payload={'provenance':'Exact-only independent reconstruction; no author proof read','claim_id':'UM-TWO-SMALL-INCIDENCE-SHARP-APPROXIMATION-v2','local_membership_checks':local_family_check(),'random_matrices':families,'threshold_checks':checks,'q2_3dm_all_subsets':dm,'status':'PASS','python':platform.python_version(),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(payload,sort_keys=True))
if __name__=='__main__': main()
