"""Finite diagnostic of general per-player gap bridge; no universal inference.
Uses old complete-tree Engine only as proposal oracle; exact canonical verification
is mandatory before accepting any bridge counterexample. Writes only this branch.
"""
from pathlib import Path
from fractions import Fraction as F
import sys, random, argparse, json, time, math, hashlib
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/counterexample_search'))
from cone_walk import Engine, baseline, verify_canonical

def recover(G,norm,x,L):
    supp=np.flatnonzero(x>1e-8).tolist(); active=np.flatnonzero(np.abs(G@x)<1e-7)
    basis={}
    for ri,row in enumerate([norm]+[G[j] for j in active]):
        v=[F(int(row[j])) for j in supp]+[F(L if ri==0 else 0)]
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
    for pivot in sorted(basis,reverse=True):sol[pivot]=basis[pivot][-1]-sum(basis[pivot][j]*sol[j] for j in range(pivot+1,len(supp)))
    if min(sol)<0:return None
    scale=math.lcm(*(v.denominator for v in sol));clones=[0]*len(x)
    for j,v in zip(supp,sol):clones[j]=int(v*scale)
    common=math.gcd(*clones);clones=[v//common for v in clones]
    if any(sum(int(row[j])*clones[j] for j in supp)<0 for row in G):return None
    return clones

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--players',type=int,default=4);ap.add_argument('--topics',type=int,default=6);ap.add_argument('--steps',type=int,default=50);ap.add_argument('--seed',type=int,default=231023);args=ap.parse_args()
    rng=random.Random(args.seed);m,p=args.players,args.topics;eng=Engine(m,p,rng);start=time.monotonic();best=F(-10**9);records=[];accepted=0
    seeds=[baseline(m,p)];endpoints=[]
    for _ in range(12):
        rr=baseline(m,p);s=rng.choice([2,5,20]);rr=[s*t for t in rr]
        for _ in range(rng.randrange(1,8)):
            mask=sum(1<<a for a in rng.sample(range(p),rng.randint(2,min(p,5))));rr[mask-1]+=rng.randrange(1,3*s)
        seeds.append(rr)
    for _ in range(20):
        rr=[rng.randrange(1,12) if rng.random()<rng.choice([.1,.3,.6]) else 0 for _ in eng.masks]
        if sum(rr):seeds.append(rr)
    seen=set()
    for step in range(args.steps):
        if seeds:rr=seeds.pop(0)
        elif endpoints:
            rr=[v*rng.choice([1,5,20]) for v in rng.choice(endpoints)]
            for _ in range(rng.randrange(1,4)):rr[rng.randrange(len(rr))]+=rng.random()*.1
        else:break
        eng.solve(rr);out=eng.R[0][0];O=max(eng.v@np.array(rr))
        vals=[]
        for target in out:
            occupied=np.flatnonzero(eng.terminal[target]);amin=min(occupied,key=lambda a:eng.u[target,a]);den=eng.u[target,amin]
            vals.append(((O-eng.w[target])/max(den,1e-30),int(target),int(amin)))
        vals.sort(reverse=True)
        if step%5==4:_,target,a=rng.choice(vals[:max(1,len(vals)//2)])
        else:_,target,a=vals[0]
        actions,G=eng.strategy(target);key=hashlib.sha256(repr(actions).encode()).hexdigest()
        if key in seen:continue
        seen.add(key)
        norm=eng.pay[target,a];W=eng.cov[target]
        js=list(dict.fromkeys([int(np.argmax(eng.v@np.array(rr))),rng.randrange(len(eng.portfolios))]))
        for jid in js:
            obj=eng.v[jid].astype(float)-W
            lp=linprog(-obj,A_ub=-G.astype(float),b_ub=np.zeros(len(G)),A_eq=[norm.astype(float)],b_eq=[eng.L],bounds=(0,None),method='highs')
            if not lp.success:continue
            proposal=float(obj@lp.x);endpoints.append(lp.x.tolist())
            record={'step':step,'a':a,'proposal_gap_over_ui':proposal,'threshold':m,'portfolio':eng.portfolios[jid],'cone_rows':len(G),'cone_sha256':key}
            records.append(record)
            if proposal>float(best)+1e-8:
                clones=recover(G,norm,lp.x,eng.L)
                if clones is None:continue
                inst,cert=verify_canonical(m,p,clones,actions,eng.terminal[target].tolist());q=tuple(map(int,eng.terminal[target]));u=inst.topic_payoff(a,q);w=inst.welfare(q);opt=inst.optimal_welfare();value=F(opt-w,u)
                accepted+=1
                if value>best:
                    best=value;proof={'scope':'one exact complete-history pure SPE; auxiliary bridge diagnostic only','parameters':vars(args),'gap_over_ui':str(value),'threshold':m,'a':a,'u':str(u),'W':w,'OPT':opt,'instance':inst.to_dict(),'strategy':cert.to_dict(),'canonical_verified':True,'cone_sha256':key}
                    (HERE/f'gap_n{m}p{p}_best.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps({'step':step,'best_exact_gap_over_ui':str(best),'threshold':m,'elapsed':round(time.monotonic()-start,2)}),flush=True)
                    if value>m:
                        records.append({'genuine_auxiliary_counterexample':True});break
        report={'scope':'finite policy-cone diagnostic, no universal conclusion','parameters':vars(args),'best_exact_gap_over_ui':str(best),'accepted_exact_improvements':accepted,'distinct_complete_policies':len(seen),'elapsed':time.monotonic()-start,'records':records}
        (HERE/f'gap_n{m}p{p}_run.json').write_text(json.dumps(report,indent=2)+'\n')
        if best>m:break
        if step%10==0:print(json.dumps({'step':step,'policies':len(seen),'best':str(best),'elapsed':round(time.monotonic()-start,2)}),flush=True)
if __name__=='__main__':main()
