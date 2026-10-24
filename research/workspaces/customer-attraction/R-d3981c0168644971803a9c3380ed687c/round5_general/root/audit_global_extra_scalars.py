"""Exact parameter identities for the economic/insurance counterfamily.

The complete-history proof is separate; this does not claim finite tests prove it.
"""
from fractions import Fraction as F
import json

rows = []
for m in (2, 3, 4, 5, 9):
    root = F(m, m-1)
    middle = F(2) + F(1, m-1)
    last = F(2)
    w = root + (m-2)*middle + last
    opt = 3*m-2
    tau = F(1, 2) + F(2*(m-1), 2*m-1)
    standard = F(1) + F(m, 2*m-1)
    standard_gap = standard-root
    gap = tau-root
    weak = F(opt, 2*m)-root
    assert w == 2*m
    assert 2*w-opt == m+2
    assert gap == F(2*m*m-9*m+5, 2*(2*m-1)*(m-1))
    assert weak == F(m*m-5*m+2, 2*m*(m-1))
    assert root+gap == tau and root+weak == F(opt, 2*m)
    assert standard_gap == F(m*m-3*m+1, (2*m-1)*(m-1))
    assert root+standard_gap == standard
    assert w-m*standard == F(m*(m-1),2*m-1)
    assert (standard_gap > 0) == (m >= 3)
    assert (gap > 0) == (m >= 4)
    assert (weak > 0) == (m >= 5)
    rows.append({'m':m, 'clients_OPT':opt, 'W':str(w),
                 'root':str(root), 'extra_fractional_value':str(tau),
                 'standard_fractional_value':str(standard),
                 'standard_individual_gap':str(standard_gap),
                 'extra_gap':str(gap), 'individual_half_opt_gap':str(weak)})
print(json.dumps({'status':'PASS','scope':'exact parameter and inverse checks; full SPE proof separate',
                  'rows':rows},indent=2))
