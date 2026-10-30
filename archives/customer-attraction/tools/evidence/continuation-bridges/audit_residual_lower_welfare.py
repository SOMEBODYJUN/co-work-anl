"""Check the lower-welfare witness mentioned by continuation_lemmas.md.

This checks this fixed fourteen-unit-customer instance, not arbitrary JSON.
It does not import the canonical model, solver, or continuation audit.
"""

from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INSTANCE = ROOT / "examples/customer_attraction/residual_counterexample.json"
CERTIFICATE = ROOT / "evidence/certificates/customer_attraction/residual_counterexample.json"


def run():
    instance = json.loads(INSTANCE.read_text())
    original = json.loads(CERTIFICATE.read_text())
    customers = tuple(frozenset(row["topics"]) for row in instance["customers"]
                      for _ in range(row["multiplicity"]))
    assert instance["players"] == 2 and instance["topics"] == ["A", "B", "T", "D", "E"]
    assert len(customers) == 14
    original_actions = {tuple(row["history"]): row["action"] for row in original["actions"]}
    assert len(original_actions) == len(original["actions"]) == 6
    assert set(original_actions) == {()} | {(a,) for a in range(5)}
    actions = dict(original_actions)
    actions[()] = 3

    def payoff(action, path):
        return sum((Fraction(1, sum(a in liked for a in path))
                    for liked in customers if action in liked), Fraction())

    def welfare(path):
        return sum(any(a in liked for a in path) for liked in customers)

    follower_rows = []
    root_values = []
    slacks = []
    for first in range(5):
        response = actions[(first,)]
        values = tuple(payoff(second, (first, second)) for second in range(5))
        assert values[response] == max(values)
        slacks.extend(values[response] - values[b] for b in range(5) if b != response)
        root_values.append(payoff(first, (first, response)))
        follower_rows.append({"first_action": first, "prescribed_response": response,
                              "payoffs_by_response": [str(v) for v in values]})
    assert root_values == [Fraction(4)] * 5
    slacks.extend(root_values[actions[()]] - root_values[b]
                  for b in range(5) if b != actions[()])
    assert len(slacks) == 24 and min(slacks) == 0
    path = (actions[()], actions[(actions[()],)])
    payoffs = tuple(payoff(action, path) for action in path)
    assert path == (3, 4) and payoffs == (4, 4)
    assert welfare(path) == 8 < 9
    optimum = max(welfare(path) for path in product(range(5), repeat=2))
    assert optimum == 10 and 2 * welfare(path) >= optimum
    certificate = {"terminal_counts": [0, 0, 0, 1, 1],
                   "actions": [{"history": list(h), "action": a}
                               for h, a in sorted(actions.items(), key=lambda row: (len(row[0]), row[0]))]}
    return {
        "scope": "One additional complete SPE witness; no exhaustive all-SPE claim",
        "arithmetic": "fractions.Fraction; expanded unit customers",
        "input_sha256": hashlib.sha256(INSTANCE.read_bytes()).hexdigest(),
        "original_certificate_sha256": hashlib.sha256(CERTIFICATE.read_bytes()).hexdigest(),
        "change_from_original_certificate": "Only the root action changes from A to D",
        "certificate": certificate,
        "path": list(path), "payoffs": [str(v) for v in payoffs],
        "welfare": welfare(path), "original_welfare": 9, "optimal_welfare": optimum,
        "checked_histories": 6, "checked_nontrivial_deviations": len(slacks),
        "minimum_deviation_slack": str(min(slacks)),
        "root_branch_payoffs": [str(v) for v in root_values],
        "follower_nodes": follower_rows,
        "original_welfare_is_not_worst_spe_welfare": True,
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
