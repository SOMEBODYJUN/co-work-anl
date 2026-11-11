#!/usr/bin/env python3
"""R/Z-seeded discounted same-source terminal requery with joint-state queries.

The input's 00 R/Z mass is reconstructed from its hist mass and three explicit
states.  Every source/orbit is normalized before billing source, price and K.
No old repository generator is imported.  The one reused module is this run's
independent exact two-state Bellman formula.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

from discounted_requery import share, dot, closed_values, local_audit

PAT=tuple(itertools.product((0,1),repeat=3))
ORBS=((0,0),(1,0),(1,1))
QUERY_NAMES=[f"A{i+1}" for i in range(6)]+["Ti","Bi","Ci","Tj","Bj","Cj","R","Z","other_T","other_B","other_C","current"]
NAMES=["source","alpha_mid","alpha_last","beta_mid","beta_last"]+[f"mu_{x}" for x in QUERY_NAMES]
DIM=len(NAMES)


def groups(hist):
    out={}
    for f,diag in ORBS:
        for wi,wj in itertools.product(PAT,repeat=2):
            ni,nj=hist[PAT.index(wi)],hist[PAT.index(wj)]
            n=ni if diag and wi==wj else (0 if diag else ni*nj-(ni if wi==wj else 0))
            if n:out[f,diag,wi,wj]=n
    for orb in ORBS:
        assert sum(n for g,n in out.items() if g[:2]==orb)==(6 if orb[1] else 30)
    return out


def query_vector(bits,hist,group,state):
    f,diag,wi,wj=group
    total=[sum(n*w[a] for n,w in zip(hist,PAT)) for a in range(3)]
    exc=wi if diag else tuple(a+b for a,b in zip(wi,wj))
    other=tuple(F(a-b,5 if diag else 4) for a,b in zip(total,exc))
    return tuple(map(F,bits+wi+wj+state))+other


def feature(p,ell,t,c,s,qs):
    z=p+t+s+c;den=p+t+s+1
    out=[share(t,z),F(s,ell+1),F(c,ell+1),F(s),F(c)]
    out.extend(q/den-share(c,z) for q in qs+(F(t),))
    assert len(out)==DIM
    return tuple(out)


def exact_projection(p,ell,t0,qs,k,params,theta):
    e={(t,c):min(dot(feature(p,ell,t,c,s,qs),params) for s in range(k-1))
       for t,c in itertools.product((0,1),repeat=2)}
    psi=closed_values(e,theta)
    v=tuple(z/(1-theta) for z in psi)
    for t in (0,1):
        assert v[t]==min(e[t,c]+theta*v[c] for c in (0,1))
    return psi[t0]


def read_input(path):
    data=json.loads(Path(path).read_text());cols=data['columns']
    hs={};hi=None
    for j,col in enumerate(cols):
        if col['kind']=='hist':
            hi=j
            hs[hi]={'column':col,'groups':groups(col['hist']),'states':defaultdict(dict)}
        elif col['kind']=='joint-reply':
            f,diag,wi,wj=col['group'];g=(f,diag,tuple(wi),tuple(wj))
            hs[hi]['states'][g][tuple(col['state'])]=F(col['weight'])
    for h in hs.values():
        hm=F(h['column']['weight'])
        for g in h['groups']:
            st=h['states'][g]
            assert set(st)=={(0,1),(1,0),(1,1)}
            st[(0,0)]=hm-sum(st.values(),F(0))
            assert min(st.values())>=0
    K=sum((F(c['weight']) for c in cols if c['kind']=='K'),F(0))
    u=[sum((F(h['column']['weight'])*share(int(h['column']['actual_bits'][i]),sum(map(int,h['column']['actual_bits']))) for h in hs.values()),F(0)) for i in range(6)]
    return data,cols,hs,K,u


def state_measure(hs,source,member,orb):
    states=defaultdict(F);ct=6 if orb[1] else 30
    for h in hs.values():
        col=h['column'];bits=tuple(map(int,col['actual_bits']));p=sum(bits[:source]);ell=sum(bits[:5])
        for group,count in h['groups'].items():
            if group[:2]!=orb:continue
            for st,mass in h['states'][group].items():
                if mass:
                    qs=query_vector(bits,col['hist'],group,st)
                    states[p,ell,st[member],qs]+=F(count,ct)*mass
    return {s:w for s,w in states.items() if w}


def budget(source,K,u):
    k=6-source
    return [u[source],(k-2)*u[5],u[5],(k-2)*K,K]+[F(0)]*(DIM-5)


def exact_row(cols,hs,source,member,orb,params,theta):
    k=6-source;ct=6 if orb[1] else 30
    out=[F(0)]*len(cols)
    cache={}
    def value(h,group,st):
        bits=tuple(map(int,h['column']['actual_bits']))
        p=sum(bits[:source]);ell=sum(bits[:5]);qs=query_vector(bits,h['column']['hist'],group,st)
        key=(p,ell,st[member],qs)
        if key not in cache:cache[key]=exact_projection(*key,k,params,theta)
        return cache[key]
    hi=None
    for j,col in enumerate(cols):
        if col['kind']=='K':
            out[j]=(k-2)*params[3]+params[4]
        elif col['kind']=='hist':
            hi=j;h=hs[j];bits=tuple(map(int,col['actual_bits']));den=sum(bits)
            out[j]=params[0]*share(bits[source],den)+((k-2)*params[1]+params[2])*share(bits[5],den)
            out[j]-=sum((F(n,ct)*value(h,g,(0,0)) for g,n in h['groups'].items() if g[:2]==orb),F(0))
        elif col['kind']=='joint-reply':
            f,diag,wi,wj=col['group'];g=(f,diag,tuple(wi),tuple(wj))
            if g[:2]!=orb:continue
            h=hs[hi];out[j]=-F(h['groups'][g],ct)*(value(h,g,tuple(col['state']))-value(h,g,(0,0)))
    return out,len(cache)


def discover_case(cols,hs,K,u,source,member,orb,theta):
    states=state_measure(hs,source,member,orb);keys=list(states);k=6-source;nvar=DIM+2*len(keys)
    rows=[];cc=[];vv=[];rhs=[]
    for q,(p,ell,t0,qs) in enumerate(keys):
        for t,c,s in itertools.product((0,1),(0,1),range(k-1)):
            r=len(rhs)
            for j,val in enumerate(feature(p,ell,t,c,s,qs)):
                if val:rows.append(r);cc.append(j);vv.append(-float(val))
            rows.extend([r,r]);cc.extend([DIM+2*q+t,DIM+2*q+c]);vv.extend([1.,-float(theta)])
            rhs.append(0.)
    mat=coo_matrix((vv,(rows,cc)),shape=(len(rhs),nvar)).tocsr()
    obj=list(map(float,budget(source,K,u)))+[0.]*(nvar-DIM)
    for q,key in enumerate(keys):obj[DIM+2*q+key[2]]=-(1-float(theta))*float(states[key])
    eq=np.zeros((1,nvar));eq[0,:DIM]=1
    bounds=[(0,None)]*DIM+[(None,None)]*(nvar-DIM)
    if k==2:bounds[1]=bounds[3]=(0,0)
    sol=linprog(obj,A_ub=mat,b_ub=rhs,A_eq=eq,b_eq=[1.],bounds=bounds,method='highs')
    result={'source':source+1,'member':member,'orbit':list(orb),'theta':str(theta),'states':len(states),'success':sol.success}
    if not sol.success:result['message']=sol.message;return result
    params=[F(float(x)).limit_denominator(1000000) if x>1e-10 else F(0) for x in sol.x[:DIM]]
    params=[x/sum(params,F(0)) for x in params]
    value=dot(params,budget(source,K,u))-sum((mass*exact_projection(*st,k,params,theta) for st,mass in states.items()),F(0))
    result.update(float_objective=float(sol.fun),exact_slack=str(value),exact_slack_float=float(value),parameters={n:str(x) for n,x in zip(NAMES,params) if x})
    if value<0:
        row,nstates=exact_row(cols,hs,source,member,orb,params,theta)
        dotval=sum((v*F(col['weight']) for v,col in zip(row,cols)),F(0))
        assert dotval==value
        result['full_column_count']=len(row);result['full_projected_states']=nstates
        result['row_nonzero']=[[i,str(v)] for i,v in enumerate(row) if v]
        result['row_sha256']=hashlib.sha256(json.dumps(list(map(str,row)),separators=(',',':')).encode()).hexdigest()
    return result


def main():
    ap=argparse.ArgumentParser();ap.add_argument('input');ap.add_argument('output')
    ap.add_argument('--thetas',default='0,1/4,1/2,3/4,9/10,99/100')
    ap.add_argument('--sources',default='1,2,3,4,5')
    args=ap.parse_args();data,cols,hs,K,u=read_input(args.input)
    results=[]
    for source in [int(x)-1 for x in args.sources.split(',')]:
        for member,orb,theta in itertools.product((0,1),ORBS,map(F,args.thetas.split(','))):
            r=discover_case(cols,hs,K,u,source,member,orb,theta);results.append(r)
            if F(r.get('exact_slack','0'))<0:print('CUT',source+1,member,orb,str(theta),r['exact_slack_float'],flush=True)
        print('SOURCE',source+1,'complete',flush=True)
    neg=[r for r in results if F(r.get('exact_slack','0'))<0]
    report={'scope':'R/Z seeded same-source discounted terminal orbit; full nonnegative weight cone at each sampled discount; input necessary point not SPE',
            'input':args.input,'input_sha256':hashlib.sha256(Path(args.input).read_bytes()).hexdigest(),
            'input_W':data['W'],'columns':len(cols),'K':str(K),'actual_u':list(map(str,u)),
            'parameter_names':NAMES,'cases':len(results),'negative_cases':len(neg),'audit':local_audit(),
            'results':results}
    Path(args.output).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'cases':len(results),'negative_cases':len(neg),'minimum_exact_slack':str(min(F(x.get('exact_slack','0')) for x in results))}),flush=True)


if __name__=='__main__':main()
