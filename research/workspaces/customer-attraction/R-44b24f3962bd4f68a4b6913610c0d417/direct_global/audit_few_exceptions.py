"""Fraction audit of the few-early-exceptions analytic certificate candidate.

All comparisons are formulas derived from real full-history SPE deviations.
Membership/corner checks audit the formulas; they do not prove general half.
"""
from fractions import Fraction as F
from pathlib import Path
import json

def parameters(m,r):
    den=m*(m*m-3*m+3)-r*(m*m-2*m+2)
    mu=F(m*(m-1)**2,den)
    cap=F((m-1)*(r+2),(m-2)*r+m-1)
    return mu,cap

def value(m,r,a,b,e,p,d,ell):
    den=p+a+b
    ua=F(a,den) if den else F(0)
    ub=F(b,den) if den else F(0)
    ue=F(e,den) if den else F(0)
    qe=F(e,p+a+1) if e else F(0)
    g=m*ua+ub/2-F(d,p+1)-F(ell,2*m*(p+a+1))+F(d*ell,m*(p+1)*(p+2))
    k=ue-F(r*a,m)+(r*ub-qe)/(m-1)
    mu,_=parameters(m,r)
    return 2*int(den>0)-int(d>0)-g-mu*k

def run():
    cases=0;parameter_cases=0;minimum=None
    for r in range(1,9):
        threshold=(r+1)**2+1
        for m in sorted({threshold,threshold+1,threshold+7,2*threshold,1000}):
            mu,cap=parameters(m,r)
            assert 1<mu<=cap
            assert mu>=F(m,m-1-r)
            q=r+1;s=m-q*q-1
            P=m**3-(r*r+2*r+4)*m*m+(2*r*r+5*r+5)*m-2*r*r-4*r
            assert P==s**3+2*q*q*s*s+(q**4+q-1)*s+q*(q-1)**2+2>0
            parameter_cases+=1
            # Large m uses all potentially extremal p plus adjacent values;
            # small m covers every allowed background p.
            for a in (0,1):
                for b in (0,1):
                    for e in range(r+1):
                        ps=([m-2-r+e] if a else
                            list(range(e,m-1)) if m<=170 else
                            sorted({e,min(m-2,e+1),max(e,r),min(m-2,max(e,r+1)),m-2}))
                        for p in ps:
                            for d,ell in ((0,0),(0,m),(1,0),(1,m),(m,0),(m,m)):
                                v=value(m,r,a,b,e,p,d,ell)
                                assert v>=0,(m,r,a,b,e,p,d,ell,v)
                                minimum=v if minimum is None else min(minimum,v)
                                cases+=1
            for t in range(1,r+1):
                A=m*(m-1)**2-r*(m*m-m+1)
                B=m*(m-2)-r*(m-1)
                assert m*B-A==r-m
                assert A-r*B==(m-1)*(m-1-r)*(m-r)
                assert mu>=F(m*(m-1)*(m-t),A-t*B)
    # Outside the theorem's range the stated template can fail; this is not SPE.
    assert value(5,2,0,0,2,2,1,0)<0
    out={'status':'exact algebra regression passed; analytic proof in companion note',
         'parameter_cases':parameter_cases,'customer_corner_cases':cases,
         'minimum_Q':str(minimum),'r_range':[1,8],
         'includes_template_failure_outside_scope':True,
         'Q_CAG_HALF':'OPEN'}
    Path(__file__).with_name('few_exceptions_audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out))

if __name__=='__main__':run()
