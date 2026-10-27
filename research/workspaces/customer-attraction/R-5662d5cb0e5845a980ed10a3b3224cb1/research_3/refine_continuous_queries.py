"""Adaptive continuous-price separation on the fixed 16-histogram graph.

This is a necessary-conditions diagnostic, never a complete SPE computation.
"""
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

def main():
 start=time.time();cols,names,m,obj,norm=base.build();base_count=len(m)
 if '--verify' in sys.argv:
  cuts=json.loads((HERE/'continuous_refinement_cuts.json').read_text())['cuts']
  for cut in cuts:names.append('continuous-old-query:'+str(cut));m.append(cc.row(cols,cut))
  d=json.loads((HERE/'continuous_refinement_exact.json').read_text());ys=[F(c['weight']) for c in d['columns']]
  assert len(ys)==len(cols) and min(ys)>=0 and sum(x*y for x,y in zip(norm,ys))==1
  slacks=[sum(x*y for x,y in zip(r,ys)) for r in m];assert min(slacks)>=0
  w=sum(x*y for x,y in zip(obj,ys));assert w==F(d['W']) and w<F(1,2)
  print({'rows':len(m),'base_rows':base_count,'cut_rows':len(cuts),'min_slack':str(min(slacks)),'W':str(w)});return
 print('built',len(m),len(cols),time.time()-start,flush=True)
 aa=np.array([[float(x) for x in r] for r in m]);cuts=[];seen=set();trace=[];last=None
 rounds=6
 if '--rounds' in sys.argv:rounds=int(sys.argv[sys.argv.index('--rounds')+1])
 for it in range(rounds+1):
  sc=np.max(abs(aa),axis=1);sc[sc==0]=1
  sol=linprog([float(x) for x in obj],A_ub=-aa/sc[:,None],b_ub=np.zeros(len(m)),A_eq=[[float(x) for x in norm]],b_eq=[1],bounds=(0,None),method='highs',options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
  assert sol.success,sol.message;last=sol
  event={'iteration':it,'W':sol.fun,'rows':len(m),'seconds':time.time()-start};trace.append(event);print(event,flush=True)
  if it==rounds:break
  found,nlp=cc.find_cuts(cols,sol.x,32);fresh=[(v,c,r) for v,c,r in found if tuple(c) not in seen]
  event.update({'negative_structures_selected':len(found),'fresh_cuts':len(fresh),'min_priced_slack':found[0][0] if found else 0})
  print({k:v for k,v in event.items() if k not in ('W','rows','seconds')},flush=True)
  if not fresh:break
  for val,cut,r in fresh:seen.add(tuple(cut));cuts.append(cut);names.append('continuous-old-query:'+str(cut));m.append(r)
  aa=np.vstack([aa,np.array([[float(v) for v in r] for _,_,r in fresh])])
 (HERE/'continuous_refinement_trace.json').write_text(json.dumps({'scope':'fixed 16-histogram support, finite iterative separation; not SPE or full-domain bound','trace':trace},indent=2)+'\n')
 (HERE/'continuous_refinement_cuts.json').write_text(json.dumps({'scope':'each rational cut is a valid priced-hidden-reply projection','cuts':cuts},indent=2)+'\n')
 exact=base.cross.cl.exact_point(cols,names,m,obj,norm,last.x);exact['scope']='exact point in finite fixed-support graph after continuous query cuts; not SPE or game';exact['base_rows']=base_count;exact['continuous_cut_rows']=len(cuts)
 (HERE/'continuous_refinement_exact.json').write_text(json.dumps(exact,indent=2)+'\n')
 print({'exact_W':exact['W'],'cut_rows':len(cuts),'seconds':time.time()-start},flush=True)
if __name__=='__main__':main()
