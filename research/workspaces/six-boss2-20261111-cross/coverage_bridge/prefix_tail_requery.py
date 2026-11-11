#!/usr/bin/env python3
"""Independent prefix weights + independently priced same-source tail closure.

Prefix: shared 34 + two PAIR branches, ending at V.
Tail: two-state terminal-requery closure, initially forced V.
All prefix source weights plus tail source weight total one; u6/K also add.
The tail's 17 static queries retain their original identities across both parts.
"""
from __future__ import annotations

import argparse,hashlib,itertools,json
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

import macro_pair_requery as prefix
import joint_discounted_requery as tail
from discounted_requery import closed_values,dot

DA,DB=prefix.DIM,tail.DIM
DIM=DA+DB


def tail_values(p,ell,qs,k,weights,delta):
    edge={(t,c):min(dot(tail.feature(p,ell,t,c,s,qs),weights) for s in range(k-1))
          for t,c in itertools.product((0,1),repeat=2)}
    psi=closed_values(edge,delta);v=tuple(x/(1-delta) for x in psi)
    for t in (0,1):assert v[t]==min(edge[t,c]+delta*v[c] for c in (0,1))
    return psi


def combined_value(p,ell,t0,qs,k,alpha,beta,delta,components=False):
    psi=tail_values(p,ell,qs,k,beta,delta);compressed=prefix.compressed_weights(alpha,qs)
    terms=[];before=[]
    for b,c,j,v in itertools.product((0,1),repeat=4):
        for s,ss in itertools.product(range(k-2),repeat=2):
            raw=prefix.raw_pair(p,ell,t0,b,c,j,v,s,ss,k)
            e=sum((dot(x,y) for x,y in zip(raw,compressed)),F(0))
            before.append(e);terms.append(e+psi[v])
    joint=min(terms)
    if components:return joint,min(before),min(psi)
    return joint


def budget_vector(source,K,u):
    k=6-source
    return [a*u[source]+b*u[5]+c*K for a,b,c in prefix.budget_vectors(k)]+tail.budget(source,K,u)


def combined_budgets(k,alpha,beta):
    bb=prefix.budget_vectors(k)
    ar,au,ak=(sum((w*b[j] for w,b in zip(alpha,bb)),F(0)) for j in range(3))
    return ar+beta[0],au+(k-2)*beta[1]+beta[2],ak+(k-2)*beta[3]+beta[4]


def exact_row(cols,hs,source,member,orb,alpha,beta,delta):
    k=6-source;ct=6 if orb[1] else 30;rb,ub,kb=combined_budgets(k,alpha,beta);assert rb==1
    out=[F(0)]*len(cols);cache={};hi=None
    def value(h,g,st):
        bits=tuple(map(int,h['column']['actual_bits']));qs=tail.query_vector(bits,h['column']['hist'],g,st)
        key=(sum(bits[:source]),sum(bits[:5]),st[member],qs)
        if key not in cache:cache[key]=combined_value(*key,k,alpha,beta,delta)
        return cache[key]
    for j,col in enumerate(cols):
        if col['kind']=='K':out[j]=kb
        elif col['kind']=='hist':
            hi=j;h=hs[j];bits=tuple(map(int,col['actual_bits']));den=sum(bits)
            out[j]=rb*tail.share(bits[source],den)+ub*tail.share(bits[5],den)
            out[j]-=sum((F(n,ct)*value(h,g,(0,0)) for g,n in h['groups'].items() if g[:2]==orb),F(0))
        elif col['kind']=='joint-reply':
            f,diag,wi,wj=col['group'];g=f,diag,tuple(wi),tuple(wj)
            if g[:2]!=orb:continue
            h=hs[hi];out[j]=-F(h['groups'][g],ct)*(value(h,g,tuple(col['state']))-value(h,g,(0,0)))
    return out,len(cache)


