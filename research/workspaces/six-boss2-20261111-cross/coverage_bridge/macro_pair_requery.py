#!/usr/bin/env python3
"""Discounted closure of the joint 34 + two-PAIR cone under T -> C(C(T)).

All 17 fixed query slots share both real branches before projection.  Query
diagonal PAIR means the average of identical pure-query pairs, hence q^2=q.
SourceT + sourceC = 1.  A finite search box on other weights is discovery only.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

import joint_discounted_requery as data_api
from discounted_requery import closed_values,dot

FEATURE_PATH=Path(__file__).resolve().parent.parent/'joint_requery'/'explore_projection.py'
sys.path.insert(0,str(FEATURE_PATH.parent))
from explore_projection import features,ALL_NAMES,hidden_configs

FIXED_NAMES=[n for n in ALL_NAMES if 'q' not in n]
QUERY_FEATURES=[n for n in ALL_NAMES if 'q' in n]
QUERY_NAMES=data_api.QUERY_NAMES[:-1]
NAMES=FIXED_NAMES+[n+'@'+q for n in QUERY_FEATURES for q in QUERY_NAMES]
DIM=len(NAMES)
assert len(FIXED_NAMES)==60 and len(QUERY_FEATURES)==16 and len(QUERY_NAMES)==17


@lru_cache(None)
def raw_pair(p,ell,t,b,c,j,v,s,ss,k):
    f0,bud=features(p,ell,t,F(0),b,c,j,v,s,ss,k)
    f1,_=features(p,ell,t,F(1),b,c,j,v,s,ss,k)
    return (tuple(f0[n] for n in FIXED_NAMES),
            tuple(f0[n] for n in QUERY_FEATURES),
            tuple(f1[n]-f0[n] for n in QUERY_FEATURES))


def float_features(raw,qs):
    fixed,zero,delta=raw
    return [float(v) for v in fixed]+[float(z)+float(q)*float(d) for z,d in zip(zero,delta) for q in qs]


def compressed_weights(params,qs):
    fixed=params[:len(FIXED_NAMES)];zero=[];qsum=[]
    for i in range(len(QUERY_FEATURES)):
        group=params[len(FIXED_NAMES)+i*len(QUERY_NAMES):len(FIXED_NAMES)+(i+1)*len(QUERY_NAMES)]
        zero.append(sum(group,F(0)));qsum.append(dot(group,qs))
    return tuple(fixed),tuple(zero),tuple(qsum)


def exact_projection(p,ell,t0,qs,k,params,theta):
    weights=compressed_weights(params,qs);edge={}
    for t,v in itertools.product((0,1),repeat=2):
        vals=[]
        for b,c,j in itertools.product((0,1),repeat=3):
            for s,ss in itertools.product(range(k-2),repeat=2):
                raw=raw_pair(p,ell,t,b,c,j,v,s,ss,k)
                vals.append(sum((dot(a,b) for a,b in zip(raw,weights)),F(0)))
        edge[t,v]=min(vals)
    psi=closed_values(edge,theta);V=tuple(v/(1-theta) for v in psi)
    for t in (0,1):assert V[t]==min(edge[t,v]+theta*V[v] for v in (0,1))
    return psi[t0]


def budget_vectors(k):
    _,bud=features(0,0,0,F(0),0,0,0,0,0,0,k)
    out=[tuple(map(F,bud[n])) for n in FIXED_NAMES]+[(F(0),F(0),F(0))]*(DIM-len(FIXED_NAMES))
    return out


def exact_row(cols,hs,source,member,orb,params,theta):
    k=6-source;ct=6 if orb[1] else 30;bud=budget_vectors(k)
    rb,ub,kb=(sum((w*b[j] for w,b in zip(params,bud)),F(0)) for j in range(3))
    assert rb==1
    out=[F(0)]*len(cols);cache={}
    def value(h,g,st):
        bits=tuple(map(int,h['column']['actual_bits']));qs=data_api.query_vector(bits,h['column']['hist'],g,st)
        key=(sum(bits[:source]),sum(bits[:5]),st[member],qs)
        if key not in cache:cache[key]=exact_projection(*key,k,params,theta)
        return cache[key]
    hi=None
    for j,col in enumerate(cols):
        if col['kind']=='K':out[j]=kb
        elif col['kind']=='hist':
            hi=j;h=hs[j];bits=tuple(map(int,col['actual_bits']));den=sum(bits)
            out[j]=rb*data_api.share(bits[source],den)+ub*data_api.share(bits[5],den)
            out[j]-=sum((F(n,ct)*value(h,g,(0,0)) for g,n in h['groups'].items() if g[:2]==orb),F(0))
        elif col['kind']=='joint-reply':
            f,diag,wi,wj=col['group'];g=(f,diag,tuple(wi),tuple(wj))
            if g[:2]!=orb:continue
            h=hs[hi];out[j]=-F(h['groups'][g],ct)*(value(h,g,tuple(col['state']))-value(h,g,(0,0)))
    return out,len(cache),(rb,ub,kb)


def discover_case(cols,hs,K,u,source,member,orb,theta,box=1000):
    k=6-source;states=data_api.state_measure(hs,source,member,orb);keys=list(states);nvar=DIM+2*len(keys)
    rr=[];cc=[];vv=[];rhs=[]
    for ix,(p,ell,t0,qs) in enumerate(keys):
        for t,v,b,c,j in itertools.product((0,1),repeat=5):
            for s,ss in itertools.product(range(k-2),repeat=2):
                row=len(rhs);fs=float_features(raw_pair(p,ell,t,b,c,j,v,s,ss,k),qs)
                for col,val in enumerate(fs):
                    if val:rr.append(row);cc.append(col);vv.append(-val)
                rr.extend([row,row]);cc.extend([DIM+2*ix+t,DIM+2*ix+v]);vv.extend([1.,-float(theta)])
                rhs.append(0.)
    mat=coo_matrix((vv,(rr,cc)),shape=(len(rhs),nvar)).tocsr();bud=budget_vectors(k)
    obj=[float(a*u[source]+b*u[5]+c*K) for a,b,c in bud]+[0.]*(nvar-DIM)
    for ix,key in enumerate(keys):obj[DIM+2*ix+key[2]]=-(1-float(theta))*float(states[key])
    eq=np.zeros((1,nvar));eq[0,NAMES.index('sourceT')]=eq[0,NAMES.index('sourceC')]=1
    bounds=[(0,box)]*DIM+[(None,None)]*(nvar-DIM)
    for n in ('sourceT','sourceC'):bounds[NAMES.index(n)]=(0,1)
    if k==3:
        for n in ('price:s','price:ss','cap:s','cap:ss'):bounds[NAMES.index(n)]=(0,0)
    sol=linprog(obj,A_ub=mat,b_ub=rhs,A_eq=eq,b_eq=[1.],bounds=bounds,method='highs')
    result={'source':source+1,'k':k,'member':member,'orbit':list(orb),'theta':str(theta),'states':len(states),'success':sol.success}
    if not sol.success:result['message']=sol.message;return result
    params=[F(float(x)).limit_denominator(1000000) if x>1e-10 else F(0) for x in sol.x[:DIM]]
    src=params[NAMES.index('sourceT')]+params[NAMES.index('sourceC')];assert src>0
    params=[v/src for v in params]
    rb,ub,kb=(sum((w*b[j] for w,b in zip(params,bud)),F(0)) for j in range(3))
    value=rb*u[source]+ub*u[5]+kb*K-sum((mass*exact_projection(*st,k,params,theta) for st,mass in states.items()),F(0))
    result.update(float_objective=float(sol.fun),exact_slack=str(value),exact_slack_float=float(value),
                  parameters={n:str(w) for n,w in zip(NAMES,params) if w},budget=[str(rb),str(ub),str(kb)])
    if value<0:
        row,nstates,check_budget=exact_row(cols,hs,source,member,orb,params,theta)
        assert (rb,ub,kb)==check_budget
        assert sum((v*F(col['weight']) for v,col in zip(row,cols)),F(0))==value
        result['full_column_count']=len(row);result['full_projected_states']=nstates
        result['row_nonzero']=[[i,str(v)] for i,v in enumerate(row) if v]
        result['row_sha256']=hashlib.sha256(json.dumps(list(map(str,row)),separators=(',',':')).encode()).hexdigest()
    return result


def main():
    ap=argparse.ArgumentParser();ap.add_argument('input');ap.add_argument('output')
    ap.add_argument('--sources',default='4');ap.add_argument('--thetas',default='1/2,3/4,9/10');ap.add_argument('--box',type=int,default=1000)
    args=ap.parse_args();data,cols,hs,K,u=data_api.read_input(args.input);results=[]
    for source in [int(x)-1 for x in args.sources.split(',')]:
        for member,orb,theta in itertools.product((0,1),data_api.ORBS,map(F,args.thetas.split(','))):
            r=discover_case(cols,hs,K,u,source,member,orb,theta,args.box);results.append(r)
            print('CASE',source+1,member,orb,str(theta),r.get('exact_slack_float',r.get('message')),flush=True)
    negatives=[r for r in results if F(r.get('exact_slack','0'))<0]
    report={'scope':'two-branch 34+PAIR common fixed-query portfolio, endpoint v reclosed by same-source C^2 map; necessary local cuts only',
            'input':args.input,'input_sha256':hashlib.sha256(Path(args.input).read_bytes()).hexdigest(),'input_W':data['W'],
            'feature_dependency':str(FEATURE_PATH),'feature_dependency_sha256':hashlib.sha256(FEATURE_PATH.read_bytes()).hexdigest(),
            'source_normalization':'sourceT+sourceC=1','other_weight_discovery_box':[0,args.box],
            'parameter_names':NAMES,'columns':len(cols),'cases':len(results),'negative_cases':len(negatives),'results':results}
    Path(args.output).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'cases':len(results),'negative_cases':len(negatives)}),flush=True)


if __name__=='__main__':main()
