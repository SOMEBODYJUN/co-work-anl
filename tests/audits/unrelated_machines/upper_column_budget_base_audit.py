#!/usr/bin/env python3
"""Exact finite audit for empty-zero occupied-copy matroid-base +B rounding.

This deliberately uses exponential lambda-vertex and integer enumeration.
It is an audit, not the polynomial exact-LP implementation from the proof.
"""
from fractions import Fraction as F
from itertools import combinations, permutations
from pathlib import Path
import hashlib
import json
import random

from occupation_vertex_audit_core import (prepare, projected_vertex,
    face_dimensions, max_matching, affine_rank, dot)


def permutation_matching(graph, occupied):
    """Independent of the recursive matching/rank oracle used by prepare()."""
    if len(occupied) != len(graph):
        return None
    for assignment in permutations(sorted(occupied)):
        if all(assignment[b] in graph[b] for b in range(len(graph))):
            return tuple(enumerate(assignment))
    return None


def copy_face_chain(y, groups, graph, offsets, all_integer_points):
    copies = [(h, q) for h, group in enumerate(groups) for q, (o, _) in enumerate(group) if o]
    fixed = {(h, q) for h, q in copies if y[offsets[h]+q] == 1}
    frac = [(h, q) for h, q in copies if 0 < y[offsets[h]+q] < 1]
    fixed_homes = {h for h, _ in fixed}
    assert len(fixed_homes) == len(fixed)
    resid_rank = len(graph)-len(fixed)
    assert sum((y[offsets[h]+q] for h, q in frac), F(0)) == resid_rank
    deficits = sum((1-y[offsets[h]+q] for h, q in frac), F(0))
    assert deficits.denominator == 1
    if not frac:
        return 0, 0, deficits, frac
    full = frozenset(range(len(frac)))
    tight = []
    for mask in range(1 << len(frac)):
        subset = frozenset(t for t in range(len(frac)) if mask & (1 << t))
        homes = fixed_homes | {frac[t][0] for t in subset}
        contracted_rank = len(max_matching(graph, homes))-len(fixed)
        val = sum((y[offsets[frac[t][0]]+frac[t][1]] for t in subset), F(0))
        assert val <= contracted_rank
        if val == contracted_rank:
            tight.append((subset, contracted_rank))
    tight_sets = {s for s, _ in tight}
    # Inclusion-maximal tight chain, via minimal strict supersets.
    chain = [frozenset()]
    while chain[-1] != full:
        supersets = [s for s in tight_sets if chain[-1] < s]
        nxt = min(supersets, key=lambda s: (len(s), tuple(sorted(s))))
        chain.append(nxt)
    blocks = [b-a for a, b in zip(chain, chain[1:])]
    c = len(blocks)
    assert all(sum((y[offsets[frac[t][0]]+frac[t][1]] for t in block), F(0)).denominator == 1 for block in blocks)
    assert all(sum((y[offsets[frac[t][0]]+frac[t][1]] for t in block), F(0)) >= 1 for block in blocks)
    assert c <= resid_rank
    assert all(all(not (s & block) or block <= s for block in blocks) for s in tight_sets)
    d_chain = len(frac)-c
    assert d_chain >= deficits
    # Independently enumerate the exact minimal face vertices of the copy base.
    face = []
    for point in all_integer_points:
        if any(point[offsets[h]+q] != 1 for h, q in fixed):
            continue
        if any(point[offsets[h]+q] and not y[offsets[h]+q] for h, q in copies):
            continue
        if any(sum((point[offsets[frac[t][0]]+frac[t][1]] for t in s), F(0)) != rhs for s, rhs in tight):
            continue
        face.append([point[offsets[h]+q] for h, q in frac])
    assert affine_rank(face) == d_chain
    return d_chain, c, deficits, frac


