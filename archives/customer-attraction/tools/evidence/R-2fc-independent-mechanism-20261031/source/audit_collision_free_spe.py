"""Independent exact audit of the five-customer collision-free SPE.

Uses only the Python standard library and explicit unit customer sets.
No canonical solver, certificate verifier, or discoverer's program is imported.
The output path is optional; a new output file is required when supplied.
"""

from fractions import Fraction
from itertools import product
import argparse
import json
from pathlib import Path


TOPICS = (
    frozenset((0, 1, 2)),
    frozenset((0, 1, 3)),
    frozenset((0, 1)),
    frozenset((3, 4)),
)
CLIENTS = tuple(range(5))
ROOT_ACTION = 2
REPLY = (1, 0, 3, 0)


def loads(profile):
    return tuple(sum(x in TOPICS[a] for a in profile) for x in CLIENTS)


def payoff(profile, player):
    counts = loads(profile)
    return sum(
        (Fraction(1, counts[x]) for x in TOPICS[profile[player]]),
        Fraction(0),
    )


def welfare(profile):
    return sum(c > 0 for c in loads(profile))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rows = []
    checked = 0
    for first in range(len(TOPICS)):
        prescribed = REPLY[first]
        values = [payoff((first, a), 1) for a in range(len(TOPICS))]
        baseline = values[prescribed]
        for deviating_action, value in enumerate(values):
            assert baseline >= value, (first, prescribed, deviating_action)
            checked += 1
        rows.append({
            "history": [first],
            "player": 1,
            "prescribed_action": prescribed,
            "payoff_by_action": [str(v) for v in values],
            "prescribed_payoff": str(baseline),
            "best_payoff": str(max(values)),
        })

    root_values = [payoff((a, REPLY[a]), 0) for a in range(len(TOPICS))]
    root_baseline = root_values[ROOT_ACTION]
    for deviating_action, value in enumerate(root_values):
        assert root_baseline >= value, deviating_action
        checked += 1
    rows.insert(0, {
        "history": [],
        "player": 0,
        "prescribed_action": ROOT_ACTION,
        "payoff_by_action_with_true_continuations": [str(v) for v in root_values],
        "prescribed_payoff": str(root_baseline),
        "best_payoff": str(max(root_values)),
    })

    actual = (ROOT_ACTION, REPLY[ROOT_ACTION])
    actual_loads = loads(actual)
    actual_welfare = welfare(actual)
    coverage_by_profile = {
        str(profile): welfare(profile)
        for profile in product(range(len(TOPICS)), repeat=2)
    }
    optimum = max(coverage_by_profile.values())
    assert checked == 20
    assert actual == (2, 3)
    assert set(actual_loads) <= {0, 1}
    assert actual_welfare == 4
    assert optimum == 5
    assert welfare((0, 3)) == 5
    assert 2 * actual_welfare >= optimum
    # For any scalar function f with f(0)=0 and f(1)=1, this is the exact
    # symbolic value of sum_x f(actual_loads[x]); higher loads never occur.
    normalized_load_function_value = sum(actual_loads)
    assert normalized_load_function_value == actual_welfare < optimum

    report = {
        "status": "all_exact_assertions_passed",
        "scope": "one explicit finite full-history pure SPE, not a half-coverage counterexample",
        "customer_count": len(CLIENTS),
        "topics": [sorted(t) for t in TOPICS],
        "decision_histories": len(rows),
        "comparisons_including_self": checked,
        "all_history_rows": rows,
        "actual_profile": actual,
        "actual_loads_by_customer": actual_loads,
        "actual_payoffs": [str(payoff(actual, i)) for i in range(2)],
        "welfare": actual_welfare,
        "optimum": optimum,
        "optimum_witness": [0, 3],
        "coverage_by_all_ordered_profiles": coverage_by_profile,
        "normalized_separable_load_value": normalized_load_function_value,
        "half_coverage_holds": 2 * actual_welfare >= optimum,
    }
    encoded = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(encoded + "\n")
    print(encoded)


if __name__ == "__main__":
    main()
