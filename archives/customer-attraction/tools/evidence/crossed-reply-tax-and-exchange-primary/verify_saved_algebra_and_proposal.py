"""Exact source-specific checks; no search and no claim over all strategies."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
import ast,json
import numpy as np
root=Path(__file__).resolve().parent
# Clear the common positive denominator (b+1)(b+2)(b+3) exactly.
u=lambda x,ys:[(Q(x),(1+sum(ys),))]
phi=lambda x,y:[(Q(1),(k,)) for k in range(1,x+y+1)]
g=lambda x,y,t:[(Q(x*y),(t+1,t+2))]
def scale(a,v):return [(v*c,d) for c,d in a]
def check_zero(terms):
 out=[Q(0)]*4
 for coefficient,den in terms:
  p=[coefficient]
  assert len(set(den))==len(den) and set(den)<={1,2,3}
  for factor in sorted({1,2,3}-set(den)):
   z=[Q(0)]*(len(p)+1)
   for i,v in enumerate(p):z[i]+=factor*v;z[i+1]+=v
   p=z
  for i,v in enumerate(p):out[i]+=v
 assert all(v==0 for v in out),out
count=0
for t,r,s,v,w,k in product(range(2),repeat=6):
 l1=u(r,[t,s])+scale(u(v,[t,k]),-1)
 l2=u(k,[t,v])+scale(u(w,[t,v]),-1)
 l3=u(s,[t,r])+scale(u(k,[t,r]),-1)
 lhs=u(t,[r,s])+scale(u(t,[v,w]),-1)
 tau=g(r,r,t)+scale(g(s,r,t),-1)
 check_zero(lhs+scale(l1,-1)+scale(l2,-1)+scale(u(s,[t]),-1)+u(k,[t])+scale(phi(v,w),-1)+phi(r,s))
 check_zero(lhs+tau+scale(l1,-1)+scale(l2,-1)+scale(l3,-1)+scale(g(r,r,t),-1)+g(k,r,t)+scale(phi(v,w),-1)+phi(r,s))
 count+=1
cert=json.loads((root/'attack-runtime/evidence/certificates/customer_attraction/individual_security_failure.json').read_text())
pol={tuple(r['history']):r['action'] for r in cert['strategy']['actions']}
assert set(pol)=={h for d in range(3) for h in product(range(6),repeat=d)}
lines=(root/'replay/attack_individual_opt_floor.py.stdout.txt').read_text().splitlines()
entries=ast.literal_eval(next(x[len('nonzero types '):] for x in lines if x.startswith('nonzero types ')))
x={sum(1<<a for a in inds):Q(v) for inds,v in entries}
assert all(v>=0 for v in x.values())
def end(h):
 h=tuple(h)
 while len(h)<3:h+=pol[h],
 return h
def payoff(a,z):
 return sum((v*Q(1,sum(bool(mask>>t&1) for t in z)) for mask,v in x.items() if mask>>a&1),Q(0))
z=end(())
slacks=[payoff(a,end(h))-payoff(t,end(h+(t,))) for h,a in pol.items() for t in range(6)]
assert len(slacks)==258 and min(slacks)==0
assert payoff(z[0],z)==1
O=sum(v for mask,v in x.items() if any(mask>>a&1 for a in (1,2,5)))
assert O==Q(2393,569)
assert (np.array([True])+np.array([True])).dtype==np.dtype(bool)
report={'symbolic_identity_membership_assignments':count,'background':'one symbolic arbitrary b>=0; both rational identities have identically zero numerator','fixed_policy_nodes':len(pol),'exact_IC_including_self':len(slacks),'minimum_IC':str(min(slacks)),'root_payoff':str(payoff(z[0],z)),'comparison_cover':str(O),'all_proposal_masses_nonnegative':True,'numpy_boolean_addition_is_OR':True,'scope':'Exact algebra and one fixed-policy feasible proposal; no LP optimality or general welfare claim.'}
(root/'self-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
