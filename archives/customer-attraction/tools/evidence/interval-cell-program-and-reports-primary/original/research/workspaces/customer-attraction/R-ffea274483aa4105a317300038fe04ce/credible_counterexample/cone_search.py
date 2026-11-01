"""Exploratory complete-continuation cone ascent. Float LP/BI is only discovery.
Every accepted final mathematical example must be rechecked with exact full-history BI.
"""
import argparse,itertools,json,math,random,time
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

def comp(n,k):
    if k==1:
        yield (n,);return
    for j in range(n+1):
        for q in comp(n-j,k-1):yield (j,)+q

class Search:
    def __init__(self,p,m):
        self.p,self.m=p,m;self.scale=math.lcm(*range(1,m+1))
        self.masks=np.arange(1,1<<p);self.bits=((self.masks[:,None]>>np.arange(p))&1).astype(np.int32)
        self.levels=[list(comp(t,p)) for t in range(m+1)]
        self.states=[q for level in self.levels for q in level];self.index={q:i for i,q in enumerate(self.states)}
        self.leaves=self.levels[-1];self.leaf_index={q:i for i,q in enumerate(self.leaves)}
        self.children=[np.array([self.index[q[:a]+(q[a]+1,)+q[a+1:]] for a in range(p)]) for q in self.states[:-len(self.leaves)]]
        self.den=np.array(self.leaves,dtype=np.int32)@self.bits.T
        inv=np.floor_divide(self.scale,self.den,out=np.zeros_like(self.den),where=self.den!=0).astype(np.int32)
        self.pay=inv[:,None,:]*self.bits.T[None,:,:]
        self.cov=(self.den>0).astype(np.int32)
        self.portfolios=list(itertools.combinations(range(p),min(m,p)))
        self.obj=np.array([np.any(self.bits[:,j],axis=1) for j in self.portfolios],dtype=np.int32)
    def solve(self,w):
        self.u=np.einsum('lak,k->la',self.pay,w);self.welfare=self.cov@w
        self.out=[None]*len(self.states);self.floors=np.zeros(len(self.children))
        for q,j in self.leaf_index.items():self.out[self.index[q]]=np.array([j],dtype=np.int32)
        for i in range(len(self.children)-1,-1,-1):
            ch=self.children[i]
            floor=max(np.min(self.u[self.out[t],a]) for a,t in enumerate(ch))
            self.floors[i]=floor
            self.out[i]=np.unique(np.concatenate([self.out[t][self.u[self.out[t],a]>=floor-1e-7] for a,t in enumerate(ch)]))
        root=self.out[0];worst=min(self.welfare[root]);best=self.obj@w
        return max(best)/worst,root[self.welfare[root]<=worst+1e-7],int(np.argmax(best))
    def cone(self,target,rng):
        seen=set();rows=set();route={}
        def rec(i,t):
            if i>=len(self.children) or (i,t) in seen:return
            seen.add((i,t));ch=self.children[i]
            actions=[a for a,j in enumerate(ch) if t in self.out[j] and self.u[t,a]>=self.floors[i]-1e-7]
            a=rng.choice(actions);route[i,t]=a;actual=self.pay[t,a]
            for b,j in enumerate(ch):
                if b==a:s=t
                else:
                    vals=self.u[self.out[j],b];mn=np.min(vals);mins=self.out[j][vals<=mn+1e-7];s=int(rng.choice(mins))
                    row=actual-self.pay[s,b]
                    if np.any(row):rows.add(row.tobytes())
                rec(j,s)
        rec(0,int(target))
        return np.array([np.frombuffer(row,dtype=np.int32) for row in rows]),len(seen),route
    def opt(self,rows,t,obj,noise=None):
        objective=self.obj[obj].astype(float)
        if noise is not None:objective+=noise
        res=linprog(-objective,A_ub=-rows,b_ub=np.zeros(len(rows)),A_eq=self.cov[t][None,:],b_eq=[1],bounds=(0,None),method='highs')
        return res

def seeds(p,m):
    z=np.zeros((1<<p)-1);z[0]=m
    for a in range(1,p):z[(1<<a)-1]=1
    yield z
    d={1:12,2:8,4:4,8:8,1|16:6,1|32:6,4|16:3,4|32:3,1|16|32:6,2|16|32:2,4|16|32:1,8|16|32:2}
    z=np.array([d.get(mask,0) for mask in range(1,1<<p)],float)
    for a in range(6,p):z[(1<<a)-1]=8
    yield z
    d={2:3,4:3,1|8:2,1|16:2,2|8|16:2,4|8|16:2}
    for mul in (m-1,m,2*m):
        d2=d.copy();d2[2|8|16]*=mul;d2[4|8|16]*=mul
        for a in range(5,p):d2[1<<a]=3
        yield np.array([d2.get(mask,0) for mask in range(1,1<<p)],float)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--p',type=int,default=7);ap.add_argument('--m',type=int,default=5);ap.add_argument('--steps',type=int,default=100);ap.add_argument('--seed',type=int,default=8008);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    rng=random.Random(args.seed);s=Search(args.p,args.m);queue=list(seeds(args.p,args.m));seen=set();best=1;records=[];start=time.time()
    step=0
    while queue and step<args.steps:
        w=queue.pop(0);ratio,targets,obj=s.solve(w)
        key=tuple(np.round(w/(sum(w) or 1),7))
        if key in seen:continue
        seen.add(key)
        if ratio>best+1e-8:
            best=ratio;print('best',step,best,flush=True)
            records.append({'step':step,'ratio':float(best),'weights':w.tolist(),'worst':[s.leaves[int(t)] for t in targets]})
            args.output.write_text(json.dumps({'p':args.p,'m':args.m,'records':records,'steps':step,'elapsed':time.time()-start},indent=2))
        for target in rng.sample(list(targets),min(len(targets),3)):
            for variant in range(2):
                rows,nstates,route=s.cone(int(target),rng)
                chosen_obj=obj if variant==0 else rng.randrange(len(s.portfolios))
                res=s.opt(rows,int(target),chosen_obj)
                step+=1
                if res.success:
                    x=res.x;x[x<1e-10]=0
                    score=float(s.obj[chosen_obj]@x)
                    print('lp',step,'rows',len(rows),'pairs',nstates,'ratio',score,flush=True)
                    if score>best+1e-8:
                        records.append({'step':step,'cone_ratio':score,'target':s.leaves[int(target)],'weights':x.tolist(),'min_slack':float(np.min(rows@x))})
                        args.output.write_text(json.dumps({'p':args.p,'m':args.m,'records':records,'steps':step,'elapsed':time.time()-start},indent=2))
                    queue.append(x)
                    # A tiny perturbation visits adjacent continuation cones rather than treating ties canonically.
                    if variant==0:
                        perturb=np.array([rng.random() if xx>1e-8 else 0 for xx in x]);queue.append(x+1e-5*perturb)
                if step>=args.steps:break
            if step>=args.steps:break
    args.output.write_text(json.dumps({'p':args.p,'m':args.m,'records':records,'steps':step,'elapsed':time.time()-start,'max_exploratory_ratio':best,'mathematical_status':'finite floating search; no universal conclusion'},indent=2))
if __name__=='__main__':main()
