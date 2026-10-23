"""One targeted, exact diagnostic of u >= theta_(r+1)(b).

Reads three existing complete certificates. No solver or author verifier imported.
All ordered decision histories are checked, and actual prefixes reported separately.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement, product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[5]
CASES = [
    ("individual_security_34", "examples/customer_attraction/individual_security_failure.json",
     "evidence/certificates/customer_attraction/individual_security_failure.json"),
    ("aggregate_theta_36", "examples/customer_attraction/aggregate_theta_failure.json",
     "evidence/certificates/customer_attraction/aggregate_theta_failure.json"),
    ("BAAF_61", "examples/customer_attraction/root_tax_failure.json",
     "research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/direct_cover/actual_root_B_certificate.json"),
]

def run_case(name, instance_file, policy_file):
    instance = json.loads((ROOT / instance_file).read_text())
    saved = json.loads((ROOT / policy_file).read_text())
    cert = saved.get("strategy", saved.get("certificate", saved))
    policy = {tuple(row["history"]): row["action"] for row in cert["actions"]}
    labels = instance["topics"]
    k, m = len(labels), instance["players"]
    customers = tuple(frozenset(row["topics"]) for row in instance["customers"]
                      for _ in range(row.get("multiplicity", 1)))

    def continuation(history):
        history = tuple(history)
        while len(history) < m:
            history += (policy[history],)
        return history

    def utility(path, i):
        return sum((F(1, sum(a in x for a in path))
                    for x in customers if path[i] in x), F())

    def theta(history):
        r = m - len(history)
        best = None
        witnesses = []
        for competitors in combinations_with_replacement(range(k), r):
            query_values = tuple(sum((F(1, 1 + sum(a in x for a in history + competitors))
                                      for x in customers if query in x), F())
                                 for query in range(k))
            cap = max(query_values)
            if best is None or cap < best:
                best, witnesses = cap, [(competitors, query_values)]
            elif cap == best:
                witnesses.append((competitors, query_values))
        return best, witnesses

    nodes = []
    comparisons = 0
    actual = continuation(())
    for depth in range(m):
        for history in product(range(k), repeat=depth):
            path = continuation(history)
            current = utility(path, depth)
            for action in range(k):
                deviated = continuation(history + (action,))
                assert current >= utility(deviated, depth), (name, history, action)
                comparisons += 1
            value, witnesses = theta(history)
            competitors, query_values = witnesses[0]
            nodes.append({"history": list(history), "history_labels": [labels[a] for a in history],
                          "remaining": m - depth, "utility": str(current), "theta_extra": str(value),
                          "margin": str(current - value), "actual_prefix": history == actual[:depth],
                          "minimizer_count": len(witnesses),
                          "one_competitor_tuple": list(competitors),
                          "one_competitor_labels": [labels[a] for a in competitors],
                          "query_values": list(map(str, query_values))})
    violations = [row for row in nodes if F(row["margin"]) < 0]
    return {"name": name, "instance_file": instance_file, "policy_file": policy_file,
            "customers": len(customers), "decision_nodes": len(nodes),
            "action_comparisons": comparisons, "complete_spe_verified": True,
            "actual": list(actual), "actual_labels": [labels[a] for a in actual],
            "actual_payoffs": [str(utility(actual, i)) for i in range(m)],
            "all_history_violation_count": len(violations), "violations": violations,
            "actual_prefix_rows": [row for row in nodes if row["actual_prefix"]],
            "minimum_margin_row": min(nodes, key=lambda row: F(row["margin"]))}

result = {"statement": "For every valid ordered background b and complete r-player SPE, first payoff u >= min_(q in S^r) max_T sum_(x in T) 1/(1+b_x+c_x(q)).",
          "scope": "Only three preselected existing certificates; no random or expanded sample.",
          "cases": [run_case(*case) for case in CASES]}
destination = Path(__file__).with_name("extra_slot_pure_theta_probe.json")
with destination.open("x") as stream:
    json.dump(result, stream, indent=2)
    stream.write("\n")
print(json.dumps(result, indent=2))
