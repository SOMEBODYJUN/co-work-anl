"""Definition-level scalar check of the inherited PB fractional-load corollary.
The all-history SPE proof is inherited from pair_attack.md, not this audit.
"""
from fractions import Fraction as F
from pathlib import Path
import json

k,d,q,r,Q,H,M,t = 3,20,12,2475,2063,100000,10**9,10
f=lambda c: F(q-1,M+c)+F(1,M+c+1)
g=lambda c: F(H*q,H*M+c)
u=d*k*f(k)
s=d*(f(1+F(r*k,Q))+(k-1)*g(r+1))
claimed=F(655518746053822970420433555247437051305,
604541061548383275389777051408169916255944671102717364)
checks={
 'gap_matches_inherited_fraction':s-u==claimed,
 'gap_positive':s>u,
 'G':g(r)>2*f(1)-f(2),
 'P':f(t)+(d-1)*f(1)+d*(k-1)*g(r)>d*(f(2)+(k-1)*g(1)),
 'Fill':k*f(k)>f(t)+(k-1)*g(1),
 'singleton':F(d*q,M+r+1)>F(1,M+1),
 'reverse_sum':(s-u)+u==s,
}
# Static customer identity, including absent comparison customers and zero load.
for dc in range(7):
 for ell in [F(0),F(1,7),F(1),F(3,2),F(17)]:
  assert int(dc>0)<=(dc+ell)/(1+ell)
assert all(checks.values())
out={'parameters':dict(k=k,d=d,q=q,r=r,Q=Q,H=H,M=M,t=t),
     'checks':checks,'u':str(u),'s':str(s),'gap':str(s-u),
     'scope':'Independent scalar arithmetic and static identity only; inherits all-history SPE proof.'}
path=Path(__file__).with_suffix('.json')
path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'checks':checks,'gap':str(s-u)},indent=2))
