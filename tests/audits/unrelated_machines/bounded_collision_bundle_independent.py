#!/usr/bin/env python3
"""Independent actual-root-tree oracle for a bounded resource collision floor.

This file imports no normative audit or constructor.  For depth-three demand
DAGs r -> X -> label -> resource, it enumerates every resource parent (including
absence).  A positive-score tree must select precisely the ancestors of its
selected resources.  Thus the oracle includes trees with several selected
labels at the same X; it does not assume the one-label normalization used by a
constructor.  All scores are exact Fraction values.  Finite tests are not the
general proof and do not establish scheduling inapproximability.

The selected-label witness chooses one nonempty label per X.  A label is
(positive demand, tuple of distinct resource IDs), demand <= cardinality.
Delta counts the selected bundles only; nonselected labels remain in the
actual DAG and may have unrestricted collisions.
"""

from collections import Counter
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import platform
import random


def check_menus(menus):
    for labels in menus:
        for demand, resources in labels:
            assert isinstance(demand, int) and not isinstance(demand, bool)
            assert demand >= 1
            assert len(resources) == len(set(resources))


def exact_tree_optimum(menus):
    """Enumerate all positive-score root trees by original resource parents."""
    check_menus(menus)
    q = len(menus)
    if q == 0:
        return Fraction(1), 1
    labels = [(x, demand, tuple(resources))
              for x, options in enumerate(menus)
              for demand, resources in options]
    resources = sorted({r for _, _, rs in labels for r in rs})
    incoming = [[-1] + [e for e, (_, _, rs) in enumerate(labels) if r in rs]
                for r in resources]
    best = Fraction(0)
    parent_choices = 0
    for parents in product(*incoming):
        parent_choices += 1
        counts = Counter(e for e in parents if e != -1)
        if not counts:
            continue
        chosen_x = {labels[e][0] for e in counts}
        # At each chosen X the degree is >=1 and its original demand is 1.
        score = min([Fraction(1), Fraction(len(chosen_x), q)] +
                    [Fraction(count, labels[e][1])
                     for e, count in counts.items()])
        best = max(best, score)
    return best, parent_choices


def collision_certificate(menus, selected):
    assert len(menus) == len(selected)
    assert menus
    used = Counter()
    for options, index in zip(menus, selected):
        demand, resources = options[index]
        assert 1 <= demand <= len(resources)
        used.update(resources)
    return max(used.values())


def group_degree(menus):
    """Count distinct X groups at each resource, never label indegree."""
    groups = {}
    for x, options in enumerate(menus):
        for _, resources in options:
            for resource in resources:
                groups.setdefault(resource, set()).add(x)
    return max(map(len, groups.values()), default=0)


