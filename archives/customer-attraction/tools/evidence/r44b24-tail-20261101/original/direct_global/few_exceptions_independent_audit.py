"""Independent exact review audit; no imports of discovery audit or solver."""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json,platform

def calculate(m,r,a,b,p,e,d,l):
 n=p+a+b
 alpha=F(a,n) if a else F(0)
 beta=F(b,n) if b else F(0)
 uE=F(e,n) if e else F(0)
 queryE=F(e,p+a+1)
 K=uE-F(r*a,m)+(r*beta-queryE)/F(m-1)
 G=m*alpha+beta/2-F(d,p+1)-F(l,2*m*(p+a+1))+F(d*l,m*(p+1)*(p+2))
 Q0=2*int(n>0)-int(d>0)-G
 D=m*(m*m-3*m+3)-r*(m*m-2*m+2)
 mu=F(m*(m-1)**2,D)
 return Q0-mu*K,Q0,K,mu

corner_count=0;identity_count=0;parameter_count=0
for m in [*range(5,81),101,257,1001]:
 for r in range(1,isqrt(m-1)):
  assert m>=(r+1)**2+1
  D=m*(m*m-3*m+3)-r*(m*m-2*m+2)
  mu=F(m*(m-1)**2,D)
  U0=F((m-1)*(r+2),(m-2)*r+m-1)
  assert 0<mu<=U0 and mu>=F(m,m-1-r)
  P=m**3-(r*r+2*r+4)*m*m+(2*r*r+5*r+5)*m-2*r*r-4*r
  q=r+1;s=m-q*q-1
  assert P==s**3+2*q*q*s*s+(q**4+q-1)*s+q*(q-1)**2+2>0
  parameter_count+=1
  corners=((0,0),(0,m),(1,0),(1,m),(m,0),(m,m))
  A0=m*(m-1)**2-r*(m*m-m+1);B0=m*(m-2)-r*(m-1)
  assert A0-r*B0==(m-1)*(m-1-r)*(m-r)>0
  for t in range(r+1):
   p=m-2-t;e=r-t
   for b in (0,1):
    for d,l in corners:
     Q,Q0,K,_=calculate(m,r,1,b,p,e,d,l)
     assert Q>=0,(m,r,t,b,d,l,Q)
     if not b:
      c=m-1-t
      assert K==F(-t*(A0-t*B0),m*(m-1)*c*(c+1))
     else:
      c=m-t
      assert K==F(-t*B0,m*(m-1)*c)
     corner_count+=1;identity_count+=1
  # For larger m take endpoint/adjacent backgrounds; analytic review handles all p.
  pvals=range(m-1) if m<=101 else sorted({0,1,r-1,r,r+1,m-3,m-2})
  for p in pvals:
   if p<0:continue
   for e in range(min(r,p)+1):
    for b in (0,1):
     for d,l in corners:
      Q,Q0,K,_=calculate(m,r,0,b,p,e,d,l)
      assert Q>=0,(m,r,p,e,b,d,l,Q)
      if b:
       assert K==F(e*(m-2)+r,(m-1)*(p+1))
      elif p:
       assert K==F(e*((m-2)*p+m-1),(m-1)*p*(p+1))
      else:assert K==0
      corner_count+=1;identity_count+=1
report={'status':'all independent exact checks passed','parameter_pairs':parameter_count,'corner_checks':corner_count,'raw_K_factor_checks':identity_count,'scope':'finite formula audit; all-parameter proof in few_exceptions_independent_review.md','python':platform.python_version()}
print(json.dumps(report,ensure_ascii=False,indent=2))
Path(__file__).with_suffix('.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
