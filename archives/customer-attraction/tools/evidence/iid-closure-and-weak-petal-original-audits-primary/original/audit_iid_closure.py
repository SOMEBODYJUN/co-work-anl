"""Exact fixed-instance audit; no finite search and no external solver.

Rebuilds the existing eight-customer SPE and its symmetric mixed Nash in
Q(sqrt(669)).  This is a logical closure of established results, not a new
customer-attraction counterexample.
"""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
import json


class Q:
    """a + b sqrt(669), with exact comparisons."""
    def __init__(self, a=0, b=0):
        self.a, self.b = F(a), F(b)
    @staticmethod
    def coerce(x):
        return x if isinstance(x, Q) else Q(x)
    def __add__(self, x):
        x = self.coerce(x)
        return Q(self.a+x.a, self.b+x.b)
    __radd__ = __add__
    def __neg__(self):
        return Q(-self.a, -self.b)
    def __sub__(self, x):
        return self + -self.coerce(x)
    def __rsub__(self, x):
        return self.coerce(x) + -self
    def __mul__(self, x):
        x = self.coerce(x)
        return Q(self.a*x.a+669*self.b*x.b, self.a*x.b+self.b*x.a)
    __rmul__ = __mul__
    def __truediv__(self, x):
        x = self.coerce(x)
        den = x.a*x.a-669*x.b*x.b
        return self*Q(x.a/den, -x.b/den)
    def __pow__(self, n):
        assert n >= 0
        ans = Q(1)
        for _ in range(n):
            ans *= self
        return ans
    def __eq__(self, x):
        x = self.coerce(x)
        return self.a == x.a and self.b == x.b
    def sign(self):
        if not self.b:
            return (self.a > 0)-(self.a < 0)
        if not self.a or (self.a > 0) == (self.b > 0):
            return (self.b > 0)-(self.b < 0)
        rat = self.a*self.a-669*self.b*self.b
        return ((rat > 0)-(rat < 0))*((self.a > 0)-(self.a < 0))
    def __lt__(self, x):
        return (self-self.coerce(x)).sign() < 0
    def __le__(self, x):
        return (self-self.coerce(x)).sign() <= 0
    def __gt__(self, x):
        return (self-self.coerce(x)).sign() > 0
    def __ge__(self, x):
        return (self-self.coerce(x)).sign() >= 0
    def __str__(self):
        return f'{self.a} + ({self.b})sqrt(669)'


# Each entry is one different unit customer, represented by covered labels.
customers = [{0, 2, 3}, {0, 2, 3}, {1}, {1}, {1}, {1}, {2}, {3}]
last = [[1,1,1,1], [1,2,3,2], [1,3,1,1], [1,2,1,1]]


def utility(a, profile):
    return sum((F(1, sum(b in row for b in profile))
                for row in customers if a in row), F())


def welfare(profile):
    return sum(any(a in row for a in profile) for row in customers)


def action(h):
    return 0 if not h else 1 if len(h) == 1 else last[h[0]][h[1]]


def finish(h):
    h = tuple(h)
    while len(h) < 3:
        h += (action(h),)
    return h


comparisons = 0
for depth in range(3):
    for h in product(range(4), repeat=depth):
        z = finish(h)
        for a in range(4):
            assert utility(action(h), z) >= utility(a, finish(h+(a,)))
            comparisons += 1
assert finish(()) == (0,1,1)
assert welfare(finish(())) == 6
assert max(map(welfare, product(range(4), repeat=3))) == 8

# Matched rational primal and correlated dual for the true security value.
p = [F(0),F(15,23),F(4,23),F(4,23)]
dual = [((1,1), F(3,23)), ((1,2), F(10,23)), ((1,3), F(10,23))]
v = F(44,23)
assert min(sum(p[a]*utility(a, B+(a,)) for a in range(4))
           for B in combinations_with_replacement(range(4), 2)) == v
caps = [sum(prob*utility(a, B+(a,)) for B,prob in dual) for a in range(4)]
assert caps == [F(26,23),v,v,v]

t = Q(F(30,7), F(-1,7))
q = [Q(0), t, (1-t)/2, (1-t)/2]
assert 0 < t and t < 1 and sum(q) == 1
assert 7*t*t-60*t+33 == 0
alpha = []
for a in range(4):
    alpha.append(sum(q[b]*q[c]*utility(a, (a,b,c))
                     for b,c in product(range(4), repeat=2)))
rho = Q(F(1448,49), F(-52,49))
assert alpha[1:] == [rho,rho,rho]
assert alpha[0] < rho
assert 2 < rho
assert alpha[1] == 4-4*t+F(4,3)*t*t
assert alpha[2] == F(5,4)+t+F(3,4)*t*t
expected_welfare = sum(q[a]*q[b]*q[c]*welfare((a,b,c))
                        for a,b,c in product(range(4), repeat=3))
assert expected_welfare == 3*rho
assert 6 < F(544,87) and F(544,87) < expected_welfare

print(json.dumps({
    'scope': 'Existing eight-customer SPE logically refutes W >= Z_3 and all-iid static dual cap W/3; true security bridge remains unrefuted.',
    'unit_customers': len(customers), 'full_ordered_history_comparisons': comparisons,
    'path': finish(()), 'W': 6, 'OPT_3': 8,
    'security_v3': str(v), 'W_minus_3v3': str(6-3*v),
    'iid_minimax_rho3': str(rho),
    'symmetric_mixed_Nash_q': [str(x) for x in q],
    'Nash_pure_query_payoffs': [str(x) for x in alpha],
    'Z_3': str(expected_welfare),
    'strict_iid_dual_failure': True,
    'general_half_coverage_proved': False,
    'aggregate_true_security_bridge_proved_or_refuted': False,
}, indent=2))
