"""Independent exact symbolic reconstruction; Python standard library only."""
from pathlib import Path
from fractions import Fraction as F
import json


def poly(x):
    return x if isinstance(x,dict) else ({(0,0):F(x)} if x else {})


def plus(a,b):
    out=dict(poly(a))
    for key,val in poly(b).items():out[key]=out.get(key,F())+val
    return {k:v for k,v in out.items() if v}


def times(a,b):
    out={}
    for (i,j),u in poly(a).items():
        for (k,l),v in poly(b).items():
            key=(i+k,j+l);out[key]=out.get(key,F())+u*v
    return {k:v for k,v in out.items() if v}


class RF:
    """Rational functions of formal h,r, with exact polynomial coefficients."""
    def __init__(self,n=0,d=1):self.n,self.d=poly(n),poly(d)
    @staticmethod
    def cast(x):return x if isinstance(x,RF) else RF(x)
    def __add__(self,x):
        x=self.cast(x);return RF(plus(times(self.n,x.d),times(x.n,self.d)),times(self.d,x.d))
    __radd__=__add__
    def __neg__(self):return RF({k:-v for k,v in self.n.items()},self.d)
    def __sub__(self,x):return self+-self.cast(x)
    def __rsub__(self,x):return self.cast(x)+-self
    def __mul__(self,x):
        x=self.cast(x);return RF(times(self.n,x.n),times(self.d,x.d))
    __rmul__=__mul__
    def __truediv__(self,x):
        x=self.cast(x);assert x.n;return RF(times(self.n,x.d),times(self.d,x.n))
    def __rtruediv__(self,x):return self.cast(x)/self
    def zero(self):return not self.n


h,r=RF({(1,0):F(1)}),RF({(0,1):F(1)})
verified=[]
for a in (0,1):
    for b in (0,1):
        f_a=a/(h+1);f_b=b/(h+1)
        left=f_b+(a/(h+a+r*b) if a else RF())
        right=f_a+(b/(h+r*a+b) if b else RF())
        assert (left-right).zero()
        P=(r*a/(h+r*a+b) if a else RF())+(r*b/(h+a+r*b) if b else RF())
        E=(RF() if a+b==0 else
           (r-1)*h/((h+r)*(h+1)) if a+b==1 else
           ((2*r-2)*h+r-2)/((h+r+1)*(h+1)))
        assert (P-left-E).zero()
        hb=h+b
        lower=b/(hb+1)+(a/(hb+a+(r-1)*b) if a else RF())
        delta=b/((h+1)*(h+2))
        assert (left-lower-delta).zero()
        verified.append(dict(a=a,b=b,kernel_symmetry=True,endpoint_identity=True,staircase_identity=True))

single=h/((h+1)*(h+2));double=2*h/((h+1)*(h+3))
assert (F(1,6)-single-(h-1)*(h-2)/(6*(h+1)*(h+2))).zero()
assert (F(4,15)-double-2*(h-2)*(2*h-3)/(15*(h+1)*(h+3))).zero()
assert (h/(h+3)-single-h*(h*h+2*h-1)/((h+1)*(h+2)*(h+3))).zero()
assert (h/(h+3)-double-h*(h-1)/((h+1)*(h+3))).zero()
checks=0
for load in range(1,501):
    for e in (F(load,(load+1)*(load+2)),F(2*load,(load+1)*(load+3))):
        for suffix_load in range(4):
            assert e<=F(load,load+suffix_load);checks+=1
report=dict(status='independent symbolic identities passed',coefficient_cases=verified,
            cohort_inequalities=checks,
            logical_scope='fixed H reply-chain endpoints and staircase identity; not global SPE payment')
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
