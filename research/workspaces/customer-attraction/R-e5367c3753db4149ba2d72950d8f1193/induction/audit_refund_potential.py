"""Definition-level audit of a general all-history deletion-potential identity.
No SPE solver or other audit implementation is imported. Finite checks audit the
formulas; the universal proof is in refund_potential_contract.md.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import product,combinations
import json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4]
NAMES=['coverage_opportunity_failure','prefix_balance_failure','individual_security_failure','root_tax_failure','global_decorrelation_failure','residual_counterexample','local_security_increment']

def fixture(name):
 data=json.loads((ROOT/'examples/customer_attraction'/f'{name}.json').read_text())
 raw=json.loads((ROOT/'evidence/certificates/customer_attraction'/f'{name}.json').read_text());s=raw.get('strategy',raw)
 return data, {tuple(row['history']):row['action'] for row in s['actions']}

def obstruction():
 topics=['A','B','T','C'];data=dict(players=3,topics=topics,customers=[dict(topics=[0,1,2],multiplicity=24),dict(topics=[0],multiplicity=1),dict(topics=[1],multiplicity=1),dict(topics=[3],multiplicity=9)])
 actions={():0,(0,):1,(1,):0,(2,):3,(3,):0}
 last=[[1,3,1,1],[3,0,0,0],[1,0,0,0],[1,0,0,0]]
 for a,b in product(range(4),repeat=2):actions[a,b]=last[a][b]
 return data,actions

def audit(name,data,actions):
 p=len(data['topics']);m=data['players'];types=[(set(c['topics']),c['multiplicity']) for c in data['customers']]
 def pay(z,i):
  return sum((F(w,sum(a in B for a in z)) for B,w in types if z[i] in B),F())
 def original_leaf(h):
  h=tuple(h)
  while len(h)<m:h+=actions[h],
  return h
 original_checks=0
 for h in actions:
  u=pay(original_leaf(h),len(h))
  for a in range(p):
   assert u>=pay(original_leaf(h+(a,)),len(h))
   original_checks+=1
 counts=dict(deletion_sets=0,projected_nodes=0,projected_comparisons=0,suffix_budgets=0)
 for q in range(m):
  for Ltuple in combinations(range(m),q):
   L=set(Ltuple);J=[j for j in range(m) if j not in L];n=len(J);counts['deletion_sets']+=1
   def lift(h):
    h=tuple(h);z=();k=0
    for j in range(m):
     if j in L:z+=actions[z],
     elif k<len(h):z+=h[k],;k+=1
     else:break
    return z
   def reduced_leaf(h):
    h=tuple(h)
    while len(h)<n:h+=actions[lift(h)],
    return h
   def quantities(y):
    z=lift(y);assert len(z)==m
    assert tuple(z[j] for j in J)==y
    old=[pay(z,j) for j in J];new=[pay(y,t) for t in range(n)]
    R=[u-v for u,v in zip(new,old)];assert min(R)>=0
    P=sum((pay(z,j) for j in L),F())
    e=sum(w for B,w in types if any(a in B for a in z) and not any(a in B for a in y))
    H=P-e
    assert H==sum(R,F()) and H>=0
    return z,old,new,R,P,e,H
   for k in range(n):
    for h in product(range(p),repeat=k):
     y=reduced_leaf(h);z,old,new,R,P,e,H=quantities(y)
     eps=[H-r for r in R];assert min(eps)>=0
     M=max(R);epsM=[M-r for r in R];assert min(epsM)>=0
     assert sum(epsM[k:],F())==(n-k)*M-H+sum(R[:k],F())
     assert sum(eps[k:],F())==(n-k-1)*H+sum(R[:k],F())
     counts['suffix_budgets']+=1;counts['projected_nodes']+=1
     for a in range(p):
      yd=reduced_leaf(h+(a,));zd,od,nd,Rd,Pd,ed,Hd=quantities(yd)
      gamma=old[k]-od[k];assert gamma>=0
      gain=nd[k]-new[k]
      assert gain-(Hd-H)==(H-R[k])-(Hd-Rd[k])-gamma
      assert gain-(Hd-H)<=H-R[k]-gamma
      Md=max(Rd)
      assert gain-(Md-M)==(M-R[k])-(Md-Rd[k])-gamma
      counts['projected_comparisons']+=1
 result=dict(name=name,original_IC_comparisons=original_checks,**counts)
 if name=='last_delete_one_failure':
  z=original_leaf(());actual=pay(z,0);last=pay(z,2)
  y=(2,actions[(2,)])
  d=original_leaf((2,));post=pay(y,0)
  result['failure']=dict(actual_leaf=z,actual_profits=[str(pay(z,i)) for i in range(m)],forced_leaf=d,old_deviation_profit=str(pay(d,0)),deleted_deviation_leaf=y,postdelete_deviation_profit=str(post),violation=str(post-actual-last),actual_captured_refund='0',deviation_captured_refund='12')
 return result
if __name__=='__main__':
 reports=[audit('last_delete_one_failure',*obstruction())]
 reports.extend(audit(name,*fixture(name)) for name in NAMES)
 result=dict(status='pass',scope='finite exact audit of total-refund H and max-refund M potential formulas and one full-SPE auxiliary counterexample; universal identities proved analytically',reports=reports)
 print(json.dumps(result,indent=2))
