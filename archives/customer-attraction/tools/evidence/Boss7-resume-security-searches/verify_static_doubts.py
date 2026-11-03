"""Finite, exact checks of two specific ambiguities in saved reports.

No original modules, SPE recurrence, strategy/IC enumeration, LP, or random search.
The n4/k5 micro-negative score gets an explicit pure saddle certificate.
The cyclic integer status is checked against all static rival counts only.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement
import hashlib
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent


def counts(n, k):
    return [tuple(s.count(a) for a in range(k))
            for s in combinations_with_replacement(range(k), n)]


def payoff(w, h, a):
    return sum((F(v, 1 + sum(h[b] for b in range(len(h)) if m >> b & 1))
                for m, v in enumerate(w, 1) if m >> a & 1), F())


def coverage(w, q):
    return sum(v for m, v in enumerate(w, 1)
               if any(q[a] and m >> a & 1 for a in range(len(q))))


def necklace(mask):
    return min(mask[i:] + mask[:i] for i in range(len(mask)))


def main():
    start = time.monotonic()
    source_sha = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in (HERE / 'original').glob('*.json')}
    index = json.loads((HERE / 'complete-record-read-index.json').read_text())
    out = {'n4_k5': [], 'cyclic_n5_k6': []}
    n4 = next(r for r in index if r['name'] == 'search_n4_k5.json')
    for group in n4['record_groups']:
        r = group['record']; w = r['weights']; h = (0, 0, 0, 3, 0)
        assert (r['n'], r['k']) == (4, 5)
        assert all(type(v) is int and v >= 0 for v in w) and len(w) == 31
        W = sum(v for m, v in enumerate(w, 1) if m >> 3 & 1)
        v = F(W, 4)
        cap = [payoff(w, h, a) for a in range(5)]
        assert max(cap) == v and cap[3] == v
        # Pure T3 guarantees |T3|/4 for every 3-slot background by denominator <=4.
        # h=3T3 caps every pure query at that same value: exact primal + dual.
        assert all(cap[a] - v <= 0 for a in range(5))
        assert r['worst_counts'] == [[0, 0, 0, 4, 0]]
        assert r['min_welfare'] == W
        assert abs(F(str(r['value'])) - v) <= F(1, 10**12)
        # This is a fixed-terminal PNE check, not a sequential SPE certificate.
        static_excess = max(F(), *(x - v for x in cap))
        assert static_excess == 0
        opt = max(coverage(w, q) for q in counts(4, 5))
        assert opt == r['max_welfare']
        out['n4_k5'].append({'locations': group['locations'], 'customers': sum(w),
                            'topic3_size': W, 'v': str(v), 'gap_W_minus_4v': '0',
                            'rival_payoff_vector': list(map(str, cap)),
                            'static_deviation_excess': str(static_excess),
                            'OPT4': opt, 'terminal_counts_checked': 70})
    cyc = next(r for r in index if r['name'] == 'cyclic_n5_k6.json')
    classes = list(map(tuple, cyc['root_fields_except_records']['classes']))
    masks = [tuple(int(m >> a & 1) for a in range(6)) for m in range(1, 64)]
    labels = [necklace(m) for m in masks]
    assert classes == sorted(set(labels) - {(1,) * 6})
    orbit_sizes = [labels.count(c) for c in classes]
    backgrounds = counts(4, 6)
    assert len(backgrounds) == 126
    for group in cyc['record_groups']:
        r = group['record']; w = r['weights']; x = r['orbit_weights']
        assert (r['n'], r['k']) == (5, 6)
        assert len(x) == 12 and len(w) == 63
        expected = [x[classes.index(lab)] if lab in classes else 0 for lab in labels]
        assert expected == w and all(type(v) is int and v >= 0 for v in w)
        # n=5 gives L=60, hence uniform query denominator 6L=360.
        nums = [sum(v * sum(mask) * (60 // (1 + sum(t * q for t, q in zip(mask, h))))
                    for v, mask in zip(w, masks)) for h in backgrounds]
        vm = min(nums)
        minimizers = [list(h) for h, z in zip(backgrounds, nums) if z == vm]
        assert vm == r['value_numerator'] and r['value_denominator'] == 360
        assert minimizers == r['minimizing_backgrounds']
        assert r['gap_numerator'] == r['min_welfare'] * 360 - 5 * vm
        assert abs(F(str(r['relative_gap'])) - F(r['gap_numerator'], 5 * vm)) < F(1, 10**15)
        # These are leaf coverage identities, without SPE qualifications.
        assert all(coverage(w, q) == r['min_welfare'] for q in r['worst_counts'])
        assert all(q in [list(t) for t in counts(5, 6)] for q in r['worst_counts'])
        assert len(r['worst_counts']) == 6
        assert all(sorted(q) == [0, 1, 1, 1, 1, 1] for q in r['worst_counts'])
        assert r['min_welfare'] == sum(w)
        out['cyclic_n5_k6'].append({'locations': group['locations'],
             'orbit_weights': x, 'customers': sum(w), 'v': str(F(vm, 360)),
             'value_numerator': vm, 'gap_numerator': r['gap_numerator'],
             'minimizing_background_count': len(minimizers),
             'all_minimizers_are_four_distinct': all(max(h) == 1 for h in minimizers)})
    assert {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (HERE / 'original').glob('*.json')} == source_sha
    out.update(status='PASS_EXACT_STATIC_DOUBTS_ONLY', source_sha256=source_sha,
               cyclic_orbit_sizes=orbit_sizes,
               exact_unique_n4_k5_inputs=len(out['n4_k5']),
               exact_unique_cyclic_inputs=len(out['cyclic_n5_k6']),
               elapsed_seconds=time.monotonic() - start,
               exclusions=['original module import', 'SPE recurrence', 'strategy reconstruction',
                           'all-history IC', 'LP', 'random search',
                           'n4_k6/n5_k6 static saddle certification'])
    (HERE / 'current-static-doubts-check.json').write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in out.items()
                      if k not in ('n4_k5', 'cyclic_n5_k6')}, indent=2))


if __name__ == '__main__':
    main()
