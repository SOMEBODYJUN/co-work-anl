"""Targeted complete-history SPE-cone face walk; floats only propose, exact rows certify.

Uses the canonical all-SPE recurrence, integer LCM-scaled utility coefficients,
and unmerged ordered-history strategy reconstruction. Only this workspace writes.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, math, random, sys, time
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
sys.path.insert(0,str(ROOT))
from customer_attraction import Instance,CustomerType,ExactSPESolver

def compositions(n,p):
    if p==1:
        yield (n,); return
    for a in range(n+1):
        for rest in compositions(n-a,p-1): yield (a,)+rest

class Engine:
    def __init__(self,m,p,rng,masks=None):
        self.m,self.p,self.rng=m,p,rng
        self.L=math.lcm(*range(1,m+1))
        self.states=[list(compositions(t,p)) for t in range(m+1)]
        self.index=[{q:i for i,q in enumerate(level)} for level in self.states]
        self.children=[]
        for t in range(m):
            self.children.append(np.array([[self.index[t+1][tuple(v+int(j==a) for j,v in enumerate(q))] for a in range(p)] for q in self.states[t]],dtype=np.int32))
        self.terminal=np.array(self.states[m],dtype=np.int16)
        self.masks=np.arange(1,1<<p) if masks is None else np.array(masks,dtype=np.int32)
        self.inc=((self.masks[None,:]>>np.arange(p)[:,None])&1).astype(np.int16)
        den=self.terminal@self.inc
        self.pay=np.zeros((len(den),p,len(self.masks)),dtype=np.int16)
        for a in range(p):
            self.pay[:,a,:]=np.where((self.inc[a]>0)&(den>0),self.L//np.maximum(den,1),0)
        self.cov=(den>0).astype(np.int16)
        self.portfolios=list(itertools.combinations(range(p),min(p,m)))
        self.v=np.array([(np.any(self.inc[list(J)],axis=0)).astype(np.int16) for J in self.portfolios])

    def solve(self,r,diverse=False):
        # Float proposal oracle only. Actual resulting strategies are certified below.
        r=np.asarray(r,dtype=float)
        self.u=np.einsum('tam,m->ta',self.pay,r)
        self.w=self.cov@r
        self.R=[None]*self.m+[[np.array([i],dtype=np.int32) for i in range(len(self.terminal))]]
        self.floor=[None]*self.m
        eps=max(1.,float(r.sum()))*1e-10
        self.eps=eps
        for t in range(self.m-1,-1,-1):
            sets=[]; floors=[]
            for childids in self.children[t]:
                child=[self.R[t+1][j] for j in childids]
                floor=max(float(self.u[C,a].min()) for a,C in enumerate(child))
                result=np.unique(np.concatenate([C[self.u[C,a]>=floor-eps] for a,C in enumerate(child)]))
                assert len(result)
                sets.append(result);floors.append(floor)
            self.R[t]=sets;self.floor[t]=floors
        outcomes=self.R[0][0]
        minimum=self.w[outcomes].min()
        worst=outcomes[self.w[outcomes]<=minimum+eps]
        if diverse:
            rich=outcomes[np.sum(self.terminal[outcomes]>0,axis=1)>=2]
            if len(rich):
                # Mix low welfare roots with random feasible multitheme roots.
                rich=rich[np.argsort(self.w[rich])[:max(5,len(rich)//2)]]
                worst=rich
        target=int(self.rng.choice(list(worst)))
        return target, float(max(self.v@r)/max(minimum,1e-30))

    def strategy(self,target):
        actions=[]; terms=[]; rows=[]
        def rec(h,t,sid,target):
            if t==self.m:return target
            childids=self.children[t][sid]
            admissible=[a for a,cid in enumerate(childids) if target in self.R[t+1][cid] and self.u[target,a]>=self.floor[t][sid]-self.eps]
            chosen=self.rng.choice(admissible)
            record=len(actions); actions.append((h,chosen)); terms.append(None)
            childterms=[]
            for a,cid in enumerate(childids):
                if a==chosen:dest=target
                else:
                    C=self.R[t+1][cid];vals=self.u[C,a];mini=vals.min()
                    dest=int(self.rng.choice(list(C[vals<=mini+self.eps])))
                childterms.append(rec(h+(a,),t+1,int(cid),dest))
            actual=childterms[chosen]
            terms[record]=actual
            for a,dest in enumerate(childterms):
                if a!=chosen: rows.append(self.pay[actual,chosen]-self.pay[dest,a])
            return actual
        rec((),0,0,target)
        G=np.unique(np.array(rows,dtype=np.int16),axis=0)
        G=G[np.any(G!=0,axis=1)]
        return actions,G

    def optimize(self,target,G,Jid,noise=0):
        welfare=self.cov[target]
        objective=self.v[Jid].astype(float)+noise*np.array([self.rng.uniform(-1,1) for _ in self.masks])
        res=linprog(-objective,A_ub=-G.astype(float),b_ub=np.zeros(len(G)),A_eq=[welfare.astype(float)],b_eq=[1.],bounds=(0,None),method='highs')
        if not res.success:return None
        return res.x,float(self.v[Jid]@res.x)

    def exact_recover(self,G,target,x):
        supp=np.flatnonzero(x>1e-8).tolist()
        base=self.cov[target]
        active=np.flatnonzero(np.abs(G@x)<1e-7)
        candidates=[base]+[G[j] for j in active]
        basis={}
        for ri,row in enumerate(candidates):
            v=[F(int(row[j])) for j in supp]+[F(ri==0)]
            for pivot in sorted(basis):
                z=v[pivot]
                if z:v=[a-z*b for a,b in zip(v,basis[pivot])]
            pivot=next((j for j,z in enumerate(v[:-1]) if z),None)
            if pivot is not None:
                z=v[pivot];basis[pivot]=[a/z for a in v]
            elif v[-1]:return None
            if len(basis)==len(supp):break
        if len(basis)!=len(supp):return None
        sol=[F(0)]*len(supp)
        for pivot in sorted(basis,reverse=True):
            sol[pivot]=basis[pivot][-1]-sum(basis[pivot][j]*sol[j] for j in range(pivot+1,len(supp)))
        if min(sol)<0:return None
        scale=math.lcm(*(v.denominator for v in sol))
        clones=[0]*len(x)
        for j,v in zip(supp,sol):clones[j]=int(v*scale)
        common=math.gcd(*clones);clones=[v//common for v in clones]
        # Exact integer row arithmetic, no numpy integer overflow.
        if any(sum(int(row[j])*clones[j] for j in supp)<0 for row in G):return None
        return clones

def baseline(m,p):
    r=[0]*((1<<p)-1);r[0]=m
    for a in range(1,p):r[(1<<a)-1]=1
    return r

def verify_canonical(m,p,clones,actions,target):
    from customer_attraction import StrategyCertificate,verify_certificate
    inst=Instance(tuple(map(str,range(p))),tuple(CustomerType(frozenset(a for a in range(p) if mask&(1<<a)),n) for mask,n in enumerate(clones,1) if n),m)
    cert=StrategyCertificate(dict(actions),tuple(target))
    report=verify_certificate(inst,cert)
    if not report.valid:raise AssertionError(str(report))
    return inst,cert

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--players',type=int,default=5);ap.add_argument('--topics',type=int,default=7);ap.add_argument('--steps',type=int,default=100);ap.add_argument('--seed',type=int,default=182026);ap.add_argument('--diverse',action='store_true');ap.add_argument('--out',default='walk_m5p7');args=ap.parse_args()
    rng=random.Random(args.seed);eng=Engine(args.players,args.topics,rng);start=time.monotonic()
    seeds=[baseline(args.players,args.topics)]
    # Layered overlaps perturb the concentrated equilibrium, instead of broad random input sweep.
    for j in range(14):
        r=baseline(args.players,args.topics);scale=rng.choice([2,5,10]);r=[scale*v for v in r]
        for k in range(rng.randrange(2,8)):
            mask=sum(1<<a for a in rng.sample(range(args.topics),rng.choice([2,2,3,4])))
            r[mask-1]+=rng.randrange(1,2*scale+1)
        seeds.append(r)
    best=F(0);seen=set();records=[];endpoints=[]
    for step in range(args.steps):
        if seeds:r=seeds.pop(0)
        elif endpoints:
            r=list(rng.choice(endpoints))
            # Face crossing: tiny positive clones at absent or present incidence types.
            scale=rng.choice([5,20,100]);r=[float(v)*scale for v in r]
            for k in range(rng.randrange(1,4)):
                j=rng.randrange(len(r));r[j]+=rng.random()*.2
        else:break
        target,inputratio=eng.solve(r,diverse=args.diverse and rng.random()<.85)
        actions,G=eng.strategy(target)
        key=hashlib.sha256(repr(actions).encode()).hexdigest()
        if key in seen:continue
        seen.add(key)
        current=eng.v@np.array(r,dtype=float)
        Jids=list(dict.fromkeys([int(np.argmax(current)),rng.randrange(len(eng.portfolios))]))
        for jid in Jids:
            result=eng.optimize(target,G,jid,noise=.002 if args.diverse and rng.random()<.5 else 0)
            if result is None:continue
            x,value=result
            endpoints.append(x.tolist())
            records.append({'step':step,'target':eng.terminal[target].tolist(),'rows':len(G),'input_ratio_proposal':inputratio,'optimized_ratio_proposal':value,'portfolio':eng.portfolios[jid],'cone_sha256':key})
            if value>float(best)+1e-9:
                clones=eng.exact_recover(G,target,x)
                if clones is None:
                    print(json.dumps({'step':step,'unrecovered_proposal':value}),flush=True);continue
                inst,cert=verify_canonical(args.players,args.topics,clones,actions,eng.terminal[target].tolist())
                ratio=F(inst.optimal_welfare(),inst.welfare(tuple(map(int,eng.terminal[target]))))
                if ratio>best:
                    best=ratio
                    proof={'seed':args.seed,'step':step,'players':args.players,'topics':args.topics,'ratio':str(ratio),'instance':inst.to_dict(),'strategy':cert.to_dict(),'canonical_full_history_verified':True,'lp_optimized_portfolio':eng.portfolios[jid],'cone_sha256':key,'scope':'one actual full-history pure SPE; not a universal result'}
                    (HERE/(args.out+'_best.json')).write_text(json.dumps(proof,indent=2)+'\n')
                    print(json.dumps({'step':step,'new_exact_best':str(best),'rows':len(G),'support':sum(v>0 for v in clones),'elapsed':round(time.monotonic()-start,2)}),flush=True)
            if value>float(2*args.players-1)/args.players-1e-8 and rng.random()<.7:
                seeds.append(x.tolist())
        if step%10==0:
            report={'parameters':vars(args),'best_exact_ratio':str(best),'finite_cones':len(seen),'records':records,'elapsed':round(time.monotonic()-start,3),'limitation':'No finite search proves universal half coverage; float proposals recorded separately.'}
            (HERE/(args.out+'_run.json')).write_text(json.dumps(report,indent=2)+'\n')
            print(json.dumps({'step':step,'cones':len(seen),'best':str(best),'elapsed':round(time.monotonic()-start,2)}),flush=True)
    report={'parameters':vars(args),'best_exact_ratio':str(best),'finite_cones':len(seen),'records':records,'elapsed':round(time.monotonic()-start,3),'limitation':'No finite search proves universal half coverage; float proposals recorded separately.'}
    (HERE/(args.out+'_run.json')).write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
