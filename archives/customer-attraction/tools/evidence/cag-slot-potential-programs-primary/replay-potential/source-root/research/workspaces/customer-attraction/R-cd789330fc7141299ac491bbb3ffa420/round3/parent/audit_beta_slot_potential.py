#!/usr/bin/env python3
"""Independent per-client exact regression for the general Beta slot potential.

This checks algebraic general claims, not SPE realizability or Q-CAG-HALF.
The universal proof is in the manuscripts. No model/solver/author import.
"""
from fractions import Fraction as Q
from itertools import combinations
from math import factorial
from pathlib import Path
import argparse
import json


def beta(a, c):
    # Integral p^(a-1) (1-p)^c dp, a positive integer, c nonnegative.
    return Q(factorial(a - 1) * factorial(c), factorial(a + c))


def harmonic(c):
    return sum((Q(1, j) for j in range(1, c + 1)), Q(0))


def phi(a_slots, c_slots):
    if not a_slots:
        return harmonic(len(c_slots))
    if a_slots & c_slots:
        return Q(0)
    return -beta(len(a_slots), len(c_slots))


def subsets(m):
    return [frozenset(i for i in range(m) if mask >> i & 1)
            for mask in range(1 << m)]


def audit(max_m):
    counters = {"profile_client_types": 0, "present_slot_marginals": 0,
                "diminishing_return_checks": 0, "prefix_query_states": 0,
                "prefix_credit_budgets": 0, "owner_minorant_checks": 0,
                "owner_error_identities": 0, "owner_prefix_states": 0,
                "owner_prefix_credit_budgets": 0}
    max_error = Q(0)
    for m in range(1, max_m + 1):
        sets = subsets(m)
        universe = frozenset(range(m))
        for a in sets:
            for c in sets:
                counters["profile_client_types"] += 1
                error = Q(0)
                for i in c:
                    old = c - {i}
                    marginal = phi(a, c) - phi(a, old)
                    payment = Q(1, len(c))
                    assert Q(0) <= marginal <= payment
                    if not a:
                        assert marginal == payment
                    elif old & a:
                        assert marginal == 0
                    elif i in a:
                        assert marginal == beta(len(a), len(old))
                    else:
                        assert marginal == beta(len(a) + 1, len(old))
                    error += payment - marginal
                    counters["present_slot_marginals"] += 1
                assert Q(0) <= error <= int(bool(a and c))
                if not a:
                    assert error == 0
                max_error = max(max_error, error)
                for owner in a:
                    owner_slots = frozenset({owner})
                    assert phi(owner_slots, c) <= phi(a, c)
                    counters["owner_minorant_checks"] += 1
                    sum_owner_error = Q(0)
                    for i in c:
                        marginal = phi(owner_slots, c) - phi(owner_slots, c - {i})
                        payment = Q(1, len(c))
                        if i == owner:
                            assert marginal == payment
                        elif owner in c:
                            assert marginal == 0
                        else:
                            assert marginal == Q(1, len(c) * (len(c) + 1))
                        sum_owner_error += payment - marginal
                    kappa = (Q(1, len(c)) if owner in c else Q(1, len(c) + 1)) if c else Q(0)
                    assert sum_owner_error == int(bool(c)) - kappa
                    counters["owner_error_identities"] += 1
                # Local square inequalities imply submodularity on slot coverage.
                missing = sorted(universe - c)
                for i, j in combinations(missing, 2):
                    gain_small = phi(a, c | {i}) - phi(a, c)
                    gain_large = phi(a, c | {i, j}) - phi(a, c | {j})
                    assert gain_small >= gain_large >= 0
                    counters["diminishing_return_checks"] += 1
            if not a:
                continue
            # Each stage may have a DIFFERENT suffix; retain only the forced
            # optimal prefix, not a fictitious common rollout or SPE.
            sum_worst = Q(0)
            sum_owner_worst = Q(0)
            owner_slots = frozenset({min(a)})
            for ordinal, i in enumerate(sorted(a), 1):
                anchored = frozenset(j for j in a if j < i) | {i}
                future = range(i + 1, m)
                max_credit = Q(0)
                max_owner_credit = Q(0)
                for mask in range(1 << (m - i - 1)):
                    c = anchored | {j for bit, j in enumerate(future)
                                    if mask >> bit & 1}
                    marginal = phi(a, c) - phi(a, c - {i})
                    credit = Q(1, len(c)) - marginal
                    assert credit >= 0
                    if ordinal == 1:
                        assert credit <= 1 - Q(1, len(a))
                        if len(a) == 1:
                            assert credit == 0
                    else:
                        assert credit <= Q(1, ordinal)
                    max_credit = max(max_credit, credit)
                    counters["prefix_query_states"] += 1
                    owner_marginal = phi(owner_slots, c) - phi(owner_slots, c - {i})
                    owner_credit = Q(1, len(c)) - owner_marginal
                    assert owner_credit >= 0
                    if ordinal == 1:
                        assert owner_credit == 0
                    else:
                        assert owner_credit <= Q(1, ordinal)
                    max_owner_credit = max(max_owner_credit, owner_credit)
                    counters["owner_prefix_states"] += 1
                sum_worst += max_credit
                sum_owner_worst += max_owner_credit
            assert sum_worst <= harmonic(len(a) - 1) <= len(a) - 1
            assert sum_owner_worst <= harmonic(len(a)) - 1 <= len(a) - 1
            counters["prefix_credit_budgets"] += 1
            counters["owner_prefix_credit_budgets"] += 1
    return {"status": "PASS", "scope": "general-lemma per-client algebra regression; no SPE or half proof",
            "max_m_regression_only": max_m, **counters,
            "maximum_total_client_error": str(max_error),
            "claims_checked": ["exact formal slot marginal", "0 <= marginal <= unit payoff",
                               "outside-OPT equality", "sum errors <= covered OPT indicator",
                               "monotone submodular slot function",
                               "independent-rollout optimal-prefix query error <= H_(a-1)",
                               "owner minorant and exact same-leaf error = I - kappa",
                               "first-owner-prefix query error <= H_a - 1"]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-m", type=int, default=8)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    assert 1 <= args.max_m <= 12
    result = audit(args.max_m)
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        with args.output.open("x") as handle:
            handle.write(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
