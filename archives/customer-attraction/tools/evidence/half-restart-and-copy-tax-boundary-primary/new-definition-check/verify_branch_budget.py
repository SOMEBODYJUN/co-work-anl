from fractions import Fraction as F
from itertools import product
import json
# Six distinct unit customers, in source order; no author code/solver imports.
clients=[{1},{1,2},{1,2},{0},{0},{0,2}]
actions={(0,):0,(1,):1,(2,):0,(0,0):1,(0,1):1,(0,2):1,(1,0):0,(1,1):0,(1,2):0,(2,0):1,(2,1):0,(2,2):0,():0}
def leaf(h):
 h=tuple(h)
 while len(h)<3:h=h+(actions[h],)
 return h
def load(path):return [sum(a in x for a in path) for x in clients]
def profit(path,i):
 q=load(path);return sum((F(1,q[j]) for j,x in enumerate(clients) if path[i] in x),F(0))
rows=[]
for length in range(3):
 for h in product(range(3),repeat=length):
  values=[profit(leaf(h+(a,)),length) for a in range(3)];chosen=actions[h];assert values[chosen]==max(values)
  rows.append(dict(history=list(h),action=chosen,values=list(map(str,values)),leaves=[list(leaf(h+(a,))) for a in range(3)]))
assert len(rows)==13

def active_profit(background,path):
 b=load(background);q=load(path)
 return sum((F(c,b[j]+c) for j,c in enumerate(q) if c),F(0))
def tax(background,path):
 b=load(background);total=F(0)
 for i,a in enumerate(path):
  k=len(path)-i
  total+=sum((F(1,b[j]+1)-F(1,b[j]+k) for j,x in enumerate(clients) if a in x),F(0))
  b=[b[j]+int(a in x) for j,x in enumerate(clients)]
 return total
def harmonic(n):return sum((F(1,j) for j in range(1,n+1)),F(0))
def phi(background,path):
 b=load(background);q=load(path);return sum((harmonic(b[j]+q[j])-harmonic(b[j]) for j in range(6)),F(0))
actual=leaf(());branch=leaf((2,));assert actual==(0,0,1) and branch==(2,0,1)
W=active_profit((),actual);C=tax((),actual);V=active_profit((2,),branch[1:]);Ct=tax((2,),branch[1:]);arrival=phi((),(2,));lhs=W+C;rhs=arrival+V+Ct
assert (W,C,V,Ct,arrival,lhs,rhs,rhs-lhs)==tuple(map(F,['6','5/2','9/2','7/6','3','17/2','26/3','1/6']))
assert profit(actual,0)==profit(branch,0)==F(3,2)
profiles={tuple(path.count(a) for a in range(3)):phi((),path) for path in product(range(3),repeat=3)}
assert len(profiles)==10 and max(profiles.values())==F(15,2) and lhs-max(profiles.values())==1
result=dict(status='pass',scope='One new independent definition check of the explicit six-unit-client, three-player strategy; not author replay, no optimizer or set-valued SPE solver.',original_program_calls=0,ordered_nonterminal_histories=13,including_self_values=39,nonself_comparisons=26,rows=rows,actual=list(actual),forced_2=list(branch),actual_payoffs=[str(profit(actual,i)) for i in range(3)],source_payoff_in_forced_branch=str(profit(branch,0)),W=str(W),ordered_self_copy_tax=str(C),forced_child_active_profit=str(V),forced_child_ordered_tax=str(Ct),first_arrival_potential=str(arrival),branch_mono_left=str(lhs),branch_mono_right=str(rhs),failure_gap=str(rhs-lhs),all_ten_count_profiles={','.join(map(str,k)):str(v) for k,v in sorted(profiles.items())},maximum_three_slot_harmonic_potential='15/2',candidate_slack='1')
print(json.dumps(result,ensure_ascii=False,indent=2))
