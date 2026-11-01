"""Discovery only: optimize fixed rational queries in a full SPE cone.
Every accepted witness is checked over Fraction; no universal bound follows.
"""
from pathlib import Path
import sys,json
from fractions import Fraction as F
from itertools import combinations
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'tests/audits'))
from customer_attraction_strategy_lp import StrategyCone,dot,integer_clones
SOURCE=ROOT/'research/workspaces/customer-attraction/R-5c4f6385eec046eb9a20052facacba11/background/global_actual_prefix_complete_spe.json'
s=json.loads(SOURCE.read_text());k=len(s['terminal_counts']);m=sum(s['terminal_counts']);pol={tuple(z['history']):z['action']for z in s['actions']};cone=StrategyCone(k,m,pol);n=(1<<k)-1
h=();actual=[]
while len(h)<m:actual.append(pol[h]);h+=pol[h],

def gp_row(q,p):
 return tuple(sum((p[a]for a in range(k)if mask>>a&1),F())/ (1+sum(q[a]for a in range(k)if mask>>a&1))for mask in range(1,1<<k))

queries=[]
for z in range(1,1<<k):
 sz=z.bit_count();queries.append(tuple(F(int(z>>a&1),sz)for a in range(k)))
best=[0]*m;witness=[]
for cnt,p in enumerate(queries):
 grows=[[gp_row(cone.terminals[tuple(actual[:i])+(a,)],p)for a in range(k)]for i in range(m)]
 rows=[tuple(-x for x in row)+(F(),)*m for row in cone.rows]
 for i in range(m):
  for grow in grows[i]:rows.append(tuple(-x for x in grow)+tuple(F(j==i)for j in range(m)))
 A=np.array(rows,dtype=float)
 for i in range(m):
  obj=np.zeros(n+m);obj[n+i]=-1
  res=linprog(obj,A_ub=A,b_ub=np.zeros(len(A)),A_eq=[list(cone.welfare)+[0]*m],b_eq=[1],bounds=[(0,None)]*n+[(None,None)]*m,method='highs')
  if not res.success:continue
  v=-res.fun
  if v>best[i]+1e-8:
   best[i]=v;print(cnt,'pos',i,'value',v,'p',[str(x)for x in p],flush=True)
  if v>1/m+1e-8:
   w=tuple(F(float(x)).limit_denominator(10**6)for x in res.x[:n])
   if cone.verify(w) and dot(cone.welfare,w)==1:
    psi=tuple(min(dot(row,w)for row in grows[j])for j in range(m))
    if psi[i]>F(1,m):
     record={'source':str(SOURCE.relative_to(ROOT)),'status':'exact full SPE cone query witness','players':m,'topics':k,'query':[str(x)for x in p],'weights':[str(x)for x in w],'psi':[str(x)for x in psi],'W':'1','positive_position':i}
     witness.append(record);print('EXACT',record,flush=True)
print('BEST',best)
Path(__file__).with_suffix('.json').write_text(json.dumps({'status':'fixed-policy finite discovery only','queries':len(queries),'best_floating':best,'witnesses':witness},indent=2))
