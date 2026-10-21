"""Independent exact check of the opportunity-boundary algebra, no solver imports."""
from fractions import Fraction as F
from math import isqrt
import json
from pathlib import Path
checked=0
for m in range(2,501):
 values=[F(m*k,k+1)+m-1-k for k in range(m)]
 after=max(values)
 delta=2*m-1-after
 q=isqrt(m)
 reduced=min(F(q)+F(m,q),F(q+1)+F(m,q+1))-1
 assert delta==reduced
 assert delta>=2*q-1
 assert all(delta<=F(j)+F(m,j)-1 for j in range(1,m+1))
 checked+=1
for q in range(2,501):
 m=q*q
 j=q
 after=F(m*(j-1),j)+m-j
 assert after==2*m-2*q
 assert F(2*m-1)-after==2*q-1
out={'status':'PASS','reviewer':'Boss5 primary; independent algebra reconstruction','formula_instances':checked,'square_instances':499,'scope':'Formula implementation checks; arbitrary-m proof is the analytic AM-GM argument, not this enumeration.','objections':[]}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
