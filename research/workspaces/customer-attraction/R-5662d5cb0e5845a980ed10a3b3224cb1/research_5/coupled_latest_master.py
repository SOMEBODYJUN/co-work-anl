"""All current local projected rows plus explicit actual-B joint branch states."""
from pathlib import Path
from fractions import Fraction as F
import json,sys,time
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
for flag in ('--latest','--local-v2'):
 if flag not in sys.argv:sys.argv.append(flag)
sys.path.insert(0,str(HERE.parent/'research_2'))
import coupled_B_branch_master as coupled
import full_new_reply_closure as cl

def build():return coupled.build()
def main():
 start=time.time();cols,names,m,obj,norm=build();print('built',len(m),'rows',len(cols),'cols',time.time()-start,flush=True)
 if '--verify' in sys.argv:
  er=json.loads((HERE/'coupled_latest_exact.json').read_text());ys=[F(c['weight']) for c in er['columns']]
  assert min(ys)>=0 and sum(v*y for v,y in zip(norm,ys))==1
  slacks=[sum(v*y for v,y in zip(row,ys)) for row in m];assert min(slacks)>=0
  w=sum(v*y for v,y in zip(obj,ys));assert w==F(er['W']) and w<F(1,2)
  print({'rows':len(m),'minimum_slack':str(min(slacks)),'W':str(w)});return
 a=np.array([[float(v) for v in row] for row in m]);sc=np.max(abs(a),axis=1);sc[sc==0]=1
 sol=linprog([float(v) for v in obj],A_ub=-a/sc[:,None],b_ub=np.zeros(len(m)),A_eq=[[float(v) for v in norm]],b_eq=[1],bounds=(0,None),method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
 report={'scope':'joint all current local rows plus actualB explicit conditional states; fixed16hist necessary graph only, not SPE','success':bool(sol.success),'status':sol.message,'W':sol.fun,'rows':len(m),'columns':len(cols),'seconds':time.time()-start};print(json.dumps(report,indent=2),flush=True)
 if sol.success and sol.fun<.5:
  er=cl.exact_point(cols,names,m,obj,norm,sol.x);er['scope']=report['scope'];(HERE/'coupled_latest_exact.json').write_text(json.dumps(er,indent=2)+'\n');report['exact_verified']=True
 (HERE/'coupled_latest_status.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
