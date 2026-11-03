"""Exact parent algebra for the explicit all-m>=53 weak-iid obstruction."""
from fractions import Fraction as F
from pathlib import Path
from math import comb
import json


def translate(coefficients, shift):
    return [sum((c*comb(i,j)*shift**(i-j) for i,c in enumerate(coefficients) if i>=j), F(0))
            for j in range(len(coefficients))]


def g(m, p):
    return (1-(1-p)**m)/(m*p) if p else F(1)


def audit():
    a=F(3,2)
    term=partial=F(1)
    for j in range(1,6):
        term*=a/j
        partial+=term
    assert partial==F(5711,1280)>F(40,9)
    assert translate([9,-21,4],5)==[4,19,4]
    assert translate([45,-212,4],53)==[45,212,4]
    checks=[]
    for m in [5,52,53,54,64,100,200]:
        t=1-a/m
        exact_B=2*(m-1)*g(m,t)
        exact_P=2*g(m,1-t)+g(m,(1-t)/m)
        lower_B=2*(m-1)*(m*m+a*m+a*a)/m**3
        lower_P=F(61,30)-F(3,4*m)
        critical=F(4*m,2*m-1)
        assert lower_B-critical==F(4*m*m-21*m+9,2*m**3*(2*m-1))
        assert lower_P-critical==F(4*m*m-212*m+45,60*m*(2*m-1))
        assert exact_B>=lower_B and exact_P>lower_P
        assert g(m,F(0))==g(m,F(0))==1 and g(m,F(1))==F(1,m)
        # Independently reverse-check the geometric-series formula.
        for p in (t,1-t,(1-t)/m):
            assert g(m,p)==sum(((1-p)**j for j in range(m)),F(0))/m
        if m>=53:
            assert min(lower_B,lower_P)>critical
        checks.append({'m':m,'K':m,'customers':3*m,'topics':m+2,
                       'rational_cut':str(t),'alpha_B':float(exact_B),'alpha_P':float(exact_P),
                       'critical':str(critical),'lower_B_gap':str(lower_B-critical),
                       'lower_P_gap':str(lower_P-critical)})
    return {'scope':'Exact algebra supporting the analytic all-m>=53 proof; SPE policy reviewed separately',
            'taylor_lower_bound':str(partial),'taylor_margin_above_40_over_9':str(partial-F(40,9)),
            'B_numerator_after_shift_m5':[4,19,4],
            'P_numerator_after_shift_m53':[45,212,4],
            'cases':checks,'all_exact_identities_and_geometric_reverse_checks':True}


if __name__=='__main__':
    result=audit()
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
