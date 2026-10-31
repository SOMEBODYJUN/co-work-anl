#!/usr/bin/env python3
"""Definition-level finite audit of the path interval rent budget.

Standard library only. Does not call an equilibrium solver, and does not
certify Q-CAG-HALF. The universal proof is in path_interval_rent_budget.md.
"""
from fractions import Fraction as F
from itertools import product
import argparse
import json
import random
from pathlib import Path


def interval_audit(bits, lengths, weights, reserve):
    m = len(bits)
    assert len(lengths) == len(weights) == max(0, m - 1)
    load = [0]
    for bit in bits:
        load.append(load[-1] + bit)
    slots = [F(0) for _ in bits]
    total = F(0)
    hit_rank_charge = [F(0) for _ in range(load[-1] + 1)]
    for j, (width, weight) in enumerate(zip(lengths, weights), 1):
        assert 0 <= width <= m - j
        assert weight >= 0
        b = load[j]
        q = load[j + width] - b
        total += weight * b * (1 / (F(b) + reserve)
                                - 1 / (F(b + q) + reserve))
        for t in range(j, j + width):
            slots[t] += j * weight
        # Independently allocate the real-window insertion to actual hit ranks.
        for t in range(j + 1, j + width + 1):
            if bits[t - 1]:
                hit_rank_charge[load[t]] += weight * b
    rank_total = sum((hit_rank_charge[k]
                      / ((reserve + k - 1) * (reserve + k))
                      for k in range(1, load[-1] + 1)), F(0))
    assert rank_total == total
    if load[-1]:
        assert hit_rank_charge[1] == 0
    congestion = max(slots, default=F(0))
    assert all(charge <= congestion for charge in hit_rank_charge[2:])
    bound = (congestion * (1 / (reserve + 1)
                           - 1 / (reserve + load[-1]))
             if load[-1] else F(0))
    assert total <= bound
    assert bound <= (congestion / (reserve + 1) if load[-1] else 0)
    return total, bound, congestion


def run():
    counts = {'single_interval_cases': 0, 'full_width_profiles': 0,
              'weighted_path_cases': 0, 'random_cases': 0}
    reserves = (F(1, 2), F(1), F(2), F(7, 3))
    # Exhaust every single interval on every finite binary path in this range.
    for m in range(1, 10):
        for bits in product((0, 1), repeat=m):
            for j in range(1, m):
                for width in range(m - j + 1):
                    lengths = [0] * (m - 1)
                    lengths[j - 1] = width
                    for reserve in reserves:
                        weights = [F(0)] * (m - 1)
                        weights[j - 1] = F(2 * j + 1, 3 * j)
                        interval_audit(bits, lengths, weights, reserve)
                        counts['single_interval_cases'] += 1
    # Exhaust simultaneous interval-length choices on the smaller range.
    for m in range(1, 6):
        for bits in product((0, 1), repeat=m):
            for lengths in product(*(range(m - j + 1) for j in range(1, m))):
                for reserve in reserves:
                    for mode in range(3):
                        weights = [F(1, j) if mode == 0
                                   else F((j % 3) + 1, j + 2) if mode == 1
                                   else F(j % 2, 2 * j)
                                   for j in range(1, m)]
                        interval_audit(bits, lengths, weights, reserve)
                        counts['full_width_profiles'] += 1
    # Width two and nonuniform larger simultaneous window families.
    width2_max = {}
    for m in range(1, 12):
        best = (F(-1), None)
        for bits in product((0, 1), repeat=m):
            lengths = [min(2, m - j) if j <= m - 2 else 0
                       for j in range(1, m)]
            weights = [F(1, j) for j in range(1, m)]
            total, bound, gamma = interval_audit(bits, lengths, weights, F(1))
            assert total <= (1 - F(2, sum(bits) + 1) if sum(bits) else 0)
            assert gamma <= 2
            if total > best[0]:
                best = (total, ''.join(map(str, bits)))
            counts['weighted_path_cases'] += 1
        width2_max[str(m)] = {'value': str(best[0]), 'path': best[1]}
    rng = random.Random(20261021)
    for _ in range(2000):
        m = rng.randint(2, 128)
        bits = [rng.randrange(2) for _ in range(m)]
        lengths = [rng.randrange(m - j + 1) for j in range(1, m)]
        weights = [F(rng.randrange(5), j * rng.randint(1, 5))
                   for j in range(1, m)]
        interval_audit(bits, lengths, weights, rng.choice(reserves))
        counts['random_cases'] += 1

    # Rejected rank-two refinement: both legal windows charge the second hit.
    two_hit = interval_audit((1, 0, 1, 0), (2, 2, 0),
                             (F(1), F(1, 2), F(1, 3)), F(1))
    assert two_hit[0] == F(1, 4)
    assert two_hit[0] > F(5, 6) - F(2, 3)

    # Dropping interval-contiguity fails even with slot congestion one.
    # One initial hit, q-1 zero slots, then q hits. Prefix j selects only
    # the single future hit at slot q+j, with row weight 1/j.
    for q in range(1, 129):
        for reserve in reserves:
            bits = [1] + [0] * (q - 1) + [1] * q
            direct = F(0)
            for j in range(1, q + 1):
                b = sum(bits[:j])
                inserted = bits[q + j - 1]
                assert b == inserted == 1
                direct += F(1, j) * b * (1 / (b + reserve)
                                          - 1 / (b + reserve + inserted))
            harmonic = sum((F(1, j) for j in range(1, q + 1)), F(0))
            assert direct == harmonic / ((reserve + 1) * (reserve + 2))
    small_noninterval = sum((F(1, 6 * j) for j in range(1, 4)), F(0))
    assert small_noninterval == F(11, 36)
    assert small_noninterval - F(3, 10) == F(1, 180)
    noninterval = sum((F(1, 6 * j) for j in range(1, 65)), F(0))
    noninterval_claim = F(1, 2) - F(1, 66)
    assert noninterval > F(1, 2) > noninterval_claim
    return {
        'status': 'all finite assertions passed',
        'scope': 'arbitrary paths and interval rent errors; no SPE or half theorem',
        'counts': counts,
        'width_two_finite_maxima_not_sharpness_claims': width2_max,
        'rejected_rank_two_refinement': {
            'bits': '1010', 'cost': str(two_hit[0]),
            'incorrect_bound': str(F(5, 6) - F(2, 3))},
        'noncontiguous_slot_packing_counterexample_arbitrary_path': {
            'small_instance': {'m': 6, 'bits': '100111',
                               'cost': str(small_noninterval),
                               'invalid_rank_bound': '3/10', 'gap': '1/180'},
            'infinite_family_formula': 'H_q/((rho+1)*(rho+2)), W=1, Gamma=1',
            'm': 128, 'client_hits': 65, 'slot_congestion': '1',
            'cost': str(noninterval), 'cost_decimal': float(noninterval),
            'invalid_interval_bound': str(noninterval_claim)},
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = run()
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        with args.output.open('x', encoding='utf-8') as out:
            out.write(rendered + '\n')
    print(rendered)