def ceil_fraction(value):
    return -((-value.numerator) // value.denominator)


def threshold_grid_constructor(menus):
    """Independent full-threshold construction, not the sorted-envelope core.

    Gamma uses every attainable d/K label ratio, d <= explicit cardinality.
    For each threshold all qualifying groups participate; each local label is
    truncated to ceil(threshold*K).  This intentionally differs from choosing
    a top-s prefix by sorted local densities.  Color order is reversed by X.
    """
    q = len(menus)
    if q == 0:
        return Fraction(1), Fraction(1), [], 0
    delta = group_degree(menus)
    gamma = {Fraction(1)}
    for options in menus:
        for demand, resources in options:
            gamma.update(Fraction(d, demand)
                         for d in range(1, min(demand, len(resources)) + 1))
    best_upper, best_tau, best_labels = Fraction(0), Fraction(0), []
    for tau in sorted(gamma):
        eligible = []
        for x, options in enumerate(menus):
            for e, (demand, resources) in enumerate(options):
                if Fraction(len(resources), demand) >= tau:
                    eligible.append((x, e))
                    break
        upper = min(tau, Fraction(len(eligible), q))
        if (upper, tau) > (best_upper, best_tau):
            best_upper, best_tau, best_labels = upper, tau, eligible
    if best_upper == 0:
        return Fraction(0), Fraction(0), [], delta
    incidence = {}
    for x, e in best_labels:
        demand, resources = menus[x][e]
        chosen = tuple(sorted(resources))[:ceil_fraction(best_tau * demand)]
        for resource in chosen:
            incidence.setdefault(resource, []).append((x, e))
    candidates = [{} for _ in range(delta)]
    for resource, owners in sorted(incidence.items()):
        for color, owner in enumerate(sorted(owners, reverse=True)):
            candidates[color].setdefault(owner, []).append(resource)
    best_score, best_witness = Fraction(0), []
    for ownership in candidates:
        witness = []
        for x, e in best_labels:
            demand, _ = menus[x][e]
            owned = ownership.get((x, e), [])
            if Fraction(len(owned), demand) >= best_tau / delta:
                witness.append((x, e, tuple(owned)))
        score = check_witness(menus, witness)
        if score > best_score:
            best_score, best_witness = score, witness
    assert best_score >= best_upper / delta
    return best_score, best_upper, best_witness, delta


def check_witness(menus, witness):
    if not menus:
        assert not witness
        return Fraction(1)
    seen_x, seen_resources = set(), set()
    score = Fraction(len(witness), len(menus))
    for x, e, owned in witness:
        assert x not in seen_x
        seen_x.add(x)
        demand, resources = menus[x][e]
        assert owned and len(owned) == len(set(owned))
        assert set(owned) <= set(resources)
        assert not seen_resources.intersection(owned)
        seen_resources.update(owned)
        score = min(score, Fraction(len(owned), demand))
    return min(Fraction(1), score)


def sorted_local_envelope(menus):
    """A formula-only crosscheck against the distinct Gamma constructor."""
    if not menus:
        return Fraction(1)
    densities = sorted((max((min(Fraction(1), Fraction(len(rs), k))
                             for k, rs in options), default=Fraction(0))
                        for options in menus), reverse=True)
    return max(min(Fraction(s, len(menus)), density)
               for s, density in enumerate(densities, 1))


def verify_group_approximation(menus, totals):
    optimum, enumerated = exact_tree_optimum(menus)
    score, upper, witness, delta = threshold_grid_constructor(menus)
    assert check_witness(menus, witness) == score
    assert sorted_local_envelope(menus) == upper
    assert optimum <= upper
    if not menus:
        assert optimum == upper == score == 1 and delta == 0
    elif delta == 0:
        assert optimum == upper == score == 0
    else:
        assert score >= upper / delta >= optimum / delta
        actual_c_bound = 2 - score
        factor_bound = (2 - Fraction(1, delta)) * (2 - optimum)
        assert actual_c_bound <= factor_bound
        # Independently reverse the final multiplicative scheduling inequality.
        assert factor_bound - (2 - optimum / delta) == (
            2 * (1 - Fraction(1, delta)) * (1 - optimum))
    totals['group_degree_approximation_dags'] += 1
    totals['approximation_resource_parent_assignments'] += enumerated


def audit():
    totals = Counter()
    examples = []
    # Four local labels on two resources: demands 1 on singletons, and demands
    # 1 or 2 on the pair.  Every nonempty local menu is retained in the full DAG.
    label_universe = [(1, (0,)), (1, (1,)), (1, (0, 1)), (2, (0, 1))]
    local_menus = [tuple(label_universe[i] for i in range(4) if mask >> i & 1)
                   for mask in range(1, 16)]
    for q in (1, 2):
        for menus in product(local_menus, repeat=q):
            optimum, enumerated = exact_tree_optimum(menus)
            totals['exhaustive_full_menu_dags'] += 1
            totals['actual_resource_parent_assignments'] += enumerated
            for selected in product(*(range(len(options)) for options in menus)):
                delta = collision_certificate(menus, selected)
                assert optimum >= Fraction(1, delta), (menus, selected, optimum)
                totals['exhaustive_selected_label_certificates'] += 1

    # Full labels include unselected alternatives, arbitrary positive demands,
    # and an optional positive-demand dead label.  The certificate uses only a
    # nonempty feasible label from each menu; the actual oracle sees all labels.
    rng = random.Random(2026101711)
    for sample in range(500):
        q = rng.randrange(1, 5)
        resource_count = rng.randrange(1, 6)
        menus = []
        selected = []
        for x in range(q):
            size = rng.randrange(1, resource_count + 1)
            resources = tuple(sorted(rng.sample(range(resource_count), size)))
            options = [(rng.randrange(1, size + 1), resources)]
            selected.append(0)
            for _ in range(rng.randrange(3)):
                size = rng.randrange(resource_count + 1)
                alt = tuple(sorted(rng.sample(range(resource_count), size)))
                # An empty positive-demand label is a legal dead end, but is
                # deliberately never part of the selected witness.
                options.append((rng.randrange(1, max(2, size + 2)), alt))
            menus.append(tuple(options))
        delta = collision_certificate(menus, selected)
        optimum, enumerated = exact_tree_optimum(menus)
        assert optimum >= Fraction(1, delta), (menus, delta, optimum)
        totals['random_full_menu_dags'] += 1
        totals['actual_resource_parent_assignments'] += enumerated
        verify_group_approximation(menus, totals)

    # The global approximation permits missing groups, positive dead labels,
    # and labels whose demand exceeds their full resource cardinality.  Six
    # label types generate every (including empty) local menu on two resources.
    extended_labels = label_universe + [(3, (0, 1)), (1, ())]
    extended_menus = [tuple(extended_labels[i] for i in range(6)
                            if mask >> i & 1) for mask in range(64)]
    for q in (1, 2):
        for menus in product(extended_menus, repeat=q):
            verify_group_approximation(menus, totals)
    for menus in ([], [()], [((1, ()),)],
                  [((2 ** 200 + 1, (0, 1)),), ()],
                  [((1, (0,)), (3, (0,)), (7, (0,)))],
                  [((1, (0,)),), (), ((2, (1, 2)),)]):
        verify_group_approximation(menus, totals)

    # Delta=2 is sharp for every positive demand K: paired identical K-sets.
    # Enumerate K=1..9 as finite attacks; the all-K proof is separate.
    for k in range(1, 10):
        menus = [((k, tuple(range(k))),)] * 2
        optimum, enumerated = exact_tree_optimum(menus)
        assert optimum == Fraction(1, 2), (k, optimum)
        totals['paired_identical_k_sets'] += 1
        totals['actual_resource_parent_assignments'] += enumerated
        examples.append({'family': 'one_identical_pair', 'K': k,
                         'Delta': 2, 'b_star': str(optimum)})
    for k in range(1, 5):
        menus = [((k, tuple(range(k))),)] * 2
        menus += [((k, tuple(range(k, 2 * k))),)] * 2
        optimum, enumerated = exact_tree_optimum(menus)
        assert optimum == Fraction(1, 2), (k, optimum)
        totals['two_disjoint_pairs'] += 1
        totals['actual_resource_parent_assignments'] += enumerated

    # Every Delta has an exact 1/Delta witness when K=1.  The two groups have
    # disjoint resources, and there are Delta copies of each singleton.
    for delta in range(1, 13):
        menus = [((1, (0,)),)] * delta + [((1, (1,)),)] * delta
        optimum, enumerated = exact_tree_optimum(menus)
        assert optimum == Fraction(1, delta), (delta, optimum)
        totals['general_delta_singleton_sharp'] += 1
        totals['actual_resource_parent_assignments'] += enumerated

    # Degenerate domains: isolated zero-demand root scores one; an X without a
    # selectable label has score zero and cannot satisfy the floor's premise.
    assert exact_tree_optimum([])[0] == 1
    assert exact_tree_optimum([()])[0] == 0
    assert exact_tree_optimum([((1, ()),)])[0] == 0
    totals['boundary_dags'] = 3
    return {
        'status': 'pass',
        'identity': 'bounded_collision_bundle_independent',
        'arithmetic': 'fractions.Fraction; full original resource-parent oracle',
        'seed': 2026101711,
        'python': platform.python_version(),
        'counts': dict(sorted(totals.items())),
        'sharpness_samples': examples,
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'scope': 'finite actual-root-tree audit only; no normative import; no general hardness proof',
    }


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2, sort_keys=True))
