"""Exact arithmetic diagnosis of PAY on two already certified SPE families.

This does not re-certify their strategy trees or prove general PAY. The all-n
positive formula is proved in strategy_and_pay_review.md, not by this loop.
"""
from fractions import Fraction as Q
import json


def charge(m, k, t, entries):
    total = Q(0)
    for b, d, count in entries:
        if d:
            value = 1 - Q(2*(k-2)*d, m*(b+k)) - min(
                t*d / (m*(b+1)), (t*d/m+4-t)/(b+k))
            total += count * value
    return total


def minimum(m, k, entries):
    points = {Q(0), Q(4)}
    points.update(Q(4*m*(b+1), d*(k-1)+m*(b+1))
                  for b, d, count in entries if d)
    return min((charge(m, k, t, entries), t) for t in points)


atoms = [(set(a), count) for a, count in [
    ('A',30), ('B',7), ('C',5), ('D',7), ('CE',2),
    ('CF',2), ('BEF',6), ('CEF',4), ('DEF',6)]]
rows = []
expected = {2:(Q(149,5),Q(16,5)), 3:(Q(91,4),Q(8,3)),
            4:(Q(345,28),Q(16,7))}
for k in (2,3,4):
    entries = [((4-k)*int('A' in s), len(s & set('ABCD')), count)
               for s, count in atoms]
    value, t = minimum(4, k, entries)
    assert (value,t) == expected[k]
    rows.append({'k':k, 't':str(t), 'charge':str(value),
                 'twice_actual_prefix_payoff':str(20*(4-k)),
                 'margin':str(20*(4-k)-value)})
all_big = []
for n in range(2,31):
    entries = [(n-2,1,n), (0,1,n-1)]
    t = Q(4*n,n+1)
    value = charge(n,2,t,entries)
    formula = 2*n-5 + Q(4*(n-2),n*n-1)
    margin = 2*(n-2)-value
    assert value == formula
    assert margin == Q((n-2)**2+3,n*n-1) > 0
    all_big.append({'n':n, 't':str(t), 'charge':str(value),
                    'margin':str(margin)})
print(json.dumps({'reserve_69':rows,'all_big_finite_formula_checks':all_big,
                  'scope':'arithmetic diagnosis; general all-n formula in prose; no new SPE or general PAY proof'},
                 ensure_ascii=False, indent=2))
