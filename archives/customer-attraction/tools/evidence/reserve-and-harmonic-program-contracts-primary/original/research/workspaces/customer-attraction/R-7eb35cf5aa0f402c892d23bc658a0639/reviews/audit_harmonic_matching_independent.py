"""Definition-level audit; independent of the proposed lemma and project modules."""
from fractions import Fraction as F
from itertools import product,combinations,permutations
import random,json
from pathlib import Path
out=Path(__file__).resolve().parent
def H(k):return sum((F(1,t) for t in range(1,k+1)),F())
def sequence_floor(bits):
 m=len(bits);b=0;s=F()
 for i,hit in enumerate(bits):
  s+=F(1,b+m-i);b+=hit
 return s
pattern_count=0
for m in range(1,13):
 for hits in product((0,1),repeat=m):
  c=sum(hits);g=sequence_floor(hits);bound=F(c,m)+H(m)-H(c)
  assert g>=bound>=1
  assert sequence_floor((1,)*c+(0,)*(m-c))==bound
  if 0<c<m:
   # Every 01->10 swap changes only the next prefix denominator.
   for j in range(m-1):
    if hits[j:j+2]==(0,1):
     swapped=hits[:j]+(1,0)+hits[j+2:]
     assert sequence_floor(swapped)<g
  pattern_count+=1
for m in range(1,31):
 kappa=F(m)+1-H(m);assert kappa>=1
 for Q in range(0,8):
  for D in range(Q+1):
   for A in range(8):
    W=Q-D+A;lb=(Q+(H(m)-1)*D)/m
    lhs=lb-(Q-W)
    assert lhs==F(Q,m)-kappa*D/m+A
    if Q:
     q=F(W,Q)
     assert lhs==(1-kappa*(1-q))*Q/m+(H(m)-1)*A/m
     if q>=1-1/kappa:assert lhs>=0

def check(catalog,m,policy,compare):
 K=len(catalog);history=()
 while len(history)<m:history+=(policy[history],)
 covered=set().union(*(catalog[a] for a in history));O=set().union(*(catalog[a] for a in compare))
 Q=len(O);W=len(covered);D=len(O-covered)
 vals=[]
 for i in range(m):
  row=[]
  for T in compare:
   dev=history[:i]+(T,)
   while len(dev)<m:dev+=(policy[dev],)
   payoff=F()
   for x in catalog[T]:payoff+=F(1,sum(x in catalog[a] for a in dev))
   row.append(payoff)
  vals.append(row)
 M=max(sum((vals[i][p[i]] for i in range(m)),F()) for p in permutations(range(m)))
 bound=(Q+(H(m)-1)*D)/m
 loadbound=sum((F(sum(x in catalog[a] for a in history),m)+H(m)-H(sum(x in catalog[a] for a in history)) for x in O),F())/m
 multbound=sum((sum(x in catalog[a] for a in compare)*(F(sum(x in catalog[a] for a in history),m)+H(m)-H(sum(x in catalog[a] for a in history))) for x in O),F())/m
 assert M>=multbound>=loadbound>=bound
 return M-bound
checked=0;zero=0
allsets=[frozenset(x for x in range(2) if mask>>x&1) for mask in range(4)]
for K,m in [(1,1),(1,2),(1,3),(2,1),(2,2),(2,3),(3,1),(3,2)]:
 histories=[h for depth in range(m) for h in product(range(K),repeat=depth)]
 for catalog in combinations(allsets,K):
  for actions in product(range(K),repeat=len(histories)):
   policy=dict(zip(histories,actions))
   for compare in product(range(K),repeat=m):
    gap=check(catalog,m,policy,compare);checked+=1;zero+=gap==0
rng=random.Random(3491)
for _ in range(60):
 K=rng.randrange(2,5);m=rng.randrange(1,7)
 catalog=tuple(frozenset(x for x in range(8) if rng.randrange(3)==0) for _ in range(K))
 histories=[h for depth in range(m) for h in product(range(K),repeat=depth)]
 policy={h:rng.randrange(K) for h in histories}
 compare=tuple(rng.randrange(K) for _ in range(m))
 check(catalog,m,policy,compare);checked+=1
report={'single_customer_patterns':pattern_count,'full_strategy_comparison_checks':checked,'exact_coarse_equalities_in_exhaustive_part':zero,'imports_candidate_or_canonical':False,'result':'PASS','scope':'Finite implementation audit; universal proof independently reconstructed in review.'}
# Frozen report is retained separately; replay prints its fresh report.
print(json.dumps(report,indent=2))
