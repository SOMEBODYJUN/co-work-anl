#!/usr/bin/env python3
"""Literal exact audits of the parity / bad-cycle selector implant.

Finite reproducible audit; no solver or randomness. Output is stdout or an exclusively created file.
Every resource test uses actual user sets and recomputed loads.
"""
from fractions import Fraction as F
from itertools import product
from hashlib import sha256
from pathlib import Path
import json
import platform
import argparse
import sys


def flipped(s, i):
    t = list(s)
    t[i] ^= 1
    return tuple(t)


def literal_cost(s, i, weights, resources):
    ans = F(0)
    for sig, degree, coefficient in resources:
        if sig[i] != s[i]:
            continue
        load = sum(w for j, w in enumerate(weights) if sig[j] == s[j])
        ans += coefficient * load ** degree
    return ans


def core_column_cost(s, i, weights, signature, degree):
    # Blocks are -1 (omitted), 0, 1. Every binary proper signature is enumerated.
    if signature[i] != s[i]:
        return 0
    load = sum(w for j, w in enumerate(weights) if signature[j] == s[j])
    return load ** degree


def full_column_cost(s, i, weights, signature, degree):
    # Blocks are masks 0, 1, 2, 3; mask3 includes the resource in both actions.
    if not (signature[i] & (1 << s[i])):
        return 0
    load = sum(w for j, w in enumerate(weights)
               if signature[j] & (1 << s[j]))
    return load ** degree


def fixture_a():
    # Two-player quadratic strict cycle 00->10->11->01->00.
    weights = (1, 2)
    resources = [((1, 1), 1, F(13)), ((1, 0), 2, F(3)),
                 ((0, 1), 2, F(3)), ((0, 0), 1, F(13))]
    return "quadratic_four_cycle", 2, F(52, 51), weights, resources


def fixture_b():
    # Four-player cubic pair fixture: weights scaled by8 and coefficients /8^3.
    weights = (8, 4, 2, 1)
    pairs = [((0, 0, 1, 1), F(1593928, 421875)),
             ((0, 1, 1, 0), F(452978, 421875)),
             ((1, -1, -1, -1), F(23816, 5859375)),
             ((1, 1, -1, -1), F(855968, 17578125))]
    resources = []
    for signs, coefficient in pairs:
        # Fixture signs: 0 means absent, +1 uses action0, -1 uses action1.
        sig = tuple(-1 if sign == 0 else int(sign < 0) for sign in signs)
        resources.append((sig, 3, coefficient / 8**3))
        resources.append((tuple(1-v if v >= 0 else -1 for v in sig),
                          3, coefficient / 8**3))
    return "cubic_eight_cycle", 3, F(21, 20), weights, resources


