"""Root raw-packet replay; no author/canonical imports; no instance search."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations_with_replacement, permutations
from functools import lru_cache
import json, hashlib, math
P=Path(__file__).resolve().parent
source=P.parent/'credible/strong_adjacent_gap_attack.json'
d=json.loads(source.read_text()); I=d['endpoint']; m=I['players']; k=len(I['topics'])
rows=[(frozenset(r['topics']),r['multiplicity']) for r in I['customers']]
assert all(isinstance(n,int) and n>0 and X and all(isinstance(a,int) and 0<=a<k for a in X) for X,n in rows)
assert len({tuple(int(a in X) for X,n in rows) for a in range(k)})==k
sig={tuple(r['history']):r['action'] for r in d['strategy']['actions']}
expected={h for j in range(m) for h in product(range(k),repeat=j)}
assert set(sig)==expected and len(sig)==len(d['strategy']['actions'])
assert all(0<=a<k for a in sig.values())
scale=math.lcm(*range(1,m+1))
def counts(z):return tuple(z.count(a) for a in range(k))
@lru_cache(None)
def data(q):
 pay=[0]*k; welfare=0
 for X,n in rows:
  c=sum(q[a] for a in X)
  if c:
   welfare+=n
   v=n*(scale//c)
   for a in X:
    if q[a]:pay[a]+=v
 return tuple(pay),welfare
def finish(h):
 while len(h)<m:h+=(sig[h],)
 return h
def payoff(z,i):return data(counts(z))[0][z[i]]
checks=0; least=None
for h in sorted(expected,key=lambda h:(len(h),h)):
 i=len(h); actual=finish(h); u=payoff(actual,i)
 for a in range(k):
  if a==sig[h]:continue
  gap=u-payoff(finish(h+(a,)),i)
  assert gap>=0,(h,a,gap)
  least=gap if least is None else min(least,gap); checks+=1
z=finish(()); ui=[F(payoff(z,i),scale) for i in range(m)]; W=data(counts(z))[1]
assert sum(ui)==W
cost=[[F(payoff(z[:i]+(a,)+z[i+1:],i),scale) for a in range(k)] for i in range(m)]
Q=sum(map(max,cost)); chosen=[max(range(k),key=lambda a:cost[i][a]) for i in range(m)]
C=[]
for i in range(m-1):
 C.append(sum((F(n,c*(c+1)) for X,n in rows if z[i] in X and z[i+1] not in X for c in [sum(a in X for a in z)]),F()))
J=sum((F(n,c+1) for X,n in rows for c in [sum(a in X for a in z)] if c),F())
Csum=sum(C,F()); gap=Q-W-Csum
OPT=max(data(counts(q))[1] for q in combinations_with_replacement(range(k),m))
best=None; best_T=None; optimal_multisets=0
for q in combinations_with_replacement(range(k),m):
 if data(counts(q))[1]!=OPT:continue
 optimal_multisets+=1
 for T in set(permutations(q)):
  v=sum((cost[i][T[i]] for i in range(m)),F())
  if best is None or v<best:best,best_T=v,T
assert gap>0 and 2*W>=OPT
assert str(Q)==str(d['true_Q']) and str(Csum)==str(d['Csum'])
assert str(gap)==str(d['true_signed_StrongA_gap'])
out={'scope':'Exact refutation of StrongA only; not Q-CAG-HALF, not a general bound.',
 'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'players':m,'distinct_catalog_topics':k,
 'unit_customers_represented':sum(n for X,n in rows),'positive_interest_types':len(rows),
 'complete_ordered_histories':len(expected),'nonself_true_IC':checks,'minimum_IC_slack_scaled':least,
 'actual':z,'actual_profits':list(map(str,ui)),'W':W,'OPT':OPT,'fixed_maximizers':chosen,
 'frozen_row_maxima':list(map(lambda r:str(max(r)),cost)),'Q':str(Q),'adjacent_wallets':list(map(str,C)),
 'Csum':str(Csum),'StrongA_gap':str(gap),'J':str(J),'common_static_surplus_gap_J':str(Q-W-J),
 'minimum_optimal_assignment':best_T,'minimum_optimal_Q':str(best),'optimal_multisets':optimal_multisets,
 'weak_optimal_assignment_gap':str(best-W-Csum),'HALF_margin':2*W-OPT,
 'status':'passed','arbitrary_half':'OPEN','optimal_assignment_Csum_candidate':'not_refuted_here'}
with (P/'strong_adjacent_root_integer_audit.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps({key:out[key] for key in ['status','actual','W','OPT','StrongA_gap','common_static_surplus_gap_J','weak_optimal_assignment_gap']}))
