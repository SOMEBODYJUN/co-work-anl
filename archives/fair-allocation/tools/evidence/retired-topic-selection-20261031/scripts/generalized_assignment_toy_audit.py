#!/usr/bin/env python3
"""Exact finite audits for GAP topic selection. No experiment is a proof.

Run: python topic-selection-drafts/generalized_assignment/toy_audit.py
All arithmetic affecting a mathematical certificate uses int or Fraction.
"""
from fractions import Fraction as F
from itertools import combinations, permutations, product
from collections import Counter
from pathlib import Path
import json
import random

HERE = Path(__file__).resolve().parent

def all_subsets(xs):
    return (set(z) for r in range(len(xs)+1) for z in combinations(xs,r))

def transversal_audit():
    # Element e can be matched to the indicated slots. Rank = 3.
    neighbors = [{0,1},{0,2},{1,2},{0},{1},{2}]
    def is_basis(xs):
        return len(xs)==3 and any(all(p[k] in neighbors[e] for k,e in enumerate(sorted(xs)))
                                  for p in permutations(range(3)))
    bases = [frozenset(z) for z in combinations(range(6),3) if is_basis(z)]
    def strong_bijection(b,d):
        left,right = sorted(b-d), sorted(d-b)
        for perm in permutations(right):
            phi = dict(zip(left,perm))
            if all(is_basis((set(b)-s)|{phi[e] for e in s}) and
                   is_basis((set(d)-{phi[e] for e in s})|s)
                   for s in all_subsets(left)):
                return phi
        return None
    pair_count=0
    for b,d in combinations(bases,2):
        assert strong_bijection(b,d) is not None
        pair_count += 1
    b,d=frozenset([0,1,2]),frozenset([3,4,5])
    phi=strong_bijection(b,d)
    rows=[[F(v) for v in [1,0,1,0,0,1]],
          [F(0),F(1,2),F(1),F(1,3),F(2,3),F(0)]]
    cost=[F(v) for v in [4,2,6,1,7,3]]
    dot=lambda a,z: sum((a[e] for e in z),F(0))
    midcost=(dot(cost,b)+dot(cost,d))/2
    raw=[]; chosen=[]; complements=[]
    for s in all_subsets(sorted(b)):
        t=frozenset((set(b)-s)|{phi[e] for e in s})
        tp=frozenset((set(d)-{phi[e] for e in s})|s)
        assert is_basis(t) and is_basis(tp)
        assert Counter(t)+Counter(tp)==Counter(b)+Counter(d)
        z=t if dot(cost,t)<=dot(cost,tp) else tp
        assert dot(cost,z)<=midcost
        raw.append(t); chosen.append(z); complements.append(tp)
    stats=[]
    for a in rows:
        mu=(dot(a,b)+dot(a,d))/2
        rawmean=sum((dot(a,z) for z in raw),F(0))/len(raw)
        variance=sum(((dot(a,z)-mu)**2 for z in raw),F(0))/len(raw)
        predicted=sum(((a[e]-a[f])**2/F(4) for e,f in phi.items()),F(0))
        assert rawmean==mu and variance==predicted and variance<=mu/F(2)
        stats.append(dict(mu=str(mu),raw_mean=str(rawmean),variance=str(variance),
                          variance_bound=str(mu/F(2)),
                          cost_selected_mean=str(sum((dot(a,z) for z in chosen),F(0))/len(chosen)),
                          max_selected_error=str(max(abs(dot(a,z)-mu) for z in chosen))))
    return dict(neighbors=[sorted(z) for z in neighbors],basis_count=len(bases),
                basis_pairs_checked=pair_count,example_bases=[sorted(b),sorted(d)],
                strong_bijection=phi,random_outcomes=len(raw),fractional_cost=str(midcost),
                selected_costs=[str(dot(cost,z)) for z in chosen],rows=stats)

def graphic_boundary_audit():
    edges=list(combinations(range(4),2))
    def tree(xs):
        p=list(range(4))
        def root(v):
            while p[v]!=v: v=p[v]
            return v
        for e in xs:
            u,v=map(root,edges[e])
            if u==v: return False
            p[u]=v
        return len(xs)==3
    bases=[frozenset(s) for s in combinations(range(6),3) if tree(s)]
    for b,d in combinations(bases,2):
        left,right=sorted(b-d),sorted(d-b)
        valid=[]
        for perm in permutations(right):
            phi=dict(zip(left,perm))
            if all(tree((set(b)-s)|{phi[e] for e in s}) and
                   tree((set(d)-{phi[e] for e in s})|s) for s in all_subsets(left)):
                valid.append(phi)
        if not valid:
            return dict(graph="K4",edges=edges,bases=[sorted(b),sorted(d)],
                        tested_bijections=len(list(permutations(right))),
                        conclusion="No strong base-ordering for this pair; independent-pair merge cannot simply cover all graphic matroids.")
    raise AssertionError("Expected a K4 obstruction")

