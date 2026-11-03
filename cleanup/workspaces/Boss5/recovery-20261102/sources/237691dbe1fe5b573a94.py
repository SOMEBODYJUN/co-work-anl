"""Discovery only: exact potential + nonnegative utilities + clone dominance.

Every sampled formal strategy keeps every ordered-history SPE row, including
the root. LP endpoints are candidates until the independent Fraction audit.
This is a larger class than customer attraction and cannot refute Q-CAG-HALF.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import itertools
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog


def run(m=3, p=3, seeds=100, distributions=8):
    terminals = list(itertools.combinations_with_replacement(range(p), m))
    backgrounds = list(itertools.combinations_with_replacement(range(p), m-1))
    fi = {q:i for i,q in enumerate(terminals)}
    gi = {q:len(fi)+i for i,q in enumerate(backgrounds)}
    d = len(fi)+len(gi)
    def row(a, h):
        z=np.zeros(d);z[fi[tuple(sorted((*h,a)))]]=1
        z[gi[tuple(sorted(h))]]=-1
        return z
    utilities = {(a,h):row(a,h) for a in range(p) for h in backgrounds}
    valid = [u for u in utilities.values()]
    clones=[]
    for h in itertools.combinations_with_replacement(range(p),m-2):
        for a,b in itertools.product(range(p),repeat=2):
            if a!=b:
                clones.append(row(a,(*h,b))-row(a,(*h,a)))
    best=-1.; count=0
    for seed in range(seeds):
        rng=np.random.default_rng(seed)
        x=rng.normal(size=d)
        actions={}
        def end(h):
            while len(h)<m:h=(*h,actions[h])
            return h
        for k in reversed(range(m)):
            for h in itertools.product(range(p),repeat=k):
                scores=[]
                for a in range(p):
                    q=end((*h,a));scores.append(row(a,q[:k]+q[k+1:])@x)
                top=max(scores)
                actions[h]=int(rng.choice([a for a in range(p) if scores[a]>top-1e-10]))
        path=end(())
        spe=[]
        for h,a in actions.items():
            k=len(h);q=end(h);chosen=row(a,q[:k]+q[k+1:])
            for b in range(p):
                if b!=a:
                    qb=end((*h,b));spe.append(chosen-row(b,qb[:k]+qb[k+1:]))
        welfare=sum((row(a,path[:i]+path[i+1:]) for i,a in enumerate(path)),np.zeros(d))
        base=np.array(valid+clones+spe)
        for trial in range(distributions):
            query=np.ones(p)/p if trial==0 else rng.dirichlet(np.ones(p))
            caps=np.array([sum((query[a]*row(a,h) for a in range(p)),np.zeros(d)) for h in backgrounds])
            aub=np.vstack([np.column_stack([-base,np.zeros(len(base))]),np.column_stack([-caps,np.ones(len(caps))])])
            eq=np.r_[welfare,0.][None,:]
            cost=np.r_[np.zeros(d),-1.]
            result=linprog(cost,A_ub=aub,b_ub=np.zeros(len(aub)),A_eq=eq,b_eq=[1],bounds=[(-20,20)]*d+[(0,None)],method='highs')
            count+=1
            if not result.success:continue
            best=max(best,float(result.x[-1]))
            if result.x[-1]>1/(m-.5)+1e-7:
                exact=[Fraction(float(t)).limit_denominator(1000000) for t in result.x[:-1]]
                def dot(z):return sum((Fraction(int(c))*v for c,v in zip(z,exact)),Fraction())
                if any(dot(z)<0 for z in base) or dot(welfare)!=1:continue
                qp=[Fraction(float(t)).limit_denominator(1000000) for t in query]
                if sum(qp)!=1:continue
                values=[sum((qp[a]*dot(row(a,h)) for a in range(p)),Fraction()) for h in backgrounds]
                security=min(values)
                if security<=Fraction(2,2*m-1):continue
                return {'status':'exact_candidate','m':m,'p':p,'seed':seed,'trial':trial,
                        'claim':'weak aggregate security fails in clone-dominant exact-potential extension; not CAG',
                        'query':list(map(str,qp)),'security_lower':str(security),
                        'welfare':str(dot(welfare)), 'terminals':terminals,'backgrounds':backgrounds,
                        'F':[str(v) for v in exact[:len(fi)]], 'G':[str(v) for v in exact[len(fi):]],
                        'actions':[{'history':h,'action':a} for h,a in sorted(actions.items())],
                        'path':path,'checked_rows':len(base),'programs':count}
    return {'status':'finite_no_separation','m':m,'p':p,'seeds':seeds,'distributions':distributions,'programs':count,'best_numerical_security_lower':best,'scope':'not a universal result'}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--m',type=int,default=3);parser.add_argument('--p',type=int,default=3)
    parser.add_argument('--seeds',type=int,default=100);parser.add_argument('--distributions',type=int,default=8);parser.add_argument('--output',type=Path)
    args=parser.parse_args();r=run(args.m,args.p,args.seeds,args.distributions)
    payload=json.dumps(r,indent=2)+'\n'
    if args.output:args.output.write_text(payload)
    print(payload)
