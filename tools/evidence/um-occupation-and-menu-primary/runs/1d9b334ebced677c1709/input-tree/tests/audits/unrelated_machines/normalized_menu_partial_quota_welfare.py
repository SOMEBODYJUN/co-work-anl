#!/usr/bin/env python3
"""给定部分支持证书的归一化菜单福利舍入与独立有限审计。

This solver accepts an explicit rational lambda witness; it does not solve an LP.
All decisions use exact Fraction arithmetic. The audit enumerates small inputs
and separately enumerates joint random actions to check the CDF formula.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import platform
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path


def rational(value, name):
    """No implicit conversion of floats, bools, strings, or other scalars."""
    if type(value) not in (int, Fraction):
        raise TypeError(f"{name}: expected int or Fraction, excluding bool/float")
    return Fraction(value)


def validate(menus, lambdas, delta=Fraction(3, 8)):
    if not isinstance(menus, (list, tuple)) or not menus:
        raise ValueError("menus: at least one explicit group is required")
    if not isinstance(lambdas, (list, tuple)) or len(lambdas) != len(menus):
        raise ValueError("lambda: exactly one row per group is required")
    delta = rational(delta, "delta")
    if not 0 < delta < 1:
        raise ValueError("delta must lie strictly between zero and one")
    rows, probabilities, width = [], [], None
    for g, (row, probability_row) in enumerate(zip(menus, lambdas)):
        if not isinstance(row, (list, tuple)) or not row:
            raise ValueError("every group must have a nonempty explicit state list")
        if not isinstance(probability_row, (list, tuple)) or len(row) != len(probability_row):
            raise ValueError("lambda row length must match the indexed state list")
        clean = []
        for s, state in enumerate(row):
            if not isinstance(state, (list, tuple)):
                raise TypeError("each state must be an explicit resource vector")
            if width is None:
                width = len(state)
            if not width or len(state) != width:
                raise ValueError("all state vectors must have the same positive length")
            weights = tuple(rational(w, f"p[{g},{s}]") for w in state)
            if any(w < 0 for w in weights):
                raise ValueError("negative state coefficient")
            if sum(weights, Fraction()) != 1:
                raise ValueError("every state must have total coefficient exactly one")
            clean.append(weights)
        prob = tuple(rational(x, f"lambda[{g}]") for x in probability_row)
        if any(x < 0 for x in prob) or sum(prob, Fraction()) > 1:
            raise ValueError("lambda rows must be nonnegative with sum at most one")
        rows.append(tuple(clean))
        probabilities.append(prob)
    total_mass = sum((sum(row, Fraction()) for row in probabilities), Fraction())
    if total_mass <= 0:
        raise ValueError("the total activation mass q must be positive")
    for u in range(width):
        column = sum(
            (probabilities[g][s] for g, row in enumerate(rows)
             for s, state in enumerate(row) if state[u] > 0), Fraction())
        if column > 1:
            raise ValueError("positive-support lambda column exceeds one")
    return tuple(rows), tuple(probabilities), delta, total_mass


def action_options(probabilities, g):
    options = [(s, p) for s, p in enumerate(probabilities[g]) if p > 0]
    inactive = 1 - sum(probabilities[g], Fraction())
    if inactive > 0:
        options.append((None, inactive))
    return options


def conditional_cdf(menus, probabilities, delta, prefix):
    """Exact conditional E[sum_u max_g bid_gu - delta * #active]."""
    n, m, fixed = len(menus), len(menus[0][0]), len(prefix)
    welfare = Fraction()
    for u in range(m):
        levels = sorted({Fraction()} | {state[u] for row in menus for state in row})
        for left, level in zip(levels, levels[1:]):
            below = Fraction(1)
            for g in range(n):
                if g < fixed:
                    bid = Fraction() if prefix[g] is None else menus[g][prefix[g]][u]
                    below *= int(bid < level)
                else:
                    p_below = 1 - sum(probabilities[g], Fraction())
                    p_below += sum(
                        (p for state, p in zip(menus[g], probabilities[g])
                         if state[u] < level), Fraction())
                    below *= p_below
            welfare += (level - left) * (1 - below)
    active = Fraction(sum(s is not None for s in prefix))
    active += sum((sum(probabilities[g], Fraction()) for g in range(fixed, n)), Fraction())
    return welfare, welfare - delta * active


def solve(menus, lambdas, delta=Fraction(3, 8)):
    """Return an actual disjoint allocation from the supplied lambda witness."""
    menus, probabilities, delta, q = validate(menus, lambdas, delta)
    n, m = len(menus), len(menus[0][0])
    expected_welfare, expected_score = conditional_cdf(menus, probabilities, delta, [])
    prefix, trace = [], []
    previous = expected_score
    for g in range(n):
        candidates = []
        for action, _ in action_options(probabilities, g):
            welfare, score = conditional_cdf(menus, probabilities, delta, prefix + [action])
            candidates.append((action, welfare, score))
        action, welfare, score = max(candidates, key=lambda item: item[2])
        if score < previous:
            raise AssertionError("conditional expectation decreased")
        prefix.append(action)
        previous = score
        trace.append(score)
    allocation = [[] for _ in menus]
    for u in range(m):
        bids = [Fraction() if s is None else menus[g][s][u] for g, s in enumerate(prefix)]
        owner = max(range(n), key=lambda g: (bids[g], -g))
        if bids[owner] > 0:
            allocation[owner].append(u)
    attaining, qualities, proxy_qualities = [], [], []
    for g, items in enumerate(allocation):
        if prefix[g] is None:
            if items:
                raise AssertionError("an inactive group received an item")
            attaining.append(0)
            qualities.append(Fraction())
            proxy_qualities.append(Fraction())
        else:
            values = [sum((state[u] for u in items), Fraction()) for state in menus[g]]
            state = max(range(len(values)), key=lambda s: values[s])
            attaining.append(state)
            qualities.append(values[state])
            proxy_qualities.append(sum((menus[g][prefix[g]][u] for u in items), Fraction()))
    proxy_welfare = sum(proxy_qualities, Fraction())
    active_count = sum(s is not None for s in prefix)
    score = proxy_welfare - delta * active_count
    high = sum(value >= delta for value in qualities)
    assert score == trace[-1] and score >= expected_score
    assert all(Fraction() <= p <= v <= 1 for p, v in zip(proxy_qualities, qualities))
    assert score <= (1 - delta) * high
    # A strictly weaker, purely rational consequence of 1 - 1/e > 5/8.
    assert expected_welfare > Fraction(5, 8) * q
    if delta < Fraction(5, 8):
        assert high > (Fraction(5, 8) - delta) * q / (1 - delta)
    return {
        "chosen_actions": prefix,
        "attaining_states": attaining,
        "allocation": allocation,
        "qualities": qualities,
        "proxy_qualities": proxy_qualities,
        "q": q,
        "delta": delta,
        "expected_welfare": expected_welfare,
        "expected_score": expected_score,
        "proxy_welfare": proxy_welfare,
        "score": score,
        "active_count": active_count,
        "high_count": high,
        "conditional_score_trace": trace,
    }


def oracle_joint(menus, probabilities, delta, prefix=()):
    """Independent oracle: explicitly expand joint random actions, not CDFs."""
    n, m = len(menus), len(menus[0][0])
    options = []
    for g in range(n):
        if g < len(prefix):
            options.append([(prefix[g], Fraction(1))])
        else:
            pairs = [(s, probabilities[g][s]) for s in range(len(menus[g]))
                     if probabilities[g][s]]
            leftover = 1 - sum(probabilities[g], Fraction())
            if leftover:
                pairs.append((None, leftover))
            options.append(pairs)
    expected_welfare, expected_score, joint_count = Fraction(), Fraction(), 0
    for joint in itertools.product(*options):
        probability = Fraction(1)
        actions = []
        for action, weight in joint:
            probability *= weight
            actions.append(action)
        welfare = Fraction()
        for u in range(m):
            bids = []
            for g, action in enumerate(actions):
                bids.append(Fraction() if action is None else menus[g][action][u])
            welfare += max(bids)
        score = welfare - delta * sum(action is not None for action in actions)
        expected_welfare += probability * welfare
        expected_score += probability * score
        joint_count += 1
    return expected_welfare, expected_score, joint_count


def audit_case(menus, lambdas, counters):
    result = solve(menus, lambdas)
    rows, probabilities, delta, _ = validate(menus, lambdas)
    frontier = [()]
    for fixed in range(len(rows) + 1):
        for prefix in frontier:
            expected = conditional_cdf(rows, probabilities, delta, list(prefix))
            welfare, score, count = oracle_joint(rows, probabilities, delta, prefix)
            assert expected == (welfare, score)
            counters["oracle_prefixes"] += 1
            counters["oracle_joint_action_visits"] += count
        if fixed < len(rows):
            frontier = [prefix + (action,) for prefix in frontier
                        for action, _ in action_options(probabilities, fixed)]
    seen = set()
    for items in result["allocation"]:
        assert seen.isdisjoint(items)
        seen.update(items)
    for g, items in enumerate(result["allocation"]):
        original_values = [sum((Fraction(state[u]) for u in items), Fraction())
                           for state in menus[g]]
        chosen = result["attaining_states"][g]
        assert type(chosen) is int and 0 <= chosen < len(menus[g])
        assert original_values[chosen] == max(original_values) == result["qualities"][g]
    if result["delta"] == Fraction(3, 8):
        assert result["high_count"] > Fraction(2, 5) * result["q"]
    counters["feasible_cases"] += 1
    return result


def audit():
    counts = Counter()
    fixtures = [
        ("singleton", [[(1,)]], [[1]]),
        ("zero_weights", [[(0, 1, 0)], [(1, 0, 0)]], [[1], [1]]),
        ("zero_activation_row", [[(1, 0)], [(0, 1)]], [[0], [1]]),
        ("tiny_q", [[(1, 0)]], [[Fraction(1, 2**257 + 1)]]),
        ("large_binary_denominator", [[(Fraction(1, 2**521 - 1),
                                          1 - Fraction(1, 2**521 - 1))]], [[1]]),
        ("duplicate_indexed_states", [[(1, 0), (1, 0)]], [[Fraction(1, 2)] * 2]),
        ("zero_probability_state", [[(1, 0), (0, 1)]], [[1, 0]]),
        ("unused_resource", [[(1, 0, 0)]], [[1]]),
    ]
    fixture_results = {}
    for name, menus, probabilities in fixtures:
        result = audit_case(menus, probabilities, counts)
        fixture_results[name] = {
            key: str(result[key]) for key in ("q", "expected_welfare", "score", "high_count")
        }
    counts["boundary_fixtures"] = len(fixtures)
    invalid = [
        ("bool_weight", [[(True,)]], [[1]], Fraction(3, 8)),
        ("float_weight", [[(1.0,)]], [[1]], Fraction(3, 8)),
        ("bool_lambda", [[(1,)]], [[True]], Fraction(3, 8)),
        ("float_lambda", [[(1,)]], [[0.5]], Fraction(3, 8)),
        ("negative_weight", [[(-1, 2)]], [[1]], Fraction(3, 8)),
        ("negative_lambda", [[(1,)]], [[-1]], Fraction(3, 8)),
        ("not_normalized", [[(Fraction(1, 2),)]], [[1]], Fraction(3, 8)),
        ("column_over_capacity", [[(1,)], [(1,)]], [[1], [1]], Fraction(3, 8)),
        ("row_over_one", [[(1,), (1,)]], [[1, 1]], Fraction(3, 8)),
        ("zero_total_q", [[(1,)]], [[0]], Fraction(3, 8)),
        ("empty_groups", [], [], Fraction(3, 8)),
        ("empty_state_list", [[]], [[]], Fraction(3, 8)),
        ("empty_resources", [[()]], [[1]], Fraction(3, 8)),
        ("lambda_size_mismatch", [[(1,)]], [[]], Fraction(3, 8)),
        ("resource_size_mismatch", [[(1,), (0, 1)]], [[Fraction(1, 2)] * 2], Fraction(3, 8)),
        ("bool_delta", [[(1,)]], [[1]], True),
        ("float_delta", [[(1,)]], [[1]], 0.375),
        ("zero_delta", [[(1,)]], [[1]], 0),
        ("one_delta", [[(1,)]], [[1]], 1),
    ]
    for name, menus, probabilities, delta in invalid:
        try:
            solve(menus, probabilities, delta)
        except (ValueError, TypeError):
            counts["invalid_inputs_rejected"] += 1
        else:
            raise AssertionError(f"invalid input accepted: {name}")
    enumeration = []
    for m in range(1, 4):
        states = [tuple(Fraction(x, 2) for x in vector)
                  for vector in itertools.product(range(3), repeat=m) if sum(vector) == 2]
        indexed_rows = list(itertools.product(states, repeat=2))
        for n in range(1, 3):
            for theta in (Fraction(1), Fraction(1, 3), Fraction(1, 2), Fraction(5, 6)):
                feasible, over_capacity = 0, 0
                for menus in itertools.product(indexed_rows, repeat=n):
                    lambdas = [[theta / 2, theta / 2] for _ in range(n)]
                    counts["enumerated_candidates"] += 1
                    try:
                        validate(menus, lambdas)
                    except ValueError as error:
                        if str(error) != "positive-support lambda column exceeds one":
                            raise
                        over_capacity += 1
                        counts["enumerated_over_capacity"] += 1
                    else:
                        audit_case(menus, lambdas, counts)
                        feasible += 1
                enumeration.append({"m": m, "n": n, "theta": str(theta),
                                    "feasible": feasible, "over_capacity": over_capacity})
    return {
        "status": "passed",
        "command": "python3 tests/audits/unrelated_machines/normalized_menu_partial_quota_welfare.py",
        "arithmetic": "exact fractions.Fraction only; no floating arithmetic in solver/oracle",
        "python": sys.version.split()[0],
        "implementation": platform.python_implementation(),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "counts": dict(sorted(counts.items())),
        "boundary_fixtures": fixture_results,
        "exhaustive_scope": {
            "resource_counts": [1, 2, 3], "group_counts": [1, 2],
            "states_per_group": 2,
            "states": "all ordered pairs, duplicates retained, of norm-one vectors over {0,1/2,1}",
            "state_probabilities": "each theta/2, inactive probability 1-theta",
            "theta": ["1", "1/3", "1/2", "5/6"],
            "oracle": "all positive-probability joint actions at every positive-probability prefix",
            "delta": "3/8", "sampling": "none",
        },
        "enumeration": enumeration,
        "limits": [
            "solver takes a supplied feasible lambda witness and does not implement an LP solver",
            "finite audit does not replace the universal welfare/count proof",
            "no general unrelated-machine schedule or hardness reduction is implemented",
            "no random samples or unlisted denominator/state-count ranges were tested",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, sort_keys=True, indent=2))
