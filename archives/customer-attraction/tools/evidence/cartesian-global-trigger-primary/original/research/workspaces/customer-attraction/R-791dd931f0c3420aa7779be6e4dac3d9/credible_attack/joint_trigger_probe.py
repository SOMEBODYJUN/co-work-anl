"""Full-Cartesian joint-trigger sufficient-policy search (not a new theorem).
Coordinates may prescribe non-SPE paths. After first joint mismatch, use a
product of coordinate child SPEs minimizing the deviator's coordinate payoff.
The sum of BI thresholds is a sufficient simultaneous-deviation bound.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,sys,time
import numpy as np
def rank(rows):
 if not rows:return 0
 a=[list(map(F,row)) for row in rows];r=0
 for c in range(len(a[0])):
  piv=next((j for j in range(r,len(a)) if a[j][c]),None)
  if piv is None:continue
  a[r],a[piv]=a[piv],a[r];v=a[r][c];a[r]=[x/v for x in a[r]]
  for j in range(r+1,len(a)):
   v=a[j][c]
   if v:a[j]=[x-v*y for x,y in zip(a[j],a[r])]
  r+=1
  if r==len(a):break
 return r

def solve(rows,rhs):
 n=len(rows);a=[list(map(F,row))+[F(b)] for row,b in zip(rows,rhs)]
 assert all(len(row)==n+1 for row in a)
 for c in range(n):
  piv=next(j for j in range(c,n) if a[j][c]);a[c],a[piv]=a[piv],a[c]
  v=a[c][c];a[c]=[x/v for x in a[c]]
  for j in range(n):
   if j!=c:
    v=a[j][c]
    if v:a[j]=[x-v*y for x,y in zip(a[j],a[c])]
 return [row[-1] for row in a]

from scipy.optimize import linprog
ROOT=next(x for x in Path(__file__).resolve().parents if (x/'customer_attraction/__init__.py').is_file())
sys.path.insert(0,str(ROOT))
from customer_attraction import Instance,CustomerType,ExactSPESolver
HERE=Path(__file__).resolve().parent

def coord(inst,label):
 p=inst.topic_count;m=5
 sol=ExactSPESolver(inst);sol.outcomes()
 terminal_payoffs=sol._payoffs
 optimum=inst.optimal_welfare()
 out=[]
 for path in product(range(p),repeat=m):
  q=inst.counts(path,terminal=True);up=terminal_payoffs.get(q)
  if up is None:up=inst.topic_payoffs(q);terminal_payoffs[q]=up
  u=tuple(up[a] for a in path)
  # At the last mover the aggregate threshold gap can only be nonpositive.
  # So discard all strictly negative last-player columns before the LP.
  pref=[0]*p;gap=[]
  for i,a in enumerate(path):
   gap.append(u[i]-sol.threshold(tuple(pref)));pref[a]+=1
  if gap[-1]<0:continue
  w=inst.welfare(q);o=optimum
  out.append({'source':label,'path':path,'gaps':gap,'w':w,'o':o})
 return out

def main():
 sources=[]
 for weights in [(5,1,1,1,1),(1,1,1,1,1),(1,1,1,1,1,1)]:
  inst=Instance(tuple(map(str,range(len(weights)))),tuple(CustomerType(frozenset([j]),int(x)) for j,x in enumerate(weights) if x),5)
  sources.append(('banks'+str(weights),inst))
 for f in sorted((ROOT/'examples/customer_attraction').glob('*.json')):
  data=json.loads(f.read_text())
  if 'instance' in data:data=data['instance']
  if 'topics' not in data:continue
  data['players']=5
  if len(data['topics'])<=7:sources.append((f.name,Instance.from_dict(data)))
 sys.path.insert(0,str(ROOT/'tests/audits'))
 from cone_attack_credible_variants import builtin_sources
 for label,inst,_ in builtin_sources():sources.append((label,inst))
 sources=[(label,Instance(inst.topics+("empty",),inst.customers,5)) for label,inst in sources]
 columns=[];seen=set();t0=time.time()
 for label,inst in sources:
  new=coord(inst,label)
  for c in new:
   key=tuple(c['gaps'])+(c['w'],c['o'])
   if key not in seen:seen.add(key);columns.append(c)
  print('seed',label,'columns',len(columns),'seconds',round(time.time()-t0,2),flush=True)
 gaps=np.array([[float(v) for v in c['gaps']] for c in columns]).T
 w=np.array([c['w'] for c in columns],float);o=np.array([c['o'] for c in columns],float)
 result=linprog(-o,A_ub=-gaps,b_ub=np.zeros(5),A_eq=w[None,:],b_eq=[1],bounds=(0,None),method='highs')
 def rational(v):return F(v)
 def exact_primal(res):
  selected=[j for j,x in enumerate(res.x) if x>1e-8];k=len(selected)
  rows=[[rational(columns[j]['w']) for j in selected]];rhs=[F(1)]
  for i in range(5):
   if abs(float(gaps[i]@res.x))<1e-7:
    row=[rational(columns[j]['gaps'][i]) for j in selected]
    if rank(rows+[row])>rank(rows):rows.append(row);rhs.append(F(0))
  if len(rows)!=k:raise AssertionError(('not a primal vertex',k,len(rows)))
  xs=solve(rows,rhs);assert min(xs)>=0
  gs=[sum(x*rational(columns[j]['gaps'][i]) for j,x in zip(selected,xs)) for i in range(5)]
  assert min(gs)>=0
  return {'weights':[{'source':columns[j]['source'],'path':columns[j]['path'],'weight':str(x),'w':columns[j]['w'],'o':columns[j]['o'],'gaps':list(map(str,columns[j]['gaps']))} for j,x in zip(selected,xs)],'aggregate_gaps':list(map(str,gs)),'ratio':str(sum(x*columns[j]['o'] for j,x in zip(selected,xs)))}
 chosen=[]
 if result.success:
  for c,x in zip(columns,result.x):
   if x>1e-8:chosen.append({**c,'weight_float':x,'gaps':list(map(str,c['gaps']))})
 report={'inputs':{label:inst.to_dict() for label,inst in sources},'status':'finite sufficient-policy search only','columns':len(columns),'success':bool(result.success),'ratio_float':None if not result.success else -float(result.fun),'chosen':chosen,'dual_float':None if not result.success else {'gaps':result.ineqlin.marginals.tolist(),'welfare':result.eqlin.marginals.tolist()}}
 if result.success:
  beta=F(str(round(-result.fun,8)))
  support=[i for i,x in enumerate(result.ineqlin.marginals) if x< -1e-8]
  equations=[];rhs=[]
  residual=beta*w-o+result.ineqlin.marginals@gaps
  for j,r in enumerate(residual):
   if abs(float(r))<1e-7:
    row=[rational(columns[j]['gaps'][i]) for i in support]
    if rank(equations+[row])>len(equations):
     equations.append(row);rhs.append(beta*columns[j]['w']-columns[j]['o'])
     if len(equations)==len(support):break
  lambdas=solve(equations,rhs);assert min(lambdas)>=0
  for col in columns:assert beta*col['w']-col['o']-sum(x*rational(col['gaps'][i]) for i,x in zip(support,lambdas))>=0
  report['finite_exact_dual']={'beta':str(beta),'lambda_by_player':{str(i+1):str(x) for i,x in zip(support,lambdas)},'all_columns_checked_exactly':True}
  report['finite_exact_optimal_primal']=exact_primal(result)
  bad=np.array([int(any(x<0 for x in c['gaps'])) for c in columns],float)
  mixed=linprog(-bad,A_ub=-gaps,b_ub=np.zeros(5),A_eq=w[None,:],b_eq=[1],bounds=(0,None),method='highs')
  if mixed.success:report['nonlocal_path_mixture']=exact_primal(mixed)
 (HERE/'joint_trigger_overlap_probe.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
