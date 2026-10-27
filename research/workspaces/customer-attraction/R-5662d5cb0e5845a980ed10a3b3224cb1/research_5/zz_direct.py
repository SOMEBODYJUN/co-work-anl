"""Exact maximal Z->Z slacks at fixed 3889-point R and (R,Z) moments."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,sys
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'work.py').exists())
OLD=ROOT/'research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra'
sys.path.insert(0,str(OLD))
import full_new_reply_closure as cl
import new_reply_budget as nr
x=json.loads((OLD/'attractive_nested_exact.json').read_text());cols=x['columns'];byhist={};hi=None
for c in cols:
 if c['kind']=='hist':hi=cols.index(c);byhist[hi]={'data':c,'groups':{}}
 if c['kind']=='joint-reply':
  f,d,wi,wj=c['group'];g=(f,d,tuple(wi),tuple(wj));byhist[hi]['groups'].setdefault(g,{})[tuple(c['state'])]=F(c['weight'])
slacks={(f,g,p):F() for f,g,p in product(range(2),range(2),cl.P4)}
for hi,dct in byhist.items():
 c=dct['data'];hm=F(c['weight']);gs=dct['groups']
 if not hm:continue
 a=tuple(map(int,c['actual_bits']));pa=sum(a[:4]);D=(pa+1)*(pa+2)
 words=[w for w,n in zip(nr.PAT,c['hist']) for _ in range(n)]
 edges=[(f,i,j) for f,i,j in product(range(2),range(6),range(6)) if f or i!=j]
 def group(e):return e[0],int(e[1]==e[2]),words[e[1]],words[e[2]]
 def moments(g):
  s=gs[g];return s[1,0]+s[1,1],s[0,1]+s[1,1],s[1,1],s[0,1]
 for e in edges:
  f,i,j=e;ge=group(e);re,ze,rze,_=moments(ge)
  for ee in edges:
   g,k,l=ee;rf,zf,rzf,ozf=moments(group(ee))
   overlap=min(rzf,re) if re<=rf else rzf+min(ozf,re-rf)
   v=F(ze-zf,pa+1)+F(overlap-rze,D)
   slacks[f,g,cl.partition((i,j,k,l))]+=v
report={'scope':'exact maximum of every Z->Z row for fixed 3889 hist/R/(R,Z) moments using common-threshold R and blockwise lowest Z; not full-domain proof, not SPE','W':x['W'],'rows':len(slacks),'minimum_slack':str(min(slacks.values())),'negative_rows':[{'row':str(k),'slack':str(v)} for k,v in slacks.items() if v<0]}
(HERE/'zz_direct_status.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
