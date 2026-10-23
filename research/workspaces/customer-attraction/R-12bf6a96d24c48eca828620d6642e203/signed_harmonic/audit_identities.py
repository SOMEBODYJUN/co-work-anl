"""Exact arithmetic checks of identities only, not the open budget."""
from fractions import Fraction as Q
from itertools import product,combinations
from pathlib import Path
import json
H=[Q(0)]
for i in range(1,41):H.append(H[-1]+Q(1,i))
n=0
for m in range(1,20):
 for c in range(m+1):
  for d in range(m+1):
   F=H[c+d]-H[c]
   assert F<=Q(d,c+1)
   if c:
    assert c*((H[c-1+d]-H[c-1])-F)==Q(d,c+d)
   for b in range(min(c,1)+1):
    R=Q(d,c+1-b)-F
    assert R>=0
    if d==1:
     assert R==(Q(1,c*(c+1)) if b else 0)
   n+=1
# Exchange formula for arbitrary sets in a 5-customer universe, supports 1..3.
U=set(range(5));sets=[set(i for i in U if mask>>i&1) for mask in range(32)]
ex=0
for Sidx in combinations(range(32),2):
 S=[sets[i] for i in Sidx];O=S[0]|S[1]
 for ti in range(2):
  other=S[1-ti];T=S[ti];P=T-other
  for Xidx,X in enumerate(sets):
   if Xidx==Sidx[1-ti]:continue
   D=P-X;G=X-O;Op=other|X
   assert Op==(O-D)|G
   for A in (set(),U,{0,2,4}):
    assert len(Op)-len(O)==len(G)-len(D)
    assert len(A&Op)-len(A&O)==len(A&G)-len(A&D)
    ex+=1
out={'arithmetic_cases':n,'exchange_cases':ex,'status':'passed','scope':'identities only; signed budgets remain open'}
print(json.dumps(out));(Path(__file__).parent/'identity_audit.json').write_text(json.dumps(out,indent=2)+'\n')
