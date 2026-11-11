#!/usr/bin/env python3
"""Exact algebra for frozen zero-K prefix/tail cuts 2 and 13.

This is a finite local-signature calculation, not a strategy search. It uses
the integer-scaled rows and checks the handwritten costs against the frozen
feature implementation before publishing any table.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import hashlib
import json
from pathlib import Path

import prefix_tail_requery as original

HERE=Path(__file__).resolve().parent
PACK=HERE/'selected_prefix_tail_5752.json'
PACK_SHA='595e7386cfacc591f513fe477453e94d9e2271e4cb63ce3f5c57a8dc34fabd50'
TAIL={2:(254,67,6,4),13:(2488,659,61,43)}
SCALE={2:999,13:10000}


def div(n,d):
    assert d or n==0
    return F(n,d) if n else F(0)


@lru_cache(None)
def tail(row,p,d,n,r):
    a,M,m,l=TAIL[row]
    q=F(45*n-r,4) if row==2 else F(439*n+r,4)
    assert 0<=q<=M
    e00=min(q/(p+1),F(m,d)+q/(p+2))
    e01=(q-M)/(p+1)+F(l,d)
    e10=F(a,p+2)+F(m,d)+q/(p+3)
    e11=(a-M+q)/(p+3)+F(m+l,d)
    edges={(0,0):e00,(0,1):e01,(1,0):e10,(1,1):e11}
    # Independent raw two-middle choices check each asserted simplification.
    for t,c in product((0,1),repeat=2):
        actual=min(div(a*t-M*c,p+t+s+c)+F(m*s+l*c,d)+q/(p+t+s+1) for s in (0,1))
        assert edges[t,c]==actual
    cand0=(q/(p+1),F(m,d)+q/(p+2),(e01+e11)/2,(2*e01+e10)/3)
    cand1=(e11,(e10+q/(p+1))/2,(e10+F(m,d)+q/(p+2))/2,(2*e10+e01)/3)
    values=(min(cand0),min(cand1))
    assert values==original.closed_values(edges,F(1,2))
    return values,(cand0,cand1)


def E2(p,d,t,b,c,j,v,x,ci,bj,a6,tau):
    Q1=F(36*x+145*ci+36*bj);Qp=2*a6+5*x+4*bj+13*tau
    return (div(431*t-24*b-241*c,p+t+b+c)
            +div(314*c-j-126*v,p+c+j+v)+F(2*b+64*j+63*v,d)
            +Q1/(p+t+b+1)+(124*b+tau)/(p+c+j+1)
            +(Qp+24*c)/(p+t+1)-(Qp*c+24*b)/((p+t+1)*(p+t+2))
            +(tau+b)/(p+c+1)-(tau*b+j)/((p+c+1)*(p+c+2)))


def E13(p,d,t,b,c,j,v,a6,n,r):
    Q2=F(103*n+r,4);Qp=F(39*n+r,4)
    return (div(4325*t-2196*c,p+t+b+c)
            +div(3187*c-59*j-1295*v,p+c+j+v)+F(630*j+624*v,d)
            +F(34*j+2162*a6,p+t+b+1)+(1081*b+Q2)/(p+c+j+1)
            +(Qp+59*v)/(p+c+1)-(Qp*v+59*j)/((p+c+1)*(p+c+2)))


@lru_cache(None)
def L2(p,d,t,x,y,ci,bj,a6,n):
    tau=F(n-x-y,4);assert 0<=tau<=1
    psi,_=tail(2,p,d,n,x+y)
    return min(E2(p,d,t,b,c,j,v,x,ci,bj,a6,tau)+psi[v] for b,c,j,v in product((0,1),repeat=4))


@lru_cache(None)
def L13(p,d,t,a6,n,r):
    psi,_=tail(13,p,d,n,r)
    return min(E13(p,d,t,b,c,j,v,a6,n,r)+psi[v] for b,c,j,v in product((0,1),repeat=4))


def lower2(p,d,t,x,y,ci,bj,a6,n):
    tau=F(n-x-y,4)
    return (L2(p,d,t,0,0,0,0,0,0)
            +(41*x+145*ci+40*bj+2*a6+13*tau)/(p+t+2)
            +(11*(x+y)+47*tau)/(p+3))


def lower13(p,d,t,a6,n,r):
    return L13(p,d,t,0,0,0)+F(2162*a6,p+t+2)+F(581*n+3*r,4*(p+3))


def make_queries(p,d,t,x,y,ci,bj,a6,n,row):
    actual=[int(i<p) for i in range(3)]+[int(d-p-1>=1),int(d-p-1>=2),a6]
    return tuple(map(F,actual+[x,0,ci,y,bj,0,t if row==2 else 0,t if row==13 else 0]))+(F(n-x-y,4),F(0),F(0))


def orbit_average(row,p,d,a6,n):
    out=F(0)
    for x,y in product((0,1),repeat=2):
        count=(n*(n-1) if x and y else (6-n)*(5-n) if not x and not y else n*(6-n))
        if not count:continue
        if row==2:value=min(L2(p,d,t,x,y,0,0,a6,n) for t in (0,1))
        else:value=min(L13(p,d,t,a6,n,x+y) for t in (0,1))
        out+=F(count,30)*value
    return out


def main():
    assert hashlib.sha256(PACK.read_bytes()).hexdigest()==PACK_SHA
    pack=json.loads(PACK.read_text());checks=0;rows={}
    for row in (2,13):
        cut=pack['cuts'][row-1];scale=SCALE[row]
        alpha=[scale*F(cut['alpha'].get(name,'0')) for name in original.prefix.NAMES]
        beta=[scale*F(cut['beta'].get(name,'0')) for name in original.tail.NAMES]
        rows[row]=(alpha,beta)
    # Check handwritten E identities on all relevant count contexts and all
    # hidden states, at a basis of visible query coordinates.
    for row in (2,13):
        alpha,beta=rows[row]
        for p,extra,t in product(range(4),range(3),(0,1)):
            d=p+extra+1
            signatures=((0,0,0,0,0,0),(1,0,0,0,0,1),(0,1,0,0,0,1),
                        (0,0,1,0,0,0),(0,0,0,1,0,0),(0,0,0,0,1,0),(0,0,0,0,0,4))
            for x,y,ci,bj,a6,n in signatures:
                qs=make_queries(p,d,t,x,y,ci,bj,a6,n,row)
                cw=original.prefix.compressed_weights(alpha,qs)
                for b,c,j,v in product((0,1),repeat=4):
                    raw=original.prefix.raw_pair(p,d-1,t,b,c,j,v,0,0,3)
                    reference=sum((original.dot(a,b) for a,b in zip(raw,cw)),F(0))
                    hand=(E2(p,d,t,b,c,j,v,x,ci,bj,a6,F(n-x-y,4)) if row==2
                          else E13(p,d,t,b,c,j,v,a6,n,x+y))
                    assert reference==hand,(row,p,d,t,b,c,j,v,(x,y,ci,bj,a6,n),reference,hand)
                    checks+=1
    table2=[];table13=[];lower_checks=[0,0];monotonic_seed=[True,True]
    for p,extra in product(range(4),range(3)):
        d=p+extra+1
        for x,y,ci,bj,a6,m in product((0,1),(0,1),(0,1),(0,1),(0,1),range(5)):
            n=x+y+m
            vv=[L2(p,d,t,x,y,ci,bj,a6,n) for t in (0,1)]
            for t in (0,1):
                assert vv[t]>=lower2(p,d,t,x,y,ci,bj,a6,n)
                assert vv[t]>=L2(p,d,t,x,y,0,0,a6,n)
                lower_checks[0]+=1
            monotonic_seed[0]&=vv[1]>=vv[0]
            table2.append({'p':p,'d':d,'x':x,'y':y,'Ci':ci,'Bj':bj,'A6':a6,'n':n,'L':list(map(str,vv))})
        for a6,r,m in product((0,1),range(3),range(5)):
            n=r+m;vv=[L13(p,d,t,a6,n,r) for t in (0,1)]
            for t in (0,1):
                assert vv[t]>=lower13(p,d,t,a6,n,r);lower_checks[1]+=1
            monotonic_seed[1]&=vv[1]>=vv[0]
            table13.append({'p':p,'d':d,'A6':a6,'n':n,'r':r,'L':list(map(str,vv))})
    baseline=[];coverage={};averages={}
    for row in (2,13):
        baseline_row=[];av=[]
        for p,extra in product(range(4),range(3)):
            d=p+extra+1
            vals=[L2(p,d,t,0,0,0,0,0,0) if row==2 else L13(p,d,t,0,0,0) for t in (0,1)]
            baseline_row.append({'p':p,'d':d,'base0':str(vals[0]),'base1':str(vals[1]),'seed_increment':str(vals[1]-vals[0])})
            for a6,n in product((0,1),range(7)):
                v=orbit_average(row,p,d,a6,n)
                av.append({'p':p,'d':d,'A6':a6,'n':n,'average':str(v)})
        miss=[orbit_average(row,0,1,0,n) for n in range(1,7)]
        A=min(miss)
        taxes=[(A*int(x['n']>0)-F(x['average']),x) for x in av if x['d']-1+x['A6']>0]
        B,worst=max(taxes,key=lambda z:z[0])
        assert orbit_average(row,0,1,0,0)>=0
        baseline.append({'cut':row,'entries':baseline_row})
        coverage[str(row)]={'uncovered_by_opt_multiplicity':list(map(str,miss)),
                            'uncovered_min_credit':str(A),'covered_tax':str(B),'worst_tax_signature':worst}
        averages[str(row)]=av
    out={'scope':'exact finite local count identities and analytic lower bounds, not complete SPE witnesses',
         'frozen_package_sha256':PACK_SHA,'integer_scales':SCALE,'feature_identity_checks':checks,
         'lower_bound_checks':lower_checks,'seed_monotone_on_complete_discrete_visible_domains':monotonic_seed,
         'baselines':baseline,'coverage_lower_bounds':coverage,'averages':averages,
         'cut2_complete_visible_table':table2,'cut13_complete_visible_table':table13}
    (HERE/'mainline_zero_capacity_v1.json').write_text(json.dumps(out,indent=2)+'\n')
    print({'feature_identity_checks':checks,'lower_bound_checks':lower_checks,'seed_monotone':monotonic_seed,
           'baselines':baseline,'coverage_lower_bounds':coverage})


if __name__=='__main__':main()
