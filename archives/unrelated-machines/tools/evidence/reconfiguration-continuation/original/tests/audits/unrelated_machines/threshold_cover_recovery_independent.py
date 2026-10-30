#!/usr/bin/env python3
"""Independent finite checks of exact-cover cost and supplied joint witnesses."""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from pathlib import Path
import hashlib
import importlib.util
import json
import platform
import random

ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT/'tests/audits/unrelated_machines/threshold_cover_recovery.py'
DEPENDENCY = TARGET.with_name('weighted_group_joint_slot.py')
FROZEN = hashlib.sha256(TARGET.read_bytes()).hexdigest()
spec = importlib.util.spec_from_file_location('threshold_subject', TARGET)
subject = importlib.util.module_from_spec(spec)
spec.loader.exec_module(subject)
SEED = 61749381
rng = random.Random(SEED)


def subset_oracle(weights, demand):
    values = [F(0)]
    for weight in weights:
        values += [v+weight for v in values]
    return min(v for v in values if v >= demand)


def check_cover(weights, demand, eta):
    optimum = subset_oracle(weights, demand)
    ids, cost, cap = subject.minimum_cover(weights, demand, eta)
    assert len(ids) == len(set(ids))
    assert all(isinstance(i, int) and 0 <= i < len(weights) for i in ids)
    assert cost == sum((weights[i] for i in ids), F(0))
    assert demand <= cost <= (1+eta)*optimum
    assert cap <= 2*len(weights)/eta+len(weights)
    return cost


def recompute(groups, sink_count, macros, T, delta, tau, eta, a, y):
    answer = subject.round_certificate(groups, sink_count, macros, T, delta,
                                       tau, eta, a, y)
    homes = [F(0)]*len(groups)
    sinks = [F(0)]*sink_count
    assert len(answer['macro_assignment']) == len(macros)
    assert len(answer['private_assignment']) == len(groups)
    for b, h in enumerate(answer['macro_assignment']):
        assert h in macros[b] and macros[b][h] <= T
        homes[h] += macros[b][h]
    for h, row in enumerate(answer['private_assignment']):
        assert len(row) == len(groups[h]['weights'])
        sent = F(0)
        ids = []
        for j, (kind, dest) in enumerate(row):
            weight = groups[h]['weights'][j]
            if kind == 'h':
                assert dest == h
                homes[h] += weight
            else:
                assert kind == 'z' and dest in groups[h]['eligible']
                sinks[dest] += weight
                sent += weight
                ids.append(j)
        if ids:
            assert ids == answer['cover_indices'][h]
            assert sent == answer['cover_costs'][h]
    assert homes == answer['home_loads']
    assert sinks == answer['sink_loads']
    assert all(v <= (1+tau)*T for v in homes)
    assert all(v <= (1+eta)*(2-tau+delta)*T for v in sinks)
    # This is the stronger local ordered-slot bound, using only positive support.
    for z, load in enumerate(sinks):
        fractional = sum((answer['cover_costs'][h]*y[h].get(z, 0)
                          for h in range(len(groups))), F(0))
        largest = max([answer['cover_costs'][h] for h in range(len(groups))
                       if y[h].get(z, 0)] or [F(0)])
        assert load <= fractional+largest
    return answer


cover_checks = 0
for n in range(7):
    for integers in combinations_with_replacement(range(6), n):
        weights = [F(v, 7) for v in integers]
        for numerator in range(sum(integers)+1):
            for eta in (F(1, 10), F(2, 5), F(3, 2)):
                check_cover(weights, F(numerator, 7), eta)
                cover_checks += 1

random_cover_checks = 0
for trial in range(800):
    n = rng.randrange(9)
    scale = F(1, 2**127+1) if trial % 13 == 0 else F(1)
    weights = [F(rng.randrange(11), rng.choice([3, 5, 7, 11]))*scale
               for _ in range(n)]
    total = sum(weights, F(0))
    demand = total*F(rng.randrange(18), 17)
    for eta in (F(1, 17), F(2, 5), F(3, 2)):
        check_cover(weights, demand, eta)
        random_cover_checks += 1

