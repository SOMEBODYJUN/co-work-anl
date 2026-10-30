#!/usr/bin/env python3
"""Exact finite checks for the Mobius compiler, not half-conjecture proof.

The candidate theorem's signed game is auxiliary. Only x_B+K is sent to Instance,
where integer multiplicities represent distinct unit customers in a shared catalog.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from functools import lru_cache
from itertools import combinations_with_replacement, product
import json
from pathlib import Path
import random
import sys
import hashlib
import platform
import subprocess

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from customer_attraction import CustomerType, ExactSPESolver, Instance


def compile_subset(values):
    if not values or len(values) & (len(values) - 1) or values[0] != 0:
        raise ValueError("Require a power-of-two table with F(empty)=0")
    p = len(values).bit_length() - 1
    if p < 1:
        raise ValueError("Require at least one topic")
    coefficients = list(map(Fraction, values))
    for a in range(p):
        for mask in range(1 << p):
            if mask >> a & 1:
                coefficients[mask] -= coefficients[mask ^ (1 << a)]
    x = [Fraction(0)] + [(-1) ** (b.bit_count() + 1) * b.bit_count()
                         * coefficients[b] for b in range(1, 1 << p)]
    for a in range(p):
        for mask in range(1 << p):
            if not mask >> a & 1:
                x[mask] -= x[mask | (1 << a)]
    # Empty customer type is irrelevant and never interpreted as a customer.
    x[0] = Fraction(0)
    return tuple(x)


def profiles(p, n):
    for labels in combinations_with_replacement(range(p), n):
        yield tuple(labels.count(a) for a in range(p))


def potential(x, q):
    harmonic = [Fraction(0)]
    for k in range(1, sum(q) + 1):
        harmonic.append(harmonic[-1] + Fraction(1, k))
    return sum((x[b] * harmonic[sum(q[a] for a in range(len(q)) if b >> a & 1)]
                for b in range(1, len(x))), Fraction(0))


def payoff(x, q, a):
    assert q[a] > 0
    return sum((x[b] / sum(q[t] for t in range(len(q)) if b >> t & 1)
                for b in range(1, len(x)) if b >> a & 1), Fraction(0))


def increment(q, a):
    return tuple(v + int(i == a) for i, v in enumerate(q))


def restricted_outcomes(x, p, n):
    """Independent recursion on ordered histories: skip every previously used label.

    It also starts at arbitrary repeated histories for the full-history boundary.
    No count-state caching and no imports from the canonical recursion core.
    """
    @lru_cache(None)
    def visit(history):
        q = tuple(history.count(a) for a in range(p))
        if len(history) == n:
            return frozenset((q,))
        actions = tuple(a for a in range(p) if not q[a])
        children = {a: visit(history + (a,)) for a in actions}
        floor = max(min(payoff(x, terminal, a) for terminal in children[a])
                    for a in actions)
        return frozenset(terminal for a in actions for terminal in children[a]
                         if payoff(x, terminal, a) >= floor)
    return visit


def verify_policy(x, p, n, policy, restricted=False):
    def visit(history):
        if len(history) == n:
            return tuple(history.count(a) for a in range(p))
        actions = tuple(a for a in range(p) if not restricted or a not in history)
        chosen = policy[history]
        assert chosen in actions
        children = {a: visit(history + (a,)) for a in actions}
        own = payoff(x, children[chosen], chosen)
        assert all(own >= payoff(x, children[a], a) for a in actions)
        return children[chosen]
    return visit(())


def make_instance(x, p, n, offset):
    weights = tuple(int(v) + offset for v in x[1:])
    assert all(Fraction(v).denominator == 1 for v in x)
    assert min(weights) >= 1
    return Instance(tuple(f"T{a}" for a in range(p)),
                    tuple(CustomerType(frozenset(a for a in range(p) if b >> a & 1),
                                       weights[b - 1]) for b in range(1, 1 << p)), n)


def main(output=None):
    rng = random.Random(6137)
    report = {"status": "exact finite audit of reviewed compiler; not a universal efficiency proof",
              "python_version": platform.python_version(),
              "base_commit": subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "replay_commands": ['python3 tests/audits/mobius_compiler_audit.py'],
              "seed": 6137, "subset_cases": 0, "potential_marginals": 0,
              "bias_squarefree_payoffs": 0, "embedding_cases": [],
              "all_ordered_policy_checks": []}
    for p in range(1, 7):
        for trial in range(4):
            table = [0] + [rng.randrange(-7, 8) for _ in range((1 << p) - 1)]
            x = compile_subset(table)
            for b in range(1 << p):
                q = tuple(int(b >> a & 1) for a in range(p))
                assert potential(x, q) == table[b]
            report["subset_cases"] += 1
            for n in range(1, min(p + 1, 5) + 1):
                for q in profiles(p, n):
                    for a in range(p):
                        if q[a]:
                            previous = tuple(v - int(t == a) for t, v in enumerate(q))
                            assert payoff(x, q, a) == potential(x, q) - potential(x, previous)
                            report["potential_marginals"] += 1
            bias = (Fraction(0),) + (Fraction(1),) * ((1 << p) - 1)
            for n in range(1, p + 1):
                constant = Fraction((1 << p) - (1 << (p - n)), n)
                for q in profiles(p, n):
                    if max(q) <= 1:
                        for a in range(p):
                            if q[a]:
                                assert payoff(bias, q, a) == constant
                                report["bias_squarefree_payoffs"] += 1

    # Exact repeat/fresh reversal with strictly positive unit-customer counts.
    x = tuple(map(Fraction, (0, -4, -3, 0)))
    r = tuple(map(Fraction, (0, 1, 2, 5)))
    assert payoff(x, (2, 0), 0) == -2 > payoff(x, (1, 1), 1) == -3
    assert payoff(r, (2, 0), 0) == 3 < payoff(r, (1, 1), 1) == Fraction(9, 2)
    report["repeat_reversal"] = {"signed": [-4, -3, 0], "offset": 5,
                                 "legal_counts": [1, 2, 5],
                                 "signed_repeat_fresh": ["-2", "-3"],
                                 "legal_repeat_fresh": ["3", "9/2"]}

    # Exact full ordered-policy enumeration; projected SPE sets, not only outcomes.
    for p, n in ((1, 1), (2, 2), (3, 2), (4, 2)):
        table = [0] + [rng.randrange(-3, 4) for _ in range((1 << p) - 1)]
        x = compile_subset(table)
        offset = int(4 * sum(map(abs, x)) + 1)
        r = (Fraction(0),) + tuple(v + offset for v in x[1:])
        histories = tuple(h for d in range(n) for h in product(range(p), repeat=d))
        legal_histories = tuple(h for h in histories if len(set(h)) == len(h))
        full_projections = set()
        for choices in product(range(p), repeat=len(histories)):
            policy = dict(zip(histories, choices))
            try:
                verify_policy(r, p, n, policy)
            except AssertionError:
                continue
            assert all(policy[h] not in h for h in histories)
            full_projections.add(tuple(policy[h] for h in legal_histories))
        restricted_policies = set()
        menus = tuple(tuple(a for a in range(p) if a not in h) for h in legal_histories)
        for choices in product(*menus):
            policy = dict(zip(legal_histories, choices))
            try:
                verify_policy(x, p, n, policy, restricted=True)
            except AssertionError:
                continue
            restricted_policies.add(choices)
        assert full_projections == restricted_policies
        report["all_ordered_policy_checks"].append({"p": p, "n": n,
            "full_policies": p ** len(histories),
            "restricted_policies": len(restricted_policies),
            "spe_projection_sets_equal": True})

    # Larger exact outcome checks at EVERY ordered prefix, including repeated ones.
    for p, n in ((3, 3), (4, 3), (5, 4), (5, 5), (6, 5)):
        table = [0] + [rng.randrange(-4, 5) for _ in range((1 << p) - 1)]
        x = compile_subset(table)
        magnitude = int(sum(map(abs, x)))
        offset = 4 * magnitude + 1
        instance = make_instance(x, p, n, offset)
        full = ExactSPESolver(instance)
        restricted = restricted_outcomes(x, p, n)
        prefix_checks = 0
        repeated_prefix_checks = 0
        for d in range(n):
            for h in product(range(p), repeat=d):
                q = tuple(h.count(a) for a in range(p))
                actual = full.outcomes(q)
                expected = restricted(h)
                assert actual == expected
                assert all(all(terminal[a] == q[a] if q[a] else terminal[a] <= 1
                               for a in range(p)) for terminal in actual)
                prefix_checks += 1
                repeated_prefix_checks += int(len(set(h)) < len(h))
        baseline = (1 << p) - (1 << (p - n))
        optimum = instance.optimal_welfare()
        minimum = min(instance.welfare(q) for q in full.outcomes())
        assert minimum >= offset * baseline - magnitude
        assert optimum <= offset * baseline + magnitude
        assert 2 * minimum - optimum >= offset * baseline - 3 * magnitude > 0
        report["embedding_cases"].append({"p": p, "n": n, "M": magnitude,
            "offset": offset, "ordered_prefix_checks": prefix_checks,
            "repeated_prefix_checks": repeated_prefix_checks,
            "root_outcomes": len(full.outcomes()), "welfare": minimum,
            "optimum": optimum, "twice_welfare_minus_optimum": 2 * minimum - optimum})

    # A monotone submodular Boolean table need not have nonnegative inverse.
    assert compile_subset([0, 1, 1, 1]) == tuple(map(Fraction, (0, -1, -1, 2)))
    # Anonymous count compatibility, including the fixed-n terminal obstruction.
    for values in product(range(-2, 3), repeat=3):
        x = (Fraction(0),) + tuple(map(Fraction, values))
        assert 2 * potential(x, (2, 0)) == 3 * potential(x, (1, 0))
        v = [potential(x, (k, 3 - k)) for k in range(4)]
        assert 3 * (v[3] - v[0]) == 11 * (v[2] - v[1])
    for singleton, shared in product(range(-2, 3), repeat=2):
        x = tuple(map(Fraction, (0, singleton, singleton, shared)))
        a, b, c = (potential(x, q) for q in ((4, 0), (3, 1), (2, 2)))
        assert 11 * (b - a) == 9 * (c - a)
    report["obstructions"] = {"monotone_submodular_inverse": [-1, -1, 2],
        "axis_relation": "2Phi(2e_a)=3Phi(e_a)",
        "terminal_relation": "3(Phi(3,0)-Phi(0,3))=11(Phi(2,1)-Phi(1,2))",
        "signed_terminal_checks": 125}
    for bad in ([], [0], [1, 0], [0, 1, 2]):
        try:
            compile_subset(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid table accepted")
    assert compile_subset([0, Fraction(1, 2)]) == (Fraction(0), Fraction(1, 2))
    rational = [0, Fraction(1, 2), Fraction(1, 3), Fraction(2, 5)]
    assert compile_subset([30 * v for v in rational]) == tuple(
        30 * v for v in compile_subset(rational))
    if output:
        output = Path(output)
        if output.exists():
            raise FileExistsError("refuse to overwrite frozen output")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args()
    main(args.output)
