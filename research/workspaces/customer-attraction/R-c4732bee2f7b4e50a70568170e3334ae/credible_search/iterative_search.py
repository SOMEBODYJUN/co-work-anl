"""Numerical BI / credible full strategy / multiplicity LP policy iteration.
Float search is never a proof. A saved selected policy is rebuilt by the canonical
Fraction cone optimizer and complete certificate verifier before a ratio is claimed.
"""
from __future__ import annotations
import sys,json,time,argparse,random
from pathlib import Path
from itertools import product,combinations
import numpy as np
from scipy.optimize import linprog
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'customer_attraction/__init__.py').is_file())
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests/audits'))
from customer_attraction import StrategyCertificate
from customer_attraction_strategy_lp import StrategyCone,serializable
from cone_attack_credible_variants import exact_export

def countvec(p,total):
    if p==1:yield (total,);return
    for j in range(total+1):
        for q in countvec(p-1,total-j):yield (j,)+q

def inc(q,a):return q[:a]+(q[a]+1,)+q[a+1:]
class Search:
    def __init__(self,p,m,seed):
        self.p=p;self.m=m;self.rng=random.Random(seed);self.masks=np.arange(1,1<<p)
        self.I=((self.masks[:,None]>>np.arange(p))&1).astype(float)
        self.Q=tuple(countvec(p,m));self.qindex={q:i for i,q in enumerate(self.Q)}
        den=np.array(self.Q)@self.I.T
        self.pay=np.divide(self.I.T[None,:,:],den[:,None,:],out=np.zeros((len(self.Q),p,len(self.masks))),where=den[:,None,:]>0)
        self.pay*= (np.array(self.Q)>0)[:,:,None]
        self.w=(den>0).astype(float)
        self.Js=list(combinations(range(p),min(p,m)))
        self.v=np.array([self.I[:,J].any(axis=1).astype(float) for J in self.Js])
        self.states=tuple(q for d in range(m,-1,-1) for q in countvec(p,d))
        self.root=(0,)*p
    def solve(self,r):
        self.U=self.pay@r;self.W=self.w@r;self.R={};self.floor={}
        for k in self.states:
            if sum(k)==self.m:self.R[k]=np.array([self.qindex[k]],dtype=int)
            else:
                children=[self.R[inc(k,a)] for a in range(self.p)]
                floor=max(self.U[ch,a].min() for a,ch in enumerate(children));self.floor[k]=floor
                self.R[k]=np.unique(np.concatenate([ch[self.U[ch,a]>=floor-1e-8] for a,ch in enumerate(children)]))
        outcomes=self.R[self.root];target=int(outcomes[np.argmin(self.W[outcomes])]);opt=self.v@r
        return float(opt.max()/self.W[target]),target,int(opt.argmax())
    def policy(self,target,mode):
        actions={};terms={}
        def expand(h,k,t):
            if len(h)==self.m:terms[h]=t;return
            choices=[a for a in range(self.p) if t in self.R[inc(k,a)] and self.U[t,a]>=self.floor[k]-1e-8]
            a=self.rng.choice(choices);actions[h]=a;terms[h]=t;actual=self.U[t,a]
            for b in range(self.p):
                child=inc(k,b)
                if b==a:dest=t
                else:
                    menu=self.R[child][self.U[self.R[child],b]<=actual+1e-8]
                    if mode=='min':menu=menu[self.U[menu,b]<=self.U[menu,b].min()+1e-8]
                    elif mode=='max':menu=menu[self.U[menu,b]>=self.U[menu,b].max()-1e-8]
                    elif mode=='lowW':menu=menu[self.W[menu]<=self.W[menu].min()+1e-8]
                    elif mode=='highW':menu=menu[self.W[menu]>=self.W[menu].max()-1e-8]
                    dest=int(self.rng.choice(list(menu)))
                expand(h+(b,),child,dest)
        expand((),self.root,target)
        keys={(terms[h],a,terms[h+(b,)],b) for h,a in actions.items() for b in range(self.p) if b!=a}
        matrix=np.unique(np.array([self.pay[t,a]-self.pay[d,b] for t,a,d,b in keys]),axis=0)
        return actions,matrix
    def optimize(self,A,target,j):
        out=linprog(-self.v[j],A_ub=-A,b_ub=np.zeros(len(A)),A_eq=self.w[[target]],b_eq=[1],bounds=(0,None),method='highs')
        return out

def seeds(p,m):
    n=(1<<p)-1
    big=np.zeros(n);big[0]=m
    for a in range(1,p):big[(1<<a)-1]=1
    yield 'big',big
    for label,weights in [('reply',{2:1,4:1,8:1,9:1,16:1,17:2,26:1,28:1}),('overlap',{1:10,2:4,4:8,6:2,8:16,12:1,16:32,17:1,24:2})]:
        r=np.zeros(n)
        for mask,c in weights.items():r[mask-1]=c
        for a in range(5,p):r[(1<<a)-1]=1
        yield label,r

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--topics',type=int,default=7);ap.add_argument('--players',type=int,default=5);ap.add_argument('--rounds',type=int,default=20);ap.add_argument('--seed',type=int,default=20261021);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    s=Search(args.topics,args.players,args.seed);queue=list(seeds(args.topics,args.players));log=[];best=0;seen=set();started=time.monotonic();best_record=None
    for it in range(args.rounds):
        label,r=queue[it%len(queue)] if it<len(queue) else s.rng.choice(queue)
        # Sparse integer perturbations leave the exact boundary, allowing new cones.
        if it>=3 and it%4==3:
            r=r.copy()
            for _ in range(3):r[s.rng.randrange(len(r))]+=s.rng.choice([.01,.05,.2])*max(r.max(),1)
        ratio,target,j=s.solve(r)
        mode=['min','max','lowW','highW','uniform'][it%5]
        actions,A=s.policy(target,mode)
        digest=hash(tuple(sorted(actions.items())))
        if digest in seen:continue
        seen.add(digest)
        Js=list(dict.fromkeys([j]+s.rng.sample(range(len(s.Js)),min(3,len(s.Js)))))
        local=None
        for jj in Js:
            out=s.optimize(A,target,jj)
            if out.success and (local is None or -out.fun>-local[0].fun):local=(out,jj)
        if local is None:continue
        out,jj=local;value=-out.fun
        queue.append((f'LP{it}',out.x))
        record={'iteration':it,'source':label,'mode':mode,'seed_ratio_float':ratio,'LP_float':value,'rows':len(A),'portfolio':s.Js[jj],'elapsed':time.monotonic()-started}
        log.append(record);print(json.dumps(record),flush=True)
        if value>best+1e-8:
            cone=StrategyCone(s.p,s.m,actions);exact=cone.optimize(s.Js[jj])
            if exact['certified']:
                proof=exact_export(cone,exact);record['ratio_exact']=str(proof['ratio'])
                best=float(proof['ratio']);best_record={'strategy':StrategyCertificate(cone.actions,cone.root).to_dict(),'root_counts':cone.root,'portfolio_proofs':[proof]}
        report={'scope':'finite float-guided complete SPE strategy iteration; selected exact full certificates','seed':args.seed,'universal_bound_proved':False,'log':log,'batches':([] if best_record is None else [{'topics':s.p,'players':s.m,'cone_proofs':[best_record]}])}
        args.output.write_text(json.dumps(serializable(report),indent=2)+'\n')
