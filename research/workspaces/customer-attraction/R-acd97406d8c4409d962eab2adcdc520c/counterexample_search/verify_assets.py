"""Fraction-only replay of the new 527-row feasible point; no LP solver."""
from pathlib import Path
from fractions import Fraction as F
import json
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent
namespace={};source=(ROOT/'tests/audits/customer_attraction_five_indexed.py').read_text()
exec(compile(source.split('from pathlib import Path')[0],'<canonical indexed row definitions>','exec'),namespace)
p=json.loads((ROOT/'evidence/certificates/customer_attraction/five_player_indexed_bound.json').read_text())['primal'];atoms=p['atoms'];report=json.loads((HERE/'augment_fixed_support.json').read_text())
point=list(map(F,report['exact_primal_point']));assert len(point)==len(atoms)==64 and all(x>=0 for x in point)
cols=[];bits=[]
for atom in atoms:
 b=list(map(int,atom['bits']));bits.append(b);cols.append(namespace['evaluate'](b,[atom['AB_hist'],atom['AE_hist'],atom['second_hist']],atom['menus_lh'],True))
rows=[[col[n] for col in cols] for n in cols[0]];assert len(rows)==437
for a in range(10):
 for r in range(10):
  if a==r:continue
  rows.append([57*(5*(F(b[0],sum(b[:5])) if b[0] else 0)-b[a])-2*(b[r]-b[a])-8*b[r]*(1-b[a]) for b in bits])
slacks=[sum(x*y for x,y in zip(row,point)) for row in rows]
assert len(slacks)==527 and min(slacks)>=0
w=sum(x*int(sum(b[:5])>0) for x,b in zip(point,bits));o=sum(x*int(any(atom['AB_hist'][4:])) for x,atom in zip(point,atoms))
assert w==1 and o==F(report['exact_primal_objective']) and o>2
print(json.dumps({'verified_nonnegative_primal':True,'rows':len(rows),'zero_slacks':sum(x==0 for x in slacks),'minimum_slack':str(min(slacks)),'welfare':str(w),'comparison_cover':str(o),'gap_above_two':str(o-2)},indent=2))
