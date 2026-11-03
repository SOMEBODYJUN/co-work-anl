"""Exact five-player strict K>Gamma example, with every ordered IC checked."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import json

S=(0,1);sizes=(5,1);m=5

def payoff(z,i):return F(sizes[z[i]],z.count(z[i]))
policy={}
@lru_cache(None)
def outcome(h):
 if len(h)==m:return h
 kids={a:outcome(h+(a,)) for a in S}
 if all(a==0 for a in h):a=0 if len(h)<4 else 1
 else:a=max(S,key=lambda a:(payoff(kids[a],len(h)),-a))
 policy[h]=a
 return kids[a]
z=outcome(())
count=0
for t in range(m):
 for h in product(S,repeat=t):
  source=outcome(h)
  for a in S:
   assert payoff(source,t)>=payoff(outcome(h+(a,)),t)
   count+=1
assert z==(0,0,0,0,1)
q=z[:3]
def phi(z):return sum(F(sizes[a])*sum((F(1,j) for j in range(1,z.count(a)+1)),F(0)) for a in S)
maxpot=max(phi(q+(a,b)) for a,b in product(S,repeat=2))
gamma=maxpot-phi(z)
astar=[a for a in S if any(phi(q+(a,b))==maxpot for b in S)]
delta={a:payoff(outcome(q+(a,)),3) for a in astar}
ustar=min(delta.values());epsilon=payoff(z,3)-ustar;K=gamma+epsilon
tau=F(5,4*5)
assert gamma==0 and K==F(1,4) and tau==K
# Genuine integer-opponent v5=1: pure A guarantees at least 1; A^4 caps both queries at 1.
assert all(F(5,1+bg.count(0))>=1 for bg in product(S,repeat=4))
assert all(F(sizes[a],1+(0,0,0,0).count(a))==1 for a in S)
out={'unit_customers':6,'full_ordered_decision_nodes':len(policy),'IC_comparisons':count,'actual':z,'profits':[str(payoff(z,i)) for i in range(m)],'v5':'1','Gamma':str(gamma),'delta_by_maximizing_first_topic':{str(a):str(d) for a,d in delta.items()},'epsilon_star':str(epsilon),'K':str(K),'tau':str(tau),'scope':'exact strict credit example; neither ONE-GAP nor HALF5 is violated'}
print(json.dumps(out,indent=2))
