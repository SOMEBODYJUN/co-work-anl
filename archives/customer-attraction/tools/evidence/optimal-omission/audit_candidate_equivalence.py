#!/usr/bin/env python3
"""Exact two-player comparison of the preserved discovery and proof inputs.

This cleanup audit reads the frozen candidate JSON and the literal GROUPS in
the preserved author source. It does not execute/import either old audit or
use an optimizer. Assertions are explicitly required. No discovery/minimality
or three-player equilibrium claim is made.
"""
import ast
from fractions import Fraction
from hashlib import sha256
from itertools import combinations_with_replacement, product
import json
from pathlib import Path

if not __debug__:
    raise RuntimeError("Run without -O/-OO: assertions must be enabled")

HERE = Path(__file__).resolve().parent
ORIGINAL = HERE / "original/research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/global"


def literal_assignment(path, name):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    values = [ast.literal_eval(node.value) for node in tree.body
              if isinstance(node, ast.Assign)
              and any(isinstance(target, ast.Name) and target.id == name
                      for target in node.targets)]
    assert len(values) == 1
    return values[0]


def expand(groups):
    clients = []
    for interest, count in groups:
        assert isinstance(count, int) and not isinstance(count, bool) and count > 0
        clients.extend(frozenset(interest) for _ in range(count))
    return clients


def covered(clients, profile):
    return {i for i, interest in enumerate(clients)
            if any(label in interest for label in profile)}


def utility(clients, profile, player):
    return sum((Fraction(1, sum(label in interest for label in profile))
                for interest in clients if profile[player] in interest), Fraction(0))


def inspect(clients, labels, reply, root):
    topics = {label: covered(clients, (label,)) for label in labels}
    matrix = [[utility(clients, (first, second), 1) for second in labels]
              for first in labels]
    intersections = [[len(topics[a] & topics[b]) for b in labels] for a in labels]
    assert len({frozenset(topic) for topic in topics.values()}) == 6
    # Full 6x6 follower comparisons plus six root continuation comparisons.
    gaps = []
    for first in labels:
        selected = utility(clients, (first, reply[first]), 1)
        for query in labels:
            gap = selected - utility(clients, (first, query), 1)
            assert gap >= 0
            gaps.append({"history": first, "query": query, "slack": str(gap)})
    root_payoff = utility(clients, (root, reply[root]), 0)
    for query in labels:
        gap = root_payoff - utility(clients, (query, reply[query]), 0)
        assert gap >= 0
        gaps.append({"history": "", "query": query, "slack": str(gap)})
    pairs = {"".join(pair): len(covered(clients, pair))
             for pair in combinations_with_replacement(labels, 2)}
    opt = max(pairs.values())
    maximizers = [pair for pair, value in pairs.items() if value == opt]
    assert maximizers == ["TQ"]
    actual = covered(clients, (root, reply[root]))
    optimal = covered(clients, ("T", "Q"))
    values = {"W": len(actual), "OPT": opt, "omitted_L": len(optimal - actual),
              "actual_exclusive_E": len(actual - optimal),
              "intersection": len(actual & optimal), "half_slack": 2 * len(actual) - opt}
    assert values == {"W": 35, "OPT": 38, "omitted_L": 36,
                      "actual_exclusive_E": 33, "intersection": 2, "half_slack": 32}
    for a, b in product(labels, repeat=2):
        assert utility(clients, (a, b), 0) == len(topics[a]) - Fraction(len(topics[a] & topics[b]), 2)
        assert utility(clients, (a, b), 1) == len(topics[b]) - Fraction(len(topics[a] & topics[b]), 2)
    return {"unit_customers": len(clients), "distinct_topics": len(topics),
            "topic_sizes": {label: len(topics[label]) for label in labels},
            "intersection_matrix": intersections,
            "follower_matrix": [[str(value) for value in row] for row in matrix],
            "all_history_comparisons_including_self": len(gaps),
            "all_history_gap_certificate": gaps,
            "unordered_pair_coverage": pairs,
            "unique_optimal_unordered_pair": "TQ", "values": values}


def run():
    candidate_path = ORIGINAL / "optimal_omission_candidate.json"
    author_path = ORIGINAL / "audit_optimal_omission.py"
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    labels = tuple(candidate["topics"])
    assert labels == tuple("ABTQRS") and candidate["players"] == 2
    groups_candidate = [("".join(labels[i] for i in row["topics"]), row["multiplicity"])
                        for row in candidate["customers"]]
    groups_family = literal_assignment(author_path, "GROUPS")
    assert len(groups_candidate) == 14 and len(groups_family) == 12
    assert groups_candidate != list(groups_family)
    c, f = expand(groups_candidate), expand(groups_family)
    assert len(c) == len(f) == 71
    root = labels[candidate["root"]]
    reply = {label: labels[action] for label, action in zip(labels, candidate["reply"])}
    assert root == "A" and reply == dict(zip(labels, "BSRSSR"))
    result_c, result_f = inspect(c, labels, reply, root), inspect(f, labels, reply, root)
    assert result_c == result_f
    comparisons = 0
    for profile in product(labels, repeat=2):
        for player in (0, 1):
            assert utility(c, profile, player) == utility(f, profile, player)
            comparisons += 1
    triple_count = lambda clients: sum(all(label in interest for label in "BRS") for interest in clients)
    triple_c, triple_f = triple_count(c), triple_count(f)
    payoff_c, payoff_f = utility(c, tuple("BRS"), 0), utility(f, tuple("BRS"), 0)
    assert (triple_c, triple_f) == (2, 6)
    assert (payoff_c, payoff_f) == (Fraction(41, 3), Fraction(15))
    return {"status": "exact candidate/proof-input comparison passed",
            "scope": "two-player payoff and pair-union equivalence; no higher-player equivalence",
            "labels": labels, "root": root, "reply": reply,
            "candidate_types": groups_candidate, "proof_k3_types": groups_family,
            "input_sha256": {p.name: sha256(p.read_bytes()).hexdigest() for p in (candidate_path, author_path)},
            "optimizer_status_copied_as_unverified_history": candidate["status"],
            "optimizer_called": False,
            "terminal_player_payoffs_compared": comparisons,
            "common_two_player_certificate": result_c,
            "higher_order_difference": {"intersection": "BRS", "candidate_count": triple_c,
                                        "proof_count": triple_f, "profile": ["B", "R", "S"],
                                        "player": 0, "candidate_payoff": str(payoff_c),
                                        "proof_payoff": str(payoff_f),
                                        "payoff_difference_proof_minus_candidate": str(payoff_f - payoff_c)}}


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
