"""Finite exact attack on OPT-W <= m min_i u_i; no universal theorem.

LP creates candidates inside a fixed full ordered-history SPE cone. Every
accepted integer point is checked with exact arithmetic at every history.
No git operation is performed. Restrict all writes to this script directory.
"""
from __future__ import annotations
import argparse, importlib.util, json, random, sys, time
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
spec = importlib.util.spec_from_file_location("strategy_lp", ROOT / "tests/audits/customer_attraction_strategy_lp.py")
lp = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lp
spec.loader.exec_module(lp)
from customer_attraction import ExactSPESolver, Instance, CustomerType, verify_certificate

def encode(x):
    if isinstance(x, Fraction): return str(x)
    if isinstance(x, dict): return {str(k): encode(v) for k,v in x.items()}
    if isinstance(x, (tuple,list)): return [encode(v) for v in x]
    return x

def attack(cone, portfolio, topic):
    pay = lp.payoff_row(cone.topics, cone.root, topic)
    cov = lp.coverage_row(cone.topics, portfolio)
    objective = tuple(o-w-cone.players*u for o,w,u in zip(cov, cone.welfare, pay))
    res = linprog(-np.array(objective,dtype=float), A_ub=-cone.matrix,
                  b_ub=np.zeros(len(cone.rows)), A_eq=np.array([cone.welfare],dtype=float),
                  b_eq=[1], bounds=(0,None), method="highs")
    if not res.success: return None
    values = tuple(Fraction(float(x)).limit_denominator(10**7) for x in res.x)
    if not cone.verify(values) or lp.dot(cone.welfare,values)!=1:
        values = cone.recover_vertex(res.x)
    if values is None or not cone.verify(values) or lp.dot(cone.welfare,values)!=1:
        return None
    value = lp.dot(objective,values)
    return value, lp.integer_clones(values), portfolio, topic

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--topics',type=int,default=5)
    ap.add_argument('--players',type=int,default=3)
    ap.add_argument('--instances',type=int,default=80)
    ap.add_argument('--seed',type=int,default=231026)
    ap.add_argument('--output',default='gap_probe.json')
    args=ap.parse_args(); rng=random.Random(args.seed); started=time.monotonic()
    seeds=list(lp.structural_seeds(args.topics,args.players))
    best=Fraction(-1000); calls=0; seen=set(); records=[]
    for k in range(args.instances):
        if seeds: clones=seeds.pop(0)
        else:
            clones=tuple(rng.randrange(1,13) if rng.random()<.35 else 0
                         for mask in range(1,1<<args.topics))
        inst=lp.instance_from_clones(args.topics,args.players,clones)
        solver=ExactSPESolver(inst)
        for target in sorted(solver.worst_outcomes())[:4]:
            cert=solver.certificate(target,
                 action_selector=lambda h,c:rng.choice(c),
                 continuation_selector=lambda h,c:rng.choice(c))
            key=tuple(sorted(cert.actions.items()))
            if key in seen: continue
            seen.add(key); cone=lp.StrategyCone(args.topics,args.players,dict(cert.actions))
            for portfolio in combinations(range(args.topics),min(args.players,args.topics)):
                for topic,n in enumerate(cone.root):
                    if not n: continue
                    calls+=1; candidate=attack(cone,portfolio,topic)
                    if candidate is None: continue
                    value, endpoint, portfolio, topic=candidate
                    if value>best:
                        best=value; print(json.dumps({'instance':k,'cones':len(seen),'calls':calls,'new_best':str(best)}),flush=True)
                    if value>0:
                        assert lp.independently_verify(cone,endpoint)
                        outinst=lp.instance_from_clones(args.topics,args.players,endpoint)
                        # Definition-level verifier is separate from outcome generation.
                        outcert=lp.StrategyCertificate(cone.actions,cone.root)
                        verification=verify_certificate(outinst,outcert)
                        if hasattr(verification,'valid'): assert verification.valid
                        utilities=outinst.topic_payoffs(cone.root)
                        min_u=min(utilities[a] for a,n in enumerate(cone.root) if n)
                        welfare=outinst.welfare(cone.root); optimum=outinst.optimal_welfare()
                        report={'status':'exact_counterexample_to_auxiliary_gap_bridge',
                                'universal_half_coverage_status':'OPEN',
                                'parameters':vars(args),'cones':len(seen),'lp_calls':calls,
                                'instance':outinst.to_dict(),'certificate':outcert.to_dict(),
                                'W':welfare,'OPT':optimum,'min_u':min_u,
                                'gap_minus_m_min':optimum-welfare-args.players*min_u,
                                'objective_portfolio':portfolio,'objective_low_topic':topic,
                                'objective_exact':value,'elapsed':time.monotonic()-started}
                        Path(__file__).with_name(args.output).write_text(json.dumps(encode(report),indent=2)+'\n')
                        print(json.dumps(encode({k:v for k,v in report.items() if k not in ('certificate','instance')})))
                        return
            records.append({'root':cone.root})
    report={'status':'finite_search_only_no_auxiliary_counterexample',
            'parameters':vars(args),'cones':len(seen),'lp_calls':calls,'best':best,
            'elapsed':time.monotonic()-started}
    Path(__file__).with_name(args.output).write_text(json.dumps(encode(report),indent=2)+'\n')
    print(json.dumps(encode(report)))

if __name__=='__main__': main()
