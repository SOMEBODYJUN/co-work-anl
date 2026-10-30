#!/usr/bin/env python3
"""Exact checks of the two explicit full-matrix witnesses; no optimizer or general theorem claim."""
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
import json


def kronecker_square():
    p={0:{0:F(1),1:F(1)},1:{2:F(1),3:F(1)}}
    bs={}
    for g in range(2):
        for l in range(2):
            for a in range(2):
                j=2+4*g+2*l+a
                b=l^(g*a)
                p[j]={2*g+l:F(1,2),4+2*a+b:F(1)}
                bs[j]=(g,l,a,b)
    assignment={}
    for j in range(10):
        for z in range(10):
            if j<2 and z<2:
                assignment[j,z]=(2*j+z,2*z+j)
            elif j<2:
                h,k,c,d=bs[z]
                assignment[j,z]=(2*j+h,4+2*c+d)
            elif z<2:
                g,l,a,b=bs[j]
                assignment[j,z]=(4+2*a+b,2*z+g)
            else:
                g,l,a,b=bs[j];h,k,c,d=bs[z]
                assignment[j,z]=(4+2*a+b,4+2*c+d) if l==h and k==g else (2*g+l,2*h+k)
    changes=[((0,7),(1,7),(0,2)),((2,1),(4,2),(0,3)),((2,6),(0,2),(4,2)),((2,7),(0,2),(4,2)),((2,8),(0,3),(4,3)),((3,9),(0,3),(6,3)),((4,7),(5,7),(1,7)),((5,7),(7,7),(1,7)),((6,1),(4,3),(2,3)),((6,8),(2,3),(4,3)),((7,9),(2,3),(7,6)),((8,7),(3,2),(5,7)),((9,1),(6,3),(3,2)),((9,7),(3,2),(6,7)),((9,9),(6,6),(6,3))]
    for job,old,new in changes:
        assert assignment[job]==old
        assignment[job]=new
    loads=defaultdict(F)
    for (j,z),(i,s) in assignment.items():
        assert i in p[j] and s in p[z]
        loads[i,s]+=p[j][i]*p[z][s]
    assert len(assignment)==100 and len(loads)==64 and set(loads.values())=={F(1)}
    finite_edges=sum(len(p[j])*len(p[z]) for j in p for z in p)
    assert finite_edges==400
    return {'machines':64,'jobs':100,'finite_edges':finite_edges,'all_machine_loads':'1','simultaneous_reassignments':len(changes),'assignments':[{'job_pair':list(j),'machine_pair':list(i)} for j,i in sorted(assignment.items())]}


def common_cycle(m):
    loads=defaultdict(F)
    jobs=0
    for x in range(m):
        loads[x,x]+=1;jobs+=1
    for i in range(m):
        for t in range(1,m):
            occupancy=[0]*m
            for x in range(m):
                d=(x-i)%m
                dest=(x+1)%m if d<t else x
                assert dest in {x,(x+1)%m}
                occupancy[dest]+=1
                loads[i,dest]+=F(1,m);jobs+=1
            assert occupancy[i]==0 and occupancy[(i+t)%m]==2
            assert all(occupancy[s]==1 for s in range(m) if s not in {i,(i+t)%m})
    assert len(loads)==m*m and set(loads.values())=={F(1)}
    assert jobs==m+m*m*(m-1)
    return {'m':m,'machines':m*m,'jobs':jobs,'finite_edges':2*m**3,'all_machine_loads':'1'}


def main():
    result={'arithmetic':'fractions.Fraction','scope':'Finite verification of stated full assignments only; no generic LP solver, hardness or general theorem test.','kronecker_square':kronecker_square(),'common_cycle':[common_cycle(m) for m in range(2,18)]}
    out=Path(__file__).with_name('structural_witness_check.json')
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'square_jobs':100,'square_machines':64,'common_cycle_m':[2,17],'checks':'passed','output':str(out)},ensure_ascii=False))


if __name__=='__main__':main()
