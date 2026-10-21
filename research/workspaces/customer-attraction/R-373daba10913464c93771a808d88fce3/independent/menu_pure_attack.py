from pathlib import Path
import sys,json
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
R=Path(__file__).resolve().parents[5]
sys.path[:0]=[str(R),str(R/'tests/audits')]
from customer_attraction_strategy_lp import StrategyCone,payoff_row,dot,integer_clones,instance_from_clones,independently_verify
from customer_attraction import Instance, StrategyCertificate

records=[]
def attack(name,p,m,actions):
 cone=StrategyCone(p,m,actions);k=(1<<p)-1
 menus=[]
 for a in range(p):
  q=list(cone.terminals[(a,)]);q[a]-=1;menus.append(tuple(q))
 best=None
 for query in range(p):
  rows=[]
  for q in menus:
   x=list(q);x[query]+=1;rows.append(payoff_row(p,tuple(x),query))
  mat=np.zeros((len(cone.rows)+p,k+1));mat[:len(cone.rows),:k]=-cone.matrix
  mat[len(cone.rows):,:k]=-np.array(rows,float);mat[len(cone.rows):,-1]=1
  obj=np.zeros(k+1);obj[-1]=-1
  eq=np.zeros((1,k+1));eq[0,:k]=np.array(cone.welfare,float)
  res=linprog(obj,A_ub=mat,b_ub=np.zeros(len(mat)),A_eq=eq,b_eq=[1],bounds=(0,None),method='highs')
  if not res.success:continue
  w=tuple(F(float(x)).limit_denominator(10**6) for x in res.x[:k])
  if not cone.verify(w) or dot(cone.welfare,w)!=1:continue
  val=min(dot(row,w) for row in rows)
  if best is None or val>best['value']:
   best={'name':name,'p':p,'m':m,'query':query,'value':val,'weights':w,'actions':actions}
 if best:
  print(name,p,m,'purecap/W',str(best['value']),'weakthreshold',str(F(2,2*m-1)),flush=True)
  records.append(best)
  if best['value']>F(2,2*m-1):
   clones=integer_clones(best['weights']);assert independently_verify(cone,clones)
   inst=instance_from_clones(p,m,clones)
   out={**best,'value':str(best['value']),'weights':clones,'actions':[{'history':h,'action':a} for h,a in actions.items()]}
   Path(__file__).with_name('weak_menu_violation.json').write_text(json.dumps(out,indent=2))
   print('FOUND WEAK COUNTEREXAMPLE',flush=True);raise SystemExit

small=json.loads((Path(__file__).parent/'root_menu_review/audit.json').read_text())
attack('root_candidate',3,3,{tuple(r['history']):r['chosen'] for r in small['rows']})
for p in sorted((R/'examples/customer_attraction').glob('*.json')):
 cert=R/'evidence/certificates/customer_attraction'/p.name
 if not cert.exists():continue
 data=json.loads(cert.read_text());data=data.get('strategy',data)
 if 'actions' not in data or 'terminal_counts' not in data:continue
 inst=Instance.from_dict(json.loads(p.read_text()))
 if inst.topic_count>7 or inst.players>4:continue
 cert=StrategyCertificate.from_dict(data)
 attack(p.stem,inst.topic_count,inst.players,dict(cert.actions))
print('DONE',len(records),flush=True)
