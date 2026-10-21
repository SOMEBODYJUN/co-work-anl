"""Float-guided full-history policy cones seeded by genuine response gadgets.

No universal conclusion is drawn from a finite run. Positive violations are
saved only after Fraction reconstruction and every-history exact replay.
"""
from pathlib import Path
import argparse, importlib.util, json, sys, time
from fractions import Fraction as F
from math import lcm, gcd
import numpy as np
from scipy.optimize import linprog

ROOT=next(p for p in Path(__file__).resolve().parents if (p/'customer_attraction/__init__.py').is_file())
SOURCE=ROOT/'research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/credible_search/iterative_search.py'
spec=importlib.util.spec_from_file_location('prior_search',SOURCE)
prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
sys.path.insert(0,str(ROOT))
from customer_attraction import Instance,CustomerType,StrategyCertificate,verify_certificate

def structured(p,m):
    for label,r in prior.seeds(p,m):yield label,r
    gadgets={
      'cap':{1:3,2:4,12:6,20:6,25:2,26:2},
      'residual':{9:2,17:2,2:3,4:3,26:2,28:2},
      'terminal_clone':{1:1,2:1,6:1,9:1,12:3},
    }
    for label,weights in gadgets.items():
        for padding in (1,3,4,6,9):
            r=np.zeros((1<<p)-1)
            for mask,n in weights.items():r[mask-1]=n
            for a in range(5,p):r[(1<<a)-1]=padding
            yield f'{label}-pad{padding}',r

def exact_point(p,m,actions,r,topic,portfolio):
    from customer_attraction_strategy_lp import StrategyCone,payoff_row,coverage_row,dot,independently_verify
    cone=StrategyCone(p,m,actions)
    norm=payoff_row(p,cone.root,topic)
    vals=tuple(F(float(x)).limit_denominator(10**7) for x in r)
    if not cone.verify(vals) or dot(norm,vals)!=1:
        old=cone.welfare;cone.welfare=norm
        vals=cone.recover_vertex(r);cone.welfare=old
    if vals is None or not cone.verify(vals) or dot(norm,vals)!=1:return None
    scale=lcm(*(x.denominator for x in vals));clones=[int(x*scale) for x in vals]
    common=gcd(*clones);clones=[x//common for x in clones]
    if not independently_verify(cone,clones):raise AssertionError('full exact replay')
    game=Instance(tuple(map(str,range(p))),tuple(CustomerType(frozenset(a for a in range(p) if mask>>a&1),n) for mask,n in enumerate(clones,1) if n),m)
    cert=StrategyCertificate(actions,cone.root);verify_certificate(game,cert).assert_valid()
    utility=game.topic_payoffs(cone.root)[topic];W=game.welfare(cone.root);OPT=game.optimal_welfare()
    return {'instance':game.to_dict(),'certificate':cert.to_dict(),'topic':topic,'W':W,'OPT':OPT,'utility':str(utility),'gap_over_utility':str(F(OPT-W)/utility),'chosen_portfolio':portfolio}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--topics',type=int,default=7);ap.add_argument('--players',type=int,default=5);ap.add_argument('--rounds',type=int,default=24);ap.add_argument('--seed',type=int,default=216741);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    s=prior.Search(args.topics,args.players,args.seed);queue=list(structured(args.topics,args.players));log=[];best=-1;started=time.monotonic()
    report={'scope':'finite full-history policy-cone attack on OPT-W<=m*u_i','seed':args.seed,'topics':args.topics,'players':args.players,'universal_result':False,'log':log}
    for it in range(args.rounds):
        label,r=queue[it] if it<len(queue) else s.rng.choice(queue)
        if it>=18 and it%4==3:
            r=r.copy()
            for _ in range(2):r[s.rng.randrange(len(r))]+=.03*max(r.max(),1)
        s.solve(r);opt=s.v@r;j=int(opt.argmax())
        def quality(t):
            used=[a for a,c in enumerate(s.Q[t]) if c]
            low=min(s.U[t,a] for a in used)
            return (opt[j]-s.W[t])/low if low>1e-10 else -1e100
        target=max(s.R[s.root],key=quality);actions,A=s.policy(int(target),['min','max','lowW','highW','uniform'][it%5])
        local=None
        for b,c in enumerate(s.Q[target]):
            if not c:continue
            for jj in list(dict.fromkeys([j]+s.rng.sample(range(len(s.Js)),min(2,len(s.Js))))):
                gain=s.v[jj]-s.w[target]
                out=linprog(-gain,A_ub=-A,b_ub=np.zeros(len(A)),A_eq=s.pay[[target],b],b_eq=[1],bounds=(0,None),method='highs')
                if out.success and (local is None or out.fun<local[0].fun):local=out,b,jj
        if local is None:continue
        out,b,jj=local;queue.append((f'LP{it}',out.x));value=-out.fun
        row={'iteration':it,'source':label,'gap_ratio_float':value,'counts':s.Q[target],'topic':b,'rows':len(A),'elapsed':time.monotonic()-started};log.append(row);print(json.dumps(row),flush=True)
        if value>best+1e-8:
            best=value;report['best_float']=value
            point=exact_point(s.p,s.m,actions,out.x,b,s.Js[jj])
            if point:report['selected_exact']=point;row['exact_gap_ratio']=point['gap_over_utility']
        args.output.write_text(json.dumps(report,indent=2)+'\n')
        if report.get('selected_exact') and F(report['selected_exact']['gap_over_utility'])>s.m:return
if __name__=='__main__':main()
