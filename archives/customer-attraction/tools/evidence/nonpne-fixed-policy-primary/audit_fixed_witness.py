"""Exact definition-level audit of one saved non-PNE full-history witness.

Standard library only. No author module, canonical solver, LP, or random search.
Integer customer multiplicity means that many distinct unit customers.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from functools import lru_cache
import hashlib
import itertools
import json
from math import lcm
from pathlib import Path


def audit(path: Path) -> dict:
    raw = path.read_bytes()
    data = json.loads(raw)
    model = data["instance"]
    n, k = model["players"], len(model["topics"])
    assert n == 5 and k == 7
    types = []
    for row in model["customers"]:
        interest = frozenset(row["topics"])
        count = row.get("multiplicity", 1)
        assert interest and all(type(a) is int and 0 <= a < k for a in interest)
        assert type(count) is int and count > 0
        types.append((interest, count))
    actions = data["strategy"]["actions"]
    policy = {tuple(row["history"]): row["action"] for row in actions}
    histories = [h for depth in range(n)
                 for h in itertools.product(range(k), repeat=depth)]
    assert len(policy) == len(actions) and set(policy) == set(histories)
    assert all(type(a) is int and 0 <= a < k for a in policy.values())
    scale = lcm(*range(1, n + 1))

    @lru_cache(None)
    def finish(history):
        if len(history) == n:
            return history
        return finish(history + (policy[history],))

    @lru_cache(None)
    def payoff_scaled(action, leaf):
        return sum(count * (scale // sum(a in interest for a in leaf))
                   for interest, count in types if action in interest)

    def welfare(leaf):
        return sum(count for interest, count in types
                   if any(a in interest for a in leaf))

    rows, payloads, depth_indexes = [], [], [[] for _ in range(n)]
    nonself_min = None
    strict = ties = 0
    by_depth = []
    for depth in range(n):
        local_min = None
        local_strict = local_ties = 0
        for h in itertools.product(range(k), repeat=depth):
            chosen = policy[h]
            values = [payoff_scaled(a, finish(h + (a,))) for a in range(k)]
            assert values[chosen] == max(values), (h, chosen, values)
            payload = [chosen, values]
            if payload not in payloads:
                payloads.append(payload)
            depth_indexes[depth].append(payloads.index(payload))
            for a, value in enumerate(values):
                if a == chosen:
                    continue
                diff = values[chosen] - value
                local_min = diff if local_min is None else min(local_min, diff)
                local_strict += diff > 0
                local_ties += diff == 0
        nonself_min = local_min if nonself_min is None else min(nonself_min, local_min)
        strict += local_strict
        ties += local_ties
        by_depth.append(dict(depth=depth, histories=k**depth,
                             nonself_comparisons=(k - 1) * k**depth,
                             minimum_nonself_slack=str(Fraction(local_min, scale)),
                             strictly_positive=local_strict, ties=local_ties))
    leaf = finish(())
    counts = [leaf.count(a) for a in range(k)]
    assert counts == data["strategy"]["terminal_counts"]
    W = welfare(leaf)
    payoffs = [Fraction(payoff_scaled(a, leaf), scale) for a in leaf]
    assert sum(payoffs) == W
    portfolios = []
    for support in itertools.combinations(range(k), min(n, k)):
        portfolios.append(dict(support=list(support), welfare=welfare(support)))
    optimum = max(row["welfare"] for row in portfolios)
    assert str(Fraction(optimum, W)) == data["ratio"]
    old, new = data["nonpne_deviation"]
    assert old in leaf and new != old
    index = leaf.index(old)
    deviated = leaf[:index] + (new,) + leaf[index+1:]
    static_old = Fraction(payoff_scaled(old, leaf), scale)
    static_new = Fraction(payoff_scaled(new, deviated), scale)
    gain = static_new - static_old
    denominator = data["parameters"]["gap_denominator"]
    assert gain > 0 and denominator * gain >= W
    actual_history = leaf[:index]
    true_leaf = finish(actual_history + (new,))
    true_new = Fraction(payoff_scaled(new, true_leaf), scale)
    assert true_new <= static_old
    # Complete exact row data in depth/lex order, deduplicated without losing values.
    ic = dict(scale=scale, labels=list(range(k)), order="depth then lexicographic history",
              payload_format="[prescribed_action, list_of_all_k_true_continuation_payoffs_times_scale]",
              payloads=payloads, payload_indexes_by_depth=depth_indexes)
    ic_bytes = json.dumps(ic, separators=(",", ":")).encode()
    output = dict(input_sha256=hashlib.sha256(raw).hexdigest(),
                  scope="one saved fixed full-history policy; exact integer arithmetic",
                  players=n, topics=k, unit_customers=sum(c for _, c in types),
                  interest_types=len(types), histories=len(histories),
                  comparisons_including_self=k*len(histories),
                  nonself_comparisons=(k-1)*len(histories),
                  strictly_positive_nonself=strict, tied_nonself=ties,
                  minimum_nonself_slack=str(Fraction(nonself_min, scale)),
                  per_depth=by_depth, actual_leaf=list(leaf), terminal_counts=counts,
                  actual_payoffs=list(map(str, payoffs)), W=W, OPT=optimum,
                  exact_ratio=str(Fraction(optimum, W)),
                  half_margin=2*W-optimum, all_five_label_supports=portfolios,
                  static_deviation=dict(old_action=old, new_action=new,
                                        affected_player_zero_based=index,
                                        frozen_other_actions_leaf=list(deviated),
                                        old_payoff=str(static_old), new_payoff=str(static_new),
                                        gain=str(gain), gain_over_W=str(gain/W),
                                        required_gain=str(Fraction(W, denominator))),
                  true_sequential_deviation=dict(history=list(actual_history),
                                                new_leaf=list(true_leaf),
                                                deviator_payoff=str(true_new)),
                  passed=True, original_imports=0, solver_runs=0, LP_runs=0,
                  random_search_runs=0, exact_ic_data_sha256=hashlib.sha256(ic_bytes).hexdigest())
    return output, ic


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ic-output", type=Path, required=True)
    args = parser.parse_args()
    result, ic = audit(args.input)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    args.ic_output.write_text(json.dumps(ic, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ["passed", "histories", "nonself_comparisons",
                                            "actual_leaf", "W", "OPT", "exact_ratio",
                                            "static_deviation", "true_sequential_deviation"]},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
