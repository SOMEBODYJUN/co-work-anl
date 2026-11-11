"""Jointly price indexed Ti branch graph and projected actual-fourth->B branch.

Every added row holds for the same original SPE, so this is a valid joint
necessary graph. A low-W point is not a game or SPE. A support infeasibility
would only concern the fixed 16 old histograms.
"""
from pathlib import Path
from fractions import Fraction as F
import json,sys,time
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
TARGET='combined_branch_local_v2' if '--local-v2' in sys.argv else ('combined_branch_local' if '--new-local' in sys.argv else ('combined_branch_latest' if '--latest' in sys.argv else 'combined_branch_master'))
for flag in ('--priced','--optimum','--old-query-cuts','--mixed-pair'):
 if flag not in sys.argv:sys.argv.append(flag)
sys.path[:0]=[str(HERE.parent/'research_3'),str(HERE.parent/'research_2')]
import all_reply_actual_floors as floors
import continuous_old_query_cuts as cont
import tail3_B_projection as branch
import full_new_reply_closure as cl

def build():
 cols,names,m,obj,norm=floors.build()
 cuts=json.loads((HERE.parent/'research_3/continuous_old_query_cuts.json').read_text())['selected']
 for c in cuts:names.append('continuous-old-query:'+str(c['cut']));m.append(cont.row(cols,c['cut']))
 tt=branch.table();row=[F()]*len(cols)
 for j,c in enumerate(cols):
  if c['kind']=='hist':row[j]=tt[c['actual_bits'],c['d']]
 names.append('actual-fourth-forced-actual-B-projection');m.append(row)
 if '--latest' in sys.argv:
  import terminal_portfolio_cuts as portfolio
  for cut in json.loads((HERE.parent/'research_3/continuous_refinement_cuts.json').read_text())['cuts']:
   names.append('continuous-refinement:'+str(cut));m.append(cont.row(cols,cut))
  for file in ('terminal_portfolio_refinement_cuts.json','terminal_capacity_refinement_cuts.json'):
   for cut in json.loads((HERE.parent/'research_3'/file).read_text())['cuts']:
    names.append('terminal-portfolio:'+str(cut));m.append(portfolio.row(cols,cut))
  for cut in json.loads((HERE.parent/'research_2/early_B_projection_certificate.json').read_text())['rows']:
   table={(z['actual_bits'],z['d']):F(z['psi']) for z in cut['table']};rr=[F()]*len(cols);rr[0]=F(cut['kappa'])
   for j,c in enumerate(cols):
    if c['kind']=='hist':rr[j]=table[c['actual_bits'],c['d']]
   names.append('early-actual-B-projection:'+str(cut['source']));m.append(rr)
 if '--new-local' in sys.argv or '--local-v2' in sys.argv:
  import nested_reply_projection as local
  import early_reply_requery_cuts as requery
  frozen=json.loads((HERE/('joint_local_v2_cuts.json' if '--local-v2' in sys.argv else 'joint_local_cuts.json')).read_text())
  for cut in frozen['nested']:
   names.append('actual4-force-new-reply-local:'+str(cut));m.append(local.row(cols,cut))
  for cut in frozen['requery']:
   names.append('same-source-reply-requery:'+str(cut));m.append(requery.row(cols,cut))
  for cut in frozen.get('portfolio',[]):
   names.append('terminal-portfolio-master:'+str(cut));m.append(portfolio.row(cols,cut))
 return cols,names,m,obj,norm

def main():
 start=time.time();cols,names,m,obj,norm=build();print('built',len(m),'rows',len(cols),'columns',time.time()-start,flush=True)
 if '--verify' in sys.argv:
  p=json.loads((HERE/(TARGET+'_exact.json')).read_text());ys=[F(c['weight']) for c in p['columns']]
  assert min(ys)>=0 and sum(v*y for v,y in zip(norm,ys))==1
  slacks=[sum(v*y for v,y in zip(row,ys)) for row in m];assert min(slacks)>=0
  w=sum(v*y for v,y in zip(obj,ys));assert w==F(p['W']) and w<F(1,2)
  print({'rows':len(m),'minimum_slack':str(min(slacks)),'W':str(w)});return
 a=np.array([[float(v) for v in row] for row in m]);scale=np.max(abs(a),axis=1);scale[scale==0]=1
 sol=linprog([float(x) for x in obj],A_ub=-a/scale[:,None],b_ub=np.zeros(len(m)),A_eq=[[float(x) for x in norm]],b_eq=[1],bounds=(0,None),method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
 report={'scope':'joint Ti-indexed graph and actual-B projected branch, fixed16hist support only; not SPE or full-domain bound','success':bool(sol.success),'status':sol.message,'W':sol.fun,'rows':len(m),'columns':len(cols),'seconds':time.time()-start};print(json.dumps(report,indent=2),flush=True)
 if sol.success and sol.fun<.5:
  er=cl.exact_point(cols,names,m,obj,norm,sol.x);er['scope']='exact jointly feasible necessary graph with actual-fourth-B branch; not SPE or game'
  (HERE/(TARGET+'_exact.json')).write_text(json.dumps(er,indent=2)+'\n');report['exact_verified']=True
 (HERE/(TARGET+'_status.json')).write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
