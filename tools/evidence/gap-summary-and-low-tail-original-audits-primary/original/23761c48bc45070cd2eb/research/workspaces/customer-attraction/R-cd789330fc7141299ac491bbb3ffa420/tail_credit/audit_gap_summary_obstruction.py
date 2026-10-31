#!/usr/bin/env python3
"""Exact arithmetic for the scalable gap-summary obstruction.

The universal formulas are proved in gap_and_deletion_obligations.md. Finite
enumeration here checks k=3,4 only, and never treats the fake menu as an SPE.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent

def counts(p,n):
    if p==1:
        yield (n,)
    else:
        for x in range(n+1):
            for tail in counts(p-1,n-x):
                yield (x,)+tail

def profit(b,q,k):
    return sum((F(k*x,x+y) for x,y in zip(q,b) if x),F())

rows=[]
for k in range(3,15):
    r=(k-1)**2+1
    b=(1,)+(0,)*(r-1)
    tail=(k-1,)+(1,)*(r-k)+(0,)*(k-1)
    assert len(tail)==r and sum(tail)==r-1
    full=(k,)+tail[1:]
    P=F(k*(r-k+1)); Pt=profit(b,tail,k)
    Froot=F(k*r); Ft=F(k*(r-1))
    tail_gap=Ft-Pt
    assert tail_gap==(k-1)**2==r-1
    root_gap=Froot-P
    assert root_gap==k*(k-1) and root_gap-r==k-2>0
    record={"k":k,"r":r,"root_payoff":"1","tail_minimum":"1",
            "root_profit":str(P),"root_optimum":str(Froot),
            "tail_profit":str(Pt),"tail_optimum":str(Ft),
            "tail_gap_minus_r_minus_1":str(tail_gap-(r-1)),
            "root_gap_minus_r":str(root_gap-r),"menu_is_SPE":False}
    if k<=4:
        qs=list(counts(r,r-1))
        best=max(profit(b,q,k) for q in qs)
        assert best==Ft
        record["tail_profiles_enumerated"]=len(qs)
        assert len(qs)==comb(2*r-2,r-1)
        for a in range(r):
            # Relabel the same actual root + tail profile to every root action.
            terminal=[0]*r;terminal[a]=k
            for j in range(1,r-k+1):
                terminal[(a+j)%r]=1
            assert sum(terminal)==r
            assert F(k,terminal[a])==1
    rows.append(record)

report={"scope":"general fake-menu summary obstruction; never a CAG SPE counterexample",
        "enumeration_scope":"k=3,4 tail optimal profiles only; all other rows exact formula arithmetic",
        "rows":rows}
(HERE/"gap_summary_obstruction_exact.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2))
