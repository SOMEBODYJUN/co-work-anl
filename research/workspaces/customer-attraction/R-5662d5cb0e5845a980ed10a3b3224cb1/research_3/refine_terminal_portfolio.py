"""Adaptive shared-terminal-portfolio cuts after the saved continuous family."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,time
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
for flag in ('--priced','--optimum','--old-query-cuts','--mixed-pair'):
 if flag not in sys.argv:sys.argv.append(flag)
import all_reply_actual_floors as base
import continuous_old_query_cuts as cc
import terminal_portfolio_cuts as pc

def main():
 tag='terminal_capacity_refinement' if '--capacity' in sys.argv else 'terminal_portfolio_refinement'
 start=time.time();cols,names,m,obj,norm=base.build()
 for cut in json.loads((HERE/'continuous_refinement_cuts.json').read_text())['cuts']:
  names.append('continuous-old-query:'+str(cut));m.append(cc.row(cols,cut))
 if '--capacity' in sys.argv:
  for cut in json.loads((HERE/'terminal_portfolio_refinement_cuts.json').read_text())['cuts']:
   names.append('prior-terminal-query-portfolio:'+str(cut));m.append(pc.row(cols,cut))
 base_count=len(m)
 if '--verify' in sys.argv:
  cuts=json.loads((HERE/(tag+'_cuts.json')).read_text())['cuts']
  for cut in cuts:names.append('terminal-query-portfolio:'+str(cut));m.append(pc.row(cols,cut))
  d=json.loads((HERE/(tag+'_exact.json')).read_text());ys=[F(c['weight']) for c in d['columns']]
  assert len(ys)==len(cols) and min(ys)>=0 and sum(x*y for x,y in zip(norm,ys))==1
  slacks=[sum(x*y for x,y in zip(r,ys)) for r in m];assert min(slacks)>=0
  w=sum(x*y for x,y in zip(obj,ys));assert w==F(d['W']) and w<F(1,2)
  print({'rows':len(m),'base_rows':base_count,'cut_rows':len(cuts),'min_slack':str(min(slacks)),'W':str(w)});return
 print('built',len(m),len(cols),time.time()-start,flush=True)
 aa=np.array([[float(x) for x in r] for r in m]);cuts=[];seen=set();trace=[];last=None
 rounds=6
 for it in range(rounds+1):
  sc=np.max(abs(aa),axis=1);sc[sc==0]=1
  sol=linprog([float(x) for x in obj],A_ub=-aa/sc[:,None],b_ub=np.zeros(len(m)),A_eq=[[float(x) for x in norm]],b_eq=[1],bounds=(0,None),method='highs',options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
  assert sol.success,sol.message;last=sol;ev={'iteration':it,'W':sol.fun,'rows':len(m),'seconds':time.time()-start};trace.append(ev);print(ev,flush=True)
  if it==rounds:break
  found,nlp=pc.find_cuts(cols,sol.x);fresh=[]
  for v,c,r in found:
   key=json.dumps(c,sort_keys=True)
   if key not in seen:seen.add(key);fresh.append((v,c,r))
  ev.update({'negative_structures':len(found),'fresh_cuts':len(fresh),'minimum_slack':found[0][0] if found else 0});print({k:v for k,v in ev.items() if k not in ('W','rows','seconds')},flush=True)
  if not fresh:break
  for v,c,r in fresh:cuts.append(c);names.append('terminal-query-portfolio:'+str(c));m.append(r)
  aa=np.vstack([aa,np.array([[float(v) for v in r] for _,_,r in fresh])])
 (HERE/(tag+'_trace.json')).write_text(json.dumps({'scope':'finite necessary-graph separation, not SPE or full-domain bound','trace':trace},indent=2)+'\n')
 (HERE/(tag+'_cuts.json')).write_text(json.dumps({'scope':'legal shared terminal-IC projections with nonnegative rational weights','cuts':cuts},indent=2)+'\n')
 exact=base.cross.cl.exact_point(cols,names,m,obj,norm,last.x);exact.update({'scope':'exact necessary point after terminal-query portfolio cuts; not SPE or game','base_rows':base_count,'terminal_portfolio_cut_rows':len(cuts)})
 (HERE/(tag+'_exact.json')).write_text(json.dumps(exact,indent=2)+'\n');print({'exact_W':exact['W'],'cut_rows':len(cuts),'seconds':time.time()-start},flush=True)
if __name__=='__main__':main()
