"""Second implementation: no import of the theorem constructor or packing code.

Enumerate every labeled lexmax tie on small inputs, then compute the minimum
pure-NE deviator load by direct complete enumeration. Also test the explicit
symmetric-menu obstruction and its zero-gain complete SPE certificate.
"""
from __future__ import annotations
import argparse
import json
import platform
import random
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from definition_check import check_ne, brute_pure_equilibria, from_pure


def all_lexmax(instance):
    k, m = instance['k'], instance['m']
    w = [F(c['weight']) for c in instance['clients']]
    best, ties = None, []
    for s in product(range(m), repeat=k):
        opts = [sorted(set(c['sites']) & set(s)) or [-1] for c in instance['clients']]
        for assignment in product(*opts):
            L = [sum(w[i] for i, t in enumerate(assignment) if t == s[f]) / s.count(s[f])
                 for f in range(k)]
            key = tuple(sorted(L))
            if best is None or key > best:
                best, ties = key, [(s, assignment, L)]
            elif key == best:
                ties.append((s, assignment, L))
    return best, ties


def uniform_probabilities(s, assignment):
    return [[F(1, s.count(t)) if t >= 0 and site == t else F(0) for site in s]
            for t in assignment]


def check_transfer_budgets(instance, s, assignment, L):
    w = [F(c['weight']) for c in instance['clients']]
    C = [set(c['sites']) for c in instance['clients']]
    k, m = instance['k'], instance['m']
    checked, orphan_covered, disappearing = 0, 0, 0
    for f in range(k):
        a, u = L[f], s[f]
        J = [i for i, t in enumerate(assignment) if t == u]
        for r in range(m):
            if r == u:
                continue
            if r in s:
                budget = sum(w[i] for i, t in enumerate(assignment) if t == r)
                if s.count(u) == 1:
                    added = sum(w[i] for i in J if r in C[i])
                    orphan_covered += bool(added)
                    budget += added
                assert budget <= (s.count(r) + 1) * a
            else:
                budget = sum(w[i] for i, t in enumerate(assignment) if t == -1 and r in C[i])
                if s.count(u) == 1:
                    budget += sum(w[i] for i in J if r in C[i])
                assert budget <= a
            checked += 1
            disappearing += s.count(u) == 1
    return checked, orphan_covered, disappearing


def tiny_all_ties():
    cases = []
    masks = [[], [0], [1], [0, 1]]
    for k in (2, 3, 4, 5):
        for weights in product((1, 2, 5), repeat=2):
            for covers in product(masks, repeat=2):
                cases.append(dict(k=k, m=2,
                    clients=[dict(weight=str(w), sites=c) for w, c in zip(weights, covers)]))
    rng = random.Random(20261003)
    for _ in range(36):
        k, m = rng.choice((2, 3, 4)), rng.choice((2, 3))
        cases.append(dict(k=k, m=m, clients=[
            dict(weight=str(F(rng.choice((1, 2, 7, 31)), rng.choice((1, 3, 5)))),
                 sites=[s for s in range(m) if rng.randrange(3)]) for _ in range(3)]))
    result = dict(cases=len(cases), labeled_lexmax_ties=0,
                  actual_deviation_extrema=0, cached_pure_NE_enumerations=0,
                  transfer_inequalities=0, overlapping_orphan_budgets=0,
                  disappearing_source_checks=0)
    records = []
    for instance in cases:
        best, ties = all_lexmax(instance)
        cache = {}
        for s, assignment, L in ties:
            got = check_ne(instance, s, uniform_probabilities(s, assignment))
            assert got == L
            b, o, d = check_transfer_budgets(instance, s, assignment, L)
            result['transfer_inequalities'] += b
            result['overlapping_orphan_budgets'] += o
            result['disappearing_source_checks'] += d
            for f in range(instance['k']):
                for r in range(instance['m']):
                    if r == s[f]:
                        continue
                    other = list(s)
                    other[f] = r
                    other = tuple(other)
                    if other not in cache:
                        cache[other] = brute_pure_equilibria(instance, other)
                    minimum = min(load[f] for _, load in cache[other])
                    assert minimum <= 2 * L[f]
                    result['actual_deviation_extrema'] += 1
        result['labeled_lexmax_ties'] += len(ties)
        result['cached_pure_NE_enumerations'] += len(cache)
        records.append(dict(instance=instance, key=[str(x) for x in best],
                            lexmax_ties=len(ties), distinct_subgames=len(cache)))
    return result, records


def symmetry_family(q):
    assert q >= 3
    k, a = q + 1, F(4*q-1, 4)
    instance = dict(k=k, m=3, clients=[
        dict(weight=str(q*q), sites=[0, 2]),
        dict(weight='1', sites=[0]),
        dict(weight=str(a), sites=[1])])
    s = (0,)*q + (1,)
    assignment = (0, 0, 1)
    base = check_ne(instance, s, uniform_probabilities(s, assignment))
    assert base == [F(q*q+1, q)]*q+[a]
    deviations = []
    for f in range(k):
        for r in range(3):
            if s[f] == r:
                continue
            other = list(s)
            other[f] = r
            stationary_A = [g for g in range(q) if g != f]
            assert len(stationary_A) >= 2
            pure = [stationary_A[0], stationary_A[1], q if f != q else -1]
            L = check_ne(instance, other, from_pure(pure, k))
            assert L[f] == 0
            deviations.append(dict(facility=f, target=r, assignment=pure,
                                   deviator_load='0'))
    bad_layout = (0,)*q+(2,)
    bad = [[F(int(f == q)) for f in range(k)],
           [F(1, q) if f < q else F(0) for f in range(k)],
           [F(0)]*k]
    bad_load = check_ne(instance, bad_layout, bad)
    assert bad_load[-1] == q*q
    if q <= 5:
        best, _ = all_lexmax(instance)
        assert tuple(sorted(base)) == best
    return dict(q=q, k=k, instance=instance, symmetric_deviation_ratio=str(q*q/a),
                full_model_alpha='1', deviations=deviations,
                independent_labeled_lexmax_checked=q <= 5)


def run():
    summary, records = tiny_all_ties()
    families = [symmetry_family(q) for q in (3, 4, 5, 8, 16, 31, 63)]
    summary.update(symmetry_family_instances=len(families),
                   symmetry_family_deviations=sum(len(c['deviations']) for c in families))
    return dict(claim='SC-K-2-E', second_claim='SC-K-SYMMETRIC-MENU-OBSTRUCTION',
                implementation='No constructor, packing, or improvement-dynamics import',
                evidence_kind='Exact finite checks, not a general proof',
                seed=20261003, python=platform.python_version(), summary=summary,
                tiny_records=records, symmetry_family=families)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    data = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2)+'\n')
    print(json.dumps(data['summary'], indent=2))
