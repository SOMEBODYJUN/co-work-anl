#!/usr/bin/env python3
"""精确审计：有限任务交换与一出一入循环的局部陷阱。

Independent audit. Generic Fraction assignment enumeration is independent
of the integer-scaled Gray-code enumerator. No search result is a general proof.
"""
from fractions import Fraction as F
from itertools import product
from collections import Counter
from math import comb
import hashlib
import json
import platform
from pathlib import Path


def fanout_instance(k):
    assert k >= 1
    # Each pair is (initial machine, alternative machine, initial time, alt time).
    jobs = [(0, 1, F(1), F(1)), (0, 2, F(1), F(1))]
    jobs += [(i, 0, F(1, k), F(1, 4*k)) for i in (1, 2) for _ in range(2*k)]
    return 3, jobs


def fraction_oracle(m, jobs):
    initial = [F(0)] * m
    for i, _, p, _ in jobs:
        initial[i] += p
    original = tuple(sorted(initial, reverse=True))
    opt = None
    opt_count = 0
    min_lex = None
    min_cmax = None
    min_max_out = None
    one_out_improving = 0
    count = 0
    for bits in product((0, 1), repeat=len(jobs)):
        load = [F(0)] * m
        out = Counter()
        for bit, (i, h, p, q) in zip(bits, jobs):
            load[h if bit else i] += q if bit else p
            if bit:
                out[i] += 1
        key = tuple(sorted(load, reverse=True))
        distance = sum(bits)
        if opt is None or key[0] < opt:
            opt, opt_count = key[0], 1
        elif key[0] == opt:
            opt_count += 1
        if key < original:
            min_lex = distance if min_lex is None else min(min_lex, distance)
            outgoing = max(out.values(), default=0)
            min_max_out = outgoing if min_max_out is None else min(min_max_out, outgoing)
            one_out_improving += int(all(v <= 1 for v in out.values()))
        if key[0] < original[0]:
            min_cmax = distance if min_cmax is None else min(min_cmax, distance)
        count += 1
    return dict(assignments=count, initial=list(map(str, original)), opt=str(opt),
                optimum_count=opt_count, min_lex_distance=min_lex,
                min_makespan_distance=min_cmax,
                min_max_out=min_max_out,
                one_out_improving=one_out_improving)


def gray_integer_oracle(k):
    m, jobs = fanout_instance(k)
    scale = 4*k
    data = [(i, h, int(p*scale), int(q*scale)) for i, h, p, q in jobs]
    load = [0]*m
    for i, _, p, _ in data:
        load[i] += p
    original = tuple(sorted(load, reverse=True))
    opt = original[0]
    opt_count = 0
    min_lex = None
    min_cmax = None
    min_max_out = None
    one_out_improving = 0
    out = [0]*m
    prev = 0
    for s in range(1 << len(data)):
        mask = s ^ (s >> 1)
        if s:
            changed = mask ^ prev
            j = changed.bit_length() - 1
            i, h, p, q = data[j]
            direction = 1 if mask & changed else -1
            load[i] -= direction*p
            load[h] += direction*q
            out[i] += direction
        key = tuple(sorted(load, reverse=True))
        distance = mask.bit_count()
        if key[0] < opt:
            opt, opt_count = key[0], 1
        elif key[0] == opt:
            opt_count += 1
        if key < original:
            min_lex = distance if min_lex is None else min(min_lex, distance)
            min_max_out = max(out) if min_max_out is None else min(min_max_out, max(out))
            one_out_improving += int(max(out) <= 1)
        if key[0] < original[0]:
            min_cmax = distance if min_cmax is None else min(min_cmax, distance)
        prev = mask
    return dict(assignments=1 << len(data), initial=[str(F(x, scale)) for x in original],
                opt=str(F(opt, scale)), optimum_count=opt_count,
                min_lex_distance=min_lex, min_makespan_distance=min_cmax,
                min_max_out=min_max_out,
                one_out_improving=one_out_improving)


def compressed_oracle(k):
    # The independent coordinates are whether each big job moves and the
    # number of original B/C small jobs that move. Every legal schedule has
    # exactly one such coordinate tuple; multiplicities recover all schedules.
    scale = 4*k
    original = (2*scale,)*3
    opt = original[0]
    optimum_count = 0
    min_lex = min_cmax = min_max_out = None
    one_out_improving = 0
    weighted_count = 0
    types = 0
    binomials = [comb(2*k, u) for u in range(2*k+1)]
    for b, c in product((0, 1), repeat=2):
        for u in range(2*k+1):
            for v in range(2*k+1):
                load = ((2-b-c)*scale+u+v,
                        (2+b)*scale-4*u, (2+c)*scale-4*v)
                key = tuple(sorted(load, reverse=True))
                multiplicity = binomials[u]*binomials[v]
                distance = b+c+u+v
                if key[0] < opt:
                    opt, optimum_count = key[0], multiplicity
                elif key[0] == opt:
                    optimum_count += multiplicity
                if key < original:
                    min_lex = distance if min_lex is None else min(min_lex, distance)
                    outgoing = max(b+c, u, v)
                    min_max_out = outgoing if min_max_out is None else min(min_max_out, outgoing)
                    one_out_improving += multiplicity if outgoing <= 1 else 0
                if key[0] < original[0]:
                    min_cmax = distance if min_cmax is None else min(min_cmax, distance)
                weighted_count += multiplicity
                types += 1
    assert weighted_count == 1 << (4*k+2)
    return dict(assignments=weighted_count,
                initial=['2']*3, opt=str(F(opt, scale)),
                optimum_count=optimum_count,
                min_lex_distance=min_lex, min_makespan_distance=min_cmax,
                min_max_out=min_max_out, one_out_improving=one_out_improving,
                compressed_types=types)


def ring_oracle(q):
    jobs = [(i, (i+1) % q, F(1), F(1,2)) for i in range(q) for _ in range(2)]
    result = fraction_oracle(q, jobs)
    assert result['opt'] == '1'
    assert result['min_lex_distance'] == q
    return result


def main():
    results = []
    for k in range(1, 6):
        fast = gray_integer_oracle(k)
        assert fast['opt'] == '1'
        assert fast['optimum_count'] == 1
        assert fast['min_lex_distance'] == k+1
        assert fast['min_makespan_distance'] == k+3
        assert fast['min_max_out'] == k
        if k >= 2:
            assert fast['one_out_improving'] == 0
        item = dict(k=k, integer_gray=fast)
        if k <= 3:
            independent = fraction_oracle(*fanout_instance(k))
            assert independent == fast, (independent, fast)
            item['independent_fraction'] = independent
        compressed = compressed_oracle(k)
        assert {a:b for a,b in compressed.items() if a != 'compressed_types'} == fast
        item['compressed'] = compressed
        results.append(item)
    large = []
    for k in (7, 31, 127, 503):
        result = compressed_oracle(k)
        assert result['opt'] == '1'
        assert result['optimum_count'] == 1
        assert result['min_lex_distance'] == k+1
        assert result['min_max_out'] == k
        assert result['min_makespan_distance'] == k+3
        assert result['one_out_improving'] == 0
        large.append(dict(k=k, compressed=result))
    rings = {str(q): ring_oracle(q) for q in range(2, 6)}
    print(json.dumps(dict(python=platform.python_version(),
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        scope='All legal assignments; fanout k=1..5, Fraction cross-check k=1..3; compressed all types k=7,31,127,503; rings q=2..5',
        fanout=results, compressed_large=large, rings=rings), indent=2))


if __name__ == '__main__':
    main()
