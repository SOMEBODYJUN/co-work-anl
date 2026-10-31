#!/usr/bin/env python3
"""Exact 16-edge integer escape for tensor+all at-most-two-level count guards.
No repository imports, matching/LP solvers, random search or large enumeration.
"""
from itertools import product,combinations
from collections import Counter
from pathlib import Path
import json,hashlib

B=((1,1,0,1),(0,0,1,1),(1,1,0,0),(1,0,1,1))
A=((0,0,0),(0,1,1),(1,0,1),(1,1,0))


def matrix_product(P,Q):
    return tuple(tuple(sum(P[i][k]*Q[k][j] for k in range(4))%2 for j in range(4)) for i in range(4))


def matvec(M,x):return tuple(sum(a*b for a,b in zip(row,x))%2 for row in M)


def audit():
    t=4;q=2;identity=tuple(tuple(int(i==j) for j in range(t)) for i in range(t));C=tuple(tuple(B[i][j]^identity[i][j] for j in range(t)) for i in range(t))
    assert matrix_product(B,B)==C and matrix_product(B,C)==identity
    basis=identity;forms=list(basis)+list(B)+list(C);assert len(set(forms))==12 and all(any(row) for row in forms)
    edges=[]
    for x in product(range(2),repeat=t):
        y,z=matvec(B,x),matvec(C,x)
        assert all((x[i],y[i],z[i]) in A for i in range(t))
        edges.append((x,y,z))
    assert len(edges)==16 and all(len({edge[axis] for edge in edges})==16 for axis in range(3))
    assert all(any(a==b for a,b in zip(e,f)) for e,f in combinations(A,2))
    prefix_checks=[]
    for axis in range(3):
        for depth in range(1,t+1):
            counts=Counter(edge[axis][:depth] for edge in edges); cap=q**(t-depth)
            assert len(counts)==q**depth and set(counts.values())=={cap}
            prefix_checks.append({'axis':axis,'depth':depth,'capacity':cap,'counts':[[key,value] for key,value in sorted(counts.items())]})
    # All nonempty choices of axes within each of one/two distinct levels:
    # 4*7+6*7^2=322 separate resource-test families. We list only observed
    # patterns; every unlisted pattern has exact load zero.
    axes_subsets=[subset for size in range(1,4) for subset in combinations(range(3),size)]
    bounded_checks=[];families=Counter()
    for s in (1,2):
        for levels in combinations(range(t),s):
            for picked_axes in product(axes_subsets,repeat=s):
                coordinates=tuple((axis,level) for level,axes in zip(levels,picked_axes) for axis in axes)
                counts=Counter(tuple(edge[axis][level] for axis,level in coordinates) for edge in edges); cap=q**(t-s)
                assert max(counts.values())<=cap
                bounded_checks.append({'levels':levels,'coordinates':coordinates,'capacity':cap,'observed_pattern_loads':[[key,value] for key,value in sorted(counts.items())],'unlisted_patterns_load':0});families[str(s)]+=1
    # The intended pair-only subproduct has 54 families, each four patterns
    # capacity4. Assign actual distinct clones to all selected edge bundles.
    pair_families=[((u,i),(v,j)) for i,j in combinations(range(t),2) for u,v in product(range(3),repeat=2)]
    clone_use=Counter();allocations=[]
    for number,edge in enumerate(edges):
        bundle=[('word',axis,edge[axis],0) for axis in range(3)]
        for family,coordinates in enumerate(pair_families):
            pattern=tuple(edge[axis][level] for axis,level in coordinates); key=('pair',family,pattern); index=clone_use[key];clone_use[key]+=1
            assert index<4;bundle.append(key+(index,))
        assert len(bundle)==57
        allocations.append({'edge_index':number,'X':edge[0],'Y':edge[1],'Z':edge[2],'assigned_resource_clones':bundle})
    used=[resource for row in allocations for resource in row['assigned_resource_clones']]
    assert len(set(used))==len(used)==16*57 and len(clone_use)==54*4 and set(clone_use.values())=={4}
    # This explicit matrix is a two-level counter, not a claim that it passes
    # all higher-order guards: X0+X1+Y2=0 violates the natural 3-level cap2.
    triple_coordinates=((0,0),(0,1),(1,2));triple_counts=Counter(tuple(edge[a][i] for a,i in triple_coordinates) for edge in edges)
    assert set(triple_counts.values())=={4} and max(triple_counts.values())>2
    # Root projection of the 16 edges visits all four base edges, proving
    # failure of the genuinely integer prefix-coherent-matching condition.
    root_projection={tuple(edge[axis][0] for axis in range(3)) for edge in edges};assert root_projection==set(A)
    return {'status':'passed','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'base_A':A,'base_q':2,'base_matching_number':1,'base_fractional_perfect_matching_weights':[[edge,'1/2'] for edge in A],'tensor_power':4,'B':B,'I_plus_B':C,'matrix_identity':'B^2=I+B and B(I+B)=I over F2','actual_integer_tensor_matching':edges,'counts':{'selected_tensor_edges':16,'base_pairwise_intersections_checked':6,'all_level_single_axis_prefix_families':12,'one_level_joint_test_families':families['1'],'two_level_joint_test_families':families['2'],'total_bounded_level_joint_test_families':len(bounded_checks),'pair_only_resource_families':54,'assigned_distinct_resource_clones':len(used)},'prefix_checks':prefix_checks,'all_one_two_level_joint_capacity_checks':bounded_checks,'explicit_pair_guard_bundle_allocation':allocations,'higher_order_countertest':{'coordinates':triple_coordinates,'natural_capacity':2,'observed_pattern_counts':[[key,value] for key,value in sorted(triple_counts.items())],'status':'this fixed B fails the displayed three-level guard'},'scope':'Actual integer source-product witness, not an LP/finite-cover surrogate. The generic fixed-L existence theorem is proved separately; this explicit B audits L=2 only. Reinforcing full-word functional coherence is outside these upper-capacity guards.'}

if __name__=='__main__':print(json.dumps(audit(),ensure_ascii=False,indent=2))