def discover_case(cols,hs,K,u,source,member,orb,delta,box):
    k=6-source;states=tail.state_measure(hs,source,member,orb);keys=list(states);nvar=DIM+3*len(keys)
    rr=[];cc=[];vv=[];rhs=[]
    def put(r,j,x):
        if x:rr.append(r);cc.append(j);vv.append(float(x))
    for ix,(p,ell,t0,qs) in enumerate(keys):
        # Tail subsolution, valid for every legal input theme at the same source.
        for t,c,s in itertools.product((0,1),(0,1),range(k-1)):
            r=len(rhs)
            for j,val in enumerate(tail.feature(p,ell,t,c,s,qs)):put(r,DA+j,-val)
            put(r,DIM+3*ix+t,1);put(r,DIM+3*ix+c,-delta);rhs.append(0.)
        # Initial genuine macro branches share their output v with the tail value.
        for b,c,j,v in itertools.product((0,1),repeat=4):
            for s,ss in itertools.product(range(k-2),repeat=2):
                r=len(rhs);fs=prefix.float_features(prefix.raw_pair(p,ell,t0,b,c,j,v,s,ss,k),qs)
                for column,val in enumerate(fs):put(r,column,-val)
                put(r,DIM+3*ix+2,1);put(r,DIM+3*ix+v,-(1-delta));rhs.append(0.)
    mat=coo_matrix((vv,(rr,cc)),shape=(len(rhs),nvar)).tocsr()
    obj=list(map(float,budget_vector(source,K,u)))+[0.]*(nvar-DIM)
    for ix,key in enumerate(keys):obj[DIM+3*ix+2]=-float(states[key])
    eq=np.zeros((1,nvar));eq[0,prefix.NAMES.index('sourceT')]=eq[0,prefix.NAMES.index('sourceC')]=eq[0,DA]=1
    bounds=[(0,box)]*DIM+[(None,None)]*(nvar-DIM)
    for j in (prefix.NAMES.index('sourceT'),prefix.NAMES.index('sourceC'),DA):bounds[j]=(0,1)
    if k==3:
        for name in ('price:s','price:ss','cap:s','cap:ss'):bounds[prefix.NAMES.index(name)]=(0,0)
    sol=linprog(obj,A_ub=mat,b_ub=rhs,A_eq=eq,b_eq=[1.],bounds=bounds,method='highs')
    record={'source':source+1,'k':k,'member':member,'orbit':list(orb),'delta':str(delta),'states':len(states),'success':sol.success}
    if not sol.success:record['message']=sol.message;return record
    weights=[F(float(x)).limit_denominator(1000000) if x>1e-10 else F(0) for x in sol.x[:DIM]]
    src=weights[prefix.NAMES.index('sourceT')]+weights[prefix.NAMES.index('sourceC')]+weights[DA];assert src>0
    weights=[x/src for x in weights];alpha,beta=weights[:DA],weights[DA:]
    rb,ub,kb=combined_budgets(k,alpha,beta);assert rb==1
    sums=[F(0),F(0),F(0)]
    for st,mass in states.items():
        parts=combined_value(*st,k,alpha,beta,delta,components=True)
        for j,x in enumerate(parts):sums[j]+=mass*x
    value=rb*u[source]+ub*u[5]+kb*K-sums[0]
    separated=rb*u[source]+ub*u[5]+kb*K-sums[1]-sums[2]
    record.update(float_objective=float(sol.fun),exact_slack=str(value),exact_slack_float=float(value),
                  alpha={n:str(w) for n,w in zip(prefix.NAMES,alpha) if w},
                  beta={n:str(w) for n,w in zip(tail.NAMES,beta) if w},
                  budget=list(map(str,(rb,ub,kb))),separate_projection_slack=str(separated),
                  joint_projection_gain=str(sums[0]-sums[1]-sums[2]))
    if value<0:
        row,nstates=exact_row(cols,hs,source,member,orb,alpha,beta,delta)
        assert sum((v*F(c['weight']) for v,c in zip(row,cols)),F(0))==value
        record['full_column_count']=len(cols);record['full_projected_states']=nstates
        record['row_nonzero']=[[i,str(v)] for i,v in enumerate(row) if v]
        record['row_sha256']=hashlib.sha256(json.dumps(list(map(str,row)),separators=(',',':')).encode()).hexdigest()
    return record


def main():
    ap=argparse.ArgumentParser();ap.add_argument('input');ap.add_argument('output')
    ap.add_argument('--sources',default='4');ap.add_argument('--deltas',default='0,1/2,3/4');ap.add_argument('--box',type=int,default=1000)
    args=ap.parse_args();data,cols,hs,K,u=tail.read_input(args.input);results=[]
    for source in [int(x)-1 for x in args.sources.split(',')]:
        for member,orb,delta in itertools.product((0,1),tail.ORBS,map(F,args.deltas.split(','))):
            r=discover_case(cols,hs,K,u,source,member,orb,delta,args.box);results.append(r)
            print('CASE',source+1,member,orb,str(delta),r.get('exact_slack_float',r.get('message')),flush=True)
    neg=[r for r in results if F(r.get('exact_slack','0'))<0]
    report={'scope':'independently weighted joint-prefix plus terminal-requery closure at shared endpoint; necessary local cuts only',
            'input':args.input,'input_sha256':hashlib.sha256(Path(args.input).read_bytes()).hexdigest(),'input_W':data['W'],
            'source_normalization':'alpha[sourceT]+alpha[sourceC]+beta[source]=1','other_weight_discovery_box':[0,args.box],
            'alpha_names':prefix.NAMES,'beta_names':tail.NAMES,'columns':len(cols),'cases':len(results),'negative_cases':len(neg),'results':results}
    Path(args.output).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'cases':len(results),'negative_cases':len(neg)}),flush=True)


if __name__=='__main__':main()
