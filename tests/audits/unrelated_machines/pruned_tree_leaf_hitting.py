#!/usr/bin/env python3
"""Independent exhaustive leaf families/subsets; no normative imports."""
from itertools import combinations, product
from pathlib import Path
from math import comb
from fractions import Fraction as F
import hashlib
import json


def families(k, h, r):
    if h == 0:
        return {1}
    child = families(k, h - 1, r)
    width = k**(h - 1); out = set()
    for chosen in combinations(range(k), r):
        for parts in product(child, repeat=r):
            mask = 0
            for index, part in zip(chosen, parts):
                mask |= part << (index * width)
            out.add(mask)
    return out


def supersets_table(N, minimal):
    out = bytearray(1 << N)
    for mask in minimal:
        out[mask] = 1
    for bit in range(N):
        flag = 1 << bit
        for mask in range(1 << N):
            if mask & flag and out[mask ^ flag]:
                out[mask] = 1
    return out


def recursive_has(mask, k, h, r):
    values = [bool((mask >> i) & 1) for i in range(k**h)]
    for level in range(h):
        values = [sum(values[i:i+k]) >= r for i in range(0, len(values), k)]
    return values[0]


def canonical_q_leaves(k, h, q):
    selected = []
    for word in product(range(k), repeat=h):
        if all(digit < q for digit in word):
            value = 0
            for digit in word:
                value = value * k + digit
            selected.append(value)
    return selected