def audit_one(groups, graph, budgets):
    for group in groups:
        assert group and group[0][0] == 0 and all(F(v) == 0 for v in group[0][1])
        assert all(o == 1 for o, _ in group[1:])
    offsets, rows, selections, integer_points = prepare(groups, graph)
    assert integer_points
    budgets = tuple(map(F, budgets))
    bound = max((sum(map(F, a), F(0)) for group in groups for o, a in group if o), default=F(0))
    allowed = [set(range(len(group))) for group in groups]
    active = list(range(len(rows)))
    records = []
    candidate_count = 0
    face_checks = 0
    while True:
        points = [p for selection, p in zip(selections, integer_points) if all(selection[h] in allowed[h] for h in range(len(groups)))]
        y, count = projected_vertex(points, rows, budgets, active)
        candidate_count += count
        d, _, support, _ = face_dimensions(y, groups, graph, offsets, integer_points)
        d_copy, blocks, deficits, frac = copy_face_chain(y, groups, graph, offsets, integer_points)
        assert d_copy == d
        assert deficits <= d <= len(active)
        face_checks += 1
        allowed = support
        if not frac:
            final = y
            break
        envelope = [sum((F(groups[h][q][1][z])*(1-y[offsets[h]+q]) for h, q in frac), F(0)) for z in range(len(rows))]
        assert sum(envelope, F(0)) <= bound*deficits
        assert sum((envelope[z] for z in active), F(0)) <= bound*len(active)
        drop = next((z for z in active if envelope[z] <= bound), None)
        assert drop is not None
        records.append((drop, dot(rows[drop], y), envelope[drop], tuple(frozenset(s) for s in support)))
        active.remove(drop)
    selected = tuple(next(q for q in range(len(group)) if final[offsets[h]+q]) for h, group in enumerate(groups))
    # Recompute actual loads directly from selected states, not from row vectors.
    loads = [sum((F(groups[h][q][1][z]) for h, q in enumerate(selected)), F(0)) for z in range(len(rows))]
    assert loads == [dot(row, final) for row in rows]
    assert all(load <= cap+bound for load, cap in zip(loads, budgets))
    for z, at_drop, envelope, old_support in records:
        assert at_drop <= budgets[z]
        assert loads[z] <= at_drop+envelope
        assert all(selected[h] in old_support[h] for h in range(len(groups)))
    occupied = {h for h, q in enumerate(selected) if groups[h][q][0]}
    match = permutation_matching(graph, occupied)
    assert match is not None
    assert len({h for _, h in match}) == len(graph)
    exact_budget_feasible_count = 0
    augmented_feasible_count = 0
    best_slack = None
    for selection in selections:
        actual = [sum((F(groups[h][q][1][z]) for h, q in enumerate(selection)), F(0)) for z in range(len(rows))]
        assert permutation_matching(graph, {h for h, q in enumerate(selection) if groups[h][q][0]}) is not None
        exact_budget_feasible_count += all(load <= cap for load, cap in zip(actual, budgets))
        augmented_feasible_count += all(load <= cap+bound for load, cap in zip(actual, budgets))
        slack = max((load-cap for load, cap in zip(actual, budgets)), default=F(0))
        best_slack = slack if best_slack is None else min(best_slack, slack)
    assert augmented_feasible_count
    return {'bound_B': str(bound), 'drops': len(records), 'vertex_candidates': candidate_count,
        'face_checks': face_checks, 'integer_choices': len(selections), 'exact_budget_feasible_choices': exact_budget_feasible_count,
        'augmented_feasible_choices': augmented_feasible_count, 'minimum_integer_uniform_slack': str(best_slack),
        'loads': list(map(str, loads)), 'budgets': list(map(str, budgets))}


def random_case(rng):
    hcount = rng.randrange(1, 4)
    kcount = rng.randrange(0, 4)
    bcount = rng.randrange(hcount+1)
    graph = [{b} | {h for h in range(hcount) if rng.randrange(2)} for b in range(bcount)]
    groups = []
    for h in range(hcount):
        group = [(0, [F(0)]*kcount)]
        for _ in range(rng.randrange(1, 3)):
            group.append((1, [F(rng.randrange(5), rng.randrange(1, 10)) for _ in range(kcount)]))
        groups.append(group)
    _, rows, _, points = prepare(groups, graph)
    weights = [rng.randrange(1, 6) for _ in points]
    total = sum(weights)
    mean = [sum((F(w, total)*p[t] for w, p in zip(weights, points)), F(0)) for t in range(len(points[0]))]
    budgets = [dot(row, mean) for row in rows]
    return groups, graph, budgets


