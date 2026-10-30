"""Discovery only: abstract anonymous exact potential + binary four-term taxes."""
import itertools,json
import numpy as np
from scipy.optimize import linprog
k=3;n=3
p3=list(itertools.combinations_with_replacement(range(k),3));p2=list(itertools.combinations_with_replacement(range(k),2))
i3={z:i for i,z in enumerate(p3)};i2={z:len(p3)+i for i,z in enumerate(p2)}
d=len(p3)+len(p2)
def u(a,H):
 r=np.zeros(d+1);r[i3[tuple(sorted((*H,a)))]]=1;r[i2[tuple(sorted(H))]]=-1;return r
last={(0,0):1,(0,1):1,(0,2):2,(1,0):1,(1,1):1,(1,2):2,(2,0):1,(2,1):0,(2,2):2}
second={0:2,1:2,2:1}
def term(h):
 h=tuple(h)
 if len(h)==0:return term((1,))
 if len(h)==1:return term((*h,second[h[0]]))
 if len(h)==2:return (*h,last[h])
 return h
def pay(z,i):return u(z[i],z[:i]+z[i+1:])
rows=[]
for l in range(3):
 for h in itertools.product(range(k),repeat=l):
  actual=term(h)
  for a in range(k): rows.append(pay(actual,l)-pay(term((*h,a)),l))
for H in p2:
 for a in range(k):rows.append(u(a,H))
for h in range(k):
 for a,b,c in itertools.product(range(k),repeat=3):
  # R_H(a,b,c)>=0 as in coverage tax identity.
  rows.append(u(b,(h,a))-u(b,(h,c))+u(a,(h,c))-u(a,(h,a)))
W=sum((pay(term(()),i) for i in range(3)),np.zeros(d+1))
Aeq=np.array([W]);beq=np.array([1.])
rng=np.random.default_rng(23)
best=None
for trial in range(100):
 p=rng.dirichlet(np.ones(k)) if trial else np.ones(k)/k
 for it in range(10):
  safe=[]
  for H in p2:
   r=sum((p[a]*u(a,H) for a in range(k)),np.zeros(d+1));r[-1]-=1;safe.append(r)
  c=np.zeros(d+1);c[-1]=-1
  sol=linprog(c,A_ub=-np.array(rows+safe),b_ub=np.zeros(len(rows)+len(safe)),A_eq=Aeq,b_eq=beq,bounds=[(-20,20)]*d+[(0,None)],method='highs')
  if not sol.success:break
  v=sol.x[-1]
  if best is None or v>best['value']:
   best={'value':v,'p':p.tolist(),'F':sol.x[:len(p3)].tolist(),'G':sol.x[len(p3):d].tolist(),'p3':p3,'p2':p2,'trial':trial,'it':it}
  mat=np.array([[u(a,H)@sol.x for a in range(k)] for H in p2])
  cc=np.r_[np.zeros(k),-1.];AA=np.c_[-mat,np.ones(len(p2))]
  ss=linprog(cc,A_ub=AA,b_ub=np.zeros(len(p2)),A_eq=[[*np.ones(k),0]],b_eq=[1],bounds=[(0,None)]*k+[(None,None)])
  if not ss.success:break
  p=ss.x[:k]
print(json.dumps(best,indent=2))
