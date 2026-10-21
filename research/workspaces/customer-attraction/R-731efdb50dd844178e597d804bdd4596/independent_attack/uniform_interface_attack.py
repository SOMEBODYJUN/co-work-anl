"""Candidate attacks on the open uniform-portfolio deviation interface (6)."""
from pathlib import Path
import sys,json,random
from itertools import combinations
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests/audits'))
from customer_attraction import ExactSPESolver
from customer_attraction_strategy_lp import instance_from_clones,payoff_row,coverage_row,integer_clones
from cone_attack_credible_variants import credible_cone

def objective(cone,J):
    p,m=cone.topics,cone.players;n=(1<<p)-1
    row=m*np.array(coverage_row(p,J),dtype=float)
    path=()
    for i in range(m):
        for a in J:row-=np.array(payoff_row(p,cone.terminals[path+(a,)],a),dtype=float)
        path+=(cone.actions[path],)
    return row,path

def main():
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--topics',type=int,default=5);ap.add_argument('--players',type=int,default=3);ap.add_argument('--trials',type=int,default=100);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    p,m=args.topics,args.players;rng=random.Random(212703);record={'scope':'floating candidate search','topics':p,'players':m,'best':None}
    best=-1e10
    for trial in range(args.trials):
        weights=[rng.randrange(1,10) if rng.random()<.3 else 0 for _ in range((1<<p)-1)]
        if not any(weights):weights[0]=1
        instance=instance_from_clones(p,m,weights);solver=ExactSPESolver(instance);target=rng.choice(sorted(solver.worst_outcomes()))
        cone,_=credible_cone(solver,target,rng,rng.choice(['uniform_credible','min_credible_welfare','max_credible_welfare','max_credible_payoff']))
        for J in combinations(range(p),min(p,m)):
            obj,path=objective(cone,J)
            res=linprog(-obj,A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),A_eq=[np.array(cone.welfare,dtype=float)],b_eq=[1],bounds=(0,None),method='highs')
            if not res.success:continue
            val=-res.fun
            if val>best+1e-8:
                best=val
                row={'trial':trial,'objective':val,'m_minus_one':m-1,'path':path,'portfolio':J}
                print(json.dumps(row),flush=True)
                ww=tuple(Fraction(float(x)).limit_denominator(10**7) for x in res.x)
                if not cone.verify(ww) or sum(x*y for x,y in zip(ww,cone.welfare))!=1:ww=cone.recover_vertex(res.x)
                record['best']={**row,'weights':[str(x) for x in ww] if ww else None,'strategy':[{'history':h,'action':a} for h,a in sorted(cone.actions.items())]};args.output.write_text(json.dumps(record,indent=2)+'\n')
            if val>m-1+1e-7:
                record['candidate_found']=True;args.output.write_text(json.dumps(record,indent=2)+'\n');return
    record['completed_trials']=args.trials;args.output.write_text(json.dumps(record,indent=2)+'\n')
if __name__=='__main__':main()
