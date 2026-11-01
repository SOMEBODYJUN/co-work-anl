#!/usr/bin/env python3
"""Exact targeted iid arithmetic; no random search or project imports."""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
from pathlib import Path
import json


def bernoulli_share(opponents, probability, background=0):
    return sum((F(comb(opponents, j)) * probability**j * (1-probability)**(opponents-j)
                / (1+background+j) for j in range(opponents+1)), F(0))


clients8 = [frozenset([0, 2, 3])] * 2 + [frozenset([1])] * 4
clients8 += [frozenset([2]), frozenset([3])]


def alpha8(t, opponents, prefix, action):
    q = [F(0), t, (1-t)/2, (1-t)/2]
    return sum((bernoulli_share(opponents, sum((q[a] for a in client), F(0)),
                               sum(a in client for a in prefix))
                for client in clients8 if action in client), F(0))


def g3(t):
    return 1-t+t*t/3


def g4(t):
    return 1-3*t/2+t*t-t*t*t/4


# Degree bounds 3,2,1 respectively make these rational interpolation checks
# exact polynomial-identity checks, not a numerical survey of instances.
for t in [F(0), F(1,3), F(2,3), F(1)]:
    a1, a2 = alpha8(t, 3, (), 1), alpha8(t, 3, (), 2)
    assert a1 == 4*g4(t)
    assert a1-a2 == (97-219*t+107*t*t-49*t*t*t)/32
for t in [F(0), F(1,2), F(1)]:
    a1, a2 = alpha8(t, 2, (0,), 1), alpha8(t, 2, (0,), 2)
    assert a1 == 4*g3(t)
    assert a2 == F(13,12)+2*t/3+t*t/4
    assert a1-a2 == (35-56*t+13*t*t)/12
for t in [F(0), F(1)]:
    a1, a2 = alpha8(t, 1, (0,1), 1), alpha8(t, 1, (0,1), 2)
    assert a1 == 2-2*t/3
    assert a2 == F(17,12)+7*t/12

assert 4*g4(F(1,2)) == F(15,8) < 2
assert 97-219*F(1,2)+107*F(1,2)**2-49*F(1,2)**3 == F(65,8) > 0
assert 97-219*F(3,5)+107*F(3,5)**2-49*F(3,5)**3 == -F(808,125) < 0
assert 35-56*F(2,3)+13*F(2,3)**2 == F(31,9) > 0
assert 35-56+13 < 0
assert 4*g3(F(2,3)) == F(52,27) < 2
assert alpha8(F(7,15), 1, (0,1), 1) == F(76,45) < 2
assert alpha8(F(7,15), 1, (0,1), 1) == alpha8(F(7,15), 1, (0,1), 2)

X, Y = tuple(range(3)), tuple(range(3,6))
clients36 = [frozenset([x,y]) for x in X for y in Y]
for i in combinations(X, 2):
    for j in combinations(Y, 2):
        clients36 += [frozenset(i+j)] * 3
assert len(clients36) == 36
for action in range(6):
    assert sum(action in c and len(c) == 2 for c in clients36) == 3
    assert sum(action in c and len(c) == 4 for c in clients36) == 18
    value = sum((sum((F(1,1+sum(a in c for a in z)) for c in clients36 if action in c),F(0))
                 for z in product(range(6), repeat=3)),F(0))/216
    assert value == F(305,36)
assert 3*bernoulli_share(3,F(1,3))+18*bernoulli_share(3,F(2,3)) == F(305,36) < 10

result = {
    "status": "Exact arithmetic for two specified pressures; EX-IID remains OPEN",
    "eight_customer_root_lambda4_strict_upper": "15/8",
    "eight_customer_prefix0_lambda3_strict_upper": "52/27",
    "eight_customer_prefix01_lambda2_exact": "76/45",
    "eight_customer_actual_payoffs": ["2", "2", "2"],
    "replicated36_k1_lambda4_exact": "305/36",
    "replicated36_all_k_root_lambda_extra_upper": "12-3/e-9/e^2<10",
    "all_k_scope": "Analytic integral proof in extra_iid_review.md; no finite extrapolation",
}
Path(__file__).with_name("extra_iid_audit.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result))
