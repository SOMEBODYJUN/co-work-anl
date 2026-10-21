"""Definition-level review of the sibling's 23-unit-customer complete SPE.
No canonical solver, model, strategy cone, or author's audit is imported.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'credible_counterexample/payoff_cap_failure.json'
raw=SOURCE.read_bytes();record=json.loads(raw);ins=record['instance'];p=len(ins['topics']);m=ins['players']
assert (p,m)==(5,3)
units=[]
for row in ins['customers']:
 assert isinstance(row['multiplicity'],int) and row['multiplicity']>0
 likes=frozenset(row['topics']);assert likes<=set(range(p))
 units.extend([likes for _ in range(row['multiplicity'])])
assert len(units)==23
expected={h for depth in range(m) for h in product(range(p),repeat=depth)}
actions={tuple(x['history']):x['action'] for x in record['strategy']['actions']}
assert len(actions)==len(record['strategy']['actions']) and set(actions)==expected
assert all(a in range(p) for a in actions.values())

def complete(prefix):
 out=tuple(prefix)
 while len(out)<m:out+=(actions[out],)
 return out

def terminal(path):
 pay=[Fraction(0) for _ in path];covered=0
 for likes in units:
  attracted=[i for i,a in enumerate(path) if a in likes]
  if attracted:
   covered+=1
   for i in attracted:pay[i]+=Fraction(1,len(attracted))
 assert sum(pay)==covered
 return tuple(pay),covered

all_profiles={s:terminal(s) for s in product(range(p),repeat=m)}
checks=[];strict=tied=0
for h in sorted(expected,key=lambda h:(len(h),h)):
 actor=len(h);actual=complete(h);u=all_profiles[actual][0][actor]
 table=[]
 for alternative in range(p):
  deviated=complete(h+(alternative,));v=all_profiles[deviated][0][actor]
  assert u>=v,(h,actions[h],alternative,u,v)
  if alternative!=actions[h]:
   strict+=int(u>v);tied+=int(u==v)
  table.append({'action':alternative,'terminal':deviated,'own_payoff':str(v)})
 checks.append({'history':h,'selected':actions[h],'actual_terminal':actual,'actual_own_payoff':str(u),'all_action_branches':table})
root=complete(());pay,W=all_profiles[root];O=max(v[1] for v in all_profiles.values())
assert root==(0,1,2) and pay==(Fraction(5),Fraction(6),Fraction(12)) and W==O==23
counts=tuple(root.count(a) for a in range(p));assert list(counts)==record['strategy']['terminal_counts']
assert list(root)==record['path'] and list(map(str,pay))==record['payoffs']
assert record['welfare']==W and record['optimum']==O
share=pay[2]/W;assert share==Fraction(record['value'])==Fraction(12,23)>Fraction(1,2)
pairratio=pay[2]/pay[0];assert pairratio==Fraction(12,5)>2
assert min(pay)>=Fraction(O,2*m-1)
report={'source':str(SOURCE.relative_to(HERE.parents[4])),'source_sha256':hashlib.sha256(raw).hexdigest(),'implementation':'independent expanded unit customers, standard-library Fraction, direct full ordered histories','units':len(units),'topics':p,'players':m,'decision_histories':len(checks),'proper_deviations':strict+tied,'strict_proper_deviations':strict,'tied_proper_deviations':tied,'including_self_comparisons':sum(len(x['all_action_branches']) for x in checks),'terminal_profiles':len(all_profiles),'all_deviations_nonprofitable':True,'root':root,'payoffs':list(map(str,pay)),'welfare':W,'optimum':O,'largest_share':str(share),'share_above_half':str(share-Fraction(1,2)),'largest_to_smallest_payoff_ratio':str(pairratio),'pairwise_cap_violation':str(pay[2]-2*pay[0]),'weak_individual_floor':str(Fraction(O,2*m-1)),'weak_individual_floor_min_slack':str(min(pay)-Fraction(O,2*m-1)),'claim_scope':'refutes every-player u_i<=W/2 and pairwise u_i<=2u_j; does not refute Q-CAG-HALF or u_i>=OPT/(2m-1)','node_checks':checks}
HERE.joinpath('payoff_cap_independent_audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='node_checks'},indent=2))
