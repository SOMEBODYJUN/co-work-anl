"""Exact QA for one analytic all-m counterfamily; no instance/policy search.
This particular explicit policy depends only on counts, so all count-prefix
states certify all ordered histories; this is not a restriction on the target.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from functools import lru_cache
from pathlib import Path
import json, math
P=Path(__file__).resolve().parent

def audit(m):
 assert m>=2
 k=m-1; C=0; A=tuple(range(1,k+1)); B=k+1; D=k+2; n=k+3
 groups=[(frozenset((C,*A,B)),k*(k+1)),*((frozenset((a,)),1) for a in A),(frozenset((B,D)),1),(frozenset((D,)),k)]
 scale=math.lcm(*range(1,m+1))
 def add(q,a):return q[:a]+(q[a]+1,)+q[a+1:]
 def policy(q):
  used=sum(q)
  if q[C]==used:return C if used<k else D
  return next((a for a in A if q[a]==0),B)
 @lru_cache(None)
 def finish(q):
  if sum(q)==m:return q
  return finish(add(q,policy(q)))
 @lru_cache(None)
 def scores(q):
  pay=[0]*n; W=0
  for X,size in groups:
   c=sum(q[a] for a in X)
   if c:
    W+=size; value=size*(scale//c)
    for a in X:
     if q[a]:pay[a]+=value
  return tuple(pay),W
 states=checks=0; minslack=None
 for length in range(m):
  for h in combinations_with_replacement(range(n),length):
   q=tuple(h.count(a) for a in range(n)); a=policy(q)
   value=scores(finish(q))[0][a]; states+=1
   for t in range(n):
    gap=value-scores(finish(add(q,t)))[0][t]
    assert gap>=0,(m,q,t,gap)
    minslack=gap if minslack is None else min(minslack,gap);checks+=1
 z=(C,)*k+(D,); q=tuple(z.count(a) for a in range(n)); W=scores(q)[1]
 matrix=[]
 for i in range(m):
  row=[]
  for t in range(n):
   zz=z[:i]+(t,)+z[i+1:];qq=tuple(zz.count(a) for a in range(n))
   row.append(F(scores(qq)[0][t],scale))
  matrix.append(row)
 for row in matrix[:k]:
  assert row[C]==m and all(row[a]==m+1 for a in A) and row[B]==F(2*m+1,2) and row[D]==F(m,2)
 assert matrix[-1][C]==m-1 and all(matrix[-1][a]==m for a in (*A,B,D))
 N=sum(size for X,size in groups); OPT=m*m+m-1
 assert W==m*m and N==OPT
 optcost=[]
 for di in range(m):
  T=list(A);T.insert(di,D)
  assert set(T)==set((*A,D))
  optcost.append(sum((matrix[i][t] for i,t in enumerate(T)),F()))
 Q=min(optcost); Cadj=F(k*(k+1),k*(k+1)); gap=Q-W-Cadj
 assert Cadj==1 and Q-W==F(m-4,2) and gap==F(m-6,2)
 assert 2*W>=OPT and (gap>0)==(m>6)
 assert len({tuple(a in X for X,size in groups) for a in range(n)})==n
 return {'m':m,'catalog_size':n,'unit_customers':N,'count_prefix_states':states,'IC_checked_with_self':checks,
   'all_ordered_histories_represented':sum(n**j for j in range(m)),
   'count_policy_is_explicit':'history all C and unused A labels depend only on prefix counts',
   'min_IC_slack_scaled':minslack,'W':W,'OPT':OPT,'minimum_optimal_Q':str(Q),'C_adj':str(Cadj),
   'minimum_optimal_gap':str(gap),'strong_gap':str(sum(map(max,matrix))-W-Cadj),
   'all_optimal_assignment_costs_by_D_position':list(map(str,optcost))}

out={'scope':'QA of explicit all-m auxiliary-counterfamily; not a HALF counterexample or search.',
 'cases':[audit(m) for m in (2,3,5,7)],'arbitrary_HALF':'OPEN','existential_adjacent_wallet_bridge':'refuted for m>=7 by analytic family'}
with (P/'optimal_adjacent_family_exact_audit.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps(out))
