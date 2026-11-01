#!/usr/bin/env python3
"""Statement-first full-tree leaf-transversal audit.

Production extraction is iterative bottom-up on an EXPLICIT full tree.
Independent finite reference enumerates every pruned leaf mask and every
leaf coloring for small trees.  No hardness_route code is read/imported.
"""
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import json


def full_tree(k,h):
    assert k>=1 and h>=1
    children=[[]];depth=[0];levels=[[0]]
    for d in range(h):
        following=[]
        for parent in levels[-1]:
            for _ in range(k):
                node=len(children);children.append([]);depth.append(d+1)
                children[parent].append(node);following.append(node)
        levels.append(following)
    leaves=levels[-1]
    assert len(leaves)==k**h
    return children,depth,leaves


def classify_and_extract(k,h,r,red_mask,tree):
    children,depth,leaves=tree
    t=k-r+1
    good=[False]*len(children)
    for i,leaf in enumerate(leaves):
        good[leaf]=not(red_mask>>i&1)
    for v in reversed(range(len(children))):
        if children[v]:
            good[v]=sum(good[w] for w in children[v])>=r
    blue=good[0];branching=r if blue else t
    selected=[0];edges=[];leaf_numbers=[]
    number={leaf:i for i,leaf in enumerate(leaves)}
    cursor=0
    while cursor<len(selected):
        node=selected[cursor];cursor+=1
        if depth[node]==h:
            leaf_numbers.append(number[node])
            continue
        eligible=[w for w in children[node] if good[w]==blue]
        assert len(eligible)>=branching
        for child in eligible[:branching]:
            selected.append(child);edges.append((node,child))
    assert len(edges)==len(selected)-1
    assert len(leaf_numbers)==branching**h
    out_mask=sum(1<<i for i in leaf_numbers)
    if blue:
        assert out_mask&red_mask==0
    else:
        assert out_mask&red_mask==out_mask
    # Actual selected degrees, full depth, parent uniqueness, original edges.
    parents={}
    outdegree={v:0 for v in selected}
    for u,v in edges:
        assert v in children[u] and v not in parents
        parents[v]=u;outdegree[u]+=1
    assert set(parents)==set(selected)-{0}
    assert all(outdegree[v]==(0 if depth[v]==h else branching) for v in selected)
    return blue,{'branching':branching,'nodes':selected,'edges':[list(e) for e in edges],
                 'leaf_indices':leaf_numbers,'leaf_mask':out_mask}


def all_pruned_masks(k,h,r):
    # Audit-only recursion; never used by the production extractor.
    if h==0:
        return [1]
    sub=all_pruned_masks(k,h-1,r);width=k**(h-1)
    masks=[]
    for chosen_children in combinations(range(k),r):
        for choices in product(sub,repeat=r):
            mask=0
            for child,below in zip(chosen_children,choices):
                mask|=below<<(child*width)
            masks.append(mask)
    assert len(set(masks))==len(masks)
    assert all(mask.bit_count()==r**h for mask in masks)
    return masks


def audit_case(k,h,r):
    tree=full_tree(k,h);n=k**h;t=k-r+1
    pruned=all_pruned_masks(k,h,r)
    minimum=None;max_no_blue=None;first_minimum=None
    colorings=1<<n
    for red in range(colorings):
        expected_hit=all(red&mask for mask in pruned)
        blue,witness=classify_and_extract(k,h,r,red,tree)
        assert blue==(not expected_hit)
        if expected_hit:
            size=red.bit_count()
            if minimum is None or size<minimum:
                minimum=size;first_minimum=red
            blue_count=n-size
            max_no_blue=blue_count if max_no_blue is None else max(max_no_blue,blue_count)
        if red.bit_count()<t**h:
            assert blue
    assert minimum==t**h
    assert max_no_blue==k**h-t**h
    # Explicit extremal blocker = first t children at every active vertex.
    blocker=all_pruned_masks(k,h,t)[0]
    assert blocker.bit_count()==t**h
    assert all(blocker&mask for mask in pruned)
    blue,red_witness=classify_and_extract(k,h,r,blocker,tree)
    assert not blue and red_witness['leaf_mask']&blocker==red_witness['leaf_mask']
    return {'k':k,'h':h,'r':r,'t':t,'explicit_vertices':len(tree[0]),
            'leaves':n,'pruned_subtrees_enumerated':len(pruned),
            'leaf_colorings_enumerated':colorings,
            'minimum_transversal':minimum,'formula_transversal':t**h,
            'maximum_leaf_subset_without_pruned_tree':max_no_blue,
            'one_extremal_blocker_mask':blocker,
            'first_minimum_hitting_mask':first_minimum}


def balanced_source_checks():
    n=3;A=1
    clauses=[tuple((v,sign) for v,sign in enumerate(signs))
             for signs in product((0,1),repeat=n)]
    positive=[sum(sign==1 and v==i for clause in clauses for v,sign in clause) for i in range(n)]
    negative=[sum(sign==0 and v==i for clause in clauses for v,sign in clause) for i in range(n)]
    assert positive==negative==[4]*3
    assignments=[]
    for bits in product((0,1),repeat=n):
        truths=[sum(bits[v]==sign for v,sign in clause) for clause in clauses]
        assert sum(truths)==12==sum(positive)>len(clauses)*A
        assert not all(t<=A for t in truths)
        assignments.append({'assignment':list(bits),'truth_counts':truths,'total':sum(truths)})
    empty_yes=sum(all(True for _ in []) for _ in product((0,1),repeat=n))
    assert empty_yes==8
    return {'nonempty_balanced_instance':{'variables':3,'clauses':8,'arity':3,'A':1,
                                         'positive_counts':positive,'negative_counts':negative,
                                         'assignments':assignments},
            'empty_formula_negative_control':{'variables':3,'clauses':0,
                                             'positive_counts':[0]*3,'negative_counts':[0]*3,
                                             'strict_satisfying_assignments':empty_yes,
                                             'conclusion':'YES-empty consequence needs at least one clause'}}


def main():
    cases=[]
    for k,hs in ((1,range(1,7)),(2,range(1,4)),(3,range(1,3)),(4,range(1,3))):
        for h in hs:
            for r in range(1,k+1):
                cases.append(audit_case(k,h,r))
    # Larger explicit-only extraction, with no exhaustive coloring claim.
    tree=full_tree(1,1000)
    blue,witness=classify_and_extract(1,1000,1,0,tree)
    assert blue and len(witness['nodes'])==1001 and len(witness['edges'])==1000
    output={'version':'independent-full-tree-pruned-duality-v1',
            'code_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'arithmetic':'Python exact integers','status':'passed',
            'complete_small_cases':cases,
            'total_complete_colorings':sum(c['leaf_colorings_enumerated'] for c in cases),
            'unary_depth_1000':{'explicit_vertices':1001,'leaf_count':1,
                               'extracted_edges':len(witness['edges'])},
            'balanced_source':balanced_source_checks(),
            'scope':'finite audits are separate from the general tree recursion proof; no dummy packing asserted'}
    print(json.dumps(output,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
