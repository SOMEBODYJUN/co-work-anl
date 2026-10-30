"""Build and independently replay a complete root SPE realizing the GLOBAL failure.

The complete strategy comes from the canonical exact oracle. The independent
unit-client replay below uses neither its payoff implementation nor verifier.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,sys

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction import CustomerType,Instance,ExactSPESolver,verify_certificate

HERE=Path(__file__).resolve().parent
ROWS=[(1,10),(2,12),(4,5),(8,5),(20,2),(24,2),(36,2),(40,2),(49,6),(50,6)]

def run():
 ins=Instance(tuple('ABTQRS'),tuple(CustomerType(frozenset(a for a in range(6) if mask&(1<<a)),n) for mask,n in ROWS),4)
 cert=ExactSPESolver(ins).certificate(on_path=(0,1,0,1))
 verify_certificate(ins,cert).assert_valid()
 clients=[frozenset(a for a in range(6) if mask&(1<<a)) for mask,n in ROWS for _ in range(n)]
 def payoff(a,terminal):
  return sum((F(1,sum(c in interest for c in terminal)) for interest in clients if a in interest),F(0))
 def follow(h):
  while len(h)<4: h=h+(cert.actions[h],)
  return h
 expected={h for n in range(4) for h in product(range(6),repeat=n)}
 assert set(cert.actions)==expected
 checked=0; minimum_slack=None
 for h in sorted(expected,key=lambda h:(len(h),h)):
  chosen=cert.actions[h]; current=payoff(chosen,follow(h))
  for a in range(6):
   slack=current-payoff(a,follow(h+(a,)))
   assert slack>=0,(h,a,slack)
   checked+=1
   minimum_slack=slack if minimum_slack is None else min(minimum_slack,slack)
 assert follow(())==(0,1,0,1)
 assert checked==259*6
 actual_u=[payoff(a,follow(())) for a in follow(())]
 assert actual_u==[F(8),F(9),F(8),F(9)]
 prefix=(0,1); actual_tail=(0,1)
 bg=[sum(a in interest for a in prefix) for interest in clients]
 assert all(v in [0,1] for v in bg)
 delta=sum(b==0 and any(a in interest for a in actual_tail) for interest,b in zip(clients,bg))
 fresh=[]
 for a in range(6):
  for b in range(a,6):
   fresh.append((sum(p==0 and (a in interest or b in interest) for interest,p in zip(clients,bg)),(a,b)))
 assert max(v for v,pair in fresh)==18
 assert delta==0 and sum(actual_u[2:])==17
 instance_data={'topics':list(ins.topics),'players':4,'customers':[{'topics':sorted(c.topics),'multiplicity':c.multiplicity} for c in ins.customers]}
 (HERE/'global_actual_prefix_instance.json').write_text(json.dumps(instance_data,indent=2))
 (HERE/'global_actual_prefix_complete_spe.json').write_text(json.dumps(cert.to_dict(),indent=2))
 result={'status':'complete root SPE independently replayed on 52 explicit unit clients','players':4,'topics':6,'unit_customers':52,'on_path':list(follow(())),'actual_utilities':[str(v) for v in actual_u],'root_welfare':34,'root_OPT_4':52,'checked_ordered_histories':len(expected),'checked_comparisons_including_self':checked,'checked_proper_deviations':checked-len(expected),'minimum_slack':str(minimum_slack),'actual_prefix':[0,1],'tail_P':17,'tail_Delta':delta,'fresh_OPT_2':18,'global_credit_gap':-1,'claim_refuted':'P+Delta>=freshOPT at every actual prefix of every complete root SPE','main_half_refuted':False}
 assert ins.optimal_welfare()==52
 (HERE/'global_actual_prefix_audit.json').write_text(json.dumps(result,indent=2))
 print(json.dumps(result,indent=2))

if __name__=='__main__': run()
