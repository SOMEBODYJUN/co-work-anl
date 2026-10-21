"""Candidate generator for the uniform true-deviation portfolio interface.

Finite cone LP searches are not a universal proof. A positive witness is
reconstructed over Fraction and replayed at every ordered history.
"""
from pathlib import Path
import sys, random, json, argparse
from fractions import Fraction
from itertools import combinations, combinations_with_replacement
import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parents[5]
sys.path[:0]=[str(ROOT),str(ROOT/'tests/audits')]
from customer_attraction import ExactSPESolver, StrategyCertificate, verify_certificate
from customer_attraction_strategy_lp import (StrategyCone, payoff_row,coverage_row,dot,
    integer_clones, instance_from_clones, independently_verify,serializable)
from cone_attack_credible_variants import credible_cone

def objective_row(cone,portfolio):
    """m O - (m-1) W - sum_{i,j} actual-prefix true deviations."""
    p,m=cone.topics,cone.players
    row=[m*v-(m-1)*w for v,w in zip(coverage_row(p,set(portfolio)),cone.welfare)]
    h=()
    for i in range(m):
        for a in portfolio:
            value=payoff_row(p,cone.terminals[h+(a,)],a)
            row=[x-y for x,y in zip(row,value)]
        h=h+(cone.actions[h],)
    return tuple(row)

def attack(cone,portfolio):
    objective=objective_row(cone,portfolio)
    res=linprog(-np.asarray(objective,dtype=float),A_ub=-cone.matrix,
        b_ub=np.zeros(len(cone.rows)),A_eq=np.asarray([cone.welfare],dtype=float),
        b_eq=[1],bounds=(0,None),method='highs')
    if not res.success:return None
    if -res.fun<1e-7:return {'float_max':-res.fun}
    values=tuple(Fraction(float(x)).limit_denominator(10**7) for x in res.x)
    if not cone.verify(values) or dot(cone.welfare,values)!=1:
        values=cone.recover_vertex(res.x)
    if values is None or not cone.verify(values):return {'recovery_failed':True}
    if dot(objective,values)<=0:return {'float_max':-res.fun,'exact_nonpositive':True}
    clones=integer_clones(values)
    if not independently_verify(cone,clones):raise AssertionError('exact full tree')
    instance=instance_from_clones(cone.topics,cone.players,clones)
    verify_certificate(instance,StrategyCertificate(cone.actions,cone.root)).assert_valid()
    return {'witness':True,'gap':dot(objective,clones),'clones':clones,
        'players':cone.players,'topics':cone.topics,'portfolio':portfolio,
        'strategy':StrategyCertificate(cone.actions,cone.root).to_dict(),
        'W':dot(cone.welfare,clones),'comparison':dot(coverage_row(cone.topics,set(portfolio)),clones),
        'OPT':instance.optimal_welfare()}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--players',type=int,default=3)
    ap.add_argument('--topics',type=int,default=4);ap.add_argument('--trials',type=int,default=100)
    ap.add_argument('--seed',type=int,default=977);ap.add_argument('--output',type=Path)
    args=ap.parse_args();rng=random.Random(args.seed);p,m=args.topics,args.players
    best=-1e10;seen=set();n=0
    for trial in range(args.trials):
        weights=[rng.choices([0,1,2,3,5,8,13,21],weights=[8,3,2,2,1,1,1,1])[0]
                 for mask in range(1,1<<p)]
        if not any(weights):continue
        solver=ExactSPESolver(instance_from_clones(p,m,weights))
        targets=list(solver.worst_outcomes())
        rng.shuffle(targets)
        for target in targets[:3]:
            for mode in ('uniform_credible','max_credible_payoff','min_credible_welfare'):
                cone,stats=credible_cone(solver,target,rng,mode)
                key=tuple(sorted(cone.actions.items()))
                if key in seen:continue
                seen.add(key);n+=1
                # An optimum never needs repeats unless p<m; include repeats anyway.
                for portfolio in combinations_with_replacement(range(p),m):
                    result=attack(cone,portfolio)
                    if result and result.get('witness'):
                        report={'status':'EXACT_AUXILIARY_INTERFACE_COUNTEREXAMPLE',
                            'main_half_counterexample':False,'seed':args.seed,'trial':trial,
                            'cones':n,'record':result}
                        if args.output:args.output.write_text(json.dumps(serializable(report),indent=2)+'\n')
                        print(json.dumps(serializable(report)),flush=True);return
                    if result:best=max(best,result.get('float_max',-1e10))
        if trial%10==0:print(json.dumps({'trial':trial,'cones':n,'best_float_gap':best}),flush=True)
    report={'status':'finite_search_no_witness','trials':args.trials,'cones':n,
        'best_float_gap':best,'universal_result':False}
    if args.output:args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))

if __name__=='__main__':main()
