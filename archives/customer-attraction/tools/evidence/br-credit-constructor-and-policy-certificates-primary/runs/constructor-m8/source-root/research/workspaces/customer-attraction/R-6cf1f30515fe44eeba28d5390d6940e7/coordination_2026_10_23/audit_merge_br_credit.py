"""Exact diagnostic of merge routes that discard all BR slack.

The strategy construction is ordinary deterministic backward induction.
Verification separately replays the exported count-policy from every count
state and every deviation, covering all ordered histories by a count-policy.
At m=5 fixed-pivot double-write fails while pivot switching repairs it.
At m=8 the first update alone forces every permitted route to fail (13).
These are counterexamples to sufficient interfaces, not to Q-CAG-HALF.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import argparse
import json

BASE = Path(__file__).resolve().parent
M = 5
P = M + 1
TOPICS = tuple(frozenset((i, M + i)) for i in range(M)) + (frozenset(range(M)),)


def count_states(total_bound, dimensions):
    if dimensions == 0:
        yield ()
        return
    for first in range(total_bound + 1):
        for tail in count_states(total_bound - first, dimensions - 1):
            yield (first,) + tail


def increment(counts, action):
    counts = list(counts)
    counts[action] += 1
    return tuple(counts)


def utility(counts, action):
    return sum((F(1, sum(counts[j] for j, topic in enumerate(TOPICS) if x in topic))
                for x in TOPICS[action]), F(0))


def welfare(counts):
    return len(frozenset().union(*(TOPICS[a] for a, n in enumerate(counts) if n)))


def construct():
    policy = {}

    @lru_cache(None)
    def solve(counts):
        if sum(counts) == M:
            return counts
        candidates = []
        for a in range(P):
            terminal = solve(increment(counts, a))
            # Fully specified deterministic tie breaking.
            candidates.append((utility(terminal, a), tuple(-q for q in terminal), a, terminal))
        _, _, a, terminal = max(candidates)
        policy[counts] = a
        return terminal

    solve((0,) * P)
    return policy


def verify(policy):
    # Recompute all terminal outcomes by exported policy, not solve().
    @lru_cache(None)
    def replay(counts):
        if sum(counts) == M:
            return counts
        return replay(increment(counts, policy[counts]))

    comparisons = 0
    for counts, chosen in policy.items():
        assert len(counts) == P and all(q >= 0 for q in counts) and sum(counts) < M
        chosen_terminal = replay(increment(counts, chosen))
        chosen_value = utility(chosen_terminal, chosen)
        for deviation in range(P):
            deviated_terminal = replay(increment(counts, deviation))
            assert chosen_value >= utility(deviated_terminal, deviation)
            comparisons += 1
    # Exhaustive coverage of all count states implies all ordered histories
    # for this policy; compare explicit compositions to exported keys.
    expected = set(count_states(M - 1, P))
    assert set(policy) == expected
    history, counts = [], (0,) * P
    while sum(counts) < M:
        chosen = policy[counts]
        history.append(chosen)
        counts = increment(counts, chosen)
    assert tuple(history) == (M,) * (M - 2) + (M - 1, M - 2)
    assert welfare(counts) == M + 2
    # All 2M clients are covered by the M themes A_i, so the global upper
    # bound 2M is attained without a combinatorial optimization oracle.
    optimum = 2 * M
    assert welfare((1,) * M + (0,)) == optimum
    root_slacks = []
    for b in range(M):
        clone = (0,) * P
        for _ in range(M - 1):
            clone = increment(clone, b)
        assert policy[clone] == M
        values = tuple(utility(increment(clone, a), a) for a in range(P))
        assert values[M] > max(values[:M])
        for a in range(M):
            if a != b:
                slack = values[M] - values[a]
                assert slack == M - 3 + F(1, M)
                root_slacks.append(slack)
    # The unique OPT multiset comprises all A_i, since y_i occurs only in A_i.
    # A fixed-pivot double-write recipe needs two distinct A_i -> R writes,
    # each with slack M-3+1/M. This does NOT cover pivot switching: a newly
    # present R can itself be used as pivot and return an existing A_i.
    rclone = (0,) * P
    for _ in range(M - 1):
        rclone = increment(rclone, M)
    r_reply = policy[rclone]
    values_r = tuple(utility(increment(rclone, a), a) for a in range(P))
    assert r_reply == M - 1
    # Expanded route: A0 -> R with pivot A1, then replace every remaining
    # A other than the highest-index A by that A, with pivot R. The latter
    # comparisons all have zero slack.
    sources = list(range(M))
    expanded_updates = []
    expanded_B = F(0)
    for old, pivot in [(0, 1)] + [(old, M) for old in range(1, M - 1)]:
        assert old in sources and pivot in sources and old != pivot
        clone = (0,) * P
        for _ in range(M - 1):
            clone = increment(clone, pivot)
        new = policy[clone]
        slack = utility(increment(clone, new), new) - utility(increment(clone, old), old)
        assert slack >= 0
        sources[sources.index(old)] = new
        expanded_B += slack
        expanded_updates.append({'old': old, 'pivot': pivot, 'new': new, 'BR_slack': str(slack)})
    assert sorted(sources) == [M - 1] * (M - 1) + [M]
    for _ in range(M - 2):
        assert sources.count(M - 1) >= 2
        sources.remove(M - 1)
    assert sorted(sources) == [M - 1, M]
    assert expanded_B == M - 3 + F(1, M)
    return {
        'status': 'exact full count-policy SPE; interface obstruction scope checked separately',
        'model': 'unit customers, common catalog, arbitrary ordered histories; selected count-policy is allowed',
        'm': M, 'topics': [sorted(t) for t in TOPICS],
        'policy_count_states': len(policy), 'exact_deviation_comparisons': comparisons,
        'actual_path': history, 'actual_terminal_counts': list(counts),
        'W': welfare(counts), 'OPT': optimum,
        'optimal_source_unique_multiset': list(range(M)),
        'initial_A_pivot_slack_per_nonpivot_A': str(root_slacks[0]),
        'R_pivot_reply': r_reply, 'R_pivot_payoffs': [str(v) for v in values_r],
        'fixed_pivot_double_write_root_BR_lower_bound': str(2 * root_slacks[0]),
        'available_half_slack_2W_minus_OPT': 2 * welfare(counts) - optimum,
        'fixed_pivot_no_BR_credit_bound_fails': 2 * root_slacks[0] > 2 * welfare(counts) - optimum,
        'expanded_route_BR_slack': str(expanded_B),
        'expanded_route_updates_at_root': expanded_updates,
        'expanded_route_then_merges_last_A_at_layers': list(range(M - 2)),
        'expanded_route_no_BR_credit_bound_holds': expanded_B <= 2 * welfare(counts) - optimum,
        'any_route_initial_BR_lower_bound': str(root_slacks[0]),
        'all_merge_routes_no_BR_credit_bound_fail': root_slacks[0] > 2 * welfare(counts) - optimum,
        'scope': ('All permitted clone-reply/merge routes fail the no-BR-credit bound (13); retaining BR credit and Q-CAG-HALF remain open.'
                  if root_slacks[0] > 2 * welfare(counts) - optimum else
                  'Fixed-pivot double-write standard recipe fails; switching pivots restores a payable route. No general candidate is refuted.'),
        'policy': [{'counts': list(c), 'action': a} for c, a in sorted(policy.items())],
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--m', type=int, default=5, choices=(5, 8))
    args = parser.parse_args()
    M = args.m
    P = M + 1
    TOPICS = tuple(frozenset((i, M + i)) for i in range(M)) + (frozenset(range(M)),)
    report = verify(construct())
    output = 'merge_br_credit_certificate.json' if M == 5 else 'merge_br_credit_m8_certificate.json'
    options = {'indent': 2} if M == 5 else {'separators': (',', ':')}
    (BASE / output).write_text(json.dumps(report, ensure_ascii=False, **options) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'policy'}, ensure_ascii=False, indent=2))
