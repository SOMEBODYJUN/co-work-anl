"""Probe the previously unexcluded weaker cap W/(n-1/2) for root stationary Q.
Every accepted candidate is exact inside a full SPE strategy cone.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import importlib.util,json,sys
import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location('cone_audit',ROOT/'tests/audits/customer_attraction_strategy_lp.py')
ca=importlib.util.module_from_spec(spec);sys.modules[spec.name]=ca;spec.loader.exec_module(ca)

def analyze(actions,n,p,certname):
 cone=ca.StrategyCone(p,n,actions)
 tails=[]
 for a in range(p):
  q=list(cone.terminals[(a,)]);q[a]-=1;tails.append(tuple(q))
 K=tuple(tuple(F(q[b],n-1) for b in range(p)) for q in tails)
 eq=[[K[a][b]-F(a==b) for a in range(p)]+[F()] for b in range(p)]+[[F(1)]*p+[F(1)]]
 pivots=[];r=0
 for col in range(p):
  k=next((k for k in range(r,len(eq)) if eq[k][col]),None)
  if k is None:continue
  eq[r],eq[k]=eq[k],eq[r];z=eq[r][col];eq[r]=[v/z for v in eq[r]]
  for k in range(len(eq)):
   if k!=r:
    z=eq[k][col];eq[k]=[x-z*y for x,y in zip(eq[k],eq[r])]
  pivots.append(col);r+=1
 if len(pivots)<p:return {'status':'stationary_not_unique','file':certname}
 pi=tuple(eq[pivots.index(j)][-1] for j in range(p));assert min(pi)>=0
 reports=[]
 for t in range(p):
  row=[F() for _ in range((1<<p)-1)]
  for a,q0 in enumerate(tails):
   q=list(q0);q[t]+=1;f=ca.payoff_row(p,tuple(q),t)
   row=[x+pi[a]*y for x,y in zip(row,f)]
  lp=linprog(-np.array(row,dtype=float),A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),A_eq=np.array([cone.welfare],dtype=float),b_eq=[1],bounds=(0,None),method='highs')
  if not lp.success:continue
  w=tuple(F(float(x)).limit_denominator(10**7) for x in lp.x)
  if not(cone.verify(w) and ca.dot(cone.welfare,w)==1):w=cone.recover_vertex(lp.x)
  exact=w is not None and cone.verify(w) and ca.dot(cone.welfare,w)==1
  value=ca.dot(row,w) if exact else F(float(-lp.fun)).limit_denominator(10**7)
  rec={'query':t,'value':str(value),'float':-lp.fun,'exact':exact}
  if exact and (F(2*n-1,2)*value>1):
   rec['violates_weaker_cap']=True;rec['weights']={mask:str(v) for mask,v in enumerate(w,1) if v}
   rec['pi']=list(map(str,pi));rec['root']=cone.root
  reports.append(rec)
 return dict(file=certname,players=n,topics=p,pi=list(map(str,pi)),reports=reports)

def run(certname,n,p):
 dat=json.loads((ROOT/'evidence/certificates/customer_attraction'/certname).read_text());dat=dat.get('strategy',dat)
 actions={tuple(e['history']):e['action'] for e in dat['actions']}
 return analyze(actions,n,p,certname)

if __name__=='__main__':
 report=[run(f,3,6) for f in ['root_stationary_kernel.json','individual_security_failure.json','aggregate_theta_failure.json']]
 Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
