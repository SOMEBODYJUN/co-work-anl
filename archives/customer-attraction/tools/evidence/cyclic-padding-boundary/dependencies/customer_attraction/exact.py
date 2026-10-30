"""All pure, arbitrarily history-dependent SPE terminal counts, exactly.

At prefix counts k each action a has a nonempty child outcome set R(k+e_a).
Set M(k) = max_a min_{c in R(k+e_a)} u_a(c). Then
R(k) = union_a {c in R(k+e_a): u_a(c) >= M(k)}.
Caching these sets by counts never commits to a single Markov continuation.
"""

from dataclasses import dataclass
from fractions import Fraction
from typing import Callable, Iterator, Sequence

from .certificate import StrategyCertificate
from .model import Counts, History, Instance

ActionSelector = Callable[[History, tuple[int, ...]], int]
ContinuationSelector = Callable[[History, tuple[Counts, ...]], Counts]


def _increment(counts: Counts, action: int) -> Counts:
    return counts[:action] + (counts[action] + 1,) + counts[action + 1:]


@dataclass(frozen=True)
class SolverStats:
    count_states: int
    terminal_states: int
    retained_outcomes: int


class ExactSPESolver:
    """Finite exact outcome enumeration, not an input-bit-polynomial algorithm.

    All equilibrium claims concern pure strategies. Mixed behavioral SPEs and
    their expected outcomes are outside this solver's contract.
    """

    def __init__(self, instance: Instance):
        if not isinstance(instance, Instance):
            raise ValueError("expected a customer-attraction Instance")
        self.instance = instance
        self._outcomes: dict[Counts, frozenset[Counts]] = {}
        self._payoffs: dict[Counts, tuple[Fraction, ...]] = {}
        self._thresholds: dict[Counts, Fraction] = {}

    def _utility(self, counts: Counts, action: int) -> Fraction:
        if counts not in self._payoffs:
            self._payoffs[counts] = self.instance.topic_payoffs(counts)
        return self._payoffs[counts][action]

    def outcomes(self, prefix_counts: Sequence[int] | None = None) -> frozenset[Counts]:
        """Every terminal count vector achievable by a pure SPE from the prefix."""
        counts = ((0,) * self.instance.topic_count if prefix_counts is None
                  else self.instance.validate_counts(prefix_counts))
        return self._solve(counts)

    def _solve(self, counts: Counts) -> frozenset[Counts]:
        if counts in self._outcomes:
            return self._outcomes[counts]
        if sum(counts) == self.instance.players:
            result = frozenset({counts})
        else:
            children = [self._solve(_increment(counts, action))
                        for action in range(self.instance.topic_count)]
            floor = max(min(self._utility(terminal, action) for terminal in child)
                        for action, child in enumerate(children))
            self._thresholds[counts] = floor
            result = frozenset(terminal for action, child in enumerate(children)
                               for terminal in child
                               if self._utility(terminal, action) >= floor)
            # Finiteness of each child and a maximizing floor action guarantee
            # nonemptiness, including the all-zero-payoff boundary game.
            if not result:
                raise AssertionError("nonempty finite game lost all SPE outcomes")
        self._outcomes[counts] = result
        return result

    def threshold(self, prefix_counts: Sequence[int]) -> Fraction:
        counts = self.instance.validate_counts(prefix_counts)
        if sum(counts) == self.instance.players:
            raise ValueError("terminal prefixes have no decision threshold")
        self._solve(counts)
        return self._thresholds[counts]

    def minimum_welfare(self) -> int:
        return min(map(self.instance.welfare, self.outcomes()))

    def maximum_welfare(self) -> int:
        return max(map(self.instance.welfare, self.outcomes()))

    def worst_outcomes(self) -> frozenset[Counts]:
        minimum = self.minimum_welfare()
        return frozenset(counts for counts in self.outcomes()
                         if self.instance.welfare(counts) == minimum)

    def inefficiency_ratio(self) -> Fraction:
        """OPT / minimum SPE welfare; use ratio 1 for a zero-coverage game."""
        optimum = self.instance.optimal_welfare()
        minimum = self.minimum_welfare()
        if not minimum:
            if optimum:
                raise ZeroDivisionError("positive optimum with zero SPE welfare")
            return Fraction(1)
        return Fraction(optimum, minimum)

    @property
    def stats(self) -> SolverStats:
        return SolverStats(len(self._outcomes),
                           sum(sum(counts) == self.instance.players
                               for counts in self._outcomes),
                           sum(len(outcomes) for outcomes in self._outcomes.values()))

    def ordered_outcomes(self, target_counts: Sequence[int] | None = None) -> Iterator[History]:
        """Enumerate every ordered path realizable by a pure SPE.

        This is a path iterator, not enumeration of all complete strategy maps.
        Each yielded path can be expanded with certificate(on_path=path).
        """
        targets = (sorted(self.outcomes()) if target_counts is None else
                   [self.instance.validate_counts(target_counts, terminal=True)])
        for target in targets:
            if target not in self.outcomes():
                raise ValueError("target terminal counts are not a pure SPE outcome")

            def paths(history: History, counts: Counts) -> Iterator[History]:
                if len(history) == self.instance.players:
                    yield history
                    return
                floor = self.threshold(counts)
                for action in range(self.instance.topic_count):
                    child = _increment(counts, action)
                    if target in self._solve(child) and self._utility(target, action) >= floor:
                        yield from paths(history + (action,), child)

            yield from paths((), (0,) * self.instance.topic_count)

    def certificate(self, target_counts: Sequence[int] | None = None, *,
                    on_path: Sequence[int] | None = None,
                    action_selector: ActionSelector | None = None,
                    continuation_selector: ContinuationSelector | None = None
                    ) -> StrategyCertificate:
        """Expand one full ordered-history pure SPE realizing the requested target.

        Off-path child b selects an SPE minimizing the current mover's u_b.
        Selector callbacks may break ties separately at each ordered history.
        They must return a member of the supplied finite candidate tuple.
        An optional on_path specifies the order as well as the terminal counts.
        """
        ordered = tuple(on_path) if on_path is not None else None
        path_counts = (self.instance.counts(ordered, terminal=True)
                       if ordered is not None else None)
        target = (self.instance.validate_counts(target_counts, terminal=True)
                  if target_counts is not None else
                  path_counts if path_counts is not None else min(self.outcomes()))
        if path_counts is not None and path_counts != target:
            raise ValueError("on_path and target terminal counts disagree")
        if target not in self.outcomes():
            raise ValueError("target terminal counts are not a pure SPE outcome")
        actions: dict[History, int] = {}

        def expand(history: History, counts: Counts, desired: Counts) -> None:
            if len(history) == self.instance.players:
                if counts != desired:
                    raise AssertionError("certificate target was not realized")
                return
            floor = self.threshold(counts)
            admissible = tuple(action for action in range(self.instance.topic_count)
                               if desired in self._solve(_increment(counts, action))
                               and self._utility(desired, action) >= floor)
            if ordered is not None and history == ordered[:len(history)]:
                chosen = ordered[len(history)]
            else:
                chosen = (action_selector(history, admissible)
                          if action_selector is not None else admissible[0])
            if isinstance(chosen, bool) or chosen not in admissible:
                raise ValueError("requested action is not admissible for this SPE continuation")
            actions[history] = chosen
            for action in range(self.instance.topic_count):
                child_history = history + (action,)
                child_counts = _increment(counts, action)
                if action == chosen:
                    child_target = desired
                else:
                    child = self._solve(child_counts)
                    minimum = min(self._utility(terminal, action) for terminal in child)
                    candidates = tuple(sorted(terminal for terminal in child
                                              if self._utility(terminal, action) == minimum))
                    child_target = (continuation_selector(child_history, candidates)
                                    if continuation_selector is not None else candidates[0])
                    try:
                        child_target = self.instance.validate_counts(child_target, terminal=True)
                    except (TypeError, ValueError) as exc:
                        raise ValueError("continuation selector returned invalid counts") from exc
                    if child_target not in candidates:
                        raise ValueError("continuation selector must select a supplied minimizer")
                expand(child_history, child_counts, child_target)

        expand((), (0,) * self.instance.topic_count, target)
        return StrategyCertificate(actions, target)

    def worst_certificate(self) -> StrategyCertificate:
        return self.certificate(min(self.worst_outcomes()))
