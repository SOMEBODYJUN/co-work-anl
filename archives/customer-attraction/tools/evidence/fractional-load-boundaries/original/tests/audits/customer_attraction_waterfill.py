"""Independent exact boundary audit of waterfill, no author/solver imports.

The rational fixtures supply an exact candidate root only when a partial stop
is needed. The audit verifies it is the unique stop by monotonicity plus exact
unit-profit equality. It is not a generic algebraic root implementation.
"""
import argparse
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json


def audit(name, universe, background, root, tails, threshold, stops=None):
    universe = frozenset(universe)
    root = frozenset(root)
    tails = tuple(frozenset(a) for a in tails)
    b = {x:F(background.get(x,0)) for x in universe}
    t=F(threshold)
    assert t>=0 and all(v>=0 for v in b.values())
    stops = {} if stops is None else {j:F(s) for j,s in stops.items()}
    n=len(tails)
    initial=(F(1),)*n
    w=list(initial)
    def c(x,weights):
        return sum((weights[j] for j in range(n) if x in tails[j]),F(0))
    def load(x,weights):
        return b[x]+int(x in root)+c(x,weights)
    def support(weights):
        return frozenset(x for x in universe if load(x,weights)>0)
    def unit(j,weights):
        assert all(load(x,weights)>0 for x in tails[j])
        return sum((1/load(x,weights) for x in tails[j]),F(0))
    def query(T,weights):
        return sum((1/(b[x]+1+c(x,weights)) for x in T),F(0))
    def R(weights):
        return sum((1/load(x,weights) for x in root),F(0))
    def B(weights):
        return sum((b[x]/load(x,weights) for x in universe if b[x]),F(0))
    def V(weights):
        return sum((c(x,weights)/load(x,weights) for x in universe if c(x,weights)),F(0))
    u=[unit(j,initial) for j in range(n)]
    D=sum((max(F(0),t-v) for v in u),F(0))
    E=F(0)
    original_support=support(initial)
    steps=[]
    for j in range(n):
        before=unit(j,w)
        if before>=t:
            continue
        assert w[j]==1
        zero=w.copy();zero[j]=F(0)
        orphan=any(load(x,zero)==0 for x in tails[j])
        if not orphan and unit(j,zero)<=t:
            w=zero
            endpoint='zero'
        else:
            rho=stops[j]
            assert 0<rho<1
            w[j]=rho
            assert unit(j,w)==t
            endpoint='positive_threshold'
        after=unit(j,w)
        assert after<=t and after>=before>=u[j]
        delta=after-before
        assert delta<=max(F(0),t-u[j])
        E+=delta
        assert support(w)==original_support
        steps.append({'tail':j,'endpoint':endpoint,'weight':str(w[j]),
                      'unit_before':str(before),'unit_after':str(after),
                      'own_increment':str(delta)})
    assert E<=D
    assert all(w[j]==1 for j in range(n) if u[j]>=t)
    assert all(unit(j,w)>=t for j in range(n) if w[j]>0)
    assert support(w)==original_support
    H=query(universe,w)-query(universe,initial)
    assert 0<=H<=E<=D
    queries=0
    for size in range(len(universe)+1):
        for T in combinations(sorted(universe),size):
            delta=query(T,w)-query(T,initial)
            assert 0<=delta<=H<=E<=D
            inserted=lambda weights:sum((1/(b[x]+1+int(x in root)+c(x,weights)) for x in T),F(0))
            delta_insert=inserted(w)-inserted(initial)
            assert 0<=delta_insert<=delta<=H
            queries+=1
    gamma=R(w)-R(initial)
    db=B(w)-B(initial)
    mass=sum(w,F(0))
    assert query(root,w)==R(w)
    assert gamma>=0 and db>=0
    assert V(w)==sum((w[j]*unit(j,w) for j in range(n) if w[j]>0),F(0))
    assert V(w)==V(initial)-gamma-db
    assert V(w)>=t*mass
    assert gamma+db+t*mass<=V(initial)
    return {'name':name,'weights':list(map(str,w)),'initial_unit':list(map(str,u)),
            'final_positive_unit':[str(unit(j,w)) if w[j]>0 else None for j in range(n)],
            'D':str(D),'E':str(E),'common_full_universe_gain':str(H),
            'gamma_root':str(gamma),'background_gain':str(db),
            'V_initial':str(V(initial)),'V_final':str(V(w)),
            'positive_mass':str(mass),'queries_checked':queries,'steps':steps}

