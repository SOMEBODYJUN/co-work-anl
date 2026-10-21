"""Definition-level audit; no solver or canonical CAG imports."""

from fractions import Fraction
from itertools import combinations_with_replacement
import json
from pathlib import Path


TOPICS = ("A", "B", "T", "Q", "R", "S")
BLOCKS = (
    ("A", 9), ("B", 9), ("T", 13), ("Q", 8),
    ("AR", 1), ("BR", 4), ("QR", 5),
    ("AS", 1), ("BS", 4), ("QS", 5),
    ("ARS", 5), ("TRS", 5), ("BTRS", 1), ("BQRS", 1),
)
RESPONSES = dict(zip(TOPICS, ("B", "R", "R", "R", "S", "R")))


def main():
    interests = []
    for labels, count in BLOCKS:
        interests.extend([frozenset(labels)] * count)
    sets = {topic: {x for x, labels in enumerate(interests) if topic in labels}
            for topic in TOPICS}

    def utility(action, profile):
        return sum((Fraction(1, sum(x in sets[t] for t in profile))
                    for x in sets[action]), Fraction(0))

    follower_table = {}
    leader_deviations = {}
    comparisons = []
    actual = ("A", "B")
    actual_u = [utility(t, actual) for t in actual]
    for first in TOPICS:
        response = RESPONSES[first]
        chosen = utility(response, (first, response))
        follower_table[first] = []
        for deviation in TOPICS:
            candidate = utility(deviation, (first, deviation))
            assert chosen >= candidate
            follower_table[first].append(str(candidate))
            comparisons.append({"history": [first], "chosen": response,
                                "deviation": deviation,
                                "slack": str(chosen - candidate)})
        candidate = utility(first, (first, response))
        assert actual_u[0] >= candidate
        leader_deviations[first] = str(candidate)
        comparisons.append({"history": [], "chosen": "A", "deviation": first,
                            "slack": str(actual_u[0] - candidate)})

    pairs = {a + b: len(sets[a] | sets[b])
             for a, b in combinations_with_replacement(TOPICS, 2)}
    optimum = max(pairs.values())
    optimizers = [p for p, value in pairs.items() if value == optimum]
    covered = sets["A"] | sets["B"]
    optimal_union = sets["T"] | sets["Q"]
    omitted = optimal_union - covered
    protected_sizes = {topic: len(sets[topic] & omitted) for topic in TOPICS}

    assert len(interests) == 71
    assert [len(sets[t]) for t in TOPICS] == [16, 19, 19, 19, 22, 22]
    assert actual_u == [16, 19]
    assert len(covered) == 35
    assert optimum == 38 and optimizers == ["TQ"]
    assert len(omitted) == 36 > len(covered)
    assert protected_sizes == dict(zip(TOPICS, [0, 0, 18, 18, 10, 10]))
    assert not (sets["T"] & sets["Q"])
    assert len(comparisons) == 42
    # General continuous upper bound min(18*tau,36)-16*tau <= 4,
    # with the maximum at tau=2; T,Q each of weight one attain it.
    assert 36 - 2 * actual_u[0] == 4 > actual_u[1] - actual_u[0]
    assert max(protected_sizes.values()) == 18
    assert len((sets["T"] | sets["Q"]) & omitted) == 36

    result = {
        "status": "PASS", "model": "two providers, unit customers, common catalogue, full-history pure SPE",
        "customers": len(interests), "topics": list(TOPICS),
        "types": [{"interests": list(labels), "count": count} for labels, count in BLOCKS],
        "responses": RESPONSES, "follower_utility_rows": follower_table,
        "leader_deviation_payoffs": leader_deviations,
        "actual_profile": list(actual), "actual_utilities": list(map(str, actual_u)),
        "actual_welfare": len(covered), "pair_coverages": pairs,
        "optimum": optimum, "unique_optimal_unordered_pair": optimizers[0],
        "optimal_omission": len(omitted), "optimal_actual_intersection": len(optimal_union & covered),
        "protected_topic_sizes": protected_sizes, "protected_price_at_16": "4",
        "decision_nodes": 7, "comparisons_checked": len(comparisons),
        "comparison_slacks": comparisons,
        "scope": "Refutes existence-of-optimal-union omission<=W; does not refute half.",
    }
    output = Path(__file__).with_name("unique_optimum_omission_audit.json")
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in (
        "status", "customers", "actual_welfare", "optimum", "optimal_omission",
        "unique_optimal_unordered_pair", "comparisons_checked")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
