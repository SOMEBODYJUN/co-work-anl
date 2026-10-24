"""Attack only the fresh-menu aggregate candidate, never infer a theorem from no hit.

Fixed anonymous count policy is a full ordered-history policy by lifting counts.
Every nonterminal count-state IC is imposed in the weight LP. The query p LP
retains independent minimization of each actual-prefix menu column.
"""
from itertools import product
from pathlib import Path
import json, math, sys
import numpy as np
from scipy.optimize import linprog

def comp(n,k):
    if k==1:
        yield (n,);return
    for j in range(n+1):
        for t in comp(n-j,k-1):yield (j,)+t

class Attack:
    def __init__(self,m,k,rng):
        self.m,self.k,self.rng=m,k,rng
        self.sig=np.array([[int(s>>a&1) for a in range(k)] for s in range(1,1<<k)])
        self.d=len(self.sig)
        self.states=[q for n in range(m+1) for q in comp(n,k)]
        self.qid={q:j for j,q in enumerate(self.states)}
        self.children={q:[q[:a]+(q[a]+1,)+q[a+1:] for a in range(k)] for q in self.states if sum(q)<m}
        self.terminal=[q for q in self.states if sum(q)==m]
        self.pay={}
        self.cover={}
        for q in self.terminal:
            load=self.sig@np.array(q)
            self.pay[q]=np.divide(self.sig.T,load,out=np.zeros((k,self.d)),where=load>0)
            self.cover[q]=(load>0).astype(float)

    def policy(self,w):
        tail={q:q for q in self.terminal};pi={}
        for q in reversed(self.states):
            if sum(q)==self.m:continue
            leaves=[tail[x] for x in self.children[q]]
            us=np.array([self.pay[leaves[a]][a]@w for a in range(self.k)])
            # Distinct random tie choices allowed at every count state.
            opts=np.flatnonzero(us>=max(us)-1e-10)
            a=int(self.rng.choice(opts));pi[q]=a;tail[q]=leaves[a]
        return pi,tail

    def matrices(self,pi,tail):
        ic=[]
        for q in self.children:
            act=pi[q];base=self.pay[tail[q]][act]
            for a in range(self.k):
                if a!=act:ic.append(self.pay[tail[self.children[q][a]]][a]-base)
        q=(0,)*self.k;path=[];menus=[]
        for i in range(self.m):
            path.append(pi[q]);mats=[]
            for a in range(self.k):
                end=list(tail[self.children[q][a]]);end[a]-=1
                load=1+self.sig@np.array(end)
                mats.append(self.sig.T/load)
            menus.append(mats);q=self.children[q][pi[q]]
        return np.array(ic),np.array(menus),self.cover[tail[(0,)*self.k]],path

    def p_lp(self,w,menus,cover):
        # vars p_k,t_m, objective max sum t - W; W is fixed.
        mat=np.zeros((self.m*self.k,self.k+self.m))
        for i in range(self.m):
            for a in range(self.k):
                mat[i*self.k+a,:self.k]=-(menus[i,a]@w)
                mat[i*self.k+a,self.k+i]=1
        obj=np.r_[np.zeros(self.k),-np.ones(self.m)]
        eq=np.zeros((1,self.k+self.m));eq[0,:self.k]=1
        r=linprog(obj,A_ub=mat,b_ub=np.zeros(len(mat)),A_eq=eq,b_eq=[1],bounds=[(0,None)]*(self.k+self.m),method='highs')
        assert r.success,r.message
        return -r.fun-cover@w,r.x[:self.k]

    def w_lp(self,p,ic,menus,cover):
        mat=np.zeros((len(ic)+self.m*self.k,self.d+self.m));mat[:len(ic),:self.d]=ic
        for i in range(self.m):
            for a in range(self.k):
                j=len(ic)+i*self.k+a
                mat[j,:self.d]=-(p@menus[i,a]);mat[j,self.d+i]=1
        obj=np.r_[cover,-np.ones(self.m)]
        eq=np.zeros((1,self.d+self.m));eq[0,:self.d]=1
        r=linprog(obj,A_ub=mat,b_ub=np.zeros(len(mat)),A_eq=eq,b_eq=[1],bounds=[(0,None)]*(self.d-1)+[(0,0)]+[(0,None)]*self.m,method='highs')
        assert r.success,r.message
        return -r.fun,r.x[:self.d]

def run(m=5,k=5,tries=200,seed=2861):
    rng=np.random.default_rng(seed);o=Attack(m,k,rng);best=-1
    for it in range(tries):
        # Each attempt searches one fixed original-class policy cone.
        w=rng.integers(0,20,size=o.d).astype(float)
        if it%3==0:w*=rng.random(o.d)<.35
        w/=sum(w)
        pi,tail=o.policy(w);ic,menus,cover,path=o.matrices(pi,tail)
        gap,p=o.p_lp(w,menus,cover)
        if it%2:p=rng.dirichlet(np.ones(k)*.4)
        for alt in range(12):
            old=gap;gap,w=o.w_lp(p,ic,menus,cover);gap,p=o.p_lp(w,menus,cover)
            if gap<=old+1e-10:break
        if gap>best+1e-10:
            best=gap;print(json.dumps({'iteration':it,'gap':gap,'path':path,'p':p.tolist()}),flush=True)
        if gap>1e-8:
            data={'m':m,'k':k,'w':w.tolist(),'p':p.tolist(),'pi':{' '.join(map(str,q)):a for q,a in pi.items()},'gap':gap,'path':path}
            Path(__file__).with_name('candidate.json').write_text(json.dumps(data,indent=2));return
    print(json.dumps({'status':'finite attack completed, no counterexample; no general conclusion','best':best,'m':m,'k':k,'tries':tries}),flush=True)

if __name__=='__main__':run(*map(int,sys.argv[1:]))
