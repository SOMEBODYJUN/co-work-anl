from fractions import Fraction as F
from copy_protection_dp import CustomerType,Instance,ExactSPESolver,compositions
from myopic_ceiling_dp import MyopicCeilingFloor
import json

def triangle_modules(m):
    types=[]
    for j in range(m):
        types.extend([CustomerType(frozenset({3*j,3*j+1})),
                      CustomerType(frozenset({3*j+1,3*j+2})),
                      CustomerType(frozenset({3*j,3*j+2}))])
    return Instance(tuple(f'T{a}' for a in range(3*m)),tuple(types),m)

def audit():
    reports=[]
    for m in range(1,5):
        ins=triangle_modules(m);exact=ExactSPESolver(ins);ceiling=MyopicCeilingFloor(ins);states=0
        for n in range(m):
            for b in compositions(n,3*m):
                assert exact.threshold(b)==2
                assert ceiling.floor(b)==2
                states+=1
        assert exact.minimum_welfare()==ins.optimal_welfare()==2*m
        assert ceiling.root()==2*m
        reports.append({'m':m,'K':2,'topics':3*m,'customers':3*m,
                        'prefixes':states,'minimum_SPE_welfare':exact.minimum_welfare(),
                        'ceiling_G':str(ceiling.root()),'OPT':ins.optimal_welfare()})
    return reports
if __name__=='__main__':print(json.dumps(audit(),indent=2))
