"""Exact full-SPE-tree optimization of the eta-only deletion candidate.

Standalone standard library implementation. Count states cache outcome SETS;
certificate reconstruction gives each ordered history its own continuation.
"""
from __future__ import annotations

import argparse
from bisect import bisect_right
from functools import lru_cache
from fractions import Fraction as F
from itertools import product
from math import lcm
from pathlib import Path
import json


class Tree:
    def __init__(self, instance):
        self.instance = instance
        self.m = instance["players"]
        self.p = len(instance["topics"])
        self.types = [(sum(1 << a for a in row["topics"]), row.get("multiplicity", 1))
                      for row in instance["customers"]]
        self.L = lcm(*range(1, self.m + 1)) if self.m else 1
        self.zero = (0,) * self.p
        self.choice = {}

    def child(self, k, a):
        return k[:a] + (k[a] + 1,) + k[a + 1:]

    @lru_cache(None)
    def cov(self, k):
        return sum(w for B, w in self.types if any(k[a] for a in range(self.p) if B >> a & 1))

    @lru_cache(None)
    def pay(self, q):
        ans = [0] * self.p
        for B, w in self.types:
            c = sum(q[a] for a in range(self.p) if B >> a & 1)
            if c:
                for a in range(self.p):
                    if q[a] and B >> a & 1:
                        ans[a] += w * (self.L // c)
        return tuple(ans)

    @lru_cache(None)
    def outcomes(self, k):
        if sum(k) == self.m:
            return frozenset([k])
        children = [self.outcomes(self.child(k, a)) for a in range(self.p)]
        threshold = max(min(self.pay(q)[a] for q in children[a]) for a in range(self.p))
        return frozenset(q for a in range(self.p) for q in children[a] if self.pay(q)[a] >= threshold)

    @lru_cache(None)
    def threshold(self, k):
        return max(min(self.pay(q)[a] for q in self.outcomes(self.child(k, a))) for a in range(self.p))

    @lru_cache(None)
    def optimum(self, k):
        if sum(k) == self.m:
            return self.cov(k)
        return max(self.optimum(self.child(k, a)) for a in range(self.p))

    def eta(self, k, s, a, q):
        r = self.m - sum(k)
        M = t = 0
        for B, w in self.types:
            if B >> a & 1 and not (B >> s & 1) and not any(k[b] for b in range(self.p) if B >> b & 1):
                M += w
                if sum(q[b] for b in range(self.p) if B >> b & 1) == 1:
                    t += w
        out = r * self.pay(q)[a] - self.L * (M + (r - 1) * t)
        assert out >= 0
        return out

    @lru_cache(None)
    def envelope(self, k, s, a):
        # For an off-path branch a, maximize eta among every child SPE
        # whose source payoff is below a given threshold.
        rows = sorted((self.pay(q)[a], self.eta(k, s, a, q), q)
                      for q in self.outcomes(self.child(k, a)))
        caps, maxima, witnesses = [], [], []
        best = -1
        for cap, eta, q in rows:
            if eta > best:
                best, witness = eta, q
            caps.append(cap)
            maxima.append(best)
            witnesses.append(witness)
        return caps, maxima, witnesses

    def local(self, k, s, q):
        cap = self.pay(q)[s]
        menu = [a for a in range(self.p) if self.optimum(self.child(k, a)) == self.optimum(k)]
        best, replies = None, {}
        for a in menu:
            if a == s:
                eta, reply = self.eta(k, s, a, q), q
            else:
                caps, values, witnesses = self.envelope(k, s, a)
                ix = bisect_right(caps, cap) - 1
                assert ix >= 0
                eta, reply = values[ix], witnesses[ix]
            replies[a] = reply
            best = eta if best is None else min(best, eta)
        return F(best, self.L * (self.m - sum(k))), replies

    @lru_cache(None)
    def path_best(self, k, q):
        if sum(k) == self.m:
            return F(0)
        best = None
        for a in range(self.p):
            child = self.child(k, a)
            if q in self.outcomes(child) and self.pay(q)[a] >= self.threshold(k):
                value, replies = self.local(k, a, q)
                value += self.path_best(child, q)
                if best is None or value > best:
                    best = value
                    self.choice[k, q] = a, replies
        assert best is not None
        return best

    def certificate(self, root):
        actions = {}
        def build(h, k, q, optimize):
            if len(h) == self.m:
                assert k == q
                return
            if optimize:
                a, replies = self.choice[k, q]
            else:
                a = next(a for a in range(self.p)
                         if q in self.outcomes(self.child(k, a)) and self.pay(q)[a] >= self.threshold(k))
                replies = {}
            actions[h] = a
            for b in range(self.p):
                d = q if b == a else replies.get(b)
                if d is None:
                    d = min(self.outcomes(self.child(k, b)), key=lambda x: (self.pay(x)[b], x))
                assert b == a or self.pay(d)[b] <= self.pay(q)[a]
                build(h + (b,), self.child(k, b), d, optimize and b == a)
        build((), self.zero, root, True)
        return actions

    def verify(self, actions):
        # Direct ordered-tree replay, independent of cached outcome membership.
        leaves = {}
        comparisons = 0
        def replay(h, k):
            nonlocal comparisons
            if len(h) == self.m:
                return k
            continuations = [replay(h + (a,), self.child(k, a)) for a in range(self.p)]
            a = actions[h]
            q = continuations[a]
            for b, d in enumerate(continuations):
                assert self.pay(q)[a] >= self.pay(d)[b], (h, a, b, q, d)
                comparisons += 1
            leaves[h] = q
            return q
        q = replay((), self.zero)
        h, k, eta_sum, detail = (), self.zero, F(0), []
        while len(h) < self.m:
            a, r = actions[h], self.m - len(h)
            terms = []
            for b in range(self.p):
                if self.optimum(self.child(k, b)) == self.optimum(k):
                    d = leaves[h + (b,)] if r > 1 else self.child(k, b)
                    terms.append((self.eta(k, a, b, d), b, d))
            eta, b, d = min(terms)
            value = F(eta, self.L * r)
            eta_sum += value
            detail.append({"history": list(h), "actual": a, "menu": [b for _, b, _ in terms],
                           "min_eta_over_r": str(value), "minimizer": b,
                           "terms": [{"action": b, "eta_over_r": str(F(v, self.L * r)), "reply_counts": list(d)}
                                     for v, b, d in terms]})
            h, k = h + (a,), self.child(k, a)
        assert k == q
        return {"path": list(h), "counts": list(q), "W": self.cov(q),
                "OPT": self.optimum(self.zero), "eta_sum": str(eta_sum),
                "half_slack": 2 * self.cov(q) - self.optimum(self.zero),
                "defect": str(eta_sum - 2 * self.cov(q) + self.optimum(self.zero)),
                "ordered_decision_histories": len(actions), "comparisons": comparisons, "path_detail": detail}

    def solve(self, save_actions=False):
        roots = self.outcomes(self.zero)
        q = max(roots, key=lambda q: (self.path_best(self.zero, q) - 2 * self.cov(q), q))
        best = self.path_best(self.zero, q) - 2 * self.cov(q) + self.optimum(self.zero)
        actions = self.certificate(q)
        report = self.verify(actions)
        assert F(report["defect"]) == best
        report.update({"root_outcomes": len(roots), "count_states": self.outcomes.cache_info().currsize,
                       "max_defect_over_all_complete_SPE": str(best), "instance": self.instance,
                       "scope": "Every pure complete ordered-history SPE of this fixed customer instance; exact BI and independent subtree assembly."})
        if save_actions:
            report["strategy"] = [{"history": list(h), "action": a} for h, a in sorted(actions.items())]
        return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("--players", type=int)
    ap.add_argument("--output", type=Path)
    ap.add_argument("--save-actions", action="store_true")
    args = ap.parse_args()
    instance = json.loads(args.input.read_text())
    if args.players is not None:
        instance["players"] = args.players
    report = Tree(instance).solve(args.save_actions)
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text)


if __name__ == "__main__":
    main()
