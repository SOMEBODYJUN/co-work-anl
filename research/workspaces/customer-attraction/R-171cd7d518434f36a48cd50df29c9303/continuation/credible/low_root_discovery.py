"""Finite credible-cone exploration from a specified low-root source.

Float LPs generate multiplicities. Every accepted endpoint is recovered exactly
and checked on all ordered histories. No coverage or completeness theorem is
inferred from the finite exploration.
"""
from pathlib import Path
from fractions import Fraction
from itertools import combinations
import argparse, json, random, sys, time
import numpy as np

ROOT=next(p for p in Path(__file__).resolve().parents if (p/'customer_attraction/__init__.py').is_file())
sys.path[:0]=[str(ROOT),str(ROOT/'tests/audits')]
from customer_attraction import ExactSPESolver,StrategyCertificate,verify_certificate
from customer_attraction_strategy_lp import instance_from_clones,integer_clones,payoff_row,serializable,independently_verify
from cone_attack_credible_variants import credible_cone


def initial():
    weights={1:3,2:4,4|8:6,4|16:6,1|8|16:2,2|8|16:2,32:10,64:10}
    return tuple(weights.get(mask,0) for mask in range(1,128))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--steps',type=int,default=8);ap.add_argument('--seed',type=int,default=319221)
    ap.add_argument('--out',type=Path,required=True);ap.add_argument('--cap',default='5/43');args=ap.parse_args()
    rng=random.Random(args.seed);source=initial();p,m=7,5;cap=Fraction(args.cap);target=(1,1,1,0,0,1,1)
    started=time.monotonic();best=Fraction(0);accepted=0;logs=[];args.out.mkdir(parents=True,exist_ok=True)
    for step in range(args.steps):
        ins=instance_from_clones(p,m,source);solver=ExactSPESolver(ins)
        candidates=[]
        for q in solver.outcomes():
            floor=solver.threshold((0,)*p)
            if any(q in solver.outcomes(tuple(int(j==a) for j in range(p))) and floor<=solver._utility(q,a)<=cap*ins.welfare(q) for a in range(p)):
                candidates.append(q)
        if not candidates:raise AssertionError('lost low-root exact source')
        if target not in candidates:target=rng.choice(candidates)
        class LowRootChoice:
            first=True
            def choice(self,options):
                if self.first:
                    self.first=False;return min(options,key=lambda a:solver._utility(target,a))
                return rng.choice(options)
        mode=rng.choice(('uniform_credible','max_credible_payoff','max_credible_welfare','min_credible_welfare'))
        cone,stats=credible_cone(solver,target,LowRootChoice(),mode)
        root_action=cone.actions[()]
        cone.rows += (tuple(cap*w-u for w,u in zip(cone.welfare,payoff_row(p,cone.root,root_action))),)
        cone.matrix=np.array(cone.rows,dtype=float)
        portfolios=list(combinations(range(p),m));rng.shuffle(portfolios)
        stepbest=Fraction(0);nextsource=None
        for J in portfolios:
            result=cone.optimize(J)
            if not result['certified']:continue
            clones=integer_clones(result['values']);candidate=instance_from_clones(p,m,clones)
            W=candidate.welfare(cone.root);OPT=candidate.optimal_welfare();ratio=Fraction(OPT,W);accepted+=1
            if ratio>stepbest:stepbest=ratio;nextsource=clones
            if ratio>best:
                cert=StrategyCertificate(cone.actions,cone.root)
                verify_certificate(candidate,cert).assert_valid()
                if not independently_verify(cone,clones):raise AssertionError('ordered-history independent exact check')
                best=ratio
                record={'scope':'one complete-history SPE; no universal theorem','instance':candidate.to_dict(),'strategy':cert.to_dict(),'source_clones':source,'mode':mode,'statistics':stats,'seed':args.seed,'step':step,'cap':cap,'first_action':root_action,'root_payoff':candidate.topic_payoffs(cone.root)[root_action],'W':W,'OPT':OPT,'ratio':ratio,'portfolio':J,'LP_value':result['value'],'seconds':time.monotonic()-started}
                (args.out/'best.json').write_text(json.dumps(serializable(record),indent=2)+'\n')
                print(json.dumps(serializable({k:v for k,v in record.items() if k not in ('instance','strategy','source_clones')})),flush=True)
            if best>2:break
        logs.append({'step':step,'source_total':sum(source),'source_W':ins.welfare(target),'target':target,'mode':mode,'statistics':stats,'step_best':stepbest,'best':best,'accepted_endpoints':accepted,'seconds':time.monotonic()-started})
        (args.out/'summary.json').write_text(json.dumps(serializable({'scope':'finite sampled cones, exact primal acceptance; no universal result','parameters':vars(args)|{'out':str(args.out)},'records':logs}),indent=2)+'\n')
        print(json.dumps(serializable(logs[-1])),flush=True)
        if best>2:break
        if nextsource is not None:source=nextsource


if __name__=='__main__':main()
