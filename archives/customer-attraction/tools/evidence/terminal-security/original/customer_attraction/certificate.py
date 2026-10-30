"""Complete ordered-history strategies and a definition-level SPE verifier.

The verifier never calls the outcome-set solver. It evaluates all action branches
of the supplied strategy tree and checks the current player's actual payoff.
"""

from dataclasses import dataclass
from fractions import Fraction
from types import MappingProxyType
from typing import Any, Mapping

from .model import Counts, History, Instance, _integer


@dataclass(frozen=True)
class StrategyCertificate:
    actions: Mapping[History, int]
    terminal_counts: Counts

    def __post_init__(self) -> None:
        actions = {}
        for history, action in self.actions.items():
            history = tuple(history)
            for topic in history:
                _integer(topic, "certificate history topic index")
            _integer(action, "certificate action")
            actions[history] = action
        object.__setattr__(self, "actions", MappingProxyType(actions))
        counts = tuple(self.terminal_counts)
        for count in counts:
            _integer(count, "certificate terminal count")
        object.__setattr__(self, "terminal_counts", counts)

    def to_dict(self) -> dict[str, Any]:
        return {
            "terminal_counts": list(self.terminal_counts),
            "actions": [{"history": list(history), "action": action}
                        for history, action in sorted(
                            self.actions.items(), key=lambda item: (len(item[0]), item[0]))],
        }

    @classmethod
    def from_dict(cls, obj: Mapping[str, Any]) -> "StrategyCertificate":
        try:
            actions = {}
            for item in obj["actions"]:
                history = tuple(item["history"])
                if history in actions:
                    raise ValueError("duplicate ordered history in certificate")
                actions[history] = item["action"]
            return cls(actions, tuple(obj["terminal_counts"]))
        except (KeyError, TypeError) as exc:
            raise ValueError("invalid strategy certificate schema") from exc


@dataclass(frozen=True)
class DeviationViolation:
    history: History
    chosen_action: int
    deviating_action: int
    chosen_counts: Counts
    deviating_counts: Counts
    chosen_payoff: Fraction
    deviating_payoff: Fraction


@dataclass(frozen=True)
class CertificateVerification:
    valid: bool
    terminal_counts: Counts | None
    terminal_history: History | None
    checked_histories: int
    checked_deviations: int
    violations: tuple[DeviationViolation, ...]
    errors: tuple[str, ...]

    def assert_valid(self) -> None:
        if not self.valid:
            detail = self.errors[0] if self.errors else str(self.violations[0])
            raise ValueError(f"invalid pure SPE certificate: {detail}")


def verify_certificate(instance: Instance, certificate: StrategyCertificate
                       ) -> CertificateVerification:
    """Check completeness and all subgame incentives from the supplied strategy.

    Each player moves once, so backward induction over this full tree proves SPE
    iff at every history the prescribed action beats each supplied continuation.
    No Markov consistency is required for equal-count ordered histories.
    """
    errors: list[str] = []
    try:
        declared = instance.validate_counts(certificate.terminal_counts, terminal=True)
    except ValueError as exc:
        errors.append(str(exc))
        declared = None
    expected: set[History] = set()

    def collect(history: History) -> None:
        if len(history) == instance.players:
            return
        expected.add(history)
        for action in range(instance.topic_count):
            collect(history + (action,))

    collect(())
    missing = expected.difference(certificate.actions)
    extra = set(certificate.actions).difference(expected)
    if missing:
        errors.append(f"missing action for ordered history {min(missing, key=lambda h: (len(h), h))}")
    if extra:
        errors.append(f"extra action outside a decision history {min(extra, key=lambda h: (len(h), h))}")
    for history, action in certificate.actions.items():
        if not isinstance(action, int) or isinstance(action, bool) or not 0 <= action < instance.topic_count:
            errors.append(f"invalid action at ordered history {history}")
    if errors:
        return CertificateVerification(False, None, None, 0, 0, (), tuple(errors))
    violations: list[DeviationViolation] = []
    checked = 0
    deviations = 0
    payoff_cache: dict[Counts, tuple[Fraction, ...]] = {}

    def payoffs(counts: Counts) -> tuple[Fraction, ...]:
        if counts not in payoff_cache:
            payoff_cache[counts] = instance.topic_payoffs(counts)
        return payoff_cache[counts]

    def walk(history: History) -> tuple[Counts, History]:
        nonlocal checked, deviations
        if len(history) == instance.players:
            return instance.counts(history, terminal=True), history
        branches = [walk(history + (action,)) for action in range(instance.topic_count)]
        chosen = certificate.actions[history]
        chosen_counts, chosen_history = branches[chosen]
        current = payoffs(chosen_counts)[chosen]
        checked += 1
        for alternative, (alternative_counts, _) in enumerate(branches):
            if alternative == chosen:
                continue
            deviations += 1
            deviation = payoffs(alternative_counts)[alternative]
            if deviation > current:
                violations.append(DeviationViolation(history, chosen, alternative,
                                                      chosen_counts, alternative_counts,
                                                      current, deviation))
        return chosen_counts, chosen_history

    terminal_counts, terminal_history = walk(())
    if declared != terminal_counts:
        errors.append("declared terminal counts disagree with the strategy's root outcome")
    return CertificateVerification(not errors and not violations, terminal_counts,
                                   terminal_history, checked, deviations,
                                   tuple(violations), tuple(errors))
