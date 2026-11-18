"""Six optimal disjoint maximum labels. Relaxation for true forced paths with suffix floors."""
from fractions import Fraction
from itertools import product
import numpy as np
from scipy.optimize import linprog

def solve(i, floors):
    # i=0..5 forced optimal action after i arbitrary labels. averaged over the 6 identities.
    types=[]
    for b in range(i+1):
        for region in (0,1,2): # 0 outside O, 1 selected optimal label, 2 other five
            for tail in product((0,1),repeat=5-i):
                types.append((b,region,(int(region==1),)+tail))
    equality={'chosen':([],1)}
    for b in range(i+1):equality[('common',b)]=([],0)
    inequality={'prefix':([],i)}
    for j in range(i+1,6):inequality[('size',j)]=([],1);inequality[('floor',j)]=([],-floors[j])
    obj=[]
    for b,r,z in types:
        member=r!=0;other=r==2; c=sum(z)+b
        def pay(j):return z[j-i]/c if z[j-i] else 0
        equality['chosen'][0].append(r==1)
        for b0 in range(i+1):equality[('common',b0)][0].append((b==b0)*(5*(r==1)-other))
        inequality['prefix'][0].append(b)
        for j in range(i+1,6):
            inequality[('size',j)][0].append(z[j-i])
            inequality[('floor',j)][0].append(-pay(j))
        obj.append(pay(i))
    def row(n,func,rhs=0):
        inequality[n]=([func(b,r,z) for b,r,z in types],rhs)
    def query(r,z,name):
        if name=='chosen':return int(r==1)
        if name=='other':return (r==2)/5
        if name=='all':return (r!=0)/6
        return z[name-i]
    def share(b,z,j):return z[j-i]/(sum(z)+b) if z[j-i] else 0
    queries=['chosen','other','all']+list(range(i+1,6))
    for j in range(i+1,6):
        for q in queries:
            row(('safe',j,q),lambda b,r,z:query(r,z,q)/(b+sum(z[:j-i])+6-j)-share(b,z,j))
    if i<4:
        def pair(b,r,z,q1,q2):
            p=b+sum(z[:4-i]);a=query(r,z,q1);a2=query(r,z,q2)
            inter=(0 if q1==q2 and q1 in ('other','all') else a*a2)
            return (a+a2)/(p+1)-(inter+z[4-i])/((p+1)*(p+2))-share(b,z,4)-share(b,z,5)
        for q1 in queries:
            for q2 in queries:
                row(('pair',q1,q2),lambda b,r,z:pair(b,r,z,q1,q2))
        for group,tau in [('other',5),('all',6),('chosen',1)]:
            def R(b,r,z,group,tau):
                p=b+sum(z[:4-i]);a=z[4-i];u=query(r,z,group)*tau
                return u/(p+1)-(u*a*(p==0))/4-tau*share(b,z,4)-share(b,z,5)/2
            row(('R',group),lambda b,r,z:R(b,r,z,group,tau))
    A,bb=zip(*inequality.values());E,ee=zip(*equality.values())
    res=linprog(obj,A_ub=A,b_ub=bb,A_eq=E,b_eq=ee,bounds=(0,None),method='highs')
    assert res.success,res.message
    print('i,g',i+1,res.fun,'binding',[(k,round(y,4)) for k,y in zip(inequality,res.ineqlin.marginals) if abs(y)>1e-7])
    return res.fun

if __name__=='__main__':
    floors=[0.0]*6
    for i in reversed(range(6)):floors[i]=solve(i,floors)
    print('sum',sum(floors))
