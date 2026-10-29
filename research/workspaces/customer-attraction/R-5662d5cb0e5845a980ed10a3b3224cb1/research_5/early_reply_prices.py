"""Earlier actual sources query the same explicit new R_e/Z_e themes.

Queries Q are actual A5, actual A6, or the forced theme itself; hence every
projected coefficient depends only one new membership bit and is affine.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,sys,time
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
TARGET='early_reply_floors' if '--floors' in sys.argv else 'early_reply'
for flag in ('--priced','--optimum'):
 if flag not in sys.argv:sys.argv.append(flag)
import cross_source_graph as cross
import full_new_reply_closure as cl
import new_reply_budget as nr
ORBS=((0,0),(1,0),(1,1))

def build():
 cols,names,m,obj,norm=cross.build()
 if '--floors' in sys.argv:
  sys.path.insert(0,str(HERE.parent/'research_3'))
  import all_reply_actual_floors as floors
  m+=floors.added_rows(cols);names+=['new-reply-floor:'+str(x) for x in floors.KEYS]
 specs=[]
 for i in (3,4):
  k=6-i
  for subject,orb,q,mode,aa,mu in product(('R','Z'),ORBS,(4,5,'self'),('all','last') if k>2 else ('last',),(F(),F(1,4),F(1,2)),(F(),F(1))):
   alpha=(aa,)*(k-1) if mode=='all' else (F(),)*(k-2)+(aa,)
   specs.append((i,subject,orb,q,alpha,mu))
 extra=[[F()]*len(cols) for _ in specs]
 hi=None;groups={}
 for j,c in enumerate(cols):
  if c['kind']=='hist':hi=j;groups[hi]={}
  elif c['kind']=='joint-reply':
   f,d,wi,wj=c['group'];g=(f,d,tuple(wi),tuple(wj));groups[hi].setdefault(g,{})[tuple(c['state'])]=j
 for hi,gs in groups.items():
  c=cols[hi];a=tuple(map(int,c['actual_bits']));s=sum(a);ell=sum(a[:5]);hc={w:n for w,n in zip(nr.PAT,c['hist'])};ui=[nr.share(x,s) for x in a]
  for ri,(i,subject,orb,q,alpha,mu) in enumerate(specs):
   p=sum(a[:i]);beta=(F(),)*len(alpha);baseprofit=ui[i]+sum(alpha)*ui[5]
   q0=0 if q=='self' else a[q];q1=1 if q=='self' else a[q]
   v0=cross.psi(p,ell,0,q0,alpha,beta,mu);v1=cross.psi(p,ell,1,q1,alpha,beta,mu)
   for g,states in gs.items():
    f,diag,wi,wj=g
    if (f,diag)!=orb:continue
    count=hc[wi] if diag else hc[wi]*hc[wj]-(hc[wi] if wi==wj else 0)
    extra[ri][hi]+=count*(baseprofit-v0)
    for (r,z),col in states.items():
     t=r if subject=='R' else z
     if t:extra[ri][col]-=count*(v1-v0)
 return cols,names+['early-reply-priced:'+str(x) for x in specs],m+extra,obj,norm

def main():
 start=time.time();cols,names,m,obj,norm=build();print('built',len(m),'rows',len(cols),'columns',time.time()-start,flush=True)
 if '--verify' in sys.argv:
  x=json.loads((HERE/(TARGET+'_exact.json')).read_text());ys=[F(c['weight']) for c in x['columns']];assert min(ys)>=0 and sum(v*y for v,y in zip(norm,ys))==1
  slacks=[sum(v*y for v,y in zip(row,ys)) for row in m];assert min(slacks)>=0
  w=sum(v*y for v,y in zip(obj,ys));assert w==F(x['W']) and w<F(1,2)
  print(json.dumps({'rows':len(m),'minimum_slack':str(min(slacks)),'W':str(w)},indent=2));return
 a=np.array([[float(x) for x in row] for row in m]);scale=np.max(abs(a),axis=1);scale[scale==0]=1
 sol=linprog([float(x) for x in obj],A_ub=-a/scale[:,None],b_ub=np.zeros(len(m)),A_eq=[[float(x) for x in norm]],b_eq=[1],bounds=(0,None),method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
 report={'scope':'fixed16hist exact graph necessary rows, not complete SPE','success':bool(sol.success),'status':sol.message,'W':sol.fun,'rows':len(m),'columns':len(cols),'seconds':time.time()-start};print(json.dumps(report,indent=2),flush=True)
 if sol.success and sol.fun<.5:
  er=cl.exact_point(cols,names,m,obj,norm,sol.x);er['scope']='exact feasible early actual-source queries to explicit R/Z themes; not SPE or game';er['additional_early_reply_rows']=len(m)-4927
  (HERE/(TARGET+'_exact.json')).write_text(json.dumps(er,indent=2)+'\n');report['exact_verified']=True
 (HERE/(TARGET+'_status.json')).write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
