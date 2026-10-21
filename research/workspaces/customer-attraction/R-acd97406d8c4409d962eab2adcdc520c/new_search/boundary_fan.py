"""Full-history strategy-cone neighbourhood MILP with fixed-chain elimination.

The unrestricted outcome DAG was already supplied by Boss1. This experiment
instead crosses only a reproducible chosen set of exact tie nodes of an
already credible full-history strategy. All other actions are fixed, but all
their genuine deviation constraints remain. Numerical results only propose
full strategies: accepted points are independently replayed over Fraction.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import random
import sys
import time

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix

ROOT = next(p for p in Path(__file__).resolve().parents
            if (p / 'customer_attraction/__init__.py').is_file())
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tests/audits'))
from customer_attraction import ExactSPESolver, StrategyCertificate, verify_certificate
from customer_attraction_strategy_lp import (StrategyCone, payoff_row, coverage_row,
    integer_clones, independently_verify, instance_from_clones, serializable, dot)


def seed_cone(p, m, path, seed, count_seed=False):
    r = [0] * ((1 << p) - 1)
    for a in range(p):
        r[(1 << a)-1] = (path.count(a) or 1) if count_seed else (m if a==0 else 1)
    ins = instance_from_clones(p, m, r)
    rng = random.Random(seed)
    solver = ExactSPESolver(ins)
    cert = solver.certificate(on_path=path,
        action_selector=lambda h, aa:rng.choice(aa),
        continuation_selector=lambda h, cc:rng.choice(cc))
    return StrategyCone(p,m,dict(cert.actions)), tuple(map(F,r))


def exact_reoptimize(cone, J):
    result = cone.optimize(J)
    if not result.get('certified'): return result
    r = result.pop('values')
    clones = integer_clones(r)
    assert independently_verify(cone, clones)
    ins = instance_from_clones(cone.topics,cone.players,clones)
    cert = StrategyCertificate(cone.actions,cone.root)
    checked = verify_certificate(ins,cert); checked.assert_valid()
    result.update(instance=ins.to_dict(), strategy=cert.to_dict(),
        ordered_path=checked.terminal_history, welfare=ins.welfare(cone.root),
        optimum=ins.optimal_welfare(), half_gap=2*ins.welfare(cone.root)-ins.optimal_welfare(),
        clones=clones, deviation_checks=len(cone.actions)*cone.topics)
    return result, r


def propose(cone, r, path, J, seed, max_free, seconds, fixed_clones=None):
    p,m = cone.topics,cone.players
    n=(1<<p)-1
    ties=[]
    for h,a in cone.actions.items():
        actual=dot(payoff_row(p,cone.terminals[h],a),r)
        bb=tuple(b for b in range(p) if b!=a and
            dot(payoff_row(p,cone.terminals[h+(b,)],b),r)==actual)
        if bb and h != path[:len(h)]: ties.append((h,bb))
    rng=random.Random(seed)
    rng.shuffle(ties)
    free={h for h,_ in ties[:max_free]}
    # Distinct same-count histories remain independent binary decisions.
    free=tuple(sorted(free,key=lambda h:(len(h),h)))
    fset=set(free)
    U={(h,a):n+i*p+a for i,h in enumerate(free) for a in range(p)}
    offset=n+len(free)*p
    Z={(h,a):offset+i*p+a for i,h in enumerate(free) for a in range(p)}
    nv=offset+len(free)*p
    lo=np.zeros(nv); hi=np.ones(nv); ints=np.zeros(nv,dtype=np.uint8)
    for j in Z.values(): ints[j]=1
    if fixed_clones is not None:
        scale=dot(cone.welfare,fixed_clones)
        for j,x in enumerate(fixed_clones):lo[j]=hi[j]=float(x/scale)
    rows={}
    def add(row,lb=-np.inf,ub=np.inf):
        row={j:x for j,x in row.items() if x}
        key=tuple(sorted(row.items()))
        old=rows.get(key,(-np.inf,np.inf))
        rows[key]=(max(old[0],lb),min(old[1],ub))
    def merge(a,b,scale=-1):
        rr=dict(a)
        for j,x in b.items():rr[j]=rr.get(j,0)+scale*x
        return rr
    anchors={}
    def expr(h,a):
        if h not in anchors:
            hh=h
            while len(hh)<m and hh not in fset:hh=hh+(cone.actions[hh],)
            anchors[h]=hh
        hh=anchors[h]
        if len(hh)<m:return {U[hh,a]:F(1)}
        q=tuple(hh.count(b) for b in range(p))
        if not q[a]:return {}
        return {j:x for j,x in enumerate(payoff_row(p,q,a)) if x}
    add({j:x for j,x in enumerate(cone.welfare) if x},1,1)
    # Valid for every full SPE normalized at root W=1, by summing each
    # actual mover's guarantee u_i >= |T|/m. This also bounds every U by 1.
    for a in range(p):add({j:F(1) for j in range(n) if (j+1)&(1<<a)},ub=1)
    objective=coverage_row(p,J)
    incumbent_value=dot(objective,r)
    add({j:x for j,x in enumerate(objective) if x},lb=incumbent_value)
    for h,a0 in cone.actions.items():
        if h not in fset:
            actual=expr(h,a0)
            for b in range(p):
                if b!=a0:add(merge(actual,expr(h+(b,),b)),lb=0)
            continue
        add({Z[h,a]:F(1) for a in range(p)},1,1)
        for a in range(p):
            # The complete eventual topic-utility vector follows its selected
            # child. No merger of different ordered histories is made.
            for b in range(p):
                rr=merge({U[h,b]:F(1)},expr(h+(a,),b))
                add(rr|{Z[h,a]:F(1)},ub=1)
                add(rr|{Z[h,a]:F(-1)},lb=-1)
            actual=expr(h+(a,),a)
            for b in range(p):
                if b!=a:
                    rr=merge(actual,expr(h+(b,),b))
                    rr[Z[h,a]]=F(-1)
                    add(rr,lb=-1)
    # Replay the known exact witness against the eliminated mixed model.
    # SciPy does not expose a MIP-start hook, so feasibility is checked rather
    # than implying that the numerical solver received this incumbent.
    seed_point=list(r)+[F(0)]*(nv-n)
    for (h,a),j in U.items():
        q=cone.terminals[h]
        seed_point[j]=dot(payoff_row(p,q,a),r) if q[a] else F(0)
    for (h,a),j in Z.items():seed_point[j]=F(a==cone.actions[h])
    for rr,(l,u) in rows.items():
        val=sum((x*seed_point[j] for j,x in rr),F(0))
        assert (l==-np.inf or val>=l) and (u==np.inf or val<=u), (val,l,u)
    ii=[];jj=[];xx=[];ll=[];uu=[]
    for rr,(l,u) in rows.items():
        i=len(ll);ll.append(l);uu.append(u)
        for j,x in rr:ii.append(i);jj.append(j);xx.append(float(x))
    A=coo_matrix((xx,(ii,jj)),shape=(len(ll),nv)).tocsc()
    cost=np.zeros(nv);cost[:n]=-np.asarray(coverage_row(p,J),float)
    started=time.monotonic()
    result=milp(cost,integrality=ints,bounds=Bounds(lo,hi),
        constraints=LinearConstraint(A,ll,uu),
        options={'time_limit':seconds,'mip_rel_gap':0.0,'presolve':True})
    meta={'seed':seed,'max_free':max_free,'exact_tie_nodes_available':len(ties),
        'free_histories':free,'variables':nv,'binary':len(Z),'rows':len(ll),
        'status':int(result.status),'message':result.message,
        'seconds':time.monotonic()-started,
        'floating_value':None if result.fun is None else -float(result.fun),
        'floating_bound_not_certificate':getattr(result,'mip_dual_bound',None),
        'fixed_clones':fixed_clones is not None,
        'known_exact_feasible_value':incumbent_value,
        'known_seed_verified_in_eliminated_model':True,
        'seed_was_not_passed_as_mip_start':True,
        'scope':'only selected tie-node fan; all ordered-history deviations enforced'}
    if result.x is None:return None,meta
    acts=dict(cone.actions)
    for h in free:
        a=max(range(p),key=lambda a:result.x[Z[h,a]])
        assert result.x[Z[h,a]]>.9
        acts[h]=a
    found=StrategyCone(p,m,acts)
    assert found.root==cone.root
    meta['changed_free_actions']=sum(acts[h]!=cone.actions[h] for h in free)
    return found,meta


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--topics',type=int,default=7)
    ap.add_argument('--path',default='0,0,0,0,1')
    ap.add_argument('--portfolio',default='0,2,3,4,5')
    ap.add_argument('--seed',type=int,default=651021)
    ap.add_argument('--count-seed',action='store_true')
    ap.add_argument('--free',type=int,default=24)
    ap.add_argument('--seconds',type=float,default=20)
    ap.add_argument('--rounds',type=int,default=3)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    path=tuple(map(int,args.path.split(','))); J=tuple(map(int,args.portfolio.split(',')))
    cone,r=seed_cone(args.topics,len(path),path,args.seed,args.count_seed)
    initial,r=exact_reoptimize(cone,J)
    out={'parameters':vars(args)|{'output':str(args.output)},
        'universal_result':False,'initial':initial,'rounds':[]}
    args.output.write_text(json.dumps(serializable(out),indent=2)+'\n')
    for i in range(args.rounds):
        new,meta=propose(cone,r,path,J,args.seed+i,args.free,args.seconds)
        rec={'milp':meta}
        if new is not None:
            exact,rr=exact_reoptimize(new,J)
            rec['exact']=exact
            if exact.get('certified') and exact['value']>=dot(coverage_row(cone.topics,J),r):
                cone,r=new,rr
        out['rounds'].append(rec)
        args.output.write_text(json.dumps(serializable(out),indent=2)+'\n')
        print(json.dumps(serializable({'round':i,'milp':meta,
            'exact':None if 'exact' not in rec else {k:v for k,v in rec['exact'].items()
                if k not in ('strategy','instance','clones','dual_support')}})),flush=True)


if __name__=='__main__':main()
