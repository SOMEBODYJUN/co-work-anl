"""Independent exact arithmetic review of NP21--NP25, without author imports."""
from fractions import Fraction as F
from pathlib import Path
import argparse,json
parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path)
args=parser.parse_args()
private_checks=shared_checks=monotone_checks=0
for n in range(2,501):
 delta=F(2*(n-1),n*(n+2)*(n+5))
 nxt=F(2*n,(n+1)*(n+3)*(n+6))
 denom=n*(n+2)*(n+5)*(n+1)*(n+3)*(n+6)
 num=2*(2*n**3+7*n*n-9*n-18)
 assert (delta-nxt)*denom==num==2*(n-2)*(2*n*n+11*n+13)+16>0
 monotone_checks+=1
for n in range(5,501):
 raw=[]
 for t in range(n-1):
  a=F(n+t,2*(t+1)*(3*n-2*t))
  poly=n*(n+t)-(t+1)*(3*n-2*t)
  assert poly==2*(F(t)-F(n-1,2))**2+F(n*n-4*n-1,2)>=0
  assert a>=F(1,2*n)
  raw.append(a);private_checks+=1
 raw.append(F(1,n+5));assert raw[-1]>=F(1,2*n)
 suffix=None;envelope=F()
 for a in reversed(raw):
  suffix=a if suffix is None else min(suffix,a);envelope+=suffix
 assert envelope>=F(1,2)
 B=[F(1,3*n-2*t) for t in range(n-1)]+[F(n+1,n*(n+5))]
 assert all(a<=b for a,b in zip(B,B[1:]))
 H=sum((F(1,n+2*r) for r in range(1,n+1)),F())
 delta=F(2*(n-1),n*(n+2)*(n+5))
 assert sum(B,F())==H-delta
 for s in range(1,7):
  for t in (0,n//2,n-2):
   actualA=F(n+t,2*(t+1))/(F(t)+F(s*(n-t),2))
   actualB=1/(F(t)+F(s*(n-t),2))
   assert actualA>=raw[t] and actualB>=B[t]
  assert F(1,n+s-1)>=raw[-1]
  assert F(n+1,n*(n+s-1))>=B[-1]
 shared_checks+=1
log=F(1)+F(1,12)+F(1,80)+F(1,448)
assert log==F(7379,6720)
lo=log/2-F(1,27)-F(16,9*11*14)
assert lo==F(665881,1330560)==F(1,2)+F(601,1330560)>F(1,2)
B9=sum((F(1,9+2*r) for r in range(2,10)),F())+F(10,9*14)
assert B9==F(229324183,456326325)>F(1,2)
result={'status':'independent exact NP21-NP25 checks passed','private_pointwise_checks':private_checks,'shared_identity_cases':shared_checks,'delta_difference_cases':monotone_checks,'s1_through_s6_denominator_comparisons':'passed','log3_lower':str(log),'shared_uniform_n9_lower':str(lo),'half_gap':str(lo-F(1,2)),'exact_B9':str(B9),'scope':'Arithmetic audit corroborates universal polynomial, monotonicity and trapezoid proofs; finite n2 through500 checks do not replace universal proof.'}
if args.output:
 args.output.parent.mkdir(parents=True,exist_ok=True)
 with args.output.open('x') as dest:dest.write(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
