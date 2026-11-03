"""Independent controller reconstruction for the peer's all-m insurance family.
No source verifier or strategy implementation is imported.
"""
from itertools import product
from functools import lru_cache
from fractions import Fraction as F
from pathlib import Path
import json

def run(m,full):
 topics=list(product(range(m),range(m-1)))
 def prescribed(h):
  if not h:return (0,0)
  anchor=h[0];mode='BASE';target=None
  ae={anchor[0]};bb={anchor[1]}
  for j,observed in enumerate(h[1:],1):
   fresh_a=min(set(range(m))-ae)
   if mode=='BASE':
    expected=(fresh_a,anchor[1]) if j==m-1 else (anchor[0],min(set(range(m-1))-bb))
    if observed!=expected and j<m-1:
     if observed[1] in bb:mode='EXIT'
     else:mode='PUNISH';target=observed[1]
   elif mode=='PUNISH':
    if observed[1] in bb:mode='EXIT'
   ae.add(observed[0]);bb.add(observed[1])
  j=len(h);a=min(set(range(m))-ae)
  if mode=='BASE':return (a,anchor[1]) if j==m-1 else (anchor[0],min(set(range(m-1))-bb))
  if mode=='EXIT':return (a,min(set(range(m-1))-bb))
  return (a,target) if j==m-1 else (a,min(set(range(m-1))-bb))
 @lru_cache(None)
 def end(h):
  return h if len(h)==m else end(h+(prescribed(h),))
 def utility(z,i):
  a,b=z[i]
  return F(1,sum(x==a for x,y in z))+F(2,sum(y==b for x,y in z))
 def unit_utility(z,i):
  a,b=z[i];clients=[('e',a)]+[('b',b,s) for s in range(2)]
  return sum((F(1,sum(x==c[1] if c[0]=='e' else y==c[1] for x,y in z)) for c in clients),F())
 checks=0
 if full:
  for n in range(m):
   for h in product(topics,repeat=n):
    v=utility(end(h),n)
    assert v==unit_utility(end(h),n)
    for t in topics:
     assert v>=utility(end(h+(t,)),n);checks+=1
 z=end(())
 W=len({a for a,b in z})+2*len({b for a,b in z})
 opt_path=tuple((a,a%(m-1)) for a in range(m))
 OPT=len({a for a,b in opt_path})+2*len({b for a,b in opt_path})
 assert OPT==3*m-2 and W==2*m
 u=utility(z,0);extra=F(1,2)+F(2*(m-1),2*m-1)
 assert u==1+F(1,m-1)
 assert extra-u==F(2*m*m-9*m+5,2*(2*m-1)*(m-1))
 if m>=4:assert extra>u
 if m>=5:assert OPT>2*m*u
 return {'m':m,'complete_history_IC_checks':checks,'all_histories_checked':full,
 'actual':z,'u1':str(u),'W':W,'OPT':OPT,'extra_fractional_value':str(extra),
 'net_floor_reserve':str(W+m*u-OPT),
 'individual_OPT_floor_gap':str(F(OPT,2*m)-u)}
rows=[run(3,True),run(4,True),run(5,False)]
# Exact positivity ranges by elementary factorization, not finite search.
assert all(2*m*m-9*m+5==1+(m-4)*(2*m-1) for m in range(4,20))
assert all(m*m-5*m+2==2+m*(m-5) for m in range(5,20))
out={'scope':'Independent finite controller replay plus analytic-formula arithmetic; all-m proof inherited/reconstructed from peer source.',
 'source':'R-d3981c0168644971803a9c3380ed687c/round5_general/security/global_extra_individual_counterfamily.md','rows':rows}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
