"""Independent bitmask/rational reconstruction; no import of original audit."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, product
import json
from pathlib import Path

A = tuple(range(6))
weights = Counter({(1 << x) | (1 << y): 1 for x in range(3) for y in range(3, 6)})
for left in combinations(range(3), 2):
    for right in combinations(range(3, 6), 2):
        weights[sum(1 << a for a in left + right)] += 3

policy = {}
for depth in range(3):
    for h in product(A, repeat=depth):
        if depth == 0:
            prescribed = 0
        elif depth == 1:
            prescribed = 3 if h[0] < 3 else 0
        else:
            pool = range(3) if h[-1] < 3 else range(3, 6)
            prescribed = min(set(pool).difference(h))
        policy[h] = prescribed

def leaf(h):
    while len(h) < 3:
        h += (policy[h],)
    return h

def income(a, profile, counts):
    return sum((F(w, sum((t >> b) & 1 for b in profile))
                for t, w in counts.items() if (t >> a) & 1), F())

def coverage(profile, counts):
    union = sum(1 << a for a in set(profile))
    return sum(w for t, w in counts.items() if t & union)

def ic_audit(counts):
    gaps = []
    for h, prescribed in policy.items():
        own = income(prescribed, leaf(h), counts)
        for a in A:
            gaps.append(own - income(a, leaf(h + (a,)), counts))
    assert len(gaps) == 258 and min(gaps) >= 0
    return str(min(gaps))

assert len(policy) == 43 and sum(weights.values()) == 36 and len(weights) == 18
actual = leaf(())
assert actual == (0, 3, 4)
assert [income(a, actual, weights) for a in actual] == [10, 12, 12]
W = coverage(actual, weights)
assert W == 34 == sum(income(a, actual, weights) for a in actual)
backgrounds = [actual[:i] + actual[i+1:] for i in range(3)]
matrix = [[income(a, B + (a,), weights) for B in backgrounds] for a in A]
assert matrix[5] == [12, 12, 12] and F(12) - F(W, 3) == F(2, 3)
fractional = [sum((F(3*w, 3 + 2*sum((t >> b) & 1 for b in actual))
                   for t, w in weights.items() if (t >> a) & 1), F()) for a in A]
assert max(fractional) - F(W, 3) == F(1, 105)
Q = list(combinations(range(3), 2)) + list(combinations(range(3, 6), 2))
dual = [sum((income(a, B + (a,), weights) for B in Q), F()) / len(Q) for a in A]
assert dual == [10] * 6
all_B = list(combinations_with_replacement(A, 2))
uniform = [sum((income(a, B + (a,), weights) for a in A), F()) / 6 for B in all_B]
assert len(all_B) == 21 and min(uniform) == 10
optimum = max(coverage(z, weights) for z in product(A, repeat=3))
assert optimum == 36 and 2*W >= optimum and W - 3*F(10) == 4

# Boundary and homogeneity checks keep every ordered history and repeat action.
fixtures = {'zero_customers': Counter(), 'one_full_interest_customer': Counter({63:1}),
            'double_original': Counter({t:2*w for t,w in weights.items()})}
boundary = {name: ic_audit(counts) for name, counts in fixtures.items()}
assert coverage(actual, fixtures['zero_customers']) == 0
assert all(income(a, (a, a, a), fixtures['one_full_interest_customer']) == F(1,3) for a in A)
for h in policy:
    for a in A:
        assert income(a, leaf(h + (a,)), fixtures['double_original']) == 2*income(a, leaf(h + (a,)), weights)
original = json.loads((Path(__file__).parent/'deletion_obstruction_audit.json').read_text())
assert original['query_matrix'] == [[str(v) for v in row] for row in matrix]
assert original['fractional_actual_load_values'] == list(map(str, fractional))
result = {'status':'exact independent reconstruction passed', 'histories':len(policy),
          'original_IC_comparisons':258,'original_min_gap':ic_audit(weights),
          'nonself_comparisons':43*5,'customer_types':len(weights),'unit_customers':sum(weights.values()),
          'W':W,'OPT3':optimum,'static_backgrounds':len(all_B),'static_value':str(min(uniform)),
          'dual_query_values':list(map(str,dual)), 'restricted_support_excess':str(F(2,3)),
          'fractional_excess':str(max(fractional)-F(W,3)), 'boundary_min_gaps':boundary,
          'historical_matrix_and_fractional_fields_match':True}
print(json.dumps(result, indent=2))
