"""Replay the two stated share-deletion closure attacks on one old input.
Finite exact checks refute only the explicit stronger closure candidates.
"""
from pathlib import Path
import sys,json
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction import CustomerType,Instance,ExactSPESolver,verify_certificate
src=ROOT/'examples/customer_attraction/individual_security_failure.json'
raw=json.loads(src.read_text())
old=Instance.from_dict(raw.get('instance',raw))
solver=ExactSPESolver(old)
scale=6

def delete(q,a):
 clients=[]
 for z in old.customers:
  c=sum(q[t] for t in z.topics)
  value=F(z.multiplicity)*(F(c-1,c) if a in z.topics else F(1))
  assert (scale*value).denominator==1
  if value:clients.append(CustomerType(z.topics,int(scale*value)))
 return Instance(old.topics,tuple(clients),old.players-1)

q=(0,1,0,0,1,1)
original_cert=solver.certificate(on_path=(1,4,5))
verify_certificate(old,original_cert).assert_valid()
reduced=delete(q,1); rs=ExactSPESolver(reduced)
remaining=(0,0,0,0,1,1)
assert remaining not in rs.outcomes()
original_pay=old.player_payoffs((1,4,5))
assert original_pay[0]==min(original_pay)
q2=(1,1,0,0,1,0)
assert q2 in solver.outcomes()
verify_certificate(old,solver.certificate(q2)).assert_valid()
W=old.welfare(q2); assert W==32
losses=[]
for a in [0,1,4]:
 game=delete(q2,a); s=ExactSPESolver(game)
 cert=s.worst_certificate(); verify_certificate(game,cert).assert_valid()
 value=F(s.minimum_welfare(),scale)
 losses.append(value)
assert losses==[F(125,6),F(125,6),F(70,3)]
assert sum(losses)==65>2*W
assert sum(losses)-2*W==1
out={'source':str(src.relative_to(ROOT)),'scale':scale,
 'minimal_payoff_first_deletion':{'path':[1,4,5],'payoffs':list(map(str,original_pay)),
 'remaining_counts':remaining,'preserved':False,'reduced_outcomes':sorted(rs.outcomes())},
 'average_closure':{'original_counts':q2,'W':W,'deleted_worst_welfares':list(map(str,losses)),
 'sum':str(sum(losses)),'claimed_upper':2*W,'strict_gap':'1'},
 'scope':'Only explicit deletion-closure candidates are refuted; no HALF counterexample.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
