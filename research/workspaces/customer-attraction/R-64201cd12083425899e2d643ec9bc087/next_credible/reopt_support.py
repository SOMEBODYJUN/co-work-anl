from pathlib import Path
from fractions import Fraction as F
import numpy as np,json
from scipy.optimize import linprog
from offdiagonal_probe import rows as extra_rows
ROOT=Path(__file__).resolve().parents[5]
ns={};source=(ROOT/'tests/audits/customer_attraction_five_indexed.py').read_text();exec(compile(source.split('from pathlib import Path')[0],'<canonical definitions>','exec'),ns)
p=json.loads((ROOT/'evidence/certificates/customer_attraction/five_player_indexed_bound.json').read_text())['primal'];atoms=p['atoms'];cols=[]
for a in atoms:
 v=ns['evaluate'](list(map(int,a['bits'])),[a['AB_hist'],a['AE_hist'],a['second_hist']],a['menus_lh'],True);v.update(extra_rows(a));cols.append(v)
names=list(cols[0]);G=[[c[n] for c in cols] for n in names];w=[int(any(map(int,a['bits'][:5]))) for a in atoms];o=[int(any(a['AB_hist'][4:])) for a in atoms]
r=linprog(-np.array(o,float),A_ub=-np.array(G,float),b_ub=np.zeros(len(G)),A_eq=[w],b_eq=[1.],bounds=(0,None),method='highs')
report={'scope':'437+27 necessary-row system restricted to original 64 atom support; floating LP only','status':r.message,'objective':-r.fun if r.success else None,'point':r.x.tolist() if r.success else None,'names':names}
print(json.dumps({k:v for k,v in report.items() if k not in ('point','names')},indent=2));Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
