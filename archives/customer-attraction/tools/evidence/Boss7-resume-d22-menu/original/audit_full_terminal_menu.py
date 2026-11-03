"""Exact audit of the full-r-slot menu on an existing strong-push counterexample."""
from fractions import Fraction as F
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'representation'/'terminal_pushforward_D_lt_C_exact.json'
j=json.loads(SOURCE.read_text()); types=j['customer_types']; paths=j['forced_root_paths']; k=len(paths)
K=[[sum((F(t['multiplicity'],1+sum(t['mask']>>b&1 for b in path)) for t in types if t['mask']>>a&1),F(0)) for path in paths] for a in range(k)]
Q=[F(x,3169) for x in (1016,1273,0,0,0,880)]
P=[F(x,15845) for x in (1525,9362,0,0,0,4958)]
upper=[sum(K[a][b]*Q[b] for b in range(k)) for a in range(k)]
lower=[sum(P[a]*K[a][b] for a in range(k)) for b in range(k)]
assert sum(P)==sum(Q)==1 and min(P)>=0 and min(Q)>=0
assert max(upper)==min(lower)==F(239604,3169)
sigma={tuple(row['history']):row['action'] for row in j['certificate']['actions']}
m=j['players']
def follow(h):
 while len(h)<m:h=h+(sigma[h],)
 return h
def util(a,z):return sum((F(t['multiplicity'],sum(t['mask']>>c&1 for c in z)) for t in types if t['mask']>>a&1),F(0))
minimum=F(0);checks=0
for h,a in sigma.items():
 chosen=util(a,follow(h))
 for b in range(k):
  slack=chosen-util(b,follow(h+(b,)));assert slack>=0
  minimum=min(minimum,slack);checks+=1
u=max(F(x) for x in j['forced_root_payoffs'])
report={'scope':'One existing exact instance; not a universal theorem or counterexample to the new menu bound.', 'players':m,'topics':k,'full_history_nodes':len(sigma),'all_action_comparisons':checks,'minimum_SPE_slack':str(minimum),'K':[[str(x) for x in row] for row in K],'primal_Q':list(map(str,Q)),'dual_P':list(map(str,P)),'primal_row_values':list(map(str,upper)),'dual_column_values':list(map(str,lower)),'menu_value':str(max(upper)),'root_u':str(u),'pure_column_0_max':str(max(row[0] for row in K)),'all_exact_checks_passed':True}
(HERE/'full_terminal_menu_audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({key:value for key,value in report.items() if key not in ['K','primal_row_values','dual_column_values']},indent=2))
