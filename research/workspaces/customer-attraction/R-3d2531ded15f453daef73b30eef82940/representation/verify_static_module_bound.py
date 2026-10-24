"""Independent definition-level exact check of the 34-customer affine bound.
No customer_attraction solver/verifier imports. Static certificate only.
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

TYPES={4:1,27:4,29:3,30:3,31:2,32:1,43:3,45:3,46:3,51:3,53:3,54:3,59:2}
P=tuple(F(x,82) for x in (10,10,21,10,10,21))
C=F(2411,246);B=F(587,246)
EXPECTED=(F(901,41),F(2369,164),C,F(304,41),F(2999,492),F(8451,1640),F(5473,1230))
def compositions(t,k=6):
 if k==1:
  yield (t,);return
 for a in range(t+1):
  for tail in compositions(t-a,k-1):yield (a,)+tail

def value(q):
 return sum((r*sum((P[a] for a in range(6) if mask>>a&1),F())/sum([1]+[q[a] for a in range(6) if mask>>a&1]) for mask,r in TYPES.items()),F())

records=[];total=0
for t,expected in enumerate(EXPECTED):
 values=[(value(q),q) for q in compositions(t)]
 actual=min(v for v,q in values)
 assert actual==expected,(t,actual,expected)
 assert all(v>=C-B*(t-2) for v,q in values)
 minimizers=[q for v,q in values if v==actual]
 records.append({'t':t,'count':len(values),'minimum':str(actual),'affine_lower_bound':str(C-B*(t-2)),'minimizers':minimizers})
 total+=len(values)
assert total==924
assert C-B*5<0
# For all t>=7 RHS is nonpositive and true query values are nonnegative.
# For n modules and 2n+1 background slots:
# (1/n) sum_j [C-B(t_j-2)] = C-B/n.
assert C-B/F(18)>F(29,3)
assert C-B/F(17)<F(29,3)
report={'kind':'static_only_exact_definition_check','base_customers':sum(TYPES.values()),'p':[str(x) for x in P],'affine_C':str(C),'affine_B':str(B),'total_counts':total,'records':records,'n18_lower':str(C-B/F(18)),'root_comparison':str(F(29,3)),'difference_n18':str(C-B/F(18)-F(29,3)),'warning':'No SPE realization or extra-slot-menu counterexample is asserted.'}
path=Path(__file__).with_name('static_module_exact_report.json')
path.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))

# Independently verify the shorter Cauchy + 21-orbit certificate.
a={mask:r*sum((P[j] for j in range(6) if mask>>j&1),F()) for mask,r in TYPES.items()}
A=sum(a.values(),F())
S=tuple(sum((v for mask,v in a.items() if mask>>j&1),F()) for j in range(6))
assert A==F(901,41)
assert S==tuple(F(x,82) for x in (1235,1235,1193,1235,1235,1193))
assert 3*1802**2-3585*1802==3281442
assert 587*1802-3585*1235==-3369701
assert 587*1235==724945
assert 724945-3369701+3281442==636686
assert 8*724945-3369701==2429859
assert 16*724945-4*3369701+3281442==1401758
perms=[]
for sx,sy,sg in product((0,1),repeat=3):
 perm=list(range(6))
 if sx:perm[0],perm[1]=perm[1],perm[0]
 if sy:perm[3],perm[4]=perm[4],perm[3]
 if sg:perm=[(j+3)%6 for j in perm]
 perms.append(tuple(perm))
for perm in perms:
 assert tuple(P[perm[j]] for j in range(6))==P
 transformed={sum(1<<perm[j] for j in range(6) if mask>>j&1):r for mask,r in TYPES.items()}
 assert transformed==TYPES
short=[]
for t,norbits in ((2,7),(3,14)):
 orbits={}
 for q in compositions(t):
  key=min(tuple(q[perm[j]] for j in range(6)) for perm in perms)
  orbits.setdefault(key,[]).append(q)
 assert len(orbits)==norbits
 for key,members in sorted(orbits.items()):
  assert all(value(q)==value(key) for q in members)
  assert value(key)>=C-B*(t-2)
  short.append({'t':t,'representative':key,'orbit_size':len(members),'value':str(value(key))})
Path(__file__).with_name('static_module_short_orbits.json').write_text(json.dumps({'A':str(A),'S':[str(v) for v in S],'orbits':short},indent=2)+'\n')
print('Short analytic certificate exact checks passed: Cauchy constants, polynomial, symmetries, 21 orbits.')
