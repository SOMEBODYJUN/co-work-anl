"""Exact static query comparison for the saved eleven-customer SPE report.

The original probe replay verifies the complete SPE. This separate new audit
checks the different query objects and the four off-path tie substitutions;
it does not repeat the SPE search or execute either floating-point LAST probe.
"""
from fractions import Fraction as F
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
REPORT = BASE / (
    "original/research/workspaces/customer-attraction/"
    "R-d1dc7a18aded4304a25a87486681fb21/exchange/"
    "actual_extra_candidate_failure.json"
)
OLD_CERT = BASE / (
    "original/evidence/certificates/customer_attraction/"
    "coverage_opportunity_failure.json"
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    data = json.loads(REPORT.read_text())
    instance = data["instance"]
    customers = instance["customers"]
    m = instance["players"]
    k = len(instance["topics"])
    require(m == 3 and k == 5, "fixed input size")
    path = data["audit"]["actual_path"]
    counts = tuple(path.count(a) for a in range(k))
    require(list(counts) == data["certificate"]["terminal_counts"], "counts")
    b = tuple(path[:-1].count(a) for a in range(k))

    def load(customer, vector):
        return sum(vector[a] for a in customer["topics"])

    query = tuple(
        sum(
            (F(c["multiplicity"], 1 + load(c, counts))
             for c in customers if t in c["topics"]), F()
        )
        for t in range(k)
    )
    welfare = sum(c["multiplicity"] for c in customers if load(c, counts))
    require([str(x) for x in query] == data["queries"], "query report")
    require(welfare == data["W"] == 8, "welfare")
    require(m * max(query) - welfare == F(data["mM_minus_W"]) == 1, "gap")

    kernel = tuple(
        tuple(
            sum(
                (F(c["multiplicity"], 1 + load(c, b) + (a in c["topics"]))
                 for c in customers if t in c["topics"]), F()
            )
            for a in range(k)
        )
        for t in range(k)
    )
    p = q = (F(0), F(1, 3), F(1, 3), F(1, 6), F(1, 6))
    require(len(p) == k and sum(p) == 1 and all(x >= 0 for x in p), "simplex")
    row_values = tuple(sum(kernel[t][a] * q[a] for a in range(k)) for t in range(k))
    column_values = tuple(sum(p[t] * kernel[t][a] for t in range(k)) for a in range(k))
    value = F(7, 3)
    require(max(row_values) == min(column_values) == value, "minimax certificates")
    require(m * value == 7 <= welfare, "LAST on this path")

    old = json.loads(OLD_CERT.read_text())
    to_map = lambda cert: {tuple(r["history"]): r["action"] for r in cert["actions"]}
    old_map, new_map = to_map(old), to_map(data["certificate"])
    require(set(old_map) == set(new_map), "history domains")
    differences = [
        {"history": list(h), "old_action": old_map[h], "new_action": new_map[h]}
        for h in sorted(old_map) if old_map[h] != new_map[h]
    ]
    require(len(differences) == 4, "tie difference count")
    for row in differences:
        require(row["history"] in ([0, 1], [0, 2], [1, 0], [2, 0]), "tie history")
        require((row["old_action"], row["new_action"]) == (3, 4), "D to E")
    # D and E have the same size and intersections with every action in
    # each affected prefix. Thus all three players' terminal payoffs agree.
    set_size = lambda a: sum(c["multiplicity"] for c in customers if a in c["topics"])
    intersect = lambda a, z: sum(
        c["multiplicity"] for c in customers if a in c["topics"] and z in c["topics"]
    )
    require(set_size(3) == set_size(4), "dummy topic sizes")
    require(all(intersect(a, 3) == intersect(a, 4) for a in (0, 1, 2)), "intersections")
    require(all(intersect(*row["history"]) == 0 for row in differences), "disjoint prefixes")

    print(json.dumps({
        "scope": "New exact static query comparison; not a second SPE search",
        "topics": instance["topics"],
        "actual_path": path,
        "actual_counts": counts,
        "actual_prelast_counts": b,
        "query_values": list(map(str, query)),
        "welfare": welfare,
        "extra_query_gap": str(m * max(query) - welfare),
        "last_kernel": [[str(x) for x in row] for row in kernel],
        "query_distribution": list(map(str, p)),
        "blocker_distribution": list(map(str, q)),
        "row_values_against_q": list(map(str, row_values)),
        "column_values_against_p": list(map(str, column_values)),
        "last_minimax_value": str(value),
        "m_times_last_value": str(m * value),
        "different_off_path_actions": differences,
        "same_instance_and_actual_path_not_same_complete_certificate": True,
        "whole_history_spe_verified_by": "one original exact probe replay",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
