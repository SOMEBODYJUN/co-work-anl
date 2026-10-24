"""Finite diagnostic of a genuinely general proposed population comparison.

Proposed claim: every m-player full SPE has W/m at least the minimum average
welfare of a symmetric static CCE with m+1 players in the same catalog.
This is not assumed true, and finite passes are not evidence of a theorem.
"""
import json,pathlib
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
ROOT=pathlib.Path(__file__).resolve().parents[5];OUT=pathlib.Path(__file__).resolve().parent

def counts(k,n):
 if k==1:yield(n,);return
 for a in range(n+1):
  for t in counts(k-1,n-a):yield(a,)+t
rows=[]
for ip in sorted((ROOT/'examples/customer_attraction').glob('*.json')):
 cp=ROOT/'evidence/certificates/customer_attraction'/ip.name
 if not cp.exists():continue
 obj=json.loads(ip.read_text());cert=json.loads(cp.read_text());strategy=cert.get('strategy',{}) if isinstance(cert,dict) else {}
 if not isinstance(strategy,dict) or not strategy.get('actions'):continue
 acts={tuple(r['history']):r['action']for r in strategy['actions']};m=obj['players'];k=len(obj['topics']);n=m+1
 if len(acts)!=sum(k**i for i in range(m)):continue
 h=()
 while len(h)<m:h=h+(acts[h],)
 cs=[(frozenset(c['topics']),c.get('multiplicity',1))for c in obj['customers']]
 W=sum(w for c,w in cs if any(a in c for a in h));qs=list(counts(k,n))
 if len(qs)>15000:continue
 wc=[];reg=[]
 for q in qs:
  loads=[sum(q[a]for a in c)for c,w in cs];wq=sum(w for (c,w),v in zip(cs,loads)if v)
  R=[sum((F(w*(n+1),v+1)if v else F(w*n) for (c,w),v in zip(cs,loads)if a in c),F())for a in range(k)]
  wc.append(wq);reg.append([float(v-wq)for v in R])
 res=linprog(np.array(wc,dtype=float)/n,A_ub=np.array(reg).T,b_ub=np.zeros(k),A_eq=np.ones((1,len(qs))),b_eq=[1],bounds=(0,None),method='highs')
 row={'instance':ip.name,'players':m,'new_players':n,'SPE_W':W,'SPE_average':W/m,'profiles':len(qs),'CCE_min_average_float':res.fun if res.success else None,'claim_gap_float':(W/m-res.fun)if res.success else None}
 if res.success:row['support']=[{'counts':q,'probability_float':v,'W':w}for q,v,w in zip(qs,res.x,wc)if v>1e-8]
 rows.append(row);print(row)
(OUT/'population_cce_check.json').write_text(json.dumps({'status':'finite floating LP diagnostic only','claim':'min CCE_(m+1) W/(m+1) <= SPE_m W/m','rows':rows},indent=2)+'\n')
