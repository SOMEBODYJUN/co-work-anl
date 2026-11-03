"""Exploratory restrictions of full strategy dual; floating results are not certificates."""
from pathlib import Path
import sys,json,itertools,importlib.util
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
spec=importlib.util.spec_from_file_location('lp',ROOT/'tests/audits/customer_attraction_strategy_lp.py')
mod=importlib.util.module_from_spec(spec);sys.modules['lp']=mod;spec.loader.exec_module(mod)
x=json.load(open(ROOT/'evidence/runs/2026-10-09/customer_attraction_strategy_lp_m4p5_certified.json'))
best={};fails={}
for ci,pr in enumerate(x['cone_proofs']):
 C=mod.StrategyCone(5,4,{tuple(v['history']):v['action'] for v in pr['actions']})
 for J in itertools.combinations(range(5),4):
  obj=np.asarray(mod.coverage_row(5,J),float)
  for mode in ['permutation_prefix','full_uniform']:
   rows=[]
   for h,act in C.actions.items():
    if mode=='permutation_prefix':
     if len(set(h))!=len(h) or not set(h)<=set(J):continue
     A=set(J)-set(h)
    else:A=J
    u=np.asarray(mod.payoff_row(5,C.terminals[h],act),float)
    row=u-sum((np.asarray(mod.payoff_row(5,C.terminals[h+(a,)],a),float) for a in A))/len(A)
    rows.append(row)
   res=linprog(-obj,A_ub=-np.asarray(rows),b_ub=np.zeros(len(rows)),A_eq=[np.asarray(C.welfare,float)],b_eq=[1],bounds=(0,None),method='highs')
   val=-res.fun if res.success else float('inf')
   if val>best.get(mode,0):best[mode]=val;print(mode,ci,J,val,flush=True)
   if val>2.00001 and mode not in fails:
    fails[mode]={'cone_index':ci,'J':J,'value':val,'status':res.message,'point':res.x.tolist() if res.success else None,'actions':pr['actions']}
 if len(fails)==2:break
out={'scope':'floating restricted-template probes only, not SPE counterexamples','best':best,'failures':fails}
Path(__file__).with_name('average_probe.json').write_text(json.dumps(out,indent=2))
