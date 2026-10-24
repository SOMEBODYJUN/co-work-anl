"""Targeted falsification of general ADM only. Float LP is discovery, never a proof."""
import sys, json, argparse, random
from pathlib import Path
from fractions import Fraction
from itertools import product
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[6]
sys.path.insert(0,str(ROOT))
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver


def ins(ins,c):
    out=[Fraction(0) for _ in ins.topics]
    for typ in ins.customers:
        share=Fraction(typ.multiplicity,1+sum(c[a] for a in typ.topics))
        for a in typ.topics:out[a]+=share
    return out


def adm(ins,solver,path):
    z=ins.counts(path,terminal=True); ui=ins.player_payoffs(path)
    D=set();q=[0]*ins.topic_count
    for i,a0 in enumerate(path):
        for a in range(ins.topic_count):
            qa=q.copy();qa[a]+=1
            D.update(y for y in solver.outcomes(qa) if ins.topic_payoff(a,y)<=ui[i])
        q[a0]+=1
    D=sorted(D); K=np.array([[float(v) for v in insv] for insv in [ins_(ins,c) for c in D]])
    res=linprog([0]*ins.topic_count+[-1],A_ub=np.column_stack([-K,np.ones(len(D))]),b_ub=np.zeros(len(D)),A_eq=[[1]*ins.topic_count+[0]],b_eq=[1],bounds=[(0,None)]*ins.topic_count+[(None,None)],method='highs')
    assert res.success
    return -res.fun,D,res.x[:-1]
ins_=ins


def check(ins,name,rng,lim):
    solver=ExactSPESolver(ins); outs=solver.outcomes(); candidates=[]
    for z in outs:
        w=ins.welfare(z); k=ins_(ins,z)
        gap=float(max(k))-w/ins.players
        if gap>1e-8:candidates.append((gap,z))
    candidates.sort(reverse=True)
    best=None;checked=0
    for _,z in candidates[:lim]:
        paths=list(solver.ordered_outcomes(z)); rng.shuffle(paths)
        for path in paths[:max(1,lim//2)]:
            value,D,p=adm(ins,solver,path);w=ins.welfare(z); gap=value-w/ins.players
            checked+=1
            if best is None or gap>best['gap']:
                best=dict(name=name,gap=gap,value=value,W=w,m=ins.players,path=path,p=p.tolist(),Dsize=len(D),outcomes=len(outs),instance=ins.to_dict())
            if gap>1e-7:return best,checked
    return best,checked


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--random',type=int,default=0);ap.add_argument('--seed',type=int,default=7351);ap.add_argument('--limit',type=int,default=8);ap.add_argument('--output',required=True);a=ap.parse_args();rng=random.Random(a.seed)
    records=[];checked=0
    files=sorted((ROOT/'examples/customer_attraction').glob('*.json'))
    for f in files:
        try:ins=Instance.from_dict(json.loads(f.read_text()))
        except Exception:continue
        if ins.players>8 or ins.topic_count>8:continue
        best,n=check(ins,f.name,rng,a.limit);checked+=n
        if best is not None:records.append(best)
        print(f.name, None if best is None else best['gap'], flush=True)
        if best is not None and best['gap']>1e-7:break
    else:
        for k in range(a.random):
            # General ADM has unrestricted input class; these are only potential counterexample seeds.
            q=rng.choice([4,5,6]);m=rng.choice([3,4,5,6])
            types=[]
            for mask in range(1,1<<q):
                w=rng.choices([0,1,2,3,5,10,20],[12,5,3,2,2,1,1])[0]
                if w:types.append(CustomerType(frozenset(i for i in range(q) if mask>>i&1),w))
            ins=Instance(tuple(map(str,range(q))),tuple(types),m)
            best,n=check(ins,f'random-{k}',rng,a.limit);checked+=n
            if best is not None:records.append(best)
            if k%25==0:print('random',k,'checked',checked,'best',max((r['gap'] for r in records),default=None),flush=True)
            if best is not None and best['gap']>1e-7:break
    out=dict(scope=__doc__,seed=a.seed,checked=checked,records=sorted(records,key=lambda r:r['gap'],reverse=True)[:12])
    Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
    print('RESULT',checked,'best',out['records'][0] if out['records'] else None)
if __name__=='__main__':main()
