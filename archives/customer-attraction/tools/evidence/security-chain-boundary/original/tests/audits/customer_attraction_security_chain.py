"""Distinct-unit-customer replay, independent of compressed audit and generators."""
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
from pathlib import Path
import json
import argparse
ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument("--output",type=Path)
args=parser.parse_args()
g=json.loads((ROOT/"examples/customer_attraction/local_security_increment.json").read_text())
c=json.loads((ROOT/"evidence/certificates/customer_attraction/local_security_increment.json").read_text())
units=[]
for row in g['customers']:
 assert type(row['multiplicity']) is int and row['multiplicity']>0
 units.extend([frozenset(row['topics'])]*row['multiplicity'])
assert len(units)==113
policy={tuple(row['history']):row['action'] for row in c['strategy']['actions']}
histories=[h for d in range(3) for h in product(range(6),repeat=d)]
assert len(policy)==len(c['strategy']['actions']) and set(policy)==set(histories)
@lru_cache(None)
def end(h):return h if len(h)==3 else end(h+(policy[h],))
@lru_cache(None)
def utilities(z):
 ans=[F(0)]*3
 for U in units:
  I=[i for i,a in enumerate(z) if a in U]
  for i in I:ans[i]+=F(1,len(I))
 return tuple(ans)
@lru_cache(None)
def static(a,B):return sum((F(1,1+sum(b in U for b in B)) for U in units if a in U),F(0))
def cover(z):return sum(any(a in U for a in z) for U in units)
slacks=[]
for h in histories:
 for a in range(6):
  slack=utilities(end(h))[len(h)]-utilities(end(h+(a,)))[len(h)];assert slack>=0;slacks.append(slack)
z=end(());assert z==(0,3,4) and utilities(z)==(F(95,3),F(110,3),F(110,3)) and cover(z)==105
assert max(cover(z) for z in product(range(6),repeat=3))==113
assert len(set(frozenset(i for i,U in enumerate(units) if a in U) for a in range(6)))==6
vs=[];bounds=[]
for spec in [c['security_global'],c['security_after_root']]:
 P=tuple(spec.get('fixed_prefix',[]));r=spec.get('remaining_players',3);p=tuple(map(F,spec['primary']));Q=[(tuple(row['rivals']),F(row['probability'])) for row in spec['dual']]
 assert min(p)>=0 and sum(p)==1 and sum(q for B,q in Q)==1 and all(q>=0 for B,q in Q)
 lo=[sum(p[a]*static(a,P+B) for a in range(6)) for B in product(range(6),repeat=r-1)];hi=[sum(q*static(a,P+B) for B,q in Q) for a in range(6)];v=F(spec['value']);assert min(lo)==max(hi)==v;vs.append(v);bounds.append((lo,hi))
p=tuple(F(x,8) for x in [1,1,2,1,1,2]);lo=[sum(p[a]*static(a,B) for a in range(6)) for B in product(range(6),repeat=2)];Q=[((0,1),F(3,5)),((0,2),F(2,5))];hi=[sum(q*static(a,B) for B,q in Q) for a in range(6)]
assert min(lo)==F(385,12) and max(hi)==F(484,15)
u=utilities(z)[0];full=u+2*vs[1]-3*vs[0];weak=u+F(3,2)*vs[1]-F(5,2)*vs[0]
assert full<0 and weak<0 and u+2*max(hi)-3*min(lo)==-F(1,20) and u+F(3,2)*max(hi)-F(5,2)*min(lo)==-F(17,120)
report={'status':'PASS','unit_customers':113,'types':len(g['customers']),'ordered_histories':43,'full_comparisons':len(slacks),'nonnegative_slacks':len(slacks),'tied_comparisons':sum(s==0 for s in slacks),'actual_path':z,'utilities':list(map(str,utilities(z))),'W':105,'OPT':113,'true_v3':str(vs[0]),'true_v2_at_root_action':str(vs[1]),'full_step_gap':str(full),'weak_step_gap':str(weak),'simple_global_primal_lower':str(min(lo)),'simple_local_dual_upper':str(max(hi)),'simple_local_dual_query_values':list(map(str,hi)),'simple_full_step_upper':str(-F(1,20)),'simple_weak_step_upper':str(-F(17,120)),'root_action_payoffs':[str(utilities(end((a,)))[0]) for a in range(6)]}
# Independent telescoping check from realized utilities and certified values.
V=(vs[0],vs[1],max(static(a,z[:-1]) for a in range(6)))
assert V[-1]==utilities(z)[-1] and V[0]<=V[1]<=V[2]
strong_terms=(utilities(z)[0]+2*V[1]-3*V[0],utilities(z)[1]+V[2]-2*V[1])
weak_terms=(utilities(z)[0]+F(3,2)*V[1]-F(5,2)*V[0],utilities(z)[1]+F(1,2)*V[2]-F(3,2)*V[1])
assert sum(strong_terms)==cover(z)-3*V[0]
assert sum(weak_terms)+utilities(z)[-1]/2==cover(z)-F(5,2)*V[0]
assert cover(z)-3*V[0]>0 and cover(z)-F(5,2)*V[0]>0
report.update({'claim_ids':['CA-SECURITY-CHAIN-INTERFACE','CA-LOCAL-SECURITY-INDUCTION-NO'],
 'strong_telescoping_terms':list(map(str,strong_terms)),
 'weak_telescoping_terms':list(map(str,weak_terms)),
 'weak_terminal_slack':str(utilities(z)[-1]/2),
 'strong_bridge_margin':str(cover(z)-3*V[0]),
 'weak_bridge_margin':str(cover(z)-F(5,2)*V[0]),
 'doubled_half_coverage_margin_2W_minus_OPT':2*cover(z)-113,
 'scope':'Two local induction inequalities fail; both aggregate bridges and half coverage hold in this witness.'})
if args.output:
 args.output.parent.mkdir(parents=True,exist_ok=True)
 with args.output.open('x') as stream:stream.write(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
