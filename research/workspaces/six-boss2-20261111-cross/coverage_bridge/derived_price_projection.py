#!/usr/bin/env python3
"""A fixed balanced u5-derived positive catalog price inside an earlier cone.

The 332 original shared-query weights and six new catalog-price weights are
customer independent.  u_source, u5, u6 and K are billed separately.  The old
six-C portfolio is fixed before any hidden reply is priced.
"""
from __future__ import annotations

import argparse,hashlib,itertools,json
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

import macro_pair_requery as old
import joint_discounted_requery as data_api
from discounted_requery import dot

LABELS=('b','c','j','v','s','ss')
NAMES=old.NAMES+[f'derived_price:{n}' for n in LABELS]
DIM=len(NAMES)


def price_from_actual_and_count(actual,L):
    p=sum(actual[:4]);ell=sum(actual[:5]);q=(2*actual[5]+L)/8
    assert 0<=q<=1
    b=F(3,8*(ell+1))+F(1,64)
    A=q/(p+1);C=b+q/(p+2);D=F(1,p+1)-b
    kappa=F(3,4)*(C-A+D)-D
    baseline=A+min(F(0),kappa)
    w=(p+2-q)/(4*(p+1)*(p+2))
    assert w==C-A-kappa and F(1,4*(p+2))<=w<=F(1,4*(p+1))
    return baseline,w


def price(qs,orb):
    actual=tuple(int(v) for v in qs[:6]);diag=orb[1]
    L=qs[8]+(F(0) if diag else qs[11])+(5 if diag else 4)*qs[16]
    assert L.denominator==1 and 0<=L<=6
    return price_from_actual_and_count(actual,L)


def verify_price_uniformity(hs):
    cases=0
    for h in hs.values():
        col=h['column'];actual=tuple(map(int,col['actual_bits']))
        total=sum(F(n)*word[2] for n,word in zip(col['hist'],itertools.product((0,1),repeat=3)))
        direct=price_from_actual_and_count(actual,total)
        for group in h['groups']:
            for st in itertools.product((0,1),repeat=2):
                qs=data_api.query_vector(actual,col['hist'],group,st)
                assert price(qs,group[:2])==direct
                cases+=1
    return cases


def extra_features(b,c,j,v,s,ss,k,baseline,w):
    counts=(b,c,j,v,s,ss);multiplicities=(1,1,1,1,k-3,k-3)
    return tuple(mult*baseline+w*count for mult,count in zip(multiplicities,counts))


def projection(p,ell,t0,qs,k,orb,alpha,gamma,parts=False):
    baseline,w=price(qs,orb);weights=old.compressed_weights(alpha,qs);joint=[];prefix=[]
    for b,c,j,v in itertools.product((0,1),repeat=4):
        for s,ss in itertools.product(range(k-2),repeat=2):
            raw=old.raw_pair(p,ell,t0,b,c,j,v,s,ss,k)
            val=sum((dot(x,y) for x,y in zip(raw,weights)),F(0))
            prefix.append(val);joint.append(val+dot(gamma,extra_features(b,c,j,v,s,ss,k,baseline,w)))
    if parts:return min(joint),min(prefix),baseline
    return min(joint)


def budgets(k,alpha,gamma):
    bs=old.budget_vectors(k)
    sr,u6,K=(sum((a*b[j] for a,b in zip(alpha,bs)),F(0)) for j in range(3))
    uses=sum(gamma[:4],F(0))+(k-3)*sum(gamma[4:],F(0))
    return sr,uses,u6+F(3,8)*uses,K+uses/64


def exact_row(cols,hs,source,member,orb,alpha,gamma):
    k=6-source;ct=6 if orb[1] else 30;sr,u5,u6,K=budgets(k,alpha,gamma);assert sr==1
    out=[F(0)]*len(cols);cache={};hi=None
    def value(h,g,st):
        actual=tuple(map(int,h['column']['actual_bits']));qs=data_api.query_vector(actual,h['column']['hist'],g,st)
        key=sum(actual[:source]),sum(actual[:5]),st[member],qs
        if key not in cache:cache[key]=projection(*key,k,orb,alpha,gamma)
        return cache[key]
    for index,col in enumerate(cols):
        if col['kind']=='K':out[index]=K
        elif col['kind']=='hist':
            hi=index;h=hs[index];a=tuple(map(int,col['actual_bits']));den=sum(a)
            out[index]=data_api.share(a[source],den)+u5*data_api.share(a[4],den)+u6*data_api.share(a[5],den)
            out[index]-=sum((F(n,ct)*value(h,g,(0,0)) for g,n in h['groups'].items() if g[:2]==orb),F(0))
        elif col['kind']=='joint-reply':
            f,diag,wi,wj=col['group'];g=f,diag,tuple(wi),tuple(wj)
            if g[:2]!=orb:continue
            h=hs[hi];out[index]=-F(h['groups'][g],ct)*(value(h,g,tuple(col['state']))-value(h,g,(0,0)))
    return out,len(cache)


