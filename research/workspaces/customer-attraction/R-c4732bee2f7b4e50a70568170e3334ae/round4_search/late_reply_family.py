"""Targeted full SPE cones: forced early A, optimal finite suffix policies.
Only the selected witness is reconstructed with exact full ordered history cones.
Every LP includes the incentive row at every count state, then the exact selected
policy is expanded to every ordered history. This samples a restricted class.
"""
from __future__ import annotations
import sys,json,time,argparse,hashlib
from pathlib import Path
from itertools import product,combinations
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'customer_attraction/__init__.py').is_file())
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests/audits'))
from customer_attraction import StrategyCertificate,verify_certificate
from customer_attraction_strategy_lp import StrategyCone,serializable,integer_clones,instance_from_clones,independently_verify

def counts(p,total):
 if p==1:yield(total,);return
 for i in range(total+1):
  for q in counts(p-1,total-i):yield(i,)+q

def inc(q,a):return q[:a]+(q[a]+1,)+q[a+1:]
class Family:
 def __init__(self,p,m,late):
  self.p=p;self.m=m;self.late=late;self.root=(0,)*p
  self.I=((np.arange(1,1<<p)[:,None]>>np.arange(p))&1).astype(float)
  self.Q=tuple(counts(p,m));self.qi={q:i for i,q in enumerate(self.Q)}
  den=np.array(self.Q)@self.I.T
  self.P=np.divide(self.I.T[None,:,:],den[:,None,:],out=np.zeros((len(self.Q),p,len(self.I))),where=den[:,None,:]>0)
  self.W=(den>0).astype(float)
  self.nodes=tuple(q for d in range(m-1,-1,-1) for q in counts(p,d))
  self.Js=tuple(combinations(range(p),min(p,m)))
  self.V=np.array([self.I[:,J].any(axis=1).astype(float) for J in self.Js])
 def policy(self,r,mode):
  U=self.P@r;W=self.W@r;term={q:self.qi[q] for q in self.Q};pol={}
  for q in self.nodes:
   t=np.array([term[inc(q,a)] for a in range(self.p)],dtype=int)
   if sum(q)<self.m-self.late:a=0
   else:
    pay=np.array([U[t[a],a] for a in range(self.p)])
    tied=np.flatnonzero(pay>=pay.max()-1e-9)
    if mode==0:a=int(tied[0])
    elif mode==1:a=int(tied[-1])
    elif mode==2:a=int(tied[np.argmin(U[t[tied],0])])
    elif mode==3:a=int(tied[np.argmax(U[t[tied],0])])
    elif mode==4:a=int(tied[np.argmin(W[t[tied]])])
    else:a=int(tied[np.argmax(W[t[tied]])])
   pol[q]=a;term[q]=int(t[a])
  keys={(term[q],a,term[inc(q,b)],b) for q,a in pol.items() for b in range(self.p) if b!=a}
  A=np.unique(np.array([self.P[t,a]-self.P[d,b] for t,a,d,b in keys]),axis=0)
  return pol,A,term[self.root]
 def optimize(self,A,t,j):
  return linprog(-self.V[j],A_ub=-A,b_ub=np.zeros(len(A)),A_eq=self.W[[t]],b_eq=[1],bounds=(0,None),method='highs')
 def export(self,pol,j):
  actions={h:pol[tuple(h.count(a) for a in range(self.p))] for d in range(self.m) for h in product(range(self.p),repeat=d)}
  cone=StrategyCone(self.p,self.m,actions);r=cone.optimize(self.Js[j])
  if not r['certified']:return None
  clones=integer_clones(r['values']);instance=instance_from_clones(self.p,self.m,clones)
  if not independently_verify(cone,clones):raise AssertionError('direct ordered history incentive failure')
  verify_certificate(instance,StrategyCertificate(actions,cone.root)).assert_valid()
  return {'root_counts':cone.root,'portfolio':self.Js[j],'objective_exact':r['value'],'W':instance.welfare(cone.root),'OPT':instance.optimal_welfare(),'ratio_exact':Fraction(instance.optimal_welfare(),instance.welfare(cone.root)),'integer_clones':clones,'dual_bound_exact':r['dual_bound'],'dual_optimal':r['dual_optimal'],'strategy':StrategyCertificate(actions,cone.root).to_dict(),'rows':len(cone.rows),'ordered_decision_histories':len(actions),'dual_support':r['dual_support']}

def seeds(p,m):
 # One distinguished early topic A, p-3 symmetric comparison topics,
 # and a two-topic late reply cycle. Grid varies the four incidence masses.
 for a,b,c,d in product((0,1,4),repeat=4):
  if not b and not c and not d:continue
  r=np.zeros((1<<p)-1)
  r[0]=a
  for i in range(1,p-2):
   r[(1<<i)-1]=b
   r[((1<<i)|(1<<(p-2))|(1<<(p-1)))-1]=d
  r[(1|(1<<(p-2)))-1]=c;r[(1|(1<<(p-1)))-1]=c
  yield (a,b,c,d),r
 # Full big/small boundary and deterministic core-sharing variations.
 for z in (0,1,2,4):
  r=np.zeros((1<<p)-1);r[0]=m
  for i in range(1,p):r[(1<<i)-1]=1;r[(1|(1<<i))-1]=z
  yield ('big',z),r

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--topics',type=int,default=7);ap.add_argument('--players',type=int,default=5);ap.add_argument('--late',type=int,default=2);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--passes',type=int,default=1);a=ap.parse_args()
 f=Family(a.topics,a.players,a.late);seen=set();log=[];best=0;selected=None;started=time.monotonic();queue=list(seeds(a.topics,a.players))
 for it,(label,r) in enumerate(queue):
  for mode in range(6):
   pol,A,t=f.policy(r,mode);key=tuple(pol[q] for q in f.nodes)
   if key in seen:continue
   seen.add(key)
   vals=[]
   for j in range(len(f.Js)):
    o=f.optimize(A,t,j)
    if o.success:vals.append((-o.fun,j,o.x))
   if not vals:continue
   val,j,endpoint=max(vals,key=lambda x:x[0]);entry={'seed':label,'tie_mode':mode,'root_counts':f.Q[t],'floating_max':val,'rows':len(A)};log.append(entry)
   if val>best+1e-8:
    exact=f.export(pol,j)
    if exact is not None:
     best=float(exact['ratio_exact']);selected=exact;entry['new_best_exact']=str(exact['ratio_exact']);print(json.dumps(serializable(entry)),flush=True)
   if a.passes>1 and len(queue)<300 and it<80:queue.append((('endpoint',it,mode),endpoint))
  if it%10==0:
   report={'scope':'targeted restricted full-policy cone family: forced early A and BI suffix generated by four-block late reply cycles','players':a.players,'topics':a.topics,'late':a.late,'universal_bound_proved':False,'number_distinct_policies':len(seen),'number_nonzero_feasible_policies':len(log),'log':log,'selected_exact':selected,'elapsed_seconds':time.monotonic()-started}
   a.output.write_text(json.dumps(serializable(report),indent=2)+'\n')
 report.update(number_distinct_policies=len(seen),number_nonzero_feasible_policies=len(log),log=log,selected_exact=selected,elapsed_seconds=time.monotonic()-started,seed_script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
 a.output.write_text(json.dumps(serializable(report),indent=2)+'\n');print(json.dumps(serializable({k:v for k,v in report.items() if k not in ('log','selected_exact')})),flush=True)
if __name__=='__main__':main()