cases=[]
cases.append(audit('zero_threshold_unchanged',['x','z'],{},['x'],[['x']],0))
cases.append(audit('unit_credit_constant_equality',['x'],{},['x'],[['x']],F(3,4),{0:F(1,3)}))
cases.append(audit('sole_tail_private_survives', ['x','outside'], {}, [], [['x']], 2, {0:F(1,2)}))
cases.append(audit('root_shared_zero_below_threshold',['x'],{},['x'],[['x']],2))
cases.append(audit('root_shared_zero_exact_threshold',['x'],{},['x'],[['x']],1))
cases.append(audit('initial_high_retained',['x','y'],{},['x'],[['x'],['x','y']],F(1,2)))
cases.append(audit('two_low_second_becomes_high',['x'],{},['x'],[['x'],['x']],F(1,2)))
cases.append(audit('empty_tail_removed',[],{},[],[[]],1))
cases.append(audit('mixed_private_partial',['x','y'],{},['x'],[['x','y']],F(8,3),{0:F(1,2)}))
cases.append(audit('repeated_tail_partial',['x'],{},['x'],[['x'],['x']],F(2,5),{0:F(1,2)}))
cases.append(audit('three_low_sequential_zero',['x'],{},['x'],[['x'],['x'],['x']],F(1,2)))
cases.append(audit('no_tails',['x','outside'],{},['x'],[],3))
for k in [1,2,7,100]:
    result=audit('old_background_return_k_'+str(k),['x','z'],{'x':k},['z'],[['x']],F(1,k))
    assert F(result['background_gain'])==k*F(result['D'])
    cases.append(result)

# One genuinely irrational stop. U(rho)=1/(1+rho)+1/rho=2 has
# unique positive root rho=1/sqrt(2). Exact rational brackets audit the
# construction without floating point or an assumption that rho is rational.
lo=F(0);hi=F(1)
def mixed_u(rho):
    return 1/(1+rho)+1/rho
for _ in range(100):
    mid=(lo+hi)/2
    if mixed_u(mid)>2:
        lo=mid
    else:
        hi=mid
assert 0<lo<hi<1 and mixed_u(lo)>2>mixed_u(hi)
assert lo*lo<F(1,2)<hi*hi
# Initial root payoff=1/2, tail unit=3/2, deficit=1/2.
# All queries share H(rho)=2/(1+rho)-1; its largest bracket value is at lo.
assert 0<2/(1+hi)-1<2/(1+lo)-1<F(1,2)
# Exact identities valid for every positive rho, checked independently at
# both bracket endpoints; their algebraic proof is in review_waterfill.md.
for rho in [lo,hi]:
    root=1/(1+rho)
    weighted_tail=rho/(1+rho)+1
    assert root+weighted_tail==2
irrational={'name':'mixed_private_irrational_stop','rho_lower':str(lo),'rho_upper':str(hi),
            'width':str(hi-lo),'root_equation':'2*rho^2=1',
            'D':'1/2','common_gain_upper':str(2/(1+lo)-1)}
out={'status':'pass','rational_cases':cases,'irrational_case':irrational,
     'scope':'finite exact boundary checks; universal proof is analytic'}
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path)
args=parser.parse_args()
if args.output:
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('x') as handle:
        handle.write(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'pass','rational_cases':len(cases),
                  'query_subsets_checked':sum(x['queries_checked'] for x in cases),
                  'both_query_models':'replacement Q and retained-root insertion J',
                  'irrational_width':str(hi-lo),
                  'background_return_over_D_at_k100':'100'}))
