#!/usr/bin/env python3
"""Finite exact regression and the non-SPE, all-m interface obstruction.

This does not prove the universal spectrum lemma by finite sampling.
Run from any directory; output is JSON on stdout only.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from math import lcm
from pathlib import Path
import json
import random
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[5]))

from customer_attraction import (  # noqa: E402
    CustomerType, ExactSPESolver, Instance, big_theme_lower_bound,
    verify_certificate,
)


def maximal_type_sets(instance: Instance) -> list[frozenset[int]]:
    distinct = set(frozenset(t for t, c in enumerate(instance.customers)
                             if a in c.topics)
                   for a in range(instance.topic_count))
    return sorted((b for b in distinct if not any(b < a for a in distinct)),
                  key=lambda x: (len(x), tuple(sorted(x))))


def path_spectrum(instance: Instance, path: tuple[int, ...]) -> list[Fraction]:
    """Recompute the literal proposed spectrum, retaining integer multiplicities."""
    maxima = maximal_type_sets(instance)
    covered = {t for t, c in enumerate(instance.customers)
               if any(a in c.topics for a in path)}
    private_missing = [
        {t for t in b if t not in covered
         and sum(t in a for a in maxima) == 1}
        for b in maxima
    ]
    missing_mass = [sum(instance.customers[t].multiplicity for t in q)
                    for q in private_missing]
    loads = [0] * len(instance.customers)
    result = []
    for i, action in enumerate(path):
        r = instance.players - i
        slots = []
        for b, q, a in zip(maxima, private_missing, missing_mass):
            beta = sum((Fraction(instance.customers[t].multiplicity, loads[t] + r)
                        for t in b - q), Fraction())
            slots.extend(Fraction(a, k) + beta
                         for k in range(1, instance.players + 1))
        slots.sort(reverse=True)
        result.append(slots[r - 1])
        for t, customer in enumerate(instance.customers):
            loads[t] += action in customer.topics
    return result


def regression() -> dict:
    rng = random.Random(20261023)
    instances = [big_theme_lower_bound(m) for m in range(1, 5)]
    instances.append(Instance.from_topic_sets([set(), set(), set()], players=3))
    instances.append(Instance.from_topic_sets(
        [{0, 1, 2}, {0, 1}, {1, 3}, {2, 3}, set()], players=4))
    for m in range(2, 5):
        for _ in range(8):
            topics = [{x for x in range(7) if rng.randrange(2)} for _ in range(4)]
            instances.append(Instance.from_topic_sets(topics, players=m))
    paths = positions = certificates = 0
    tight_positions = 0
    minimum_slack = None
    for instance in instances:
        solver = ExactSPESolver(instance)
        first = True
        for path in solver.ordered_outcomes():
            spectrum = path_spectrum(instance, path)
            payoffs = instance.player_payoffs(path)
            assert all(u >= floor for u, floor in zip(payoffs, spectrum))
            assert sum(payoffs) >= sum(spectrum)
            paths += 1
            positions += instance.players
            for u, floor in zip(payoffs, spectrum):
                slack = u - floor
                tight_positions += slack == 0
                minimum_slack = slack if minimum_slack is None else min(slack, minimum_slack)
            if first:
                verify_certificate(instance, solver.certificate(on_path=path)).assert_valid()
                certificates += 1
                first = False
    return {
        "instances": len(instances), "all_supported_ordered_paths": paths,
        "position_inequalities": positions, "tight_positions": tight_positions,
        "minimum_slack": str(minimum_slack),
        "full_history_certificates_replayed": certificates,
        "purpose": "Finite implementation regression, not a universal proof.",
    }


def graph_bank_instance(m: int) -> tuple[Instance, tuple[int, ...], int, int]:
    L = lcm(*range(1, m + 1))
    K = (m - 1) * L
    labels = tuple(f"B{j + 1}" for j in range(m)) + tuple(f"A{r}" for r in range(1, m + 1))
    customers = tuple(CustomerType(frozenset({j, k}), L)
                      for j, k in combinations(range(m), 2)) + tuple(
        CustomerType(frozenset({m + r - 1}), K // r) for r in range(1, m + 1))
    instance = Instance(labels, customers, m)
    path = tuple(m + r - 1 for r in range(m, 0, -1))
    return instance, path, L, K


def obstruction(m: int) -> dict:
    instance, path, L, K = graph_bank_instance(m)
    payoffs = instance.player_payoffs(path)
    floors = path_spectrum(instance, path)
    expected = tuple(Fraction(K, r) for r in range(m, 0, -1))
    assert payoffs == expected
    assert floors == list(expected)
    assert all(sum(c.multiplicity for c in instance.customers if a in c.topics) <= K
               for a in range(instance.topic_count))
    W = sum(payoffs)
    D = Fraction(m * K, 2)
    assert D > 2 * W
    # All comparisons and all covers follow analytically from |T|<=K.
    # Independently replay the terminal menu after the penultimate B1 deviation.
    prefix = path[:-2] + (0,)
    follower = {instance.topics[a]: instance.player_payoffs(prefix + (a,))[-1]
                for a in range(instance.topic_count)}
    assert follower["A1"] == K
    assert all(v < K for name, v in follower.items() if name != "A1")
    deviator = instance.player_payoffs(prefix + (m,))[-2]
    assert deviator == K > payoffs[-2] == Fraction(K, 2)
    return {
        "m": m, "L": L, "K": K, "unit_customer_count": instance.customer_count,
        "all_slots_tight": True, "welfare": str(W),
        "optimal_welfare_lower_bound": str(D), "lower_bound_over_W": str(D / W),
        "all_fractional_prefix_rows": "Analytic: |E| <= K tau = r tau u_i for every E and cover.",
        "not_SPE": True, "penultimate_on_path_payoff": str(payoffs[-2]),
        "penultimate_deviation_payoff": str(deviator),
        "last_player_unique_best_reply": "A1",
        "next_best_last_player_payoff": str(max(v for k, v in follower.items() if k != "A1")),
    }


def main() -> None:
    H13 = sum((Fraction(1, r) for r in range(1, 14)), Fraction())
    assert 13 - 4 * H13 == Fraction(25177, 90090) > 0
    result = {
        "identity": "Joint real-prefix omission spectrum and all-m interface obstruction",
        "date": "2026-10-23", "universal_result_basis": "Analytic proof in companion Markdown",
        "regression": regression(), "obstruction": [obstruction(m) for m in (13, 20)],
        "m13_minus_four_H13": str(13 - 4 * H13),
        "Q_CAG_HALF": "OPEN; the obstruction paths are explicitly not SPE.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
