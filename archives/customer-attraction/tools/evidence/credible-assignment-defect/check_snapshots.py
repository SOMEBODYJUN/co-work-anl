"""Verify the two saved assignment probes using exact standard-library arithmetic."""

import json
from fractions import Fraction
from functools import cache
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, permutations, product
from pathlib import Path
from sys import argv


SOURCE = Path(__file__).resolve().parent / "source"
HASHES = {
    "assignment_defect_probe.py": "ca4e322c840c40e5748427e36589be83443e90fbe28114e7134a315ea0761be3",
    "assignment_probe_m5p9.json": "f5595322c2b6e38b87012057150277597ff89cbcd56fa84c9310ab7d669738c8",
    "assignment_probe_m5p9.json.summary.json": "4fb7380c6f1a8b11110e12d00287a9072c01d77f90b5c310bf092094c4fa67a5",
    "assignment_probe_m5p10.json": "285d424910b9481431f52f89e17c99a5fb4408b0cb4a35ea1f383c0eb912506b",
    "assignment_probe_m5p10.json.summary.json": "7fea23d1d682b4582e2531a012463cdafd6e9e7fea613df7e9b76885fcfa5e16",
}


def coverage(topics, portfolio):
    return set().union(*(topics[label] for label in portfolio))


def check_snapshot(name, replay_dir):
    data = json.loads((SOURCE / name).read_text())
    summary = json.loads((SOURCE / (name + ".summary.json")).read_text())
    p, m, n = (data[key] for key in ("p", "m", "n"))
    labels = range(p)
    members = data["member"]
    assert len(members) == n
    assert all(len(row) == p and set(row) <= {0, 1} for row in members)
    topics = [frozenset(x for x, row in enumerate(members) if row[a]) for a in labels]
    assert all(topics)
    policy = {tuple(counts): a for counts, a in data["count_policy"]}
    assert len(policy) == len(data["count_policy"])
    assert all(a in labels for a in policy.values())

    def counts_of(history):
        return tuple(history.count(a) for a in labels)

    @cache
    def terminal(counts):
        if sum(counts) == m:
            return counts
        return terminal(add(counts, policy[counts]))

    def add(counts, a):
        return counts[:a] + (counts[a] + 1,) + counts[a + 1:]

    @cache
    def payoff(counts, a):
        return sum(
            (Fraction(1, sum(counts[b] for b in labels if x in topics[b]))
             for x in topics[a]),
            Fraction(0),
        )

    seen_counts = set()
    nodes = 0
    for depth in range(m):
        for history in product(labels, repeat=depth):
            counts = counts_of(history)
            seen_counts.add(counts)
            chosen = policy[counts]
            chosen_payoff = payoff(terminal(add(counts, chosen)), chosen)
            for a in labels:
                assert chosen_payoff >= payoff(terminal(add(counts, a)), a), (history, a)
            nodes += 1
    assert seen_counts == set(policy)

    def follow(history):
        while len(history) < m:
            history += (policy[counts_of(history)],)
        return history

    actual = follow(())
    assert actual == tuple(data["actual"])
    actual_cover = coverage(topics, actual)
    assert len(actual_cover) == sum(len(topics[a]) for a in actual)
    assert len(actual_cover) == data["W"]
    last = actual[-1]
    last_size = len(topics[last])

    def kernel(background, t, r, d):
        response = Fraction(r - t, background + t + r) if r != t else 0
        return response - Fraction(d, background + t + 1)

    def row_cost(i, a):
        overlap = len(topics[actual[i]] & topics[a])
        if i == m - 1:
            return -Fraction(overlap, 2)
        changed = follow(actual[:i] + (a,))
        reply = changed[-1]
        changed_counts = counts_of(changed)
        last_deviation = counts_of(changed[:-1] + (last,))
        actual_last_deviation = counts_of(actual[:-1] + (reply,))
        own_size = len(topics[actual[i]])
        gaps = (
            own_size - payoff(changed_counts, a),
            payoff(changed_counts, reply) - payoff(last_deviation, last),
            last_size - payoff(actual_last_deviation, reply),
        )
        assert min(gaps) >= 0
        row_target = len(topics[a]) - Fraction(len(topics[a] & actual_cover) - overlap, 2)
        slack = sum(gaps) + Fraction(len(topics[actual[i]] - topics[reply]), 2)
        defect = slack + row_target - Fraction(3 * own_size, 2)
        old_background = actual[:i] + actual[i + 1:-1]
        new_background = changed[:i] + changed[i + 1:-1]
        kernel_defect = Fraction(0)
        for x in range(n):
            t, r, d = (int(x in topics[b]) for b in (a, reply, last))
            h = sum(x in topics[b] for b in new_background)
            b = sum(x in topics[c] for c in old_background)
            kernel_defect += kernel(h, t, r, d) - kernel(b, t, r, d)
        assert defect == kernel_defect
        return defect - Fraction(overlap, 2)

    costs = [[row_cost(i, a) for a in labels] for i in range(m)]
    optimum = max(len(coverage(topics, t)) for t in combinations(labels, m))
    assert optimum == data["OPT"]
    portfolios = [
        t for t in combinations(labels, m) if len(coverage(topics, t)) == optimum
    ]
    multi_optimal = [
        t for t in combinations_with_replacement(labels, m)
        if len(coverage(topics, t)) == optimum
    ]
    assert all(len(set(t)) == m for t in multi_optimal)

    def assignment_value(portfolio, perm):
        return sum(costs[i][portfolio[j]] for i, j in enumerate(perm)) - Fraction(last_size, 2)

    minimum = min(
        assignment_value(t, perm) for t in portfolios for perm in permutations(range(m))
    )
    portfolio = tuple(data["portfolio"])
    assignment = data["assignment"]
    assert portfolio in portfolios
    assert sorted(assignment) == list(range(m))
    assert [[row[a] for a in portfolio] for row in costs] == [
        [Fraction(x) for x in row] for row in data["cost"]
    ]
    assert minimum == assignment_value(portfolio, assignment) == Fraction(data["excess"])
    assert Fraction(summary["best_excess"]) == minimum
    assert 0 <= data["trial"] < summary["trials_executed"] <= summary["trials_requested"]
    assert summary["counterexample_found"] == (minimum > 0)
    if replay_dir:
        assert (replay_dir / name).read_bytes() == (SOURCE / name).read_bytes()
        replay_summary = json.loads((replay_dir / (name + ".summary.json")).read_text())
        assert summary.keys() == replay_summary.keys()
        assert all(summary[key] == replay_summary[key] for key in summary if key != "seconds")
    return {
        "source": name,
        "count_rows": len(policy),
        "ordered_history_nodes": nodes,
        "nontrivial_deviations": nodes * (p - 1),
        "early_row_defects": (m - 1) * p,
        "optimal_portfolios": len(portfolios),
        "optimal_multisets_including_repeats": len(multi_optimal),
        "minimum_excess": str(minimum),
        "replay_matches": bool(replay_dir),
    }


if __name__ == "__main__":
    assert all(sha256((SOURCE / name).read_bytes()).hexdigest() == digest
               for name, digest in HASHES.items())
    replay_dir = Path(argv[1]) if len(argv) > 1 else None
    print(json.dumps([check_snapshot(f"assignment_probe_m5p{p}.json", replay_dir)
                      for p in (9, 10)], indent=2))
