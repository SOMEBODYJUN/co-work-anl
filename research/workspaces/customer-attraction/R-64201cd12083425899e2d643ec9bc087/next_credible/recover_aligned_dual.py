"""Exact dual on the original 64 atom support only, NOT a full-type certificate."""
from pathlib import Path
from fractions import Fraction as F
import json
from offdiagonal_probe import rows as offrows
from crossmenu_probe import rows as crossrows
from menutax_probe import rows as taxrows
from alignedtax_probe import rows as alignrows
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).parent
ns={};src=(ROOT/'tests/audits/customer_attraction_five_indexed.py').read_text();exec(compile(src.split('from pathlib import Path')[0],'<canonical row definitions>','exec'),ns)
primal=json.loads((ROOT/'evidence/certificates/customer_attraction/five_player_indexed_bound.json').read_text())['primal'];atoms=primal['atoms'];cols=[]
for a in atoms:
 v=ns['evaluate'](list(map(int,a['bits'])),[a['AB_hist'],a['AE_hist'],a['second_hist']],a['menus_lh'],True);v.update(offrows(a));v.update(crossrows(a));v.update(taxrows(a));v.update(alignrows(a));cols.append(v)
floating=json.loads((HERE/'reopt_aligned.json').read_text());names=floating['names'];active=[names[i] for i,x in enumerate(floating['dual_lambda']) if x>1e-9]
w=[int(any(map(int,a['bits'][:5]))) for a in atoms];o=[int(any(a['AB_hist'][4:])) for a in atoms];support=[i for i,x in enumerate(floating['point']) if x>1e-9]
basis={};nvar=1+len(active)
for i in support:
 v=[F(w[i])]+[-cols[i][n] for n in active]+[F(o[i])]
 for pivot,b in sorted(basis.items()):
  x=v[pivot]
  if x:v=[a-x*c for a,c in zip(v,b)]
 pivot=next((i for i,x in enumerate(v[:-1]) if x),None)
 if pivot is None:
  assert v[-1]==0;continue
 x=v[pivot];basis[pivot]=[a/x for a in v]
assert len(basis)==nvar,(len(basis),nvar,len(support))
x=[F()]*nvar
for pivot,b in sorted(basis.items(),reverse=True):x[pivot]=b[-1]-sum(b[i]*x[i] for i in range(pivot+1,nvar))
beta=x[0];lam=dict(zip(active,x[1:]));assert beta<2 and min(lam.values())>=0
residuals=[beta*w[i]-o[i]-sum(lam[n]*cols[i][n] for n in active) for i in range(len(atoms))];assert min(residuals)>=0
report={'scope':'exact certificate only over 64 frozen customer-type atoms; all other legal atoms unverified','beta':str(beta),'gap_below_two':str(2-beta),'multipliers':{n:str(v) for n,v in lam.items()},'support_column_residuals':[str(x) for x in residuals],'verified_nonnegative_on_64_columns':True,'full_type_certificate':False}
(HERE/'aligned_support_exact_dual.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('multipliers','support_column_residuals')},indent=2))
