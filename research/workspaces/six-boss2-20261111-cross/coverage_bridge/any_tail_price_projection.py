#!/usr/bin/env python3
"""General balanced real-source catalog prices inside a different real source.

Discovery uses the full Bellman inequalities. Exact reconstruction minimizes
over middle counts, then four deterministic two-state policies. It never
assumes k>2 retains the balanced four-edge identity of k=2.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

import macro_pair_requery as prefix
import joint_discounted_requery as data_api
from discounted_requery import closed_values,dot

LABELS=('b','c','j','v','s','ss')
PRICE_NAMES=['alpha_mid','alpha_last','beta_mid','beta_last']+['mu_'+n for n in prefix.QUERY_NAMES]+['mu_self']
DP=len(PRICE_NAMES);DA=prefix.DIM;DIM=DA+6*DP
assert DP==22 and DIM==464


@lru_cache(None)
def price_features(p,ell,t,c,s,qs):
    den=p+t+s+c
    shared=F(t-c,den) if t!=c else F(0)
    qden=p+t+s+1
    return (F(s,ell+1),F(c,ell+1),F(s),F(c),
            *(shared+q/qden for q in qs),shared+F(t,qden))


def price_values(qs,price_source,theta,prices):
    p=sum(map(int,qs[:price_source]));ell=sum(map(int,qs[:5]));k=6-price_source
    output=[]
    for beta in prices:
        edges={(t,c):min(dot(price_features(p,ell,t,c,s,qs),beta) for s in range(k-1))
               for t,c in itertools.product((0,1),repeat=2)}
        psi=closed_values(edges,theta);V=tuple(x/(1-theta) for x in psi)
        assert all(V[t]==min(edges[t,c]+theta*V[c] for c in (0,1)) for t in (0,1))
        a=sum(beta[4:],F(0));mu=beta[-1];q=dot(beta[4:-1],qs);w=psi[1]-psi[0]
        low=(1-theta)*((a-q)/(p+k-1)+(mu+q)/(p+k))
        high=(1-theta)*((a-q)/(p+1)+(mu+q)/(p+2))
        assert 0<=q<=a-mu and 0<=low<=w<=high
        if a:assert w>0
        output.append(psi)
    return output


def budgets(k,price_k,alpha,prices):
    bs=prefix.budget_vectors(k)
    sr,u6,K=(sum((a*b[j] for a,b in zip(alpha,bs)),F(0)) for j in range(3))
    pr=F(0)
    for mult,beta in zip((1,1,1,1,k-3,k-3),prices):
        pr+=mult*sum(beta[4:],F(0))
        u6+=mult*((price_k-2)*beta[0]+beta[1])
        K+=mult*((price_k-2)*beta[2]+beta[3])
    return sr,pr,u6,K


def projection(p,ell,t0,qs,k,price_source,theta,alpha,prices,components=False):
    values=price_values(qs,price_source,theta,prices)
    cw=prefix.compressed_weights(alpha,qs);multi=(1,1,1,1,k-3,k-3)
    baseline=sum((m*psi[0] for m,psi in zip(multi,values)),F(0))
    slopes=[psi[1]-psi[0] for psi in values]
    old=[];joint=[]
    for b,c,j,v in itertools.product((0,1),repeat=4):
        for s,ss in itertools.product(range(k-2),repeat=2):
            raw=prefix.raw_pair(p,ell,t0,b,c,j,v,s,ss,k)
            e=sum((dot(a,b) for a,b in zip(raw,cw)),F(0))
            old.append(e);joint.append(e+baseline+dot(slopes,(b,c,j,v,s,ss)))
    if components:return min(joint),min(old),baseline
    return min(joint)


def exact_row(cols,hs,source,price_source,member,orb,theta,alpha,prices):
    k=6-source;pk=6-price_source;ct=6 if orb[1] else 30
    sr,pr,u6,K=budgets(k,pk,alpha,prices);assert sr==1
    row=[F(0)]*len(cols);cache={};hi=None
    def value(h,g,st):
        actual=tuple(map(int,h['column']['actual_bits']))
        qs=data_api.query_vector(actual,h['column']['hist'],g,st)
        key=sum(actual[:source]),sum(actual[:5]),st[member],qs
        if key not in cache:cache[key]=projection(*key,k,price_source,theta,alpha,prices)
        return cache[key]
    for index,col in enumerate(cols):
        if col['kind']=='K':row[index]=K
        elif col['kind']=='hist':
            hi=index;h=hs[index];a=tuple(map(int,col['actual_bits']));den=sum(a)
            row[index]=data_api.share(a[source],den)+pr*data_api.share(a[price_source],den)+u6*data_api.share(a[5],den)
            row[index]-=sum((F(n,ct)*value(h,g,(0,0)) for g,n in h['groups'].items() if g[:2]==orb),F(0))
        elif col['kind']=='joint-reply':
            f,diag,wi,wj=col['group'];g=f,diag,tuple(wi),tuple(wj)
            if g[:2]!=orb:continue
            h=hs[hi]
            row[index]=-F(h['groups'][g],ct)*(value(h,g,tuple(col['state']))-value(h,g,(0,0)))
    return row,len(cache)


def discover_case(cols,hs,K,u,source,price_source,member,orb,theta,box):
    k=6-source;pk=6-price_source;multi=(1,1,1,1,k-3,k-3)
    states=data_api.state_measure(hs,source,member,orb);keys=list(states)
    nvar=DIM+13*len(keys);rr=[];cc=[];vv=[];rhs=[]
    def put(r,j,x):
        if x:rr.append(r);cc.append(j);vv.append(float(x))
    for ix,(p,ell,t0,qs) in enumerate(keys):
        pp=sum(map(int,qs[:price_source]))
        for price_index in range(6):
            for t,c,s in itertools.product((0,1),(0,1),range(pk-1)):
                r=len(rhs)
                for j,x in enumerate(price_features(pp,ell,t,c,s,qs)):put(r,DA+price_index*DP+j,-x)
                put(r,DIM+13*ix+2*price_index+t,1)
                put(r,DIM+13*ix+2*price_index+c,-theta);rhs.append(0.)
        for b,c,j,v in itertools.product((0,1),repeat=4):
            for s,ss in itertools.product(range(k-2),repeat=2):
                r=len(rhs)
                fs=prefix.float_features(prefix.raw_pair(p,ell,t0,b,c,j,v,s,ss,k),qs)
                for column,x in enumerate(fs):put(r,column,-x)
                for price_index,(count,mult) in enumerate(zip((b,c,j,v,s,ss),multi)):
                    put(r,DIM+13*ix+2*price_index,-(1-theta)*(mult-count))
                    put(r,DIM+13*ix+2*price_index+1,-(1-theta)*count)
                put(r,DIM+13*ix+12,1);rhs.append(0.)
    mat=coo_matrix((vv,(rr,cc)),shape=(len(rhs),nvar)).tocsr()
    obj=[float(a*u[source]+b*u[5]+c*K) for a,b,c in prefix.budget_vectors(k)]
    for mult in multi:
        obj += [float(mult*(pk-2)*u[5]),float(mult*u[5]),float(mult*(pk-2)*K),float(mult*K)]
        obj += [float(mult*u[price_source])]*18
    obj += [0.]*(nvar-DIM)
    for ix,key in enumerate(keys):obj[DIM+13*ix+12]=-float(states[key])
    eq=np.zeros((1,nvar));eq[0,prefix.NAMES.index('sourceT')]=eq[0,prefix.NAMES.index('sourceC')]=1
    bounds=[(0,box)]*DIM+[(None,None)]*(nvar-DIM)
    for name in ('sourceT','sourceC'):bounds[prefix.NAMES.index(name)]=(0,1)
    if k==3:
        for name in ('price:s','price:ss','cap:s','cap:ss'):bounds[prefix.NAMES.index(name)]=(0,0)
        for j in range(DA+4*DP,DIM):bounds[j]=(0,0)
        for ix in range(len(keys)):
            for j in range(8,12):bounds[DIM+13*ix+j]=(0,0)
    if pk==2:
        for j in range(6):
            for pos in (0,2):bounds[DA+j*DP+pos]=(0,0)
    sol=linprog(obj,A_ub=mat,b_ub=rhs,A_eq=eq,b_eq=[1.],bounds=bounds,method='highs')
    rec={'source':source+1,'k':k,'price_source':price_source+1,'price_k':pk,
         'member':member,'orbit':list(orb),'theta':str(theta),'states':len(states),'success':sol.success}
    if not sol.success:rec['message']=sol.message;return rec
    for grid in (1000,10000,100000,1000000,10000000):
        ints=[max(0,round(float(x)*grid)) for x in sol.x[:DIM]]
        denom=ints[prefix.NAMES.index('sourceT')]+ints[prefix.NAMES.index('sourceC')];assert denom>0
        params=[F(x,denom) for x in ints];alpha=params[:DA]
        prices=[params[DA+j*DP:DA+(j+1)*DP] for j in range(6)]
        bgt=budgets(k,pk,alpha,prices);sums=[F(0)]*3
        for st,mass in states.items():
            parts=projection(*st,k,price_source,theta,alpha,prices,components=True)
            for j,x in enumerate(parts):sums[j]+=mass*x
        value=bgt[0]*u[source]+bgt[1]*u[price_source]+bgt[2]*u[5]+bgt[3]*K-sums[0]
        if sol.fun>=-1e-9 or value<0:break
    active={label:{name:str(x) for name,x in zip(PRICE_NAMES,beta) if x}
            for label,beta in zip(LABELS,prices) if any(beta)}
    rec.update(float_objective=float(sol.fun),grid=grid,common_source_denominator=denom,
               alpha={n:str(x) for n,x in zip(prefix.NAMES,alpha) if x},prices=active,
               budget=list(map(str,bgt)),exact_slack=str(value),exact_slack_float=float(value))
    if value<0:
        row,count=exact_row(cols,hs,source,price_source,member,orb,theta,alpha,prices)
        assert sum((a*F(c['weight']) for a,c in zip(row,cols)),F(0))==value
        _,old_u6,old_K=(sum((a*b[j] for a,b in zip(alpha,prefix.budget_vectors(k))),F(0)) for j in range(3))
        before=u[source]+old_u6*u[5]+old_K*K-sums[1]
        rec.update(prefix_only_slack=str(before),
                   separate_projection_slack=str(bgt[0]*u[source]+bgt[1]*u[price_source]+bgt[2]*u[5]+bgt[3]*K-sums[1]-sums[2]),
                   joint_projection_gain=str(sums[0]-sums[1]-sums[2]),
                   full_column_count=len(cols),full_projected_states=count,
                   row_nonzero=[[j,str(x)] for j,x in enumerate(row) if x],
                   row_sha256=hashlib.sha256(json.dumps(list(map(str,row)),separators=(',',':')).encode()).hexdigest())
    return rec


def main():
    ap=argparse.ArgumentParser();ap.add_argument('input');ap.add_argument('output')
    ap.add_argument('--source',type=int,default=3);ap.add_argument('--price-source',type=int,default=4)
    ap.add_argument('--theta',default='1/2');ap.add_argument('--box',type=int,default=1000)
    args=ap.parse_args();data,cols,hs,K,u=data_api.read_input(args.input);results=[]
    source=args.source-1;price_source=args.price_source-1;theta=F(args.theta)
    assert 0<=source<=3 and 0<=price_source<=4 and 0<=theta<1
    for member,orb in itertools.product((0,1),data_api.ORBS):
        r=discover_case(cols,hs,K,u,source,price_source,member,orb,theta,args.box);results.append(r)
        print('CASE',source+1,'priced by',price_source+1,member,orb,str(theta),
              r.get('exact_slack_float',r.get('message')),'prices',list(r.get('prices',{})),flush=True)
    neg=[r for r in results if F(r.get('exact_slack','0'))<0]
    report={'scope':'balanced arbitrary-tail actual-source uniform positive prices inside a separately paid actual-source prefix',
            'input':args.input,'input_sha256':hashlib.sha256(Path(args.input).read_bytes()).hexdigest(),'input_W':data['W'],
            'source_normalization':'alpha[sourceT]+alpha[sourceC]=1; each price a0=sum static and self query weights',
            'other_weight_discovery_box':[0,args.box],'alpha_names':prefix.NAMES,'price_names':PRICE_NAMES,
            'budget_order':[f'u{source+1}',f'u{price_source+1}','u6','K'],
            'columns':len(cols),'cases':len(results),'negative_cases':len(neg),'results':results}
    Path(args.output).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print({'cases':len(results),'negative_cases':len(neg)},flush=True)


if __name__=='__main__':main()
