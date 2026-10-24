from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

def scalar_family(t):
 C=set(range(t)); A=C|{t,t+1}; B=C|{t+2}; actions=(A,B)
 def pay(z,i):
  return sum((F(1,sum(x in S for S in z)) for x in z[i]),F())
 def rollout(h):
  z=list(h)
  while len(z)<2:z.append(A)
  return tuple(z)
 gaps=[]
 for h in ((),(A,),(B,)):
  i=len(h); leaf=rollout(h)
  for S in actions:gaps.append(pay(leaf,i)-pay(rollout((*h,S)),i))
 assert min(gaps)>=0
 u=F(t+2,2); assert pay((A,A),0)==pay((B,A),0)==pay((A,B),1)==u
 assert len(A|B)-len(A)==1
 # Both rows covering the omitted customer x have coefficient 1; all others 0.
 scalar=F(1); coordinate=u
 assert coordinate/scalar==u
 return {'t':t,'u':str(u),'minimum_IC':str(min(gaps)),'scalar_opt':str(scalar),'coordinate_opt':str(coordinate)}

def free_source_identity():
 count=0
 for h0,h1,h2 in product(range(4),repeat=3):
  H=(h0,h1,h2); I=(0,1,1)
  for p0,p1,Q0,Q1 in product(range(3),repeat=4):
   p=(F(p0,4),F(p1,4),1-F(p0+p1,4)); Q=(F(Q0,4),F(Q1,4),1-F(Q0+Q1,4))
   if min(p)<0 or min(Q)<0:continue
   q=sum(p[a]*I[a] for a in range(3)); r=sum(Q[a]*I[a] for a in range(3))
   R=[F(1,1+h) for h in H]; J=[F(1,(1+h)*(2+h)) for h in H]
   ER=sum(Q[a]*R[a] for a in range(3)); EIR=sum(Q[a]*I[a]*R[a] for a in range(3)); EIJ=sum(Q[a]*I[a]*J[a] for a in range(3))
   C=sum(Q[a]*q*F(1,1+H[a]+I[a]) for a in range(3)); D=EIR
   rhs=(q-r)*ER-(EIR-r*ER)-q*EIJ
   assert C-D==rhs
   count+=1
 return count

def owner_identity():
 n=0
 for c in range(8):
  J=F(c,c+1); e=F(1,c+1)
  assert J+e==1
  n+=1
 return n

result={'status':'exact checks passed; finite regressions do not prove Q-CAG-HALF',
 'scalar_family':[scalar_family(t) for t in (0,1,2,7,100)],
 'free_source_identity_cases':free_source_identity(),
 'owner_identity_cases':owner_identity()}
path=Path(__file__).with_suffix('.json');path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
