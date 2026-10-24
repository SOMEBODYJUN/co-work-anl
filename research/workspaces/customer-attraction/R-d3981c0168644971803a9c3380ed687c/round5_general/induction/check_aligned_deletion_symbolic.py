"""Formal polynomial cross-multiplication, not a parameter scan or half proof.
Uses only the standard library. Rational identities are checked after multiplying
by their stated positive common denominators.
"""
from pathlib import Path
from fractions import Fraction as Q
import json
HERE=Path(__file__).resolve().parent
N=6
class P:
    def __init__(self,value=0,terms=None):
        self.terms={k:v for k,v in (terms if terms is not None else {(0,)*N:Q(value)}).items() if v}
    def __add__(self,other):
        if not isinstance(other,P):other=P(other)
        out=self.terms.copy()
        for k,v in other.terms.items():out[k]=out.get(k,Q())+v
        return P(terms=out)
    __radd__=__add__
    def __neg__(self):return P(terms={k:-v for k,v in self.terms.items()})
    def __sub__(self,other):return self+-asP(other)
    def __rsub__(self,other):return asP(other)+-self
    def __mul__(self,other):
        other=asP(other);out={}
        for k,v in self.terms.items():
            for l,w in other.terms.items():
                z=tuple(a+b for a,b in zip(k,l));out[z]=out.get(z,Q())+v*w
        return P(terms=out)
    __rmul__=__mul__
    def zero(self):return not self.terms

def asP(value):return value if isinstance(value,P) else P(value)
def var(i):
    e=[0]*N;e[i]=1
    return P(terms={tuple(e):Q(1)})
b,t,r,a,ap,app=[var(i) for i in range(N)]
c=b+t
checks={
 'refund_equals_utility_minus_social_marginal':((t-1)-((c-1)-b)).zero(),
 'sum_deleted_payoffs_equals_rU_minus_marginal':((r-t)*(c-1)+(t-1)*c-(r*(c-1)-b)).zero(),
 'old_potential_decreasing_difference':(r*(c-1)*(c+1)-b*(c+1)-r*c*(c-1)+b*(c-1)-(r*(c-1)-2*b)).zero(),
 'nonnegative_difference_numerator_factor':(r*(c-1)-2*b-((r-2)*b+r*(t-1))).zero(),
}
left=(r-t)*a+(t-1)*ap-((r-t+1)*ap+(t-2)*app)
right=(r-t)*(a-ap)+(t-2)*(ap-app)
checks['deletion_operator_second_difference_factor']=(left-right).zero()
rows=[]
for k in range(1,6):
    original=Q(1,k);marginal=Q(1) if k==1 else Q()
    summed=5*original-marginal
    rows.append({'t':k,'original':str(original),'sum_four_deleted':str(summed),'mean':str(summed/4)})
assert all(checks.values())
result={'status':'formal polynomial identities passed; sign claims use stated r>=2,b>=1,t>=1 and t<=r domains',
        'method':'standard-library exact multivariate polynomial expansion after positive denominator cross-multiplication',
        'scope':'no SPE-repair construction or half proof','checks':checks,'m5_fresh_table':rows,
        'fresh_exclusive_boundary':'t=1,b=0: sum four physical utilities is4; q=1; refund sum0'}
(HERE/'aligned_deletion_symbolic_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