def private_readout_certificates(positive, negative):
    """Two complete170-machine297-job original matrices; no generator import."""
    k, h, N = 4, 3, 64
    machines = []; internal = {}
    for sign in (0, 1):
        for level in range(h):
            for word in product(range(k), repeat=level):
                internal[sign, word] = len(machines)
                machines.append({'kind': 'internal', 'sign': sign, 'word': word})
    assert len(machines) == 42
    for sign in (0, 1):
        for code in range(N):
            machines.append({'kind': 'private_host', 'sign': sign, 'leaf_code': code})
    jobs = [{'kind': 'selector', 'eligible': {internal[0, ()]: F(1), internal[1, ()]: F(1)}}]
    for sign in (0, 1):
        for level in range(1, h):
            for word in product(range(k), repeat=level):
                jobs.append({'kind': 'tree_edge', 'sign': sign, 'word': word,
                             'eligible': {internal[sign, word[:-1]]: F(1, k), internal[sign, word]: F(1)}})
        for code, word in enumerate(product(range(k), repeat=h)):
            host = 42 + sign * N + code
            jobs.append({'kind': 'leaf_port', 'sign': sign, 'word': word, 'leaf_code': code,
                         'eligible': {internal[sign, word[:-1]]: F(1, k), host: F(1)}})
    assert len(jobs) == 169
    output = []
    for name, sets, full_positive in (
            ('all_positive64_open_exact_OPT1', (list(range(N)), []), True),
            ('r_free37_plus27_open_exact_OPT7_over4', (positive, negative), False)):
        open_hosts = {42 + sign * N + code for sign in (0, 1) for code in sets[sign]}
        assert len(open_hosts) == 64
        best_each = [max([0] + [r for r in range(1, k + 1)
                               if recursive_has(sum(1 << code for code in sets[sign]), k, h, r)])
                     for sign in (0, 1)]
        best = max(best_each)
        optimum = F(2) - F(best, k)
        chosen_code = positive[0]
        chosen_word = tuple((chosen_code // k**power) % k for power in range(h - 1, -1, -1))
        sigma = []
        for job in jobs:
            if job['kind'] == 'selector':
                owner = internal[0, ()]
            elif job['kind'] == 'tree_edge':
                sign, word = job['sign'], job['word']
                down = sign == 0 and (full_positive or word == chosen_word[:len(word)])
                owner = internal[sign, word if down else word[:-1]]
            else:
                sign, word, code = job['sign'], job['word'], job['leaf_code']
                out = sign == 0 and (full_positive or code == chosen_code)
                owner = 42 + sign * N + code if out else internal[sign, word[:-1]]
            sigma.append(owner)
        pins = [{'kind': 'actual_fixed_preload',
                 'eligible': {host: F(0 if host in open_hosts else 1)}}
                for host in range(42, 170)]
        original = jobs + pins
        sigma += list(range(42, 170))
        loads = [F(0)] * 170
        for job, owner in zip(original, sigma):
            assert owner in job['eligible']
            loads[owner] += job['eligible'][owner]
        assert len(original) == len(sigma) == 297
        assert max(loads) == optimum == (F(1) if full_positive else F(7, 4))
        output.append({'name': name, 'machines': machines, 'original_jobs': original,
                       'open_hosts': sorted(open_hosts), 'open_leaf_codes_by_sign': sets,
                       'sigma': sigma, 'actual_machine_loads': loads, 'actual_makespan': max(loads),
                       'maximum_uniform_pruning_quota_by_sign': best_each,
                       'exact_optimum_by_open_leaf_DP_and_closed_host_bound': optimum,
                       'scope': 'two private0/1preload states; not a counterexample to dense globalSTmatching'})
    return output


def audit():
    cases = [(1, h) for h in range(1, 5)]
    cases += [(2, h) for h in range(1, 4)]
    cases += [(3, h) for h in range(1, 3)]
    cases += [(4, h) for h in range(1, 3)]
    checked = subsets = family_count = 0
    records = []
    for k, h in cases:
        N = k**h; full = (1 << N) - 1
        for r in range(1, k + 1):
            q = k - r + 1
            r_family = families(k, h, r); q_family = families(k, h, q)
            contained = supersets_table(N, r_family)
            dual_contained = supersets_table(N, q_family)
            max_free = -1; min_hit = N + 1; nonmono = False
            expected_family_count = comb(k, r)**sum(r**level for level in range(h))
            assert len(r_family) == expected_family_count
            for mask in range(1 << N):
                hitting = not contained[full ^ mask]
                assert hitting == bool(dual_contained[mask])
                if hitting:
                    min_hit = min(min_hit, mask.bit_count())
                if not contained[mask]:
                    max_free = max(max_free, mask.bit_count())
                mono = contained[mask] or contained[full ^ mask]
                if 2 * (r - 1) < k:
                    assert mono
                nonmono |= not mono
                assert recursive_has(mask, k, h, r) == bool(contained[mask])
                subsets += 1
            assert min_hit == q**h and max_free == N - q**h
            assert nonmono == (2 * (r - 1) >= k)
            checked += 1; family_count += len(r_family)
            records.append({'k': k, 'h': h, 'r': r, 'leaf_count': N,
                            'all_r_subtree_leafsets': len(r_family),
                            'minimum_hitting': min_hit, 'maximum_free': max_free,
                            'two_color_universal_monochromatic': not nonmono})
    k, h, r, q, N = 4, 3, 2, 3, 64
    hit = set(canonical_q_leaves(k, h, q))
    free = [leaf for leaf in range(N) if leaf not in hit]
    positive = free; negative = free[:27]
    mask = lambda selected: sum(1 << leaf for leaf in selected)
    assert len(hit) == 27 and len(positive) == 37 and len(negative) == 27
    assert not recursive_has(mask(positive), k, h, r)
    assert not recursive_has(mask(negative), k, h, r)
    return {'status': 'pass', 'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'counts': {'parameter_cases': checked, 'leaf_subsets_checked': subsets,
                       'explicit_r_subtree_leafsets': family_count},
            'records': records,
            'bad_half_matching': {'k': k, 'h': h, 'r': r,
                'positive_leaf_codes': positive, 'negative_leaf_codes': negative,
                'selected_total': len(positive) + len(negative),
                'both_rails_r_free': True,
                'scope': 'explicit64-leaf construction only; no2^64 subset enumeration or full actual scheduling enumeration'},
            'private_readout_certificates': private_readout_certificates(positive, negative),
            'scope': 'independent explicit r-subtree families, allsmall leaf subsets, duality, extremal counts and two-color threshold; primitive tree fact only'}


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2, sort_keys=True, default=str))
