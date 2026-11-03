"""Exact on-path query totals over all complete pure SPE of a finite instance.

This is an auxiliary attacker for the general query-payment candidates, not a
welfare theorem or a polynomial-time solver. Count caching retains conditional
outcome sets and does not impose a Markov strategy. See working.md for the proof.
"""
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[5]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
from customer_attraction import ExactSPESolver, Instance
from customer_attraction.certificate import StrategyCertificate


def increment(counts, action):
    return counts[:action] + (counts[action] + 1,) + counts[action + 1:]


class QueryEnvelope:
    def __init__(self, instance: Instance, query_weights):
        if instance.players < 1:
            raise ValueError('the research contract requires at least one player')
        self.instance = instance
        self.weights = tuple(Fraction(w) for w in query_weights)
        if len(self.weights) != instance.topic_count or any(w < 0 for w in self.weights):
            raise ValueError('one nonnegative rational query weight per topic is required')
        self.solver = ExactSPESolver(instance)
        self.empty = (0,) * instance.topic_count
        self.actions_for_sum = {}

    @lru_cache(None)
    def utility(self, terminal, action):
        return self.instance.topic_payoff(action, terminal)

    @lru_cache(None)
    def floors(self, counts):
        return tuple(min(self.utility(t, a)
                         for t in self.solver.outcomes(increment(counts, a)))
                     for a in range(self.instance.topic_count))

    @lru_cache(None)
    def conditional(self, counts, terminal):
        """Return minimum total queries and minimum individual row, given leaf.

        The two minima may require different complete SPE. A terminal state's
        minimum row is None, since its remaining path has no decision node.
        """
        if terminal not in self.solver.outcomes(counts):
            raise ValueError('conditional leaf is not a feasible SPE outcome')
        if sum(counts) == self.instance.players:
            return Fraction(0), None
        g = self.floors(counts)
        floor = max(g)
        base = sum(w * v for w, v in zip(self.weights, g))
        best_sum = best_row = None
        best_action = None
        for a in range(self.instance.topic_count):
            child = increment(counts, a)
            if (terminal not in self.solver.outcomes(child)
                    or self.utility(terminal, a) < floor):
                continue
            current = base + self.weights[a] * (self.utility(terminal, a) - g[a])
            child_sum, child_row = self.conditional(child, terminal)
            total = current + child_sum
            one_row = current if child_row is None else min(current, child_row)
            if best_sum is None or total < best_sum:
                best_sum, best_action = total, a
            if best_row is None or one_row < best_row:
                best_row = one_row
        assert best_sum is not None and best_action is not None
        self.actions_for_sum[counts, terminal] = best_action
        return best_sum, best_row

    def values(self):
        return {t: self.conditional(self.empty, t)
                for t in self.solver.outcomes()}

    def sum_certificate(self, terminal):
        """Full ordered-history certificate attaining the conditional sum.

        Only the unique actual path optimizes the query objective. Every other
        child is reconstructed separately to attain the parent mover's floor.
        Repeated count states are not forced to share a prescribed continuation.
        """
        self.conditional(self.empty, terminal)
        actions = {}

        def expand(history, counts, target, on_actual):
            if sum(counts) == self.instance.players:
                assert counts == target
                return
            g = self.floors(counts)
            floor = max(g)
            eligible = tuple(a for a in range(self.instance.topic_count)
                             if target in self.solver.outcomes(increment(counts, a))
                             and self.utility(target, a) >= floor)
            chosen = (self.actions_for_sum[counts, target]
                      if on_actual else eligible[0])
            actions[history] = chosen
            for a in range(self.instance.topic_count):
                child = increment(counts, a)
                desired = (target if a == chosen else
                           min(self.solver.outcomes(child),
                               key=lambda t: (self.utility(t, a), t)))
                expand(history + (a,), child, desired, on_actual and a == chosen)

        expand((), self.empty, terminal, True)
        return StrategyCertificate(actions, terminal)

    def root_repair_bad_gap(self):
        """Exact optimum of OPT-2W-3*root_regret for credible-child plans.

        Uses the pre-existing constant-three root-repair reduction. Positive
        output requires separate reconstruction and original-model certification;
        nonpositive output concerns this one finite instance only.
        """
        optimum = self.instance.optimal_welfare()
        floor = max(self.floors(self.empty))
        best = None
        for a in range(self.instance.topic_count):
            for terminal in self.solver.outcomes(increment(self.empty, a)):
                regret = max(Fraction(0), floor - self.utility(terminal, a))
                value = optimum - 2 * self.instance.welfare(terminal) - 3 * regret
                candidate = (value, a, terminal, regret)
                if best is None or candidate > best:
                    best = candidate
        return best
