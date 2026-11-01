"""Fixed-input attack of SELF-MENU (stronger than Mfull), not a search for HALF.
The exact general claim under attack is E_p D_A >= E_(p*p) K(T,A).
Inputs: existing 52-customer SPE; literature all-big m5; existing petal m5,J3.
Every claimed SPE is checked at every ordered history; no finite pass is proof.
"""
from pathlib import Path
from itertools import product, combinations
from fractions import Fraction as F
import json, sys
import numpy as np
from scipy.optimize import minimize, linprog
ROOT=Path(__file__).resolve().parents[6]
sys.path.insert(0,str(ROOT))
from customer_attraction.model import Instance,CustomerType,big_theme_lower_bound
from customer_attraction.exact import ExactSPESolver
from customer_attraction.certificate import StrategyCertificate,verify_certificate
P=Path(__file__).resolve().parent

def finish(actions,m,h):
 while len(h)<m:h=h+(actions[h],)
 return h

def check_case(name,I,C):
 V=verify_certificate(I,C);V.assert_valid();m=I.players;k=I.topic_count
 Z=V.terminal_history
 D=[];K=[[F(0) for a in range(k)]for t in range(k)];leaves=[]
 for a in range(k):
  z=finish(C.actions,m,(a,));leaves.append(z);cnt=I.counts(z,terminal=True)
  D.append(I.topic_payoff(a,cnt))
  for t in range(k):
   K[t][a]=sum((F(c.multiplicity,1+sum(cnt[b]for b in c.topics))for c in I.customers if t in c.topics),F(0))
 M=np.array([[float((D[i]+D[j])/2-(K[i][j]+K[j][i])/2)for j in range(k)]for i in range(k)])
 starts=[np.full(k,1/k)]+[np.eye(k)[i]for i in range(k)]
 for size in range(2,k+1):
  for ss in combinations(range(k),size):
   starts.append(np.array([1/size if i in ss else 0 for i in range(k)]))
 best=None
 for p in starts:
  r=minimize(lambda q:float(q@M@q),p,jac=lambda q:2*M@q,method='SLSQP',constraints=[{'type':'eq','fun':lambda q:q.sum()-1,'jac':lambda q:np.ones(k)}],bounds=[(0,1)]*k,options={'maxiter':300,'ftol':1e-12})
  if best is None or r.fun<best.fun:best=r
 p=[F(float(x)).limit_denominator(100000)for x in best.x];s=sum(p);p=[x/s for x in p]
 gap=sum((p[a]*D[a]for a in range(k)),F(0))-sum((p[t]*p[a]*K[t][a]for t in range(k)for a in range(k)),F(0))
 # Mfull primal min_q t: Kq <= t.
 Knum=np.array([[float(x)for x in row]for row in K])
 lp=linprog([0]*k+[1],A_ub=np.column_stack([Knum,-np.ones(k)]),b_ub=np.zeros(k),A_eq=[[1]*k+[0]],b_eq=[1],bounds=[(0,None)]*k+[(None,None)],method='highs')
 assert lp.success
 cov=F(0);selfref=F(0)
 for c in I.customers:
  px=sum(p[a]for a in c.topics)
  vals=[]
  for a,z in enumerate(leaves):
   tail=sum(b in c.topics for b in z[1:]);alpha=int(a in c.topics)
   vals.append(F(1,1+tail))
   selfref+=c.multiplicity*px*p[a]*alpha*F(1,(1+tail)*(2+tail))
  cov+=c.multiplicity*(sum((p[a]*int(a in c.topics)*vals[a]for a in range(k)),F(0))-px*sum((p[a]*vals[a]for a in range(k)),F(0)))
 assert cov+selfref==gap
 return {'name':name,'m':m,'topics':k,'customers':I.customer_count,'actual':Z,'W':I.welfare(I.counts(Z)),'OPT':I.optimal_welfare(),'u':[str(x)for x in I.player_payoffs(Z)],'histories':V.checked_histories,'deviations':V.checked_deviations,'root_D':[str(x)for x in D],'root_leaves':leaves,'K':[[str(x)for x in row]for row in K],'SELF_numerical_min':float(best.fun),'SELF_exact_at_rationalized_optimizer':str(gap),'p':[str(x)for x in p],'response_covariance':str(cov),'self_refund':str(selfref),'Mfull_numerical':float(lp.fun),'root_u':str(I.player_payoffs(Z)[0]),'certificate':C.to_dict(),'instance':I.to_dict()}

def petal(m,J):
 I=Instance(('A','B')+tuple(f'Q{j}'for j in range(J)),(CustomerType(frozenset([0]+list(range(2,J+2))),2),CustomerType(frozenset([1]),2*(m-1)))+tuple(CustomerType(frozenset([2+j]),1)for j in range(J)),m)
 def act(h):
  if not h:return 0
  if len(h)<m-1:return 1
  small=[a for a in h if a!=1]
  if not small:return 2
  if len(small)==1:
   if small[0]==0:return 1
   return 3 if small[0]==2 else 2
  return 1
 actions={h:act(h)for d in range(m)for h in product(range(J+2),repeat=d)}
 z=finish(actions,m,())
 return I,StrategyCertificate(actions,I.counts(z,terminal=True))

src=ROOT/'research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/static_matching/static_matching_counterexample.json'
old=json.loads(src.read_text())
I0=Instance.from_dict(old['instance']);C0=StrategyCertificate.from_dict(old['certificate'])
I1=big_theme_lower_bound(5);C1=ExactSPESolver(I1).certificate(on_path=(0,)*5)
I2,C2=petal(5,3)
results=[check_case('old52',I0,C0),check_case('literature_all_big_m5',I1,C1),check_case('existing_petal_m5_J3',I2,C2)]
out={'scope':'Fixed-input attacks of general SELF-MENU sufficient candidate. Complete SPE verified; numerical minimization not exact nonnegativity proof. No HALF claim.','results':results}
(P/'root_menu_pressure.json').write_text(json.dumps(out,indent=2)+'\n')
for r in results:print({key:r[key]for key in ('name','m','histories','deviations','SELF_exact_at_rationalized_optimizer','response_covariance','self_refund','Mfull_numerical','root_u')})