def perfect_pairings(items):
    if not items:
        yield []
        return
    a=items[0]
    for j in range(1,len(items)):
        b=items[j]
        for tail in perfect_pairings(items[1:j]+items[j+1:]):
            yield [(a,b)]+tail

def bm_pair_audit():
    # Six items; one small pair-bin and two large pair-bins. Capacities 2 and 4.
    pairings=list(perfect_pairings(list(range(6))))
    checked=0; feasible=0
    for weights in product(range(1,5),repeat=6):
        # Unit profit, target 2 => each pair satisfies the profit threshold.
        for small_bins in [1,2]:
            witness=False; matching_condition=False
            for pairs in pairings:
                sums=[weights[a]+weights[b] for a,b in pairs]
                if max(sums)<=4 and sum(z<=2 for z in sums)>=small_bins:
                    matching_condition=True
                # Explicitly choose which pair is sent to which capacity class.
                for small_positions in combinations(range(3),small_bins):
                    if all(sums[k] <= (2 if k in small_positions else 4) for k in range(3)):
                        witness=True
            assert witness==matching_condition
            feasible+=witness; checked+=1
    # Naive uncolored maximum matching can fail although a correct one exists.
    weights=[2,2,1,1]
    naive=[(0,2),(1,3)]
    repaired=[(0,1),(2,3)]
    assert all(sum(weights[e] for e in pair)<=4 for pair in naive)
    assert not any(sum(weights[e] for e in pair)<=2 for pair in naive)
    assert sum(weights[e] for e in repaired[0])<=4
    assert sum(weights[e] for e in repaired[1])<=2
    # Independently optimizing the large bin can starve the small one.
    sequential=dict(capacities=[1,2],items=[dict(weight=1,profit=2),dict(weight=1,profit=2),dict(weight=2,profit=3)],
                    large_first_optimal_subset=[0,1],remaining_small_profit=0,
                    globally_feasible_bundles=[[0],[2]],global_min_profit=2)
    return dict(exhaustive_cases=checked,feasible_cases=feasible,all_checks_passed=True,
                capacities=[2,4],item_weights_domain=[1,2,3,4],n_items=6,profits="all 1",target=2,
                small_bin_counts=[1,2],pairings_per_instance=len(pairings),
                uncolored_matching_failure=dict(weights=weights,capacities=[2,4],naive=naive,repaired=repaired),
                separate_capacity_optimization_failure=sequential)

def budget_and_rounding_audit():
    # A rank-one base with two incompatible exact budgets.
    x=[F(1,2),F(1,2)]; costs=[[0,2],[2,0]]
    budgets=[sum(F(c)*v for c,v in zip(row,x)) for row in costs]
    assert budgets==[F(1),F(1)]
    for selected in [0,1]:
        assert any(row[selected]>bound for row,bound in zip(costs,budgets))
    # Max-GAP: two unit bins and two unit-value/unit-size items.
    # Each bin samples one item independently; retain one copy of every sampled item.
    values=[len(set(picks)) for picks in product([0,1],repeat=2)]
    mean=F(sum(values),len(values))
    assert mean==F(3,2) and mean/F(2)==F(3,4)
    return dict(two_exact_budget_obstruction=dict(fractional=x,costs=costs,budgets=budgets,
                     conclusion="No integral basis meets both; one-cost theorem cannot be promoted to two exact budgets."),
                independent_configuration_sampling=dict(outcomes=values,expected_profit=str(mean),opt=2,ratio=str(mean/F(2)),
                     conclusion="3/4 here is a loss of independent rounding, not an integrality-gap certificate."))

