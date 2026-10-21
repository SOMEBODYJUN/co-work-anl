"""Exact certificate for all customer-specific nonnegative backgrounds.
This imports neither discovery code nor an SPE solver. All source multipliers
are reconstructed as the integers0/1 and probability1/2 from the saved output.
"""
from fractions import Fraction as F
from pathlib import Path
import json
P=Path(__file__).resolve().parent
src=json.loads((P/'group3_background_Q.json').read_text())
def sigma(h):
 if not h:return 0
 if len(h)==1:return 3 if h[0]<3 else 0
 return next(a for a in (range(3) if h[1]<3 else range(3,6)) if a not in h)
def end(h):
 while len(h)<3:h=h+(sigma(h),)
 return h
# Numerators after multiplying by positive D(b)=(b+1)(b+2)(b+3), ascending powers.
poly={1:(6,5,1),2:(3,4,1),3:(2,3,1)}
def term(a,z,mask):
 return poly[sum(bool(mask&(1<<b)) for b in z)] if mask&(1<<a) else (0,0,0)
def add(v,w,scale=1):return tuple(x+scale*y for x,y in zip(v,w))
Q=[(tuple(r['B']),F(r['p']).limit_denominator(2)) for r in src['Q']]
lam=[(r['a'],tuple(r['h']),r['b'],F(r['value']).limit_denominator(1)) for r in src['lambda']]
assert Q==[((0,1),F(1,2)),((0,2),F(1,2))]
assert all(v==1 for a,h,b,v in lam)
root=end(())
remainders=[];all_zero=[]
for a in range(6):
 az=True
 for mask in range(1,64):
  remainder=add(term(root[0],root,mask),term(root[1],root,mask))
  for B,p in Q:remainder=add(remainder,term(a,B+(a,),mask),-2*p)
  for aa,h,b,value in lam:
   if a==aa:
    remainder=add(remainder,term(sigma(h),end(h),mask),-value)
    remainder=add(remainder,term(b,end(h+(b,)),mask),value)
  assert min(remainder)>=0,(a,mask,remainder)
  az=az and not any(remainder)
  remainders.append({'a':a,'mask':mask,'coefficients':list(map(str,remainder))})
 if az:all_zero.append(a)
report={'scope':'Fixed six-label, three-player complete opposite-group strategy; arbitrary nonnegative customer-specific background loads; nonnegative customer masses; every historical SPE incentive required','root':root,'Q':[{'B':list(B),'p':str(v)} for B,v in Q],'lambda':[{'a':a,'h':list(h),'b':b,'value':str(v)} for a,h,b,v in lam],'residual_denominator':'(b+1)(b+2)(b+3)>0 for all b>=0','checked_polynomial_coefficients':len(remainders)*3,'exact_identity_queries':all_zero,'nonnegative_coefficients_verified':True,'remainders':remainders}
(P/'group3_background_exact_certificate.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('lambda','remainders')},indent=2))
