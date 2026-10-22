#!/usr/bin/env python3
"""Literal-resource Fraction audit for sparse ascending anchored gates.

This is finite transcription/logic evidence, not an infinite proof. All player
costs below are evaluated from resource incidences and actual total load.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path


@dataclass(frozen=True)
class Resource:
    # masks[i] has bit a set precisely when player i's action a uses this resource.
    masks: tuple[int, ...]
    coefficients: tuple[F, ...]

    def latency(self, load: F) -> F:
        return sum((a * load**k for k, a in enumerate(self.coefficients)), F(0))


def costs(resources: list[Resource], weights: tuple[F, ...], s: tuple[int, ...]):
    out = [F(0)] * len(weights)
    for resource in resources:
        users = [i for i, mask in enumerate(resource.masks) if mask & (1 << s[i])]
        latency = resource.latency(sum((weights[i] for i in users), F(0)))
        for i in users:
            out[i] += latency
    return tuple(out)


def social(c, weights):
    return sum((w * x for w, x in zip(weights, c)), F(0))


def flip(s, i):
    return s[:i] + (1 - s[i],) + s[i+1:]


def front(s, n):
    return sum(s[i] != s[i+1] for i in range(n-1)) <= 1


def triggered(s, j):
    return s[0] == s[j+1] != s[j]


def serialize(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): serialize(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [serialize(v) for v in value]
    return value


def gate_resources(n, w, peaks, degree):
    result = []
    for j, peak in enumerate(peaks, 1):
        for side in (0, 1):
            masks = [0] * (n+1)
            for i, xor in ((0, 0), (j, 1), (j+1, 0)):
                masks[i] = 1 << (side ^ xor)
            coeff = [F(0)] * degree + [peak / (3*w)**degree]
            result.append(Resource(tuple(masks), tuple(coeff)))
    return result


def base_resources(n, w, p):
    # Includes one mandatory unequal-weight background user of A. All varying
    # class players have two actions. Additional resource choices are asymmetric.
    a_masks = (1,) * n + (3,)
    b_masks = (2,) * n + (0,)
    c_masks = tuple(1 << (i % 2) for i in range(n)) + (0,)
    total = n*w + F(5, 2)
    return [
        Resource(a_masks, tuple([F(0)] * p + [F(1) / total**p])),
        Resource(b_masks, (F(7, 5),)),
        Resource(c_masks, (F(0), F(1, 10*n))),
    ]


def coarse_bound(resources, weights, n):
    candidate = []
    for i in range(n):
        candidate.append(sum((r.latency(sum(
            (weights[k] for k, mask in enumerate(r.masks) if mask), F(0)))
            for r in resources if r.masks[i]), F(0)))
    return max(candidate)


def run_case(n, alpha, p, epsilon, *, degree_override=None):
    w = F(7, 5)
    weights = (w,) * n + (F(5, 2),)
    base = base_resources(n, w, p)
    B = coarse_bound(base, weights, n)
    rho, sigma = F(1, 7), F(1, 11)
    A = 2*alpha
    Q = 4*((alpha+p+1)*B + rho + sigma)
    peaks = tuple(Q*A**j for j in range(n-2))
    S = sum((A**j for j in range(n-2)), F(0))
    D = 1
    while F(1, 3)**D > 1/(4*alpha) or F(2, 3)**D*S > epsilon/Q:
        D += 1
    if degree_override is not None:
        D = degree_override
    delta, zeta = F(2, 3)**D, F(1, 3)**D
    u = tuple(delta*v for v in peaks)
    z = tuple(zeta*v for v in peaks)
    d = tuple(3*v-2*uu-zz for v, uu, zz in zip(peaks, u, z))
    U = (sum(u, F(0)),) + tuple(
        (u[i-2] if i >= 2 else F(0)) + (u[i-1] if i <= n-2 else F(0))
        for i in range(1, n))
    K = w*sum((2*uu+zz for uu, zz in zip(u, z)), F(0))
    repair_slacks = [v-alpha*(zz+(peaks[j-1] if j else F(0))+B)
                     for j, (v, zz) in enumerate(zip(peaks, z))]
    social_slacks = [dd-(d[j-1] if j else F(0))-(p+1)*B
                     for j, dd in enumerate(d)]
    assert min(repair_slacks) >= rho
    assert min(social_slacks) >= sigma
    gates = gate_resources(n, w, peaks, D)
    assert len(gates) == 2*(n-2)
    assert sum(sum(bool(mask & (1 << a)) for a in (0, 1))
               for r in gates for mask in r.masks) == 6*(n-2)
    states = [bits+(0,) for bits in itertools.product((0, 1), repeat=n)]
    base_table = {s: costs(base, weights, s) for s in states}
    gate_table = {s: costs(gates, weights, s) for s in states}
    table = {s: tuple(a+b for a, b in zip(base_table[s], gate_table[s])) for s in states}
    assert max(x for s in states for x in base_table[s][:n]) <= B
    min_escape_increase = None
    min_repair_margin = None
    min_social_drop = None
    repair_edges = 0
    core_edges = 0
    escape_edges = 0
    stable_literal = []
    stable_predicted = []
    for s in states:
        actual_trigger = [j for j in range(1, n-1) if triggered(s, j)]
        assert bool(actual_trigger) == (not front(s, n))
        assert social(gate_table[s], weights) == K+w*sum(
            (d[j-1] for j in actual_trigger), F(0))
        if all(table[s][i] <= alpha*table[flip(s, i)][i] for i in range(n)):
            stable_literal.append(s[:n])
        predicted = front(s, n) and all(
            base_table[s][i]-alpha*base_table[flip(s, i)][i] <= (alpha-1)*U[i]
            for i in range(n) if front(flip(s, i), n))
        if predicted:
            stable_predicted.append(s[:n])
        for i in range(n):
            t = flip(s, i)
            if front(s, n) and front(t, n):
                core_edges += 1
                assert gate_table[s][i] == gate_table[t][i] == U[i]
                assert table[s][i]-alpha*table[t][i] == (
                    base_table[s][i]-alpha*base_table[t][i]-(alpha-1)*U[i])
            if front(s, n) and not front(t, n):
                escape_edges += 1
                increase = table[t][i]-table[s][i]
                assert increase >= rho
                min_escape_increase = increase if min_escape_increase is None else min(increase, min_escape_increase)
        for j in actual_trigger:
            repair_edges += 1
            t = flip(s, j)
            assert sum(x != t[0] for x in t[1:n]) == sum(x != s[0] for x in s[1:n])-1
            changed = set(actual_trigger) ^ {k for k in range(1, n-1) if triggered(t, k)}
            assert changed <= {j-1, j}
            margin = table[s][j]-alpha*table[t][j]
            drop = social(table[s], weights)-social(table[t], weights)
            assert margin >= rho
            assert drop >= w*sigma
            min_repair_margin = margin if min_repair_margin is None else min(margin, min_repair_margin)
            min_social_drop = drop if min_social_drop is None else min(drop, min_social_drop)
        # A deterministic member of the permitted repair schedules, evaluated
        # again from literal costs at every step.
        current = s
        steps = 0
        while not front(current, n):
            j = next(k for k in range(1, n-1) if triggered(current, k))
            nxt = flip(current, j)
            assert table[current][j] > alpha*table[nxt][j]
            assert social(table[current], weights) > social(table[nxt], weights)
            current = nxt
            steps += 1
            assert steps <= n-2
    assert stable_literal == stable_predicted
    optimum = min(social(table[s], weights) for s in states)
    assert all(front(s, n) for s in states if social(table[s], weights) == optimum)
    assert optimum == K+min(social(base_table[s], weights) for s in states if front(s, n))
    if degree_override is None:
        assert sum(u, F(0)) <= epsilon
        assert max(U) <= epsilon
        assert K <= 3*w*epsilon
    return serialize(dict(n=n, alpha=alpha, p=p, w=w, B=B, D=D,
        states=len(states), repair_edges=repair_edges, core_edges=core_edges,
        escape_edges=escape_edges, min_repair_margin=min_repair_margin,
        min_social_drop=min_social_drop, min_escape_cost_increase=min_escape_increase,
        gate_resources=len(gates), max_peak=peaks[-1], front_tax=K,
        actual_sum_u=sum(u, F(0)), requested_epsilon=epsilon,
        stable_states=stable_literal, optimum=optimum,
        coarse_global_escape_condition=(B+sum(u, F(0)) <= alpha*min(peaks))))


def audit_detection():
    tested = 0
    for n in range(3, 9):
        for j in range(1, n-1):
            suffix = (0,)*(j-1)+(1,0)+(1,)*(n-j-2)
            s = (0,)+suffix
            inversions = [(a,b) for a in range(1,n) for b in range(a+1,n)
                          if s[0] == s[b] != s[a]]
            assert inversions == [(j,j+1)]
            tested += 1
    return dict(n_range=[3,8], unique_trigger_witnesses=tested)


def main():
    cases = [run_case(n, alpha, p, F(1, 5))
             for n in range(3, 7)
             for alpha in (F(1), F(3, 2))
             for p in (1, 3)]
    # Deliberately keep D small: R/S still hold while the coarse global peak
    # comparison fails. Literal escapes nevertheless strictly raise cost.
    no_global_escape = run_case(7, F(1), 1, F(1, 5), degree_override=2)
    assert not no_global_escape['coarse_global_escape_condition']
    out = dict(status='all exact assertions passed',
               scope='finite literal-resource audit; not an infinite proof',
               source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               detection=audit_detection(), cases=cases,
               R_without_coarse_global_escape=no_global_escape,
               total_states=sum(c['states'] for c in cases)+no_global_escape['states'])
    path = Path(__file__).with_suffix('.json')
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: out[k] for k in ('status', 'total_states', 'source_sha256')}, indent=2))


if __name__ == '__main__':
    main()
