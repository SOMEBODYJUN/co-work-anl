"""Exact arithmetic for a corollary of old PB; not a full-tree SPE audit."""
from fractions import Fraction as F
from pathlib import Path
import json
r,Q,H,M,d=2475,2063,100000,10**9,20
f=lambda c:F(11,1)/(M+c)+F(1,1)/(M+c+1)
g=lambda c:F(1200000,1)/(H*M+c)
L=F(3*r,Q)
real,dummy=f(1+L),g(1)
hr=(F(11,1)/(M+1+L)**2+F(1,1)/(M+2+L)**2)/Q
hd=F(1200000,(H*M+1)**2)
delta=d*(real+2*dummy)
u=d*3*f(3)
s=d*(real+2*g(r+1))
theta=3*(L-1)/(r-1)
U=d*(9*f(3)+1648*f(1)+824*f(2)+4944*g(2472))
checks={
 'query_support':real<dummy,
 'gradient_support':hr>hd,
 'singleton_query':delta>F(1,M+1),
 'singleton_gradient':3*d*hr>max(F(1,Q)/(M+1+L)**2,F(1,(H*M+1)**2)),
 'strict_local_deficit':delta>s>u,
 'child_mixture':0<=theta<=1,
 'hot_denominator':1+(r-1)*theta/3==L,
 'outside_denominator':(r-1)*(3-theta)/(Q-3)==L,
 'aggregate_survives':U>r*delta,
}
assert all(checks.values()),checks
out=dict(scope='Exact scalar corollary of old PB only; original game/SPE theorem inherited',checks=checks,L=str(L),theta=str(theta),local_balance=str(u-delta),aggregate_balance=str(U-r*delta))
Path(__file__).with_name('extra_fractional_plateau_check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
