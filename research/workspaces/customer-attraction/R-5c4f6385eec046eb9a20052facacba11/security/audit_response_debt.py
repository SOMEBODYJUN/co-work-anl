"""Independent standard-library exact audit of the local response identity."""
from fractions import Fraction as F
import itertools
import json
from pathlib import Path


def check(background, probability, indicator, load):
    # A selected query covers the customer, hence its branch load is >=1.
    assert all(not i or c >= 1 for i,c in zip(indicator,load))
    t=sum((p*i for p,i in zip(probability,indicator)),F())
    L=sum((p*c for p,c in zip(probability,load)),F())
    A=background+1+L
    D=sum((p/(background+c) for p,i,c in zip(probability,indicator,load) if i),F())
    covariance=sum((p*i*c for p,i,c in zip(probability,indicator,load)),F())-t*L
    J=sum((p*(background+c-A)**2/(background+c)
           for p,i,c in zip(probability,indicator,load) if i),F())
    rhs=(t-covariance+J)/A**2
    assert D-t/A == rhs
    diameter=max(load)-min(load)
    assert covariance <= diameter*t*(1-t)
    cross_stable=all(load[a]<=1+load[b]
        for a in range(len(load))for b in range(len(load))
        if indicator[a] and not indicator[b])
    if cross_stable:
        assert covariance<=t*(1-t)
        assert D>=t/A
    if diameter<=1:
        assert covariance<=t
        assert D>=t/A
    return diameter<=1,cross_stable


def main():
    allchecks=stable=crossstable=0
    # Includes zero-probability branches and the t=0, t=1 degeneracies.
    for background in range(4):
        for masses in itertools.product(range(4),repeat=3):
            total=sum(masses)
            if not total:continue
            probability=tuple(F(v,total)for v in masses)
            for indicator in itertools.product(range(2),repeat=3):
                for load in itertools.product(range(5),repeat=3):
                    if any(i and c==0 for i,c in zip(indicator,load)):continue
                    s,cs=check(background,probability,indicator,load)
                    stable+=s;crossstable+=cs
                    allchecks+=1
    necessary=0
    for background in range(4):
        for included_load in range(1,8):
            for excluded_load in range(8):
                d=included_load-excluded_load
                if d<=1:continue
                eps=F(d-1,2*d)
                D=eps/F(background+included_load)
                Fx=eps/(background+1+eps*included_load+(1-eps)*excluded_load)
                assert D<Fx
                necessary+=1
    result=dict(status='exact_pass',local_identities=allchecks,
                diameter_at_most_one_cases=stable,
                cross_membership_stable_cases=crossstable,
                exact_necessity_witnesses=necessary,
                scope='Scalar identity and sufficient-condition regression; not a general SPE proof')
    path=Path(__file__).with_name('response_debt_audit.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))

if __name__=='__main__':main()
