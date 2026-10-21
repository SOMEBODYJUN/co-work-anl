#!/usr/bin/env python3
"""Finite independent resource-incidence audits, not an infinite-family proof.

Uses actual prescribed resource sides. Fractions make endpoint comparisons
exact. The near-unit tail itself is proved in proof.md, Sections 2 and 7.
"""

from fractions import Fraction as F
from itertools import product
from math import comb
import argparse
import hashlib
import json
from pathlib import Path
import platform


def bits(phase, size):
    phase %= 2 * size
    if phase < size:
        return [int(j < phase) for j in range(size)]
    return [int(j >= phase - size) for j in range(size)]


def sigma(anchor_j, user_j, orientation):
    # The heavy class precedes the light class within each index.
    return int(2 * user_j + 1 > 2 * anchor_j) ^ int(orientation == -1)


def pair_sides(size, width, orientation, heavy_bits, light_bits, anchor_j):
    participants = [("h", anchor_j, heavy_bits[anchor_j])]
    for offset in range(width):
        j = (anchor_j + offset) % size
        participants.append(("l", j, light_bits[j] ^ sigma(anchor_j, j, orientation)))
    return participants


def cost(size, width, orientation, hb, lb, mover_class, mover_j, q, degree):
    result = F(0)
    for anchor_j in range(size):
        participants = pair_sides(size, width, orientation, hb, lb, anchor_j)
        matches = [side for cls, j, side in participants if (cls, j) == (mover_class, mover_j)]
        if not matches:
            continue
        assert len(matches) == 1
        side = matches[0]
        load = sum((F(1) if cls == "h" else q)
                   for cls, j, member_side in participants if member_side == side)
        result += load ** degree
    return result


def endpoint_costs(size, width, orientation, hp, lp, mover_class, direction, q, degree):
    hb, lb = bits(hp, size), bits(lp, size)
    phase = hp if mover_class == "h" else lp
    mover_j = (phase if direction == 1 else phase - 1) % size
    old = cost(size, width, orientation, hb, lb, mover_class, mover_j, q, degree)
    next_hb, next_lb = hb[:], lb[:]
    (next_hb if mover_class == "h" else next_lb)[mover_j] ^= 1
    new = cost(size, width, orientation, next_hb, next_lb, mover_class, mover_j, q, degree)
    return old, new


def audit_heavy_and_light():
    count = 0
    for size in range(3, 9):
        for width in range(1, size):
            q, degree = F(1, 13), 3
            x = sum((1 + r * q) ** degree for r in range(1, width + 1))
            for relative in range(2 * size):
                h = width - min(relative, width) if relative <= size else min(relative - size, width)
                expected = ((1 + h * q) ** degree, (1 + (width - h) * q) ** degree)
                actual = endpoint_costs(size, width, -1, 0, relative, "h", 1, q, degree)
                assert actual == expected, ("heavy forward", size, width, relative, actual, expected)
                rp = (relative + 1) % (2 * size)
                hnext = width - min(rp, width) if rp <= size else min(rp - size, width)
                expected_backward = ((1 + (width - hnext) * q) ** degree, (1 + hnext * q) ** degree)
                actual_backward = endpoint_costs(size, width, -1, 0, relative, "h", -1, q, degree)
                assert actual_backward == expected_backward, ("heavy backward r+1", size, width, relative)

                hb, lb = bits(relative, size), bits(0, size)
                old_formula = new_formula = F(0)
                for k in range(width):
                    anchor = (-k) % size
                    mover_side = lb[0] ^ sigma(anchor, 0, -1)
                    e = int(hb[anchor] == mover_side)
                    old_formula += ((width - k) * q + e) ** degree
                    new_formula += ((k + 1) * q + 1 - e) ** degree
                actual_light = endpoint_costs(size, width, -1, relative, 0, "l", 1, q, degree)
                assert actual_light == (old_formula, new_formula), ("light formula", size, width, relative)
                for direction in (-1, 1):
                    old, new = endpoint_costs(size, width, -1, relative, 0, "l", direction, q, degree)
                    assert max(old, new) <= x, ("light area bound", size, width, relative, direction)
                count += 1
    return count


def return_e(size, relative):
    hb = bits(relative, size)
    return [int(hb[(-k) % size] == int(k == 0)) for k in range(size)]


