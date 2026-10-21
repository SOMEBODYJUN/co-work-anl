"""LP discovery on full exact-SPE strategy cones with rank-two customers.

LP outputs are discovery data. Rational witnesses must be replayed separately.
"""
import argparse
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path
import random
import sys
import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver

def cone_matrix(supports,actions,players,topics,mode):
    def terminal(h):
        while len(h)<players:h=h+(actions[h],)
        return h
    def payoff(h,who):
        a=h[who]
        return np.array([float(Fraction(int(a in b),sum(c in b for c in h)))
                         if a in b else 0 for b in supports])
    root=terminal(())
    coverage=np.array([int(any(a in b for a in root)) for b in supports])
    rows=[]
    for length in range(players):
        for h in product(range(topics),repeat=length):
            actual=payoff(terminal(h),length)
            for a in range(topics):
                rows.append(np.r_[payoff(terminal(h+(a,)),length)-actual,0])
            if length==players-1:
                rows.append(np.r_[-actual,1])
    objective=(np.r_[coverage,-players] if mode=='aggregate'
               else np.r_[payoff(root,0),-1])
    return np.array(rows),objective,root

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--cases',type=int,default=1000)
    p.add_argument('--seed',type=int,default=79213)
    p.add_argument('--topics',type=int,default=6)
    p.add_argument('--players',type=int,default=3)
    p.add_argument('--mode',choices=['aggregate','root'],default='aggregate')
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    rng=random.Random(args.seed)
    supports=[frozenset(s) for k in [1,2]
              for s in combinations(range(args.topics),k)]
    report={'seed':args.seed,'topics':args.topics,'players':args.players,
            'requested_cases':args.cases,'cases':0,'failures':[],
            'best_objective':1.,'total_lp_rows':0,'mode':args.mode}
    for case in range(args.cases):
        customers=tuple(CustomerType(s,m) for s in supports
                        if (m:=rng.choice([0,0,1,2,3,5,8,13,21])))
        instance=Instance(tuple(map(str,range(args.topics))),customers,args.players)
        solver=ExactSPESolver(instance)
        outcomes=sorted(solver.outcomes())
        target=rng.choice(outcomes)
        cert=solver.certificate(target,
            action_selector=lambda h,opts:rng.choice(opts),
            continuation_selector=lambda h,opts:rng.choice(opts))
        matrix,c,root=cone_matrix(supports,cert.actions,args.players,args.topics,args.mode)
        result=linprog(c,A_ub=matrix,b_ub=np.zeros(len(matrix)),
              A_eq=np.array([[1.]*len(supports)+[0.]]),b_eq=[1.],
              bounds=[(0,None)]*(len(supports)+1),method='highs')
        if not result.success:raise RuntimeError(result.message)
        report['cases']+=1
        report['total_lp_rows']+=len(matrix)
        report['best_objective']=min(report['best_objective'],result.fun)
        if result.fun < -1e-8:
            report['failures'].append({'case':case,'objective':result.fun,
                 'seed_instance':instance.to_dict(),'root':root,
                 'supports':[sorted(s) for s in supports],
                 'weights':result.x[:-1].tolist(),'theta_lower':result.x[-1],
                 'actions':[{ 'h':list(h),'a':a } for h,a in cert.actions.items()]})
            break
    with args.output.open('x') as f:json.dump(report,f,indent=2)

if __name__=='__main__':main()
