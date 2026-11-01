"""Definition-level independent audit; does not import the CAG implementation."""
import json,itertools
from fractions import Fraction
from pathlib import Path
p=Path(__file__).with_name('k_plus_m_minus_one_failure.json')
z=json.loads(p.read_text());ins=z['instance'];m=ins['players'];k=len(ins['topics'])
customers=[frozenset(row['topics']) for row in ins['customers'] for _ in range(row['multiplicity'])]
pol={tuple(row['history']):row['action'] for row in z['certificate']['actions']}
def end(h):
 while len(h)<m:h=h+(pol[h],)
 return h
def utility(h,i):
 return sum((Fraction(1,sum(a in x for a in h)) for x in customers if h[i] in x),Fraction())
checks=0
for i in range(m):
 for h in itertools.product(range(k),repeat=i):
  val=utility(end(h),i)
  for a in range(k):
   assert val>=utility(end(h+(a,)),i),(h,a)
   checks+=1
path=end(());u=tuple(utility(path,i) for i in range(m))
K=max(sum(j in x for x in customers) for j in range(k))
O=max(sum(any(j in x for j in t) for x in customers) for t in itertools.product(range(k),repeat=m))
assert K+(m-1)*min(u)<O
assert 2*m*min(u)>=O
print(json.dumps({'histories':len(pol),'all_action_comparisons':checks,'path':path,'u':list(map(str,u)),'K':K,'OPT':O,'failed_left_side':str(K+(m-1)*min(u)),'weak_2m_left_side':str(2*m*min(u))},indent=2))
