"""Exact first-divergence portfolio check for the frozen R-275 moments."""
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, combinations_with_replacement, product
import json
from math import comb
from pathlib import Path
import sys


def audit(source):
    payload = json.loads(source.read_text())
    candidate = payload["exact_candidate"]
    players = payload["milp"]["players"]
    topic_count = payload["milp"]["topics"]
    distinguished = payload["milp"]["distinguished_topics"]
    inside = (1 << distinguished) - 1
    topics = range(topic_count)
    zero = (0,) * topic_count
    values = dict(zip(map(tuple, payload["moment_orbits"]), map(Fraction, candidate["values"])))

    def coverage(support):
        if not support:
            return Fraction()
        return values[support & inside, (support >> distinguished).bit_count()]

    def support_of_counts(counts):
        return sum(1 << a for a in topics if counts[a])

    def welfare(counts):
        return coverage(support_of_counts(counts))

    def add(counts, a):
        return counts[:a] + (counts[a] + 1,) + counts[a + 1:]

    def counts(history):
        return tuple(history.count(a) for a in topics)

    @lru_cache(None)
    def utility(terminal, action):
        others = tuple(a for a in topics for _ in range(terminal[a] - int(a == action)))
        assert len(others) == players - 1
        result = Fraction()
        for length in range(players):
            for preceding in combinations(range(players - 1), length):
                support = sum(1 << a for a in {others[i] for i in preceding})
                marginal = coverage(support | (1 << action)) - coverage(support)
                result += marginal / (players * comb(players - 1, length))
        return result

    @lru_cache(None)
    def credible(k):
        if sum(k) == players:
            return frozenset((k,))
        alternatives = {a: credible(add(k, a)) for a in topics}
        floor = max(min(utility(t, a) for t in alternatives[a]) for a in topics)
        return frozenset(t for a in topics for t in alternatives[a] if utility(t, a) >= floor)

    @lru_cache(None)
    def minimum(k, a):
        return min(utility(t, a) for t in credible(add(k, a)))

    def admits(path):
        terminal = counts(path)
        k = zero
        for a in path:
            if terminal not in credible(add(k, a)):
                return False
            if utility(terminal, a) < max(minimum(k, b) for b in topics):
                return False
            k = add(k, a)
        return True

    def matrix(path):
        terminal = counts(path)
        k = zero
        result = []
        for a in path:
            result.append(tuple(utility(terminal, a) if b == a else minimum(k, b) for b in topics))
            k = add(k, a)
        return tuple(result)

    actions = {tuple(row["history"]): row["action"] for row in candidate["complete_strategy"]["actions"]}

    def finish(history, policy):
        while len(history) < players:
            history += (policy[history],)
        return history

    path = tuple(payload["milp"]["path"])
    assert finish((), actions) == path

    def fixed_matrix(policy):
        return tuple(tuple(utility(counts(finish(path[:i] + (b,), policy)), b) for b in topics)
                     for i in range(players))

    assert admits(path)
    original = fixed_matrix(actions)
    minimizing = matrix(path)
    assert all(x >= y for row_a, row_b in zip(original, minimizing) for x, y in zip(row_a, row_b))
    chosen = tuple(payload["milp"]["portfolio"])
    allowed = tuple(combinations_with_replacement(topics, players))
    optimum = max(welfare(counts(t)) for t in allowed)
    optimal = tuple(t for t in allowed if welfare(counts(t)) == optimum)

    def query(mat, portfolio):
        return sum(row[a] for row in mat for a in portfolio)

    def slack(p, q, mat):
        return (players - 1) * welfare(counts(p)) + query(mat, q) - players * welfare(counts(q))

    paths = [p for p in product(topics, repeat=players) if admits(p)]
    assert {counts(p) for p in paths} == credible(zero)
    min_all = min((slack(p, q, mat), p, q, query(mat, q))
                  for p in paths for mat in [matrix(p)] for q in allowed)
    min_opt = min((slack(p, q, mat), p, q, query(mat, q))
                  for p in paths for mat in [matrix(p)] for q in optimal)

    # Independently construct and definition-audit one complete strategy for the
    # global UP-minimizing path, choosing each child's least entering-player payoff.
    minimizing_path = min_all[1]
    glued = {}

    def expand(h, k, t):
        if len(h) == players:
            assert k == t
            return
        floor = max(minimum(k, b) for b in topics)
        possible = tuple(a for a in topics if t in credible(add(k, a)) and utility(t, a) >= floor)
        a = minimizing_path[len(h)] if h == minimizing_path[:len(h)] else possible[0]
        assert a in possible
        glued[h] = a
        for b in topics:
            child = add(k, b)
            selected = t if b == a else min(credible(child), key=lambda u: (utility(u, b), u))
            expand(h + (b,), child, selected)

    expand((), zero, counts(minimizing_path))
    assert len(glued) == sum(topic_count ** i for i in range(players))
    assert finish((), glued) == minimizing_path
    total_comparisons = 0
    for h, a in glued.items():
        own = utility(counts(finish(h + (a,), glued)), a)
        for b in topics:
            if b != a:
                assert own >= utility(counts(finish(h + (b,), glued)), b)
                total_comparisons += 1
    assert matrix(minimizing_path) == tuple(
        tuple(utility(counts(finish(minimizing_path[:i] + (b,), glued)), b) for b in topics)
        for i in range(players))

    return {
        "source": source.name,
        "root_paths": len(paths),
        "root_counts": len(credible(zero)),
        "least_SPE_W": min(map(welfare, credible(zero))),
        "best_SPE_W": max(map(welfare, credible(zero))),
        "comparison_multisets": len(allowed),
        "optimal_comparison_multisets": len(optimal),
        "OPT": optimum,
        "frozen_original_path": path,
        "frozen_comparison": chosen,
        "frozen_actual_matrix": original,
        "same_path_minimal_matrix": minimizing,
        "frozen_UP_D": slack(path, chosen, original),
        "same_path_minimal_UP_D": slack(path, chosen, minimizing),
        "all_paths_all_portfolios_minimum_slack_path_portfolio_query": min_all,
        "all_paths_optimal_portfolios_minimum_slack_path_portfolio_query": min_opt,
        "minimizer_glued_histories": len(glued),
        "minimizer_glued_deviations": total_comparisons,
    }


if __name__ == "__main__":
    print(json.dumps([audit(Path(source)) for source in sys.argv[1:]], indent=2, default=str))
