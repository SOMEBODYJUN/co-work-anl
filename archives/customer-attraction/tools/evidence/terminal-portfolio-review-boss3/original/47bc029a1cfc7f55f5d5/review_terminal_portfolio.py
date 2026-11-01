"""Independent literal hidden-bit and budget identity audit of terminal portfolio."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent

def share(n,d):return F(n,d) if n else F()
params=[(F(),F(),F(),F(),(F(),)*13),(F(1,7),F(2,9),F(1,13),F(3,11),tuple(F(2,11) if j==5 else F() for j in range(13))),(F(4,9),F(1,8),F(),F(1,17),tuple(F(j+1,20) for j in range(13)))]
qs=[(0,)*13,(1,)*13,tuple(j%2 for j in range(13))]+[tuple(int(j==k) for j in range(13)) for k in (0,5,7,11,12)]
count=identities=0
for n in range(1,6):
 for p in range(6-n):
  for ell in range(p,6):
   for t,q,(am,al,bm,bl,mus) in product(range(2),qs,params):
    M=sum(mus);Q=sum(v*b for v,b in zip(mus,q));literal=[]
    for fs in product(range(2),repeat=n):
     g=fs[-1];z=p+t+sum(fs);alphas=(am,)*(n-1)+(al,);betas=(bm,)*(n-1)+(bl,)
     h=share(t,z)+sum((be+aa/F(ell+1))*f for be,aa,f in zip(betas,alphas,fs))-M*share(g,z)+F(Q,p+t+sum(fs[:-1])+1)
     literal.append(h)
     u=F(13,17);last=F(19,23);K=F(29,31)
     lhs=u+sum(alphas)*last+sum(betas)*K-h
     rhs=(u-share(t,z))+sum(aa*(last-F(f,ell+1))+be*(K-f) for aa,be,f in zip(alphas,betas,fs))+sum(mu*(share(g,z)-F(bit,p+t+sum(fs[:-1])+1)) for mu,bit in zip(mus,q))
     assert lhs==rhs;identities+=1
    compressed=min(share(t-M*g,p+t+s+g)+F(am*s+al*g,ell+1)+bm*s+bl*g+F(Q,p+t+s+1) for s,g in product(range(n),range(2)))
    assert min(literal)==compressed;count+=1
out={'scope':'independent general nonnegative-row identity and exact literal-vs-count checks, not LP/SPE/global-half audit','exact_identity_checks':identities,'exact_minimum_checks':count,'alpha_beta_mu_patterns':len(params),'query_bit_patterns':len(qs),'K_coefficient':'(n-1)*beta_middle+beta_last','status':'PASS'}
(HERE/'review_terminal_portfolio.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
