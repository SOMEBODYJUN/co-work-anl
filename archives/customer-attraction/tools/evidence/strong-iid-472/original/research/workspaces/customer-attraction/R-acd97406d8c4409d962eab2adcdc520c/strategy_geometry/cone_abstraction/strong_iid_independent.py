"""Independent definition-level audit of the integer strong-iid witness.

Imports no repository model, solver, constructor, or original iid verifier.
The static expectation is enumerated over ordered opponent profiles, rather
than using the constructor's per-type closed formula.
"""

from fractions import Fraction as F
from itertools import product
import json
import hashlib
from pathlib import Path
import sys


def main():
    workspace = Path(__file__).resolve().parents[2]
    witness_path = (Path(sys.argv[1]) if len(sys.argv) > 1 else
                    workspace / "dynamic_security" / "strong_iid_472_five_topics.json")
    data = json.loads(witness_path.read_text())
    n = data["players"]
    labels = tuple(data["topics"])
    assert n == 3 and labels == tuple(range(len(labels)))
    weights = {int(mask): count for mask, count in data["weights"].items()}
    assert all(isinstance(count, int) and count > 0 for count in weights.values())
    assert all(0 < mask < 2 ** len(labels) for mask in weights)
    policy = {tuple(history): action for history, action in data["actions"]}
    histories = tuple(h for depth in range(n) for h in product(labels, repeat=depth))
    assert len(policy) == len(data["actions"]) == len(histories)
    assert set(policy) == set(histories)
    assert set(policy.values()) <= set(labels)
    q = tuple(map(F, data["q"]))
    assert len(q) == len(labels) and min(q) >= 0 and sum(q) == 1

    def final_profile(history):
        history = tuple(history)
        while len(history) < n:
            history += (policy[history],)
        return history

    def utility(action, profile):
        value = F(0)
        for mask, count in weights.items():
            if mask & (1 << action):
                covered_by = sum(bool(mask & (1 << selected)) for selected in profile)
                assert covered_by > 0
                value += F(count, covered_by)
        return value

    def welfare(profile):
        return sum(count for mask, count in weights.items()
                   if any(mask & (1 << selected) for selected in profile))

    slacks = []
    root_menu = None
    for history in histories:
        selected = policy[history]
        continuation = final_profile(history)
        actual = utility(selected, continuation)
        menu = []
        for alternative in labels:
            deviated = final_profile(history + (alternative,))
            counterfactual = utility(alternative, deviated)
            menu.append(counterfactual)
            slacks.append(actual - counterfactual)
        if not history:
            root_menu = menu
    assert min(slacks) >= 0

    # Directly integrate the pure query against every ordered iid pair.
    alpha = []
    for action in labels:
        expected = F(0)
        for opponents in product(labels, repeat=n - 1):
            probability = F(1)
            for other in opponents:
                probability *= q[other]
            expected += probability * utility(action, (action,) + opponents)
        alpha.append(expected)
    support = tuple(a for a in labels if q[a] > 0)
    common_value = alpha[support[0]]
    assert all(alpha[a] == common_value for a in support)
    assert all(value <= common_value for value in alpha)

    # Independently enumerate the expected coverage of all 6^3 iid profiles.
    Z = F(0)
    for profile in product(labels, repeat=n):
        probability = F(1)
        for selected in profile:
            probability *= q[selected]
        Z += probability * welfare(profile)
    assert Z == n * sum(q[a] * alpha[a] for a in labels)
    actual_profile = final_profile(())
    W = welfare(actual_profile)
    best = max(welfare(profile) for profile in product(labels, repeat=n))
    optimal_profiles = tuple(profile for profile in product(labels, repeat=n)
                             if welfare(profile) == best)
    signatures = {a: tuple(bool(mask & (1 << a)) for mask in weights) for a in labels}
    assert len(set(signatures.values())) == len(labels)
    assert all(any(signature) for signature in signatures.values())
    assert actual_profile == tuple(data["path"])
    assert str(W) == data["W"] and str(Z) == data["Z"]
    assert alpha == list(map(F, data["alpha"]))
    if "minimum_incentive" in data:
        assert str(min(slacks)) == data["minimum_incentive"]
    assert W < Z
    report = {
        "status": "exact independent audit passed",
        "scope": "refutes only strong W>=Z_n bridge",
        "players": n, "labels": len(labels), "integer_unit_customers": sum(weights.values()),
        "interest_types": len(weights), "distinct_nonempty_topics": True,
        "ordered_decision_nodes": len(histories), "all_history_comparisons": len(slacks),
        "minimum_SPE_slack": str(min(slacks)),
        "strict_nonself_comparisons": sum(value > 0 for value in slacks),
        "root_deviation_menu": list(map(str, root_menu)),
        "actual_profile": actual_profile,
        "actual_individual_utilities": [str(utility(action, actual_profile)) for action in actual_profile],
        "q": list(map(str, q)), "q_support": support,
        "iid_query_utilities_from_ordered_opponent_profiles": list(map(str, alpha)),
        "iid_KKT_support_value": str(common_value),
        "iid_KKT_offsupport_slacks": {str(a): str(common_value - alpha[a])
                                        for a in labels if not q[a]},
        "W": str(W), "Z_from_ordered_profiles": str(Z), "Z_minus_W": str(Z - W),
        "OPT_3": str(best), "optimal_profile_example": optimal_profiles[0],
        "half_coverage_margin_2W_minus_OPT": str(2 * W - best),
        "weak_iid_margin_W_minus_5Z_over_6": str(F(W) - F(5, 6) * Z),
        "source_witness": str(witness_path),
        "source_sha256": hashlib.sha256(witness_path.read_bytes()).hexdigest(),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
