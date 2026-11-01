import json,math
from fractions import Fraction
from itertools import product
from scipy.optimize import linprog, milp, Bounds, LinearConstraint
import numpy as np
from customer_attraction import Instance, CustomerType, StrategyCertificate,verify_certificate
from pathlib import Path
base=Path(__file__).parent
raw=json.loads((base/'kernel_no_common_parameter_raw.json').read_text());acts={tuple(h):a for h,a in raw['actions']};p=4;n=3
types=[tuple(i for i in range(p) if mask>>i&1) for mask in range(1,1<<p)]
def term(h):
 while len(h)<n:h=h+(acts[h],)
 return h
def row(h,a):
 ac=acts[h];q=term(h);r=term(h+(a,))
 return [[int(ac in B and sum(x in B for x in q)==d+1)-int(a in B and sum(x in B for x in r)==d+1) for B in types] for d in range(n)]
A=[];b=[]
for d in range(n):
 for h in product(range(p),repeat=d):
  for a in range(p):
   rows=row(h,a);A.append([-float(sum(Fraction(rows[d][j],d+1) for d in range(n))) for j in range(len(types))]);b.append(0.)
r1=row((1,0),3);r2=row((3,0),2);r3=row((3,3),1)
eq=[r1[0],[3*x+2*y for x,y in zip(r1[1],r1[2])],r3[1],[3*x+y for x,y in zip(r3[0],r3[2])]]
A.extend([r1[1],[-x for x in r3[0]],r2[0]]);b.extend([-2.,-1.,-1.])
z=milp(np.ones(len(types)),integrality=np.ones(len(types)),bounds=Bounds(np.zeros(len(types)),np.full(len(types),np.inf)),constraints=[LinearConstraint(np.array(A),np.full(len(A),-np.inf),np.array(b)),LinearConstraint(np.array(eq),np.zeros(len(eq)),np.zeros(len(eq)))],options={'time_limit':30.})
print(z.success,z.fun,z.message)
ws=[Fraction(float(x)).limit_denominator(10000) for x in z.x]
lcm=math.lcm(*(w.denominator for w in ws));ws=[int(w*lcm) for w in ws]
gcd=math.gcd(*ws);ws=[w//gcd for w in ws]
print([(B,w) for B,w in zip(types,ws) if w])
ins=Instance(tuple('ABCD'),tuple(CustomerType(frozenset(B),w) for B,w in zip(types,ws) if w),n)
path=term(());cert=StrategyCertificate(acts,ins.counts(path,terminal=True));report=verify_certificate(ins,cert);report.assert_valid()
for h,a in [((1,0),3),((3,0),2),((3,3),1)]:
 print(h,a,[sum(w*c for w,c in zip(ws,r)) for r in row(h,a)])
out={'topics':list('ABCD'),'players':3,'customers':[{'topics':list(B),'multiplicity':w} for B,w in zip(types,ws) if w],'actions':[(list(h),a) for h,a in acts.items()]}
(base/'kernel_no_common_parameter.json').write_text(json.dumps(out,indent=2)+'\n')
print('path',path,'welfare',ins.welfare(ins.counts(path,terminal=True)),'OPT',ins.optimal_welfare())