witness_checks = 0
nonintegral_witnesses = 0
no_sink_witnesses = 0
rejected_for_budget = 0
for trial in range(2400):
    H, sinks = rng.randrange(9), rng.randrange(5)
    if H+sinks == 0:
        sinks = 1
    tau = rng.choice([F(1, 2), F(3, 5), F(3, 4), F(9, 10)])
    eta = rng.choice([F(1, 17), F(2, 5), F(3, 2)])
    delta = F(2, 5)
    groups = []
    for h in range(H):
        while True:
            weights = [F(rng.randrange(18), 50) for _ in range(rng.randrange(9))]
            if sum(weights, F(0)) <= 1:
                break
        E = [z for z in range(sinks) if rng.randrange(3)]
        groups.append({'weights':weights, 'eligible':E})
    costs = [subject.minimum_cover(g['weights'], max(F(0), sum(g['weights'])-tau), eta)[1]
             for g in groups]
    usable = [h for h, g in enumerate(groups) if g['eligible'] or costs[h] == 0]
    B = rng.randrange(len(usable)+1)
    macros = [{h:F(rng.randrange(11, 21), 20) for h in range(H)} for _ in range(B)]
    a = [{} for _ in range(B)]
    y = [{} for _ in range(H)]
    masses = [rng.randrange(1, 7) for _ in range(rng.randrange(2, 8))]
    denominator = sum(masses)
    for mass in masses:
        share = F(mass, denominator)
        injection = rng.sample(usable, B)
        for b, h in enumerate(injection):
            a[b][h] = a[b].get(h, F(0))+share
            E = groups[h]['eligible']
            z = None if costs[h] == 0 and (not E or rng.randrange(2)) else rng.choice(E)
            y[h][z] = y[h].get(z, F(0))+share
    if any(sum((costs[h]*y[h].get(z, 0) for h in range(H)), F(0)) > 1+eta
           for z in range(sinks)):
        rejected_for_budget += 1
        continue
    recompute(groups, sinks, macros, 1, delta, tau, eta, a, y)
    witness_checks += 1
    nonintegral_witnesses += any(v.denominator > 1 for row in a+y for v in row.values())
    no_sink_witnesses += sinks == 0

prefix_family = []
for r in range(1, 21):
    s = F(1, 10*r)
    count = 5*r
    weights = [F(1, 5)]+[s]*(3*r+1)
    groups = [{'weights':weights, 'eligible':[0]} for _ in range(count)]
    macros = [{h:F(1, 2)+s} for h in range(count)]
    a = [{h:F(1)} for h in range(count)]
    y = [{0:F(1)} for _ in range(count)]
    answer = recompute(groups, 1, macros, 1, F(1, 5), F(1, 2), F(1, 100), a, y)
    assert answer['sink_loads'] == [F(1, 2)]
    assert max(answer['home_loads']) == 1+s
    assert F(count)*2*s == 1
    assert (F(1, 2)+s)+sum(weights)-2*s == 1
    prefix_family.append({'r':r, 'prefix_sink':str(count*weights[0]),
                          'correct_cover_sink':str(answer['sink_loads'][0]),
                          'correct_home_max':str(max(answer['home_loads']))})

search_checks = 0
for bound in range(10):
    for kstar in range(bound+1):
        for mask in range(1 << kstar):
            def accepted(k):
                return k >= kstar or bool((mask >> k) & 1)
            low, high = -1, bound
            while high-low > 1:
                mid = (high+low)//2
                if accepted(mid):
                    high = mid
                else:
                    low = mid
            assert accepted(high) and high <= kstar
            search_checks += 1

assert FROZEN == hashlib.sha256(TARGET.read_bytes()).hexdigest(), 'subject changed during review'
print(json.dumps({'verdict':'finite exact checks passed; theorem conditional on corrected prose',
                  'python':platform.python_version(), 'seed':SEED,
                  'target_sha256':FROZEN,
                  'dependency_sha256':hashlib.sha256(DEPENDENCY.read_bytes()).hexdigest(),
                  'review_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  'integer_scaled_cover_checks':cover_checks,
                  'rational_sample_cover_checks':random_cover_checks,
                  'valid_joint_witness_checks':witness_checks,
                  'fractional_joint_witnesses':nonintegral_witnesses,
                  'no_sink_witnesses':no_sink_witnesses,
                  'discarded_overbudget_draws':rejected_for_budget,
                  'prefix_family':prefix_family,
                  'one_sided_search_predicates':search_checks,
                  'scope':'exact subset oracle; supplied valid joint witnesses; original-task resummation; no LP generation'},
                 ensure_ascii=False, indent=2))
