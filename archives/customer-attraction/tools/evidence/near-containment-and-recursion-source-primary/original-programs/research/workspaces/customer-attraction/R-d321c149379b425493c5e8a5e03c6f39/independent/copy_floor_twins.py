"""Exact checks for the failure of zero-cost containment-following floors."""
from fractions import Fraction as F
from math import comb
from copy_protection_dp import CopyProtectionFloor, CustomerType, Instance, compositions
import json


def twins(m,K):
    assert m>=1 and K>=1
    types=[]
    for j in range(m):
        types.extend([CustomerType(frozenset({2*j,2*j+1}),K),
                      CustomerType(frozenset({2*j}),1),
                      CustomerType(frozenset({2*j+1}),1)])
    return Instance(tuple(f'T{a}' for a in range(2*m)),tuple(types),m)


def audit():
    reports=[]
    for m,K in [(1,2),(2,2),(3,3),(4,4)]:
        ins=twins(m,K);dp=CopyProtectionFloor(ins)
        checked=0
        for n in range(m):
            for b in compositions(n,2*m):
                r=m-n
                assert dp.floor(b,r)==F(K,r)+1
                checked+=1
        G=sum((F(K,r)+1 for r in range(1,m+1)),F())
        assert dp.root()==G
        assert ins.optimal_welfare()==m*(K+1)
        assert checked==comb(3*m-1,2*m)
        reports.append({'m':m,'K':K,'states':checked,'G':str(G),
                        'OPT':m*(K+1)})
    for m,K in [(5,12),(7,140),(10,10),(100,100)]:
        H=sum((F(1,r) for r in range(1,m+1)),F())
        G=K*H+m;O=m*(K+1)
        assert O>2*G
        reports.append({'m':m,'K':K,'H':str(H),'G':str(G),
                        'OPT':O,'OPT_minus_2G':str(O-2*G),
                        'ratio':str(F(O)/G)})
    assert sum((F(1,r) for r in range(1,6)),F())==F(137,60)
    assert F(5*13)-(2*(12*F(137,60)+5))==F(1,5)
    assert F(7*141)-(2*(140*sum((F(1,r) for r in range(1,8)),F())+7))==247
    return reports

if __name__=='__main__': print(json.dumps(audit(),indent=2))
