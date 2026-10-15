"""Independent exact arithmetic audit; no real-exponent claim is inferred here."""
from fractions import Fraction as F
from itertools import product
from random import Random
import hashlib
import json
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[4] / 'research/current/weighted_congestion/common_power_mixture_obstruction.md'


def params(d):
    return F(d,16),d*d+1,d*(d+1),(d*(d+1))**(4*d)


def delta(x,p):
    return 1-F(x-1,x)**p


def differences(d,p):
    r,A,K,W=params(d)
    h=F(W)**(p-d)*(r-F(A)**(p-d)*delta(A,p))
    l=r*F(W)**(p-d)*delta(W,p)-1
    kappa=F(4,d*K**(4*d-2))
    assert kappa*h+l < 0
    assert kappa*h+l <= -F(11,16)
    return h,l


def literal(d,p,bad_h,bad_l):
    r,A,K,W=params(d)
    coefficients=[r/F(W)**d,F(1,(A*W)**d),F(1),r/F(W)**d]
    loads=[W if bad_h else 0,(A-1)*W+(0 if bad_h else W),
           0 if bad_l else 1,W-1+(1 if bad_l else 0)]
    objective=sum((coef*F(load)**p for coef,load in zip(coefficients,loads)),F(0))
    mobile_costs=[coefficients[0]*W**d if bad_h else coefficients[1]*(A*W)**d,
                  coefficients[3]*W**d if bad_l else F(1)]
    assert mobile_costs == [r if bad_h else F(1),r if bad_l else F(1)]
    return objective


def main():
    inequality_degrees=0
    for d in range(32,513):
        r,A,K,W=params(d)
        assert A <= 4**d
        assert F(K*K,4*r) >= 16*r
        assert F(4,d*K**(4*d-2)) <= 1
        assert K <= d**3
        assert 16*r*r <= d*d
        assert 2*d*d-2*d+2 >= 12*d-4
        inequality_degrees += 1
    exact_power_cases=literal_states=mixtures=0
    for d in [32,33,64]:
        ps=sorted(set([1,2,d-1,d,d+1,d+2]))
        differences_by_power={p:differences(d,p) for p in ps}
        exact_power_cases += len(ps)
        if d==32:
            for p in [1,d,d+1]:
                costs={s:literal(d,p,*s) for s in product([False,True],repeat=2)}
                base=costs[False,False]
                h,l=differences_by_power[p]
                for s,value in costs.items():
                    assert value == base+s[0]*h+s[1]*l
                    literal_states += 1
        rng=Random(3851+d)
        for _ in range(8):
            weights={p:F(rng.randrange(1,11),rng.randrange(1,8)) for p in ps}
            dh=sum((weights[p]*differences_by_power[p][0] for p in ps),F(0))
            dl=sum((weights[p]*differences_by_power[p][1] for p in ps),F(0))
            values={s:s[0]*dh+s[1]*dl for s in product([False,True],repeat=2)}
            minimum=min(values.values())
            assert all(any(s) for s,value in values.items() if value==minimum)
            mixtures += 1
    print(json.dumps({
        'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'arithmetic_degrees_checked':[32,512],
        'arithmetic_degree_count':inequality_degrees,
        'exact_integer_power_cases':exact_power_cases,
        'literal_four_resource_states':literal_states,
        'exact_positive_mixtures':mixtures,
        'mixture_seeds':[3883,3884,3915],
        'real_exponents':'covered by independent interval proof, not finite test',
        'continuous_measures':'covered by integrability and pointwise-separation proof'
    },indent=2))


if __name__=='__main__':
    main()
