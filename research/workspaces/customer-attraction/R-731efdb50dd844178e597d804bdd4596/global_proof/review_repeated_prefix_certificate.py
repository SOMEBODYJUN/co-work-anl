"""Independent raw membership audit; imports no author's proof or code."""
from itertools import product
from collections import defaultdict
from pathlib import Path
import json

WTS=(420,16,78,1471,799,245,20,405,105,107,10,254,222,24,444,64,72,159)
NAMES=('S','Z0','V0','FB','FA','BQ','MR','CR','BR','QV','MZ','CZ','BZ','QZ','BT','RT','ZT','CL')
PATS=tuple(product((0,1),repeat=5))
CORNERS=((0,0),(0,5),(1,0),(1,5),(5,0),(5,5))
def share(bit,den):
 if not bit:return 0
 assert den in (1,2,3,4,5)
 assert 60%den==0
 return 60//den

def raw(p,c,a,b,q,r,v,z,T,L):
 Uc=share(c,p+c+a+b);Ua=share(a,p+c+a+b);Ub=share(b,p+c+a+b)
 Uq=share(q,p+b+q+r);Ur=share(r,p+b+q+r);Uz=share(z,p+a+v+z)
 h=p+c
 A=[sum(Ua-share(t,h+t+l) for t,l in zip(T,L)),
    sum(Ub-share(l,h+l+a) for l in L),
    sum(share(L[i],h+T[i]+L[i])-share(L[j],h+T[i]+L[j]) for i in range(5) for j in range(5) if i!=j),
    Uc-share(b,p+b+q+r),Uc-share(a,p+a+v+z),Ub-share(q,h+q+a),
    sum(share(l,h+t+l)-share(r,h+t+r) for t,l in zip(T,L)),
    Uc-share(r,p+3),Ub-share(r,h+r+a),Uq-share(v,p+b+2),
    sum(share(l,h+t+l)-share(z,h+t+z) for t,l in zip(T,L)),
    Uc-share(z,p+3),Ub-share(z,h+z+a),Uq-share(z,p+b+2),
    sum(Ub-share(t,h+t+a) for t in T),sum(Ur-share(t,p+b+q+t) for t in T),
    sum(Uz-share(t,p+a+v+t) for t in T),sum(Uc-share(l,p+3) for l in L)]
 assert len(A)==len(WTS)
 return sum(w*x for w,x in zip(WTS,A))

out={'scope':'independent customer-by-customer integer-share audit of 18 true SPE slacks; no author implementation imported','h_coefficient_numerator':WTS[0]-5*WTS[2]-WTS[6]-WTS[10]}
assert out['h_coefficient_numerator']==0
for version in ('repeated','containing_prefix'):
 n=0;minimum=None;corners=defaultdict(lambda:[None]*6);agg_checks=0
 PC=((0,0),(2,1)) if version=='repeated' else ((0,0),(1,0),(2,0),(2,1))
 for p,c in PC:
  for a,b,q,r,v,z in product((0,1),repeat=6):
   cache={}
   for T in PATS:
    for L in PATS:
     G=raw(p,c,a,b,q,r,v,z,T,L);d,ell=sum(T),sum(L);key=(d,ell)
     if key in cache:assert cache[key]==G;agg_checks+=1
     else:cache[key]=G
     R=60000*(2*int(p+c+a+b>0)-int(d>0))-G
     assert R>=0,(version,p,c,a,b,q,r,v,z,T,L,R)
     minimum=R if minimum is None else min(minimum,R);n+=1
   for j,key in enumerate(CORNERS):
    R=60000*(2*int(p+c+a+b>0)-int(key[0]>0))-cache[key]
    kk=(p,c,a,b);corners[kk][j]=R if corners[kk][j] is None else min(corners[kk][j],R)
 out[version]={'literal_columns':n,'aggregate_invariance_checks':agg_checks,'minimum_scaled_residual':minimum,'scale':60000,'corner_table':[{'prefix_load_p':p,'C':c,'A':a,'B':b,'minima':values} for (p,c,a,b),values in sorted(corners.items())]}
path=Path(__file__).with_name('independent_repeated_prefix_audit.json');path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v if not isinstance(v,dict) else {a:b for a,b in v.items() if a!='corner_table'} for k,v in out.items()},indent=2))