def audit_return():
    count = 0
    for size in range(3, 13):
        q, degree = F(1, 7 * size), 4
        for relative in range(2 * size):
            es = return_e(size, relative)
            old = sum(((size - k) * q + e) ** degree for k, e in enumerate(es))
            new = sum(((k + 1) * q + 1 - e) ** degree for k, e in enumerate(es))
            actual = endpoint_costs(size, size, 1, relative, 0, "l", 1, q, degree)
            assert actual == (old, new), ("return forward", size, relative)
            # Backward from light phase 0 reverses a forward edge with relative r+1.
            next_es = return_e(size, relative + 1)
            next_old = sum(((size - k) * q + e) ** degree for k, e in enumerate(next_es))
            next_new = sum(((k + 1) * q + 1 - e) ** degree for k, e in enumerate(next_es))
            actual_back = endpoint_costs(size, size, 1, relative, 0, "l", -1, q, degree)
            assert actual_back == (next_new, next_old), ("return backward r+1", size, relative)
            count += 1
        for t in range(size):
            even_es = return_e(size, -t)
            assert [k for k, e in enumerate(even_es) if not e] == list(range(t + 1))
            odd_es = return_e(size, size - t + 1)
            assert sum(odd_es) == (0 if t == 0 else t), ("parity defects", size, t)
            count += 1
    return count


def audit_twist():
    count = 0
    for size in range(3, 10):
        for orientation in (-1, 1):
            for anchor in range(size):
                for user in range(size):
                    ew_h, ew_l = int(anchor == size - 1), int(user == size - 1)
                    new_anchor, new_user = (anchor + 1) % size, (user + 1) % size
                    assert sigma(new_anchor, new_user, orientation) == (sigma(anchor, user, orientation) ^ ew_h ^ ew_l)
                    for lbit in (0, 1):
                        # Every pair side undergoes the same swap, by the anchor's wrap bit.
                        assert (lbit ^ ew_l ^ sigma(new_anchor, new_user, orientation)) == (lbit ^ sigma(anchor, user, orientation) ^ ew_h)
                    count += 1
        for phase in range(2 * size):
            old = bits(phase, size)
            translated = [0] * size
            for j in range(size):
                translated[(j + 1) % size] = old[j] ^ int(j == size - 1)
            assert translated == bits(phase + 1, size)
    return count


def triggered(bitstring, i, j):
    a, b, c = bitstring[0], bitstring[i] ^ 1, bitstring[j]
    return a == b == c


def audit_clock():
    count = 0
    for size in range(3, 11):
        triples = [(i, j) for i in range(1, size) for j in range(i + 1, size)]
        max_count = comb(size - 1, 2)
        for bitstring in product((0, 1), repeat=size):
            is_front = sum(bitstring[j] != bitstring[j - 1] for j in range(1, size)) <= 1
            assert is_front == (not any(triggered(bitstring, i, j) for i, j in triples))
            for mover in range(size):
                assert sum(mover in (0, i, j) for i, j in triples) <= max_count
            if not is_front:
                mover = next(j for j in range(1, size) if bitstring[j] != bitstring[0])
                assert any(triggered(bitstring, i, j) and mover in (0, i, j) for i, j in triples)
                repaired = list(bitstring)
                repaired[mover] = bitstring[0]
                assert not any(triggered(repaired, i, j) and mover in (0, i, j) for i, j in triples)
            count += 1
    return count


def ceildiv(a, b):
    return (a + b - 1) // b


def audit_tail_rounding():
    degrees = set()
    for exponent in range(20, 101):
        degrees.update((2 ** exponent - 1, 2 ** exponent, 2 ** exponent + 1))
    degrees.update((2 ** 1000, 2 ** 1000 + 1, 10 ** 1000))
    count = 0
    for d in sorted(x for x in degrees if x >= 2 ** 20):
        logceil = (d - 1).bit_length()
        n = ceildiv(d, 1200 * logceil ** 2)
        assert d > 1200 * logceil ** 2
        assert n >= 2 and d >= 8 * n
        assert n * 600 * logceil ** 2 <= d
        assert F(d, 9 * n) >= F(200, 3) * logceil ** 2 > 4 + 2 * logceil
        assert 200 * n * logceil ** 2 <= F(d, 3)
        assert F(d, n) <= 1200 * logceil ** 2
        count += 1
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    checks = [audit_heavy_and_light, audit_return, audit_twist, audit_clock, audit_tail_rounding]
    results = {}
    for check in checks:
        results[check.__name__] = check()
    record = {'status':'PASS', 'checks':results, 'total_exact_cases':sum(results.values()),
              'arithmetic':'Fraction and integer', 'seed':None,
              'python_version':platform.python_version(),
              'scope':'finite endpoint, parity, twist, repair and rounding audits only; universal tail has a separate analytic proof',
              'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    output = json.dumps(record, indent=2)+'\n'
    if args.output:
        with args.output.open('x') as f:
            f.write(output)
    print(output, end='')


if __name__ == "__main__":
    main()
