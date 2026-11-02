"""Exact, LP-free verification of overlap-sensitive two-player identity.
Finite binary cases audit an algebraic identity; theorem uses symbolic slacks.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

def f(a,b):return F(a,1+b)
rows=[]
for c,d,t1,t2,r1,r2 in product((0,1),repeat=6):
 t=t1+t2;r=r1+r2;h=t1*r1+t2*r2;z=t1*t2
 alpha=f(c,d);beta=f(d,c)
 Fsum=2*alpha-f(t1,r1)-f(t2,r2)
 Psum=2*beta-f(t1,c)-f(t2,c)
 Zsum=2*beta-f(r1,c)-f(r2,c)
 Vsum=f(r1,t1)-f(t2,t1)+f(r2,t2)-f(t1,t2)
 G=3*Fsum+Psum+4*Zsum+4*Vsum
 expanded=6*alpha+10*beta-7*t-F(h,2)-F(t,1+c)+F(4*c*r,1+c)+4*z
 assert G==expanded
 residual=10*int(c+d>0)+2*c*d-8*int(t>0)-G
 rho=4*c-8*int(t>0)+7*t+F(h,2)+F(t,1+c)-F(4*c*r,1+c)-4*z
 assert residual==rho and rho>=0
 table=([[F(0),F(h,2),4+F(r,2)],[4-2*r,F(7,2)+F(h,2)-2*r,7-F(3*r,2)]][c][t])
 assert rho==table
 rows.append({'bits':[c,d,t1,t2,r1,r2],'residual':str(rho)})

def utility(S,T):return sum(F(1,1+(x in T))for x in S)
def audit(topics,replies,actual):
 for a,S in enumerate(topics):
  assert utility(topics[replies[a]],S)==max(utility(T,S)for T in topics)
 c,d=actual
 pay=utility(topics[c],topics[d])
 assert replies[c]==d
 assert pay==max(utility(S,topics[replies[a]])for a,S in enumerate(topics))
 W=len(topics[c]|topics[d]);I=len(topics[c]&topics[d]);O=max(len(S|T)for S in topics for T in topics)
 assert 8*O==10*W+2*I
 return {'topics':[sorted(S)for S in topics],'replies':replies,'actual':actual,'W':W,'I':I,'OPT':O,'comparisons':len(topics)**2+len(topics)}
first=[{0,1,2},{0,1,3},{0,1},{3,4}]
second=[{5,6},{7}]
end1=audit(first,[1,0,3,0],[2,3]);end2=audit(second,[0,0],[0,0])
cart=[S|T for S in first for T in second]
replies=[2*[1,0,3,0][a]+[0,0][b]for a in range(4)for b in range(2)]
joined=audit(cart,replies,[4,6])
out={'binary_cases':len(rows),'minimum_residual':str(min(F(x['residual'])for x in rows)),'endpoints':[end1,end2],'cartesian_product':joined,'residuals':rows}
path=Path(__file__).with_suffix('.json');path.write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items()if k!='residuals'},indent=2))
