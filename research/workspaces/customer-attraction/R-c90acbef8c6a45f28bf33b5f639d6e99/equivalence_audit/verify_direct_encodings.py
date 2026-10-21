#!/usr/bin/env python3
"""Definition-level finite audit of two explicit encodings; not a general proof.

No project solver or discovery code is imported. All utilities are computed
from individual unit customers, and all scheduling objectives from assignments.
Run from any directory; JSON is printed to stdout, never overwritten implicitly.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, product
import json


def utility(topics, actions, player):
    load = Counter(x for a in actions for x in topics[a])
    return sum((F(1, load[x]) for x in topics[actions[player]]), F(0))


def coverage(topics, actions):
    return len(set().union(*(topics[a] for a in actions)))


def finish(history, players, rule):
    actions = tuple(history)
    while len(actions) < players:
        actions += (rule(actions),)
    return actions


def check_full_spe(topics, players, rule):
    histories = comparisons = 0
    for depth in range(players):
        for h in product(range(len(topics)), repeat=depth):
            histories += 1
            actual = finish(h, players, rule)
            actual_u = utility(topics, actual, depth)
            for action in range(len(topics)):
                alternative = finish(h + (action,), players, rule)
                assert actual_u >= utility(topics, alternative, depth)
                comparisons += 1
    return histories, comparisons


def reciprocal_objective_family(players):
    topics = [frozenset(range(players))]
    topics += [frozenset([players + j]) for j in range(players - 1)]
    speeds = [len(t) for t in topics]
    rule = lambda history: 0
    histories, comparisons = check_full_spe(topics, players, rule)
    actual = finish((), players, rule)
    best_cover = 0
    best_makespan = None
    reciprocal_checks = 0
    for actions in combinations_with_replacement(range(len(topics)), players):
        counts = Counter(actions)
        makespan = max(F(counts[a], speeds[a]) for a in counts)
        best_makespan = makespan if best_makespan is None else min(best_makespan, makespan)
        best_cover = max(best_cover, coverage(topics, actions))
        for i, a in enumerate(actions):
            assert utility(topics, actions, i) * F(counts[a], speeds[a]) == 1
            reciprocal_checks += 1
    actual_cover = coverage(topics, actual)
    actual_makespan = F(players, speeds[0])
    assert actual_cover == players
    assert best_cover == 2 * players - 1
    assert actual_makespan == best_makespan == 1
    return {
        "players": players,
        "ordered_histories_checked": histories,
        "deviation_comparisons_including_self": comparisons,
        "reciprocal_checks": reciprocal_checks,
        "cag_welfare": actual_cover,
        "cag_optimum": best_cover,
        "cag_ratio": str(F(best_cover, actual_cover)),
        "scheduling_makespan": str(actual_makespan),
        "scheduling_optimum": str(best_makespan),
    }


def union_configuration_family(size):
    jobs = range(size)
    times = [[1] * size] + [[size + 1] * size for _ in range(size - 1)]
    threshold = 1
    catalogs = []
    for row in times:
        configs = set()
        for k in range(size + 1):
            for subset in combinations(jobs, k):
                if sum(row[j] for j in subset) <= threshold:
                    configs.add(frozenset(subset))
        catalogs.append(configs)
    topics = sorted(set().union(*catalogs), key=lambda s: (len(s), tuple(sorted(s))))
    assert topics == [frozenset()] + [frozenset([j]) for j in jobs]

    def rule(history):
        used = set().union(*(topics[a] for a in history))
        return next(a for a, topic in enumerate(topics) if topic and topic.isdisjoint(used))

    histories, comparisons = check_full_spe(topics, size, rule)
    actual = finish((), size, rule)
    assert coverage(topics, actual) == size
    optimum = min(
        max(sum(times[i][j] for j, a in enumerate(assignment) if a == i) for i in range(size))
        for assignment in product(range(size), repeat=size)
    )
    grouped_full_cover = any(
        len(set().union(*chosen)) == size
        for chosen in product(*(sorted(c, key=lambda s: (len(s), tuple(sorted(s)))) for c in catalogs))
    )
    assert optimum == size > threshold
    assert not grouped_full_cover
    return {
        "machines_and_jobs": size,
        "threshold": threshold,
        "union_catalog_full_spe_welfare": size,
        "union_catalog_optimum": size,
        "original_scheduling_optimum": optimum,
        "grouped_catalog_can_cover_all": grouped_full_cover,
        "ordered_histories_checked": histories,
        "deviation_comparisons_including_self": comparisons,
    }


if __name__ == "__main__":
    result = {
        "arithmetic": "fractions.Fraction; no randomization or external dependencies",
        "scope": "finite independent audits; arbitrary-parameter claims rely on the written proofs",
        "reciprocal_objective_family": [reciprocal_objective_family(m) for m in range(2, 7)],
        "union_configuration_family": [union_configuration_family(q) for q in range(2, 6)],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
