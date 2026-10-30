#!/usr/bin/env python3
"""Independent exact audit; only standard-library arithmetic and set membership."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import json
import random


def coeff_a(h, acount, bcount, ina, inb):
    return F(ina, h + acount * ina + bcount * inb) if ina else F(0)


def error_coeff(h, r, ina, inb):
    hits = ina + inb
    if hits == 0:
        return F(0)
    if hits == 1:
        return F((r - 1) * h, (h + r) * (h + 1))
    return F((2 * r - 2) * h + r - 2, (h + r + 1) * (h + 1))


def audit_coefficients():
    checked = 0
    for h, r, ina, inb in product(range(61), range(1, 20), range(2), range(2)):
        fa, fb = F(ina, h + 1), F(inb, h + 1)
        lab = coeff_a(h, 1, r, ina, inb)
        lba = coeff_a(h, 1, r, inb, ina)
        kab, kba = fb + lab, fa + lba
        assert kab == kba
        assert kab == fa + fb - F(r * ina * inb, (h + 1) * (h + r + 1))
        if r >= 2:
            # Consume one pivot b into H and lower its active clone count.
            hnew = h + inb
            knew = F(inb, hnew + 1) + coeff_a(hnew, 1, r - 1, ina, inb)
            assert kab - knew == F(inb, (h + 1) * (h + 2))
        if r >= 2:
            pab = r * (coeff_a(h, r, 1, ina, inb)
                       + coeff_a(h, r, 1, inb, ina))
            assert pab == kab + error_coeff(h, r, ina, inb)
            assert error_coeff(h, r, ina, inb) >= 0
        if r == 2:
            ec = error_coeff(h, r, ina, inb)
            assert ec == h * (F(1, h + 1) - F(1, h + 1 + ina + inb))
            assert ec <= F(4, 15)
            if ina + inb == 1:
                assert ec <= F(1, 6)
            for z in range(4):
                incumbent = F(h, h + z) if h else F(0)
                assert ec <= incumbent
        checked += 1
    assert error_coeff(2, 2, 1, 1) == F(4, 15)
    assert error_coeff(1, 2, 1, 0) == F(1, 6)
    return checked


def audit_instance(topics, prefix, r, rng):
    clients = sorted(set().union(*topics))
    h = {x: sum(x in topics[a] for a in prefix) for x in clients}
    n = len(topics)

    def f(a):
        return sum((F(1, h[x] + 1) for x in topics[a]), F(0))

    def payoff(a, na, b, nb):
        return sum((F(1, h[x] + na + nb * (x in topics[b]))
                    for x in topics[a]), F(0))

    def k(a, b):
        return f(b) + payoff(a, 1, b, r)

    def p(a, b):
        return r * (payoff(a, r, b, 1) + payoff(b, r, a, 1))

    def e(a, b):
        return sum((error_coeff(h[x], r, x in topics[a], x in topics[b])
                    for x in clients), F(0))

    replies = []
    for b in range(n):
        values = [payoff(a, 1, b, r) for a in range(n)]
        best = max(values)
        replies.append(rng.choice([a for a in range(n) if values[a] == best]))

    chain_count = 0
    cycle_count = 0
    for a0, b0 in product(range(n), repeat=2):
        assert k(a0, b0) == k(b0, a0)
        if r >= 2:
            assert p(a0, b0) == k(a0, b0) + e(a0, b0)
            assert p(a0, b0) == p(b0, a0)
        a, b = a0, b0
        gap_sum = F(0)
        for _ in range(3 * n + 2):
            c = replies[b]
            true_gap = payoff(c, 1, b, r) - payoff(a, 1, b, r)
            assert true_gap >= 0
            assert true_gap == k(b, c) - k(a, b)
            gap_sum += true_gap
            a, b = b, c
            if r >= 2:
                assert p(a, b) - p(a0, b0) == gap_sum + e(a, b) - e(a0, b0)
                assert p(a0, b0) <= p(a, b) + e(a0, b0) - e(a, b)
                if r == 2:
                    n1 = sum(h[x] > 0 and ((x in topics[a0]) + (x in topics[b0]) == 1)
                             for x in clients)
                    n2 = sum(h[x] > 0 and x in topics[a0] and x in topics[b0]
                             for x in clients)
                    assert p(a0, b0) <= p(a, b) + F(n1, 6) + F(4 * n2, 15)
            chain_count += 1

    for start in range(n):
        walk, seen = [], {}
        b = start
        while b not in seen:
            seen[b] = len(walk)
            walk.append(b)
            b = replies[b]
        cycle = walk[seen[b]:]
        edges = [k(cycle[i], cycle[(i + 1) % len(cycle)]) for i in range(len(cycle))]
        assert all(val == edges[0] for val in edges)
        for i, pivot in enumerate(cycle):
            prev, nxt = cycle[i - 1], cycle[(i + 1) % len(cycle)]
            assert payoff(prev, 1, pivot, r) == payoff(nxt, 1, pivot, r)
        cycle_count += 1
    return chain_count, cycle_count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    checks = audit_coefficients()
    rng = random.Random(20261021)
    chains, cycles, instances = 0, 0, 0
    for nclients, nlabels, prelen, r in product(range(1, 7), range(1, 8), range(5), range(1, 6)):
        topics = [frozenset(x for x in range(nclients) if rng.randrange(2))
                  for _ in range(nlabels)]
        prefix = tuple(rng.randrange(nlabels) for _ in range(prelen))
        nc, ny = audit_instance(topics, prefix, r, rng)
        chains += nc
        cycles += ny
        instances += 1
    stairs = 0
    for _ in range(240):
        n = rng.randrange(1, 8)
        nclients = rng.randrange(1, 9)
        topics = [frozenset(x for x in range(nclients) if rng.randrange(2))
                  for _ in range(n)]
        prefix = tuple(rng.randrange(n) for _ in range(rng.randrange(4)))
        h = [sum(x in topics[a] for a in prefix) for x in range(nclients)]
        h0 = h.copy()
        r = rng.randrange(2, 10)
        a, b = rng.randrange(n), rng.randrange(n)
        reply_cache = {}

        def kernel(a, b, hh, rr):
            return sum((F(x in topics[b], hh[x] + 1)
                        + (F(1, hh[x] + 1 + rr * (x in topics[b]))
                           if x in topics[a] else F(0))
                        for x in range(nclients)), F(0))

        initial = kernel(a, b, h, r)
        gap = F(0)
        delta = F(0)
        while r >= 2:
            choices = [kernel(c, b, h, r) for c in range(n)]
            best = max(choices)
            history = prefix + (b,) * r
            if history not in reply_cache:
                reply_cache[history] = rng.choice([c for c in range(n) if choices[c] == best])
            c = reply_cache[history]
            assert choices[c] == best
            gap += best - kernel(a, b, h, r)
            assert kernel(c, b, h, r) == kernel(b, c, h, r)
            delta += sum((F(1, (h[x] + 1) * (h[x] + 2))
                          for x in topics[c]), F(0))
            h = [h[x] + (x in topics[c]) for x in range(nclients)]
            prefix += (c,)
            a, b = b, c
            r -= 1
            stairs += 1
        rent = sum((F(1, h0[x] + 1) - F(1, h[x] + 1)
                    for x in range(nclients)), F(0))
        assert delta == rent
        assert kernel(a, b, h, r) - initial == gap - rent
        assert initial <= kernel(a, b, h, r) + rent

    report = {"status": "passed", "identity_membership_checks": checks,
              "random_fixed_prefix_instances": instances,
              "exact_reply_chain_steps": chains, "exact_reply_cycle_checks": cycles,
              "r2_single_hit_max": "1/6", "r2_double_hit_max": "4/15",
              "r2_error_paid_by_any_actual_prefix_cohort_profit": True,
              "exact_reply_staircase_steps": stairs,
              "scope": "Reciprocal chains and one-prefix-pivot staircases only; no general half proof."}
    if args.output:
        if args.output.exists():
            raise FileExistsError(args.output)
        args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
