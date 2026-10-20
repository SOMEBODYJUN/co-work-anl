"""Exact integer probes for fixed-heavy EF residuals. Python standard library only."""
from itertools import product
import json,random
from pathlib import Path


def verify(n,m,s,h,x):
    revenue=[s[i]+sum(x.get((i,j),0) for j in range(n)) for i in range(n)]
    violations=[]
    for i in range(n):
        for j in range(n):
            if i!=j and revenue[i]<h.get((i,j),0)+x.get((j,i),0):
                violations.append([i,j,revenue[i],h.get((i,j),0)+x.get((j,i),0)])
    return not violations,revenue,violations


def brute(n,m,s,h):
    pairs=list(m)
    for vals in product(*(range(m[e]+1) for e in pairs)):
        x={}
        for (i,j),v in zip(pairs,vals):x[i,j]=v;x[j,i]=m[i,j]-v
        if verify(n,m,s,h,x)[0]:return x
    return None


def forest(n,m,s,h):
    adj=[[] for _ in range(n)]
    for (i,j),v in m.items():
        assert i<j and v>0
        adj[i].append(j);adj[j].append(i)
    par=[None]*n;roots=[];order=[]
    for r in range(n):
        if par[r] is not None:continue
        roots.append(r);par[r]=-1;stack=[r]
        while stack:
            i=stack.pop();order.append(i)
            for j in adj[i]:
                if j==par[i]:continue
                if par[j] is not None:raise ValueError('unit support not a forest')
                par[j]=i;stack.append(j)
    def mult(i,j):return m[min(i,j),max(i,j)]
    threshold={};upper={}
    for i in reversed(order):
        children=[j for j in adj[i] if par[j]==i]
        for j in children:
            if threshold[j]>mult(i,j):return None
            upper[i,j]=mult(i,j)-threshold[j]
        S=sum(upper[i,j] for j in children)
        # x is incoming count from parent. Other comparisons have coefficient one.
        T=0
        for j in range(n):
            if j==i or j==par[i]:continue
            rhs=h.get((i,j),0)
            if j in children:rhs+=mult(i,j)-upper[i,j]
            T=max(T,rhs-s[i]-S)
        if par[i]!=-1:
            p=par[i]
            T=max(T,(h.get((i,p),0)+mult(i,p)-s[i]-S+1)//2)
        elif T>0:return None
        threshold[i]=max(T,0)
    x={}
    for (i,j),u in upper.items():x[i,j]=u;x[j,i]=mult(i,j)-u
    assert verify(n,m,s,h,x)[0]
    return x


def main():
    n=5;m={(1,2):100,(2,3):100,(3,4):100};s=[87,0,0,0,0];h={(1,0):87}
    x={(1,2):87,(2,1):13,(2,3):74,(3,2):26,(3,4):50,(4,3):50}
    ok,rev,viol=verify(n,m,s,h,x)
    # Heavy endpoint names v,u,w,z,t. Revenue at w is 13+74=87.
    # With w-z and z-t halved, EF w against u forces u-w<=75.
    counter={'names':['v','u','w','z','t'],'heavy':[0,1,87,0],'unit_multiplicities':[[i,j,v] for (i,j),v in m.items()],
             'x':[[i,j,v] for (i,j),v in x.items()],'EF':ok,'revenue':rev,'balanced_internal_max_u':75,
             'forest_solution':[[i,j,v] for (i,j),v in forest(n,m,s,h).items()]}
    rng=random.Random(37042026);tests=0;feasible=0
    cases=[]
    for n in range(1,8):
        for _ in range(600):
            m={}
            for i in range(1,n):
                if rng.random()<.85:
                    p=rng.randrange(i);m[p,i]=rng.randrange(1,5)
            s=[rng.randrange(8) for _ in range(n)]
            h={(i,j):rng.randrange(8) for i in range(n) for j in range(n) if i!=j and rng.random()<.25}
            b=brute(n,m,s,h);d=forest(n,m,s,h)
            tests+=1;feasible+=b is not None
            if (b is None)!=(d is None):
                raise AssertionError({'n':n,'m':m,'s':s,'h':h,'b':b,'d':d})
    out={'counterexample':counter,'random_forest_checks':{'seed':37042026,'tests':tests,'feasible':feasible,'max_n':7,'multiplicities':'1..4','offsets':'0..7','mismatches':0},'arithmetic':'Python arbitrary precision integers'}
    Path(__file__).with_name('results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
