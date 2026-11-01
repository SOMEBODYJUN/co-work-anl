"""Exact audit of individual-incentive rows at deviation rank at most one.

The formal policy is defined at every ordered history by ``policy``.  It is
NOT an SPE.  The positive result checked is only that every action comparison
at every node with D_sigma(h) <= 1 holds.  The root violates half coverage.
No optimizer, canonical SPE solver, or floating-point arithmetic is used.
"""
from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from math import lcm
import argparse
import json


class RankOneFamily:
    def __init__(self, players: int):
        if players < 1:
            raise ValueError("players must be positive")
        self.m = players
        self.L = lcm(*range(1, (players + 1) // 2 + 1))
        # All themes are pairwise disjoint, with this many distinct unit clients.
        self.sizes = tuple(self.L // ((players - i + 1) // 2)
                           for i in range(players)) + (self.L,) * players
        self.p = len(self.sizes)

    def name(self, action):
        return f"A{action + 1}" if action < self.m else f"B{action - self.m + 1}"

    @lru_cache(None)
    def first_deviation_plan(self, prefix, action):
        """Complete path after the first departure from A1,...,Am."""
        r = self.m - len(prefix)
        past = prefix.count(action)
        denominator = self.L // self.sizes[action]
        total = max(past + 1, (r + past + 1) // (denominator + 1))
        extra = total - past - 1
        path = prefix + (action,) * (extra + 1)
        # Fresh big themes are legal; at most m-1 are ever required.
        for big in range(self.m, 2 * self.m):
            if len(path) == self.m:
                break
            if big not in path:
                path += (big,)
        assert len(path) == self.m
        return path

    @lru_cache(None)
    def policy(self, history):
        """A complete, ordered-history-dependent pure formal policy.

        Follow rewards until the first departure, then follow its specified
        plan until the second departure.  Thereafter repeat the last action.
        """
        if len(history) >= self.m:
            raise ValueError("terminal history has no decision")
        first = next((i for i, a in enumerate(history) if a != i), None)
        if first is None:
            return len(history)
        plan = self.first_deviation_plan(history[:first], history[first])
        if all(history[j] == plan[j] for j in range(first + 1, len(history))):
            return plan[len(history)]
        return history[-1]

    def rank(self, history):
        return sum(action != self.policy(history[:j])
                   for j, action in enumerate(history))

    def terminal(self, prefix):
        path = prefix
        while len(path) < self.m:
            path += (self.policy(path),)
        return path

    def utility(self, terminal, position):
        action = terminal[position]
        return Fraction(self.sizes[action], terminal.count(action))

    def constrained_nodes(self):
        """Exactly the nodes with D_sigma(h)<=1, without a huge full tree."""
        nodes = {tuple(range(i)) for i in range(self.m)}
        for i in range(self.m):
            prefix = tuple(range(i))
            for alternative in range(self.p):
                if alternative == i:
                    continue
                plan = self.first_deviation_plan(prefix, alternative)
                for depth in range(i + 1, self.m):
                    nodes.add(plan[:depth])
        assert all(self.rank(h) <= 1 for h in nodes)
        # Closure: each prescribed child keeps its rank; every alternative
        # child of a rank-zero node has rank one, and is included if nonterminal.
        # Conversely every rank-one node has a unique first departure from the
        # root reward path and then follows that departure's specified plan.
        for h in tuple(nodes):
            if len(h) + 1 < self.m:
                prescribed = self.policy(h)
                assert h + (prescribed,) in nodes
                if self.rank(h) == 0:
                    for a in range(self.p):
                        assert h + (a,) in nodes
        return sorted(nodes, key=lambda h: (len(h), h))

    def audit(self):
        nodes = self.constrained_nodes()
        minimum = None
        comparisons = 0
        ranks = {0: 0, 1: 0}
        for h in nodes:
            ranks[self.rank(h)] += 1
            actual = self.utility(self.terminal(h), len(h))
            for alternative in range(self.p):
                deviation = self.utility(self.terminal(h + (alternative,)), len(h))
                slack = actual - deviation
                assert slack >= 0, (h, alternative, actual, deviation)
                minimum = slack if minimum is None else min(minimum, slack)
                comparisons += 1
        root = self.terminal(())
        assert root == tuple(range(self.m))
        welfare = sum(self.sizes[a] for a in set(root))
        optimum = self.m * self.L
        harmonic_formula = sum((Fraction(1, (r + 1) // 2)
                                for r in range(1, self.m + 1)), Fraction())
        assert welfare == self.L * harmonic_formula
        output = {
            "players": self.m,
            "topics": self.p,
            "all_themes_disjoint": True,
            "big_theme_size": self.L,
            "theme_sizes": {self.name(a): size for a, size in enumerate(self.sizes)},
            "unit_customers": sum(self.sizes),
            "root_path": [self.name(a) for a in root],
            "root_welfare": welfare,
            "optimum": optimum,
            "optimum_over_welfare": str(Fraction(optimum, welfare)),
            "optimum_minus_twice_welfare": optimum - 2 * welfare,
            "constrained_nodes": len(nodes),
            "nodes_by_rank": ranks,
            "exact_action_comparisons": comparisons,
            "minimum_slack": str(minimum),
            "status": "rank_at_most_one_rows_only_NOT_SPE",
        }
        if self.m >= 3:
            h = (self.m, self.m + 1)
            alternative = self.m + 2
            assert self.rank(h) == 2
            actual = self.utility(self.terminal(h), len(h))
            deviation = self.utility(self.terminal(h + (alternative,)), len(h))
            assert deviation > actual
            output["explicit_missing_rank_two_violation"] = {
                "history": [self.name(a) for a in h],
                "prescribed": self.name(self.policy(h)),
                "deviation": self.name(alternative),
                "actual_utility": str(actual),
                "deviation_utility": str(deviation),
                "slack": str(actual - deviation),
            }
        return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--players", type=int, default=9)
    parser.add_argument("--through", type=int, default=12,
                        help="audit every family member from 1 through this number")
    args = parser.parse_args()
    result = RankOneFamily(args.players).audit()
    RankOneFamily.policy.cache_clear()
    RankOneFamily.first_deviation_plan.cache_clear()
    table = []
    for m in range(1, args.through + 1):
        audit = RankOneFamily(m).audit()
        RankOneFamily.policy.cache_clear()
        RankOneFamily.first_deviation_plan.cache_clear()
        table.append({key: audit[key] for key in (
            "players", "root_welfare", "optimum", "optimum_over_welfare",
            "optimum_minus_twice_welfare", "constrained_nodes", "exact_action_comparisons")})
    result["family_audits"] = table
    result["first_half_violation_in_audited_family"] = next(
        (item["players"] for item in table if item["optimum_minus_twice_welfare"] > 0), None)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
