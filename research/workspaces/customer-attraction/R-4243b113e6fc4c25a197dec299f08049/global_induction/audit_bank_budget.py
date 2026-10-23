#!/usr/bin/env python3
"""Self-contained exact finite replay of the joint-deviation bank budgets.

The general proof is in bank_joint_deviation_budget.md. This script builds a
complete ordered-history SPE separately in each finite game, with independently
chosen ties at every ordered node. It does not impose componentwise policies.
"""

from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import json
from pathlib import Path
import random


SEED = 42431023
RNG = random.Random(SEED)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def catalog(customer_count, desired_topics):
    topics = []
    while len(topics) < desired_topics:
        topic = frozenset(x for x in range(customer_count) if RNG.randrange(2))
        if topic not in topics:
            topics.append(topic)
    return tuple(topics)


def run_case(m, main, bank, label):
    topics = tuple(product(range(len(main)), range(len(bank))))
    policy, outcomes = {}, {}

    @lru_cache(None)
    def utilities(profile):
        result = []
        for coordinate, sets in ((0, main), (1, bank)):
            counts = {}
            for action in profile:
                for x in sets[action[coordinate]]:
                    counts[x] = counts.get(x, 0) + 1
            result.append(tuple(sum((F(1, counts[x])
                                     for x in sets[action[coordinate]]), F(0))
                                for action in profile))
        return tuple(result)

    def build(history):
        if len(history) == m:
            outcomes[history] = history
            return history
        children = [(a, build(history + (a,))) for a in topics]
        i = len(history)
        best = max(sum(utilities(leaf)[c][i] for c in (0, 1))
                   for _, leaf in children)
        tied = [(a, leaf) for a, leaf in children
                if sum(utilities(leaf)[c][i] for c in (0, 1)) == best]
        action, leaf = RNG.choice(tied)
        policy[history], outcomes[history] = action, leaf
        return leaf

    actual = build(())
    comparisons = 0
    for history, action in policy.items():
        i = len(history)
        follow = utilities(outcomes[history])
        for alternative in topics:
            deviation = utilities(outcomes[history + (alternative,)])
            require(follow[0][i] + follow[1][i] >=
                    deviation[0][i] + deviation[1][i], "full SPE edge")
            comparisons += 1

    actual_u = utilities(actual)
    covered = frozenset().union(*(bank[b] for _, b in actual))
    wb = F(len(covered))
    bank_max = max(bank, key=len)
    largest = len(bank_max)
    require(wb >= largest, "last bank best response gives W_B >= L")
    rs, ks, kappas, ds, rhos, fs = [], [], [], [], [], []
    point_rows = []
    for i, (actual_a, actual_b) in enumerate(actual):
        history = actual[:i]
        remaining = m - i
        previous = {x: sum(x in bank[b] for _, b in history)
                    for x in frozenset().union(*bank)}
        g = [sum((F(1, previous[x] + remaining) for x in b), F(0))
             for b in bank]
        k = max(g)
        values = [[utilities(outcomes[history + ((a, b),)])[0][i]
                   for b in range(len(bank))]
                  for a in range(len(main))]
        um, ub = actual_u[0][i], actual_u[1][i]
        r = max(min(row) for row in values) - um
        kappa = um - min(values[actual_a])
        best_main = max(row[actual_b] for row in values)
        d = best_main - um
        rho = min(row[actual_b] - min(row) for row in values
                  if row[actual_b] == best_main)
        f = g[actual_b]
        require(k >= F(largest, m), "K_i >= L/m")
        require(r <= ub - k, "signed node budget")
        require(kappa >= 0 and r >= -kappa, "kappa lower bound")
        require(d >= 0 and rho >= 0, "nonnegative d/rho")
        require(d <= ub - k + rho, "d/rho node budget")
        require(d <= ub - f and ub >= f, "fixed-current-bank node budget")
        rs.append(r); ks.append(k); kappas.append(kappa)
        ds.append(d); rhos.append(rho); fs.append(f)
        point_rows.append({"R": str(r), "K": str(k), "kappa": str(kappa),
                           "d": str(d), "rho": str(rho), "f": str(f)})

    require(sum(rs) <= wb - sum(ks), "signed sum budget")
    require(sum(max(r, F(0)) for r in rs) <=
            wb - sum(ks) + sum(kappas), "kappa positive-part budget")
    require(sum(ds) <= wb - sum(ks) + sum(rhos), "d/rho sum budget")
    require(sum(ds) <= wb - sum(fs), "fixed-bank sum budget")

    omega = F(0)
    omission_lower_bound = F(0)
    for x in bank_max:
        for i in range(m):
            omitted = sum(x not in bank[b] for _, b in actual[:i])
            omega += F(1, m - omitted) - F(1, m)
    for j, (_, b) in enumerate(actual[:-1], start=1):
        omission_lower_bound += F((m-j) * len(bank_max - bank[b]), m*m)
    require(sum(ks) >= largest + omega, "Omega floor strengthening")
    require(omega >= omission_lower_bound, "Omega omission lower bound")

    spectral = F(0)
    total_incidence = 0
    for x in covered:
        indices = [i for i, (_, b) in enumerate(actual, start=1) if x in bank[b]]
        c = len(indices)
        floor_sum = sum((F(1, m-i+t) for t, i in enumerate(indices, start=1)), F(0))
        residual = 1-floor_sum
        require(0 <= residual <= 1-F(c, m), "customer spectral interval")
        require((residual == 0) == (indices == list(range(m-c+1, m+1))),
                "zero spectral residual iff final suffix")
        spectral += residual
        total_incidence += c
    require(spectral == wb - sum(fs), "exact spectral identity")
    nested = all(bank[actual[i][1]] <= bank[actual[i+1][1]] for i in range(m-1))
    require((spectral == 0) == nested, "zero capacity iff increasing nesting")
    require(spectral <= wb - F(total_incidence, m) <= (1-F(1, m))*wb,
            "global spectral capacity bounds")
    if nested:
        require(all(d == 0 for d in ds), "nested bank cannot insure main regret")

    # Build every mapped main history from the prescribed current bank action.
    mapped, extracted = {}, {}
    saturation = True

    def map_histories(main_history, joint_history):
        nonlocal saturation
        mapped[main_history] = joint_history
        if len(main_history) == m:
            return
        a, b = policy[joint_history]
        extracted[main_history] = a
        continuation = outcomes[joint_history]
        for _, later_b in continuation[len(main_history)+1:]:
            saturation = saturation and bank[b] <= bank[later_b]
        for alternative_a in range(len(main)):
            map_histories(main_history + (alternative_a,),
                          joint_history + ((alternative_a, b),))

    map_histories((), ())
    projection_edges = 0
    if saturation:
        @lru_cache(None)
        def main_outcome(history):
            if len(history) == m:
                return history
            return main_outcome(history + (extracted[history],))

        @lru_cache(None)
        def main_utilities(profile):
            counts = {}
            for a in profile:
                for x in main[a]:
                    counts[x] = counts.get(x, 0) + 1
            return tuple(sum((F(1, counts[x]) for x in main[a]), F(0)) for a in profile)

        for history in extracted:
            i = len(history)
            own = main_utilities(main_outcome(history))[i]
            for alternative_a in range(len(main)):
                dev = main_utilities(main_outcome(history + (alternative_a,)))[i]
                require(own >= dev, "saturated-bank extracted complete main SPE")
                projection_edges += 1

    return {"label": label, "m": m, "topics": [len(main), len(bank)],
            "main_catalog": [sorted(a) for a in main],
            "bank_catalog": [sorted(b) for b in bank],
            "complete_decision_nodes": len(policy), "SPE_comparisons": comparisons,
            "actual": actual, "W_B": str(wb), "L": largest,
            "sum_R": str(sum(rs)), "sum_K": str(sum(ks)),
            "sum_kappa": str(sum(kappas)), "sum_d": str(sum(ds)),
            "sum_rho": str(sum(rhos)), "bank_capacity": str(spectral),
            "Omega": str(omega), "nested": nested,
            "projection_condition": saturation, "projection_edges": projection_edges,
            "rows": point_rows}


