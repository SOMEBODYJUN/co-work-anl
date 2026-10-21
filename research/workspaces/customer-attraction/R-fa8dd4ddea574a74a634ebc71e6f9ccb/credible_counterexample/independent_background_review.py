"""Exact multivariate identities for an independent background theorem review.

Does not import or run the author's checker or finite parameter scan.
"""
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json


class Poly:
    def __init__(self,terms):
        self.terms={p:c for p,c in terms.items() if c}
    @classmethod
    def constant(cls,c):return cls({(0,)*5:c})
    @classmethod
    def variable(cls,i):
        p=[0]*5;p[i]=1;return cls({tuple(p):1})
    @staticmethod
    def cast(x):return x if isinstance(x,Poly) else Poly.constant(x)
    def __add__(self,x):
        x=self.cast(x);out=defaultdict(int,self.terms)
        for p,c in x.terms.items():out[p]+=c
        return Poly(dict(out))
    __radd__=__add__
    def __neg__(self):return Poly({p:-c for p,c in self.terms.items()})
    def __sub__(self,x):return self+-self.cast(x)
    def __rsub__(self,x):return self.cast(x)+-self
    def __mul__(self,x):
        x=self.cast(x);out=defaultdict(int)
        for p,c in self.terms.items():
            for q,d in x.terms.items():out[tuple(a+b for a,b in zip(p,q))]+=c*d
        return Poly(dict(out))
    __rmul__=__mul__
    def __pow__(self,n):
        out=Poly.constant(1)
        for _ in range(n):out=out*self
        return out
    def substitute(self,i,value):
        out=Poly.constant(0)
        for p,c in self.terms.items():
            q=list(p);q[i]=0
            out+=Poly({tuple(q):c})*self.cast(value)**p[i]
        return out


def same(a,b):
    assert a.terms==b.terms,(a-b).terms


k,b,d,h,t=[Poly.variable(i) for i in range(5)]
common=k*(k-1)*(2*k-5)
an=2*(k-2)*(k-1)*(2*k-5)
bn=(7*k-16)*(k-1)
cn=k*(k-4)
dn=an+bn-common
en=cn*(k-1)
z=b-k+5
q=(4*k*k-11*k+4)*d*d-10*(k-1)*(k-2)*d+k*(k-4)*(k-5)
n=(an*d*(b+d)*(b+1+h)+(bn*d+cn*h)*(b+k)*(b+d)
   -common*d*(b+k)*(b+1+h))
n0=d*((b+1)*dn*z+(d-1)*(an*(b+1)+bn*(b+k)))
n1=(b+k)*((k-1)*q+(dn*d+en)*z)
same(n.substitute(3,0),n0)
same(n.substitute(3,k-1),n1)
same((k-1)*n,(k-1-h)*n0+h*n1)
same(dn,2*(k-1)**2*(k-2))
same(q,q.substitute(2,1)+(d-1)*(2*k*k-3*k-8)
     +(4*k*k-11*k+4)*(d-1)*(d-2))
same(q.substitute(2,1).substitute(0,t+12),t**3+21*t*t+111*t+20)
same((2*k*k-3*k-8).substitute(0,t+12),2*t*t+45*t+244)
same((4*k*k-11*k+4).substitute(0,t+12),4*t*t+85*t+448)
# Clear positive denominators in the disjoint-catalog bridge gap identity.
# F=(k)/(k-5), 2(k-2)K=(k-2)/(k-3), 4theta=4/(k-5).
same((k-4)*(k-3)-(k-2)*(k-5),Poly.constant(2))

# New signed-error extension: direct rational reconstruction of its strict
# heterogeneous-background example, independently of the author's audit.
def error(kval,bval,dval,tval):
    if not dval:return F(0)
    abase=F(2*(kval-2),kval)
    return (F(dval,bval+dval)-abase*F(dval,bval+kval)
            -min(tval*dval/(kval*(bval+1)),
                 (tval*dval/kval+4-tval)/(bval+kval)))
low=error(12,0,1,F(68,19));high=error(12,10,1,F(68,19))
assert low==F(137,171) and high==F(-5,418)
assert low+110*high==F(-88,171)
assert F(10,11)>F(25,33) and F(1)>F(25,33)

source=Path(__file__).resolve().parents[1]/'background_induction/joint_baseline_half_profit.md'
report={
    'review_status':'Independent analytic review: no fatal objection found',
    'scope':'all integer k>=12, real b>=k-5, integer d in 0..k, real h in 0..k-1',
    'method':'symbolic multivariate integer polynomial identities; no author checker imported',
    'identities_checked':9,
    'core_nonnegative_certificate':{
      'Q':'Q(1)+(d-1)*(2k^2-3k-8)+(4k^2-11k+4)*(d-1)*(d-2)',
      'Q_at_1_k_12_plus_t':'t^3+21t^2+111t+20',
      'difference_k_12_plus_t':'2t^2+45t+244',
      'quadratic_k_12_plus_t':'4t^2+85t+448',
      'N0':'d*((b+1)*D*z+(d-1)*(A*(b+1)+B*(b+k)))',
      'N1':'(b+k)*(Q/(k*(2k-5))+(D*d+E)*z)',
      'variables':'D=A+B-1, E=C*(k-1), z=b-k+5; N=(b+k)*(b+d)*(b+1+h)*slack',
      'interpolation':'N=((k-1-h)*N0+h*N1)/(k-1)'},
    'theta_obligation':'valid: each last-two competition tuple contains exactly k-1 legal themes added after the base history',
    'lower_background_obligation':'valid bridge counterexample at b=k-6; not a half-profit or half-coverage counterexample',
    'signed_error_extension':'valid for k>=4: derivative has constant sign in h; each t gives a bound, so minimizing total error over t preserves it',
    'signed_example_exact':{'low_error':str(low),'high_error':str(high),'total_error':str(low+110*high)},
    'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
    'reviewer_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'limitations':'No claim for k<12 or b<k-5; root half coverage remains open.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
