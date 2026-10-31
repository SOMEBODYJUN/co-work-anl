"""Exact, all-count-state audit of a full SPE anchor lift.

The policy is a function of counts, hence every ordered history is covered.
Protected nodes implement the proof; every other node is completed by exact
backward induction. This is an auxiliary bridge counterexample, not Q-CAG-HALF.
"""
import argparse
from functools import lru_cache
from itertools import combinations
import json
from math import lcm
from pathlib import Path


def compositions(n, k):
    if k == 1:
        yield (n,)
    else:
        for x in range(n + 1):
            for tail in compositions(n - x, k - 1):
                yield (x,) + tail


def run(m, last_pair='AB'):
    assert m >= 2
    k = m + 3
    # Gadget labels A,B,T,D,E are 0,...,4. The others are private anchors.
    customers = [((1,), 3), ((2,), 3), ((0, 3), 2), ((0, 4), 2),
                 ((1, 3, 4), 2), ((2, 3, 4), 2)]
    customers += [((a,), 4) for a in range(5, k)]
    scale = lcm(*range(1, m + 1))
    rho = (3, 3, 3, 4, 3)
    beta = (1, 3, 3, 4, 3)
    absorber_pairs = {tuple(sorted((a, rho[a]))) for a in range(5)}
    terminal_values = {}

    def utility(q):
        if q not in terminal_values:
            result = [0] * k
            for members, count in customers:
                denominator = sum(q[a] for a in members)
                if denominator:
                    share = count * (scale // denominator)
                    for a in members:
                        result[a] += share
            terminal_values[q] = tuple(result)
        return terminal_values[q]

    policies = {}
    chosen_terminals = {}
    categories = {'anchors_then_pair': 0, 'gadget_reply': 0, 'absorbed_fill': 0, 'free_BI': 0}
    comparisons = 0
    minimum_slack = None
    for depth in range(m, -1, -1):
        for q in compositions(depth, k):
            if depth == m:
                chosen_terminals[q] = q
                continue
            children = [q[:a] + (q[a] + 1,) + q[a + 1:] for a in range(k)]
            scores = [utility(chosen_terminals[c])[a] for a, c in enumerate(children)]
            gadget_count = sum(q[:5])
            anchor_simple = all(c <= 1 for c in q[5:])
            unused = [a for a in range(5, k) if not q[a]]
            if anchor_simple and gadget_count == 0:
                action = unused[0] if unused else (0 if last_pair == 'AB' else 3)
                category = 'anchors_then_pair'
            elif anchor_simple and gadget_count == 1:
                first = next(a for a in range(5) if q[a])
                action = rho[first] if unused else beta[first]
                category = 'gadget_reply'
            elif (anchor_simple and gadget_count == 2
                  and tuple(a for a in range(5) for _ in range(q[a])) in absorber_pairs):
                assert unused
                action = unused[0]
                category = 'absorbed_fill'
            else:
                action = max(range(k), key=lambda a: (scores[a], -a))
                category = 'free_BI'
            for alternative, value in enumerate(scores):
                slack = scores[action] - value
                assert slack >= 0, (m, q, category, action, alternative, slack)
                comparisons += 1
                minimum_slack = slack if minimum_slack is None else min(slack, minimum_slack)
            categories[category] += 1
            policies[q] = action
            chosen_terminals[q] = chosen_terminals[children[action]]
    root = (0,) * k
    q = root
    path = []
    while sum(q) < m:
        a = policies[q]
        path.append(a)
        q = q[:a] + (q[a] + 1,) + q[a + 1:]
    payoffs = [utility(q)[a] // scale for a in path]
    welfare = sum(count for members, count in customers if any(q[a] for a in members))
    opt = max(sum(count for members, count in customers if set(members) & set(support))
              for support in combinations(range(k), m))
    assert welfare == 4 * m + (1 if last_pair == 'AB' else 0)
    assert opt == 4 * m + 2
    assert payoffs == [4] * (m - 1) + [5 if last_pair == 'AB' else 4]
    return {'players': m, 'topics': k, 'last_pair': last_pair, 'unit_customers': 4 * m + 6,
            'welfare': welfare, 'optimum': opt, 'path': path, 'payoffs': payoffs,
            'last_threshold_violation': (m - 1) * payoffs[-1] - welfare,
            'count_decision_states': len(policies), 'all_history_comparisons_by_counts': comparisons,
            'terminal_count_states': len(terminal_values), 'minimum_scaled_slack': minimum_slack,
            'categories': categories,
            'status': 'complete count policy; all ordered histories covered by count invariance'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--max-players', type=int, default=7)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    records = [run(m, pair) for m in range(2, args.max_players + 1) for pair in ['AB', 'DE']]
    args.output.write_text(json.dumps(records, indent=2))
    for row in records:
        print(json.dumps(row), flush=True)


if __name__ == '__main__':
    main()
