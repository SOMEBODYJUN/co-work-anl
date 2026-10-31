"""Targeted independent exact checks for the general uniform-contraction review.
Universal claims are proved in the accompanying review, not inferred from samples.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
source=HERE.parent/'credible'/'waterfill_credibility_uniform_contraction.md'

def check_family(n,core_background,scope):
    # Retained A has one private customer; Q has n fresh customers.
    # Common-core customers have effective initial background given in the list.
    rows=[(frozenset([0]),F(1),1),(frozenset([1]),F(0),n)]
    rows += [(frozenset([0,1]),F(b),1) for b in core_background]
    def K(weight):return sum((F(1)/(b+n*weight) for b in core_background),F(0))
    def pay(topic,z,weight):
        return sum((count*weight/(background+weight*sum(a in likes for a in z)) for likes,background,count in rows if topic in likes),F(0))
    histories=[h for depth in range(n) for h in product(range(2),repeat=depth)]
    comparisons=0
    for weight in [F(1),F(3,4),F(1,7)]:
        for h in histories:
            actual=(*h,*([1]*(n-len(h))))
            prescribed=pay(1,actual,weight)
            for alt in range(2):
                z=(*h,alt,*([1]*(n-len(h)-1)))
                assert prescribed>=pay(alt,z,weight)
                comparisons+=1
    S=F(n*n,(n+1)**2);assert 0<S<1
    minimum=1+K(F(1));delta=F(1,3);target=minimum+delta
    def density(weight):return 1/weight+K(weight)
    low,high=F(0),F(1)
    # Never evaluate the zero endpoint: the fresh term diverges there.
    for _ in range(110):
        middle=(low+high)/2
        if density(middle)>target:low=middle
        else:high=middle
    assert low>0 and density(low)>=target>=density(high)
    def pool(weight):return n*(F(1)/(1+n*weight)-F(1,n+1))+K(weight)-K(F(1))
    assert pool(low)<delta<=n*delta
    # Exact whole-customer conservation, allowing heterogeneous core backgrounds.
    for weight in [F(1),F(3,4),low,high]:
        Gamma=K(weight)-K(F(1))
        old_return=sum(((b-1)*(F(1)/(b+n*weight)-F(1,b+n)) for b in core_background),F(0))
        V=n+n*weight*K(weight);V1=n+n*K(F(1))
        assert Gamma+old_return+V==V1
        assert V-n*weight*target==n*weight*(density(weight)-target)
        H=pool(weight)
        assert H<=S*(1/weight-1)+K(weight)-K(F(1))
    # t below/equal to the original minimum must use the positive part in the bound.
    for trivial_t in [F(0),minimum-F(1,4),minimum]:
        assert trivial_t>=0 and pool(F(1))==0
        assert 0<=max(trivial_t-minimum,F(0))==0
    return dict(n=n,core_background=list(map(str,core_background)),scope=scope,a_star='1',S=str(S),all_history_comparisons=comparisons,water_lambda_lower=str(low),water_lambda_upper=str(high),H_upper=str(pool(low)),minimum_deficit=str(delta),total_deficit=str(n*delta))

cases=[]
for n in [1,3,7]:
    cases.append(check_family(n,[],'legal original CAG prefix'))
    cases.append(check_family(n,[1,1],'legal original CAG prefix'))
cases.append(check_family(3,[1,3,7],'stronger frozen-background extension; not a same-catalog legal-prefix example'))
# Zero fresh threshold: positive mass cannot reach K(0), and lambda=1 handles t<=K(1).
a0=[]
for n,backgrounds in [(1,[1]),(3,[1]),(3,[1,3])]:
    def K(weight):return sum((F(1)/(b+n*weight) for b in backgrounds),F(0))
    K0=K(F(0));K1=K(F(1));assert K0>K1
    for weight in [F(1),F(3,4),F(1,1000)]:assert K(weight)<K0
    target=(K0+K1)/2;low,high=F(0),F(1)
    for _ in range(110):
        middle=(low+high)/2
        if K(middle)>target:low=middle
        else:high=middle
    assert low>0 and K(low)>=target>=K(high)
    assert target-K1<=n*(target-K1)
    a0.append(dict(n=n,b=list(map(str,backgrounds)),K0=str(K0),K1=str(K1),interior_target=str(target),lambda_lower=str(low),lambda_upper=str(high),at_or_above_K0='No positive uniform mass can meet the higher threshold'))
# Degenerate empty core/no fresh clients: only t=0 is covered by lambda=1.
assert F(0)==max(F(0)-F(0),F(0))
# Two universal local identities, tested exactly at boundary and interior points.
identity_checks=0
for b in [0,1,7]:
    for load in [1,3,8]:
        for weight in [F(1),F(3,4),F(1,1000)]:
            gap=F(1,b+load)-weight/(b+weight*load)
            assert gap==b*(1-weight)/((b+load)*(b+weight*load))>=0
            lhs=F(1)/(1+weight*load)-F(1,1+load)
            rhs=F(load,(1+load)**2)*(1/weight-1)
            assert lhs<=rhs
            identity_checks+=1
out=dict(status='PASS after positive-part correction; actual-leaf water/credit and full-child SPE are distinct quantifiers',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),local_identity_checks=identity_checks,cases=cases,zero_fresh_boundary=a0,empty_core_zero_fresh='lambda=1 for t=0; no positive-mass guarantee for t>0')
(HERE/'uniform_credible_contraction_review_audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(status=out['status'],families=len(cases),all_history_comparisons=sum(c['all_history_comparisons'] for c in cases),zero_fresh_cases=len(a0),local_identity_checks=identity_checks),indent=2))
