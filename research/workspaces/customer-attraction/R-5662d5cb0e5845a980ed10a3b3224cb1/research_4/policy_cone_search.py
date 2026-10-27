"""Original-model n=6 policy-cone counterexample attack, numerical discovery.

All policies depend on counts, hence are defined at every ordered history.
No negative numerical run is mathematical evidence for the universal target.
"""
import argparse, json, time
from pathlib import Path
from itertools import combinations
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix

def compositions(n,k):
    if k==1:
        yield (n,); return
    for v in range(n+1):
        for w in compositions(n-v,k-1): yield (v,)+w

class Cone:
    def __init__(self,k=7,m=6):
        self.k,self.m=k,m
        self.bits=np.array([[(b>>j)&1 for b in range(1,1<<k)] for j in range(k)],float)
        self.levels=[[q for q in compositions(t,k)] for t in range(m+1)]
        self.term=self.levels[m]
        self.tidx={q:i for i,q in enumerate(self.term)}
        self.load=np.array(self.term)@self.bits
        self.cover=(self.load>0).astype(float)
        self.U=np.zeros((len(self.term),k,(1<<k)-1))
        for it,q in enumerate(self.term):
            inv=np.divide(1,self.load[it],out=np.zeros_like(self.load[it]),where=self.load[it]>0)
            self.U[it]=self.bits*inv
        # exact optimum objective always first six distinct labels (or all labels if fewer)
        self.opt=(self.bits[:min(m,k)].sum(axis=0)>0).astype(float)
        self.distinct_rows=-np.array([self.bits[i]!=self.bits[j] for i,j in combinations(range(k),2)],float)
        self.distinct_epsilon=0.
        self.states=[q for lv in self.levels[:-1] for q in lv]
        self.sidx={q:i for i,q in enumerate(self.states)}
        self.children={q:[q[:j]+(q[j]+1,)+q[j+1:] for j in range(k)] for q in self.states}

    def policy(self,w,rng,tie=1e-7):
        terminal={q:self.tidx[q] for q in self.term}
        act={}
        profits=self.U@w
        welfare=self.cover@w
        for lv in self.levels[-2::-1]:
            for q in lv:
                kids=self.children[q]
                vals=np.array([profits[terminal[t],j] for j,t in enumerate(kids)])
                cand=np.flatnonzero(vals>=max(vals)-tie)
                # Random choices among exact/near ties expose adjacent cones.
                if rng.random()<.7:
                    wc=np.array([welfare[terminal[kids[j]]] for j in cand])
                    cand=cand[wc<=min(wc)+tie]
                a=int(rng.choice(cand))
                act[q]=a; terminal[q]=terminal[kids[a]]
        return act,terminal

    def optimize(self,act,terminal,side=None,minvalue=None):
        rows=[]
        for q in self.states:
            a=act[q]; prescribed=terminal[q]
            for j,t in enumerate(self.children[q]):
                if j==a:continue
                rows.append(self.U[terminal[t],j]-self.U[prescribed,a])
        root=terminal[(0,)*self.k]
        rhs=np.zeros(len(rows))
        if self.distinct_epsilon:
            rows.extend(self.distinct_rows);rhs=np.append(rhs,np.full(len(self.distinct_rows),-self.distinct_epsilon))
        if minvalue is not None:
            rows.append(-self.opt);rhs=np.append(rhs,-minvalue)
        ans=linprog(-self.opt if side is None else -side,A_ub=csr_matrix(np.array(rows)),b_ub=rhs,
                    A_eq=self.cover[root:root+1],b_eq=[1.],bounds=(0,None),method='highs')
        return ans,root

    def constant_policy(self,a=0):
        act={q:a for q in self.states}
        terminal={q:self.tidx[q] for q in self.term}
        for lv in self.levels[-2::-1]:
            for q in lv:terminal[q]=terminal[self.children[q][a]]
        return act,terminal

    def write_candidate(self,path,w,act,terminal,value):
        root=terminal[(0,)*self.k]
        obj={'k':self.k,'m':self.m,'ratio_comparison':float(value),'terminal':self.term[root],
             'weights':{str(b):float(v) for b,v in enumerate(w,1) if v>1e-12},
             'policy':{','.join(map(str,q)):a for q,a in act.items()}}
        Path(path).write_text(json.dumps(obj,indent=2))

