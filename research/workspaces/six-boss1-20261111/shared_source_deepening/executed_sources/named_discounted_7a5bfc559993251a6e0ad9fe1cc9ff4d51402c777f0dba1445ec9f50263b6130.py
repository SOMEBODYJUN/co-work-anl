#!/usr/bin/env python3
"""Same-source discounted terminal map, seeded by genuine H/M themes.

All fixed query weights, source weight, prices and capacities are globally
nonnegative.  One normalized source budget funds the whole geometric orbit.
Y-average occurs only in the linear fixed query menu, never as a theme state.
Discovery is numerical; every reported row and value is rebuilt with Fraction.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
import gzip
import hashlib
from itertools import product
import json
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
RUN = HERE.parent
sys.path.insert(0, str(RUN/'cross_branch_math'))
import new_theme_early_projections as old
sys.path.insert(0, str(RUN.parent/'six-boss2-20261111-cross/coverage_bridge'))
from discounted_requery import closed_values
from previous_theme_requery import policy_inverses

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix


def share(n,d):
    return F(n,d) if n else F()


def dot(a,b):
    return sum((x*y for x,y in zip(a,b) if x and y), F())


def canonical(row):
    return json.dumps([[int(i),str(F(v))] for i,v in sorted(row) if F(v)],separators=(',',':')).encode()


def names_for(family,columns,indices,previous=False):
    c=columns[indices[0]]
    named=(['M'] if family=='M1' else [])+[f'H{i}' for i in range(len(c['hidden']))]
    queries=[f'A{i+1}' for i in range(6)]+named+['Y-average']
    parameters=['source','alpha_middle','alpha_last','beta_middle','beta_last']
    parameters += ['mu_'+q for q in queries]+['mu_current']
    if previous: parameters += ['mu_previous']
    return named,queries,parameters


def local_feature(p,ell,t,c,s,qs,a=None):
    z=p+t+s+c;den=p+t+s+1
    tail_share=share(c,z)
    ans=(share(t,z),F(s,ell+1),F(c,ell+1),F(s),F(c))
    ans+=tuple(q/den-tail_share for q in qs)+(F(t,den)-tail_share,)
    if a is not None:ans+=(F(a,den)-tail_share,)
    return ans


def exact_projection(case,k,parameters,theta,previous=False,return_audit=False):
    p,ell,a0,t0,qs=case
    if not previous:
        edge={(t,c):min(dot(local_feature(p,ell,t,c,s,qs),parameters)
                       for s in range(k-1)) for t,c in product((0,1),repeat=2)}
        psi=closed_values(edge,theta)
        vals=tuple(x/(1-theta) for x in psi)
        slack=[dot(local_feature(p,ell,t,c,s,qs),parameters)+theta*vals[c]-vals[t]
               for t,c in product((0,1),repeat=2) for s in range(k-1)]
        assert min(slack)>=0
        for t in (0,1):assert vals[t]==min(edge[t,c]+theta*vals[c] for c in (0,1))
        result=psi[t0]
    else:
        edge={(a,t,c):min(dot(local_feature(p,ell,t,c,s,qs,a),parameters)
                         for s in range(k-1)) for a,t,c in product((0,1),repeat=3)}
        candidates=[]
        states=tuple(product((0,1),repeat=2))
        for policy,inverse in policy_inverses(theta):
            cost=[edge[a,t,policy[i]] for i,(a,t) in enumerate(states)]
            candidates.append(tuple(dot(row,cost) for row in inverse))
        vals=tuple(min(v[i] for v in candidates) for i in range(4))
        assert vals in candidates
        slack=[dot(local_feature(p,ell,t,c,s,qs,a),parameters)+theta*vals[2*t+c]-vals[2*a+t]
               for a,t,c in product((0,1),repeat=3) for s in range(k-1)]
        assert min(slack)>=0
        for a,t in states:assert vals[2*a+t]==min(edge[a,t,c]+theta*vals[2*t+c] for c in (0,1))
        result=(1-theta)*vals[2*a0+t0]
    if return_audit:return result,len(slack),min(slack),tuple(vals)
    return result


def state_case(column,actual,source,forced,previous_theme,queries):
    t=old.feature(column,actual,forced)
    a=old.feature(column,actual,previous_theme) if previous_theme else F()
    assert t in (0,1) and a in (0,1)
    return (sum(actual[:source]),sum(actual[:5]),int(a),int(t),
            tuple(old.feature(column,actual,q) for q in queries))


def state_measure(columns,hist,masses,indices,source,forced,previous_theme,queries):
    out=defaultdict(F)
    for j in indices:
        if not masses[j]:continue
        c=columns[j];a=tuple(map(int,hist[c['hist_column']]['actual_bits']))
        out[state_case(c,a,source,forced,previous_theme,queries)]+=masses[j]
    return dict(out)


def budget(source,profits,K,dim):
    middle=4-source
    return (profits[source],middle*profits[5],profits[5],middle*K,K)+(F(),)*(dim-5)


def discover_case(columns,hist,masses,profits,families,family,source,forced,previous_theme,theta,
                  baseline=None,construct_all=False):
    started=time.monotonic();previous=previous_theme is not None
    named,queries,pnames=names_for(family,columns,families[family],previous)
    dim=len(pnames);k=6-source;ns=4 if previous else 2
    measure=state_measure(columns,hist,masses,families[family],source,forced,previous_theme,queries)
    keys=list(measure);nv=dim+ns*len(keys)
    rr=[];cc=[];vv=[];rhs=[]
    for vi,(p,ell,a0,t0,qs) in enumerate(keys):
        for a,t,c,s in product(range(2 if previous else 1),(0,1),(0,1),range(k-1)):
            row=len(rhs)
            for j,x in enumerate(local_feature(p,ell,t,c,s,qs,a if previous else None)):
                if x:rr.append(row);cc.append(j);vv.append(-float(x))
            now=2*a+t if previous else t
            nxt=2*t+c if previous else c
            rr.extend((row,row));cc.extend((dim+ns*vi+now,dim+ns*vi+nxt));vv.extend((1.,-float(theta)))
            rhs.append(0.)
    mat=coo_matrix((vv,(rr,cc)),shape=(len(rhs),nv)).tocsr()
    wallet=budget(source,profits,masses[0],dim)
    objective=list(map(float,wallet))+[0.]*(nv-dim)
    for vi,case in enumerate(keys):
        init=2*case[2]+case[3] if previous else case[3]
        objective[dim+ns*vi+init]=-(1-float(theta))*float(measure[case])
    eq=coo_matrix(([1.]*dim,([0]*dim,list(range(dim)))),shape=(1,nv)).tocsr()
    bounds=[(0,None)]*dim+[(None,None)]*(nv-dim)
    if k==2:bounds[1]=bounds[3]=(0,0)
    solution=linprog(objective,A_ub=mat,b_ub=rhs,A_eq=eq,b_eq=[1.],bounds=bounds,
                     method='highs',options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
    record={'family':family,'actual_source_zero_based':source,'forced':forced,
            'previous_theme':previous_theme,'theta':str(theta),'state_count':ns,
            'queries':queries,'parameter_names':pnames,'positive_visible_types':len(keys),
            'lp_variables':nv,'lp_inequalities':len(rhs),'success':bool(solution.success),
            'normalization':'sum of all globally nonnegative parameters = 1'}
    if not solution.success:
        record['message']=solution.message;return record
    params=tuple(F(float(x)).limit_denominator(1000000) if x>1e-10 else F() for x in solution.x[:dim])
    norm=sum(params,F());assert norm>0
    params=tuple(x/norm for x in params)
    assert min(params)>=0 and sum(params,F())==1
    cache={}
    def project(case):
        if case not in cache:cache[case]=exact_projection(case,k,params,theta,previous,True)
        return cache[case][0]
    slack=dot(wallet,params)-sum((mass*project(case) for case,mass in measure.items()),F())
    record.update(float_objective=float(solution.fun),parameters={n:str(v) for n,v in zip(pnames,params) if v},
                  parameters_full=list(map(str,params)),exact_slack=str(slack),exact_slack_float=float(slack))
    if slack<0 or construct_all:
        row={}
        cap=(k-2)*params[3]+params[4]
        if cap:row[0]=cap
        for j in families[family]:
            c=columns[j];a=tuple(map(int,hist[c['hist_column']]['actual_bits']));total=sum(a)
            case=state_case(c,a,source,forced,previous_theme,queries)
            value=params[0]*share(a[source],total)+((k-2)*params[1]+params[2])*share(a[5],total)-project(case)
            if value:row[j]=value
        assert sum((v*masses[j] for j,v in row.items()),F())==slack
        encoded=canonical(row.items())
        record.update(coefficients=json.loads(encoded),vector_sha256=hashlib.sha256(encoded).hexdigest(),
                      baseline_matches=[] if baseline is None else baseline.get(encoded,[]),
                      full_column_count=len(columns),original_columns=4849,
                      all_zero_mass_family_columns_constructed=True,
                      full_visible_types=len(cache),bellman_inequalities_checked=sum(v[1] for v in cache.values()),
                      minimum_bellman_slack=str(min(v[2] for v in cache.values())))
    record['elapsed_seconds']=time.monotonic()-started
    return record


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--point',type=Path,default=RUN/'zz_closure_lp/round2/augmented_lp_exact.json')
    ap.add_argument('--matrix',type=Path,default=RUN/'zz_closure_lp/round2/exact_matrix.json.gz')
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--sources',default='5,4,3,2,1')
    ap.add_argument('--families',default='M1,B2,B3,B4')
    ap.add_argument('--thetas',default='0,1/4,1/2,3/4,9/10')
    ap.add_argument('--previous',choices=('none','A6','all-named'),default='none')
    ap.add_argument('--forced',default='all')
    args=ap.parse_args();raw=args.point.read_bytes();point=json.loads(raw)
    assert hashlib.sha256(raw).hexdigest()=='bf47390017e37f49f47a8f89126eb8e812982e16bd535adb555f042c178a2ca3'
    columns,hist,masses,profits,families,_=old.topology(point)
    matrix_raw=args.matrix.read_bytes();matrix=json.loads(gzip.decompress(matrix_raw))
    desc=lambda c:{k:v for k,v in c.items() if k!='weight'}
    assert [desc(c) for c in columns]==matrix['columns']
    baseline=defaultdict(list)
    for i,row in enumerate(matrix['rows']):baseline[canonical(row)].append({'index':i,'name':matrix['row_names'][i]})
    out={'scope':'Genuine named H/M seeds; same-source discounted terminal requery; finite sampled discounts and full global nonnegative parameter cone at each case; no SPE or half claim',
         'input':str(args.point.resolve()),'input_sha256':hashlib.sha256(raw).hexdigest(),
         'matrix':str(args.matrix.resolve()),'matrix_sha256':hashlib.sha256(matrix_raw).hexdigest(),
         'input_W':point['W'],'columns':len(columns),'baseline_rows':len(matrix['rows']),
         'actual_utilities':list(map(str,profits)),'K':str(masses[0]),'results':[],
         'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    start=time.monotonic()
    for family in args.families.split(','):
        named,_,_=names_for(family,columns,families[family])
        forceds=named if args.forced=='all' else [x for x in args.forced.split(',') if x in named]
        for source1 in map(int,args.sources.split(',')):
            for forced in forceds:
                prevs=[None] if args.previous=='none' else (['A6'] if args.previous=='A6' else [x for x in named if x!=forced])
                for previous,theta in product(prevs,map(F,args.thetas.split(','))):
                    record=discover_case(columns,hist,masses,profits,families,family,source1-1,forced,previous,theta,baseline)
                    out['results'].append(record)
                    summary={k:record[k] for k in ('family','actual_source_zero_based','forced','previous_theme','theta','success')}
                    if record['success']:summary.update(exact_slack_float=record['exact_slack_float'])
                    print(json.dumps(summary,ensure_ascii=False),flush=True)
                    out['cases']=len(out['results']);out['negative_cases']=sum(F(r.get('exact_slack','0'))<0 for r in out['results'])
                    out['elapsed_seconds']=time.monotonic()-start
                    args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('cases','negative_cases','elapsed_seconds')}),flush=True)


if __name__=='__main__':main()
