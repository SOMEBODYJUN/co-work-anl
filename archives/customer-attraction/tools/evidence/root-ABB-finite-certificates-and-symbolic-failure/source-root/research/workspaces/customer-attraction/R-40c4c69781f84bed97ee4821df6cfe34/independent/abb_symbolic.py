"""Exact rational-polynomial certificate, without symbolic-library dependencies."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,math
OUT=Path(__file__).resolve().parent

def trim(p):
 p=list(map(F,p))
 while len(p)>1 and p[-1]==0:p.pop()
 return tuple(p)
def add(a,b):return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])
def neg(a):return tuple(-v for v in a)
def mul(a,b):
 c=[F(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return trim(c)
def divmodp(a,b):
 a=list(a);out=[F(0)]*max(1,len(a)-len(b)+1)
 while len(a)>=len(b) and any(a):
  j=len(a)-len(b);v=a[-1]/b[-1];out[j]+=v
  for i,x in enumerate(b):a[i+j]-=v*x
  a=list(trim(a))
 return trim(out),trim(a)
def gcd(a,b):
 while any(b):a,b=b,divmodp(a,b)[1]
 return trim([v/a[-1] for v in a])
class R:
 def __init__(self,a=0,b=1):
  if isinstance(a,R):self.a,self.b=a.a,a.b;return
  a=trim(a if isinstance(a,(list,tuple)) else (a,));b=trim(b if isinstance(b,(list,tuple)) else (b,))
  assert any(b)
  g=gcd(a,b);a=divmodp(a,g)[0];b=divmodp(b,g)[0]
  v=b[-1];self.a=trim([x/v for x in a]);self.b=trim([x/v for x in b])
 def __add__(self,o):
  o=R(o);return R(add(mul(self.a,o.b),mul(o.a,self.b)),mul(self.b,o.b))
 __radd__=__add__
 def __neg__(self):return R(neg(self.a),self.b)
 def __sub__(self,o):return self+-R(o)
 def __rsub__(self,o):return R(o)+-self
 def __mul__(self,o):
  o=R(o);return R(mul(self.a,o.a),mul(self.b,o.b))
 __rmul__=__mul__
 def __truediv__(self,o):
  o=R(o);return R(mul(self.a,o.b),mul(self.b,o.a))
 def __rtruediv__(self,o):return R(o)/self
 def __bool__(self):return any(self.a)
 def pack(self):
  den=math.lcm(*(v.denominator for v in self.a+self.b))
  return {'numerator_l_ascending':[int(v*den) for v in self.a],'denominator_l_ascending':[int(v*den) for v in self.b]}
L=R((0,1));k=2*L+1;m=3*L+1

def components(a,b,q,r,d):
 p=(k-1)*a+(L-2)*b;c=k*a+L*b
 ua=a/c if a else R(0);vb=b/c if b else R(0)
 ub=b/(p+b+q+r) if b else R(0);ur=r/(p+b+q+r) if r else R(0)
 KQ=3*ua-3*q/(p+3);KR=3*ua-3*r/(p+3)
 P=m*vb-d/(p+a+b+1);FF=ua-ub;J=m*ur-d/(p+b+q+1)
 return [KQ,FF,m*KR-P+J],P
keys=((0,1,1,0,1),(0,1,1,1,1),(1,1,0,0,1))
mat=[]
for key in keys:
 row,base=components(*key);mat.append(row+[1-base])
for col in range(3):
 pivot=next(r for r in range(col,3) if mat[r][col]);mat[col],mat[pivot]=mat[pivot],mat[col]
 v=mat[col][col];mat[col]=[x/v for x in mat[col]]
 for r in range(3):
  if r==col:continue
  v=mat[r][col];mat[r]=[a-v*b for a,b in zip(mat[r],mat[col])]
x,f,j=(mat[r][3] for r in range(3))
mults={'K_Q':x,'K_R':m*j,'P':1-j,'F':f,'J':j}

def shift(p,by=2):
 out=[F(0)]*len(p)
 for i,v in enumerate(p):
  for h in range(i+1):out[h]+=v*math.comb(i,h)*by**(i-h)
 return trim(out)
def positive_certificate(val):
 a=shift(val.a);b=shift(val.b)
 ok=all(v>=0 for v in a) and all(v>=0 for v in b) and b[0]>0
 return {'shifted_numerator_ascending':list(map(str,a)),'shifted_denominator_ascending':list(map(str,b)),'all_coefficients_nonnegative':ok}
proof=[]
for a,b,q,r,d in product((0,1),repeat=5):
 coeff,base=components(a,b,q,r,d)
 residual=2*int(bool(a or b))-d-base-sum((u*v for u,v in zip(coeff,(x,f,j))),R(0))
 proof.append({'membership':[a,b,q,r,d],'residual':residual.pack(),'positivity':positive_certificate(residual)})
print('MULTIPLIERS',json.dumps({n:v.pack() for n,v in mults.items()},indent=2))
print('PROVED',sum(r['positivity']['all_coefficients_nonnegative'] for r in proof),len(proof))
report={'scope':'k=2*l+1,l>=2, terminal suffix ABB','multipliers':{n:{'value':v.pack(),'positivity':positive_certificate(v)} for n,v in mults.items()},'residuals':proof}
(OUT/'abb_symbolic_report.json').write_text(json.dumps(report,indent=2))
