from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
# New known-input arithmetic reconstruction from the full primary Markdown only.
# Does not import any original program, solver, model, verifier, or old output.
second=(1,2,3,4,2)
last=((2,2,2,2,2),(2,2,3,2,2),(2,3,3,2,3),(2,2,2,2,2),(2,2,3,2,2))
clients=[]
for mask,n in [((0,),3),((1,),4),((2,3),6),((2,4),6),((0,3,4),2),((1,3,4),2)]:
 clients += [frozenset(mask)]*n
assert len(clients)==23
assert all(last[a][b]==last[b][a] for a,b in product(range(5),repeat=2))
def action(h):return 0 if not h else second[h[0]] if len(h)==1 else last[h[0]][h[1]]
def finish(h):
 h=tuple(h)
 while len(h)<3:h+=action(h),
 return h
def pay(z,i):
 return sum((F(1,sum(a in x for a in z)) for x in clients if z[i] in x),F())
def cov(z):return sum(any(a in x for a in z) for x in clients)
rows=[];strict=ties=0
for depth in range(3):
 for h in product(range(5),repeat=depth):
  a=action(h);z=finish(h);u=pay(z,depth);vals=[]
  for b in range(5):
   v=pay(finish(h+(b,)),depth);assert u>=v;(strict if False else 0)
   if b!=a:
    strict+=u>v;ties+=u==v
   vals.append(str(v))
  rows.append({'history':list(h),'prescribed':a,'true_final_payoffs':vals,'prescribed_profit':str(u)})
assert len(rows)==31 and strict+ties==124
assert [r['true_final_payoffs'] for r in rows if len(r['history'])==1]==[['5/2','6','6','6','6'],['5','3','9','6','6'],['5','5','5','6','5'],['4','5','5','4','5'],['4','5','6','5','4']]
assert rows[0]['true_final_payoffs']==['5']*5
actual=finish(());assert actual==(0,1,2)
profits=[pay(actual,i) for i in range(3)];W=cov(actual);OPT=max(map(cov,product(range(5),repeat=3)))
assert profits==[5,6,12] and W==OPT==23
assert strict==95 and ties==29
out={'scope':'new known-input direct-unit check of the explicit Markov strategy in the primary MD only; not original joint/MILP strategy or old audit replay; not blind','unit_clients':len(clients),'players':3,'topics':5,'complete_ordered_decision_histories':len(rows),'comparisons_including_self':len(rows)*5,'nonself_comparisons':strict+ties,'strict_nonself':strict,'ties_nonself':ties,'Markov_last_table_symmetry_checked':True,'actual':list(actual),'profits':list(map(str,profits)),'W':W,'OPT':OPT,'OPT_tuple_candidates':125,'inequalities':{'2W':2*W,'(m+1)u_last':4*profits[-1],'u_last_minus_2u_first':profits[-1]-2*profits[0]},'all_rows':rows}
Path('direct-23-report.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='all_rows'},ensure_ascii=False,indent=2))
