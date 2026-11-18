"""Necessary-row all-depth probe with multiple previously committed disjoint optimum anchors."""
from itertools import product
import numpy as np
from scipy.optimize import linprog

def solve(i,k,floors, witness=False):
    # i past actions, including k marked, distinct, optimal labels of size 1.
    groups=[0,1]+([2] if k<5 else [])+([3] if k else [])
    types=[(b,r,(int(r==1),)+z) for b in range(i-k+1) for r in groups for z in product(range(2),repeat=5-i)]
    Ds={};Es={}
    def coefs(ledger,name,f,rhs=0):
        ledger[name]=([f(b,r,z) for b,r,z in types],rhs)
    coefs(Es,'chosen',lambda b,r,z: int(r==1),1)
    if k:coefs(Es,'old',lambda b,r,z: int(r==3),k)
    if k<5:
        for bb in range(i-k+1):
            coefs(Es,('balance',bb),lambda b,r,z:(b==bb)*((5-k)*(r==1)-(r==2)))
    coefs(Ds,'old_capacity',lambda b,r,z:b,i-k)
    def prefix(j,b,r,z):return b+(r==3)+sum(z[:j-i])
    def pay(j,b,r,z):
        if z[j-i]==0:return 0
        return 1/(b+(r==3)+sum(z))
    for j in range(i+1,6):
        coefs(Ds,('size',j),lambda b,r,z:z[j-i],1)
        coefs(Ds,('floor_1',j),lambda b,r,z:-pay(j,b,r,z),-floors[j,k+1])
    queries={'chosen':(lambda r,z:r==1,1)}
    if k:queries['marked']=(lambda r,z:r==3,k)
    if k<5:queries['remaining']=(lambda r,z:r==2,5-k)
    queries['unmarked']=(lambda r,z:r in (1,2),6-k)
    queries['all']=(lambda r,z:r!=0,6)
    for qj in range(i+1,6):queries[f'leaf{qj}']=(lambda r,z,j=qj:z[j-i],1)
    for j in range(i+1,6):
        for name,(f,s) in queries.items():
            coefs(Ds,('true',j,name),lambda b,r,z:f(r,z)/(s*(prefix(j,b,r,z)+6-j))-pay(j,b,r,z))
    if i<4:
        for name,(f,s) in queries.items():
            def R(b,r,z,f=f,s=s):
                p=prefix(4,b,r,z)
                return f(r,z)/(p+1)-f(r,z)*z[4-i]*(p==0)/4-s*pay(4,b,r,z)-pay(5,b,r,z)/2
            coefs(Ds,('R',name),R)
            for name2,(f2,s2) in queries.items():
                def pair(b,r,z,f=f,s=s,f2=f2,s2=s2,same=name==name2):
                    p=prefix(4,b,r,z); a=f(r,z)/s;aa=f2(r,z)/s2
                    # for repeated query, distinct indices if feasible; otherwise two independent queries.
                    g=0 if (same and s>=2) else a*aa
                    return (a+aa)/(p+1)-(g+z[4-i])/((p+1)*(p+2))-pay(4,b,r,z)-pay(5,b,r,z)
                coefs(Ds,('pair',name,name2),pair)
    A,rhs=zip(*Ds.values());E,y=zip(*Es.values())
    x=linprog([pay(i,b,r,z) for b,r,z in types],A_ub=A,b_ub=rhs,A_eq=E,b_eq=y,bounds=(0,None),method='highs');assert x.success,x.message
    return x.fun

if __name__=='__main__':
    g={}
    for i in reversed(range(6)):
        for k in range(i+1):
            g[i,k]=solve(i,k,g)
        print(i+1,[g[i,k] for k in range(i+1)])
    print('sum arbitrary-history floors',sum(g[i,0] for i in range(6)))
