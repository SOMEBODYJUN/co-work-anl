"""Definition-level exact audit for the sunflower-reservoir weak iid gap.

No SPE oracle, LP, numerical root or floating comparison is used.  Complete
small trees sanity-check the universal policy proof.  The formal large
instance follows from the history case proof and rational crossing bounds.
"""
from fractions import Fraction as F
from itertools import product
from math import comb, factorial
import json


def customers(m, k):
    # 0=C, 1=B, j+2=P_j. All entries represent different unit customers.
    core = set([0]+list(range(2,k+2)))
    return [core.copy(),core.copy()]+[{1} for _ in range(2*(m-1))]+[
        {j+2} for j in range(k)]


def action(h, m, k):
    if not h:
        return 0
    if len(h) < m-1:
        return 1
    non_b = [a for a in h if a != 1]
    if not non_b:
        return 2
    if len(non_b) == 1:
        a = non_b[0]
        return 1 if a == 0 else 2+(a-1) % k
    return 1


def finish(h, m, k):
    h = tuple(h)
    while len(h) < m:
        h += (action(h,m,k),)
    return h


def utility(a, z, unit_customers):
    return sum((F(1,sum(b in row for b in z))
                for row in unit_customers if a in row),F())


small = []
for m,k in [(2,2),(3,2),(4,3)]:
    unit = customers(m,k)
    total = 0
    minimum = None
    for depth in range(m):
        for h in product(range(k+2),repeat=depth):
            incumbent = action(h,m,k)
            u = utility(incumbent,finish(h,m,k),unit)
            for a in range(k+2):
                diff = u-utility(a,finish(h+(a,),m,k),unit)
                assert diff >= 0
                minimum = diff if minimum is None else min(minimum,diff)
                total += 1
    assert finish((),m,k) == (0,)+(1,)*(m-1)
    small.append({'m':m,'K':k,'all_ordered_comparisons':total,
                  'minimum_SPE_slack':str(minimum)})

m = k = 100
unit = customers(m,k)
z = finish((),m,k)
assert len(unit) == 300 and len(z) == 100
assert sum(any(a in row for a in z) for row in unit) == 200
assert all(utility(a,z,unit) == 2 for a in z)
# An actual legal m-1-topic background caps every pure query at 2.
background = (1,)*(m-2)+(2,)
caps = [utility(a,background+(a,),unit) for a in range(k+2)]
assert max(caps) == 2
assert caps[0] == 1 and caps[1] == 2 and caps[2] == F(3,2)
assert all(x == 2 for x in caps[3:])

# Exact history-case upper bounds at the large instance. The proof explains
# why these t-only bounds cover every ordered history and every petal repeat.
for t in range(2,m):
    assert F(2*(m-1),m-t) > 2  # all-B continuation payoff
    assert F(2,t+1)+1 < 2       # arbitrary petal deviation payoff upper bound
assert F(2*(m-1),m-2) > 2      # the one-old-petal case, nonlast node


def g(n,s):
    return sum(((1-s)**j for j in range(n)),F())/n


t0 = F(1969,2000)
alpha_b = 2*(m-1)*g(m,t0)
alpha_p = 2*g(m,1-t0)+g(m,(1-t0)/k)
lower = F(2011,1000)
target = F(4*m,2*m-1)
assert alpha_b > lower > target
assert alpha_p > lower

# Short exact inequalities used in the written proof.
s = F(31,2000)
poly8 = sum(((-1)**j*comb(100,j)*s**j for j in range(9)),F())
assert (1-s)**100 <= poly8 < F(21,100)
assert (F(31,2000))**100 < F(341,3960000)
alpha_p_lower = F(158,155)+1-F(3069,400000)
assert alpha_p > alpha_p_lower > lower
assert alpha_p_lower-lower == F(8461,12400000)
assert F(199,2)*lower-200 == F(189,2000)

# Universal family certificate: all m=K>=53, with t=1-3/(2m).
# The positivity is algebraic in n=m-53, rather than finite m sampling.
exp_lower = sum(((F(3,2))**j/F(factorial(j)) for j in range(6)),F())
assert exp_lower == F(5711,1280) and exp_lower > F(40,9)
assert [4,403,10132] == [4,8*53-21,4*53**2-21*53+9]
assert [4,212,45] == [4,8*53-212,4*53**2-212*53+45]
assert all(x > 0 for x in [4,403,10132,4,212,45])
m53 = 53
a = F(3,2)
cut53 = 1-a/m53
b53 = 2*(m53-1)*g(m53,cut53)
p53 = 2*g(m53,1-cut53)+g(m53,(1-cut53)/m53)
r53 = F(4*m53,2*m53-1)
b53_lower = 2*(m53-1)*(m53*m53+a*m53+a*a)/(m53**3)
p53_lower = F(61,30)-F(3,4*m53)
assert b53 >= b53_lower > r53 and p53 > p53_lower > r53
assert b53_lower-r53 == F(4*m53*m53-21*m53+9,
                          2*m53**3*(2*m53-1))
assert p53_lower-r53 == F(4*m53*m53-212*m53+45,
                          60*m53*(2*m53-1))
defect53 = min(F(4*m53*m53-21*m53+9,4*m53**3),
               F(4*m53*m53-212*m53+45,120*m53))
assert defect53 == F(3,424)

print(json.dumps({
    'scope':'True complete SPE weak-iid bridge counterexample, not a half-coverage or true-security counterexample. General policy proof is analytic; finite replay is not its arbitrary-m proof.',
    'small_complete_tree_sanity_checks':small,
    'formal_fixed_instance':{'m':m,'K':k,'topics':k+2,'unit_customers':len(unit),
        'W':200,'OPT':299,'true_security_v_upper_bound':2,
        'legal_background':'B^98 P_1',
        'rational_cut_t0':str(t0),
        'alpha_B_at_cut':str(alpha_b),
        'alpha_P_at_cut':str(alpha_p),
        'common_equilibrium_payoff_strict_lower_bound':str(lower),
        'weak_bridge_payoff_threshold':str(target),
        'weak_bridge_defect_strict_lower_bound':str(F(189,2000))},
    'short_bound_checks':{'Taylor_degree_8_upper_bound':str(poly8),
        'Taylor_bound_below_21_over_100':True,
        'alpha_P_short_lower_bound':str(alpha_p_lower)},
    'universal_family_certificate':{
        'range':'Every m=K>=53, from explicit inequalities and positive polynomial coefficients, not a finite sample.',
        'exp_3_over_2_strict_lower_bound':str(exp_lower),
        'numerator_B_in_n_m_minus_53':[4,403,10132],
        'numerator_P_in_n_m_minus_53':[4,212,45],
        'm53_unit_customers':159,'m53_topics':55,'m53_W':106,'m53_OPT':158,
        'm53_rational_cut':str(cut53),
        'm53_alpha_B_lower_bound':str(b53_lower),
        'm53_alpha_P_lower_bound':str(p53_lower),
        'm53_weak_defect_strict_lower_bound':str(defect53)},
    'general_half_proved_or_refuted':False,
    'true_aggregate_security_proved_or_refuted':False,
},indent=2))
