"""Three-actor Cartesian-product convexification mechanism.

This computes an asymptotic product relaxation, not an actual SPE witness.
A negative value needs rational reconstruction plus finite rounding control.
The exact menu characterization is written in cartesian_limit.md.
"""
from pathlib import Path
import argparse,json,random,sys
sys.dont_write_bytecode=True
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from math import lcm
import numpy as np
from scipy.optimize import linprog

def analyze(k,w):
    inc=np.array([[(t>>a)&1 for a in range(k)] for t in range(1,1<<k)],np.int64);w=np.array(w,np.int64)
    triples=list(product(range(k),repeat=3));pay={}
    for z in triples:
        load=inc[:,z].sum(axis=1);sc=np.array([6//int(x) if x else 0 for x in load])*w
        pay[z]=tuple(sc@inc)
    phi=[];menus=[];ga=[];pure_ga=[];ga_mix=[]
    for a in range(k):
        rows=[];floors=[]
        for b in range(k):
            choices=[c for c in range(k) if pay[a,b,c][c]==max(pay[a,b,d][d] for d in range(k))]
            floors.append(min(pay[a,b,c][b] for c in choices))
            rows.extend((a,b,c) for c in choices)
        f=max(floors);phi.append(f);menus.append(rows)
        u1=np.array([pay[z][z[0]] for z in rows])/6;u2=np.array([pay[z][z[1]] for z in rows])/6
        pure_ga.append(min(u1[j] for j in range(len(rows)) if u2[j]>=f/6-1e-9))
        lp=linprog(u1,A_ub=[-u2],b_ub=[-f/6],A_eq=[np.ones(len(rows))],b_eq=[1],bounds=(0,None),method='highs');assert lp.success
        ga.append(lp.fun);ga_mix.append([(z,float(p)) for z,p in zip(rows,lp.x) if p>1e-9])
    g=max(ga);rows=[z for r in menus for z in r]
    u1=np.array([pay[z][z[0]] for z in rows])/6;u2=np.array([pay[z][z[1]] for z in rows])/6;u3=np.array([pay[z][z[2]] for z in rows])/6
    y2=np.array([pay[z][z[1]]-phi[z[0]] for z in rows])/6;W=u1+u2+u3
    lp=linprog(W,A_ub=np.array([-u1,-y2]),b_ub=[-g-1e-6,0],A_eq=[np.ones(len(rows))],b_eq=[1],bounds=(0,None),method='highs')
    if not lp.success:
        lp=linprog(W,A_ub=np.array([-u1,-y2]),b_ub=[-g,0],A_eq=[np.ones(len(rows))],b_eq=[1],bounds=(0,None),method='highs');assert lp.success
    B=list(combinations_with_replacement(range(k),2));M=np.array([(w/(1+inc[:,b].sum(axis=1)))@inc for b in B])
    sec=linprog(np.r_[np.zeros(k),-1.],A_ub=np.c_[-M,np.ones(len(B))],b_ub=np.zeros(len(B)),A_eq=[np.r_[np.ones(k),0]],b_eq=[1],bounds=[(0,None)]*k+[(None,None)],method='highs');assert sec.success
    v=sec.x[-1]
    return dict(status='numerical asymptotic Cartesian-product relaxation only',k=k,weights=w.tolist(),phi=[x/6 for x in phi],root_floor_by_action=ga,pure_root_floor_by_action=pure_ga,root_floor=g,pure_root_floor=max(pure_ga),root_minimizers=ga_mix,relaxed_W=lp.fun,security=v,gap=lp.fun-3*v,actual_payoffs=[float(u@lp.x) for u in [u1,u2,u3]],actual_second_surplus=float(y2@lp.x),actual_first_margin=float(u1@lp.x-g),actual_mix=[dict(terminal=z,probability=float(p)) for z,p in zip(rows,lp.x) if p>1e-9],query=sec.x[:-1].tolist(),opponent=[dict(background=b,probability=float(q)) for b,q in zip(B,-sec.ineqlin.marginals) if q>1e-9])

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--k',type=int,default=6);ap.add_argument('--samples',type=int,default=500);ap.add_argument('--seed',type=int,default=7301201);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();rng=random.Random(a.seed);best=None;count=0
    for i in range(a.samples):
        d=rng.choice([.1,.3,.6,1]);w=[rng.randint(1,20) if rng.random()<d else 0 for _ in range((1<<a.k)-1)];w[-1]=0
        if not any(w):continue
        z=analyze(a.k,w);count+=1
        if best is None or z['gap']<best['gap']-1e-8:
            best=z;print(json.dumps(dict(sample=i,gap=z['gap'],first_margin=z['actual_first_margin'],W=z['relaxed_W'],v=z['security'])),flush=True)
        if z['gap'] < -1e-6:break
    a.output.write_text(json.dumps(dict(status='numerical product-limit mechanism screen, not finite SPE proof',completed=count,requested=a.samples,seed=a.seed,best=best),indent=2)+'\n')

if __name__=='__main__':main()
