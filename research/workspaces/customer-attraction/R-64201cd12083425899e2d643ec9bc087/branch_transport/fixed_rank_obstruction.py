"""Full formal policy and exact audit for every fixed departure-rank cutoff.

NOT an SPE or a counterexample to half coverage. Only incentive rows at
D_sigma(h)<=cutoff are asserted. Every row uses its genuine policy continuation.
"""
from fractions import Fraction
from math import comb, lcm
import argparse
import json


class FixedRankFamily:
    def __init__(self, players, cutoff):
        if players < 1 or cutoff < 0:
            raise ValueError("positive players and nonnegative cutoff required")
        self.m, self.k = players, cutoff
        self.M = 2 ** cutoff
        self.L = lcm(*range(1, (players + self.M - 1) // self.M + 1))
        self.sizes = tuple(self.L // ((players - i + self.M - 1) // self.M)
                           for i in range(players)) + (self.L,) * players
        self.p = 2 * players

    def reaction(self, history, action, new_rank):
        """The complete terminal plan upon a genuine departure at this node."""
        remaining = self.m - len(history)
        if new_rank > self.k:
            return history + (action,) * remaining
        a = 2 ** (self.k - new_rank)
        d = self.L // self.sizes[action]
        past = history.count(action)
        q = max(past + 1, (remaining + past + 1) // (a * d + 1))
        plan = history + (action,) * (q - past)
        for big in range(self.m, 2 * self.m):
            if len(plan) == self.m:
                break
            if big not in plan:
                plan += (big,)
        assert len(plan) == self.m
        return plan

    def state(self, history):
        """Evaluate the complete policy at an arbitrary full ordered history."""
        rank = 0
        plan = tuple(range(self.m))
        for i, action in enumerate(history):
            if action != plan[i]:
                rank += 1
                plan = self.reaction(history[:i], action, rank)
        return rank, plan

    def policy(self, history):
        return self.state(history)[1][len(history)]

    def terminal(self, history):
        return self.state(history)[1]

    def utility(self, plan, position):
        action = plan[position]
        return Fraction(self.sizes[action], plan.count(action))

    def audit(self):
        # Every state explicitly retains its full ordered history, departure
        # rank, and current complete terminal plan. No count-state merging.
        stack = [((), 0, tuple(range(self.m)))]
        nodes = comparisons = 0
        by_rank = [0] * (min(self.k, self.m - 1) + 1)
        minimum = Fraction()
        while stack:
            history, rank, plan = stack.pop()
            nodes += 1
            by_rank[rank] += 1
            depth = len(history)
            assert self.state(history) == (rank, plan)
            actual = self.utility(plan, depth)
            prescribed = plan[depth]
            for alternative in range(self.p):
                child_rank = rank + (alternative != prescribed)
                child_plan = (plan if alternative == prescribed else
                              self.reaction(history, alternative, child_rank))
                deviation = self.utility(child_plan, depth)
                slack = actual - deviation
                assert slack >= 0, (history, alternative, rank, actual, deviation)
                minimum = min(minimum, slack)
                comparisons += 1
                if depth + 1 < self.m and child_rank <= self.k:
                    stack.append((history + (alternative,), child_rank, child_plan))
        expected = [comb(self.m, j + 1) * (self.p - 1) ** j
                    for j in range(len(by_rank))]
        assert by_rank == expected
        assert nodes == sum(expected)
        return self.summary() | {
            "constrained_nodes": nodes,
            "nodes_by_rank": by_rank,
            "exact_comparisons": comparisons,
            "minimum_slack": str(minimum),
            "audit": "complete_all_individual_rows_at_rank_at_most_cutoff",
        }

    def summary(self):
        welfare = sum(self.sizes[:self.m])
        optimum = self.m * self.L
        return {
            "players": self.m, "cutoff": self.k, "M": self.M,
            "L": self.L, "reward_sizes": self.sizes[:self.m],
            "big_theme_count": self.m, "big_theme_size": self.L,
            "unit_customers": sum(self.sizes),
            "root_welfare": welfare, "optimum": optimum,
            "optimum_over_welfare": str(Fraction(optimum, welfare)),
            "optimum_minus_twice_welfare": optimum - 2 * welfare,
            "status": "RESTRICTED_ROWS_ONLY_NOT_SPE",
        }


def audit_integer_bounds():
    checks = 0
    for a in (1, 2, 4, 8, 16, 32, 64):
        for d in range(1, 61):
            for remaining in range(1, 101):
                for past in (0, 1, 2, remaining, 2 * remaining):
                    q = max(past + 1, (remaining + past + 1) // (a * d + 1))
                    assert 0 <= q - past - 1 <= remaining - 1
                    assert d * q >= (remaining + 2 * a - 1) // (2 * a)
                    if q > past + 1:
                        last_remaining = remaining - q + past + 1
                        assert a * d * q <= last_remaining
                    checks += 1
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--players", type=int)
    parser.add_argument("--cutoff", type=int)
    args = parser.parse_args()
    if args.players is not None or args.cutoff is not None:
        if args.players is None or args.cutoff is None:
            parser.error("supply both --players and --cutoff")
        print(json.dumps(FixedRankFamily(args.players, args.cutoff).audit(), indent=2))
        return
    configs = ((5, 0), (9, 1), (6, 2), (5, 3), (4, 4))
    output = {
        "complete_small_audits": [FixedRankFamily(m, k).audit() for m, k in configs],
        "integer_parameter_checks": audit_integer_bounds(),
        "half_violating_family_summaries_analytic_not_full_tree_audits": [],
    }
    for k in range(8):
        M = 2 ** k
        first = 4 * M + (5 * M) // 18 + 1
        previous = FixedRankFamily(first - 1, k).summary()
        witness = FixedRankFamily(first, k).summary()
        assert previous["optimum_minus_twice_welfare"] <= 0
        assert witness["optimum_minus_twice_welfare"] > 0
        output["half_violating_family_summaries_analytic_not_full_tree_audits"].append(witness)
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