def audit(fixture):
    name, d, alpha, old_weights, old_resources = fixture
    n = len(old_weights)
    ordinary_n = max(n, d+2)
    extra = ordinary_n-n
    # Positive integers deliberately differ from base players' weights.
    weights = old_weights + tuple(3+2*j for j in range(extra)) + (7,)
    flag = ordinary_n
    active = d+2
    N = ordinary_n+1
    resources = [(sig+(-1,)*(extra+1), k, a)
                 for sig, k, a in old_resources]
    q = (0,)*ordinary_n
    base_cycle = []
    x = q
    for step in range(2*n):
        base_cycle.append(x)
        x = flipped(x, step % n)
    assert x == q
    assert len(set(base_cycle)) == 2*n
    recurrence = tuple(x+(1,) for x in base_cycle)
    Q = set(recurrence)
    cycle_next = {s: recurrence[(j+1) % len(recurrence)]
                  for j, s in enumerate(recurrence)}
    states = tuple(product((0, 1), repeat=N))
    H = {}
    movers = {}
    for s in states:
        if s[flag] == 0:
            i = 0 if sum(s[:active]) % 2 == 0 else flag
        elif s in Q:
            t = cycle_next[s]
            differences = [i for i in range(N) if s[i] != t[i]]
            assert len(differences) == 1
            i = differences[0]
        else:
            i = next(i for i in range(ordinary_n) if s[i] != q[i])
        movers[s] = i
        H[s] = flipped(s, i)
    # Every state routes to precisely Q and is never a self-loop.
    largest_transient_time = 0
    for s in states:
        t = s
        seen = set()
        steps = 0
        while t not in Q:
            assert t not in seen
            seen.add(t)
            t = H[t]
            steps += 1
        largest_transient_time = max(largest_transient_time, steps)
        assert steps <= ordinary_n+2
    for j, s in enumerate(recurrence):
        assert H[s] == recurrence[(j+1) % len(recurrence)]
    assert all(H[s] != s for s in states)

    support = tuple(s for s in states if s[flag] == 0
                    and s[active:ordinary_n] == q[active:ordinary_n]
                    and sum(s[:active]) % 2 == 0)
    assert len(support) == 2**(d+1)
    assert all(s not in Q and movers[s] == 0 for s in support)
    arrival_support = {H[s] for s in support}
    assert len(arrival_support) == len(support)
    assert all(sum(s[:active]) % 2 == 1 and s[flag] == 0
               for s in arrival_support)

    core_checked = full_checked = 0
    max_arrival = 0
    for signature in product((-1, 0, 1), repeat=N):
        if all(v == -1 for v in signature):
            continue
        for k in range(d+1):
            old_sum = sum(core_column_cost(s, 0, weights, signature, k)
                          for s in support)
            new_sum = sum(core_column_cost(H[s], 0, weights, signature, k)
                          for s in support)
            assert old_sum == new_sum
            assert old_sum-alpha*new_sum <= 0
            max_arrival = max(max_arrival, new_sum)
            core_checked += 1
    # Stronger audit includes arbitrary mandatory blocks; claim only needs core.
    for signature in product(range(4), repeat=N):
        if not any(signature):
            continue
        for k in range(d+1):
            old_sum = sum(full_column_cost(s, 0, weights, signature, k)
                          for s in support)
            new_sum = sum(full_column_cost(H[s], 0, weights, signature, k)
                          for s in support)
            assert old_sum == new_sum
            assert old_sum-alpha*new_sum <= 0
            full_checked += 1

    margins = {s: literal_cost(s, movers[s], weights, resources)
               -alpha*literal_cost(H[s], movers[s], weights, resources)
               for s in states}
    eta = min(margins[s] for s in recurrence)
    assert eta > 0
    M = max([F(0)]+[-margins[s] for s in states if s not in Q])
    assert sum(margins[s] for s in support) <= 0
    bound = eta/(eta+M)
    assert 0 < bound <= 1
    for s in states:
        singleton = [-1]*N
        singleton[movers[s]] = s[movers[s]]
        assert core_column_cost(s, movers[s], weights, singleton, 0) == 1
        assert core_column_cost(H[s], movers[s], weights, singleton, 0) == 0

    return {"fixture": name, "degree": d, "alpha": str(alpha),
            "weights": list(weights), "original_players": n,
            "parity_players": active, "added_ordinary_players": extra,
            "total_players_including_flag": N, "all_states": len(states),
            "unique_recurrent_cycle_length": len(recurrence),
            "fully_transient_dual_support": len(support),
            "core_columns_checked": core_checked,
            "full_columns_checked": full_checked,
            "maximum_first_hit_time": largest_transient_time,
            "all_recurrent_real_margins": [str(margins[s]) for s in recurrence],
            "eta": str(eta), "M": str(M),
            "every_dual_transient_mass_at_least": str(bound),
            "all_point_masses_rejected_by_literal_singleton_constant": True}


if __name__ == "__main__":
    report = {"scope": "Finite exact replay of parity/bad-cycle full-cone implant; no general existence inference",
              "python": platform.python_version(),
              "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
              "arithmetic": "Python arbitrary integers and fractions.Fraction; no floating tolerance or randomness",
              "fixtures": [audit(fixture_a()), audit(fixture_b())]}
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    report.update(command=' '.join(sys.argv),seed=None)
    output=json.dumps(report,ensure_ascii=False,indent=2)+'\n'
    if args.output:
        with args.output.open('x') as stream:stream.write(output)
        print(json.dumps({'output':str(args.output),'status':'PASS'}))
    else:print(output,end='')
