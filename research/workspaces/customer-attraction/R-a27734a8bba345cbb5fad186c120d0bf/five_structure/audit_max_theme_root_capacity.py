"""Exact local-coefficient checks for max_theme_root_capacity.md."""
from fractions import Fraction as F
from pathlib import Path
import json

A, B = F(1999, 1000), F(5, 3)
integer_checks = 0
for k in range(1, 5):
    for c in range(1, 6):
        lhs = F(c) + F(k * (k + 1), c) - (2 * k + 1)
        rhs = F((c-k)*(c-k-1), c)
        assert lhs == rhs and lhs >= 0
        integer_checks += 1

complement_checks = 0
for j in range(6):
    for t in range(2):
        value = F(0)
        if j:
            for included in (0, 1):
                count = j if included else 5-j
                e = j-included
                value += count * (F(e, t+e) if e else F(0)) / 5
        lower = F(4, 5)*bool(j)-F(2, 5)*t
        assert value >= lower
        complement_checks += 1

expected = [(9097,3497,1200),(3100,15491,1200),
            (-2897,33482,1200),(-4447,28735,600)]
for k, (cm,cu,den) in enumerate(expected, 1):
    assert F(cm,den) == F(5,4)*(A*(4-2*k)+B+F(2,5))
    assert F(cu,den) == F(5,4)*(A*k*(k+1)-B)
    assert A*k*(k+1)-B > 0

o,u,K = F(83705,36641),F(8897,73282),F(16741,36641)
assert F(1,5)*K <= u <= K <= 1
assert o == 5*K
assert 2400*o == 5997-5000*u+203*K
assert 1200*o+2897*K == 33482*u
for cm,cu,den in expected:
    assert den*o <= cm*K+cu*u

# Scalar dual: combine the three active inequalities with nonnegative weights.
# Their forms are 2400O+5000u-203K<=5997,
# 1200O-33482u+2897K<=0, and O-5K<=0.
lambda_actual = F(83705,36641*5997)
lambda_capacity = lambda_actual*F(5000,33482)
lambda_size = (-203*lambda_actual+2897*lambda_capacity)/5
assert lambda_actual > 0 and lambda_capacity > 0 and lambda_size > 0
assert 2400*lambda_actual+1200*lambda_capacity+lambda_size == 1
assert 5000*lambda_actual-33482*lambda_capacity == 0
assert -203*lambda_actual+2897*lambda_capacity-5*lambda_size == 0
assert 5997*lambda_actual == o

root = Path(__file__).resolve().parents[5]
cert = json.loads((root/'evidence/certificates/customer_attraction/five_player_indexed_bound.json').read_text())
p = cert['primal']
den = p['denominator']
old_o = F(p['comparison_cover'])
old_u = F(0)
old_y = F(0)
for atom in p['atoms']:
    mass = F(atom['mass_numerator'],den)
    bits = tuple(map(int,atom['bits']))
    load = sum(bits[:5])
    if bits[0]:
        old_u += mass/load
    if bits[9]:
        old_y += mass
assert old_y == 5*old_u
slack3 = 33482*old_u-1200*old_o-2897*old_y
slack4 = 28735*old_u-600*old_o-4447*old_y
assert slack3 < 0 and slack4 < 0

report = {
    'scope':'exact coefficients and diagnostic only; no SPE enumeration',
    'integer_load_checks':integer_checks,
    'complement_checks':complement_checks,
    'all_four_rows_exact':True,
    'scalar_optimum':{'O':str(o),'u':str(u),'K':str(K)},
    'scalar_dual':{'actual':str(lambda_actual),'capacity3':str(lambda_capacity),'size':str(lambda_size)},
    'old437':{'u':str(old_u),'Y_size':str(old_y),'O':str(old_o),'cut3_slack':str(slack3),'cut4_slack':str(slack4)},
}
out = Path(__file__).with_name('audit_max_theme_root_capacity.json')
out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
