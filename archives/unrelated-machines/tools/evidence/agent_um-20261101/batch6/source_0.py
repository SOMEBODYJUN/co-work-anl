"""Exact standalone star law audit; actual OPT is one, no deep-owner law is built."""
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path
import argparse
import json


def falling(n,k):
    v=1
    for a in range(k):v*=n-a
    return v


def laws(d,s):
    assert d%2==s%2==0 and 2<=s<=d//2
    eta=F(s,d);h=s//2
    p=eta**3/1000;u=4*p*(1-eta);e=1-F(1,5)-p-u
    raw=[(1,d,p),(1,0,F(1,20)),(1,h,F(1,20)),
         (0,0,F(1,20)),(0,h,F(1,20)),(0,d//2,u),(0,d,e)]
    cfg=[(1,s,p/eta),(1,0,F(1,20)+p-p/eta),(1,h,F(1,20)),
         (0,0,F(1,20)+u/2),(0,h,F(1,20)),(0,d,e+u/2)]
    assert sum(p for _,_,p in raw)==sum(p for _,_,p in cfg)==1
    assert all(p>=0 for _,_,p in raw+cfg)
    assert all(F(c)+F(k,d)<=1+eta for c,k,p in cfg)
    return eta,raw,cfg


def value(d,law,has_c,home_count,weighted=False,eta=None):
    denom=falling(d,home_count)
    ans=F(0)
    for c,h,p in law:
        if has_c and not c:continue
        prob=F(falling(h,home_count),denom)
        ans+=p*prob*((1+eta-c-F(h,d)) if weighted else 1)
    return ans


def masks(n,degree):
    return [sum(1<<j for j in subset) for k in range(degree+1)
            for subset in combinations(range(n),k)]


def matrix(d,law,degree,weighted=False,eta=None):
    basis=masks(d+1,degree)
    cache={}
    def get(mask):
        key=(bool(mask&1),(mask>>1).bit_count())
        if key not in cache:cache[key]=value(d,law,*key,weighted=weighted,eta=eta)
        return cache[key]
    return [[get(a|b) for b in basis] for a in basis]


def exact_psd(a):
    a=[list(row) for row in a];rank=0
    for i in range(len(a)):
        pivot=a[i][i]
        assert pivot>=0,('negative pivot',i,pivot)
        col=[a[j][i] for j in range(i+1,len(a))]
        if not pivot:
            assert not any(col),('nonzero zero-pivot row',i)
            continue
        rank+=1
        for jj,x in enumerate(col,i+1):
            if not x:continue
            for kk in range(jj,len(a)):
                y=col[kk-i-1]
                if y:
                    a[kk][jj]-=x*y/pivot
                    a[jj][kk]=a[kk][jj]
    return {'dimension':len(a),'rank':rank,'exact_PSD':True}


def audit(d,s,full=False):
    eta,raw,cfg=laws(d,s)
    for mask in masks(d+1,2):
        key=(bool(mask&1),(mask>>1).bit_count())
        assert value(d,raw,*key)==value(d,cfg,*key)
    lam=F(2,eta)
    assert 4*lam*lam-4*lam+3<=16/(eta*eta)
    p=eta**3/1000
    assert F(eta,40)>p*(1-eta)*16/(eta*eta)
    a=[]
    for c,h,prob in raw:
        vec=[F(1),F(h,d),F(h*(h-1),d*(d-1)),F(c),F(c*h,d)]
        a.append((prob*(1+eta-c-F(h,d)),vec))
    sym=[[sum(w*v[i]*v[j] for w,v in a) for j in range(5)] for i in range(5)]
    out={'d':d,'s':s,'eta':str(eta),'bad_mass':str(p),
         'row_CFG_first_pair_exact':True,'symmetric_signedslack':exact_psd(sym),
         'original_machines':d+2,'original_jobs':d+1,'finite_entries':2*(d+1),
         'complete_actual_OPT1_assignment':'all original jobs at their unique homes'}
    if full:
        out['full_M3']=exact_psd(matrix(d,raw,3))
        out['full_global_quadratic_signedslack']=exact_psd(matrix(d,raw,2,True,eta))
        states=[]
        for c,h,prob in raw:
            for subset in combinations(range(d),h):
                mask=c|sum(1<<(j+1) for j in subset)
                states.append((mask,prob/comb(d,h)))
                loads=[F(1-c),F(c)+F(h,d)]+[F(j not in subset) for j in range(d)]
                assert all(x<=1 for i,x in enumerate(loads) if i!=1)
                assert len(loads)==d+2 and max(loads)<=2
        assert sum(prob for _,prob in states)==1
        for monomial in masks(d+1,min(6,d+1)):
            direct=sum(prob for mask,prob in states if (mask&monomial)==monomial)
            assert direct==value(d,raw,bool(monomial&1),(monomial>>1).bit_count())
        out['full_assignment_states_enumerated']=len(states)
        out['all_degree_le_six_true_moments_checked']=len(masks(d+1,min(6,d+1)))
    return out


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    if args.output.exists():parser.error('output already exists')
    cases=[audit(d,s,full=d in (4,8)) for d,s in
           [(4,2),(8,2),(8,4),(16,2),(16,4),(16,8),
            (64,2),(64,16),(64,32),(1000,2),(1000,100),(1000,500)]]
    result={'scope':__doc__,'cases':cases,
            'not_claimed':['actual gap greater than one','deep internal-child budget',
                           'full growing-depth H_U law','general algorithm']}
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'exact_cases':len(cases),'full_small_M3_and_quadratic_checks':3,
                      'output':str(args.output)},sort_keys=True))


if __name__=='__main__':main()
