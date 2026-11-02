"""Informed, independent arithmetic for the 17 displayed weights.

This does not import/run the source checker, solve LPs, construct full policies,
or recheck every source row. It checks target scope and incidence realization.
"""
from fractions import Fraction as F
from math import lcm
import json

rows = [
    (1,40,F(21238,2249025)), (1,32,F(78121,2998700)),
    (2,16,F(300193,7496750)), (2,0,F(300193,14993500)),
    (3,63,F(1947217,7496750)), (4,0,F(754001,7496750)),
    (5,46,F(7872,749675)), (5,44,F(1082,149935)),
    (8,0,F(444629,4498050)), (9,47,F(25333,749675)),
    (16,0,F(444629,4498050)), (17,47,F(25333,749675)),
    (32,0,F(444629,4498050)), (33,47,F(25333,749675)),
    (64,0,F(223484,2249025)), (65,47,F(38971,1499350)),
    (65,44,F(2339,749675)),
]
route = (0,0,0,0,1,0)
assert all(w > 0 for _,_,w in rows)
assert sum((w for _,_,w in rows),F()) == 1
assert all(all(not(j>>t&1) or (i>>route[t]&1) for t in range(6))
           and bool(j>>5&1) == bool(i&1) for i,j,w in rows)
private = [sum((w for i,j,w in rows if i==1<<k),F()) for k in range(7)]
assert all(x>0 for x in private) # private clients witness incomparable B_k
covered = sum((w for i,j,w in rows if j),F())
base = covered-F(1,2)
targets = [base+x/2 for x in private]
assert base == F(-148577,8996100)
assert min(targets) == F(7387,5997400)>0
shared = sum((w for i,j,w in rows if 2<=i.bit_count()<=6),F())
pay4 = sum((w*F(j>>4&1,j.bit_count()) for i,j,w in rows if j),F())
source_m4 = pay4-F(1,12)
true_mixed_m4 = pay4-sum(private,F())/12-shared/11
assert source_m4==0
assert true_mixed_m4 == -shared/F(132)<0
denominator = lcm(*(w.denominator for i,j,w in rows))
data = {
    'status':'passed',
    'script_scope':'informed independent exact target/route/maximality/M4 arithmetic only',
    'new_original_checker_runs':0,
    'LP_runs':0,
    'full_strategy_constructions_or_verifications':0,
    'support_count':len(rows),
    'route':route,
    'private_mass_by_label':list(map(str,private)),
    'fixed_six_comparison_target_by_excluded_label':list(map(str,targets)),
    'OPT6_target':str(min(targets)),
    'U_target':str(base),
    'covered_mass':str(covered),
    'shared_mass':str(shared),
    'pay4':str(pay4),
    'source_weakened_M4_average':str(source_m4),
    'full_mixed_M4_average':str(true_mixed_m4),
    'common_integer_denominator':denominator,
    'integer_support_masses':[int(w*denominator) for i,j,w in rows],
    'incidence_realizability':'all columns satisfy fixed route; all seven private blocks positive; B labels pairwise incomparable; adding A_t subset B_route[t] creates no extra maxima',
    'SPE_realizability':'excluded by stronger valid mixed M4 bound, not checked through a full policy',
}
print(json.dumps(data,ensure_ascii=False,indent=2))
