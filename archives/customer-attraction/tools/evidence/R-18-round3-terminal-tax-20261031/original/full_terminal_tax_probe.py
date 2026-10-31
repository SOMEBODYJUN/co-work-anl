"""Attack the full-terminal-load tax bridge in specified complete SPE cones.

This is a finite candidate generator, never a universal proof.  The conjectured
bridge is OPT_m <= W + sum_{x:c_x>0} c_x/(c_x+1), with all m actual players
included in c. Float LP endpoints must pass exact Fraction cone and tree checks.
"""
from fractions import Fraction as F
from itertools import combinations
import argparse
import json
from pathlib import Path
import random
import sys

ROOT = next(p for p in Path(__file__).resolve().parents if (p/'customer_attraction/model.py').is_file())
sys.path[:0] = [str(ROOT),str(ROOT/'tests/audits')]
import numpy as np
from scipy.optimize import linprog
from customer_attraction import Instance, ExactSPESolver, StrategyCertificate, big_theme_lower_bound, verify_certificate
from customer_attraction_strategy_lp import StrategyCone, coverage_row, dot, integer_clones, instance_from_clones, serializable
from cone_attack_credible_variants import builtin_sources, credible_cone


def tax_row(cone):
    return tuple(F(c,c+1) for mask in range(1,1<<cone.topics)
                 for c in [sum(cone.root[a] for a in range(cone.topics) if mask&(1<<a))])


def attack(cone, label):
    tax=tax_row(cone)
    best=None
    for support in combinations(range(cone.topics),min(cone.topics,cone.players)):
        objective=tuple(a-b for a,b in zip(coverage_row(cone.topics,support),tax))
        res=linprog(-np.asarray(objective,dtype=float),A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),
                    A_eq=np.asarray([cone.welfare],dtype=float),b_eq=[1],bounds=(0,None),method='highs')
        if not res.success:
            continue
        v=tuple(F(float(x)).limit_denominator(10**7) for x in res.x)
        if not cone.verify(v) or dot(cone.welfare,v)!=1:
            v=cone.recover_vertex(res.x)
        if v is None or not cone.verify(v) or dot(cone.welfare,v)!=1:
            continue
        value=dot(objective,v)
        if best is None or value>best['value']:
            best={'source':label,'value':value,'support':support,'players':cone.players,'topics':cone.topics}
        if value>1:
            clones=integer_clones(v)
            inst=instance_from_clones(cone.topics,cone.players,clones)
            cert=StrategyCertificate(cone.actions,cone.root)
            verify_certificate(inst,cert).assert_valid()
            result={**best,'instance':inst.to_dict(),'strategy':cert.to_dict(),'integer_clones':clones,
                    'welfare':inst.welfare(cone.root),'optimum':inst.optimal_welfare(),'tax':dot(tax,clones),
                    'claim':'Full terminal tax bridge counterexample; not a half-coverage counterexample'}
            return result
    return best


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--variants',type=int,default=1)
    args=ap.parse_args()
    if args.output.exists():raise FileExistsError(args.output)
    rng=random.Random(5211026)
    results=[]
    sources=[]
    raw=json.loads((ROOT/'evidence/certificates/customer_attraction/root_tax_failure.json').read_text())
    actions={tuple(x['history']):x['action'] for x in raw['strategy']['actions']}
    sources.append(('root-tax-four-player',StrategyCone(6,4,actions)))
    for m in range(1,6):
        inst=big_theme_lower_bound(m)
        cert=ExactSPESolver(inst).certificate(on_path=(0,)*m)
        sources.append((f'classic-{m}',StrategyCone(m,m,dict(cert.actions))))
    for label,inst,target in builtin_sources():
        solver=ExactSPESolver(inst)
        for mode in ('max_credible_payoff','max_credible_welfare','min_credible_welfare','uniform_credible'):
            for _ in range(args.variants):
                cone,_=credible_cone(solver,target,rng,mode)
                sources.append((label+'-'+mode,cone))
    for label,cone in sources:
        result=attack(cone,label)
        results.append(result)
        print(json.dumps(serializable(result if 'instance' not in (result or {}) else
                         {k:v for k,v in result.items() if k not in ('instance','strategy','integer_clones')})),flush=True)
        if result and 'instance' in result:
            args.output.write_text(json.dumps(serializable({'seed':5211026,'results':results}),indent=2)+'\n')
            return
    args.output.write_text(json.dumps(serializable({'seed':5211026,'results':results,
                          'status':'No violating endpoint in these specified cones; no universal conclusion'}),indent=2)+'\n')


if __name__=='__main__':main()
