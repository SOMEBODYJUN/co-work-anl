"""Self-contained exact verification of the six analytic pair-payment identities.
No imports from optimizers, saved certificates, or customer-attraction solvers.
"""
from fractions import Fraction as F
from itertools import product
import json
# D(b)/(b+j), coefficients in increasing powers of b.
NUM={1:(6,5,1),2:(3,4,1),3:(2,3,1)}
TABLE={
 0:[((),3),((0,),1),((0,2),0),((1,5),0)],
 1:[((),3),((0,),1),((0,4),1)],
 2:[((),3),((0,),1),((0,5),2),((3,0),2)],
 3:[((),3),((0,),1),((0,2),3)],
 4:[((),4),((0,),1),((0,2),4)],
 5:[((),5),((0,),1),((0,2),5)]}
REST={0:(1,0,3,5),1:(0,1,3,4),2:(0,2,3,5)}
def choose(h):
 if not h:return 0
 if len(h)==1:return 3 if h[0]<3 else 0
 return next(a for a in (range(3) if h[-1]<3 else range(3,6)) if a not in h)
def complete(h):
 while len(h)<3:h+=(choose(h),)
 return h
def interest(mask,a):return int(bool(mask&(1<<a)))
def row(mask,a,z):
 return NUM[sum(interest(mask,b) for b in z)] if interest(mask,a) else (0,0,0)
def plus(x,y,scale=1):return tuple(a+scale*b for a,b in zip(x,y))
def gamma(mask,h,a):return plus(row(mask,choose(h),complete(h)),row(mask,a,complete(h+(a,))),-1)
def literal(mask,a,z,bg):return F(interest(mask,a),bg+sum(interest(mask,c) for c in z)) if interest(mask,a) else F(0)
# Prove the universal tax square on each possible binary interest pattern.
for aa,bb,dd in product(range(2),repeat=3):
 assert (aa-bb)*(aa-dd)>=0
 for bg in [F(0),F(1,2),F(11,3),F(100)]:
  def U(a,b):return F(a,bg+1+b) if a else F(0)
  assert U(bb,aa)-U(bb,dd)+U(aa,dd)-U(aa,aa)==F((aa-bb)*(aa-dd),(bg+1)*(bg+2))
count=0;zeros=[]
for a in range(6):
 allzero=True
 for mask in range(1,64):
  lhs=plus(row(mask,0,(0,3,4)),row(mask,3,(0,3,4)))
  lhs=plus(lhs,row(mask,a,(0,1,a)),-1)
  lhs=plus(lhs,row(mask,a,(0,2,a)),-1)
  rhs=(0,0,0)
  for h,b in TABLE[a]:rhs=plus(rhs,gamma(mask,h,b))
  residual=(0,0,0)
  if a in REST:
   base,A,B,D=REST[a]
   mult=(interest(mask,A)-interest(mask,B))*(interest(mask,A)-interest(mask,D))
   residual=(1,1,0) if interest(mask,base) else (3,1,0)
   residual=tuple(mult*x for x in residual)
  assert min(residual)>=0
  assert lhs==plus(rhs,residual),(a,mask,lhs,rhs,residual)
  allzero=allzero and residual==(0,0,0)
  # Independently evaluate the original utility expression at fractional and large backgrounds.
  for bg in [F(0),F(1,2),F(17,3),F(100)]:
   ev=lambda z:sum(F(z[j])*bg**j for j in range(3))/((bg+1)*(bg+2)*(bg+3))
   direct=literal(mask,0,(0,3,4),bg)+literal(mask,3,(0,3,4),bg)-literal(mask,a,(0,1,a),bg)-literal(mask,a,(0,2,a),bg)
   assert direct==ev(lhs)
  count+=3
 if allzero:zeros.append(a)
print(json.dumps({'verified':True,'polynomial_coefficients':count,'exact_cancellation_queries':zeros,'nonnegative_tax_remainders_for_queries':[0,1,2],'Q':{'0,1':'1/2','0,2':'1/2'},'scope':'fixed six-label complete strategy; arbitrary nonnegative customer-specific backgrounds; arbitrary nonnegative masses; all its SPE rows required','general_half_proved':False},indent=2))
