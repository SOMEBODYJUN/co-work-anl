"""Independent literal unit-set replay of the compact StrongA witness."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
P=Path(__file__).resolve().parent
clients=[frozenset((0,1,2)) for _ in range(6)]+[frozenset((1,)),frozenset((2,3)),frozenset((3,)),frozenset((3,))]
last=((3,2,1,1),(2,2,2,2),(1,1,1,1),(1,2,1,1))
sigma={():0,**{(a,):s for a,s in enumerate((0,1,2,1))},**{(a,b):last[a][b] for a,b in product(range(4),repeat=2)}}
def finish(h):
 while len(h)<3:h+=(sigma[h],)
 return h
def pay(z,i):return sum((F(1,sum(a in x for a in z)) for x in clients if z[i] in x),F())
def cover(z):return sum(any(a in x for a in z) for x in clients)
assert len({tuple(a in x for x in clients) for a in range(4)})==4
slacks=[]
for j in range(3):
 for h in product(range(4),repeat=j):
  for a in range(4):
   slack=pay(finish(h),j)-pay(finish(h+(a,)),j)
   assert slack>=0,(h,a);slacks.append(slack)
z=finish(()); W=cover(z)
M=[[pay(z[:i]+(a,)+z[i+1:],i) for a in range(4)] for i in range(3)]
C=sum((F(1,c*(c+1)) for x in clients for j in range(2) if z[j] in x and z[j+1] not in x for c in [sum(a in x for a in z)]),F())
J=sum((F(1,c+1) for x in clients for c in [sum(a in x for a in z)] if c),F())
OPT=max(cover(q) for q in product(range(4),repeat=3))
opt=[q for q in product(range(4),repeat=3) if cover(q)==OPT]
Q=lambda q:sum((M[i][q[i]] for i in range(3)),F())
assert z==(0,0,3) and W==9 and OPT==10
assert M==[[F(3),F(4),F(7,2),F(3,2)]]*2+[[F(2),F(3),F(3),F(3)]]
assert C==1 and J==F(7,2) and sum(map(max,M))-W-C==1
assert Q((1,1,3))==11 and cover((1,1,3))==OPT
assert min(Q(q) for q in opt)==Q((3,3,1))==6
out={'scope':'StrongA and every-optimal-assignment adjacent-wallet bridges false only; not HALF.',
 'unit_clients':len(clients),'distinct_topics':4,'players':3,'ordered_histories':len(sigma),'IC_with_self':len(slacks),'min_slack':str(min(slacks)),
 'actual':z,'profits':[str(pay(z,i)) for i in range(3)],'W':W,'OPT':OPT,
 'frozen_matrix':[[str(v) for v in row] for row in M],'Csum':str(C),'J_base':str(J),
 'sum_frozen_regrets':str(sum(map(max,M))-W),'strong_gap':str(sum(map(max,M))-W-C),
 'optimal_bad_assignment':[1,1,3],'optimal_bad_Q':str(Q((1,1,3))),
 'optimal_good_assignment':[3,3,1],'optimal_good_Q':str(Q((3,3,1))),
 'status':'passed','HALF':'not_refuted'}
with (P/'compact_adjacent_root_literal_audit.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps({k:out[k] for k in ('status','W','OPT','Csum','J_base','strong_gap')}))
