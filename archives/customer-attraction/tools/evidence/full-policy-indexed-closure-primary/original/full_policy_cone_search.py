"""Genuine full-tree SPE cone search, separate from indexed relaxations.

Each policy is a canonical complete ordered-history SPE certificate. Its entire
one-step-deviation cone is optimized over all customer types. Every retained
rational point is scaled to unit-customer multiplicities and verified by the
canonical full-tree verifier. Search failure proves no general bound.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
from math import gcd, lcm
from pathlib import Path
import argparse
import importlib.util
import json
import random
import sys
import numpy as np
from scipy.optimize import linprog

ROOT=next(p for p in Path(__file__).resolve().parents
          if (p/'customer_attraction/__init__.py').exists())
sys.path.insert(0,str(ROOT))
from customer_attraction import Instance, CustomerType, ExactSPESolver, verify_certificate

OLD=ROOT/'research/workspaces/customer-attraction/R-d7f409d6a5914bdeb09875ab32618466/credible_counterexample/frozen_support_closure.py'
SPEC=importlib.util.spec_from_file_location('recover_source',OLD)
R=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(R)
HERE=Path(__file__).resolve().parent


def instance(weights,p,m):
    den=lcm(*(x.denominator for x in weights))
    ints=[int(x*den) for x in weights]
    common=0
    for x in ints:common=gcd(common,x)
    if common:ints=[x//common for x in ints]
    return Instance(tuple(f'T{i}' for i in range(p)),
       tuple(CustomerType(frozenset(i for i in range(p) if mask>>i&1),n)
             for mask,n in enumerate(ints,1) if n),m)


def cone(cert,p,m):
    masks=np.arange(1,1<<p,dtype=np.int64)
    membership=((masks[:,None]>>np.arange(p))&1)
    scale=lcm(*range(1,m+1))
    @lru_cache(None)
    def ending(h):
        if len(h)==m:return tuple(h.count(a) for a in range(p))
        return ending(h+(cert.actions[h],))
    @lru_cache(None)
    def coeff(counts,action):
        load=membership@np.array(counts,dtype=np.int64)
        return tuple(int(scale//n) if member and n else 0
                     for member,n in zip(membership[:,action],load))
    rows=set()
    for depth in range(m):
        for h in product(range(p),repeat=depth):
            chosen=cert.actions[h]
            lhs=np.array(coeff(ending(h),chosen),dtype=np.int64)
            for a in range(p):
                if a!=chosen:
                    row=tuple(lhs-np.array(coeff(ending(h+(a,)),a),dtype=np.int64))
                    if any(row):rows.add(row)
    path=ending(())
    w=np.array([int(any(member and n for member,n in zip(row,path)))
                for row in membership],dtype=np.int64)
    return np.array(sorted(rows),dtype=np.int64),w,membership,path


def optimize(cert,p,m,current):
    G,w,membership,path=cone(cert,p,m)
    best=None
    # All maximum-coverage comparison supports have <=m labels, so padding
    # gives an m-element support for p>=m.
    for selected in combinations(range(p),min(p,m)):
        objective=(membership[:,selected].sum(axis=1)>0).astype(np.int64)
        result=linprog(-objective.astype(float),A_ub=-G.astype(float),
                       b_ub=np.zeros(len(G)),A_eq=[w.astype(float)],b_eq=[1],
                       bounds=(0,None),method='highs')
        if not result.success:continue
        if best is None or -result.fun>best[0]+1e-8:
            best=(-result.fun,result,objective,selected)
    if best is None:return None
    value,result,objective,selected=best
    active=np.abs(G@result.x)<1e-7
    weights=R.recover(np.concatenate([w[None,:],G[active].astype(object)]),
                      [1]+[0]*int(sum(active)),result.x)
    if weights is None or min(weights)<0:return None
    assert sum(F(int(x))*r for x,r in zip(w,weights))==1
    slacks=[sum(F(int(x))*r for x,r in zip(row,weights)) for row in G]
    if min(slacks,default=F(0))<0:return None
    inst=instance(weights,p,m)
    report=verify_certificate(inst,cert)
    report.assert_valid()
    attained=F(sum(F(int(x))*r for x,r in zip(objective,weights)))
    return inst,{'unique_full_tree_deviation_rows':len(G),'full_history_nodes':len(cert.actions),
                 'fixed_path_counts':path,'chosen_comparison_support':selected,
                 'exact_cone_ratio':str(attained),'floating_cone_ratio':value,
                 'minimum_exact_cone_slack':str(min(slacks,default=F(0))),
                 'certificate_verified':True}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--p',type=int,default=7)
    ap.add_argument('--m',type=int,default=5);ap.add_argument('--seeds',type=int,default=4)
    ap.add_argument('--iterations',type=int,default=3);args=ap.parse_args()
    p,m=args.p,args.m;rng=random.Random(9051284)
    rounds=[];global_best=F(0);bestfiles=None
    for seed in range(args.seeds):
        weights=[F(0)]*((1<<p)-1)
        if seed==0:
            for a in range(p):weights[(1<<a)-1]=F(m if a==0 else 1)
        else:
            for a in range(p):weights[(1<<a)-1]=F(rng.randint(2,12))
            # Sparse overlaps are needed for continuation changes.
            for mask in range(1,1<<p):
                if 2<=mask.bit_count()<=3 and rng.random()<0.08:
                    weights[mask-1]=F(rng.randint(1,3))
        inst=instance(weights,p,m)
        previous=None
        for iteration in range(args.iterations):
            solver=ExactSPESolver(inst)
            cert=solver.worst_certificate()
            ratio=solver.inefficiency_ratio()
            entry={'seed':seed,'iteration':iteration,'initial_exact_ratio':str(ratio),
                   'initial_welfare':solver.minimum_welfare(),'initial_optimum':inst.optimal_welfare(),
                   'count_states':solver.stats.count_states}
            verify_certificate(inst,cert).assert_valid()
            if ratio>global_best:
                global_best=ratio
                bestfiles=(inst,cert)
            result=optimize(cert,p,m,inst)
            if result is None:
                entry['exact_recovery']='failed';rounds.append(entry);break
            inst,details=result;entry.update(details);rounds.append(entry)
            print(json.dumps(entry),flush=True)
            # The verified cone improvement can be lower than the fresh worst
            # SPE ratio only if the former optimum support changes; retain it.
            cone_ratio=F(details['exact_cone_ratio'])
            if cone_ratio>global_best:
                global_best=cone_ratio;bestfiles=(inst,cert)
            signature=json.dumps(inst.to_dict(),sort_keys=True)
            if signature==previous:break
            previous=signature
    prefix=HERE/f'full_policy_p{p}_m{m}'
    if bestfiles:
        bestinst,bestcert=bestfiles
        prefix.with_name(prefix.name+'_instance.json').write_text(json.dumps(bestinst.to_dict(),indent=2)+'\n')
        prefix.with_name(prefix.name+'_certificate.json').write_text(json.dumps(bestcert.to_dict(),indent=2)+'\n')
        verify_certificate(bestinst,bestcert).assert_valid()
    report={'status':'finite exact verified full-policy search; no general theorem',
            'p':p,'m':m,'seeds':args.seeds,'iterations':args.iterations,
            'random_seed':9051284,'best_verified_ratio_at_least':str(global_best),
            'half_counterexample_found':global_best>2,'cone_optimality_certified':False,
            'exact_cone_ratio_meaning':'exact attained feasible ratio; not a certified LP optimum',
            'rounds':rounds}
    prefix.with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='rounds'},indent=2))


if __name__=='__main__':main()
