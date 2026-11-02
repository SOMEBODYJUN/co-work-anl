#!/usr/bin/env python3
"""Exact finite regression for the private fractional-cover prefix-profit note.

The universal claim is proved in the note. Canonical set-valued SPE enumeration
is used only to supply finite paths; full certificates receive the separate
definition-level verifier. No LP solver or floating point is used.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
from itertools import combinations, product
import json
from pathlib import Path
import random
import sys

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))
from customer_attraction import CustomerType, ExactSPESolver, Instance, verify_certificate


def product_bound(m: int, tau: F) -> F:
    if m < 1 or tau < 1:
        raise ValueError("positive player count and tau>=1 required")
    q = F(1)
    for r in range(1, m + 1):
        q *= 1 - F(1, r) / tau
    return 1 - q


def uniform_bound(m: int, tau: F) -> F:
    return sum((1 / (m + (tau - 1) * r) for r in range(1, m + 1)), F())


def arithmetic_checks() -> dict:
    cases = 0
    for m in range(1, 81):
        for tau in [F(1), F(3, 2), F(2), F(29, 10), F(3), F(7, 2), F(4), F(m)]:
            value = product_bound(m, tau)
            p = F()
            for r in range(m, 0, -1):
                p = (1 - 1 / (r * tau)) * p + 1 / (r * tau)
            assert p == value
            assert value >= uniform_bound(m, tau)
            assert product_bound(m + 1, tau) >= value
            assert product_bound(m, tau + F(1, 7)) <= value
            assert product_bound(m, F(1)) == 1
            cases += 1
    bernoulli_cases = 0
    for a in [F(1), F(1, 2), F(1, 3), F(2, 7), F(7, 8)]:
        for r in range(1, 31):
            q = F(1)
            for t in range(31):
                assert q >= F(r) / (r + a * t)
                lhs = (r + t + 1 - a) * (r + a * (t + 1))
                rhs = (r + t + 1) * (r + a * t)
                assert lhs - rhs == a * (1 - a) * (t + 1)
                q *= 1 - a / (r + t + 1)
                bernoulli_cases += 1
    assert product_bound(5, F(7, 2)) == F(8656, 16807) > F(1, 2)
    assert product_bound(5, F(3)) == F(421, 729)
    assert product_bound(7, F(4)) == F(132355, 262144)
    assert uniform_bound(5, F(3)) == F(22003, 45045) < F(1, 2)
    return {"product_recurrence_cases": cases, "bernoulli_comparison_cases": bernoulli_cases,
            "F_5_7_over_2": str(product_bound(5, F(7, 2))),
            "F_5_3": str(product_bound(5, F(3))),
            "F_7_4": str(product_bound(7, F(4))),
            "old_uniform_5_3": str(uniform_bound(5, F(3)))}


def comparison_covers(instance: Instance) -> list[tuple[tuple[int, ...], tuple[F, ...]]]:
    """Supply exact feasible covers, without claiming minimum fractional cost."""
    k = instance.topic_count
    interested = tuple(c.multiplicity if c.topics else 0 for c in instance.customers)
    candidates = [(tuple(0 for _ in instance.customers), tuple(F() for _ in range(k)))]
    if any(interested):
        d = min(len(c.topics) for c in instance.customers if c.topics)
        candidates.append((interested, tuple(F(1, d) for _ in range(k))))
    dense = tuple(c.multiplicity if len(c.topics) >= 2 else 0 for c in instance.customers)
    if any(dense):
        candidates.append((dense, tuple(F(1, 2) for _ in range(k))))
    best_size, best_support = -1, ()
    for size in range(min(k, instance.players) + 1):
        for support in combinations(range(k), size):
            covered = sum(c.multiplicity for c in instance.customers if c.topics.intersection(support))
            if covered > best_size:
                best_size, best_support = covered, support
    optimal = tuple(c.multiplicity if c.topics.intersection(best_support) else 0
                    for c in instance.customers)
    candidates.append((optimal, tuple(F(int(t in best_support)) for t in range(k))))
    for t in range(k):
        selected = tuple(c.multiplicity if t in c.topics else 0 for c in instance.customers)
        candidates.append((selected, tuple(F(int(t == j)) for j in range(k))))
    # A proper subcollection of a repeated customer type is allowed as C.
    partial = tuple(max(1, c.multiplicity // 2) if c.topics else 0 for c in instance.customers)
    if any(partial):
        candidates.append((partial, tuple(F(1) for _ in range(k))))
    return list(dict.fromkeys(candidates))


def check_path(instance: Instance, path: tuple[int, ...], covers: list, stats: dict) -> None:
    m = instance.players
    payoffs = instance.player_payoffs(path)
    welfare = sum(payoffs)
    assert welfare == instance.welfare(instance.counts(path))
    prefix_counts = [0] * instance.topic_count
    past_profit = F()
    for i, action in enumerate(path):
        r = m - i
        loads = [sum(prefix_counts[t] for t in c.topics) for c in instance.customers]
        for selected, z in covers:
            O = sum(selected)
            if not O:
                assert welfare >= 0
                stats["empty_comparisons"] += 1
                continue
            tau = sum(z)
            assert tau >= 1
            for c, count in zip(instance.customers, selected):
                assert 0 <= count <= c.multiplicity
                if count:
                    assert sum(z[t] for t in c.topics) >= 1
            g = tuple(sum((F(count, b + r) for c, count, b in
                           zip(instance.customers, selected, loads) if t in c.topics), F())
                      for t in range(instance.topic_count))
            assert all(payoffs[i] >= v for v in g)
            past_g = sum((g[t] * prefix_counts[t] for t in range(instance.topic_count)), F())
            fractional_g = sum((z[t] * g[t] for t in range(instance.topic_count)), F())
            assert O <= past_g + r * fractional_g
            assert past_g <= past_profit
            assert fractional_g <= tau * payoffs[i]
            assert O <= past_profit + r * tau * payoffs[i]
            assert welfare >= O * product_bound(m, tau)
            assert payoffs[i] >= F(O) / (i + r * tau)
            stats["prefix_comparison_checks"] += 1
            if tau == 1:
                assert welfare >= O
                stats["tau_one_checks"] += 1
        prefix_counts[action] += 1
        past_profit += payoffs[i]
    stats["ordered_spe_paths"] += 1


def check_instance(instance: Instance, stats: dict) -> None:
    solver = ExactSPESolver(instance)
    covers = comparison_covers(instance)
    first_path = None
    for path in solver.ordered_outcomes():
        if first_path is None:
            first_path = path
        check_path(instance, path, covers, stats)
    assert first_path is not None
    certificate = solver.certificate(on_path=first_path)
    verify_certificate(instance, certificate).assert_valid()
    stats["full_strategy_certificates"] += 1
    stats["certificate_nodes"] += len(certificate.actions)
    stats["instances"] += 1
    if not instance.customer_count:
        stats["zero_customer_instances"] += 1
    if any(not any(t in c.topics for c in instance.customers) for t in range(instance.topic_count)):
        stats["instances_with_empty_topics"] += 1


def finite_spe_checks() -> dict:
    stats = {key: 0 for key in ["instances", "ordered_spe_paths", "prefix_comparison_checks",
             "empty_comparisons", "tau_one_checks", "full_strategy_certificates",
             "certificate_nodes", "zero_customer_instances", "instances_with_empty_topics"]}
    # Every 0/1 interest-type multiplicity for up to three labelled topics.
    for k in range(1, 4):
        signatures = [frozenset(t for t in range(k) if mask >> t & 1)
                      for mask in range(1, 1 << k)]
        for present in product([0, 1], repeat=len(signatures)):
            customers = tuple(CustomerType(s) for s, chosen in zip(signatures, present) if chosen)
            for m in range(1, 5):
                check_instance(Instance(tuple(f"T{t}" for t in range(k)), customers, m), stats)
    # Nonuniform integer multiplicities, four topics, and five-player continuations.
    rng = random.Random(621031)
    for case in range(24):
        k = 4
        customers = []
        for mask in range(1, 1 << k):
            multiplicity = rng.randrange(4)
            if multiplicity:
                customers.append(CustomerType(frozenset(t for t in range(k) if mask >> t & 1),
                                              multiplicity))
        if case % 6 == 0:
            customers.append(CustomerType(frozenset(), 2))
        check_instance(Instance(tuple(f"T{t}" for t in range(k)), tuple(customers), 5), stats)
    stats["range"] = "all binary nonempty interest signatures, k=1..3,m=1..4; 24 seeded k=4,m=5 games with multiplicities 0..3 and selected uninterested clients"
    stats["cover_scope"] = "exact supplied covers: uniform minimum incidence, dense half weights, one optimal integral portfolio, each single topic, partial repeated types, and empty C; fractional optimum is not computed"
    return stats


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = {"status": "passed", "identity": "private exact audit; universal proof is in note",
              "arithmetic": arithmetic_checks(), "finite_spe": finite_spe_checks(),
              "limitations": ["finite SPE regressions do not prove the theorem",
                              "no global half-coverage claim", "fractional optimum not computed"]}
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        with args.output.open("x", encoding="utf-8") as f:
            f.write(text)
    print(text, end="")


if __name__ == "__main__":
    main()
