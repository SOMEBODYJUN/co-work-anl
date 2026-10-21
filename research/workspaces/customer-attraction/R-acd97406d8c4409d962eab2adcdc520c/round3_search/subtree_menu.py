"""Whole-subtree multiple-choice neighbourhood of complete-history SPE cones.

Every option is an action map on an entire ordered-history root-child subtree.
MILP chooses one option for each root action and retains every root incentive.
Its floating incumbent only selects a complete strategy; exact cone recovery and
a self-contained Fraction checker, which does not import the game implementation,
must accept an integer point before any mathematical claim is exported.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
import hashlib
import json
from pathlib import Path
import random
import sys
import time

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, linprog, milp
from scipy.sparse import coo_matrix

ROOT = next(p for p in Path(__file__).resolve().parents
            if (p / 'customer_attraction/__init__.py').is_file())
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT/'tests/audits'))
from customer_attraction import ExactSPESolver, StrategyCertificate
from customer_attraction_strategy_lp import (StrategyCone, coverage_row, payoff_row,
    instance_from_clones, integer_clones, serializable, dot)


def inc(k, a): return k[:a] + (k[a]+1,) + k[a+1:]


def source_seeds(p, m, q):
    """A few structured source geometries, rather than a random instance sweep."""
    n=(1<<p)-1
    weights={1:m, **{1<<a:1 for a in range(1,p)}}
    yield 'private_big', tuple(weights.get(b,0) for b in range(1,n+1))
    weights={1<<a:max(1,q[a]) for a in range(p)}
    yield 'private_count', tuple(weights.get(b,0) for b in range(1,n+1))
    if p>=5:
        for label,weights in [
            ('reply_cycle',{2:1,4:1,8:1,9:1,16:1,17:2,26:1,28:1}),
            ('overlap_cycle',{1:10,2:4,4:8,6:2,8:16,12:1,16:32,17:1,24:2}),
            ('residual_reply',{2:3,4:3,9:2,17:2,26:2*m,28:2*m})]:
            weights=dict(weights)
            for a in range(5,p): weights[1<<a]=1
            yield label,tuple(weights.get(b,0) for b in range(1,n+1))


class Option:
    def __init__(self,p,m,branch,actions,label):
        self.p,self.m,self.branch,self.actions,self.label=p,m,branch,actions,label
        expected={h for depth in range(1,m) for h in product(range(p),repeat=depth)
                  if h[0]==branch}
        assert set(actions)==expected
        terms={}
        for depth in range(m,0,-1):
            for tail in product(range(p),repeat=depth-1):
                h=(branch,)+tail
                terms[h]=(tuple(h.count(a) for a in range(p)) if depth==m
                          else terms[h+(actions[h],)])
        self.target=terms[(branch,)]
        rows=set()
        for h,a in actions.items():
            actual=payoff_row(p,terms[h],a)
            for b in range(p):
                if b!=a:
                    other=payoff_row(p,terms[h+(b,)],b)
                    row=tuple(x-y for x,y in zip(actual,other))
                    if any(row): rows.add(row)
        self.rows=frozenset(rows)
        self.digest=hashlib.sha256(repr(sorted(actions.items())).encode()).hexdigest()


def sample_subtree(solver,branch,target,rng,mode):
    p,m=solver.instance.topic_count,solver.instance.players
    actions={}
    def expand(h,k,wanted):
        if len(h)==m: assert wanted==k; return
        floor=solver.threshold(k)
        choices=[a for a in range(p) if wanted in solver.outcomes(inc(k,a))
                 and solver._utility(wanted,a)>=floor]
        a=rng.choice(choices); actions[h]=a; actual=solver._utility(wanted,a)
        for b in range(p):
            child=inc(k,b)
            if b==a: next_target=wanted
            else:
                menu=[c for c in solver.outcomes(child) if solver._utility(c,b)<=actual]
                if mode=='min':
                    value=min(solver._utility(c,b) for c in menu)
                    menu=[c for c in menu if solver._utility(c,b)==value]
                elif mode=='max':
                    value=max(solver._utility(c,b) for c in menu)
                    menu=[c for c in menu if solver._utility(c,b)==value]
                elif mode=='lowW':
                    value=min(solver.instance.welfare(c) for c in menu)
                    menu=[c for c in menu if solver.instance.welfare(c)==value]
                elif mode!='uniform': raise ValueError(mode)
                next_target=rng.choice(sorted(menu))
            expand(h+(b,),child,next_target)
    k=inc((0,)*p,branch)
    assert target in solver.outcomes(k)
    expand((branch,),k,target)
    return actions


def generate_menus(p,m,q,root_action,rng,variants,extra_sources=()):
    menus=[[] for _ in range(p)]; seen=[set() for _ in range(p)]
    sources=list(source_seeds(p,m,q))+list(extra_sources)
    for label,r in sources:
        solver=ExactSPESolver(instance_from_clones(p,m,r))
        for b in range(p):
            child=inc((0,)*p,b); candidates=sorted(solver.outcomes(child))
            if b==root_action:
                targets=[q] if q in candidates else []
            else:
                low=min(solver._utility(c,b) for c in candidates)
                low_targets=[c for c in candidates if solver._utility(c,b)==low]
                lowW=min(solver.instance.welfare(c) for c in candidates)
                lowW_targets=[c for c in candidates if solver.instance.welfare(c)==lowW]
                targets=list(dict.fromkeys([rng.choice(low_targets),rng.choice(lowW_targets)]
                    +rng.sample(candidates,min(variants,len(candidates)))))
            for target in targets:
                for mode in ('min','max','uniform')[:variants]:
                    actions=sample_subtree(solver,b,target,rng,mode)
                    option=Option(p,m,b,actions,label+':'+mode)
                    if option.digest not in seen[b]:
                        seen[b].add(option.digest);menus[b].append(option)
    assert all(menus)
    return menus


def choose_menu(p,m,q,root_action,menus,objective,seconds):
    n=(1<<p)-1
    z={};idx=n
    for b,opts in enumerate(menus):
        for j in range(len(opts)): z[b,j]=idx;idx+=1
    rows={}
    def add(rr,lo=-np.inf,hi=np.inf):
        key=tuple(sorted((j,v) for j,v in rr.items() if v))
        old=rows.get(key,(-np.inf,np.inf))
        rows[key]=(max(lo,old[0]),min(hi,old[1]))
    w=coverage_row(p,[a for a,c in enumerate(q) if c])
    actual=payoff_row(p,q,root_action)
    add({j:v for j,v in enumerate(w) if v},1,1)
    # At a genuine SPE every actual player guarantees |T|/m; summing yields
    # |T| <= W=1. Thus any utility and any payoff difference lies in [0,1]
    # and [-1,1], respectively. Conditional constant one is rigorous.
    for a in range(p): add({j:1 for j in range(n) if (j+1)&(1<<a)},hi=1)
    conditional_groups=0; common_rows=set()
    for b,opts in enumerate(menus):
        add({z[b,j]:1 for j in range(len(opts))},1,1)
        owners=defaultdict(list)
        for j,opt in enumerate(opts):
            if b==root_action: assert opt.target==q
            for row in opt.rows: owners[row].append(j)
            # Keep every genuine root comparison, including off-root branches.
            dev=payoff_row(p,opt.target,b)
            row=tuple(x-y for x,y in zip(actual,dev))
            if any(row): owners[row].append(j)
        for row,jj in owners.items():
            jj=sorted(set(jj));rr={j:v for j,v in enumerate(row) if v}
            if len(jj)==len(opts): common_rows.add(row)
            else:
                for j in jj: rr[z[b,j]]=-1
                add(rr,lo=-1);conditional_groups+=1
    for row in common_rows: add({j:v for j,v in enumerate(row) if v},lo=0)
    ii=[];jj=[];xx=[];ll=[];uu=[]
    for row,(lo,hi) in rows.items():
        i=len(ll);ll.append(lo);uu.append(hi)
        for j,v in row:ii.append(i);jj.append(j);xx.append(float(v))
    A=coo_matrix((xx,(ii,jj)),shape=(len(ll),idx)).tocsc()
    cost=np.zeros(idx);cost[:n]=-np.array(objective,float)
    ints=np.zeros(idx,dtype=np.uint8);ints[n:]=1
    began=time.monotonic()
    result=milp(cost,integrality=ints,bounds=Bounds(np.zeros(idx),np.ones(idx)),
        constraints=LinearConstraint(A,ll,uu),options={'time_limit':seconds,'mip_rel_gap':0.0})
    meta={'variables':idx,'binary_options':idx-n,'rows':len(ll),
          'menu_lengths':list(map(len,menus)),'conditional_row_groups':conditional_groups,
          'common_rows':len(common_rows),'seconds':time.monotonic()-began,
          'status':int(result.status),'message':result.message,
          'floating_value':None if result.fun is None else -float(result.fun),
          'floating_bound_not_a_mathematical_certificate':True,
          'all_root_constraints_retained':True}
    if result.x is None: return None,meta
    actions={():root_action};selected=[]
    for b,opts in enumerate(menus):
        j=max(range(len(opts)),key=lambda j:result.x[z[b,j]])
        assert result.x[z[b,j]]>.9
        actions.update(opts[j].actions)
        selected.append({'branch':b,'index':j,'target':opts[j].target,
                         'label':opts[j].label,'digest':opts[j].digest})
    cone=StrategyCone(p,m,actions)
    assert cone.root==q
    meta['selected']=selected
    return cone,meta


def exact_optimize(cone,objective,J,target):
    result=linprog(-np.array(objective,float),A_ub=-cone.matrix,
        b_ub=np.zeros(len(cone.rows)),A_eq=[cone.welfare],b_eq=[1],
        bounds=(0,None),method='highs')
    if not result.success: return {'certified':False,'status':result.message}
    values=tuple(F(float(x)).limit_denominator(10**7) for x in result.x)
    if not cone.verify(values) or dot(cone.welfare,values)!=1:
        values=cone.recover_vertex(result.x)
    if values is None or not cone.verify(values) or dot(cone.welfare,values)!=1:
        return {'certified':False,'status':'exact_primal_recovery_failed'}
    clones=integer_clones(values)
    cert=StrategyCertificate(cone.actions,cone.root).to_dict()
    checked=independent_check(cone.topics,cone.players,clones,cert)
    beta=F(float(-result.eqlin.marginals[0])).limit_denominator(10**7)
    mu=tuple(F(float(-x)).limit_denominator(10**7) for x in result.ineqlin.marginals)
    dual_ok=all(x>=0 for x in mu) and all(
        beta*w-sum(x*row[j] for x,row in zip(mu,cone.rows))>=v
        for j,(w,v) in enumerate(zip(cone.welfare,objective)))
    objective_value=dot(objective,values)
    u=checked['topic_payoffs'][target];w=F(checked['welfare']);opt=checked['optimum']
    return {'certified':True,'objective_value':objective_value,
        'dual_bound':beta if dual_ok else None,'dual_optimal':dual_ok and beta==objective_value,
        'dual_support':[(j,x) for j,x in enumerate(mu) if x] if dual_ok else [],
        'integer_clones':clones,'strategy':cert,'independent_check':checked,
        'portfolio':J,'target':target,'OPT_over_target_payoff':F(opt)/u,
        'welfare_ratio':F(opt)/w,'weak_OPT_floor_gap':2*cone.players*u-opt,
        'weak_residual_floor_gap':cone.players*u-(opt-w),
        'half_gap':2*w-opt}


def independent_check(p,m,clones,certificate):
    """Definition-level replay, no cone, solver, Instance, or payoff-row calls."""
    actions={tuple(r['history']):r['action'] for r in certificate['actions']}
    expected={h for d in range(m) for h in product(range(p),repeat=d)}
    assert len(actions)==len(certificate['actions']) and set(actions)==expected
    assert all(a in range(p) for a in actions.values())
    assert len(clones)==(1<<p)-1 and all(isinstance(x,int) and x>=0 for x in clones)
    @lru_cache(None)
    def terminal(h):
        if len(h)==m:return h
        return terminal(h+(actions[h],))
    @lru_cache(None)
    def payoff(path,a):
        u=F(0)
        for mask,count in enumerate(clones,1):
            if count and mask>>a&1:
                denominator=sum(bool(mask>>b&1) for b in path)
                assert denominator>0
                u+=F(count,denominator)
        return u
    strict=tied=0;root_comparisons=[]
    for h,a in actions.items():
        actual=payoff(terminal(h),a)
        for b in range(p):
            if b==a:continue
            alternate=payoff(terminal(h+(b,)),b)
            assert actual>=alternate,(h,a,b,actual,alternate)
            strict+=actual>alternate;tied+=actual==alternate
            if not h:root_comparisons.append((b,actual,alternate))
    path=terminal(());q=tuple(path.count(a) for a in range(p))
    assert q==tuple(certificate['terminal_counts'])
    def coverage(topics):
        topic_mask=sum(1<<a for a in topics)
        return sum(count for mask,count in enumerate(clones,1) if mask&topic_mask)
    w=coverage(set(path));opt=max(coverage(J) for J in combinations(range(p),min(p,m)))
    topic_payoffs=[payoff(path,a) if q[a] else F(0) for a in range(p)]
    assert sum(q[a]*topic_payoffs[a] for a in range(p))==w
    return {'verified':True,'histories':len(actions),'nonself_comparisons':strict+tied,
        'strict':strict,'ties':tied,'path':path,'root_comparisons':root_comparisons,
        'welfare':w,'optimum':opt,'topic_payoffs':topic_payoffs,
        'client_count':sum(clones),'positive_types':sum(bool(x) for x in clones)}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',default='3,2,0,0,0,0,0')
    ap.add_argument('--root-action',type=int,default=0)
    ap.add_argument('--portfolio',default='2,3,4,5,6')
    ap.add_argument('--target',type=int,default=1)
    ap.add_argument('--objective',choices=['half','individual','residual'],default='half')
    ap.add_argument('--variants',type=int,default=2)
    ap.add_argument('--source-result',type=Path,action='append',default=[],
                    help='add exact integer endpoints of an earlier run as subtree-menu sources')
    ap.add_argument('--all-portfolios',action='store_true',
                    help='after MIP selection, float-scan every legal comparison portfolio in that fixed cone')
    ap.add_argument('--seconds',type=float,default=15)
    ap.add_argument('--seed',type=int,default=64261021)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();q=tuple(map(int,args.root.split(',')));p=len(q);m=sum(q)
    J=tuple(map(int,args.portfolio.split(',')));assert q[args.root_action] and q[args.target]
    assert len(set(J))==len(J)<=m
    v=coverage_row(p,J);w=coverage_row(p,[a for a,c in enumerate(q) if c])
    u=payoff_row(p,q,args.target)
    objective=(v if args.objective=='half' else tuple(
        vv-(2*m*uu if args.objective=='individual' else ww+m*uu)
        for vv,ww,uu in zip(v,w,u)))
    began=time.monotonic()
    extra_sources=[]
    for source in args.source_result:
        saved=json.loads(source.read_text()); endpoint=saved['exact']
        assert endpoint['certified']
        clones=tuple(endpoint['integer_clones']); assert len(clones)==(1<<p)-1
        independent_check(p,m,clones,endpoint['strategy'])
        extra_sources.append((source.stem,clones))
    menus=generate_menus(p,m,q,args.root_action,random.Random(args.seed),args.variants,extra_sources)
    construction=time.monotonic()-began
    cone,meta=choose_menu(p,m,q,args.root_action,menus,objective,args.seconds)
    if cone is not None and args.all_portfolios:
        best=None
        for candidate_J in combinations(range(p),min(p,m)):
            vv=coverage_row(p,candidate_J)
            obj=(vv if args.objective=='half' else tuple(
                vj-(2*m*uj if args.objective=='individual' else wj+m*uj)
                for vj,wj,uj in zip(vv,w,u)))
            out=linprog(-np.array(obj,float),A_ub=-cone.matrix,
                b_ub=np.zeros(len(cone.rows)),A_eq=[cone.welfare],b_eq=[1],
                bounds=(0,None),method='highs')
            if out.success and (best is None or -out.fun>best[0]):
                best=(-out.fun,candidate_J,obj)
        assert best is not None
        _,J,objective=best
        meta['fixed_cone_all_portfolio_float_scan']=True
        meta['fixed_cone_selected_portfolio']=J
    exact=exact_optimize(cone,objective,J,args.target) if cone is not None else None
    report={'scope':'finite whole-subtree joint neighbourhood; complete SPE witnesses only',
        'universal_claim_proved':False,'parameters':dict(vars(args)),
        'menu_construction_seconds':construction,'milp':meta,'exact':exact}
    report['parameters']['output']=str(args.output)
    report['parameters']['source_result']=list(map(str,args.source_result))
    args.output.write_text(json.dumps(serializable(report),indent=2)+'\n')
    small={k:v for k,v in report.items() if k!='exact'}
    small['exact']=None if exact is None else {k:v for k,v in exact.items()
        if k not in ('integer_clones','strategy','dual_support')}
    print(json.dumps(serializable(small)),flush=True)


if __name__=='__main__':main()
