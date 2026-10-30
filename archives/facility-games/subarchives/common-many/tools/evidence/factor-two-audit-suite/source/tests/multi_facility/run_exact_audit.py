"""Reproducible finite arithmetic attacks, not a proof of SC-K-2-E."""
from __future__ import annotations
import argparse
import copy
import json
import platform
import random
import sys
from fractions import Fraction as F
from itertools import combinations_with_replacement, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from multi_facility_spe.two_exists import (Instance, construct, merge_pack,
    search_lexmax, uniform_profile, loads, deviation_witness, pure_profile)
from definition_check import check_certificate, check_ne, independent_lexmax, brute_pure_equilibria


def instance(weights, covers, m, k):
    return Instance(tuple(F(x) for x in weights), tuple(frozenset(c) for c in covers), m, k)


def run():
    seed = 20261002
    rng = random.Random(seed)
    results = []
    feature_counts = dict(singleton_departures=0, nonsingleton_departures=0,
                          occupied_targets=0, unoccupied_targets=0,
                          isolated_giants=0, strict_customer_moves=0)
    default_count = 0
    reverse_lex_checks = 0
    pure_extremum_comparisons = 0
    saved = []

    cases = []
    # Exhaust all ordered two-client coverage/weight inputs over two sites,
    # including globally unreachable clients. Full labeled continuation check.
    masks = [set(), {0}, {1}, {0, 1}]
    for k in (2, 3, 4):
        for weights in product((1, 2, 5), repeat=2):
            for covers in product(masks, repeat=2):
                cases.append((f'exhaustive-k{k}-{len(cases)}',
                              instance(weights, covers, 2, k), True, False))
    # Exact rational, overlapping, duplicate-coverage and asymmetric examples.
    specials = [
        ('heavy-three-sites', instance([100, 1, 20], [{0, 1}, {0}, {2}], 3, 5)),
        ('orphan-overlap', instance([5, 7, 11, 1], [{0, 1}, {1, 2}, {0, 2}, {0}], 3, 3)),
        ('rational', instance([F(1, 97), F(3, 7), F(11, 13), F(2, 5)],
                              [{0}, {0, 1}, {1, 2}, {2}], 3, 4)),
        ('single-site', instance([100, 2, 3], [{0}, {0}, set()], 1, 7)),
        ('zero-clients', instance([], [], 3, 3)),
        ('unreachable-only', instance([1, 100], [set(), set()], 3, 3)),
        ('one-facility', instance([3, 7, 11], [{0}, {1}, {0, 2}], 3, 1)),
    ]
    for name, inst in specials:
        cases.append((name, inst, True, True))
    for j in range(120):
        m = rng.choice((2, 3))
        k = rng.choice((2, 3, 4, 5, 6))
        n = rng.randrange(1, 7)
        weights = [F(rng.choice((1, 2, 3, 7, 19, 101)), rng.choice((1, 1, 2, 7)))
                   for _ in range(n)]
        covers = [{s for s in range(m) if rng.randrange(3)} for _ in range(n)]
        inst = instance(weights, covers, m, k)
        cases.append((f'random-{j}', inst, j < 15 and n <= 4 and k <= 4,
                      j < 12 and n <= 4 and k <= 4))
    # Scalable families test growing k without pretending finite checks prove it.
    for k in (7, 12, 25, 50):
        cases.append((f'growing-k-{k}',
                      instance([k*k, 1, 2*k], [{0, 1}, {0}, {2}], 3, k),
                      False, False))

    for index, (name, inst, full, reverse) in enumerate(cases):
        cert = construct(inst)
        checked = check_certificate(cert, all_layouts=full)
        default_count += checked['unlisted_labeled_layouts_checked']
        if reverse:
            independent = independent_lexmax(inst.to_json())
            assert tuple(F(x) for x in cert['search_audit']['lex_key']) == independent
            reverse_lex_checks += 1
        for d in cert['deviations']:
            stats = d['audit']
            if inst.covers and any(inst.covers):
                feature_counts['singleton_departures' if stats['departed_site_disappears']
                               else 'nonsingleton_departures'] += 1
                feature_counts['occupied_targets' if stats['target_previously_occupied']
                               else 'unoccupied_targets'] += 1
                feature_counts['isolated_giants'] += stats['isolated_giants']
                feature_counts['strict_customer_moves'] += stats['strict_improvement_steps']
            if reverse and inst.k <= 4 and len(inst.weights) <= 4:
                target = list(cert['on_path']['layout'])
                target[d['facility']] = d['site']
                equilibria = brute_pure_equilibria(inst.to_json(), target)
                minimum = min(L[d['facility']] for _, L in equilibria)
                a = check_ne(inst.to_json(), cert['on_path']['layout'],
                             cert['on_path']['probabilities'])[d['facility']]
                assert minimum <= 2 * a
                pure_extremum_comparisons += 1
        results.append(dict(name=name, instance=inst.to_json(),
                            on_path_layout=cert['on_path']['layout'],
                            lex_key=cert['search_audit']['lex_key'],
                            **checked))
        if name in ('heavy-three-sites', 'orphan-overlap', 'rational', 'growing-k-12'):
            saved.append((name, cert))
    # Independent small packing domain, including exact capacity equalities.
    packing_cases = 0
    for q in range(1, 7):
        for n in range(0, 6):
            for weights in combinations_with_replacement((F(1, 2), F(1), F(2), F(3), F(5)), n):
                if sum(weights, F(0)) > q + 1:
                    continue
                inst = instance(weights, [set() for _ in weights], 1, 1)
                bins = merge_pack(inst, list(range(n)), q, F(1))
                assert sorted(i for b in bins for i in b) == list(range(n))
                assert len(bins) <= q
                assert all(sum(weights[i] for i in b) <= 2 or
                           (len(b) == 1 and weights[b[0]] > 2) for b in bins)
                packing_cases += 1
    # Mutations must be rejected by the checker, not by the constructor.
    base = saved[0][1]
    mutations = []
    broken = copy.deepcopy(base)
    broken['deviations'].pop()
    mutations.append(broken)
    broken = copy.deepcopy(base)
    broken['on_path']['probabilities'][0] = ['0'] * base['instance']['k']
    mutations.append(broken)
    broken = copy.deepcopy(base)
    broken['deviations'][0]['pure_assignment'][0] = -1
    mutations.append(broken)
    rejected = 0
    for broken in mutations:
        try:
            check_certificate(broken)
        except AssertionError:
            rejected += 1
    assert rejected == len(mutations)
    for name, cert in saved:
        path = ROOT / 'evidence' / 'certificates' / 'multi_facility' / f'{name}.json'
        # Frozen examples were created once; a regression must not overwrite them.
        roundtrip = json.loads(path.read_text())
        assert roundtrip == cert
        check_certificate(roundtrip)
        example = ROOT / 'examples' / 'multi_facility' / f'{name}.json'
        assert json.loads(example.read_text()) == cert['instance']
    return dict(claim='SC-K-2-E', evidence_kind='finite exact arithmetic attacks only',
                seed=seed, python=platform.python_version(),
                full_proof='research/current/multi_facility/uniform_two.md',
                cases=len(results), actual_deviations=sum(r['actual_deviations_checked'] for r in results),
                unlisted_labeled_layouts_checked=default_count,
                independent_labeled_lexmax_comparisons=reverse_lex_checks,
                independent_pure_NE_extremum_comparisons=pure_extremum_comparisons,
                packing_cases=packing_cases, mutations_rejected=rejected,
                feature_counts=feature_counts, results=results)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({k: v for k, v in output.items() if k != 'results'}, indent=2))
