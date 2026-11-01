"""Use the existing all-history joint MILP with an explicitly changed objective.

The model source is loaded locally, with exactly one objective-line replacement;
all constraints, root guarantee bounds and complete-tree semantics are retained.
Float output is only a proposal: the separate Fraction cone attack reconstructs
and verifies each accepted unit-customer endpoint.
"""
from fractions import Fraction as F
import argparse
import hashlib
import inspect
import json
from pathlib import Path
import sys

ROOT=next(p for p in Path(__file__).resolve().parents if (p/'customer_attraction/model.py').is_file())
sys.path[:0]=[str(ROOT),str(ROOT/'tests/audits'),str(Path(__file__).resolve().parent)]
import cone_attack_joint_milp as base
from customer_attraction_strategy_lp import serializable
from full_terminal_tax_probe import attack


def tax_objective(p,path,portfolio):
    coverage=base.coverage_row(p,portfolio)
    counts=tuple(path.count(a) for a in range(p))
    return tuple(v-F(c,c+1) for mask,v in enumerate(coverage,1)
                 for c in [sum(counts[a] for a in range(p) if mask&(1<<a))])


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--topics',type=int,default=4)
    ap.add_argument('--path',action='append',required=True)
    ap.add_argument('--seconds',type=float,default=20)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    if args.output.exists():raise FileExistsError(args.output)
    source=inspect.getsource(base.joint_candidate)
    old='objective[:n]=-np.array(coverage_row(p,portfolio),dtype=float)'
    new='objective[:n]=-np.array(tax_objective(p,path,portfolio),dtype=float)'
    if source.count(old)!=1:raise RuntimeError('Source objective changed; re-audit before replacing it.')
    env=dict(vars(base));env['tax_objective']=tax_objective
    exec(compile(source.replace(old,new),'<complete-tree-tax-objective>','exec'),env)
    report={'base_model_sha256':hashlib.sha256(inspect.getsource(base.joint_candidate).encode()).hexdigest(),
            'scope':'Finite joint full-history proposal plus exact fixed-cone reconstruction; not a general proof',
            'runs':[]}
    for raw in args.path:
        path=tuple(map(int,raw.split(',')))
        portfolio=tuple(range(min(args.topics,len(path))))
        cone,meta=env['joint_candidate'](args.topics,path,portfolio,args.seconds)
        result=attack(cone,'joint-'+raw) if cone is not None else None
        report['runs'].append({'path':path,'metadata':meta,'exact_cone_result':result})
        print(json.dumps(serializable({'path':path,'metadata':meta,'result':
              {k:v for k,v in (result or {}).items() if k not in ('instance','strategy','integer_clones')}})),flush=True)
        args.output.write_text(json.dumps(serializable(report),indent=2)+'\n')
        if result and 'instance' in result:return


if __name__=='__main__':main()
