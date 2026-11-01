"""Independent definition-level verification of an existing 61-customer instance.
Does not import the canonical model, exact solver, or certificate verifier.
"""
import json
from fractions import Fraction as F
from itertools import product
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROWS=[((0,),12),((1,),8),((2,),4),((3,),8),((0,4),6),((0,5),6),((2,4),3),((2,5),3),((0,4,5),6),((1,4,5),2),((2,4,5),1),((3,4,5),2)]
obj=json.loads((HERE/'actual_root_B_certificate.json').read_text())
actions={tuple(x['history']):x['action'] for x in obj['certificate']['actions']}
expected={h for i in range(4) for h in product(range(6),repeat=i)}
assert set(actions)==expected

def pay(h,i):
 a=h[i]
 return sum((F(n,sum(b in B for b in h)) for B,n in ROWS if a in B),F(0))
def walk(h):
 while len(h)<4:h=h+(actions[h],)
 return h
checked=0
for h in expected:
 own=pay(walk(h),len(h))
 for a in range(6):
  assert own>=pay(walk(h+(a,)),len(h)),(h,a)
  checked+=1
actual=walk(())
assert actual==(1,0,0,5)
assert tuple(pay(actual,i) for i in range(4))==(9,13,13,11)
assert walk((0,))==(0,0,0,5)
V=tuple(tuple(pay(walk(actual[:i]+(a,)),i) for a in range(6)) for i in range(4))
assert V==((9,9,9,9,9,9),(13,5,11,10,11,11),(13,5,11,10,11,11),(10,5,11,10,11,11))
root_A_incumbent=[]
for a,b in product(range(6),repeat=2):
 vals=tuple(pay((0,a,b,last),3) for last in range(6))
 root_A_incumbent.extend(pay((0,a,b,last),0) for last in range(6) if vals[last]==max(vals))
assert min(root_A_incumbent)==9
assert V[0][0]<F(3,4)*V[1][0]
assert max(V[0])<F(3,4)*max(V[1])
expected_brs=((2,4,5),(0,),(0,),(0,),(0,),(0,))
expected_first=((15,13,13),(5,),(11,),(10,),(11,),(11,))
expected_inc=((15,13,13),(15,),(15,),(15,),(13,),(13,))
for a in range(6):
 vals=tuple(pay((1,0,a,b),3) for b in range(6))
 br=tuple(b for b in range(6) if vals[b]==max(vals))
 assert br==expected_brs[a]
 assert tuple(pay((1,0,a,b),2) for b in br)==expected_first[a]
 assert tuple(pay((1,0,a,b),1) for b in br)==expected_inc[a]
assert min(expected_first[0])>max(v for row in expected_first[1:] for v in row)
print(f'PASS: {len(expected)} ordered histories, {checked} real branch comparisons, V matrix, root-A last-BR lower bound, and six-row conditional SPE table.')
