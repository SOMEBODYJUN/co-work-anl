"""One new stdlib entry: new53/100 cuts and symbolic identities only.

No old eight-customer SPE/security/Nash audit, oldm20/K100 certificate,
complete petal policy tree, solver or absent original audit is rerun.
Universal quantifiers are proved in the accompanying analytic text.
"""
from pathlib import Path
from fractions import Fraction as F
from math import comb, factorial
import json
E=Path(__file__).resolve().parent
OUT=E/'new-petal-threshold-certificates.json'
if OUT.exists():raise SystemExit('Successful new certificate entry exists; do not rerun')

def add(a,b):
    a=list(a);b=list(b);a += [F(0)]*(len(b)-len(a));b += [F(0)]*(len(a)-len(b))
    return [x+y for x,y in zip(a,b)]
def scale(a,c):return [F(c)*x for x in a]
def mul(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out
def trim(a):
    a=list(a)
    while len(a)>1 and not a[-1]:a.pop()
    return a
def shift(a,c):
    out=[F(0)]*len(a)
    for i,x in enumerate(a):
        for j in range(i+1):out[j]+=x*comb(i,j)*F(c)**(i-j)
    return trim(out)

M=[F(0),F(1)];Mm1=[F(-1),F(1)];twom1=[F(-1),F(2)]
N1=[F(9),F(-21),F(4)];N2=[F(45),F(-212),F(4)]
first=add(mul(scale(mul(Mm1,[F(9,4),F(3,2),F(1)]),4),twom1),[0,0,0,0,F(-8)])
second=add(mul([F(-45),F(122)],twom1),[0,0,F(-240)])
assert trim(first)==N1 and trim(second)==N2
assert shift(N1,5)==[F(4),F(19),F(4)]
assert shift(N1,53)==[F(10132),F(403),F(4)]
assert shift(N2,53)==[F(45),F(212),F(4)]
reciprocal=add(add(mul([1,1],[2,1]),scale(mul([0,1],[2,1]),-2)),mul([0,1],[1,1]))
assert trim(reciprocal)==[2]
exp5=sum(F(3,2)**j/factorial(j) for j in range(6))
exp3=sum(F(3,2)**j/factorial(j) for j in range(4))
assert exp5==F(5711,1280)>F(40,9) and exp3==F(67,16)>4

def g(m,s):return sum(((1-s)**j for j in range(m)),F(0))/m
def values(m,K,t):return 2*(m-1)*g(m,t),2*g(m,1-t)+g(m,(1-t)/K)

m=100;s=F(31,2000);t=1-s;L=F(2011,1000);R=F(400,199)
F100,G100=values(m,m,t)
taylor8=sum((-1)**j*comb(100,j)*s**j for j in range(9))
assert (1-s)**100<=taylor8<F(21,100)
assert s**100<F(1,2)**100<F(1,2)**14<F(341,3960000)
private_lower=1-F(3069,400000)
petal_lower=F(158,155)+private_lower
assert g(100,s/100)>=private_lower
assert petal_lower==F(24944861,12400000) and petal_lower-L==F(8461,12400000)>0
assert F100==F(3960,1969)*(1-s**100)>L and G100>petal_lower>L>R
assert F(199,2)*L-200==F(189,2000)>0

cases=[]
for m in (53,100):
    K=m;a=F(3,2);t=1-a/m;ff,gg=values(m,K,t);r=F(4*m,2*m-1)
    fl=F(2*(m-1),m**3)*(m*m+a*m+a*a);gl=F(61,30)-F(3,4*m)
    assert ff>=fl>r and gg>gl>r
    gap1=F(4*m*m-21*m+9,4*m**3);gap2=F(4*m*m-212*m+45,120*m)
    bound=min(gap1,gap2)
    assert F(2*m-1,2)*(fl-r)==gap1 and F(2*m-1,2)*(gl-r)==gap2
    assert bound>0
    if m==53:assert bound==F(3,424)
    cases.append({'m':m,'K':K,'unit_clients':3*m,'topics':m+2,'actual_W_by_analytic_policy':2*m,'OPT_by_analytic_catalog_formula':3*m-1,'test_t':t,'actual_B_query_at_cut':ff,'actual_petal_query_at_cut':gg,'B_lower':fl,'petal_lower':gl,'critical_rho':r,'weak_bridge_reverse_margin_strict_lower':bound})

def enc(v):
    if isinstance(v,F):return str(v)
    if isinstance(v,dict):return {k:enc(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [enc(x) for x in v]
    return v
result={'status':'passed','new_definition_entry_attempts':1,'new_definition_entry_successes':1,'failed_math_attempts':0,'original_audit_CLI_entries':0,'external_solver_calls':0,
 'scope':'new symbolic threshold identities and exact cuts; no full-policy or static-Nash-root numerical reconstruction',
 'symbolic':{'reciprocal_second_difference_numerator':trim(reciprocal),'B_lower_minus_threshold_numerator':N1,'petal_lower_minus_threshold_numerator':N2,'B_numerator_shift_m5':shift(N1,5),'B_numerator_shift_m53':shift(N1,53),'petal_numerator_shift_m53':shift(N2,53),'exp3_lower':exp3,'exp5_lower':exp5,'universal_range_m_ge53_proof':'positive shifted polynomial coefficients and analytic inequalities, not an enumerated range'},
 'new_fixed100':{'s':s,'t':t,'L':L,'critical_rho':R,'actual_B_at_cut':F100,'actual_petal_at_cut':G100,'Taylor8':taylor8,'Taylor8_less_21_over100':True,'private_Bernoulli_lower':private_lower,'petal_rational_lower':petal_lower,'petal_lower_minus_L':petal_lower-L,'reverse_margin_over_weak_threshold_strict_lower':F(189,2000)},
 'm_equals_K_cases':cases,
 'reused_without_rerun':{'existing_eight_customer_full_history_comparisons':84,'existing_eight_customer_W':6,'existing_eight_customer_OPT':8,'existing_eight_customer_true_security':'44/23','oldm20_K100_cut':True,'old_fixedK100_allm_ge41_proof':True},
 'not_newly_executed':['any full petal policy tree','original20/84/780 small-tree audit','original quadratic iidcap audit1728Jensen','original independent policy review implementation','old8customerNash/CCE/security/fullhistory certificate'],
 'asymptotic_claim':'analytic c_star argument in body only, no numerical root scan or finite extrapolation'}
OUT.write_text(json.dumps(enc(result),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(enc({'status':'passed','new_entries':1,'original_CLI_entries':0,'solver_calls':0,'m100_strict_gap':F(189,2000),'m53_strict_gap':F(3,424),'symbolic_numerators':[N1,N2],'full_policy_reruns':0}),ensure_ascii=False))
