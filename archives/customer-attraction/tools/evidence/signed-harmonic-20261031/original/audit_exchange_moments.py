from fractions import Fraction as Q
from math import comb
from itertools import combinations,product
from pathlib import Path
import json

def C(n,k):return comb(n,k) if 0<=k<=n else 0
H=[Q(0)]
for i in range(1,31):H.append(H[-1]+Q(1,i))
count=0
for m in range(1,26):
 for c in range(m+1):
  qq=[Q(C(m-c,r),C(m,r)) for r in range(m+1)]
  if c:
   assert sum((1-qq[r])/r for r in range(1,m+1))==H[c]
   assert sum((1-qq[r])/Q(m-r) for r in range(m))==H[m]-Q(1,c)
  for d in range(1,m+1):
   pp=[Q(C(r,d),C(m,d)) for r in range(m+1)]
   k=sum(pp[r]*qq[r]/r for r in range(1,m+1))
   assert k==Q(C(m,c+d),d*C(m,c)*C(m,d))
   if c:
    rev=sum(pp[r]*qq[r]/Q(m-r) for r in range(m))
    assert rev==Q(C(m,c+d),c*C(m,c)*C(m,d))
   else:
    assert k==Q(1,d)
    assert sum(pp[r]/Q(m-r) for r in range(m))==H[m]-H[d]
   count+=1
# Independent subset probability reconstruction for all c,d at m<=7.
prob=0
for m in range(1,8):
 for r in range(m+1):
  sels=list(combinations(range(m),r))
  for c,d in product(range(m+1),repeat=2):
   miss_actual=sum(not(set(s)&set(range(c))) for s in sels)
   remove_opt=sum(set(range(d))<=set(s) for s in sels)
   assert Q(miss_actual,len(sels))==Q(C(m-c,r),C(m,r))
   assert Q(remove_opt,len(sels))==Q(C(r,d),C(m,d))
   prob+=1
out=dict(status='passed',coefficient_cases=count,subset_probability_cases=prob,scope='exchange coefficient identities; no SPE welfare conclusion')
print(json.dumps(out));(Path(__file__).parent/'exchange_moment_audit.json').write_text(json.dumps(out,indent=2)+'\n')
