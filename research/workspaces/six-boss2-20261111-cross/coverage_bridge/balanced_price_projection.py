#!/usr/bin/env python3
"""Independently optimized positive catalog prices from actual source five.

Each real hidden B,C,J,V (and each middle theme) receives its own balanced
k=2 terminal-closure price.  All static queries are fixed before pricing F.
The source-five costs add, and never merge into the earlier source wallet.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

import macro_pair_requery as prefix
import joint_discounted_requery as data_api
from discounted_requery import dot

LABELS=('b','c','j','v','s','ss')
PRICE_NAMES=['alpha_last','beta_last']+['mu_'+n for n in prefix.QUERY_NAMES]+['mu_self']
DP=len(PRICE_NAMES)
DA=prefix.DIM
NAMES=prefix.NAMES+[f'price_{label}:{name}' for label in LABELS for name in PRICE_NAMES]
DIM=len(NAMES)
assert DP==20 and DIM==452


def price_features(qs,theta):
    """Linear coefficients of A, A+kappa, and w=Psi1-Psi0."""
    actual=tuple(map(int,qs[:6]));p=sum(actual[:4]);ell=sum(actual[:5])
    D=(p+1)*(p+2)
    g=[F(0),F(0)]+[(F(p+2)-q)/D for q in qs]+[F(2*p+3,D)]
    A=[F(0),F(0)]+[q/(p+1) for q in qs]+[F(0)]
    second=[F(1,ell+1),F(1)]+[a+theta*d-F(1,p+1) for a,d in zip(A[2:],g[2:])]
    w=[(1-theta)*x for x in g]
    assert all(x>=0 for x in w)
    return tuple(A),tuple(second),tuple(w)


def price_values(qs,theta,prices):
    aa,bb,ww=price_features(qs,theta)
    vals=[]
    for beta in prices:
        s=min(dot(aa,beta),dot(bb,beta));w=dot(ww,beta)
        assert w>=0
        vals.append((s,w))
    return vals


def budgets(k,alpha,prices):
    old=prefix.budget_vectors(k)
    sr,u6,K=(sum((a*b[j] for a,b in zip(alpha,old)),F(0)) for j in range(3))
    u5=F(0)
    for mult,beta in zip((1,1,1,1,k-3,k-3),prices):
        u5+=mult*sum(beta[2:],F(0));u6+=mult*beta[0];K+=mult*beta[1]
    return sr,u5,u6,K


def projection(p,ell,t0,qs,k,theta,alpha,prices,components=False):
    pv=price_values(qs,theta,prices);cw=prefix.compressed_weights(alpha,qs)
    multi=(1,1,1,1,k-3,k-3)
    constant=sum((m*s for m,(s,w) in zip(multi,pv)),F(0))
    joint=[];old=[]
    for b,c,j,v in itertools.product((0,1),repeat=4):
        for s,ss in itertools.product(range(k-2),repeat=2):
            raw=prefix.raw_pair(p,ell,t0,b,c,j,v,s,ss,k)
            e=sum((dot(x,y) for x,y in zip(raw,cw)),F(0))
            add=sum((count*w for count,(base,w) in zip((b,c,j,v,s,ss),pv)),constant)
            old.append(e);joint.append(e+add)
    if components:return min(joint),min(old),constant
    return min(joint)


def exact_row(cols,hs,source,member,orb,theta,alpha,prices):
    k=6-source;ct=6 if orb[1] else 30;sr,u5,u6,K=budgets(k,alpha,prices);assert sr==1
    row=[F(0)]*len(cols);cache={};hi=None
    def value(h,g,st):
        actual=tuple(map(int,h['column']['actual_bits']))
        qs=data_api.query_vector(actual,h['column']['hist'],g,st)
        key=sum(actual[:source]),sum(actual[:5]),st[member],qs
        if key not in cache:cache[key]=projection(*key,k,theta,alpha,prices)
        return cache[key]
    for index,col in enumerate(cols):
        if col['kind']=='K':row[index]=K
        elif col['kind']=='hist':
            hi=index;h=hs[index];a=tuple(map(int,col['actual_bits']));den=sum(a)
            row[index]=data_api.share(a[source],den)+u5*data_api.share(a[4],den)+u6*data_api.share(a[5],den)
            row[index]-=sum((F(n,ct)*value(h,g,(0,0)) for g,n in h['groups'].items() if g[:2]==orb),F(0))
        elif col['kind']=='joint-reply':
            f,diag,wi,wj=col['group'];g=f,diag,tuple(wi),tuple(wj)
            if g[:2]!=orb:continue
            h=hs[hi]
            row[index]=-F(h['groups'][g],ct)*(value(h,g,tuple(col['state']))-value(h,g,(0,0)))
    return row,len(cache)


def discover_case(cols,hs,K,u,source,member,orb,theta,box):
    k=6-source;multi=(1,1,1,1,k-3,k-3)
    states=data_api.state_measure(hs,source,member,orb);keys=list(states)
    nvar=DIM+7*len(keys);rr=[];cc=[];vv=[];rhs=[]
    def put(r,j,x):
        if x:rr.append(r);cc.append(j);vv.append(float(x))
    for ix,(p,ell,t0,qs) in enumerate(keys):
        aa,bb,ww=price_features(qs,theta)
        for price_index in range(6):
            for bound in (aa,bb):
                r=len(rhs)
                for j,x in enumerate(bound):put(r,DA+price_index*DP+j,-x)
                put(r,DIM+7*ix+price_index,1);rhs.append(0.)
        for b,c,j,v in itertools.product((0,1),repeat=4):
            for s,ss in itertools.product(range(k-2),repeat=2):
                r=len(rhs)
                fs=prefix.float_features(prefix.raw_pair(p,ell,t0,b,c,j,v,s,ss,k),qs)
                for column,x in enumerate(fs):put(r,column,-x)
                for price_index,(count,mult) in enumerate(zip((b,c,j,v,s,ss),multi)):
                    for column,x in enumerate(ww):put(r,DA+price_index*DP+column,-count*x)
                    put(r,DIM+7*ix+price_index,-mult)
                put(r,DIM+7*ix+6,1);rhs.append(0.)
    mat=coo_matrix((vv,(rr,cc)),shape=(len(rhs),nvar)).tocsr()
    obj=[float(a*u[source]+b*u[5]+c*K) for a,b,c in prefix.budget_vectors(k)]
    for mult in multi:obj += [float(mult*u[5]),float(mult*K)]+[float(mult*u[4])]*18
    obj += [0.]*(nvar-DIM)
    for ix,key in enumerate(keys):obj[DIM+7*ix+6]=-float(states[key])
    eq=np.zeros((1,nvar));eq[0,prefix.NAMES.index('sourceT')]=eq[0,prefix.NAMES.index('sourceC')]=1
    bounds=[(0,box)]*DIM+[(None,None)]*(nvar-DIM)
    for name in ('sourceT','sourceC'):bounds[prefix.NAMES.index(name)]=(0,1)
    if k==3:
        for name in ('price:s','price:ss','cap:s','cap:ss'):bounds[prefix.NAMES.index(name)]=(0,0)
        for j in range(DA+4*DP,DIM):bounds[j]=(0,0)
    sol=linprog(obj,A_ub=mat,b_ub=rhs,A_eq=eq,b_eq=[1.],bounds=bounds,method='highs')
    rec={'source':source+1,'k':k,'member':member,'orbit':list(orb),'theta':str(theta),
         'states':len(states),'success':sol.success}
    if not sol.success:rec['message']=sol.message;return rec
    for grid in (1000,10000,100000,1000000,10000000):
        ints=[max(0,round(float(x)*grid)) for x in sol.x[:DIM]]
        denom=ints[prefix.NAMES.index('sourceT')]+ints[prefix.NAMES.index('sourceC')];assert denom>0
        params=[F(x,denom) for x in ints];alpha=params[:DA]
        prices=[params[DA+j*DP:DA+(j+1)*DP] for j in range(6)]
        bgt=budgets(k,alpha,prices);sums=[F(0)]*3
        for st,mass in states.items():
            parts=projection(*st,k,theta,alpha,prices,components=True)
            for j,x in enumerate(parts):sums[j]+=mass*x
        value=bgt[0]*u[source]+bgt[1]*u[4]+bgt[2]*u[5]+bgt[3]*K-sums[0]
        if sol.fun>=-1e-9 or value<0:break
    active={label:{name:str(x) for name,x in zip(PRICE_NAMES,beta) if x}
            for label,beta in zip(LABELS,prices) if any(beta)}
    rec.update(float_objective=float(sol.fun),grid=grid,common_source_denominator=denom,
               alpha={n:str(x) for n,x in zip(prefix.NAMES,alpha) if x},prices=active,
               budget=list(map(str,bgt)),exact_slack=str(value),exact_slack_float=float(value))
    if value<0:
        row,count=exact_row(cols,hs,source,member,orb,theta,alpha,prices)
        assert sum((a*F(c['weight']) for a,c in zip(row,cols)),F(0))==value
        _,old_u6,old_K=(sum((a*b[j] for a,b in zip(alpha,prefix.budget_vectors(k))),F(0)) for j in range(3))
        before=u[source]+old_u6*u[5]+old_K*K-sums[1]
        rec.update(prefix_only_slack=str(before),
                   separate_projection_slack=str(bgt[0]*u[source]+bgt[1]*u[4]+bgt[2]*u[5]+bgt[3]*K-sums[1]-sums[2]),
                   joint_projection_gain=str(sums[0]-sums[1]-sums[2]),
                   full_column_count=len(cols),full_projected_states=count,
                   row_nonzero=[[j,str(x)] for j,x in enumerate(row) if x],
                   row_sha256=hashlib.sha256(json.dumps(list(map(str,row)),separators=(',',':')).encode()).hexdigest())
    return rec


def main():
    ap=argparse.ArgumentParser();ap.add_argument('input');ap.add_argument('output')
    ap.add_argument('--sources',default='4');ap.add_argument('--thetas',default='3/4');ap.add_argument('--box',type=int,default=1000)
    args=ap.parse_args();data,cols,hs,K,u=data_api.read_input(args.input);results=[]
    for source in [int(x)-1 for x in args.sources.split(',')]:
        for member,orb,theta in itertools.product((0,1),data_api.ORBS,map(F,args.thetas.split(','))):
            r=discover_case(cols,hs,K,u,source,member,orb,theta,args.box);results.append(r)
            print('CASE',source+1,member,orb,str(theta),r.get('exact_slack_float',r.get('message')),
                  'prices',list(r.get('prices',{})),flush=True)
    neg=[r for r in results if F(r.get('exact_slack','0'))<0]
    report={'scope':'independently optimized balanced actual-source-five uniform positive catalog prices inside earlier 34+PAIR',
            'input':args.input,'input_sha256':hashlib.sha256(Path(args.input).read_bytes()).hexdigest(),'input_W':data['W'],
            'source_normalization':'alpha[sourceT]+alpha[sourceC]=1; each price a0=sum(static mu)+mu_self, paid in separate u5 wallet',
            'other_weight_discovery_box':[0,args.box],'alpha_names':prefix.NAMES,'price_names':PRICE_NAMES,
            'budget_order':['actual_source','u5','u6','K'],'columns':len(cols),'cases':len(results),
            'negative_cases':len(neg),'results':results}
    Path(args.output).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print({'cases':len(results),'negative_cases':len(neg)},flush=True)


if __name__=='__main__':main()
