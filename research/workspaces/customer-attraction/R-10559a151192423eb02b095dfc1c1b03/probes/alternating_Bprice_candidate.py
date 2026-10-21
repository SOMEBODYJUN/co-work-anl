"""Bounded true-SPE cone/fractional-cover alternation for B(u_i) <= W.

No finite nonseparation proves the bridge. A positive candidate is retained only
after integer clone recovery and every ordered-history deviation is verified.
"""
from pathlib import Path
import argparse, importlib.util, json, random, time, hashlib
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[4]
SRC=ROOT/'research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/counterexample_search/cone_walk.py'
spec=importlib.util.spec_from_file_location('Bprice_engine',SRC)
engine=importlib.util.module_from_spec(spec);spec.loader.exec_module(engine)

def best_z(eng,r,attack,target):
    n=len(r);p=eng.p;u=float(eng.pay[target,attack]@r/eng.L)
    cost=np.r_[np.repeat(u,p),-np.asarray(r)]
    mat=np.c_[-eng.inc.T.astype(float),np.eye(n)]
    out=linprog(cost,A_ub=mat,b_ub=np.zeros(n),bounds=[(0,1)]*(p+n),method='highs')
    if not out.success:return None
    return out.x[:p]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--players',type=int,default=5)
    ap.add_argument('--topics',type=int,default=7);ap.add_argument('--seconds',type=float,default=45)
    ap.add_argument('--steps',type=int,default=150);ap.add_argument('--seed',type=int,default=6920261021)
    ap.add_argument('--min-support',type=int,default=2)
    ap.add_argument('--discount',type=int,default=0);a=ap.parse_args()
    rng=random.Random(a.seed);m,p=a.players,a.topics;eng=engine.Engine(m,p,rng)
    baseline=engine.baseline(m,p);seeds=[baseline];endpoints=[];records=[];seen=set();best=F(-10**9)
    for i in range(30):
        r=np.array(baseline,dtype=float)*rng.choice([1,2,5,10])
        for j in range(rng.randrange(1,11)):
            mask=sum(1<<k for k in rng.sample(range(p),rng.choice([1,2,2,3,min(4,p)])))
            r[mask-1]+=rng.randint(1,15)
        seeds.append(r)
    started=time.monotonic();positive=False
    for step in range(a.steps):
        if time.monotonic()-started>a.seconds:break
        if seeds:r=seeds.pop(0)
        elif endpoints:
            r=np.array(rng.choice(endpoints),dtype=float)*rng.choice([1,3,10])
            for j in range(rng.randrange(1,5)):r[rng.randrange(len(r))]+=rng.random()*.05
        else:break
        eng.solve(r);targets=[int(t) for t in eng.R[0][0] if sum(eng.terminal[t]>0)>=a.min_support]
        if not targets:continue
        # Mix low-welfare and arbitrary multi-action paths to avoid the all-A cone.
        ranked=sorted(targets,key=lambda t:eng.w[t])
        target=rng.choice(ranked[:max(1,len(ranked)//2)])
        acts=[k for k,q in enumerate(eng.terminal[target]) if q]
        attack=min(acts,key=lambda k:eng.u[target,k])
        actions,G=eng.strategy(target);key=hashlib.sha256(repr(actions).encode()).hexdigest()
        if key in seen:continue
        seen.add(key);x=np.array(r,dtype=float)
        for iteration in range(4):
            z=best_z(eng,x,attack,target)
            if z is None:break
            coef=np.minimum(1,eng.inc.T@z)+(a.discount-z.sum())*eng.pay[target,attack]/eng.L-eng.cov[target]
            out=linprog(-coef,A_ub=-G.astype(float),b_ub=np.zeros(len(G)),
                        A_eq=[eng.cov[target].astype(float)],b_eq=[1],bounds=(0,None),method='highs')
            if not out.success:break
            x=out.x;endpoints.append(x.tolist());value=float(coef@x)
            row={'step':step,'iteration':iteration,'target':eng.terminal[target].tolist(),
                 'attacked_topic':attack,'proposal_gap_per_W':value,'fractional_z':z.tolist(),
                 'rows':len(G),'cone_sha256':key};records.append(row)
            if value>float(best)+1e-9:
                clones=eng.exact_recover(G,target,x)
                if clones is None:row['exact_recovery']=False;continue
                inst,cert=engine.verify_canonical(m,p,clones,actions,eng.terminal[target].tolist())
                q=tuple(map(int,eng.terminal[target]));W=inst.welfare(q);u=inst.topic_payoff(attack,q)
                Z=tuple(F(float(t)).limit_denominator(10**6) for t in z)
                coverage=[min(F(1),sum(Z[k] for k in range(p) if mask&(1<<k))) for mask in eng.masks]
                Bz=sum(F(c)*r for c,r in zip(coverage,clones))-sum(Z)*u
                gap=Bz-W+a.discount*u;rate=gap/W;row['exact_gap_per_W']=str(rate)
                if rate>best:
                    best=rate
                    proof={'scope':'one genuine full-history SPE and fixed rational z; B bridge attack only',
                           'parameters':vars(a),'step':step,'attacked_topic':attack,'gap':str(gap),
                           'gap_per_W':str(rate),'u':str(u),'Bz':str(Bz),'W':W,'OPT':inst.optimal_welfare(),
                           'z':[str(t) for t in Z],'instance':inst.to_dict(),'strategy':cert.to_dict(),
                           'all_ordered_histories_verified':True,'cone_sha256':key}
                    suffix='' if a.discount==0 else f'-discount{a.discount}'
                    (BASE/f'agent-independent-attack-Bprice-m{m}p{p}{suffix}.best.json').write_text(json.dumps(proof,indent=2)+'\n')
                    print(json.dumps({'m':m,'p':p,'step':step,'best_gap_per_W':str(best),'elapsed':round(time.monotonic()-started,3)}),flush=True)
                    if gap>0:positive=True;break
        if positive:break
    report={'scope':'bounded sampled true full-history SPE cones; absence of separation proves nothing',
            'parameters':vars(a),'elapsed':time.monotonic()-started,'cones':len(seen),
            'best_gap_per_W':str(best),'separated':positive,'records':records}
    suffix='' if a.discount==0 else f'-discount{a.discount}'
    (BASE/f'agent-independent-attack-Bprice-m{m}p{p}{suffix}.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='records'}),flush=True)

if __name__=='__main__':main()
