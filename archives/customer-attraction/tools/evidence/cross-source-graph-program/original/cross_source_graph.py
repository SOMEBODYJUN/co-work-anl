"""Explicit prices/capacities and early source queries for old B_i,C_i labels."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,sys,time
from functools import lru_cache
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'work.py').exists())
sys.path.insert(0,str(ROOT))
import split_basic_graph as sb
from customer_attraction.priced_hidden_reply import projected_by_count
import full_new_reply_closure as cl
import new_reply_budget as nr
@lru_cache(None)
def psi(p,ell,t,q,alpha,beta,mu):return projected_by_count(p,ell,t,q,alpha,beta,mu)

def build():
 cols,names,m,obj,norm=sb.build();hids=[j for j,c in enumerate(cols) if c['kind']=='hist']
 def add(name,coef,k=F()):
  row=[F()]*len(cols);row[0]=k
  for j in hids:row[j]=coef(cols[j])
  names.append(name);m.append(row)
 def datum(c):
  a=tuple(map(int,c['actual_bits']));s=sum(a);words=[w for w,n in zip(nr.PAT,c['hist']) for _ in range(n)];return a,s,words
 for i,q in product(range(6),(1,2)):
  def fun(c,i=i,q=q):
   a,s,words=datum(c);return 6*nr.share(a[i],s)-F(sum(w[q] for w in words),sum(a[:i])+6-i)
  add('actual-floor:'+str((i,q)),fun)
 for q in (1,2):
  add('old-capacity:'+str(q),lambda c,q=q:-F(sum(w[q] for w in datum(c)[2])),F(6))
 # Exact optimum-one-replacement rows, valid only when the T tuple is optimal.
 # This explicitly uses O and d, unlike all other rows that hold for arbitrary tuple.
 if '--optimum' in sys.argv:
  for query in list(range(6))+['B','C']:
   def fun(c,query=query):
    a,s,words=datum(c);dd=c['d'];r=6*a[query] if isinstance(query,int) else sum(w[1 if query=='B' else 2] for w in words)
    return F(6*(dd==1)-r*(dd==1)-6*r*(dd==0))
   add('OPT-one-replace:'+str(query),fun)
 # General priced source projections querying the legal old B_i/C_i labels.
 if '--priced' in sys.argv:
  for i in range(4):
   k=6-i
   for tcol,qcol in product((1,2),range(3)):
    for mode,aa,mu in product(('all','last'),(F(0),F(1,8),F(1,4),F(1,2),F(1)),(F(0),F(1,2),F(1),F(2))):
     alpha=(aa,)*(k-1) if mode=='all' else (F(),)*(k-2)+(aa,)
     beta=(F(),)*(k-1)
     def fun(c,i=i,tcol=tcol,qcol=qcol,alpha=alpha,beta=beta,mu=mu):
      a,s,words=datum(c);p=sum(a[:i]);ell=sum(a[:5])
      return 6*nr.share(a[i],s)+6*sum(alpha)*nr.share(a[5],s)-sum(psi(p,ell,w[tcol],w[qcol],alpha,beta,mu) for w in words)
     add('old-priced:'+str((i,tcol,qcol,mode,aa,mu)),fun)
 return cols,names,m,obj,norm

def main():
 tag='cross_source'+('_priced' if '--priced' in sys.argv else '')+('_optimum' if '--optimum' in sys.argv else '')
 start=time.time();cols,names,m,obj,norm=build();print('built',len(m),'rows',len(cols),'cols',time.time()-start,flush=True)
 if '--verify' in sys.argv:
  report=json.loads((HERE/(tag+'_exact.json')).read_text());ys=[F(c['weight']) for c in report['columns']]
  assert len(ys)==len(cols) and min(ys)>=0 and sum(v*y for v,y in zip(norm,ys))==1
  slacks=[sum(v*y for v,y in zip(row,ys)) for row in m];assert min(slacks)>=0
  w=sum(v*y for v,y in zip(obj,ys));assert w==F(report['W']) and w<F(1,2)
  print(json.dumps({'rows':len(m),'minimum_slack':str(min(slacks)),'W':str(w)},indent=2));return
 a=np.array([[float(x) for x in row] for row in m]);scale=np.max(abs(a),axis=1);scale[scale==0]=1
 sol=linprog([float(x) for x in obj],A_ub=-a/scale[:,None],b_ub=np.zeros(len(m)),A_eq=[[float(x) for x in norm]],b_eq=[1],bounds=(0,None),method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
 tag='cross_source'+('_priced' if '--priced' in sys.argv else '')+('_optimum' if '--optimum' in sys.argv else '')
 report={'scope':'fixed 16 histogram support necessary graph; not full-domain proof or SPE','success':bool(sol.success),'status':sol.message,'W':sol.fun,'rows':len(m),'columns':len(cols),'seconds':time.time()-start}
 print(json.dumps(report,indent=2),flush=True)
 if sol.success and sol.fun<.5:
  exact=cl.exact_point(cols,names,m,obj,norm,sol.x);exact['scope']='exact feasible cross-source shared-reply necessary graph; not SPE or game';exact['additional_cross_source_rows']=len(m)-3945
  (HERE/(tag+'_exact.json')).write_text(json.dumps(exact,indent=2)+'\n');report['exact_verified']=True
 (HERE/(tag+'_status.json')).write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
