"""Exact audit of universal polynomial/fraction identities; no LP or BI."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
checks=0;minimum=None
for bg in [0,1,2,3,4,7,10,100,10**9]:
 f=F(1,bg+1);g=F(1,(bg+1)*(bg+2))
 def U(x,y):return f*x-g*x*y
 for c,d,t1,t2,r1,r2 in product((0,1),repeat=6):
  t=t1+t2;r=r1+r2;h=t1*r1+t2*r2;z=t1*t2
  alpha=U(c,d);beta=U(d,c)
  FF=2*alpha-U(t1,r1)-U(t2,r2)
  PP=2*beta-U(t1,c)-U(t2,c)
  ZZ=2*beta-U(r1,c)-U(r2,c)
  VV=U(r1,t1)-U(t2,t1)+U(r2,t2)-U(t1,t2)
  G=3*FF+PP+4*ZZ+4*VV
  Gformula=6*alpha+10*beta-8*f*t+g*c*t-g*h+4*g*c*r+8*g*z
  assert G==Gformula
  R=U(t1,t2)+U(t2,t1)
  psi=8*c-c*t+h-4*c*r+8*z
  assert psi>=0
  assert 6*alpha+10*beta+8*g*c-8*R-G==g*psi
  correction=4*g*c*(d-bg)
  assert 6*alpha+10*beta+8*g*c==10*(alpha+beta)+correction
  Inew=int(bg==0 and c==1 and d==1)
  assert correction<=2*Inew
  checks+=1
  minimum=psi if minimum is None else min(minimum,psi)
out={'backgrounds':[0,1,2,3,4,7,10,100,10**9],'binary_cases_per_background':64,'checks':checks,'minimum_psi':minimum,'status':'exact identities and nonnegative residual verified; arbitrary background theorem uses symbolic proof'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
