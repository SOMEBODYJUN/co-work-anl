"""Independent raw-block checks; general all-history proof is separate.

No discovery program, repository model, SPE solver or controller is imported.
"""
from fractions import Fraction as F
from itertools import product
import json

BLOCKS = [({0}, 3), ({1}, 4), ({2, 3}, 6), ({2, 4}, 6),
          ({0, 3, 4}, 2), ({1, 3, 4}, 2)]
CLIENTS = [frozenset(s) for s, n in BLOCKS for _ in range(n)]

def profit(z, i):
    return sum((F(1, sum(a in s for a in z))
                for s in CLIENTS if z[i] in s), F(0))

def query(z, a):
    return sum((F(1, 1 + sum(b in s for b in z))
                for s in CLIENTS if a in s), F(0))

def main():
    second = (1, 2, 3, 4, 2)
    third = ((2, 2, 2, 2, 2), (2, 2, 3, 2, 2),
             (2, 3, 3, 2, 3), (2, 2, 2, 2, 2),
             (2, 2, 3, 2, 2))
    for a, b in product(range(5), repeat=2):
        vals = [profit((a, b, c), 2) for c in range(5)]
        assert profit((a, b, third[a][b]), 2) == max(vals) >= 5
    for a in range(5):
        vals = [profit((a, b, third[a][b]), 1) for b in range(5)]
        assert vals[second[a]] == max(vals) >= 5
        assert profit((a, second[a], third[a][second[a]]), 0) == 5
    bad = {1: (1, 2, 3), 2: (2, 3, 2), 3: (3, 4, 2), 4: (4, 2, 3)}
    exceptions = {(2, 4): 2, (3, 2): 2, (4, 3): 2}
    for a, z in bad.items():
        assert profit(z, 0) == 5
        assert min(profit(z, i) for i in (1, 2)) >= 5
        assert max(query(z, t) for t in range(5)) <= 5
        v = profit(z, 1)
        for b in range(5):
            if b == z[1]: c = z[2]
            elif query((a,), b) <= v: continue
            else:
                c = exceptions[a, b]
                assert profit((a, b, c), 1) <= v
                assert max(query((a, b, c), t) for t in range(5)) <= 5
            target = profit((a, b, c), 2)
            assert target == max(profit((a, b, d), 2) for d in range(5)) >= 5
    assert [query((0, 1, a), 2) for a in range(5)] == [12, 12, 6, 9, 9]
    assert [query((0, 1, 2), a) for a in range(5)] == [F(5,2), 3, 6, 5, 5]
    assert [query((2, 3, 4), a) for a in range(5)] == [F(11,3), F(14,3), 4, F(10,3), F(10,3)]
    rows = []
    for k in (1, 2, 6, 12, 22):
        m, w = k + 3, 5*k + 23
        tau = F(11,2) + F(5*k*k,k+1)
        weak = 6*m - w - 6
        full = 6*m + tau + 6 - 2*w
        assert weak == k-11 and weak+w+6 == 6*m
        assert full == F(2*k*k-41*k-33,2*(k+1))
        assert full+2*w == 6*m+tau+6
        assert F(5*k,k+1) < 5
        tp = F(5*k,(k+1)*(k+2))
        assert min(6*m-F(31,6),6*m-5,3*m-F(7,3),6*m-6+tp) > 0
        rows.append({'k':k,'m':m,'W_OPT':w,'weak_gap':str(weak),'full_gap':str(full)})
    print(json.dumps({'status':'PASS','scope':'finite core primitives and exact parameter identities; all-history proof separate',
                      'unit_core_clients':len(CLIENTS),'terminal_raw_BR_checks':25,'second_rows':5,'parameter_rows':rows},indent=2))

if __name__ == '__main__': main()
