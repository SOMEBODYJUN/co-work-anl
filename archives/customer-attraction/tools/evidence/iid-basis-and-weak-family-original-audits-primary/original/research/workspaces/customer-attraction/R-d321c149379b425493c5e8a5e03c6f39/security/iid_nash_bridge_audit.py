"""Exact independent unit-customer and Q(sqrt(669)) audit; stdlib only."""
from fractions import Fraction as F
from itertools import product
from math import sqrt

D=669
class K:
    def __init__(self,a=0,b=0): self.a,self.b=F(a),F(b)
    def __add__(self,other):
        other=other if isinstance(other,K) else K(other)
        return K(self.a+other.a,self.b+other.b)
    __radd__=__add__
    def __neg__(self):return K(-self.a,-self.b)
    def __sub__(self,o):return self+-asK(o)
    def __rsub__(self,o):return asK(o)+-self
    def __mul__(self,o):
        o=asK(o);return K(self.a*o.a+D*self.b*o.b,self.a*o.b+self.b*o.a)
    __rmul__=__mul__
    def __truediv__(self,o):
        o=asK(o);den=o.a*o.a-D*o.b*o.b
        return self*K(o.a/den,-o.b/den)
    def __eq__(self,o):o=asK(o);return self.a==o.a and self.b==o.b
    def sign(self):
        if not self.b:return (self.a>0)-(self.a<0)
        if not self.a:return (self.b>0)-(self.b<0)
        if self.a>0 and self.b>0:return 1
        if self.a<0 and self.b<0:return -1
        gap=self.a*self.a-D*self.b*self.b
        return ((gap>0)-(gap<0)) * (1 if self.a>0 else -1)
    def __repr__(self):return f'({self.a})+({self.b})sqrt({D})'
    def approximate(self):return float(self.a)+float(self.b)*sqrt(D)
def asK(x):return x if isinstance(x,K) else K(x)

# Eight separate, named unit customers.
S=({0,1},{2,3,4,5},{0,1,6},{0,1,7})
last=((1,1,1,1),(1,2,3,2),(1,3,1,1),(1,2,1,1))
def action(h):return 0 if not h else 1 if len(h)==1 else last[h[0]][h[1]]
def continuation(h):
    while len(h)<3:h=h+(action(h),)
    return h
def utilities(z):
    return tuple(sum((F(1,sum(x in S[a] for a in z)) for x in S[ai]),F(0)) for ai in z)
def welfare(z):return len(set().union(*(S[a] for a in z)))
comparisons=0
for depth in range(3):
    for h in product(range(4),repeat=depth):
        actual=utilities(continuation(h))[depth]
        for a in range(4):
            assert actual>=utilities(continuation(h+(a,)))[depth]
            comparisons+=1
assert continuation(())==(0,1,1)
assert utilities(continuation(()))==(2,2,2)
assert welfare(continuation(()))==6

r=K(F(30,7),F(-1,7));q=(K(0),r,(1-r)/2,(1-r)/2)
assert sum(q)==1 and all(x.sign()>=0 for x in q)
assert 7*r*r-60*r+33==0
expected_W=K(0);expected_u=[K(0)]*3;dev=[[K(0) for _ in range(4)]for _ in range(3)]
for z in product(range(4),repeat=3):
    probability=q[z[0]]*q[z[1]]*q[z[2]]
    expected_W+=probability*welfare(z)
    for i in range(3):
        expected_u[i]+=probability*utilities(z)[i]
        for a in range(4):
            zz=z[:i]+(a,)+z[i+1:]
            dev[i][a]+=probability*utilities(zz)[i]
Z=K(F(4344,49),F(-156,49))
assert expected_W==Z and expected_W==sum(expected_u)
for i in range(3):
    for a in range(4):assert (expected_u[i]-dev[i][a]).sign()>=0
assert (Z-6).sign()>0
assert (r-F(15,26)).sign()>0
print({'histories':21,'SPE_comparisons':comparisons,'iid_profiles':64,'q':list(map(repr,q)),
       'Z':repr(Z),'Z_approx':Z.approximate(),'Z_minus_SPE':repr(Z-6),
       'static_Nash_and_CCE':True,'genuine_security_bridge':'not refuted'})
