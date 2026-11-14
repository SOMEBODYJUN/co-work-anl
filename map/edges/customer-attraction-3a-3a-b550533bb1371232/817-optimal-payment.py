from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib
import json
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: b550-exact-817-optimal.py PATH_TO_fractional_global_raw.json")
source = Path(sys.argv[1]).read_bytes()
assert hashlib.sha256(source).hexdigest() == "0955adeb922963dbfbe3aed265f55d98dfac0b30e6256ed61a9b2205af166a02"
game = json.loads(source)
weights = {int(mask): weight for mask, weight in game["customer_mask_multiplicities"].items()}
policy = {tuple(row["history"]): row["action"] for row in game["policy"]}
labels = range(6)

def included(mask, label):
    return bool(mask & (1 << label))

def alpha(mask, probability):
    return sum(probability[label] for label in labels if included(mask, label))

def dot(left, right):
    return sum(a * b for a, b in zip(left, right))

def query(background):
    denominator = {mask: 1 + 2 * alpha(mask, background) for mask in weights}
    return [sum(weights[mask] / denominator[mask] for mask in weights if included(mask, a)) for a in labels]

def leaf(history):
    while len(history) < 3:
        history += (policy[history],)
    return history

def payoff(slot, outcome):
    return sum(
        Fraction(weight, sum(included(mask, a) for a in outcome))
        for mask, weight in weights.items()
        if included(mask, outcome[slot])
    )

histories = {h for depth in range(3) for h in product(labels, repeat=depth)}
assert set(policy) == histories
assert all(payoff(len(h), leaf(h)) >= payoff(len(h), leaf(h + (a,))) for h in histories for a in labels)
actual = leaf(())
assert actual == (0, 3, 4)
welfare = sum(payoff(i, actual) for i in range(3))
assert welfare == 597

p0 = [Fraction(a, 10000) for a in (1085, 1981, 606, 2224, 2160, 1944)]
q0 = [Fraction(a, 10000) for a in (3175, 1349, 438, 1824, 1726, 1488)]
assert sum(p0) == sum(q0) == 1 and min(p0) > 0 and min(q0) > 0
prices = query(q0)
tangent_slopes = [
    sum(weight * alpha(mask, p0) / (1 + 2 * alpha(mask, q0)) ** 2
        for mask, weight in weights.items() if included(mask, a))
    for a in labels
]
level = Fraction(41717, 250)
tangent_lower = dot(p0, prices) + 2 * (dot(q0, tangent_slopes) - max(tangent_slopes))
assert level < tangent_lower <= max(prices) < Fraction(166887, 1000)

# Each row gives five terms (source label, destination label, step in units of 1/10000,
# multiplier in units of 1/10000), all with nonnegative multiplier.
# For each label the two rows lower-bound +p[label] and -p[label], respectively.
multipliers = (
    ((0,1,100,808),(0,3,100,3910),(0,4,100,3422),(0,5,100,3081),(2,5,200,824)),
    ((1,0,100,743),(3,0,100,3951),(4,0,100,3521),(5,0,100,3010),(5,2,100,1613)),
    ((1,0,100,766),(1,2,100,429),(1,3,100,1267),(1,4,100,1313),(1,5,100,858)),
    ((0,1,100,787),(2,1,100,441),(3,1,100,1309),(4,1,100,1373),(5,1,100,835)),
    ((0,3,100,1634),(2,1,100,483),(2,3,100,445),(2,4,100,1853),(2,5,100,8003)),
    ((1,2,100,388),(3,0,100,1633),(3,2,100,516),(4,2,100,1977),(5,2,100,7888)),
    ((3,0,100,3915),(3,1,100,1316),(3,2,100,1017),(3,4,100,159),(5,2,100,1074)),
    ((0,3,100,3945),(1,3,100,1259),(2,3,100,997),(2,5,100,1140),(4,3,100,230)),
    ((4,0,100,3455),(4,1,100,1368),(4,2,100,1082),(4,3,100,177),(5,2,100,812)),
    ((0,4,100,3487),(1,4,100,1318),(2,4,100,1064),(2,5,100,873),(3,4,100,212)),
    ((3,0,100,1157),(4,0,100,23),(4,1,100,901),(5,0,100,3519),(5,2,100,7945)),
    ((0,3,100,1024),(0,5,100,3637),(1,3,100,33),(1,4,100,760),(2,5,100,7945)),
)
low = [Fraction(a, 1000) for a in (84, 187, 37, 207, 201, 170)]
high = [Fraction(a, 1000) for a in (133, 209, 84, 238, 231, 219)]

for index, terms in enumerate(multipliers):
    a, sign = index // 2, 1 - 2 * (index % 2)
    coefficients = [Fraction(sign if b == a else 0) for b in labels]
    for src, dst, step, weight in terms:
        q = q0.copy()
        q[src] -= Fraction(step, 10000)
        q[dst] += Fraction(step, 10000)
        assert min(q) >= 0 and sum(q) == 1 and weight > 0
        coefficients = [
            old - Fraction(weight, 10000) * (g - level)
            for old, g in zip(coefficients, query(q))
        ]
    assert min(coefficients) >= (low[a] if sign > 0 else -high[a])

# If p is free-fractional optimal, query(q)·p >= level for each q above.
# The previous inequalities imply low <= p <= high. Bound each summand of
# the original rolewise mean-load payment separately on that box and simplex.
bounds = []
for i in range(3):
    branches = [leaf(actual[:i] + (a,)) for a in labels]
    deleted = [z[:i] + z[i+1:] for z in branches]
    bound = Fraction()
    for mask, weight in weights.items():
        numerator = min(alpha(mask, high), 1 - alpha(63 ^ mask, low))
        loads = [sum(included(mask, b) for b in z) for z in deleted]
        denominator = 1 + max(dot(loads, low), 2 - dot([2 - load for load in loads], high))
        bound += weight * numerator / denominator
    bounds.append(bound)

assert all(bound < limit for bound, limit in zip(bounds, [195, 190, 201]))
assert sum(bounds) < 585 < welfare
print("verified", {"W": str(welfare), "tangent_lower_floor": str(level), "payment_upper": 585,
                   "exact_role_bounds": list(map(str, bounds))})
