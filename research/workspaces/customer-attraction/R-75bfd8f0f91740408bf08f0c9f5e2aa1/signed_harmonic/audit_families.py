"""Exact regression for symbolic complete-SPE families; no SPE scan."""
from fractions import Fraction as F
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT))
from customer_attraction import Instance, CustomerType
from audit_known import budgets


def family(n):
    H = sum((F(1, j) for j in range(1, n+1)), F(0))
    # Literature sharp family, actual A^n; optimum A plus n-1 singletons.
    sharp = Instance(tuple(map(str, range(n))),
                     (CustomerType(frozenset({0}), n),)+tuple(
                         CustomerType(frozenset({j}), 1) for j in range(1,n)), n)
    sharpActual = (n,)+(0,)*(n-1)
    sharpOpt = (1,)*n
    a = budgets(sharp, sharpActual, sharpOpt)
    assert a['B'] == a['D'] == n-F(1,n+1)
    assert a['outside'] == 0

    # Fractional-actual-load failure family, actual B^(n-1)A.
    frac = Instance(('A','B','Q','D'), (
        CustomerType(frozenset({0}),n-1), CustomerType(frozenset({2}),1),
        CustomerType(frozenset({0,3}),1),
        CustomerType(frozenset({1,2,3}),n*(n-1))), n)
    b = budgets(frac, (1,n-1,0,0), (n-1,0,1,0))
    assert b['B'] == n*H and b['D'] == F(n*(n+1),2)
    assert b['B_gap'] <= 0 and b['D_gap'] <= 0

    # Prefix-balance family, n>=4; actual AB^(n-1), opt all n leaves.
    if n >= 4:
        types = []
        for j in range(n):
            leaf = j+2
            types += [CustomerType(frozenset({leaf}), n-2),
                      CustomerType(frozenset({1,leaf}), n-2)]
            types.append(CustomerType(frozenset({0,leaf}) if j<n-1 else
                                      frozenset({0,1,leaf}), 1 if j<n-1 else n-1))
        prefix = Instance(tuple(map(str, range(n+2))), tuple(types), n)
        c = budgets(prefix, (1,n-1)+(0,)*n, (0,0)+(1,)*n)
        assert -c['B_gap'] == -c['D_gap'] == F(n-1,2)+F(2,n+1)
    else:
        c = None

    # Collision-free family, n=k+1; actual C_1,...,C_k,D.
    k = n-1
    types = [CustomerType(frozenset({3*i,3*i+1,3*i+2}),2)
             for i in range(k)]
    types += [CustomerType(frozenset({3*i}),1) for i in range(k)]
    types += [CustomerType(frozenset({3*i+1 for i in range(k)}|{3*k}),1),
              CustomerType(frozenset({3*k}),1)]
    collision = Instance(tuple(map(str,range(3*k+1))), tuple(types),n)
    collisionActual = tuple(int(a%3==2 or a==3*k) for a in range(3*k+1))
    collisionOpt = tuple(int(a%3==0) for a in range(3*k+1))
    d = budgets(collision, collisionActual, collisionOpt)
    assert d['B_gap'] == d['D_gap'] == -1
    return {'players':n, 'sharp':a, 'fractional':b, 'prefix':c, 'collision_free':d}


if __name__ == '__main__':
    report = {'status':'exact formula regression, not a proof of complete-SPE families',
              'range':'2 <= m <= 30', 'representative_rows':[family(n) for n in range(2,31)]}
    (HERE/'family_formula_audit.json').write_text(json.dumps(report,indent=2,default=str)+'\n')
    print(json.dumps({'status':report['status'], 'range':report['range'], 'all_assertions_passed':True},indent=2))
