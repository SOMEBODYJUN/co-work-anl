"""Exact tests of priority-dependent row selection, not a half counterexample."""
from fractions import Fraction as F
from itertools import permutations, product, combinations
from pathlib import Path
import json

def audit(topics, m, policy):
 def follow(h):
  while len(h)<m:h=h+(policy[h],)
  return h
 def pay(z):
  out=[F(0)]*m
  for x in set().union(*topics):
   own=[i for i,a in enumerate(z) if x in topics[a]]
   for i in own:out[i]+=F(1,len(own))
  return tuple(out)
 gaps=[]
 for d in range(m):
  for h in product(range(len(topics)),repeat=d):
   z=follow(h)
   for a in range(len(topics)):
    v=follow(h+(a,));g=pay(z)[d]-pay(v)[d]
    assert g>=0
    gaps.append(g)
 def winner(z,i,pi):
  rank={who:k for k,who in enumerate(pi)}
  return sum(x in topics[z[i]] and all(rank[i]<rank[j] for j,a in enumerate(z) if j!=i and x in topics[a]) for x in set().union(*topics))
 for z in product(range(len(topics)),repeat=m):
  for i in range(m):
   assert F(sum(winner(z,i,pi) for pi in permutations(range(m))),len(tuple(permutations(range(m)))))==pay(z)[i]
 return follow,pay,winner,len(gaps)

# Root IC: A1 then B2, with follower always B.
A=frozenset({0});B=frozenset({1,2})
f,p,w,ic=audit((A,B),2,{():0,(0,):1,(1,):1})
z=f(());dev=f((1,));records=[]
for pi in permutations(range(2)):
 lam=int(pi.index(0)<pi.index(1));delta=w(z,0,pi)-w(dev,0,pi)
 records.append({'priority':pi,'lambda':lam,'winner_IC_difference':delta})
weighted=sum(F(v['lambda']*v['winner_IC_difference'],2) for v in records)
Gamma=p(z)[0]-p(dev)[0]
assert weighted==F(-1,2) and Gamma==0

# Last IC: A2 then B1. Adaptive query picks A iff current has earlier priority.
A=frozenset({0,1});B=frozenset({2})
f2,p2,w2,ic2=audit((A,B),2,{():0,(0,):1,(1,):0})
z2=f2(());selected=[]
for pi in permutations(range(2)):
 a=0 if pi.index(1)<pi.index(0) else 1
 end=(0,a)
 selected.append({'priority':pi,'query':a,'pointwise_row_mass':1,'winner_payoff':w2(end,1,pi)})
selected_pay=sum(F(v['winner_payoff'],2) for v in selected)
assert selected_pay==F(3,2)>p2(z2)[1]==1
assert all(p2((0,a))[1]==1 for a in (0,1))
# Reconstruct selected payment by ordinary shares + covariance (actual u=1).
assert selected_pay-p2(z2)[1]==F(1,2)
# Boundaries: zero clients, unique empty topic; one provider no adaptive priority gain.
f0,p0,w0,ic0=audit((frozenset(),),2,{():0,(0,):0})
assert p0(f0(()))==(0,0)
f1,p1,w1,ic1=audit((frozenset(),A,B),1,{():1})
assert p1(f1(()))==(2,)
assert max(w1((a,),0,(0,)) for a in range(3))==2
report={'status':'PASS','scope':'Two naive priority payment claims fail on full-history original CAG SPE; no target counterexample','root_conditional_IC':{'actual':z,'deviation':dev,'Gamma':str(Gamma),'IC_checks':ic,'priority_cases':records,'weighted_expected_IC':str(weighted)},'adaptive_last_query':{'actual':z2,'actual_payoffs':list(map(str,p2(z2))),'IC_checks':ic2,'priority_cases':selected,'selected_expected_payoff':str(selected_pay),'ordinary_row_profit':'1','strict_gap':str(selected_pay-1),'W':3,'OPT_2':3},'boundary_IC_checks':{'zero_clients':ic0,'one_provider':ic1}}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
