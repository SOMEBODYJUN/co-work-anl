"""Exploratory exact integer BI with floating LP safety screening. No finite output proves the bridge."""
import itertools, math, json, sys, time
from pathlib import Path
import numpy as np
from scipy.optimize import linprog


def comps(total,k):
    if k==1:
        yield (total,);return
    for a in range(total+1):
        for tail in comps(total-a,k-1): yield (a,)+tail

class Probe:
    def __init__(self,n,k):
        self.n,self.k=n,k
        self.types=np.arange(1,1<<k)
        self.inc=((self.types[None,:]>>np.arange(k)[:,None])&1)
        self.term=list(comps(n,k));self.tidx={q:i for i,q in enumerate(self.term)}
        self.q=np.array(self.term,dtype=np.int16)
        self.loads=self.q@self.inc
        self.scale=math.lcm(*range(1,n+1))
        self.pay=np.zeros((len(self.term),k,(1<<k)-1),dtype=np.int16)
        for i,q in enumerate(self.term):
            for a in range(k):
                if q[a]: self.pay[i,a]=self.inc[a]*np.where(self.loads[i]>0,self.scale//np.maximum(1,self.loads[i]),0)
        self.cov=self.loads>0
        self.backgrounds=np.array(list(comps(n-1,k)),dtype=np.int16)
        self.security=np.array([self.inc/(1+b@self.inc) for b in self.backgrounds])
        self.states=[list(comps(d,k)) for d in range(n+1)]
        self.children={q:[q[:a]+(q[a]+1,)+q[a+1:] for a in range(k)] for d in range(n) for q in self.states[d]}
    def solve(self,w):
        pay=self.pay@w
        results={q:np.array([i],dtype=np.int32) for i,q in enumerate(self.term)}
        for d in range(self.n-1,-1,-1):
            for q in self.states[d]:
                ch=[results[c] for c in self.children[q]]
                floor=max(pay[cs,a].min() for a,cs in enumerate(ch))
                good=[cs[pay[cs,a]>=floor] for a,cs in enumerate(ch)]
                results[q]=np.unique(np.concatenate(good))
        outcomes=results[(0,)*self.k]
        welfare=self.cov@w
        target=int(outcomes[np.argmin(welfare[outcomes])])
        mat=(self.security@w).T
        lp=linprog(np.r_[np.zeros(self.k),-1.],A_ub=np.c_[-mat.T,np.ones(len(self.backgrounds))],b_ub=np.zeros(len(self.backgrounds)),A_eq=[np.r_[np.ones(self.k),0.]],b_eq=[1.],bounds=[(0,None)]*self.k+[(None,None)],method='highs')
        v=-lp.fun
        return float(welfare[target]/(self.n*v)) if v else 1., target, v, lp.x[:-1], results, pay

if __name__=='__main__':
    n,k,tries=map(int,sys.argv[1:4]);out=Path(sys.argv[4]);rng=np.random.default_rng(20261021)
    p=Probe(n,k); best=2.;t=time.time()
    for i in range(tries):
        # Sparse integer weights deliberately retain meaningful equality faces.
        w=rng.integers(0,6,size=(1<<k)-1)
        w[rng.random(len(w))<.83]=0
        if not w.sum():continue
        ratio,target,v,mix,_,_=p.solve(w)
        if ratio<best-1e-9:
            best=ratio
            data={'iteration':i,'n':n,'k':k,'ratio_W_over_nv':ratio,'v_screen':v,'target':p.term[target],'weights':w.tolist(),'query_screen':mix.tolist()}
            out.write_text(json.dumps(data,indent=2)+'\n')
            print(i,round(best,8),p.term[target],round(v,8),'seconds',round(time.time()-t,2),flush=True)
    print('done',tries,'best',best,'seconds',time.time()-t,flush=True)
