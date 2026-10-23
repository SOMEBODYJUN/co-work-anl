"""Exact audit of the all-population no-union-deletion family."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement
from pathlib import Path
import json


def comps(k, n):
    for history in combinations_with_replacement(range(k), n):
        yield tuple(history.count(i) for i in range(k))


def audit(m, t=2, d=1):
    L = d + (m + 1) * t // 2
    T = m

    def utility(a, terminal):
        if a == T:
            return F(d, terminal[T]) + sum((F(t, terminal[i] + terminal[T]) for i in range(m)), F(0))
        return F(L - t, terminal[a]) + F(t, terminal[a] + terminal[T])

    def welfare(terminal):
        return sum(L - t for i in range(m) if terminal[i]) + sum(
            t for i in range(m) if terminal[i] or terminal[T]) + (d if terminal[T] else 0)

    records = {}

    @lru_cache(None)
    def solve(prefix):
        if sum(prefix) == m:
            return prefix
        children = []
        values = []
        for a in range(m + 1):
            child = list(prefix)
            child[a] += 1
            terminal = solve(tuple(child))
            children.append(terminal)
            values.append(utility(a, terminal))
        if prefix[T] or max(prefix[:m], default=0) <= 1:
            chosen = next(i for i in range(m) if prefix[i] == 0)
        else:
            chosen = max(range(m + 1), key=lambda a: (values[a], -a))
        assert values[chosen] == max(values), (m, prefix, chosen, values)
        records[prefix] = (chosen, children[chosen], values)
        return children[chosen]

    root = solve((0,) * (m + 1))
    assert root == (1,) * m + (0,)
    assert welfare(root) == m * L
    assert max(welfare(q) for q in comps(m + 1, m)) == m * L
    less_population_checks = 0
    minimum_gaps = {}
    for s in range(1, m):
        gaps = []
        for blocks in comps(m, s - 1):
            t_query = F(d) + sum((F(t, 1 + c) for c in blocks), F(0))
            assert t_query >= L + F((m - s) * t, 2) > L
            gaps.append(t_query - L)
            less_population_checks += 1
        minimum_gaps[str(s)] = str(min(gaps))
    return {
        "players": m, "block_size": L, "marked_per_block": t,
        "T_private": d, "customer_count": m * L + d,
        "terminal": list(root), "welfare_and_OPT": m * L,
        "decision_count_states": len(records),
        "all_action_comparisons": len(records) * (m + 1),
        "smaller_population_prefix_checks": less_population_checks,
        "minimum_T_deviation_gaps": minimum_gaps,
    }


report = {"status": "exact audit passed; deletion closure false, half not refuted",
          "cases": [audit(m) for m in range(2, 7)]}
print(json.dumps(report, ensure_ascii=False, indent=2))
Path(__file__).with_name("population_deletion_audit.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + "\n")
