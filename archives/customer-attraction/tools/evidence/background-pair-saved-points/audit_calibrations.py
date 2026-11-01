"""One independent audit of three NEW exact six-customer calibrations.

This does not recover historical weights or historical missing prefixes.
No original module, equilibrium solver, LP, or random search is invoked.
The historical JSON numbers are retained as lexical decimal tokens in the
reading view; their declared policies are reused only in separately defined
games with empty prefix and the integer customers specified below.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement, product
import json
from pathlib import Path


CASES = (
    ("279e0263ac887d49cc5c", 4, 7, 117, ((2, 1), (8, 1), (117, 4))),
    ("69c12c9898ca4b63b7fd", 5, 6, 61, ((2, 1), (61, 5))),
    ("f93fbed3f5d9b7b93343", 5, 7, 125, ((2, 1), (125, 5))),
)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def payoff(action, terminal, customers):
    return sum((F(mass, sum(bool(mask & (1 << b)) for b in terminal))
                for mask, mass in customers if mask & (1 << action)), F(0))


def static_payoff(action, prefix, rivals, customers):
    return payoff(action, tuple(prefix) + (action,) + tuple(rivals), customers)


def run_case(path, specification):
    source_id, n, k, big_mask, customers = specification
    before = digest(path)
    raw = json.loads(path.read_text(), parse_float=str)
    assert (raw["n"], raw["k"]) == (n, k)
    assert set(raw) == {"status", "n", "k", "seed", "completed", "elapsed", "best"}
    assert raw["status"] == "numerical screening only; no exact certificate"
    best = raw["best"]
    assert set(best) == {"gap", "weights", "p", "q", "first", "rivals", "iteration", "policy"}
    histories = tuple(h for depth in range(n) for h in product(range(k), repeat=depth))
    assert [tuple(row["history"]) for row in best["policy"]] == list(histories)
    assert all(set(row) == {"history", "action"} for row in best["policy"])
    policy = {h: row["action"] for h, row in zip(histories, best["policy"])}
    assert all(isinstance(a, int) and 0 <= a < k for a in policy.values())
    assert len(best["weights"]) == 2 ** k - 1
    assert len(best["p"]) == k
    assert best["rivals"] == [list(z) for z in combinations_with_replacement(range(k), n - 3)]
    assert len(best["q"]) == len(best["rivals"])

    # Lossless semantic reading view: a depth gives the actions in the exact
    # lexicographic product order. Decode and compare every original pair.
    by_depth = []
    for depth in range(n):
        digit_string = "".join(str(policy[h]) for h in product(range(k), repeat=depth))
        decoded = [(h, int(a)) for h, a in zip(product(range(k), repeat=depth), digit_string)]
        assert decoded == [(h, policy[h]) for h in histories if len(h) == depth]
        by_depth.append({"depth": depth, "rows": k ** depth, "actions": digit_string})
    view = {key: value for key, value in raw.items() if key != "best"}
    view["best"] = {key: value for key, value in best.items() if key != "policy"}
    view["policy_encoding"] = "At depth d, position j uses the j-th tuple of product(range(k), repeat=d); each character is its action. Float strings preserve original numeric lexemes."
    view["policy_by_depth"] = by_depth

    big_labels = tuple(a for a in range(k) if big_mask & (1 << a))
    singleton_labels = tuple(a for a in range(k) if a not in big_labels)
    assert all(a in big_labels for a in policy.values())
    assert sum(mass for _, mass in customers) == 6
    assert dict(customers)[big_mask] == n
    assert sorted(mask for mask, mass in customers if mask != big_mask) == [1 << a for a in singleton_labels]
    assert all(mass == 1 for mask, mass in customers if mask != big_mask)

    # All continuations use some big-block alias. For an arbitrary history h
    # and deviation a the mover's exact payoff can therefore be read directly:
    # n/(number of previous big actions + 1 + number of later movers), or
    # 1/(number of previous uses of that singleton + 1).
    rows_by_depth = []
    all_slacks = Counter()
    for depth in range(n):
        comparisons = strict = ties = nonself_ties = 0
        local_slacks = Counter()
        for h in product(range(k), repeat=depth):
            previous_big = sum(a in big_labels for a in h)
            chosen = F(n, previous_big + n - depth)
            assert chosen >= 1
            for action in range(k):
                alternative = chosen if action in big_labels else F(1, h.count(action) + 1)
                slack = chosen - alternative
                assert slack >= 0
                comparisons += 1
                strict += slack > 0
                ties += slack == 0
                nonself_ties += slack == 0 and action != policy[h]
                local_slacks[str(slack)] += 1
                all_slacks[str(slack)] += 1
        rows_by_depth.append(dict(depth=depth, histories=k ** depth, comparisons=comparisons,
                                  strict=strict, ties=ties, nonself_ties=nonself_ties,
                                  exact_slack_histogram=dict(sorted(local_slacks.items()))))

    root_path = ()
    while len(root_path) < n:
        root_path += (policy[root_path],)
    assert list(root_path[:2]) == best["first"]
    root_payoffs = [payoff(a, root_path, customers) for a in root_path]
    assert root_payoffs == [F(1)] * n
    root_upper_background = (big_labels[0],) * (n - 1)
    tail_upper_background = (big_labels[0],) * (n - 3)
    root_upper_values = [static_payoff(a, (), root_upper_background, customers) for a in range(k)]
    tail_upper_values = [static_payoff(a, root_path[:2], tail_upper_background, customers) for a in range(k)]
    assert root_upper_values == tail_upper_values == [F(1)] * k
    # Lower bound is analytic, not a sampled matrix claim: any big query has
    # n unit customers and at most n covering providers including fixed prefix.
    # These pure upper backgrounds make every query exactly 1, so v_root=v_tail=1.
    pair_gap = root_payoffs[0] + root_payoffs[1] + (n - 2) * F(1) - n * F(1)
    assert pair_gap == 0
    cover = sum(mass for mask, mass in customers if any(mask & (1 << a) for a in root_path))
    portfolio = (big_labels[0],) + singleton_labels
    portfolio += (big_labels[0],) * (n - len(portfolio))
    opt = sum(mass for mask, mass in customers if any(mask & (1 << a) for a in portfolio))
    assert cover == n and opt == 6

    decimal_vectors = {key: list(map(F, best[key])) for key in ("weights", "p", "q")}
    assert all(x >= 0 for key in ("p", "q") for x in decimal_vectors[key])
    assert all(a in big_labels for a, x in enumerate(decimal_vectors["p"]) if x)
    assert all(all(a in big_labels for a in B) for B, x in zip(best["rivals"], decimal_vectors["q"]) if x)
    # A new normalization of the saved decimal p/q is legal and optimal for the
    # new game by support alone. This does not certify p/q for original weights.
    normalized = {key: [str(x / sum(decimal_vectors[key])) for x in decimal_vectors[key]] for key in ("p", "q")}
    exact_weights = [F(dict(customers).get(mask, 0), 6) for mask in range(1, 2 ** k)]
    max_weight_change = max(abs(a - b) for a, b in zip(decimal_vectors["weights"], exact_weights))
    after = digest(path)
    assert before == after
    result = dict(
        source_id=source_id, bytes=path.stat().st_size, source_sha256=before,
        original_prefix_missing=True,
        original_numbers={"interpretation": "exact decimal reading only, not binary float rerun",
                          "vector_sums": {key: str(sum(value)) for key, value in decimal_vectors.items()},
                          "negative_weights": [{"mask": i + 1, "token": best["weights"][i]} for i, x in enumerate(decimal_vectors["weights"]) if x < 0],
                          "nonzero_weights": [{"mask": i + 1, "token": best["weights"][i]} for i, x in enumerate(decimal_vectors["weights"]) if x],
                          "gap_token": best["gap"]},
        new_game={"identity": "new explicit calibration, not historical recovery", "prefix": [],
                  "players": n, "topics": list(range(k)), "integer_customers": [{"mask": m, "multiplicity": c} for m, c in customers],
                  "unit_customers": 6, "big_labels": list(big_labels), "singleton_labels": list(singleton_labels),
                  "max_absolute_decimal_weight_change_to_normalized_calibration": str(max_weight_change)},
        full_policy={"histories": len(histories), "comparisons_including_self": len(histories) * k,
                     "comparisons_excluding_self": len(histories) * (k - 1), "all_chosen_actions_are_big_aliases": True,
                     "root_path": list(root_path), "root_payoffs_integer_scale": list(map(str, root_payoffs)),
                     "by_depth": rows_by_depth, "exact_slack_histogram": dict(sorted(all_slacks.items())),
                     "proof": "All future actions are big aliases at every history; chosen payoff n/(r+n-d)>=1, each singleton deviation gives 1/(past singleton uses+1)<=1; big deviations tie."},
        exact_static_certificate={"root_prefix": [], "tail_prefix": list(root_path[:2]),
                                  "lower_query": big_labels[0], "lower_bound_reason": "n big-block customers, denominator at most n against every legal opponent background",
                                  "root_upper_background": list(root_upper_background), "tail_upper_background": list(tail_upper_background),
                                  "root_upper_query_values": list(map(str, root_upper_values)), "tail_upper_query_values": list(map(str, tail_upper_values)),
                                  "root_value_integer_scale": "1", "tail_value_integer_scale": "1",
                                  "root_value_normalized": "1/6", "tail_value_normalized": "1/6",
                                  "new_normalized_saved_p": normalized["p"], "new_normalized_saved_q": normalized["q"],
                                  "new_normalized_pq_optimal_by_all_big_support": True},
        result={"PAIR_gap_integer_scale": str(pair_gap), "PAIR_gap_normalized": "0", "welfare_integer": cover,
                "OPT_integer": opt, "OPT_portfolio": list(portfolio), "welfare_over_OPT": str(F(cover, opt)),
                "full_SPE_for_new_game": True, "historical_exact_certificate": False},
        source_unchanged=True,
    )
    return result, view


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    assert len(args.source) == len(CASES)
    args.output.mkdir(parents=True, exist_ok=True)
    audited = [run_case(path, specification) for path, specification in zip(args.source, CASES)]
    report = {"status": "PASS", "scope": "one new exact empty-prefix calibration per frozen report; no claim of historical recovery",
              "original_main_calls": 0, "original_helper_calls": 0, "LP_calls": 0, "solver_calls": 0, "random_searches": 0,
              "original_tables": 3, "policy_nodes": sum(r["full_policy"]["histories"] for r, _ in audited),
              "all_action_comparisons": sum(r["full_policy"]["comparisons_including_self"] for r, _ in audited),
              "cases": [r for r, _ in audited]}
    (args.output / "exact-calibration-audit.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    (args.output / "complete-reading-view.json").write_text(json.dumps({"scope": "lossless field/action view; original bytes remain authoritative", "cases": [v for _, v in audited]}, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({key: value for key, value in report.items() if key != "cases"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
