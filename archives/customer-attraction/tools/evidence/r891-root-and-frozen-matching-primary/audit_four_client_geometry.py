"""One known-input, exact unit-client check of the R891 README example.

No native matching-probe import/run, LP, BI, search, or old 52-client recheck.
The reported value 5/2 after first B corrects the README's all-2 assertion.
"""
from fractions import Fraction as F
from itertools import product, combinations, permutations
import json
from pathlib import Path
import argparse


def audit():
    labels = ["A", "B", "T", "D"]
    themes = [frozenset("xy"), frozenset("bc"),
              frozenset("xyc"), frozenset("xyb")]
    policy = {(): 0, (0,): 1, (1,): 3, (2,): 3, (3,): 2}
    histories = [()] + [(a,) for a in range(4)]
    assert set(policy) == set(histories)

    def finish(h):
        while len(h) < 2:
            h = h + (policy[h],)
        return h

    def payoff(leaf, mover):
        return sum((F(1, sum(x in themes[a] for a in leaf))
                    for x in themes[leaf[mover]]), F(0))

    def coverage(leaf):
        return len(frozenset().union(*(themes[a] for a in leaf)))

    rows = []
    strict = ties = 0
    for h in histories:
        mover = len(h)
        values = [payoff(finish(h + (a,)), mover) for a in range(4)]
        chosen = policy[h]
        assert values[chosen] == max(values)
        for a in range(4):
            if a != chosen:
                strict += values[chosen] > values[a]
                ties += values[chosen] == values[a]
        rows.append(dict(history=list(h), prescribed=chosen,
                         true_leaf_values=list(map(str, values)),
                         true_leaves=[list(finish(h + (a,))) for a in range(4)]))
    assert strict == 10 and ties == 5
    actual = finish(())
    assert actual == (0, 1)
    assert list(map(str, rows[0]["true_leaf_values"])) == ["2", "3/2", "2", "2"]
    prescribed_last = [payoff(finish((a,)), 1) for a in range(4)]
    assert prescribed_last == [F(2), F(5, 2), F(2), F(2)]
    frozen = [[payoff(tuple(a if j == i else actual[j] for j in range(2)), i)
               for a in range(4)] for i in range(2)]
    W = coverage(actual)
    optimum = max(coverage(J) for J in product(range(4), repeat=2))
    assert W == optimum == 4
    optimal = []
    for J in combinations(range(4), 2):
        if coverage(J) != optimum:
            continue
        values = [sum((frozen[i][a] for i, a in enumerate(pi)), F(0))
                  for pi in permutations(J)]
        E = len((themes[actual[0]] | themes[actual[1]]) -
                (themes[J[0]] | themes[J[1]]))
        optimal.append(dict(support=list(J), frozen_assignment_values=list(map(str, values)),
                            minimum=str(min(values)), actual_outside_comparison=E))
    assert [r["support"] for r in optimal] == [[0, 1], [1, 2], [1, 3], [2, 3]]
    assert [r["minimum"] for r in optimal] == ["2", "3", "3", "9/2"]
    assert optimal[-1]["frozen_assignment_values"] == ["9/2", "9/2"]
    return dict(scope="one README input; exact full two-player policy and all comparison supports",
                topics=labels, customers=["x", "y", "b", "c"],
                covers=[sorted(T) for T in themes],
                players=2, histories=5, comparisons_including_self=20,
                proper_comparisons=15, strict_proper=strict, tied_proper=ties,
                actual_path=list(actual), actual_payoffs=["2", "2"],
                welfare=W, optimum=optimum, all_history_rows=rows,
                prescribed_last_payoffs=list(map(str, prescribed_last)),
                README_claim_all_prescribed_last_payoffs_equal_2=False,
                corrected_B_then_D_last_payoff="5/2",
                frozen_price_rows=[list(map(str, row)) for row in frozen],
                all_optimal_distinct_supports=optimal,
                repeated_two_topic_portfolios_also_checked_in_optimum=True,
                bad_given_optimal_support=[2, 3],
                given_support_minimum_gap="1/2",
                exists_other_safe_optimal_support=True,
                original_matching_probe_runs=0, LP_runs=0, BI_runs=0,
                old_52_client_runs=0, passed=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    with args.output.open("x") as stream:
        stream.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in
                      ["passed", "histories", "comparisons_including_self",
                       "corrected_B_then_D_last_payoff", "given_support_minimum_gap"]}))
