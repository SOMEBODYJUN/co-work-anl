"""Exact complete-tree audit of the 35-customer COPY2 counterexample.

This audit constructs one complete SPE by finite backward induction on all
other children and directly replays all ordered histories afterwards.  It
does not import the repository's solver or verifier.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
LABELS = ["A", "E", "D", "F1", "F2"]
BLOCKS = {"C": 6, "P": 12, "X": 8, "Y1": 2, "Y2": 2, "Z": 5}
TOPIC_BLOCKS = [("C", "P"), ("X",), ("Y1", "Y2", "Z"),
                ("C", "X", "Y1"), ("C", "X", "Y2")]


def main():
    customers = {b: tuple(f"{b}{i}" for i in range(w)) for b, w in BLOCKS.items()}
    topics = [frozenset(x for b in bs for x in customers[b]) for bs in TOPIC_BLOCKS]
    assert len(set(topics)) == 5

    def utility(i, z):
        return sum((Q(1, sum(x in topics[t] for t in z)) for x in topics[z[i]]), Q())

    def welfare(z):
        return len(set().union(*(topics[t] for t in z)))

    policy = {}
    # Last player: use the least-label best response except the five stated
    # replies in the A child. Each override is itself checked as a best reply.
    overrides = [3, 2, 3, 4, 3]
    for a, b in product(range(5), repeat=2):
        values = [utility(2, (a, b, t)) for t in range(5)]
        chosen = overrides[b] if a == 0 else max(range(5), key=lambda t: (values[t], -t))
        assert values[chosen] == max(values)
        policy[(a, b)] = chosen

    # Second player: take E after A and least-label best replies elsewhere.
    for a in range(5):
        values = [utility(1, (a, t, policy[(a, t)])) for t in range(5)]
        chosen = 1 if a == 0 else max(range(5), key=lambda t: (values[t], -t))
        assert values[chosen] == max(values)
        policy[(a,)] = chosen
    policy[()] = 0

    def leaf(h):
        h = tuple(h)
        while len(h) < 3:
            h += (policy[h],)
        return h

    rows = []
    for depth in range(3):
        for h in product(range(5), repeat=depth):
            values = [utility(depth, leaf(h + (t,))) for t in range(5)]
            assert values[policy[h]] == max(values), (h, values)
            rows.append({"history": list(h), "action": policy[h],
                         "true_deviation_utilities": list(map(str, values))})
    assert len(rows) == 31

    actual = leaf(())
    copied = leaf((0, 0))
    actual_payoffs = [utility(i, actual) for i in range(3)]
    copied_payoffs = [utility(i, copied) for i in range(3)]
    assert actual == (0, 1, 2)
    assert copied == (0, 0, 3)
    assert actual_payoffs == [Q(18), Q(8), Q(9)]
    assert copied_payoffs == [Q(8), Q(8), Q(12)]
    assert 2 * copied_payoffs[1] < actual_payoffs[0]
    assert 2 * actual_payoffs[1] < actual_payoffs[0]
    assert topics[actual[0]].isdisjoint(topics[actual[1]])
    optimum = max(welfare(z) for z in product(range(5), repeat=3))
    assert welfare(actual) == optimum == len(set().union(*topics)) == 35

    out = {
        "scope": "Counterexample to COPY2 and whole-profit earlier/later ratio2 only; not to prefix request cap2 or half",
        "players": 3, "topic_labels": LABELS,
        "blocks": BLOCKS, "topic_blocks": TOPIC_BLOCKS,
        "expanded_customers": customers, "expanded_topics": [sorted(t) for t in topics],
        "topic_sizes": list(map(len, topics)), "strategy": rows,
        "ordered_nodes": 31, "spe_action_comparisons": 155,
        "actual_leaf": actual, "actual_payoffs": list(map(str, actual_payoffs)),
        "copied_leaf": copied, "copied_payoffs": list(map(str, copied_payoffs)),
        "copy2_gap_original_minus_twice_copy": str(actual_payoffs[0] - 2 * copied_payoffs[1]),
        "ratio2_gap_original_minus_twice_later": str(actual_payoffs[0] - 2 * actual_payoffs[1]),
        "actual_source_recipient_intersection": 0,
        "all_prefix_qplus_to_recipient2": "0",
        "welfare": welfare(actual), "optimum": optimum,
    }
    path = HERE / "copy2_counterexample_audit.json"
    path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k: out[k] for k in ["ordered_nodes", "spe_action_comparisons", "actual_leaf",
          "actual_payoffs", "copied_leaf", "copied_payoffs", "welfare", "optimum"]}))


if __name__ == "__main__":
    main()
