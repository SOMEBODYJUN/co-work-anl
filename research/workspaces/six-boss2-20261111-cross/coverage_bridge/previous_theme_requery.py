#!/usr/bin/env python3
"""Four-state discounted requery, retaining the previous legal query theme.

State (a,t) moves to (t,c).  At every genuine terminal node, the previous
orbit theme is an available legal query, including the freely chosen initial
previous theme.  It is never asserted to have been played in source history.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

import joint_discounted_requery as base

NAMES=base.NAMES+["mu_previous"]
DIM=len(NAMES)
STATES=tuple(itertools.product((0,1),repeat=2))


def feature(p,ell,a,t,c,s,qs):
    return base.feature(p,ell,t,c,s,qs)+(F(a,p+t+s+1)-base.share(c,p+t+s+c),)


def rational_solve(matrix,rhs):
    aug=[list(map(F,row))+[F(r)] for row,r in zip(matrix,rhs)]
    n=len(rhs)
    for j in range(n):
        pivot=next(i for i in range(j,n) if aug[i][j])
        aug[j],aug[pivot]=aug[pivot],aug[j]
        val=aug[j][j];aug[j]=[x/val for x in aug[j]]
        for i in range(n):
            if i!=j and aug[i][j]:
                f=aug[i][j];aug[i]=[x-f*y for x,y in zip(aug[i],aug[j])]
    return tuple(row[-1] for row in aug)


@lru_cache(None)
def policy_inverses(theta):
    result=[]
    for policy in itertools.product((0,1),repeat=4):
        mat=[[F(i==j) for j in range(4)] for i in range(4)]
        for i,(a,t) in enumerate(STATES):mat[i][2*t+policy[i]]-=theta
        cols=[rational_solve(mat,[F(i==j) for i in range(4)]) for j in range(4)]
        inverse=tuple(tuple(cols[j][i] for j in range(4)) for i in range(4))
        result.append((policy,inverse))
    return tuple(result)


def exact_projection(p,ell,a0,t0,qs,k,params,theta):
    edge={(a,t,c):min(base.dot(feature(p,ell,a,t,c,s,qs),params) for s in range(k-1))
          for a,t,c in itertools.product((0,1),repeat=3)}
    candidates=[]
    for policy,inverse in policy_inverses(theta):
        costs=[edge[a,t,policy[i]] for i,(a,t) in enumerate(STATES)]
        candidates.append(tuple(base.dot(row,costs) for row in inverse))
    v=tuple(min(c[i] for c in candidates) for i in range(4))
    assert any(c==v for c in candidates)
    for i,(a,t) in enumerate(STATES):
        assert v[i]==min(edge[a,t,c]+theta*v[2*t+c] for c in (0,1))
    return (1-theta)*v[2*a0+t0]


def state_measure(hs,source,member,orb):
    states=defaultdict(F);ct=6 if orb[1] else 30
    for h in hs.values():
        col=h['column'];bits=tuple(map(int,col['actual_bits']));p=sum(bits[:source]);ell=sum(bits[:5])
        for group,count in h['groups'].items():
            if group[:2]!=orb:continue
            for st,mass in h['states'][group].items():
                if mass:
                    qs=base.query_vector(bits,col['hist'],group,st)
                    states[p,ell,st[1-member],st[member],qs]+=F(count,ct)*mass
    return {s:w for s,w in states.items() if w}


def budget(source,K,u):return base.budget(source,K,u)+[F(0)]


def exact_row(cols,hs,source,member,orb,params,theta):
    k=6-source;ct=6 if orb[1] else 30;out=[F(0)]*len(cols);cache={}
    def value(h,g,st):
        bits=tuple(map(int,h['column']['actual_bits']));qs=base.query_vector(bits,h['column']['hist'],g,st)
        key=(sum(bits[:source]),sum(bits[:5]),st[1-member],st[member],qs)
        if key not in cache:cache[key]=exact_projection(*key,k,params,theta)
        return cache[key]
    hi=None
    for j,col in enumerate(cols):
        if col['kind']=='K':out[j]=(k-2)*params[3]+params[4]
        elif col['kind']=='hist':
            hi=j;h=hs[j];bits=tuple(map(int,col['actual_bits']));den=sum(bits)
            out[j]=params[0]*base.share(bits[source],den)+((k-2)*params[1]+params[2])*base.share(bits[5],den)
            out[j]-=sum((F(n,ct)*value(h,g,(0,0)) for g,n in h['groups'].items() if g[:2]==orb),F(0))
        elif col['kind']=='joint-reply':
            f,diag,wi,wj=col['group'];g=(f,diag,tuple(wi),tuple(wj))
            if g[:2]!=orb:continue
            h=hs[hi];out[j]=-F(h['groups'][g],ct)*(value(h,g,tuple(col['state']))-value(h,g,(0,0)))
    return out,len(cache)


def discover_case(cols,hs,K,u,source,member,orb,theta):
    states=state_measure(hs,source,member,orb);keys=list(states);k=6-source;nvar=DIM+4*len(keys)
    rr=[];cc=[];vv=[];rhs=[]
    for q,(p,ell,a0,t0,qs) in enumerate(keys):
        for a,t,c,s in itertools.product((0,1),(0,1),(0,1),range(k-1)):
            r=len(rhs)
            for j,val in enumerate(feature(p,ell,a,t,c,s,qs)):
                if val:rr.append(r);cc.append(j);vv.append(-float(val))
            rr.extend([r,r]);cc.extend([DIM+4*q+2*a+t,DIM+4*q+2*t+c]);vv.extend([1.,-float(theta)])
            rhs.append(0.)
    mat=coo_matrix((vv,(rr,cc)),shape=(len(rhs),nvar)).tocsr()
    obj=list(map(float,budget(source,K,u)))+[0.]*(nvar-DIM)
    for q,key in enumerate(keys):obj[DIM+4*q+2*key[2]+key[3]]=-(1-float(theta))*float(states[key])
    eq=np.zeros((1,nvar));eq[0,:DIM]=1
    bounds=[(0,None)]*DIM+[(None,None)]*(nvar-DIM)
    if k==2:bounds[1]=bounds[3]=(0,0)
    sol=linprog(obj,A_ub=mat,b_ub=rhs,A_eq=eq,b_eq=[1.],bounds=bounds,method='highs')
    result={'source':source+1,'member':member,'previous_member':1-member,'orbit':list(orb),'theta':str(theta),'states':len(states),'success':sol.success}
    if not sol.success:result['message']=sol.message;return result
    params=[F(float(x)).limit_denominator(1000000) if x>1e-10 else F(0) for x in sol.x[:DIM]]
    params=[x/sum(params,F(0)) for x in params]
    value=base.dot(params,budget(source,K,u))-sum((mass*exact_projection(*st,k,params,theta) for st,mass in states.items()),F(0))
    result.update(float_objective=float(sol.fun),exact_slack=str(value),exact_slack_float=float(value),parameters={n:str(x) for n,x in zip(NAMES,params) if x})
    if value<0:
        row,nstates=exact_row(cols,hs,source,member,orb,params,theta)
        assert sum((v*F(col['weight']) for v,col in zip(row,cols)),F(0))==value
        result['full_column_count']=len(row);result['full_projected_states']=nstates
        result['row_nonzero']=[[i,str(v)] for i,v in enumerate(row) if v]
        result['row_sha256']=hashlib.sha256(json.dumps(list(map(str,row)),separators=(',',':')).encode()).hexdigest()
    return result


def main():
    ap=argparse.ArgumentParser();ap.add_argument('input');ap.add_argument('output')
    ap.add_argument('--thetas',default='0,1/2,3/4,9/10');ap.add_argument('--sources',default='5')
    args=ap.parse_args();data,cols,hs,K,u=base.read_input(args.input);results=[]
    for source in [int(x)-1 for x in args.sources.split(',')]:
        for member,orb,theta in itertools.product((0,1),base.ORBS,map(F,args.thetas.split(','))):
            r=discover_case(cols,hs,K,u,source,member,orb,theta);results.append(r)
            if F(r.get('exact_slack','0'))<0:print('CUT',source+1,member,orb,str(theta),r['exact_slack_float'],flush=True)
        print('SOURCE',source+1,'complete',flush=True)
    negatives=[r for r in results if F(r.get('exact_slack','0'))<0]
    report={'scope':'four-state previous-theme same-source discounted orbit; fixed true source and exact joint initial R/Z; necessary point not SPE',
            'input':args.input,'input_sha256':hashlib.sha256(Path(args.input).read_bytes()).hexdigest(),'input_W':data['W'],
            'columns':len(cols),'K':str(K),'actual_u':list(map(str,u)),'parameter_names':NAMES,
            'cases':len(results),'negative_cases':len(negatives),'results':results}
    Path(args.output).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'cases':len(results),'negative_cases':len(negatives),'minimum_exact_slack':str(min(F(x.get('exact_slack','0')) for x in results))}),flush=True)


if __name__=='__main__':main()
