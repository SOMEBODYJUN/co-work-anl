"""Designated-certificate diagnostic for LAST-DELETE-ONE and refund identities.
Finite diagnostic only. Universal bounds in last_deletion_contract.md are analytic.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import json,sys
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction.model import Instance
NAMES=['coverage_opportunity_failure','prefix_balance_failure','individual_security_failure','root_tax_failure','global_decorrelation_failure','residual_counterexample','local_security_increment']

def check(name):
 instance=Instance.from_dict(json.loads((ROOT/'examples/customer_attraction'/f'{name}.json').read_text()))
 data=json.loads((ROOT/'evidence/certificates/customer_attraction'/f'{name}.json').read_text()); strategy=data.get('strategy',data)
 actions={tuple(row['history']):row['action'] for row in strategy['actions']}
 p=instance.topic_count;m=instance.players
 def leaf(h,deleted=False):
  h=tuple(h)
  while len(h)<m-(1 if deleted else 0):h+=actions[h],
  return h
 def pay(z,i):
  return sum((F(c.multiplicity, sum(a in c.topics for a in z)) for c in instance.customers if z[i] in c.topics),F())
 records=[];maxratio=F();worst=None;checks=0
 for d in range(m-1):
  for h in product(range(p),repeat=d):
   z=leaf(h);zd=leaf(h,True);u=pay(z,d);last=pay(z,m-1);removed=pay(zd,d);refund=removed-u
   rho=F();best=None
   for a in range(p):
    t=leaf(h+(a,));td=leaf(h+(a,),True)
    value=pay(td,d);slack=u-pay(t,d);r=pay(td,d)-pay(t,d)
    assert value-removed==r-refund-slack
    assert value-removed<=u-refund
    assert value-removed<=2*last-refund
    if value-removed>rho:rho=value-removed;best=a
    checks+=1
   ratio=(rho+refund)/last if last else F()
   if ratio>maxratio:
    maxratio=ratio;worst=dict(history=h,leaf=z,retained_leaf=zd,current=d,last_profit=str(last),old_profit=str(u),refund=str(refund),regret=str(rho),best_action=best,ratio=str(ratio))
 return dict(name=name,checks=checks,max_refund_adjusted_regret_ratio=str(maxratio),witness=worst)
if __name__=='__main__':
 reports=[check(n) for n in NAMES]
 print(json.dumps(dict(scope='seven explicitly named old full SPE certificates; no universal inference from finite results',candidate='rho(h)+R_current(z) <= u_last(z)',reports=reports),indent=2))
