"""One fixed-input exact audit of saved share points and their supplied seed vectors.

No original module, canonical solver/verifier, LP, MILP, or random search.
All customer multiplicities are counts of distinct unit customers.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from functools import lru_cache
import hashlib
from itertools import combinations, product
import json
from math import lcm
from pathlib import Path


FILES = ["last_share_m3p5.json", "last_share_m3p7.json", "last_share_m4p6.json",
         "last_share_m5p7.json", "compiler_last_share_m3p6.json", "joint_share_m3p5.json"]


def evaluate(model, strategy):
    n, k = model["players"], len(model["topics"])
    assert 2 <= n <= 5 and 3 <= k <= 7
    types = []
    for customer in model["customers"]:
        mask = sum(1 << a for a in customer["topics"])
        count = customer.get("multiplicity", 1)
        assert type(count) is int and count > 0 and 0 < mask < 1 << k
        assert len(set(customer["topics"])) == len(customer["topics"])
        types.append((mask, count))
    actions = strategy["actions"]
    policy = {tuple(row["history"]): row["action"] for row in actions}
    histories = [h for depth in range(n) for h in product(range(k), repeat=depth)]
    assert len(policy) == len(actions) and set(policy) == set(histories)
    assert all(type(a) is int and 0 <= a < k for a in policy.values())
    scale = lcm(*range(1, n + 1))

    @lru_cache(None)
    def finish(h):
        return h if len(h) == n else finish(h + (policy[h],))

    @lru_cache(None)
    def utility(action, counts):
        return sum(count * (scale // sum(counts[a] for a in range(k) if mask >> a & 1))
                   for mask, count in types if mask >> action & 1)

    def counts(leaf):
        return tuple(leaf.count(a) for a in range(k))

    def welfare(leaf):
        return sum(count for mask, count in types if any(mask >> a & 1 for a in leaf))

    payloads, indexes = [], [[] for _ in range(n)]
    strict = ties = 0
    minimum = None
    for h in histories:
        chosen = policy[h]
        values = [utility(a, counts(finish(h + (a,)))) for a in range(k)]
        assert values[chosen] == max(values), (h, chosen, values)
        payload = [chosen, values]
        if payload not in payloads:
            payloads.append(payload)
        indexes[len(h)].append(payloads.index(payload))
        for a in range(k):
            if a == chosen:
                continue
            gap = values[chosen] - values[a]
            minimum = gap if minimum is None else min(minimum, gap)
            strict += gap > 0
            ties += gap == 0
    leaf = finish(())
    root = counts(leaf)
    assert list(root) == strategy["terminal_counts"]
    payoffs = [F(utility(a, root), scale) for a in leaf]
    W = welfare(leaf)
    assert W > 0 and sum(payoffs) == W
    portfolios = [(J, welfare(J)) for J in combinations(range(k), min(k, n))]
    optimum = max(value for J, value in portfolios)
    classes = {}
    for a in range(k):
        classes.setdefault(tuple(bool(mask >> a & 1) for mask, _ in types), []).append(a)
    result = dict(players=n, topics=k, customers=sum(count for _, count in types),
                  positive_types=len(types), histories=len(histories),
                  nonself_comparisons=(k-1)*len(histories),
                  comparisons_including_self=k*len(histories),
                  strict_nonself=strict, tied_nonself=ties,
                  minimum_nonself_slack=str(F(minimum, scale)),
                  actual_path=list(leaf), terminal_counts=list(root),
                  payoffs=list(map(str, payoffs)), welfare=W, optimum=optimum,
                  any_player_share=str(max(payoffs)/W), last_share=str(payoffs[-1]/W),
                  half_margin=2*W-optimum,
                  coverage_label_classes=list(classes.values()),
                  empty_topic_labels=[a for a in range(k)
                                      if not any(mask >> a & 1 for mask, _ in types)],
                  maximizing_portfolios=[list(J) for J, value in portfolios if value == optimum],
                  all_portfolio_values=[dict(support=list(J), welfare=value) for J, value in portfolios],
                  passed=True)
    ic = dict(scale=scale, order="depth then lexicographic history",
              payload_format="[prescribed_action, all_k_true_continuation_payoffs_times_scale]",
              payloads=payloads, payload_indexes_by_depth=indexes)
    return result, ic, policy, finish, types


def one_row_certificate(model, strategy, result, policy, finish, types):
    n, k = model["players"], len(model["topics"])
    actual = finish(())
    forced = finish((1,))
    assert actual == (0,)*(n-1) + (1,)
    assert forced.count(0) == n-2 and forced.count(1) == 2
    assert set(forced) <= {0, 1}
    beta, mu, coefficient = F(2, n+1), F(2*(n-1), n+1), F(n-1, n*(n+1))
    # Verify the explicit coefficient identity on every nonempty interest type.
    for mask in range(1, 1 << k):
        A, B = bool(mask & 1), bool(mask & 2)
        c = F(A or B)
        uA = F(1, n-1) if A and not B else F(1, n) if A else F(0)
        forcedB = F(1, 2) if B and not A else F(1, n) if B else F(0)
        uB = F(1) if B and not A else F(1, n) if B else F(0)
        assert beta*c - uB == mu*(uA-forcedB) + coefficient*int(A and B)
    intersection = sum(count for mask, count in types if mask & 1 and mask & 2)
    x = sum(count for mask, count in types if mask & 1 and not mask & 2)
    y = sum(count for mask, count in types if mask & 2 and not mask & 1)
    gamma = F(x, n-1) - F(y, 2)
    assert gamma >= 0 and intersection == 0 and gamma == 0
    assert F(result["last_share"]) == beta
    assert F(result["any_player_share"]) == beta
    return dict(actual_path=list(actual), forced_root_B_real_path=list(forced),
                forced_root_B_counts=[forced.count(a) for a in range(k)],
                beta=str(beta), root_IC_multiplier=str(mu),
                overlap_residual_coefficient=str(coefficient),
                exact_root_IC_slack=str(gamma), intersection_customers=intersection,
                all_interest_type_coefficients_checked=(1 << k)-1,
                fixed_policy_sharp_last_and_any_share=True,
                proof_scope="all nonnegative masses preserving this same policy, not all SPE policies")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ic-output", type=Path, required=True)
    args = parser.parse_args()
    cases, source_cases, ic_values, one_rows = [], [], {}, []
    for filename in FILES:
        raw = (args.input_dir / filename).read_bytes()
        data = json.loads(raw)
        records = (data["improvements"] if "improvements" in data else
                   [row["exact_cone_optimization"] for row in data["records"]])
        for i, record in enumerate(records):
            name = filename + ":" + str(i)
            result, ic, policy, finish, types = evaluate(record["instance"], record["strategy"])
            assert result["actual_path"] == record["path"]
            assert result["payoffs"] == record["payoffs"]
            assert result["welfare"] == record["welfare"]
            assert result["optimum"] == record["optimum"]
            assert result["histories"] == record["checked_histories"]
            assert result["nonself_comparisons"] == record["checked_deviations"]
            root = result["terminal_counts"]
            action = record["objective_action"]
            assert root[action] > 0
            mover = result["actual_path"].index(action)
            assert F(result["payoffs"][mover])/result["welfare"] == F(record["value"])
            result.update(name=name, input_sha256=hashlib.sha256(raw).hexdigest(),
                          objective_action=action, source_value=record["value"],
                          reported_exact_dual_bound=record["exact_dual_bound"],
                          original_dual_multipliers_present=False)
            cases.append(result)
            ic_values[name] = ic
            if "source_clones" in record:
                cert = one_row_certificate(record["instance"], record["strategy"],
                                           result, policy, finish, types)
                cert["name"] = name
                one_rows.append(cert)
                clones = record["source_clones"]
                assert len(clones) == (1 << len(record["instance"]["topics"]))-1
                seed_model = dict(topics=record["instance"]["topics"],
                                  players=record["instance"]["players"],
                                  customers=[dict(topics=[a for a in range(len(record["instance"]["topics"]))
                                                         if mask >> a & 1], multiplicity=count)
                                             for mask, count in enumerate(clones, 1) if count])
                seed, seed_ic, *_ = evaluate(seed_model, record["strategy"])
                seed["name"] = name + ":source_clones"
                source_cases.append(seed)
                ic_values[seed["name"]] = seed_ic
    result = dict(scope="fixed saved points and supplied seeds only; exact integer full-history arithmetic",
                  saved_points=cases, source_seed_checks=source_cases,
                  analytic_one_root_IC_certificates=one_rows,
                  saved_point_count=len(cases), source_seed_count=len(source_cases),
                  checked_histories=sum(c["histories"] for c in cases+source_cases),
                  checked_nonself_comparisons=sum(c["nonself_comparisons"] for c in cases+source_cases),
                  original_imports=0, original_program_runs=0, LP_runs=0, MILP_runs=0,
                  BI_runs=0, random_search_runs=0, fixed_input_audit_invocations=1, passed=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
    args.ic_output.write_text(json.dumps(ic_values, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps({key: result[key] for key in ["passed", "saved_point_count", "source_seed_count",
                                                  "checked_histories", "checked_nonself_comparisons",
                                                  "LP_runs", "MILP_runs", "BI_runs", "random_search_runs"]},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
