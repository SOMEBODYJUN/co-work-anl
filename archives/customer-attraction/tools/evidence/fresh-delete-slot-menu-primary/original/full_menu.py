"""Exact arbitrary-history SPE menu oracle for one fixed original-class instance.

For prescribed query p, maximize the stated candidate's LHS-W over all SPEs.
The finite test concerns that general candidate only, not a restricted theorem.
"""
from attack import Attack
from functools import lru_cache
from pathlib import Path
import json, math, sys
import numpy as np
from fractions import Fraction as F

class FullMenu:
    def __init__(self,o,w):
        assert o.m>=1 and o.k>=1 and len(w)==o.d
        assert all(isinstance(t,(int,np.integer)) and not isinstance(t,bool) and t>=0 for t in w)
        self.o,self.w=o,tuple(map(int,w))
        self.L=math.lcm(*range(1,o.m+1))
        # Integer utility scale, without floating coefficients or int64 overflow.
        self.pay={}
        for q in o.terminal:
            loads=o.sig@np.array(q)
            self.pay[q]=tuple(sum(self.w[j]*(self.L//int(loads[j])) for j in range(o.d) if o.sig[j,a] and loads[j]) for a in range(o.k))
        self.E={q:{q} for q in o.terminal};self.floor={}
        for q in reversed(o.states):
            if sum(q)==o.m:continue
            child=[self.E[r] for r in o.children[q]]
            floor=max(min(self.pay[z][a] for z in child[a]) for a in range(o.k))
            self.floor[q]=floor
            self.E[q]={z for a in range(o.k) for z in child[a] if self.pay[z][a]>=floor}

    def best(self,p,exact=False):
        o=self.o
        zero=F(0) if exact else 0.
        if exact:
            p=tuple(map(F,p))
            assert len(p)==o.k and all(t>=0 for t in p) and sum(p)==1
            pw=[sum((p[a] for a in range(o.k) if o.sig[j,a]),F(0)) for j in range(o.d)]
        # f(A,z) for deleting the distinguished forced A from terminal z.
        f={}
        for z in o.terminal:
            for a in range(o.k):
                if z[a]:
                    bg=list(z);bg[a]-=1
                    denom=1+o.sig@np.array(bg)
                    if exact:f[a,z]=sum((pw[j]*self.w[j]/int(denom[j]) for j in range(o.d)),F(0))
                    else:f[a,z]=float((p@o.sig.T/denom)@np.array(self.w,dtype=float))
        best=(-float('inf'),None,None,None)
        root=(0,)*o.k
        for B in self.E[root]:
            @lru_cache(None)
            def dp(q):
                if sum(q)==o.m:return zero,(),()
                opts=[]
                for a in range(o.k):
                    if B not in self.E[o.children[q][a]] or self.pay[B][a]<self.floor[q]:continue
                    ends=[];v=f[a,B]
                    for b in range(o.k):
                        if a==b:ends.append(B);continue
                        allowed=[z for z in self.E[o.children[q][b]] if self.pay[z][b]<=self.pay[B][a]]
                        assert allowed
                        z=max(allowed,key=lambda z:f[b,z]);ends.append(z);v=min(v,f[b,z])
                    rest,path,ms=dp(o.children[q][a]);opts.append((v+rest,(a,)+path,(tuple(ends),)+ms))
                return max(opts,key=lambda x:x[0])
            val,path,ms=dp(root);gap=val-sum(int(c)*w for c,w in zip(o.cover[B],self.w))
            if gap>best[0]:best=(gap,B,path,ms)
        return best

    def materialize(self,result):
        # Generate all ordered-history nodes; every off-path terminal target is
        # selected within E and its action payoff satisfies the parent's IC.
        o=self.o;_,B,path,menus=result;pi={};leaves={}
        def rec(h,q,target,actual):
            if len(h)==o.m:leaves[h]=q;return
            if actual:
                a=path[len(h)];ends=menus[len(h)]
            else:
                a=next(a for a in range(o.k) if target in self.E[o.children[q][a]] and self.pay[target][a]>=self.floor[q])
                ends=tuple(target if b==a else min(self.E[o.children[q][b]],key=lambda z:self.pay[z][b]) for b in range(o.k))
            pi[h]=a
            for b in range(o.k):rec(h+(b,),o.children[q][b],ends[b],actual and b==a)
            leaves[h]=leaves[h+(a,)]
        rec((),(0,)*o.k,B,True)
        ic=[]
        for h,a in pi.items():
            for b in range(o.k):
                if b!=a:ic.append(o.pay[leaves[h+(b,)]][b]-o.pay[leaves[h]][a])
        mats=[]
        for i,ends in enumerate(menus):
            row=[]
            for a,z in enumerate(ends):
                bg=list(z);bg[a]-=1
                row.append(o.sig.T/(1+o.sig@np.array(bg)))
            mats.append(row)
        return np.array(ic),np.array(mats),o.cover[B],pi

def run(m=5,k=5,tries=80,seed=65421):
    rng=np.random.default_rng(seed);o=Attack(m,k,rng);best=-1e99
    for j in range(tries):
        w=rng.integers(0,15,size=o.d)
        if j%2:w*=rng.random(o.d)<.35
        if not sum(w):continue
        oracle=FullMenu(o,w);p=rng.dirichlet(np.ones(k)*.5)
        for alt in range(5):
            result=oracle.best(p);ic,menus,cover,pi=oracle.materialize(result)
            assert np.max(ic@w)<1e-8
            gap,p=o.p_lp(w,menus,cover)
            if gap>best+1e-9:
                best=gap;print(json.dumps({'iteration':j,'alt':alt,'gap':gap,'path':result[2],'p':p.tolist()}),flush=True)
            if gap>1e-7:
                data={'m':m,'k':k,'w':w.tolist(),'p':p.tolist(),'pi':{' '.join(map(str,q)):a for q,a in pi.items()},'gap':gap,'path':result[2]}
                Path(__file__).with_name('full_candidate.json').write_text(json.dumps(data,indent=2));return
    print(json.dumps({'status':'finite candidate attack ended; no general inference','best':best,'m':m,'k':k,'tries':tries}),flush=True)

if __name__=='__main__':run(*map(int,sys.argv[1:]))
