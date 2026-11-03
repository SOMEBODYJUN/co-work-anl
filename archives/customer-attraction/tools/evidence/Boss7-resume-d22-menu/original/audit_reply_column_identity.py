"""Definition-level Fraction audits; finite checks supplement algebra, not universality."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
checks=0
for t in range(12):
 for a,b,ra,rb in product((0,1),repeat=4):
  f=lambda c:F(c,t+1)
  g=F(1,(t+1)*(t+2));h=F(2,(t+1)*(t+2)*(t+3))
  D=F(a,t+1+ra)
  K=F(a,t+1+b+rb)
  slack=F(ra-rb,t+1+a)
  lhs=D+f(ra)-f(rb)-K
  rhs=slack+a*b*(g-h*rb)
  assert lhs==rhs
  assert g-h*rb>=F(1,(t+2)*(t+3))>0
  checks+=1
# Universal potential identity uses arbitrary valid loads of the r-1 tail.
general=0
for t in range(7):
 def Hload(d):return sum((F(1,t+j) for j in range(1,d+1)),F(0))
 for r in range(1,9):
  for a,b in product((0,1),repeat=2):
   for ya,yb in product(range(r),repeat=2):
    D=F(a,t+1+ya)
    K=F(a,t+1+b+yb)
    Fa,Fb=Hload(ya),Hload(yb)
    R=Hload(a+yb)-Hload(a+ya)
    delta=F(a*b,(t+1+yb)*(t+2+yb))
    assert K==D+Fa-Fb+R-delta
    general+=1
report={'two_player_membership_identity_checks':checks,'general_potential_identity_checks':general,'all_exact_checks_passed':True,'scope':'Finite definition-level checks supplement self-contained algebra; no assertion that r>=3 joint-potential regret is nonpositive.'}
(HERE/'reply_column_identity_audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
