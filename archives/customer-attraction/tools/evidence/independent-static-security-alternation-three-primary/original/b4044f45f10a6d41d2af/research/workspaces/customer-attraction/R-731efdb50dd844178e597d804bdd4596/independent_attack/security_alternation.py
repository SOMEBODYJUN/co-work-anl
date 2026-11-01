"""Uncertified alternating LP search for aggregate static-security violations."""
from pathlib import Path
import sys, json, random
from itertools import combinations_with_replacement
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests/audits'))
from customer_attraction import ExactSPESolver, Instance
from customer_attraction_strategy_lp import StrategyCone,instance_from_clones,cone_from_solver
from cone_attack_credible_variants import credible_cone

def table(p,m):
    profiles=list(combinations_with_replacement(range(p),m-1))
    out=np.zeros((len(profiles),p,(1<<p)-1))
    for j,B in enumerate(profiles):
        for a in range(p):
            for mask in range(1,1<<p):
                if mask&(1<<a):out[j,a,mask-1]=1/(1+sum(bool(mask&(1<<b)) for b in B))
    return out

def security(T,w):
    pay=T@w;p=pay.shape[1]
    r=linprog(np.r_[np.zeros(p),-1],A_ub=np.c_[-pay,np.ones(len(pay))],b_ub=np.zeros(len(pay)),A_eq=[np.r_[np.ones(p),0]],b_eq=[1],bounds=[(0,None)]*p+[(None,None)],method='highs')
    assert r.success
    return r.x[:-1],r.x[-1]

def alternate(cone,w,T,steps=12):
    n=len(w);w=w/(np.array(cone.welfare,dtype=float)@w)
    best=None
    for step in range(steps):
        p,v=security(T,w)
        if best is None or v>best[0]:best=(v,w.copy(),p.copy())
        A=np.vstack([np.c_[-cone.matrix,np.zeros(len(cone.rows))],np.c_[-np.einsum('a,jak->jk',p,T),np.ones(len(T))]])
        r=linprog(np.r_[np.zeros(n),-1],A_ub=A,b_ub=np.zeros(len(A)),A_eq=[np.r_[np.array(cone.welfare,dtype=float),0]],b_eq=[1],bounds=[(0,None)]*n+[(None,None)],method='highs')
        if not r.success:break
        w=r.x[:-1]
        if abs(r.x[-1]-v)<1e-10:break
    return best

def main():
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--topics',type=int,default=4);ap.add_argument('--players',type=int,default=3);ap.add_argument('--trials',type=int,default=50);ap.add_argument('--seed',type=int,default=902710);ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();p,m=args.topics,args.players;rng=random.Random(args.seed);T=table(p,m)
    record={'scope':'floating candidate search only','players':m,'topics':p,'seed':args.seed,'trials':[]};best=0
    for trial in range(args.trials):
        w=np.array([rng.randrange(8) if rng.random()<.35 else 0 for _ in range((1<<p)-1)])
        if not any(w):w[0]=1
        if trial==0 and p>=4:
            w*=0;w[1]=4;w[3]=1;w[7]=1;w[12]=2
        instance=instance_from_clones(p,m,tuple(map(int,w)))
        solver=ExactSPESolver(instance);target=rng.choice(sorted(solver.worst_outcomes()))
        cone,_=credible_cone(solver,target,rng,rng.choice(['uniform_credible','max_credible_welfare','min_credible_welfare','max_credible_payoff']))
        ans=alternate(cone,w,T)
        if ans is None:continue
        v,ww,pp=ans;score=m*v
        row={'trial':trial,'m_v_over_W':score,'target':target};record['trials'].append(row)
        if score>best+1e-8:
            best=score;print(json.dumps(row),flush=True)
            record['best']={**row,'weights':ww.tolist(),'query':pp.tolist(),'strategy':[{"history":list(h),"action":a} for h,a in sorted(cone.actions.items())]}
            args.output.write_text(json.dumps(record,indent=2)+'\n')
        if score>1+1e-7:break
    record['completed_trials']=len(record['trials']);args.output.write_text(json.dumps(record,indent=2)+'\n')

if __name__=='__main__':main()