def main():
    cases = []
    for m in range(1, 5):
        for trial in range(8):
            cases.append(run_case(m, catalog(6, 3), catalog(5, 3),
                                  f"random-m{m}-{trial}"))
    # Explicit saturated-bank inputs make the all-history projection check
    # nonvacuous independently of whether random product policies saturate.
    for m in range(1, 5):
        cases.append(run_case(m, catalog(7, 3), (frozenset(range(5)),),
                              f"single-bank-topic-m{m}"))
    # Empty bank is also within the stated model.
    cases.append(run_case(3, catalog(6, 3), (frozenset(),), "empty-bank"))
    result = {
        "status": "exact_finite_audit_passed",
        "seed": SEED,
        "case_count": len(cases),
        "complete_decision_nodes": sum(c["complete_decision_nodes"] for c in cases),
        "SPE_comparisons": sum(c["SPE_comparisons"] for c in cases),
        "saturated_projection_cases": sum(c["projection_condition"] for c in cases),
        "projection_comparisons": sum(c["projection_edges"] for c in cases),
        "negative_R_cases": sum(any(F(r["R"]) < 0 for r in c["rows"]) for c in cases),
        "positive_d_cases": sum(F(c["sum_d"]) > 0 for c in cases),
        "scope": "Finite implementation audit only; universal proof is in the companion note.",
        "cases": cases,
    }
    path = Path(__file__).with_name("bank_budget_audit.json")
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "cases"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
