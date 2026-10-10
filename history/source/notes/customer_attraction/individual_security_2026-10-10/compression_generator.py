import json
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from itertools import product,combinations_with_replacement,combinations
import numpy as np
from scipy.optimize import milp,LinearConstraint,Bounds,linprog
P=Path('/workspace/scratch/4fa21fc3d3cc/security_cone_attack/individual_security_failure_360.json')
source=json.loads(P.read_text());n=3;m=6;N=63
policy={tuple(r['history']):r['action'] for r in source['strategy']['actions']}
@lru_cache(None)
def term(h):return h if len(h)==n else term(h+(policy[h],))
def row(a,z):
 return tuple(F(int(bool(T&(1<<a))),sum(bool(T&(1<<b)) for b in z)) if T&(1<<a) else F() for T in range(1,N+1))
def diff(x,y):return tuple(a-b for a,b in zip(x,y))
G=set()
for h,chosen in policy.items():
 actual=row(chosen,term(h))
 for a in range(m):
  d=diff(actual,row(a,term(h+(a,))))
  if any(d):G.add(d)
G=sorted(G);p=list(map(F,source['security']['primary']));u0=row(policy[()],term(()));static=list(combinations_with_replacement(range(m),n-1))
secr=[]
for B in static:
 e=tuple(sum(p[a]*row(a,(a,)+B)[j] for a in range(m)) for j in range(N))
 secr.append(diff(e,u0))
sep=[tuple(F(bool(T&(1<<a)) != bool(T&(1<<b))) for T in range(1,N+1)) for a,b in combinations(range(m),2)]
# All coefficients times16344 are integral; strict positive difference is at least1/16344.
scale=16344
assert all((scale*x).denominator==1 for R in secr for x in R)
A=np.array([[float(x*6) for x in R] for R in G]+[[float(x*scale) for x in R] for R in secr]+[[float(x) for x in R] for R in sep]);lb=np.array([0]*len(G)+[1]*len(secr)+[1]*len(sep))
res=milp(np.ones(N),integrality=np.ones(N),bounds=Bounds(0,np.inf),constraints=LinearConstraint(A,lb,np.inf),options={'time_limit':45,'mip_rel_gap':0})
if res.x is None:raise SystemExit(str(res.message))
w=[int(round(x)) for x in res.x]
def dot(R):return sum(x*val for x,val in zip(R,w))
assert min(map(dot,G))>=0 and min(map(dot,secr))>0 and min(map(dot,sep))>=1
rvals=np.array([[float(sum(row(a,(a,)+B)[j]*w[j] for j in range(N))) for B in static] for a in range(m)])
lp=linprog([0]*m+[-1],A_ub=np.column_stack([-rvals.T,np.ones(len(static))]),b_ub=np.zeros(len(static)),A_eq=[[1]*m+[0]],b_eq=[1],bounds=[(0,None)]*m+[(None,None)],method='highs')
newp=[F(float(x)).limit_denominator(10**6) for x in lp.x[:m]]
qlp=linprog([0]*len(static)+[1],A_ub=np.column_stack([rvals,-np.ones(m)]),b_ub=np.zeros(m),A_eq=[[1]*len(static)+[0]],b_eq=[1],bounds=[(0,None)]*len(static)+[(None,None)],method='highs')
newq=[F(float(x)).limit_denominator(10**6) for x in qlp.x[:len(static)]]
assert sum(newp)==sum(newq)==1
lower=min(sum(newp[a]*dot(row(a,(a,)+B)) for a in range(m)) for B in static)
upper=max(sum(newq[k]*dot(row(a,(a,)+B)) for k,B in enumerate(static)) for a in range(m))
assert lower==upper and lower>dot(u0)
source['claim']='individual mixed-security bridge failure, integer compression'
source['game']['customers']=[{'topics':[a for a in range(m) if T&(1<<a)],'multiplicity':w[T-1]} for T in range(1,N+1) if w[T-1]]
source['security']={'primary':list(map(str,newp)),'dual':[{'rivals':B,'probability':str(newq[k])} for k,B in enumerate(static) if newq[k]],'value':str(lower)}
source.pop('source_normalized_gap',None);source.pop('integer_scale',None)
source['compression']={'fixed_source_p_strict_gap':str(min(map(dot,secr))),'solver_status':res.message,'objective':sum(w),'mip_gap':getattr(res,'mip_gap',None),'dual_bound':getattr(res,'mip_dual_bound',None),'scope':'MILP only proposes integer weights; all weights and full SPE/static inequalities verified exactly, no global minimality claim'}
out=Path('/workspace/scratch/4fa21fc3d3cc/constant_prefix_cones/individual_security_compressed.json');out.write_text(json.dumps(source,indent=2)+'\n')
z=term(());utilities=[dot(row(a,z)) for a in z];W=sum(w[T-1] for T in range(1,N+1) if any(T&(1<<a) for a in z))
O=max(sum(w[T-1] for T in range(1,N+1) if any(T&(1<<a) for a in o)) for o in combinations_with_replacement(range(m),n))
print(json.dumps({'customers':sum(w),'positive_types':sum(bool(x) for x in w),'p':list(map(str,newp)),'security':str(lower),'u':list(map(str,utilities)),'W':W,'OPT':O,'gap':str(lower-utilities[0]),'compression':source['compression']},indent=2),flush=True)
