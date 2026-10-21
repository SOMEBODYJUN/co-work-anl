"""Standalone standard-library replay of subtree-menu results.

Does not import the searcher, model, payoff helpers, equilibrium solver, or LP.
It follows each branch forward and evaluates the original unit customers.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
import argparse
import hashlib
import json
from pathlib import Path


def verify(path):
    raw=path.read_bytes(); report=json.loads(raw); end=report['exact']
    if end is None or not end['certified']:
        return {'file':path.name,'exact_endpoint_present':False}
    q=tuple(map(int,report['parameters']['root'].split(',')));p=len(q);m=sum(q)
    clones=end['integer_clones'];assert len(clones)==(1<<p)-1
    assert all(type(x) is int and x>=0 for x in clones)
    records=end['strategy']['actions'];acts={tuple(x['history']):x['action'] for x in records}
    expected={h for depth in range(m) for h in product(range(p),repeat=depth)}
    assert len(acts)==len(records) and set(acts)==expected
    assert all(type(a) is int and 0<=a<p for a in acts.values())
    customers=[mask for mask,count in enumerate(clones,1) for _ in range(count)]
    @lru_cache(None)
    def forward(h):
        while len(h)<m: h=h+(acts[h],)
        return h
    @lru_cache(None)
    def utility(terminal,a):
        return sum((F(1,sum(bool(mask&(1<<b)) for b in terminal))
                    for mask in customers if mask&(1<<a)),F(0))
    @lru_cache(None)
    def coeff(terminal,a):
        return tuple(F(1,sum(bool(mask&(1<<b)) for b in terminal)) if mask&(1<<a)
                     else F(0) for mask in range(1,1<<p))
    strict=tied=0;root=[];rows=set()
    for h in sorted(acts,key=lambda h:(len(h),h)):
        a=acts[h];selected=forward(h);u=utility(selected,a)
        ca=coeff(selected,a)
        for b in range(p):
            if b==a:continue
            alternative=forward(h+(b,));v=utility(alternative,b)
            assert u>=v,(path.name,h,a,b,u,v)
            strict+=u>v;tied+=u==v
            if not h:root.append((b,str(u),str(v)))
            cb=coeff(alternative,b);row=tuple(x-y for x,y in zip(ca,cb))
            if any(row):rows.add(row)
    terminal=forward(())
    assert tuple(terminal.count(a) for a in range(p))==q==tuple(end['strategy']['terminal_counts'])
    chosen_mask=sum(1<<a for a in set(terminal))
    w=sum(bool(mask&chosen_mask) for mask in customers)
    def coverage(J):
        mask=sum(1<<a for a in J)
        return sum(bool(mask&other) for other in customers)
    opt=max(coverage(J) for J in combinations(range(p),min(p,m)))
    target=end['target'];u=utility(terminal,target);J=end['portfolio']
    mode=report['parameters']['objective'];comparison=coverage(J)
    value=F(comparison,w)
    if mode=='individual':value-=F(2*m)*u/w
    if mode=='residual':value-=1+F(m)*u/w
    assert value==F(end['objective_value'])
    assert F(opt,w)==F(end['welfare_ratio'])
    assert F(opt)/u==F(end['OPT_over_target_payoff'])
    assert 2*w-opt==F(end['half_gap'])
    assert 2*m*u-opt==F(end['weak_OPT_floor_gap'])
    assert m*u-(opt-w)==F(end['weak_residual_floor_gap'])
    saved=end['independent_check']
    assert (saved['histories'],saved['nonself_comparisons'],saved['strict'],saved['ties'])==(
        len(acts),strict+tied,strict,tied)
    assert (saved['welfare'],saved['optimum'],tuple(saved['path']))==(w,opt,terminal)
    dual_verified=False
    if end['dual_bound'] is not None:
        rows=sorted(rows);mu=[F(0)]*len(rows)
        for j,x in end['dual_support']:
            assert type(j) is int and j in range(len(rows)) and mu[j]==0
            mu[j]=F(x)
        assert all(x>=0 for x in mu)
        beta=F(end['dual_bound']);ut=coeff(terminal,target)
        Jmask=sum(1<<a for a in J)
        for j,mask in enumerate(range(1,1<<p)):
            v=F(bool(mask&Jmask));ww=F(bool(mask&chosen_mask))
            if mode=='individual':v-=2*m*ut[j]
            if mode=='residual':v-=ww+m*ut[j]
            assert beta*ww-sum((x*row[j] for x,row in zip(mu,rows)),F(0))>=v
        if end['dual_optimal']:assert beta==value
        dual_verified=True
    return {'file':path.name,'sha256':hashlib.sha256(raw).hexdigest(),
        'histories':len(acts),'nonself_comparisons':strict+tied,
        'unit_customers':len(customers),'strict':strict,'ties':tied,'path':terminal,
        'root_comparisons':root,'welfare':w,'optimum':opt,
        'welfare_ratio':str(F(opt,w)),'objective_value':str(value),
        'half_gap':2*w-opt,'OPT_over_target_payoff':str(F(opt)/u),
        'weak_OPT_floor_gap':str(2*m*u-opt),
        'weak_residual_floor_gap':str(m*u-(opt-w)),
        'exact_fixed_cone_dual_verified':dual_verified}


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('files',nargs='+',type=Path)
    ap.add_argument('--output',type=Path);args=ap.parse_args()
    report={'scope':'unit-customer direct full-history SPE and exact fixed-cone dual replay',
            'reports':[verify(p) for p in args.files]}
    if args.output:args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report),flush=True)
