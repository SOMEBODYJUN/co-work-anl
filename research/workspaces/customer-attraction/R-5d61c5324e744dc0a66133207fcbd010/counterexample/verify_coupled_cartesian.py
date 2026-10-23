#!/usr/bin/env python3
"""Independent exact complete-policy DAG audit of coupled_cartesian_family.md.
No imports from the canonical solver, no finite computation proves all n.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import lcm
import argparse, json

ACTIONS=tuple(product(range(3),repeat=2))

def inc(k,a):return tuple(x+(i==a) for i,x in enumerate(k))

def audit(n,b,s,d):
    assert n>=2 and 0<d<=b and n*d<=2*s
    m=n+2;w=((2*b-d,b,b*n),(s,s*(n+1),s))
    def u(k,a,j):return F(w[j][a],k[a])
    factor_comparisons=0
    @lru_cache(None)
    def first(k):
        nonlocal factor_comparisons
        if sum(k)==m:return None,k
        child=[first(inc(k,a))[1] for a in range(3)]
        a,e,c=k
        if a>=2 or(a>=1 and e>=1):chosen=2
        elif a==1 and e==0:chosen=1
        elif a==0 and e<=1:chosen=0
        else:chosen=max(range(3),key=lambda z:u(child[z],z,0))
        own=u(child[chosen],chosen,0)
        for z in range(3):
            assert own>=u(child[z],z,0),(n,b,s,d,'first',k,chosen,z,child)
            factor_comparisons+=1
        return chosen,child[chosen]
    @lru_cache(None)
    def second(k,mode):
        if sum(k)==m:return None,k
        x,y,z=k
        if mode=='high' and x<=1 and z<=1 and y<=n:
            chosen=1 if y<n else 0 if not x else 2
        else:chosen=0 if sum(k)==m-1 and x+z==0 else 1
        child=inc(k,chosen)
        return chosen,second(child,mode)[1]
    # Check second policies independently over all count states, including off-path.
    for t in range(m):
        for x in range(t+1):
            for y in range(t-x+1):
                k=(x,y,t-x-y)
                for mode in ('low','high'):
                    a,q=second(k,mode);v=u(q,a,1)
                    for z in range(3):
                        qz=second(inc(k,z),mode)[1]
                        assert v>=u(qz,z,1),(n,b,s,d,'second',k,mode,a,z,q,qz)
                        factor_comparisons+=1
    nodes=0;comparisons=0;minimum_slack=None
    @lru_cache(None)
    def tree(k1,k2,phase):
        nonlocal nodes,comparisons,minimum_slack
        nodes+=1
        if sum(k1)==m:return None,(k1,k2)
        if phase=='root':chosen=(0,1)
        elif phase=='afterA':chosen=(0,1)
        else:chosen=(first(k1)[0],second(k2,phase)[0])
        children={}
        for a in ACTIONS:
            if phase=='root':nextphase='afterA' if a[0]==0 else 'low'
            elif phase=='afterA':nextphase='high' if a==(0,1) else 'low'
            else:nextphase=phase
            children[a]=tree(inc(k1,a[0]),inc(k2,a[1]),nextphase)[1]
        q=children[chosen]
        own=sum(u(q[j],chosen[j],j) for j in range(2))
        for a,qa in children.items():
            alt=sum(u(qa[j],a[j],j) for j in range(2));slack=own-alt
            assert slack>=0,(n,b,s,d,'global',k1,k2,phase,chosen,a,q,qa,slack)
            comparisons+=1
            minimum_slack=slack if minimum_slack is None else min(slack,minimum_slack)
        return chosen,q
    root=(0,0,0);_,target=tree(root,root,'root')
    assert target==((2,0,n),(1,n,1)),target
    k1=k2=root;phase='root';path=[];payoffs=[]
    while sum(k1)<m:
        a,_=tree(k1,k2,phase);path.append(a)
        payoffs.append(sum(u(target[j],a[j],j) for j in range(2)))
        if phase=='root':nextphase='afterA' if a[0]==0 else 'low'
        elif phase=='afterA':nextphase='high' if a==(0,1) else 'low'
        else:nextphase=phase
        k1,k2,phase=inc(k1,a[0]),inc(k2,a[1]),nextphase
    W=sum(weight for ws,q in zip(w,target) for weight,c in zip(ws,q) if c)
    OPT=sum(map(sum,w));assert W==b*(n+2)-d+s*(n+3) and OPT==W+b
    assert sum(payoffs)==W and F(OPT,W)<=F(n+3,n+2)
    K=w[0][2]+w[1][1]
    old=lambda r: K if r==1 else K+2*b-d+s if r==2 else OPT
    padded=max(F(old(r))+(m-r)*F(K,m) for r in range(1,m+1))
    assert padded<2*W
    assert all(first((a,e,m-a-e))[1] == (a,e,m-a-e) for a in range(m+1) for e in range(m-a+1))
    return {'n':n,'m':m,'b':b,'s':s,'d':d,'weights':w,'target':target,
            'path':path,'path_payoffs':list(map(str,payoffs)),'W':W,'OPT':OPT,
            'ratio':str(F(OPT,W)),'architecture_ceiling':str(F(n+3,n+2)),
            'safe_padded_OPT':str(padded),'safe_padded_ratio':str(padded/W),
            'dag_nodes':nodes,'global_comparisons':comparisons,
            'minimum_slack':str(minimum_slack),'factor_comparisons':factor_comparisons,
            'ordered_decision_histories':(9**m-1)//8,'complete':True}

def main():
    p=argparse.ArgumentParser();p.add_argument('--max-n',type=int,default=9)
    p.add_argument('--output');a=p.parse_args()
    reports=[audit(n,3*n,2*n,3) for n in range(2,a.max_n+1)]
    # Boundary parameters exercise exact equality nd=2s and d=b.
    reports += [audit(n,b,s,d) for n,b,s,d in [(2,1,1,1),(3,2,3,2),(4,10,2,1),(5,100,5,2)]]
    output={'claim':'COUPLED-CARTESIAN-INSURANCE-v1','finite_scope_only':True,'reports':reports}
    result=json.dumps(output,indent=2)
    if a.output:
        with open(a.output,'x') as f:f.write(result+'\n')
    else:print(result)
if __name__=='__main__':main()
