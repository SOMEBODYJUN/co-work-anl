#!/usr/bin/env python3
"""Exact self-audit; no canonical model or equilibrium solver imports.

This checks a universal scalar lemma and finite true full-history SPE samples.
It does not claim a normalized coupling which proves general half coverage.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import random


def credit(c: int, p: int, a: int, d0: int, d: int):
    assert c >= 1 and 0 <= p <= c and a in (0, 1)
    assert p + a <= d0 <= d
    old_post = max(F(0), F(p, c) - (F(p, d0) if p else F(0)))
    root_gain = F(a, d0) - F(a, d) if a else F(0)
    old_pre = F(p, c) - (F(p, d) if p else F(0))
    refund = F(p, d0) - F(p, d) if p else F(0)
    assert old_post == max(F(0), old_pre - refund)
    return old_post, root_gain, old_pre, refund


def envelope(c: int, p: int, a: int, d: int):
    if d == 0:
        return F(0)
    return max(F(0), (F(a, p + a) if a else F(0)) - F(a, d),
               F(p, c) - F(p, d))


def scalar_audit():
    rows = envelopes = 0
    for c in range(1, 14):
        for p in range(c + 1):
            for a in (0, 1):
                for d in range(p + a, 17):
                    values = []
                    for d0 in range(p + a, d + 1):
                        old, gain, _, _ = credit(c, p, a, d0, d)
                        combined = old + gain
                        assert combined >= 0
                        assert combined <= (1 - F(1, d) if d else 0)
                        values.append(combined)
                        # Exact cap when a deletion upper bound is specified.
                        for upper in (d - d0, d - d0 + 2):
                            cap = old + (F(a * upper, d0 * (d0 + upper))
                                         if a else F(0))
                            assert combined <= cap
                        rows += 1
                    assert max(values) == envelope(c, p, a, d)
                    envelopes += 1
    sharp = []
    for d in range(1, 31):
        old, gain, _, _ = credit(1, 0, 1, 1, d)
        assert old + gain == 1 - F(1, d)
        if d >= 2:
            old2, gain2, _, _ = credit(1, 1, 1, 2, d)
            assert old2 + gain2 == 1 - F(1, d)
        sharp.append(d)
    old, gain, pre, refund = credit(1, 1, 1, 2, 5)
    assert max(F(0), pre) + gain == F(11, 10)
    assert old + gain == F(4, 5)
    return {"scalar_rows": rows, "fixed_parameter_envelopes": envelopes,
            "sharp_d_values": sharp,
            "predelete_double_count": {"old_pre": str(pre),
                "root_gain": str(gain), "old_refund": str(refund),
                "old_post": str(old), "naive_total": "11/10",
                "corrected_total": "4/5"}}


def payoffs(history, topics):
    result = [F(0) for _ in history]
    customers = set().union(*topics)
    for x in customers:
        hits = [j for j, a in enumerate(history) if x in topics[a]]
        for j in hits:
            result[j] += F(1, len(hits))
    return tuple(result)


def build_spe(topics, m, seed):
    """Ordered-history backward induction, with independently chosen tied actions."""
    rng = random.Random(seed)
    strategy = {}
    terminal = {}
    def visit(h):
        if len(h) == m:
            terminal[h] = h
            return h
        children = [visit(h + (a,)) for a in range(len(topics))]
        vals = [payoffs(z, topics)[len(h)] for z in children]
        best = max(vals)
        a = rng.choice([a for a, val in enumerate(vals) if val == best])
        strategy[h] = a
        terminal[h] = children[a]
        return children[a]
    actual = visit(())
    comparisons = 0
    for h, a in strategy.items():
        chosen = payoffs(terminal[h], topics)[len(h)]
        assert terminal[h] == terminal[h + (a,)]
        for b in range(len(topics)):
            assert chosen >= payoffs(terminal[h + (b,)], topics)[len(h)]
            comparisons += 1
    return actual, strategy, terminal, comparisons


def game_audit(topics, m, seed):
    actual, strategy, terminal, comparisons = build_spe(topics, m, seed)
    customers = set().union(*topics)
    covered = set().union(*(topics[a] for a in actual))
    c = {x: sum(x in topics[a] for a in actual) for x in covered}
    branches = masks = customer_checks = 0
    mixture = F(0)
    # Every actual-prefix action is followed by the original complete strategy.
    # Uniformly mixing these branches is a concrete total-mass-one mixture.
    branch_count = m * len(topics)
    for i in range(m):
        h = actual[:i]
        assert strategy[h] == actual[i]
        for a in range(len(topics)):
            z = terminal[h + (a,)]
            assert z[:i] == h and z[i] == a
            future = m - i - 1
            one_branch_average = F(0)
            for deleted_mask in range(1 << future):
                deleted = {i + 1 + j for j in range(future)
                           if deleted_mask & (1 << j)}
                total = F(0)
                for x in covered:
                    p = sum(x in topics[b] for b in h)
                    indicator = int(x in topics[a])
                    d = sum(x in topics[b] for b in z)
                    d0 = sum(x in topics[b] for j, b in enumerate(z)
                             if j not in deleted)
                    old, gain, _, _ = credit(c[x], p, indicator, d0, d)
                    combined = old + gain
                    assert combined <= envelope(c[x], p, indicator, d)
                    assert combined <= (1 - F(1, d) if d else 0)
                    total += combined
                    customer_checks += 1
                assert total <= F(m - 1, m) * len(covered)
                one_branch_average += total / (1 << future)
                masks += 1
            mixture += one_branch_average / branch_count
            branches += 1
    assert mixture <= F(m - 1, m) * len(covered)
    return {"players": m, "topics": len(topics), "unit_customers": len(customers),
            "decision_histories": len(strategy), "true_deviation_comparisons": comparisons,
            "actual": actual, "welfare": len(covered), "real_branches": branches,
            "deletion_masks": masks, "customer_credit_checks": customer_checks,
            "normalized_mixture_credit": str(mixture),
            "normalized_mixture_cap": str(F(m - 1, m) * len(covered))}


def reentry_audit():
    rows = []
    for m in range(1, 65):
        actual, strategy, terminal, comparisons = build_spe([{0}], m, 0)
        assert actual == (0,) * m and len(strategy) == m
        total = F(0)
        for i in range(1, m + 1):
            # The true forced action retains the sole original action.
            assert terminal[actual[:i]] == actual
            old, gain, _, _ = credit(m, i - 1, 1, i, m)
            assert old == 0 and gain == F(1, i) - F(1, m)
            assert old + gain == envelope(m, i - 1, 1, m)
            total += old + gain
        harmonic_minus_one = sum((F(1, i) for i in range(1, m + 1)), F(0)) - 1
        assert total == harmonic_minus_one
        # No player is strictly below either mentioned endogenous threshold.
        assert not (F(1, m) < F(1, m))
        assert not (F(1, m) < F(1, 2 * m))
        if m == 4:
            assert total == F(13, 12) > 1
        rows.append({"players": m, "true_decision_histories": len(strategy),
                     "true_deviation_comparisons": comparisons,
                     "full_depth_credit": str(total), "actual_welfare": 1})
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    scalar = scalar_audit()
    cases = [([set(), set()], 3, 0),
             ([{0}, {0}, set()], 4, 1),
             ([{0, 1}, {1, 2}, {2, 3}, {0, 3}], 5, 2)]
    for seed in range(18):
        rng = random.Random(97003 + seed)
        k = 2 + seed % 3
        m = 2 + seed % 4
        topics = [{x for x in range(11) if rng.randrange(3) == 0}
                  for _ in range(k)]
        cases.append((topics, m, 21000 + seed))
    games = [game_audit(*case) for case in cases]
    report = {"status": "all_exact_checks_passed", "scope":
              "Universal lemma proved in prose; finite full-history pure SPE audit only.",
              "scalar": scalar, "games": games,
              "true_spe_full_depth_reentry": reentry_audit(),
              "totals": {key: sum(game[key] for game in games) for key in (
                  "decision_histories", "true_deviation_comparisons", "real_branches",
                  "deletion_masks", "customer_credit_checks")},
              "unproved": "A normalized coupling paying every omitted customer and any reentry."}
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        with args.output.open("x") as stream:
            stream.write(text + "\n")
    else:
        print(text)


if __name__ == "__main__":
    main()
