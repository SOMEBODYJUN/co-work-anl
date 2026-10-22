"""Float discovery in fully specified policies for k group/r anchor gadgets.

Two group columns aggregate k distinct customer types with identical weights.
Every off-path continuation comes from full set-valued backward induction;
the prescribed root path may fail initially, but a feasible cone LP enforces
every node inequality, including all the forced path inequalities.
"""
from pathlib import Path
import argparse, importlib.util, json, math, random, time
import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parents[5]
OLD=ROOT/'research/workspaces/customer-attraction/R-ffea274483aa4105a317300038fe04ce/credible_counterexample/cone_search.py'
spec=importlib.util.spec_from_file_location('old_cone',OLD)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

class AnchorSearch:
    def __init__(self,k,r,individual=False):
        self.k,self.r=k,r;self.p=k*(r+2)+r;self.m=k+r;self.scale=math.lcm(*range(1,self.m+1))
        self.supports=[[(1<<(r+2)*i)*((1<<(r+2))-1) for i in range(k)], [1<<((r+2)*i+1) for i in range(k)]]
        if individual:
            self.supports=[]
            for i in range(k):
                self.supports.extend([[(1<<(r+2)*i)*((1<<(r+2))-1)],[1<<((r+2)*i+1)]])
        for core in range(1,1<<(2*r)):
            mask=0
            for b in range(r):
                if core>>b&1:
                    for i in range(k):mask|=1<<((r+2)*i+2+b)
            for d in range(r):
                if core>>(r+d)&1:mask|=1<<(k*(r+2)+d)
            self.supports.append([mask])
        flat=[z for group in self.supports for z in group];starts=np.cumsum([0]+[len(g) for g in self.supports])
        bits=np.array([[(mask>>a)&1 for a in range(self.p)] for mask in flat],dtype=np.int32)
        self.levels=[list(module.comp(t,self.p)) for t in range(self.m+1)]
        self.states=[q for level in self.levels for q in level];self.index={q:i for i,q in enumerate(self.states)}
        self.leaves=self.levels[-1];self.leaf_index={q:i for i,q in enumerate(self.leaves)}
        self.children=[np.array([self.index[q[:a]+(q[a]+1,)+q[a+1:]] for a in range(self.p)]) for q in self.states[:-len(self.leaves)]]
        den=np.array(self.leaves,dtype=np.int32)@bits.T
        inv=np.floor_divide(self.scale,den,out=np.zeros_like(den),where=den!=0).astype(np.int32)
        raw=inv[:,None,:]*bits.T[None,:,:]
        self.pay=np.stack([raw[:,:,starts[c]:starts[c+1]].sum(axis=2) for c in range(len(self.supports))],axis=2).astype(np.int32)
        self.path=tuple(i*(r+2) for i in range(k))+tuple(range(k*(r+2),self.p))
        target=tuple(self.path.count(a) for a in range(self.p));self.target=self.leaf_index[target]
    def solve(self,w):
        self.u=np.einsum('lak,k->la',self.pay,w)
        self.out=[None]*len(self.states);self.floors=np.zeros(len(self.children))
        for q,j in self.leaf_index.items():self.out[self.index[q]]=np.array([j],dtype=np.int32)
        for i in range(len(self.children)-1,-1,-1):
            ch=self.children[i];floor=max(np.min(self.u[self.out[t],a]) for a,t in enumerate(ch));self.floors[i]=floor
            self.out[i]=np.unique(np.concatenate([self.out[t][self.u[self.out[t],a]>=floor-1e-7] for a,t in enumerate(ch)]))
    def cone(self,rng):
        seen=set();rows=set();routes={}
        pathstates={self.index[tuple(self.path[:j].count(a) for a in range(self.p))]:self.path[j] for j in range(self.m)}
        def rec(i,t,forced):
            if i>=len(self.children) or (i,t,forced) in seen:return
            seen.add((i,t,forced));ch=self.children[i]
            if forced:a=pathstates[i]
            else:
                actions=[a for a,j in enumerate(ch) if t in self.out[j] and self.u[t,a]>=self.floors[i]-1e-7];a=rng.choice(actions)
            routes[i,t,forced]=a;actual=self.pay[t,a]
            for b,j in enumerate(ch):
                if b==a:s=t
                else:
                    vals=self.u[self.out[j],b];mn=np.min(vals);s=int(rng.choice(self.out[j][vals<=mn+1e-7]))
                    row=actual-self.pay[s,b]
                    if np.any(row):rows.add(row.tobytes())
                rec(j,s,forced and b==a)
        rec(0,self.target,True)
        return np.array([np.frombuffer(row,dtype=np.int32) for row in rows]),routes

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--k',type=int,default=2);ap.add_argument('--r',type=int,default=3)
    ap.add_argument('--steps',type=int,default=150);ap.add_argument('--seed',type=int,default=610215)
    ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();rng=random.Random(args.seed)
    search=AnchorSearch(args.k,args.r);n=len(search.supports);best=0;records=[];start=time.time()
    def known_seed():
        w=np.zeros(n);w[0]=2;w[1]=1
        w[2+((1<<0)|(1<<args.r))-1]=1
        w[2+(1<<args.r)-1]=1
        for d in range(1,args.r):w[2+(1<<(args.r+d))-1]=2
        return w
    w=known_seed()
    for step in range(args.steps):
        if step%7==0:
            w=known_seed()*60
            if step:
                for j in range(rng.randrange(2,8)):w[rng.randrange(2,n)]+=rng.randrange(1,10)
        search.solve(w);rows,routes=search.cone(rng)
        objective=np.zeros(n);objective[1]=-1
        if step%3==1:objective[2:]=np.array([rng.random()-.5 for _ in range(n-2)])*1e-5
        res=linprog(objective,A_ub=-rows,b_ub=np.zeros(len(rows)),bounds=[(1,1),(0,5)]+[(0,50)]*(n-2),method='highs')
        if res.success:
            if res.x[1]>best+1e-8:
                best=float(res.x[1]);records.append({'step':step,'a':best,'weights':res.x.tolist(),'rows':len(rows),'policy_objects':len(routes),'min_slack':float(np.min(rows@res.x))})
                print('BEST',step,best,'rows',len(rows),'policy_objects',len(routes),'seconds',time.time()-start,flush=True)
            w=res.x*120
        else:w[rng.randrange(2,n)]+=rng.randrange(1,4)
        if step%5==0:
            args.output.write_text(json.dumps({'k':args.k,'r':args.r,'steps':step,'max_a':best,'records':records,'seconds':time.time()-start,'status':'floating complete-policy cone discovery; no universal conclusion'},indent=2))
            print('STEP',step,'best',best,'seconds',time.time()-start,flush=True)
    args.output.write_text(json.dumps({'k':args.k,'r':args.r,'steps':args.steps,'max_a':best,'records':records,'seconds':time.time()-start,'status':'floating complete-policy cone discovery; no universal conclusion'},indent=2))

if __name__=='__main__':main()
