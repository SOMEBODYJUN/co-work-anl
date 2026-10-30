#!/usr/bin/env python3
"""Literal Fraction audit for ordered-cohort freezing; finite evidence only."""
from fractions import Fraction as Q
from itertools import combinations, product
from math import factorial
import argparse
import hashlib
import json
import random
import sys


def subsets(s):
    s = tuple(sorted(s))
    return [frozenset(t) for r in range(len(s)+1) for t in combinations(s, r)]


def ordered_partitions(n):
    if n == 0:
        yield []
        return
    for partition in ordered_partitions(n-1):
        for k in range(len(partition)):
            yield [block + [n-1] if j == k else list(block)
                   for j, block in enumerate(partition)]
        for k in range(len(partition)+1):
            yield partition[:k] + [[n-1]] + partition[k:]


def full_support_parameter(weights, groups, d):
    values = []
    for j, group in enumerate(groups):
        a, b = min(weights[i] for i in group), max(weights[i] for i in group)
        tail = sum((weights[i] for later in groups[j+1:] for i in later), Q(0))
        values.append(b/a*(1+tail/a)**d)
    return max(values)


def poly(coeffs, x):
    return sum((a*x**k for k, a in enumerate(coeffs)), Q(0))


def audit(weights, strategies, coeffs, groups):
    n, resources = len(weights), range(len(coeffs))
    d = max(len(c)-1 for c in coeffs)
    potential = [{i for i in range(n) if any(e in s for s in strategies[i])}
                 for e in resources]
    params = {}
    for j, group in enumerate(groups):
        later = set().union(*map(set, groups[j+1:]))
        for e in resources:
            users = potential[e] & set(group)
            if users:
                a, b = min(weights[i] for i in users), max(weights[i] for i in users)
                tail = sum((weights[i] for i in later & potential[e]), Q(0))
                params[e, j] = (a, b/a, (1+tail/a)**d)
    alpha = max((ratio*beta for _, ratio, beta in params.values()), default=Q(1))

    def cost(state, i, choice):
        return sum((poly(coeffs[e], weights[i] + sum(
            (weights[k] for k in range(n) if k != i and state[k] is not None
             and e in state[k]), Q(0))) for e in choice), Q(0))

    def stage_phi(state, j):
        total = Q(0)
        for e in resources:
            if (e, j) not in params:
                continue
            a, _, beta = params[e, j]
            group_users = frozenset(i for i in groups[j] if e in state[i])
            heavy = sum((weights[i] for k in range(j) for i in groups[k]
                         if e in state[i]), Q(0))
            m = len(group_users)
            for t in subsets(group_users):
                if t:
                    z = sum((weights[i] for i in t), Q(0))
                    total += beta/a * Q(factorial(len(t)-1)*factorial(m-len(t)),
                                        factorial(m)) * z*poly(coeffs[e], heavy+z)
        return total

    def stage_marginal(state, j, i):
        empty = list(state)
        empty[i] = frozenset()
        return stage_phi(state, j)-stage_phi(empty, j)

    prefixes = [[None]*n]
    stage_states = stage_candidates = 0
    for j, group in enumerate(groups):
        next_prefixes = []
        for prefix in prefixes:
            candidates = []
            for choices in product(*(strategies[i] for i in group)):
                state = list(prefix)
                for i, choice in zip(group, choices):
                    state[i] = choice
                candidates.append((stage_phi(state, j), state))
            stage_candidates += len(candidates)
            optimum = min(v for v, _ in candidates)
            minima = [state for v, state in candidates if v == optimum]
            stage_states += len(minima)
            next_prefixes.extend(minima)
        prefixes = next_prefixes

    deviations = 0
    for final in prefixes:
        for j, group in enumerate(groups):
            reduced = list(final)
            for later in groups[j+1:]:
                for i in later:
                    reduced[i] = None
            for i in group:
                old_cost = cost(final, i, final[i])
                old_marginal = stage_marginal(reduced, j, i)
                assert old_cost <= old_marginal
                for choice in strategies[i]:
                    moved = list(reduced)
                    moved[i] = choice
                    new_marginal = stage_marginal(moved, j, i)
                    new_stage_cost = cost(reduced, i, choice)
                    new_final_cost = cost(final, i, choice)
                    assert old_marginal <= new_marginal
                    assert new_marginal <= alpha*new_stage_cost
                    assert new_stage_cost <= new_final_cost
                    assert old_cost <= alpha*new_final_cost
                    deviations += 1
    return {'players': n, 'degree': d, 'alpha': str(alpha),
            'input': {'weights':list(map(str, weights)),
                      'strategies':[[sorted(s) for s in fam] for fam in strategies],
                      'coefficients':[[str(a) for a in c] for c in coeffs],
                      'groups':groups},
            'stage_candidates': stage_candidates, 'stage_minima': stage_states,
            'final_profiles': len(prefixes), 'deviations': deviations}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', help='Create a NEW JSON record; refuse existing paths.')
    parser.add_argument('--check', help='Recompute and compare an existing record without modifying it.')
    args = parser.parse_args()
    if args.output and args.check:
        parser.error('--output and --check are mutually exclusive')
    rng = random.Random(712941)
    cases = []
    # Boundary cases: zero polynomials, constants, empty strategies/resources,
    # retained resources, one stage, singleton and nonuniform local groups.
    cases.append(audit([Q(1)], [[frozenset(), frozenset({0})]], [[Q(0)]], [[0]]))
    cases.append(audit([Q(1)], [[frozenset()]], [[Q(3)]], [[0]]))
    cases.append(audit([Q(9), Q(1)], [[frozenset({0})], [frozenset({0,1}),
                 frozenset({1})]], [[Q(2)], [Q(0)]], [[0], [1]]))
    all_s = subsets(range(3))
    for index in range(40):
        if index % 2:
            weights, groups = [Q(64), Q(64), Q(4), Q(4), Q(1,8)], [[0,1],[2,3],[4]]
        else:
            weights, groups = [Q(24), Q(16), Q(4), Q(1), Q(1,2)], [[0,1],[2],[3,4]]
        strategies = []
        for i in range(len(weights)):
            pool = all_s if (index+i) % 7 == 0 else all_s[1:]
            strategies.append(rng.sample(pool, rng.randint(1,3)))
        d = index % 6
        coeffs = [[Q(rng.randint(0,3), rng.randint(1,4)) for _ in range(d+1)]
                  for _ in range(3)]
        cases.append(audit(weights, strategies, coeffs, groups))

    # Exact two dense-cohort tail factors; arbitrary n is proved in the text.
    dense = []
    for d in [2,3,4,8,16]:
        for n in [d,d*d,2*d*d]:
            heavy = d*n
            beta = (1+Q(n,heavy))**d
            assert beta == Q(d+1,d)**d
            assert beta < Q(11,4)
            assert Q((heavy+n)**d, heavy**d) == beta
            q_min = Q(1, n*heavy+n)
            share_factor = 1/(1-(1-q_min)**d)
            assert share_factor >= 1/(d*q_min)
            dense.append({'d':d,'n':n,'heavy_weight':heavy,'alpha':str(beta),
                          'support':2*n,'min_share':str(q_min),
                          'high_degree_factor':str(share_factor)})
    parameter_limits = []
    for heavy in [Q(1), Q(3,2), Q(2)]:
        ceiling_square = -(-(heavy**2).numerator // (heavy**2).denominator)
        for k in sorted({1, 2, ceiling_square}):
            weights = [heavy]+[Q(1)]*k
            partitions = list(ordered_partitions(k+1))
            for d in [1,2,3,5]:
                values = [full_support_parameter(weights, groups, d) for groups in partitions]
                assert min(values) == min(heavy, (1+Q(k)/heavy)**d)
                if k == ceiling_square:
                    assert min(values) == heavy
                parameter_limits.append({'d':d, 'heavy':str(heavy), 'light_count':k,
                                         'partitions':len(partitions),
                                         'minimum_parameter':str(min(values)),
                                         'formula':str(min(heavy, (1+Q(k)/heavy)**d))})
    result = {'finite_evidence_only':True, 'python':sys.version.split()[0],
              'seed':712941, 'arithmetic':'fractions.Fraction',
              'source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest(),
              'games':len(cases),
              'stage_candidates':sum(c['stage_candidates'] for c in cases),
              'stage_minima':sum(c['stage_minima'] for c in cases),
              'final_profiles':sum(c['final_profiles'] for c in cases),
              'deviations':sum(c['deviations'] for c in cases),
              'parameter_limit_cases':len(parameter_limits),
              'parameter_partition_checks':sum(c['partitions'] for c in parameter_limits),
              'cases':cases,'dense_cohort_parameters':dense,
              'parameter_limits':parameter_limits}
    if args.output:
        with open(args.output, 'x', encoding='utf-8') as target:
            json.dump(result, target, ensure_ascii=False, indent=2)
            target.write('\n')
    elif args.check:
        with open(args.check, encoding='utf-8') as source:
            assert json.load(source) == result, 'Recomputation differs from frozen record'
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.output or args.check:
        print(json.dumps({k:result[k] for k in ['finite_evidence_only','games',
              'stage_candidates','stage_minima','final_profiles','deviations',
              'parameter_limit_cases','parameter_partition_checks','source_sha256']},
              ensure_ascii=False))


if __name__ == '__main__':
    main()