def discover_case(cols,hs,K,u,source,member,orb,box):
    k=6-source;states=data_api.state_measure(hs,source,member,orb);keys=list(states);nvar=DIM+len(keys)
    rr=[];cc=[];vv=[];rhs=[]
    for ix,(p,ell,t0,qs) in enumerate(keys):
        baseline,w=price(qs,orb)
        for b,c,j,v in itertools.product((0,1),repeat=4):
            for s,ss in itertools.product(range(k-2),repeat=2):
                r=len(rhs);fs=old.float_features(old.raw_pair(p,ell,t0,b,c,j,v,s,ss,k),qs)
                fs+=list(map(float,extra_features(b,c,j,v,s,ss,k,baseline,w)))
                for column,val in enumerate(fs):
                    if val:rr.append(r);cc.append(column);vv.append(-val)
                rr.append(r);cc.append(DIM+ix);vv.append(1.);rhs.append(0.)
    mat=coo_matrix((vv,(rr,cc)),shape=(len(rhs),nvar)).tocsr()
    base_budgets=old.budget_vectors(k);B5=u[4]+F(3,8)*u[5]+K/64
    obj=[float(a*u[source]+b*u[5]+c*K) for a,b,c in base_budgets]
    obj += [float(mult*B5) for mult in (1,1,1,1,k-3,k-3)]
    obj += [-float(states[key]) for key in keys]
    eq=np.zeros((1,nvar));eq[0,old.NAMES.index('sourceT')]=eq[0,old.NAMES.index('sourceC')]=1
    bounds=[(0,box)]*DIM+[(None,None)]*len(keys)
    for name in ('sourceT','sourceC'):bounds[old.NAMES.index(name)]=(0,1)
    if k==3:
        for name in ('price:s','price:ss','cap:s','cap:ss','derived_price:s','derived_price:ss'):bounds[NAMES.index(name)]=(0,0)
    sol=linprog(obj,A_ub=mat,b_ub=rhs,A_eq=eq,b_eq=[1.],bounds=bounds,method='highs')
    r={'source':source+1,'k':k,'member':member,'orbit':list(orb),'states':len(states),'success':sol.success}
    if not sol.success:r['message']=sol.message;return r
    # Common grid makes the full exact certificate readable and cheap to replay.
    for grid in (1000,10000,100000,1000000,10000000):
        ints=[max(0,round(float(v)*grid)) for v in sol.x[:DIM]]
        source_mass=ints[old.NAMES.index('sourceT')]+ints[old.NAMES.index('sourceC')];assert source_mass>0
        weights=[F(x,source_mass) for x in ints];alpha,gamma=weights[:old.DIM],weights[old.DIM:]
        bgt=budgets(k,alpha,gamma);sums=[F(0)]*3
        for st,mass in states.items():
            parts=projection(*st,k,orb,alpha,gamma,parts=True)
            for j,val in enumerate(parts):sums[j]+=mass*val
        value=bgt[0]*u[source]+bgt[1]*u[4]+bgt[2]*u[5]+bgt[3]*K-sums[0]
        if sol.fun>=-1e-9 or value<0:break
    r.update(float_objective=float(sol.fun),grid=grid,common_source_denominator=source_mass,
             alpha={n:str(x) for n,x in zip(old.NAMES,alpha) if x},
             gamma={n:str(x) for n,x in zip(LABELS,gamma) if x},budget=list(map(str,bgt)),
             exact_slack=str(value),exact_slack_float=float(value))
    if value<0:
        row,nstates=exact_row(cols,hs,source,member,orb,alpha,gamma)
        assert sum((v*F(c['weight']) for v,c in zip(row,cols)),F(0))==value
        _,old_u,old_K=(sum((a*b[j] for a,b in zip(alpha,base_budgets)),F(0)) for j in range(3))
        before=u[source]+old_u*u[5]+old_K*K-sums[1]
        r.update(prefix_only_slack=str(before),separate_projection_slack=str(before+bgt[1]*(B5-sums[2])),
                 joint_projection_gain=str(sums[0]-sums[1]-bgt[1]*sums[2]),
                 full_column_count=len(cols),full_projected_states=nstates,
                 row_nonzero=[[i,str(v)] for i,v in enumerate(row) if v],
                 row_sha256=hashlib.sha256(json.dumps(list(map(str,row)),separators=(',',':')).encode()).hexdigest())
    return r


def main():
    ap=argparse.ArgumentParser();ap.add_argument('input');ap.add_argument('output');ap.add_argument('--sources',default='4');ap.add_argument('--box',type=int,default=1000)
    args=ap.parse_args();data,cols,hs,K,u=data_api.read_input(args.input);checked=verify_price_uniformity(hs);results=[]
    for source in [int(x)-1 for x in args.sources.split(',')]:
        for member,orb in itertools.product((0,1),data_api.ORBS):
            r=discover_case(cols,hs,K,u,source,member,orb,args.box);results.append(r)
            print('CASE',source+1,member,orb,r.get('exact_slack_float',r.get('message')),'gamma',r.get('gamma'),flush=True)
    neg=[r for r in results if F(r.get('exact_slack','0'))<0]
    report={'scope':'fixed positive u5-derived uniform catalog price in earlier shared 34+PAIR; explicit distinct actual income wallets',
            'input':args.input,'input_sha256':hashlib.sha256(Path(args.input).read_bytes()).hexdigest(),'input_W':data['W'],
            'theta':'3/4','static_price_query':'q=(2*A6+sum six original C_i)/8, independent of priced theme',
            'uniformity_cases':checked,'source_normalization':'alpha[sourceT]+alpha[sourceC]=1',
            'other_weight_discovery_box':[0,args.box],'alpha_names':old.NAMES,'gamma_names':LABELS,
            'budget_order':['actual_source','u5','u6','K'],'columns':len(cols),'cases':len(results),'negative_cases':len(neg),'results':results}
    Path(args.output).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print({'cases':len(results),'negative_cases':len(neg)},flush=True)


if __name__=='__main__':main()