class OrderedCone(Cone):
    """Separate selectors at all ordered histories, including equal-count histories."""
    def __init__(self,k=7,m=6):
        super().__init__(k,m)
        counts=np.zeros((1,k),dtype=np.int16)
        self.ordered_counts=[counts]
        for t in range(m):
            counts=np.repeat(counts,k,axis=0)+np.tile(np.eye(k,dtype=np.int16),(len(counts),1))
            self.ordered_counts.append(counts)
        self.ordered_leaves=np.array([self.tidx[tuple(q)] for q in counts])

    def policy(self,w,rng,tie=1e-7):
        profits=self.U@w; welfare=self.cover@w
        terminal=[None]*(self.m+1);act=[None]*self.m
        terminal[self.m]=self.ordered_leaves
        for t in range(self.m-1,-1,-1):
            kids=terminal[t+1].reshape(-1,self.k)
            vals=profits[kids,np.arange(self.k)[None,:]]
            cand=vals>=np.max(vals,axis=1)[:,None]-tie
            if rng.random()<.7:
                wc=np.where(cand,welfare[kids],np.inf)
                cand &= wc<=np.min(wc,axis=1)[:,None]+tie
            scores=rng.random(cand.shape); scores[~cand]=-1
            act[t]=scores.argmax(axis=1)
            terminal[t]=kids[np.arange(len(kids)),act[t]]
        return act,terminal

    def constant_policy(self,a=0):
        terminal=[None]*(self.m+1);act=[None]*self.m
        terminal[self.m]=self.ordered_leaves
        for t in range(self.m-1,-1,-1):
            kids=terminal[t+1].reshape(-1,self.k)
            act[t]=np.full(len(kids),a,dtype=np.int16)
            terminal[t]=kids[:,a]
        return act,terminal

    def optimize(self,act,terminal,side=None,minvalue=None):
        keys=[]
        for t in range(self.m):
            kids=terminal[t+1].reshape(-1,self.k)
            aa=np.repeat(act[t],self.k)
            src=np.repeat(terminal[t],self.k)
            jj=np.tile(np.arange(self.k),len(kids))
            dst=kids.reshape(-1)
            keys.append(np.array([aa,src,jj,dst]).T[aa!=jj])
        keys=np.unique(np.concatenate(keys),axis=0)
        A=self.U[keys[:,3],keys[:,2]]-self.U[keys[:,1],keys[:,0]]
        root=int(terminal[0][0])
        rhs=np.zeros(len(A))
        if self.distinct_epsilon:
            A=np.vstack([A,self.distinct_rows]);rhs=np.append(rhs,np.full(len(self.distinct_rows),-self.distinct_epsilon))
        if minvalue is not None:
            A=np.vstack([A,-self.opt]);rhs=np.append(rhs,-minvalue)
        ans=linprog(-self.opt if side is None else -side,A_ub=csr_matrix(A),b_ub=rhs,
                    A_eq=self.cover[root:root+1],b_eq=[1.],bounds=(0,None),method='highs')
        return ans,root

    def recompute(self,act):
        terminal=[None]*(self.m+1)
        terminal[self.m]=self.ordered_leaves
        for t in range(self.m-1,-1,-1):
            kids=terminal[t+1].reshape(-1,self.k)
            terminal[t]=kids[np.arange(len(kids)),act[t]]
        return terminal

    def mutated(self,act,rng):
        mutated=[v.copy() for v in act]
        t=int(rng.choice(np.arange(self.m),p=np.array([1,2,3,4,5,5])/20))
        idx=0
        for j in range(t):
            pick=int(act[j][idx])
            if rng.random()<.35: pick=int(rng.integers(self.k))
            idx=idx*self.k+pick
        old=mutated[t][idx]
        new=int(rng.integers(self.k-1));new+=new>=old
        mutated[t][idx]=new
        return mutated,self.recompute(mutated)

    def write_candidate(self,path,w,act,terminal,value):
        root=int(terminal[0][0])
        obj={'k':self.k,'m':self.m,'ratio_comparison':float(value),'terminal':self.term[root],
             'weights':{str(b):float(v) for b,v in enumerate(w,1) if v>1e-12},
             'ordered_policy':{str(t):v.tolist() for t,v in enumerate(act)}}
        Path(path).write_text(json.dumps(obj,indent=2))

