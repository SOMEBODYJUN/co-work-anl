"""Float discovery only: search local fractional-security drift cones.

Each policy is a complete count-based BI policy, hence defines an action at every
ordered history. Fixed rational fractional optimizers are imposed by their exact
KKT inequalities, which are linear in customer multiplicities. A float output is
not a counterexample until independent Fraction verification.
"""
from __future__ import annotations
import argparse, json, random, sys, time
from fractions import Fraction
from itertools import combinations_with_replacement
from pathlib import Path
import numpy as np
from scipy.optimize import linprog, minimize

def counts(k, n):
    if k == 1:
        yield (n,); return
    for j in range(n+1):
        for rest in counts(k-1,n-j): yield (j,)+rest

def inc(c,a): return c[:a]+(c[a]+1,)+c[a+1:]

class Engine:
    def __init__(self,k,n,seed):
        self.k,self.n=k,n; self.rng=np.random.default_rng(seed)
        self.masks=np.arange(1,1<<k)
        self.I=((self.masks[None,:]>>np.arange(k)[:,None])&1).astype(float)
        self.layers=[list(counts(k,d)) for d in range(n+1)]
        self.ends=self.layers[n]; self.eid={c:i for i,c in enumerate(self.ends)}
        loads=np.array(self.ends)@self.I
        self.pay=np.divide(self.I[None,:,:],loads[:,None,:],out=np.zeros((len(loads),k,len(self.masks))),where=loads[:,None,:]>0)
        self.cover=(loads>0).astype(float)
    def policy(self,w):
        U=self.pay@w; end={c:self.eid[c] for c in self.ends}; sigma={}
        for layer in reversed(self.layers[:-1]):
            for c in layer:
                es=np.array([end[inc(c,a)] for a in range(self.k)])
                vals=U[es,np.arange(self.k)]; mx=vals.max()
                candidates=np.flatnonzero(vals>mx-1e-8)
                a=int(self.rng.choice(candidates));sigma[c]=a;end[c]=int(es[a])
        rows=[]
        for c,a in sigma.items():
            u=self.pay[end[c],a]
            for b in range(self.k):
                if b!=a:rows.append(u-self.pay[end[inc(c,b)],b])
        gamma=np.unique(np.array(rows),axis=0)
        return sigma,end,gamma
    def fractional(self,w,b,r):
        if r==1:
            vals=self.I@(w/(b+1));q=np.zeros(self.k);q[np.argmax(vals)]=1;return q
        def fun(q): return -np.dot(w,np.log(b+1+(r-1)*(q@self.I)))/(r-1)
        def jac(q): return -(self.I@(w/(b+1+(r-1)*(q@self.I))))
        out=minimize(fun,np.ones(self.k)/self.k,jac=jac,bounds=[(0,1)]*self.k,constraints=[{'type':'eq','fun':lambda q:q.sum()-1,'jac':lambda q:np.ones(self.k)}],method='SLSQP',options={'ftol':1e-12,'maxiter':1000})
        q=np.maximum(out.x,0);q[q<1e-6]=0;q/=q.sum();return q
    def rational(self,q,den):
        qq=[Fraction(float(x)).limit_denominator(den) for x in q]
        total=sum(qq);return [x/total for x in qq]
    def kkt(self,q,b,r):
        qq=np.array(list(map(float,q)));t=qq@self.I
        G=self.I/(b+1+(r-1)*t)
        lam=qq@G
        return lam-G,lam
    def search(self,trials,den,output):
        started=time.time(); log=[];best=0;queue=[]
        root=(0,)*self.k
        for trial in range(trials):
            if queue and trial%3:
                w=queue[int(self.rng.integers(len(queue)))].copy()
                if trial%5==4:w+=self.rng.exponential(.01,len(w))*(self.rng.random(len(w))<.1)
            else:
                w=self.rng.exponential(1,len(self.masks))*(self.rng.random(len(self.masks))<.35)
            w/=w.sum()
            sigma,end,gamma=self.policy(w);a=sigma[root]
            q=self.rational(self.fractional(w,np.zeros(len(w)),self.n),den)
            qq=self.rational(self.fractional(w,self.I[a],self.n-1),den)
            K0,L0=self.kkt(q,np.zeros(len(w)),self.n)
            K1,L1=self.kkt(qq,self.I[a],self.n-1)
            obj=self.pay[end[root],a]+(self.n-1)*L1-self.n*L0
            A=np.vstack([gamma,K0,K1]); out=linprog(obj,A_ub=-A,b_ub=np.zeros(len(A)),A_eq=np.ones((1,len(w))),b_eq=[1],bounds=(0,None),method='highs')
            record={'trial':trial,'value_float':None if not out.success else float(out.fun),'rows':len(gamma),'elapsed':time.time()-started}
            log.append(record)
            if out.success:
                queue.append(out.x)
                if len(queue)>50:queue.pop(0)
                if out.fun<best-1e-9:
                    best=float(out.fun)
                    witness={'policy':{','.join(map(str,c)):a for c,a in sigma.items()},'q0':list(map(str,q)),'q1':list(map(str,qq)),'weights_float':out.x.tolist(),'root_action':a,'root_terminal':self.ends[end[root]],'value_float':best}
                    report={'status':'float discovery only','topics':self.k,'players':self.n,'best':best,'witness':witness,'log':log}
                    output.write_text(json.dumps(report,indent=2)+'\n')
                    print(json.dumps({'best':best,**record}),flush=True)
                    if best < -1e-7:return
            if trial%10==0:print(json.dumps(record),flush=True)
        output.write_text(json.dumps({'status':'finite float search, no theorem','topics':self.k,'players':self.n,'best':best,'log':log},indent=2)+'\n')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--topics',type=int,default=7);ap.add_argument('--players',type=int,default=5);ap.add_argument('--trials',type=int,default=100);ap.add_argument('--denominator',type=int,default=100);ap.add_argument('--seed',type=int,default=41241);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    Engine(args.topics,args.players,args.seed).search(args.trials,args.denominator,args.output)