def joint_canonical_audit():
    # Test the new exchange lemma, conditional on fixed global joint labels.
    # Two long bins have two expensive slots each; one short bin has two slots.
    # Items 6 and 7 are initially unused. All cost/profit comparisons are exact.
    rng=random.Random(20261020)
    cases=3000; swaps_total=0
    delta=F(1,100)
    for _ in range(cases):
        n=8
        weights=[F(rng.randrange(1,9),20) for _ in range(n)]
        profits=[F(rng.randrange(2000,2100),10000) for _ in range(n)]
        ceil_div=lambda a,b: -((-a)//b)
        u1=[ceil_div(w,F(1,10))*F(1,10) for w in weights]
        u2=[ceil_div(w,F(3,20))*F(3,20) for w in weights]
        g=[(p//delta)*delta for p in profits]
        tau=[(u1[e],u2[e],g[e]) for e in range(n)]
        oldlong=[[0,1],[2,3]]; oldshort=[4,5]
        critical=set(oldlong[0]+oldlong[1]); current=list(map(list,oldlong)); short=list(oldshort)
        target=set()
        for t in set(tau):
            count=sum(tau[e]==t for e in critical)
            eligible=[e for e in range(n) if tau[e]==t]
            eligible.sort(key=lambda e:(weights[e],e),reverse=True)
            target.update(eligible[:count])
        initial_short_weight=sum(weights[e] for e in short)
        initial_short_profit=sum(profits[e] for e in short)
        for t in set(tau):
            leaving=sorted([e for e in critical-target if tau[e]==t],key=lambda e:(weights[e],e))
            entering=sorted([e for e in target-critical if tau[e]==t],key=lambda e:(weights[e],e))
            assert len(leaving)==len(entering)
            for e,f in zip(leaving,entering):
                assert weights[e]<=weights[f]
                for bundle in current:
                    if e in bundle: bundle[bundle.index(e)]=f; break
                else: raise AssertionError("Missing critical slot")
                if f in short: short[short.index(f)]=e
                swaps_total+=1
        assert set(current[0]+current[1])==target
        assert len(set(current[0]+current[1]+short))==6
        assert [sorted(tau[e] for e in b) for b in current]==[sorted(tau[e] for e in b) for b in oldlong]
        for old,new,u in zip(oldlong,current,[u1,u2]):
            assert sum(u[e] for e in old)==sum(u[e] for e in new)
            assert sum(g[e] for e in old)==sum(g[e] for e in new)
        assert sum(weights[e] for e in short)<=initial_short_weight
        assert sum(profits[e] for e in short)>initial_short_profit-2*delta
    # Minimal independent-choice collision: same two original items, two slots.
    conflict=dict(items=[dict(id="a",weight="2/5",profit="1/2"),dict(id="b",weight="3/10",profit="1/2")],
                  capacities=[1,2],joint_rounded_weights=["2/5","2/5"],critical_slot_counts=[1,1],
                  independent_heaviest_choices=["a","a"],joint_selection=["a","b"],
                  note="Two candidates and two slots already disprove independent selection; this is not a counterexample to the joint lemma.")
    return dict(seed=20261020,cases=cases,swaps=swaps_total,all_checks_passed=True,
                delta=str(delta),long_bins=2,critical_slots_per_long_bin=2,short_bins=1,short_slots=2,
                minimal_independent_collision=conflict,
                conclusion="Fixed joint-type slot multisets and rounded loads preserved; short weight never increases and short profit loss is below 2 delta.")

def parameter_audit():
    checked=0
    for den in range(100,1001):
        z=F(1,den); u=1-z; gamma=u*z; delta=u*z*z
        pre=F(2,3)-8*z; q=pre-3*z; out=q-4*z
        assert u*(F(2,3)-6*z)-pre==F(4,3)*z+6*z*z
        assert pre/u<F(2,3)-6*z
        assert u*(F(2,3)-z)>=F(2,3)-2*z
        assert 3*z-2*delta>gamma
        difference=out/(1+z)-(F(2,3)-16*z)
        assert difference==(z/F(3)+16*z*z)/(1+z) and difference>0
        checked+=1
    # Literal mandatory full coverage is impossible even with fractional feasibility.
    # One item of weight 2 split over two capacity-1 bins; profits may be arbitrarily cheap.
    weights=[F(2)]; capacities=[F(1),F(1)]; x=[F(1,2),F(1,2)]
    assert all(weights[0]*v<=b for v,b in zip(x,capacities))
    assert all(weights[0]>b for b in capacities)
    return dict(zeta_denominators=[100,1000],cases=checked,all_checks_passed=True,
                grid_identity="(2/3-15z)/(1+z)-(2/3-16z)=(z/3+16z^2)/(1+z)",
                mandatory_full_coverage_obstruction=dict(weight=2,capacities=[1,1],fractional=["1/2","1/2"],
                    conclusion="No integral full coverage; discard-allowed contract is essential."))

def default(o):
    if isinstance(o,F): return str(o)
    raise TypeError(type(o))

if __name__=="__main__":
    result=dict(arithmetic="integers and fractions.Fraction",random_seed="joint_canonical:20261020; other finite audits exhaustive",
                transversal_merge=transversal_audit(),graphic_boundary=graphic_boundary_audit(),
                two_capacity_pairs=bm_pair_audit(),joint_canonical=joint_canonical_audit(),parameters=parameter_audit(),sanity=budget_and_rounding_audit(),
                limitations="Finite audits only. No claimed universal rounding or approximation theorem is established.")
    out=HERE/"evidence"/"toy_audit.json"
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2,default=default)+"\n")
    print(json.dumps(dict(output=str(out),transversal_bases=result['transversal_merge']['basis_count'],
                         transversal_pairs=result['transversal_merge']['basis_pairs_checked'],
                         pair_instances=result['two_capacity_pairs']['exhaustive_cases'],
                         all_checks_passed=True),ensure_ascii=False))
