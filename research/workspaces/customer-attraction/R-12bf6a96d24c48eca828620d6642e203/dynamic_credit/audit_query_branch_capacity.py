#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
import json
count=0
for r in range(1,18):
 for b in range(14):
  for k in range(r):
   d=F(k*(r-b-2-k),(b+1)*(b+1+k))
   assert F(r-1-k,b+1)==F(r-1,b+1+k)+d
   assert (d>0)==(1<=k<=r-b-3)
   if r<=3:assert d<=0
   count+=1
for b in range(14):
 for k in range(18):
  lhs=F(k,b+1)-(F(k,b+k) if k else F())
  rhs=F(k*(k-1),(b+1)*(b+k)) if k else F()
  assert lhs==rhs and rhs>=0
  count+=1
report={'status':'exact scalar algebra checks passed','checks':count,'scope':'finite audit of implementation; universal identity follows from displayed algebra','independent_review':'root and direct_cover independently reconstructed all-client identity; no general SPE relay claimed'}
print(json.dumps(report,indent=2))
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
