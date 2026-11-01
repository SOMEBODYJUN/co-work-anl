"""Discovery-only: perturb 41-client full policy cone while p_bad stays optimal.

The pure dual cap (0,4) is held fixed. Every customer type is allowed.
The safety-optimal face is then reoptimized, never replaced by one chosen p.
"""
import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import linprog


def main():
    par=argparse.ArgumentParser()
    par.add_argument('--trials',type=int,default=1000)
    par.add_argument('--output',type=Path,required=True)
    args=par.parse_args()
    src=Path('research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/security_aggregate/pair_theory/all_optimal_query_failure_41.json')
    data=json.loads(src.read_text())
    n=data['players'];k=len(data['topics']);T=(1<<k)-1
    M=np.array([[(mask>>a)&1 for mask in range(1,1<<k)] for a in range(k)],float)
    sig={tuple(row['history']):row['action'] for row in data['actions']}
    def term(h):
        while len(h)<n:h+=(sig[h],)
        return h
    def util(a,z):
        return M[a]/np.maximum(sum(M[b] for b in z),1)
    G=[]
    for h,a in sig.items():
        for b in range(k):
            G.append(util(a,term(h))-util(b,term(h+(b,))))
    G=np.unique(np.array(G),axis=0)
    z=term(());coverage=(sum(M[a] for a in z)>0).astype(float)
    R=np.array([sum(util(a,z[:i]+(a,)+z[i+1:]) for i in range(n)) for a in range(k)])
    BB=list(itertools.combinations_with_replacement(range(k),n-1))
    payoff=np.array([[util(a,B+(a,)) for a in range(k)] for B in BB])
    p=np.array([float(Fraction(x)) for x in data['bad_optimal_query']])
    beta=np.einsum('a,bat->bt',p,payoff)
    cap=payoff[BB.index(tuple(data['static_cap_background']))]
    # Fixed primal p and dual pure-cap are jointly optimal in every feasible w.
    A=np.vstack([np.column_stack([-G,np.zeros(len(G))]),
                 np.column_stack([-beta,np.ones(len(beta))]),
                 np.column_stack([cap,-np.ones(k)])])
    eq=[np.r_[coverage,0.]]
    bounds=[(0,None)]*T+[(0,None)]
    rng=np.random.default_rng(310102106)
    report={'status':'numerical_only','source':str(src),'completed':0,
            'max_min_optimal_regret':-1.,'counterexample_candidate':None}
    def inspect(w):
        game=np.einsum('bat,t->ba',payoff,w)
        val=min(game@p)
        rr=R@w;W=coverage@w
        # Exact optimal-face equality is enforced to floating tolerance here.
        opt=linprog(rr,A_ub=-game,b_ub=-np.ones(len(game))*(val-1e-10),
                    A_eq=[np.ones(k)],b_eq=[1.],bounds=[(0,None)]*k,method='highs')
        if not opt.success:raise ValueError(opt.message)
        return float(opt.fun-W),opt.x,float(val),rr
    for trial in range(args.trials):
        if trial==0:obj=-(p@R-coverage)
        elif trial%3==0:
            obj=-(p@R-coverage)+rng.normal(0,.005,T)
        else:obj=rng.normal(0,1,T)
        out=linprog(np.r_[obj,0.],A_ub=A,b_ub=np.zeros(len(A)),
                    A_eq=eq,b_eq=[1.],bounds=bounds,method='highs')
        if not out.success:raise ValueError(out.message)
        gap,good,v,rr=inspect(out.x[:-1])
        report['completed']=trial+1
        if gap>report['max_min_optimal_regret']+1e-9:
            report['max_min_optimal_regret']=gap
            report['incumbent']={'trial':trial,'weights':out.x[:-1].tolist(),
                                  'good_optimal_query':good.tolist(),'security':v,
                                  'R_values':rr.tolist(),'chosen_bad_R':float(p@rr)}
            print(json.dumps({'trial':trial,'gap':gap,'v':v,'badR':float(p@rr)}),flush=True)
        if gap>1e-7:
            report['counterexample_candidate']=report['incumbent']
            args.output.write_text(json.dumps(report,indent=2)+'\n')
            return
        if trial%50==0:args.output.write_text(json.dumps(report,indent=2)+'\n')
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('FINISHED',report['completed'],report['max_min_optimal_regret'],flush=True)


if __name__=='__main__':main()
