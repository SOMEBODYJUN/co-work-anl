"""One fixed-cone attack on the general safety-optimal query aggregate.
No sampling of models, policies, query supports or player numbers.
Reuse one pre-existing fully audited complete automaton; fix its original exact
static saddle, then optimize the C-W linear form over all incidence types while
keeping that saddle and every automaton-node SPE inequality.
Negative output is a bounded diagnostic only, never a general theorem.
"""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,gzip,json,itertools,math,hashlib
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[6]
OUT=Path(__file__).resolve().parent
SRC=ROOT/'research/workspaces/customer-attraction/R-e6796fb9db2a4ae9994cee93ac9bd152/security/cone_security_probe.py'
spec=importlib.util.spec_from_file_location('oldcone',SRC);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
n,k,masks,gamma,coeff,cover,w=mod.load('all')
p0,v0=mod.query_lp(w,coeff)
p=[F(float(z)).limit_denominator(10000000)for z in p0];assert sum(p)==1
# Opponent minimax, with rows=pure queries and columns=all n-1 backgrounds.
A=np.einsum('bta,t->ba',coeff,w).T
rr=linprog(np.r_[np.zeros(A.shape[1]),1.],A_ub=np.c_[A,-np.ones(k)],b_ub=np.zeros(k),A_eq=[np.r_[np.ones(A.shape[1]),0]],b_eq=[1.],bounds=[(0,None)]*A.shape[1]+[(None,None)],method='highs');assert rr.success
backs=list(mod.compositions(n-1,k))
Q=[(backs[j],F(float(z)).limit_denominator(10000000))for j,z in enumerate(rr.x[:-1])if z>1e-9];assert sum(z for B,z in Q)==1
packet_path=mod.PACKET
packet=json.load(gzip.open(packet_path,'rt'));nodes=packet['nodes'];end={}
for j in sorted(range(len(nodes)),key=lambda j:sum(nodes[j]['counts']),reverse=True):
 q=nodes[j];end[j]=tuple(q['counts'])if q.get('terminal')else end[q['children'][q['action']]]
def beta(B):return tuple(sum((p[a]for a in range(k)if mask&(1<<a)),F())/F(1+sum(B[a]for a in range(k)if mask&(1<<a)))for mask in masks)
def pure(a,B):return tuple(F(1,1+sum(B[t]for t in range(k)if mask&(1<<t)))if mask&(1<<a)else F()for mask in masks)
# Static saddle constraints, expressed against all nonnegative incidence mass.
primal=[beta(B)for B in backs]
dual=[tuple(sum((q*pure(a,B)[j]for B,q in Q),F())for j in range(len(masks)))for a in range(k)]
C=[F()for _ in masks];j=packet['root']
while not nodes[j].get('terminal'):
 q=nodes[j]
 for a,ch in enumerate(q['children']):
  B=list(end[ch]);B[a]-=1
  b=beta(tuple(B))
  for t,x in enumerate(b):C[t]+=p[a]*x
 j=q['children'][q['action']]
objective=[c-F(int(x))for c,x in zip(C,cover)]
oldw=[F()for _ in masks]
for customer in packet['instance']['customers']:
 mask=sum(1<<a for a in customer['topics'])
 oldw[mask-1]+=customer.get('multiplicity',1)
old_primal=min(sum((a*x for a,x in zip(row,oldw)),F())for row in primal)
old_dual=max(sum((a*x for a,x in zip(row,oldw)),F())for row in dual)
assert old_primal==old_dual
old_C=sum((a*x for a,x in zip(C,oldw)),F())
old_W=sum((F(int(a))*x for a,x in zip(cover,oldw)),F())
G=np.c_[-gamma,np.zeros(len(gamma))]
G=np.r_[G,np.c_[-np.array(primal,float),np.ones(len(primal))],np.c_[np.array(dual,float),-np.ones(k)]]
r=linprog(np.r_[-np.array(objective,float),0],A_ub=G,b_ub=np.zeros(len(G)),A_eq=[[1.]*len(masks)+[0.]],b_eq=[1.],bounds=[(0,None)]*len(masks)+[(None,None)],method='highs')
report={'scope':'One fixed automaton and one fixed original exact safety saddle; no general positive conclusion from a nonpositive LP optimum.','packet_sha256':hashlib.sha256(packet_path.read_bytes()).hexdigest(),'n':n,'k':k,'gamma_distinct':len(gamma),'static_backgrounds':len(backs),'types':len(masks),'p':[str(x)for x in p],'Q':[{'background':B,'probability':str(q)}for B,q in Q],'original_exact_safety_value':str(old_primal),'original_exact_sum_C':str(old_C),'original_W':str(old_W),'status':r.message,'max_C_minus_W_normalized':None if not r.success else -r.fun}
if r.success:
 wr=[F(float(x)).limit_denominator(10000000)for x in r.x[:-1]];v=F(float(r.x[-1])).limit_denominator(10000000)
 # Integer Gamma rows are exact at denominator lcm(1,...,n).
 L=math.lcm(*range(1,n+1));Gi=np.rint(gamma*L).astype(np.int64)
 slacks=[sum((F(int(g),L)*x for g,x in zip(row,wr)),F())for row in Gi]
 slacks += [sum((a*x for a,x in zip(row,wr)),F())-v for row in primal]
 slacks += [v-sum((a*x for a,x in zip(row,wr)),F())for row in dual]
 gap=sum((x*y for x,y in zip(objective,wr)),F())
 report.update(rational_min_slack=str(min(slacks)),rational_C_minus_W=str(gap),rational_v=str(v),weights={str(int(m)):str(x)for m,x in zip(masks,wr)if x})
report['outcome']='strict exact candidate refutation; requires separate all-history unit-client reconstruction'if r.success and min(slacks)>=0 and gap>0 else 'no strict refutation found: floating optimum 0; rational all-interest feasible point has exact gap 0'
(OUT/'optimal_query_fixed_cone_attack.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({x:report[x]for x in ('n','k','gamma_distinct','static_backgrounds','status','max_C_minus_W_normalized','rational_min_slack','rational_C_minus_W','outcome')},indent=2))
