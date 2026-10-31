"""Independent permutation realization check for the activation audit DAG.

No game solver, no new game instance and no SPE scope inference.  The earlier
immutable activation report supplies the exact Bernoulli integral marginals.
"""
from collections import Counter
from fractions import Fraction
from itertools import permutations
from pathlib import Path
from math import factorial
import json

DAG = {
    (0, "a"): ((1, "b"), (3, "a"), (5, "b")),
    (1, "b"): ((2, "a"), (3, "b"), (4, "a")),
    (2, "a"): ((3, "a"), (5, "a")),
    (3, "a"): ((4, "b"), (5, "a")),
    (3, "b"): ((4, "a"), (5, "b")),
    (4, "a"): ((5, "a"),),
    (4, "b"): (),
    (5, "a"): (),
    (5, "b"): (),
}
M = 6
root = Path(__file__).parent
with (root / "predictable_activation_audit.json").open(encoding="utf-8") as f:
    prior = json.load(f)
assert prior["status"] == "passed"
expected = {
    tuple(report["source"]): {
        tuple(s["state"]): Fraction(s["absorb"]) for s in report["states"]
    } for report in prior["reports"]
}
counts = {source: Counter() for source in DAG}
worlds = 0
routes = 0
for order in permutations(range(M)):
    rank = {i: k for k, i in enumerate(order)}
    for source in DAG:
        owner = source[0]
        state = source
        while True:
            successors = [j for j in DAG[state] if rank[j[0]] >= rank[owner]]
            if not successors:
                counts[source][state] += 1
                routes += 1
                break
            target = successors[0]
            assert target[0] > state[0]
            state = target
    worlds += 1
assert worlds == factorial(M)
checks = 0
for source in DAG:
    assert sum(counts[source].values()) == worlds
    for state in DAG:
        actual = Fraction(counts[source][state], worlds)
        assert actual == expected[source].get(state, 0), (source, state, actual)
        checks += 1
report = {
    "status": "passed",
    "scope": "same fixed definition-level DAG; independent rank-world enumeration",
    "priority_worlds": worlds,
    "sources": len(DAG),
    "unit_routes": routes,
    "exact_marginal_comparisons": checks,
    "each_source_unit_in_every_world": True,
    "proves_general_budget": False,
}
with (root / "priority_coupling_audit.json").open("x", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(json.dumps(report, ensure_ascii=False))
