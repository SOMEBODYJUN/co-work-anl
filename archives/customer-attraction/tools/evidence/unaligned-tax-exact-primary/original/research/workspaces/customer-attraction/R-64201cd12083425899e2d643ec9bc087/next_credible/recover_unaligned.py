"""Recover an exact >2 obstruction after off-diagonal/cross-menu/all-pair tax rows.
This point is cut by aligned tax rows and is not a SPE.
"""
from pathlib import Path
from fractions import Fraction as F
import json,sys
import numpy as np
from offdiagonal_probe import rows as offrows
from crossmenu_probe import rows as crossrows
from menutax_probe import rows as taxrows
from alignedtax_probe import rows as alignrows
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).parent
ns={};src=(ROOT/'tests/audits/customer_attraction_five_indexed.py').read_text();exec(compile(src.split('from pathlib import Path')[0],'<canonical row definitions>','exec'),ns)
primal=json.loads((ROOT/'evidence/certificates/customer_attraction/five_player_indexed_bound.json').read_text())['primal'];atoms=primal['atoms'];cols=[]
for a in atoms:
 v=ns['evaluate'](list(map(int,a['bits'])),[a['AB_hist'],a['AE_hist'],a['second_hist']],a['menus_lh'],True);v.update(offrows(a));v.update(crossrows(a));v.update(taxrows(a));cols.append(v)
names=list(cols[0]);G=[[c[n] for c in cols] for n in names];w=[int(any(map(int,a['bits'][:5]))) for a in atoms];o=[int(any(a['AB_hist'][4:])) for a in atoms]
point=json.loads((HERE/'reopt_tax.json').read_text())['point'];S=[i for i,x in enumerate(point) if x>1e-8];active=[row for row in G if abs(sum(float(a)*b for a,b in zip(row,point)))<1e-7]
basis={}
for row,rhs in [(w,F(1))]+[(r,F(0)) for r in active]:
 v=[F(row[i]) for i in S]+[rhs]
 for pivot,b in sorted(basis.items()):
  x=v[pivot]
  if x:v=[a-x*c for a,c in zip(v,b)]
 pivot=next((i for i,x in enumerate(v[:-1]) if x),None)
 if pivot is None:
  assert v[-1]==0;continue
 x=v[pivot];basis[pivot]=[a/x for a in v]
 if len(basis)==len(S):break
assert len(basis)==len(S)
x=[F(0)]*len(S)
for pivot,b in sorted(basis.items(),reverse=True):x[pivot]=b[-1]-sum(b[i]*x[i] for i in range(pivot+1,len(S)))
r=[F(0)]*len(atoms)
for i,a in zip(S,x):r[i]=a
assert min(r)>=0 and sum(a*b for a,b in zip(w,r))==1
slack={n:sum(col[n]*x for col,x in zip(cols,r)) for n in names};assert min(slack.values())>=0
value=sum(a*b for a,b in zip(o,r));assert value>2
extra={}
for a,x in zip(atoms,r):
 for n,v in alignrows(a).items():extra[n]=extra.get(n,F())+x*v
record={'scope':'exact LP necessary-condition obstruction; no SPE completion claimed','rows':len(names),'atoms':len(atoms),'positive_atoms':sum(x>0 for x in r),'objective':str(value),'gap_above_two':str(value-2),'point':[str(x) for x in r],'all_rows_verified_exactly':True,'aligned_tax_violations':{n:str(v) for n,v in extra.items() if v<0}}
(HERE/'unaligned_exact_obstruction.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({k:v for k,v in record.items() if k!='point'},indent=2))
