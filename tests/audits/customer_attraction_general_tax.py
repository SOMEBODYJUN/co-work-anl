"""Independent Fraction audit of a fixed-background general-tax failure.

The universal counterexample proof is in general_tax_counterexample.md.
This audit imports neither the canonical model, SPE recurrence, nor certificate
checker. It verifies the complete ordered subgame and the all-A root strategy,
and enumerates every comparison allocation for the supplied finite examples.
"""

from argparse import ArgumentParser
from fractions import Fraction
from itertools import product
import hashlib
import json
from pathlib import Path
import platform
import subprocess


ROOT = Path(__file__).resolve().parents[2]


def expanded_preferences(instance):
    return tuple(frozenset(item["topics"])
                 for item in instance["customers"]
                 for _ in range(item["multiplicity"]))


def payoff(preferences, action, path):
    return sum((Fraction(1, sum(chosen in liked for chosen in path))
                for liked in preferences if action in liked), Fraction(0))


def remaining_total(preferences, prefix, suffix):
    return sum((payoff(preferences, action, prefix + suffix)
                for action in suffix), Fraction(0))


def tax(preferences, prefix, suffix_before_last):
    value = Fraction(0)
    for liked in preferences:
        background = sum(action in liked for action in prefix)
        added = sum(action in liked for action in suffix_before_last)
        value += Fraction(1, background + 1) - Fraction(1, background + added + 1)
    return value


def verify_constant_subgame(preferences, topics, prefix, remaining):
    """Check all histories and true prescribed continuations from this prefix."""
    histories = deviations = 0
    minimum_margin = None
    for depth in range(remaining):
        for history in product(range(topics), repeat=depth):
            histories += 1
            full_prefix = prefix + history
            suffix = (0,) * (remaining - depth)
            actual_payoff = payoff(preferences, 0, full_prefix + suffix)
            for alternative in range(1, topics):
                alternate = (alternative,) + (0,) * (remaining - depth - 1)
                alternate_payoff = payoff(preferences, alternative, full_prefix + alternate)
                margin = actual_payoff - alternate_payoff
                assert margin >= 0
                minimum_margin = margin if minimum_margin is None else min(minimum_margin, margin)
                deviations += 1
    return histories, deviations, minimum_margin


def check_example(instance, expected):
    preferences = expanded_preferences(instance)
    topics = len(instance["topics"])
    prefix = tuple(instance["fixed_prefix"])
    remaining = instance["remaining_players"]
    assert instance["players"] == len(prefix) + remaining
    actual = (0,) * remaining
    sub_histories, sub_deviations, sub_margin = verify_constant_subgame(
        preferences, topics, prefix, remaining)
    # The small main example is embedded at an actually reached root history.
    # For the larger companion the formula proof covers the whole root tree;
    # only the complete remaining-player subgame is explicitly enumerated here.
    root_checks = None
    if instance["players"] <= 7:
        root_checks = verify_constant_subgame(preferences, topics, (), instance["players"])

    comparisons = {
        suffix: remaining_total(preferences, prefix, suffix)
        for suffix in product(range(topics), repeat=remaining)
    }
    optimum = max(comparisons.values())
    maximizing_counts = sorted({tuple(suffix.count(action) for action in range(topics))
                                for suffix, value in comparisons.items() if value == optimum})
    actual_total = remaining_total(preferences, prefix, actual)
    tax_value = tax(preferences, prefix, actual[:-1])
    gap = optimum - actual_total - tax_value
    assert (actual_total, tax_value, optimum, gap) == expected
    assert gap > 0
    assert maximizing_counts == [(2, 1, 1)]

    # Allocation-class maxima give an independent exhaustive F_4 certificate.
    classes = {
        count: max(value for suffix, value in comparisons.items()
                   if suffix.count(0) == count)
        for count in range(remaining + 1)
    }
    full_actual = prefix + actual
    root_welfare = sum(any(action in liked for action in full_actual)
                       for liked in preferences)
    # There are three disjoint topics and at least three root players, so every
    # client can be covered in the root optimum.
    root_optimum = len(preferences)
    assert 2 * root_welfare >= root_optimum

    return {
        "unit_customers": len(preferences),
        "players": instance["players"],
        "fixed_prefix": list(prefix),
        "remaining_players": remaining,
        "actual_suffix": list(actual),
        "subgame_checked_histories": sub_histories,
        "subgame_checked_deviations": sub_deviations,
        "subgame_minimum_incentive_margin": str(sub_margin),
        "root_checked_histories": root_checks[0] if root_checks else None,
        "root_checked_deviations": root_checks[1] if root_checks else None,
        "actual_remaining_total": str(actual_total),
        "tax_before_last_remaining_player": str(tax_value),
        "F_4": str(optimum),
        "total_tax_gap": str(gap),
        "maximizing_remaining_counts": maximizing_counts,
        "allocation_class_maxima_by_A_count": {str(key): str(value) for key, value in classes.items()},
        "comparison_ordered_allocations": len(comparisons),
        "root_welfare": root_welfare,
        "root_optimum": root_optimum,
        "root_half_coverage_holds": True,
    }


def run():
    input_path = ROOT / "examples/customer_attraction/general_tax_failure.json"
    certificate_path = ROOT / "evidence/certificates/customer_attraction/general_tax_failure_subgame.json"
    instance = json.loads(input_path.read_text())
    certificate = json.loads(certificate_path.read_text())
    actions = {tuple(item["suffix_history"]): item["action"]
               for item in certificate["actions"]}
    assert certificate["scope"] == "fixed_prefix_subgame_only"
    assert certificate["fixed_prefix"] == instance["fixed_prefix"]
    expected_histories = {history for depth in range(instance["remaining_players"])
                          for history in product(range(len(instance["topics"])), repeat=depth)}
    assert set(actions) == expected_histories and set(actions.values()) == {0}
    assert certificate["actual_suffix"] == [0] * instance["remaining_players"]

    small = check_example(instance, (Fraction(4), Fraction(3, 4), Fraction(24, 5), Fraction(1, 20)))
    larger = {
        "topics": ["A", "B", "C"], "players": 14,
        "customers": [{"topics": [0], "multiplicity": 84},
                      {"topics": [1], "multiplicity": 6},
                      {"topics": [2], "multiplicity": 6}],
        "fixed_prefix": [0] * 10, "remaining_players": 4,
    }
    large = check_example(larger, (Fraction(24), Fraction(18, 11), Fraction(26), Fraction(4, 11)))
    return {
        "audit": "customer_attraction_general_total_tax_counterexample",
        "arithmetic": "fractions.Fraction",
        "scope": "Two explicit fixed-background total-tax counterexamples; no refutation of root half coverage or root total tax.",
        "python_version": platform.python_version(),
        "base_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "audit_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "input_sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
        "subgame_certificate_sha256": hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
        "nine_unit_customer_example": small,
        "ninety_six_unit_customer_companion": large,
    }


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = json.dumps(run(), ensure_ascii=False, indent=2) + "\n"
    if args.output:
        if args.output.exists():
            raise SystemExit("Refusing to overwrite frozen audit output")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result)
    print(result, end="")
