#!/usr/bin/env python3
"""Definition-level finite audit of the Hamming/suffix credibility obstruction.

No canonical equilibrium solver, LP, or numerical arithmetic is used. Formal
strategies are complete functions of ordered histories. Exhaustive tail checks
use count representatives only after the strategy has entered its explicitly
count-dependent fresh-B suffix. Large tail domains are labeled sampled.
This finite audit does not prove the general claim; see the accompanying proof.
"""
from fractions import Fraction
from itertools import combinations, product
from math import comb, lcm
from pathlib import Path
import argparse
import json
import random


class Construction:
    def __init__(self, m, k, r, empty=False):
        assert m >= 1 and 0 <= k <= m - 1
        self.m, self.k, self.r = m, k, r
        self.n = m - k
        assert 0 <= r <= self.n - 1
        self.d = self.n - r
        self.scale = lcm(*range(1, self.d + 1))
        self.sizes = tuple(self.scale // max(self.d - i, 1)
                           for i in range(self.n)) + (self.scale,) * m
        if empty:
            self.sizes += (0,)
        self.p = len(self.sizes)
        self.b_labels = range(self.n, self.n + m)

    def fresh_b(self, h):
        return next(b for b in self.b_labels if b not in h)

    def action(self, h):
        assert len(h) < self.m
        if len(h) >= self.n:
            return self.fresh_b(h)
        wrong = [i for i, a in enumerate(h) if a != i]
        if not wrong:
            return len(h)
        if len(wrong) <= self.r:
            return self.fresh_b(h)
        return h[wrong[0]]

    def terminal(self, h):
        while len(h) < self.m:
            h += (self.action(h),)
        return h

    def payoff(self, a, z):
        return Fraction(self.sizes[a], z.count(a))

    def comparisons(self, h):
        a = self.action(h)
        actual = self.payoff(a, self.terminal(h))
        return tuple(actual - self.payoff(b, self.terminal(h + (b,)))
                     for b in range(self.p))

    def protected_histories(self):
        """All early histories at Hamming distance at most r from actual prefix."""
        for depth in range(self.n):
            for distance in range(min(self.r, depth) + 1):
                for changed in combinations(range(depth), distance):
                    alternatives = [tuple(a for a in range(self.p) if a != j)
                                    for j in changed]
                    for chosen in product(*alternatives):
                        h = list(range(depth))
                        for j, a in zip(changed, chosen):
                            h[j] = a
                        yield tuple(h)


def count_histories(p, length):
    def recurse(a, left, prefix):
        if a == p - 1:
            yield prefix + (a,) * left
            return
        for count in range(left + 1):
            yield from recurse(a + 1, left - count, prefix + (a,) * count)
    yield from recurse(0, length, ())


def audit(m, k, r, *, empty=False, count_limit=25000):
    c = Construction(m, k, r, empty)
    protected = 0
    min_gamma = None
    for h in c.protected_histories():
        gamma = c.comparisons(h)
        assert min(gamma) >= 0, (m, k, r, h, gamma)
        protected += 1
        min_gamma = min(gamma) if min_gamma is None else min(min_gamma, *gamma)
    # Every actual path node is checked, including nodes outside early protection.
    actual = c.terminal(())
    for depth in range(m):
        assert min(c.comparisons(actual[:depth])) >= 0
    welfare = sum(c.sizes[a] for a in set(actual))
    formula = c.scale * (sum((Fraction(1, j) for j in range(1, c.d + 1)), Fraction(0)) + r + k)
    assert welfare == formula
    # All themes have size <= L, while m disjoint B themes cover mL.
    optimum = m * c.scale
    assert max(c.sizes) == c.scale
    tail_report = []
    rng = random.Random(104729 + 100 * m + 10 * k + r)
    for depth in range(c.n, m):
        count = comb(depth + c.p - 1, c.p - 1)
        if count <= count_limit:
            histories = count_histories(c.p, depth)
            scope = "exhaustive_count_representatives"
        else:
            chosen = {actual[:depth]}
            chosen.update((a,) * depth for a in range(c.p))
            chosen.update(tuple(sorted(rng.randrange(c.p) for _ in range(depth)))
                          for _ in range(1000))
            histories = iter(sorted(chosen))
            scope = "deterministic_sample_only"
        checked = 0
        for h in histories:
            gamma = c.comparisons(h)
            assert min(gamma) >= 0, (m, k, r, h, gamma)
            checked += 1
        tail_report.append({"depth": depth, "scope": scope,
                            "checked_representatives": checked,
                            "total_count_representatives": count})
    bad = None
    if c.d >= 2:
        h = tuple(range(c.n, c.n + r + 1))
        alternative = c.n + r + 1
        gamma = c.comparisons(h)[alternative]
        assert gamma == Fraction(c.scale, c.d) - c.scale < 0
        bad = {"history": h, "specified": c.action(h),
               "alternative": alternative, "gamma": str(gamma)}
    return {"players": m, "suffix": k, "radius": r, "d": c.d,
            "empty_theme_added": empty, "topics": c.p,
            "scale": c.scale, "A_sizes": c.sizes[:c.n],
            "protected_early_histories": protected,
            "protected_early_comparisons": protected * c.p,
            "all_onpath_nodes_checked": m,
            "tail_checks": tail_report,
            "actual_terminal": actual, "welfare": welfare,
            "optimum": optimum, "ratio": str(Fraction(optimum, welfare)),
            "half_gap_2W_minus_OPT": 2 * welfare - optimum,
            "uncredible_node": bad}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    cases = [(1, 0, 0, False), (3, 0, 0, False), (5, 0, 2, False),
             (6, 2, 1, False), (7, 1, 0, False), (7, 1, 0, True),
             (10, 1, 1, False), (10, 2, 0, False)]
    report = {"status": "all_exact_finite_checks_passed",
              "general_theorem_proved_by": "accompanying symbolic proof, not this audit",
              "cases": [audit(m, k, r, empty=empty) for m, k, r, empty in cases]}
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        with args.output.open("x", encoding="utf-8") as out:
            out.write(text)
    print(text)


if __name__ == "__main__":
    main()
