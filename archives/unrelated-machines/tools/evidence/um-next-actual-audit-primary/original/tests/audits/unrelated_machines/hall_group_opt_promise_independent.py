"""Independent finite OPT-promise corollary audit; explicit original jobs.
No imported matrix, flow, Hall, or optimum routine. Only candidate.solve is called.
"""
from fractions import Fraction as Q
from itertools import product
from functools import lru_cache
from random import Random
import json,hashlib
from pathlib import Path
import importlib.util,sys,platform
base=Path(__file__).resolve().parent
source=Path(sys.argv[1]) if len(sys.argv)>1 else next(p for p in (base/'hall_group_joint_flow.py',base/'hall_joint_coupling.py') if p.exists())
spec=importlib.util.spec_from_file_location('hall_group_candidate',source)
candidate=importlib.util.module_from_spec(spec)
spec.loader.exec_module(candidate)


def build(groups,E,B,k):
 h=len(groups);A=[]
 for row in B:A.append(tuple((i,p) for i,p in enumerate(row) if p is not None))
 for i,G in enumerate(groups):
  for w in G:A.append(((i,w),)+tuple((h+z,w) for z in E[i]))
 return tuple(A)


def exact_opt(A,m):
 # Every actual makespan is a per-machine subset sum; enumerate those candidates.
 if not A:return Q(0)
 thresholds={Q(0)}
 for i in range(m):
  S={Q(0)}
  for C in A:
   p=dict(C).get(i)
   if p is not None:S|={s+p for s in S}
  thresholds|=S
 A=tuple(sorted(A,key=lambda C:(len(C),-max((p for _,p in C),default=Q(0)))))
 def feasible(T):
  @lru_cache(None)
  def f(t,L):
   if t==len(A):return True
   for i,p in A[t]:
    if L[i]+p<=T:
     K=list(L);K[i]+=p
     if f(t+1,tuple(K)):return True
   return False
  return f(0,(Q(0),)*m)
 L=sorted(thresholds);a,b=0,len(L)-1
 assert feasible(L[b])
 while a<b:
  c=(a+b)//2
  if feasible(L[c]):b=c
  else:a=c+1
 return L[a]


def bottleneck(E,B,k,q):
 # Joint macro/home/receiver choice by independent small-instance exhaustive search.
 if not B:return Q(0)
 best=None;used=set();counts=[0]*k
 def f(j,peak):
  nonlocal best
  if best is not None and peak>=best:return
  if j==len(B):best=peak;return
  for i,p in enumerate(B[j]):
   if p is None or i in used:continue
   used.add(i)
   for z in E[i]:
    if counts[z]<q:
     counts[z]+=1;f(j+1,max(peak,p));counts[z]-=1
   used.remove(i)
 f(0,Q(0));return best


def run():
 rng=Random(778791);N=0;promise=0;success=0;Tstrict=0
 for q,d,templates in [
  (2,Q(1,2),[(Q(1,2),)*2]),
  (3,Q(1,3),[(Q(1,3),)*3,(Q(1,3),Q(1,3),Q(1,6))]),
  (4,Q(3,8),[(Q(1,4),)*3,(Q(1,4),)*4]),
 ]:
  for _ in range(100):
   h=rng.choice([1,2]);k=rng.choice([1,2])
   G=[rng.choice(templates) for i in range(h)]
   E=[tuple(z for z in range(k) if rng.getrandbits(1)) for i in range(h)]
   B=[]
   for j in range(rng.randint(0,h)):
    row=tuple(rng.choice([None,Q(3,5),Q(3,4),Q(1),Q(3,2)]) for i in range(h))
    if all(p is None for p in row):row=(Q(1),)+tuple(None for i in range(h-1))
    B.append(row)
   A=build(G,E,B,k);opt=exact_opt(A,h+k);N+=1
   theta=Q(1,2)+Q(1,q)
   if not (all(theta*opt<=sum(row,Q(0))<=opt for row in G)
    and all(w<=d*opt for row in G for w in row)
    and all(p is None or p>opt/2 for row in B for p in row)):continue
   promise+=1
   Bstar=bottleneck(E,B,k,q)
   assert Bstar is not None and Bstar<=opt
   W=max([sum(row,Q(0)) for row in G]+[Q(0)])
   w=max([w for row in G for w in row]+[Q(0)])
   T=max(W,w/d,Bstar)
   assert T<=opt
   Tstrict+=T<opt
   out=candidate.solve_promise(G,E,B,k,q,d)
   assert out['threshold']==T
   assert out is not None;success+=1
   sigma=list(out['macro_assignment'])+[x for row in out['assignment'] for x in row]
   assert len(sigma)==len(A)
   L=[Q(0)]*(h+k)
   for C,(kind,i) in zip(A,sigma):
    assert kind in {'h','z'}
    endpoint=i if kind=='h' else h+i
    assert endpoint in dict(C)
    L[endpoint]+=dict(C)[endpoint]
   r=Q(2*q+q*d,q+1)
   assert all(v<=r*T<=r*opt for v in L)
 # A valid promise case whose recovered threshold is strictly below actual OPT.
 G=[[Q(1,6)]*6 for _ in range(2)];E=[(0,),(0,)];B=[(Q(3,5),None),(None,Q(3,5))]
 A=build(G,E,B,1);opt=exact_opt(A,3)
 assert opt==Q(11,10)
 out=candidate.solve_promise(G,E,B,1,3,Q(1,3))
 assert out['threshold']==1<opt
 assert max(out['loads'])<=out['rho']*opt
 Tstrict+=1;N+=1;promise+=1;success+=1
 zero=candidate.solve_promise([[Q(0)]],[()],[],0,2,Q(0))
 assert zero['threshold']==0 and max(zero['loads'])==0
 return {'sampled_inputs':N,'exact_OPT_promise_cases':promise,
 'successful_outputs':success,'strict_t_less_than_OPT_cases':Tstrict,
 'seed':778791,'python':platform.python_version(),'arithmetic':'Fraction/int','status':'PASS',
 'oracle':'original individual-job subset-sum threshold enumeration plus DFS; bottleneck by exhaustive joint choices',
 'candidate_sha256':hashlib.sha256(Path(candidate.__file__).read_bytes()).hexdigest(),
 'audit_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

if __name__=='__main__':print(json.dumps(run(),indent=2))
