"""One marked anchor, three other disjoint fresh maximum anchors, three actual successors.
No catalogue bound. LP rows include fresh query on the actual distinct-prefix leaf.
"""
from itertools import product
from scipy.optimize import linprog
from fractions import Fraction as Q

def share(a,n):return Q(a,n) if a else Q()
def model():
    # Locations are old T, two other prior anchors, three free anchors, outside all.
    C=[(r,ww) for r in range(4) for ww in product(range(2),repeat=3)]
    D={};E={}
    def row(name,func,bound=0,eq=False):
        (E if eq else D)[name]=([func(r,ww) for r,ww in C],Q(bound))
    for i,size in enumerate([1,2,3]):row(('size',i),lambda r,w:r==i,size,True)
    past=lambda r:int(r<2)
    obj=[share(r==0,past(r)+sum(w)) for r,w in C]
    u=lambda i,r,w:share(w[i],past(r)+sum(w))
    for i in range(3):row(('capacity',i),lambda r,w:w[i],1)
    row('first-floor',lambda r,w: -u(0,r,w),-Q(3,4))
    for i in range(3):
        for j in range(3):
            row(('safe-actual',i,j),lambda r,w:share(w[j],past(r)+sum(w[:i])+3-i)-u(i,r,w))
        for rr,n in enumerate([1,2,3]):
            row(('safe-anchor',i,rr),lambda r,w:share(r==rr,n*(past(r)+sum(w[:i])+3-i))-u(i,r,w))
    # From any true penultimate source choose one of the 3 still-free comparison anchors,
    # exploit same-last-reply deficit and use another of the same three anchors at its last seat.
    for ti in range(0,61):
        t=Q(ti,60)
        def penu(r,w):
            p=past(r)+w[0];h=min(Q(1,p+1),Q(1-t,p+2)+t)
            return (r==2)*(h+t/(p+1))/3-u(1,r,w)
        row(('penu',ti),penu,t)
    # Strong pair with two different choices among the free anchors.
    def pair(r,w):
        p=past(r)+w[0];return 2*Q(r==2,3*(1+p))-Q(w[1],(p+1)*(p+2))-u(1,r,w)-u(2,r,w)
    row('pair',pair)
    A,b=zip(*D.values());Aeq,beq=zip(*E.values())
    res=linprog(obj,A_ub=A,b_ub=b,A_eq=Aeq,b_eq=beq,bounds=(0,None),method='highs');assert res.success,res.message
    print('floor',res.fun, Q(res.fun).limit_denominator(100000),'nonzero weights',[(k,Q(-v).limit_denominator(100000)) for k,v in zip(D,res.ineqlin.marginals) if abs(v)>1e-7]);print('atoms',[(r,w,str(Q(v).limit_denominator(100000))) for (r,w),v in zip(C,res.x) if v>1e-7]);print('equal',[(k,Q(v).limit_denominator(100000)) for k,v in zip(E,res.eqlin.marginals) if abs(v)>1e-7]);return res
if __name__=='__main__':model()
