"""Known-input exact audit of the separate four-customer table in the review.

This does not import the author's eight-customer audit or a game solver.
Labels below are 0..3, obtained by subtracting one from the review's 1..4.
Only this fixed complete policy is checked; no search or general-SPE claim.
"""
from fractions import Fraction as F
from itertools import product
import json

TOPICS = (frozenset("ab"), frozenset("bc"),
          frozenset("ad"), frozenset("cd"))
SECOND = (1, 0, 0, 1)
LAST = ((3, 2, 3, 3), (3, 2, 2, 2),
        (3, 1, 1, 1), (0, 2, 0, 0))


def action(history):
    if not history:
        return 0
    if len(history) == 1:
        return SECOND[history[0]]
    return LAST[history[0]][history[1]]


def finish(history):
    history = tuple(history)
    while len(history) < 3:
        history += (action(history),)
    return history


def utility(leaf, role):
    return sum((F(1, sum(x in TOPICS[a] for a in leaf))
                for x in TOPICS[leaf[role]]), F(0))


def main():
    rows = []
    strict = ties = 0
    for depth in range(3):
        for history in product(range(4), repeat=depth):
            chosen = action(history)
            leaf = finish(history)
            incumbent = utility(leaf, depth)
            queried = [utility(finish(history + (a,)), depth) for a in range(4)]
            assert queried[chosen] == incumbent
            assert all(incumbent >= x for x in queried)
            for a, x in enumerate(queried):
                if a != chosen:
                    strict += incumbent > x
                    ties += incumbent == x
            rows.append({"history": history, "action": chosen,
                         "actual_completion": leaf,
                         "forced_current_payoffs": list(map(str, queried))})
    assert len(rows) == 21 and strict + ties == 63
    branches = [finish((a,)) for a in range(4)]
    assert branches == [(0, 1, 2), (1, 0, 3), (2, 0, 3), (3, 1, 2)]
    payoffs = [[utility(z, i) for i in range(3)] for z in branches]
    assert all(v == [F(1), F(3, 2), F(3, 2)] for v in payoffs)
    root_to_tail = [[F(z[1:].count(a), 2) for a in range(4)] for z in branches]
    pi = [F(1, 4)] * 4
    pushed = [sum(pi[i] * root_to_tail[i][j] for i in range(4)) for j in range(4)]
    assert pushed == pi
    client_rows = []
    for x in "abcd":
        indicators = [int(x in TOPICS[a]) for a in range(4)]
        loads = [sum(x in TOPICS[a] for a in z[1:]) for z in branches]
        d = sum(pi[i] * F(indicators[i], indicators[i] + loads[i]) for i in range(4))
        p = sum(pi[i] * F(indicators[i] + loads[i], indicators[i] + loads[i]) for i in range(4))
        s = 2 * sum(pi[i] * indicators[i] for i in range(4)) - sum(pi[i] * loads[i] for i in range(4))
        assert loads == [1] * 4 and (d, p, s) == (F(1, 4), F(1), F(0))
        client_rows.append({"client": x, "root_membership": indicators,
                            "tail_loads": loads, "D": str(d), "P": str(p), "S": str(s)})
    static_rows = []
    for history in product(range(4), repeat=2):
        values = [utility(history + (a,), 2) for a in range(4)]
        static_rows.append({"competitor_pair": history,
                            "query_values": list(map(str, values)),
                            "maximum": str(max(values))})
    theta = min(F(r["maximum"]) for r in static_rows)
    actual = finish(())
    w = len(set().union(*(TOPICS[a] for a in actual)))
    optimum = max(len(set().union(*(TOPICS[a] for a in z)))
                  for z in product(range(4), repeat=3))
    assert (theta, w, optimum) == (F(1), 4, 4)
    result = {"scope": "one fixed four-unit-customer complete policy from the original review; known-input reconstruction",
              "source_sha256": "c5a0fd96f1586f597569d176281fa5e8a1915ac48626ff93201db5c5f81c0d33",
              "labels": "0..3 equals original review 1..4 minus one",
              "topics": [sorted(a) for a in TOPICS], "second": SECOND, "last": LAST,
              "histories": len(rows), "comparisons_including_self": 84,
              "comparisons_nonself": strict + ties, "strict_nonself": strict, "tied_nonself": ties,
              "all_ordered_history_rows": rows,
              "root_branches": branches, "root_branch_payoffs": [[str(x) for x in v] for v in payoffs],
              "root_to_tail_kernel_row_convention": [[str(x) for x in row] for row in root_to_tail],
              "pi": list(map(str, pi)), "pi_times_kernel": list(map(str, pushed)),
              "client_stationarity_rows": client_rows,
              "static_competitor_pair_rows": static_rows,
              "theta_3": str(theta), "actual": actual, "W": w, "OPT_3": optimum,
              "original_author_entry_imports": 0, "LP_MILP_BI_or_random_calls": 0}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