def main():
    p=argparse.ArgumentParser();p.add_argument('--k',type=int,default=7);p.add_argument('--steps',type=int,default=50)
    p.add_argument('--seed',type=int,default=1);p.add_argument('--output',default='policy_candidate.json')
    p.add_argument('--ordered',action='store_true')
    p.add_argument('--mutate',action='store_true')
    p.add_argument('--distinct',type=float,default=1e-6,help='minimum positive symmetric-difference mass / on-path welfare')
    a=p.parse_args(); rng=np.random.default_rng(a.seed); C=(OrderedCone if a.ordered else Cone)(a.k)
    C.distinct_epsilon=a.distinct
    best=0.; stale=0; w=rng.exponential(1,size=(1<<a.k)-1)
    curact,curterminal=C.constant_policy(0);curvalue=0.
    for step in range(a.steps):
        if step%10==0:
            # Sparse and highly nonsymmetric starts include pure-private, pair, and dense types.
            w=rng.exponential(1,size=len(w))*(rng.random(len(w))<rng.choice([.1,.3,.6,1]))
            w[rng.integers(len(w))]+=rng.uniform(0,10)
        if a.mutate and step>0:
            act,terminal=C.mutated(curact,rng)
        elif step==0:
            act,terminal=C.constant_policy(0)
        else:
            act,terminal=C.policy(w,rng)
        ans,root=C.optimize(act,terminal)
        if not ans.success:
            print(json.dumps({'step':step,'status':ans.message}),flush=True);w=rng.exponential(1,size=len(w));continue
        v=-ans.fun
        if v>best+1e-8:
            best=v;C.write_candidate(a.output,ans.x,act,terminal,v)
            print(json.dumps({'step':step,'best_ratio':v,'terminal':C.term[root],
                              'support':int(sum(ans.x>1e-9))}),flush=True)
        if v>2+1e-6:
            print('STRICT_TARGET_CANDIDATE',flush=True);break
        if a.mutate:
            temp=.025 if step%60<50 else .15
            if v>=curvalue or rng.random()<np.exp((v-curvalue)/temp):
                curact,curterminal,curvalue=act,terminal,v
            if step%20==0:print(json.dumps({'step':step,'current':curvalue,'trial':v}),flush=True)
            continue
        # Expose nonprivate nearby faces without a blind restart at every iteration.
        if rng.random()<.6:
            side=rng.normal(size=len(w))
            sideans,_=C.optimize(act,terminal,side=side,minvalue=v-rng.choice([1e-7,.01,.1,.3]))
            if sideans.success:
                ans=sideans
        # LP vertex plus sparse random perturbations, with occasional large excursions.
        noise=rng.exponential(1,size=len(w))*(rng.random(len(w))<.1)
        eps=rng.choice([1e-7,1e-5,1e-3,.03,.2])
        w=np.maximum(ans.x,0)+eps*noise
    print(json.dumps({'steps':step+1,'best':best,'k':a.k,'seed':a.seed}),flush=True)

if __name__=='__main__':main()
