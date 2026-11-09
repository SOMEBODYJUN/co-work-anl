"""Verify the exact fixed-path one-added-label obstruction using the standard library."""
import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from math import comb
from pathlib import Path

F = Fraction
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("point", type=Path, help="Frozen original private-point JSON")
point_bytes = parser.parse_args().point.read_bytes()
assert sha256(point_bytes).hexdigest() == "08ca100b2cfa8b5e878193c49b27bb73b0cdbb2addb7fefe52cdfecfe8b95b5f"

weights = []
membership = []
for (mask, degree, reply_degree, overlap), mass in json.loads(point_bytes)["positive_types"]:
    for subset in combinations(range(6), degree):
        comparison = sum(1 << index for index in subset)
        reply = {
            (0, 0): 0,
            (degree, degree): comparison,
            (6 - degree, 0): 63 ^ comparison,
            (6, degree): 63,
        }[reply_degree, overlap]
        membership.append(tuple((bits >> i) & 1 for bits in (mask, comparison, reply) for i in range(6)))
        weights.append(F(mass) / comb(6, degree))
assert len(set(membership)) == len(weights) == 117
assert all(weight > 0 for weight in weights)

prefix = [sum(bits[:4]) for bits in membership]
payoffs = [
    sum(weight * F(bits[j], sum(bits[:6])) for weight, bits in zip(weights, membership) if bits[j])
    for j in range(6)
]
assert sum(payoffs) == 1

def old_last_quote(penultimate, last):
    return sum(
        weight * F(bits[last], p + bits[penultimate] + 1)
        for weight, bits, p in zip(weights, membership, prefix)
    )

strict_bad_actions = {5: F(34953296381, 968958877616)}
strict_bad_actions.update({a: F(32131453849, 726719158212) for a in range(12, 18)})
theta = {}
for action, gap in strict_bad_actions.items():
    quotes = [old_last_quote(action, last) for last in range(18)]
    theta[action] = max(quotes)
    min_source = min(
        sum(weight * F(bits[action], p + 1 + bits[last])
            for weight, bits, p in zip(weights, membership, prefix))
        for last, quote in enumerate(quotes) if quote == theta[action]
    )
    assert min_source - payoffs[4] == gap

def row_safety(position):
    return [F(1, sum(bits[:position]) + 6 - position) for bits in membership], payoffs[position]

def row_block(action):
    return [-F(1, p + bits[action] + 1) for bits, p in zip(membership, prefix)], -theta[action]

def row_source(last):
    return [
        F(1, p + 1 + (bits[last] if last < 18 else 1))
        for bits, p in zip(membership, prefix)
    ], payoffs[4]

def last_after_new(last):
    if last == 18:
        return F(0), [F(1, p + 2) for p in prefix]
    intercept = sum(weight * F(bits[last], p + 1) for weight, bits, p in zip(weights, membership, prefix))
    slope = [-F(bits[last], (p + 1) * (p + 2)) for bits, p in zip(membership, prefix)]
    return intercept, slope

def row_best(last, competitor):
    intercept, slope = last_after_new(last)
    other_intercept, other_slope = last_after_new(competitor)
    return [a - b for a, b in zip(other_slope, slope)], intercept - other_intercept

expected = [
    F(57717224941, 787279088063), F(57717224941, 787279088063),
    F(59021226681, 787279088063), F(412900756571, 4723674528378),
    F(12649356467, 726719158212), F(32131453849, 1453438316424),
    *([F(84264935023, 4360314949272)] * 6),
    *([F(34953296381, 1937917755232)] * 6), F(39334587019, 1937917755232),
]
cross_reply = {4: 16, 6: 16, 7: 12, 8: 12, 9: 12, 10: 16, 11: 17}
for last in range(19):
    if last < 4:
        rows = [(F(1, 13), row_source(last))]
        rows += [(F(2, 13), row_best(last, b)) for b in range(6, 12)]
    elif last in cross_reply:
        a = cross_reply[last]
        rows = [(F(1, 3), row) for row in (row_block(a), row_source(last), row_best(last, a))]
    elif last == 5 or 12 <= last <= 17:
        rows = [(F(1, 2), row) for row in (row_block(last), row_source(last))]
    else:
        rows = [(F(33, 98), row_safety(3)), (F(17, 98), row_safety(5))]
        rows += [(F(4, 49), row_best(last, b)) for b in range(6, 12)]
    assert all(multiplier > 0 for multiplier, _ in rows)
    combined_coefficients = [
        sum(multiplier * coeffs[i] for multiplier, (coeffs, _) in rows)
        for i in range(len(weights))
    ]
    box_lower = sum(min(coef, 0) * weight for coef, weight in zip(combined_coefficients, weights))
    row_upper = sum(multiplier * rhs for multiplier, (_, rhs) in rows)
    gap = box_lower - row_upper
    assert gap == expected[last] and gap > 0
    print(f"last={last}: box_lower={box_lower}, row_upper={row_upper}, gap={gap}")