def bad_naive_copy_graph():
    graph = [{0}, {0, 1}]
    # home0 has two copies; home1 has one. Naively copying macro neighbours
    # lets macro0 and macro1 both occupy home0, which the parallel extension forbids.
    copied_graph = [{0, 1}, {0, 1, 2}]
    fake = permutation_matching(copied_graph, {0, 1})
    assert fake is not None
    assert permutation_matching(graph, {0}) is None
    groups = [[(0, [F(0)]), (1, [F(0)]), (1, [F(0)])], [(0, [F(0)]), (1, [F(100)])]]
    _, rows, selections, points = prepare(groups, graph)
    assert len(points) == 2
    assert all(dot(rows[0], point) == 100 for point in points)
    return {'actual_bases': len(points), 'actual_resource_cost': '100', 'naive_copy_fake_resource_cost': '0',
        'reason': 'The naive graph selects two occupied copies of the same home.'}


def main():
    rng = random.Random(913014)
    cases = [audit_one(*random_case(rng)) for _ in range(180)]
    # One rank-one parallel class with several occupied copies, all empty costs zero.
    for k in (2, 3, 5):
        group = [(0, [F(0)]*k)] + [(1, [F(int(i == j)) for j in range(k)]) for i in range(k)]
        cases.append(audit_one([group], [{0}], [F(1, k)]*k))
    cases.append(audit_one([[(0, [F(0)]), (1, [F(0)])]], [{0}], [F(0)]))
    cases.append(audit_one([[(0, []), (1, [])]], [{0}], []))
    cases.append(audit_one([], [], []))
    huge = 10**95+39
    cases.append(audit_one([[(0, [F(0), F(0)]), (1, [F(1, huge), F(0)]), (1, [F(0), F(1, huge)])]], [{0}], [F(1, 2*huge)]*2))
    source = Path(__file__).read_bytes()
    dependency = Path(__file__).with_name('occupation_vertex_audit_core.py').read_bytes()
    result = {'scope': 'Finite exact Fraction audit only. Explicit integer bases and lambda vertices enumerated exponentially.',
        'arithmetic': 'fractions.Fraction; exact enumeration, no floating-point decisions',
        'python': __import__('sys').version, 'seed': 913014, 'case_count': len(cases), 'random_case_count': 180,
        'face_checks': sum(c['face_checks'] for c in cases),
        'vertex_candidates': sum(c['vertex_candidates'] for c in cases),
        'integer_choices_checked': sum(c['integer_choices'] for c in cases),
        'total_deleted_rows': sum(c['drops'] for c in cases), 'max_deleted_rows': max(c['drops'] for c in cases),
        'cases_without_exact_budget_integer_choice': sum(c['exact_budget_feasible_choices'] == 0 for c in cases),
        'invariants': ['one zero-cost empty mode per home', 'at most one occupied copy per home',
            'tight rank-set chain spans all tight equations', 'd=number_of_fractional_copies-number_of_blocks',
            'sum(1-x)<=d<=retained_rows', 'sum(envelope)<=B*sum(1-x)',
            'support zeros never reopen', 'all final actual row loads<=C+B', 'independent permutation matching recovery'],
        'naive_copy_graph_counterexample': bad_naive_copy_graph(),
        'not_checked': ['Production polynomial rational-LP backend', 'General-input structure extraction', 'External novelty'],
        'script_sha256': hashlib.sha256(source).hexdigest(),
        'vertex_core_sha256': hashlib.sha256(dependency).hexdigest(), 'all_assertions_passed': True}
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
