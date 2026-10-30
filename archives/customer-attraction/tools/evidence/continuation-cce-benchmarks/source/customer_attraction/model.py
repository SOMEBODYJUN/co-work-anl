"""Finite common themes, sequential unit players, and equal unit-customer shares."""

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from typing import Any, Iterable, Mapping, Sequence

Counts = tuple[int, ...]
History = tuple[int, ...]


def _integer(value: Any, label: str, minimum: int = 0) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise ValueError(f"{label} must be an integer at least {minimum}")
    return value


@dataclass(frozen=True)
class CustomerType:
    """A positive number of identical unit customers liking the listed themes."""

    topics: frozenset[int]
    multiplicity: int = 1

    def __post_init__(self) -> None:
        try:
            topics = frozenset(self.topics)
        except TypeError as exc:
            raise ValueError("customer topics must be an iterable of indices") from exc
        for topic in topics:
            _integer(topic, "customer topic index")
        object.__setattr__(self, "topics", topics)
        _integer(self.multiplicity, "customer multiplicity", 1)


@dataclass(frozen=True)
class Instance:
    """All players choose once from the same labeled finite theme catalog.

    Empty theme coverage and different themes with identical coverage are legal.
    An empty catalog is legal only for the zero-player boundary instance.
    """

    topics: tuple[str, ...]
    customers: tuple[CustomerType, ...]
    players: int

    def __post_init__(self) -> None:
        topics = tuple(self.topics)
        customers = tuple(self.customers)
        _integer(self.players, "players")
        if any(not isinstance(name, str) or not name for name in topics):
            raise ValueError("topic labels must be nonempty strings")
        if len(set(topics)) != len(topics):
            raise ValueError("topic labels must be distinct; coverage may be identical")
        if self.players and not topics:
            raise ValueError("positive-player games need at least one legal topic")
        for customer in customers:
            if not isinstance(customer, CustomerType):
                raise ValueError("customers must be CustomerType objects")
            if any(topic >= len(topics) for topic in customer.topics):
                raise ValueError("customer topic index is outside the catalog")
        object.__setattr__(self, "topics", topics)
        object.__setattr__(self, "customers", customers)

    @property
    def topic_count(self) -> int:
        return len(self.topics)

    @property
    def customer_count(self) -> int:
        return sum(customer.multiplicity for customer in self.customers)

    def validate_counts(self, counts: Sequence[int], *, terminal: bool = False) -> Counts:
        counts = tuple(counts)
        if len(counts) != self.topic_count:
            raise ValueError("count vector has the wrong number of topics")
        for count in counts:
            _integer(count, "topic count")
        total = sum(counts)
        if total > self.players or (terminal and total != self.players):
            raise ValueError("count vector has the wrong number of players")
        return counts

    def counts(self, history: Sequence[int], *, terminal: bool = False) -> Counts:
        history = tuple(history)
        if len(history) > self.players or (terminal and len(history) != self.players):
            raise ValueError("history has the wrong number of players")
        counts = [0] * self.topic_count
        for topic in history:
            _integer(topic, "history topic index")
            if topic >= self.topic_count:
                raise ValueError("history topic index is outside the catalog")
            counts[topic] += 1
        return tuple(counts)

    def topic_payoffs(self, counts: Sequence[int]) -> tuple[Fraction, ...]:
        """Terminal payoff of each occupied topic; absent topics have value zero.

        For customer type S and final c, every attracted player gets
        multiplicity(S) / sum(c[b] for b in S). No indivisible weighted customer
        or customer-side equilibrium is introduced by the compressed encoding.
        """
        counts = self.validate_counts(counts, terminal=True)
        payoffs = [Fraction(0)] * self.topic_count
        for customer in self.customers:
            attracted = sum(counts[topic] for topic in customer.topics)
            if attracted:
                share = Fraction(customer.multiplicity, attracted)
                for topic in customer.topics:
                    if counts[topic]:
                        payoffs[topic] += share
        return tuple(payoffs)

    def topic_payoff(self, topic: int, counts: Sequence[int]) -> Fraction:
        _integer(topic, "topic index")
        if topic >= self.topic_count:
            raise ValueError("topic index is outside the catalog")
        return self.topic_payoffs(counts)[topic]

    def player_payoffs(self, history: Sequence[int]) -> tuple[Fraction, ...]:
        history = tuple(history)
        payoffs = self.topic_payoffs(self.counts(history, terminal=True))
        return tuple(payoffs[topic] for topic in history)

    def welfare(self, counts: Sequence[int]) -> int:
        counts = self.validate_counts(counts)
        return sum(customer.multiplicity for customer in self.customers
                   if any(counts[topic] for topic in customer.topics))

    def optimal_welfare(self) -> int:
        """Exact coverage optimum; finite subset enumeration, no efficiency claim."""
        best = 0
        for size in range(min(self.players, self.topic_count) + 1):
            for support in combinations(range(self.topic_count), size):
                counts = tuple(int(topic in support) for topic in range(self.topic_count))
                best = max(best, self.welfare(counts))
        return best

    def to_dict(self) -> dict[str, Any]:
        return {
            "topics": list(self.topics),
            "customers": [{"topics": sorted(customer.topics),
                           "multiplicity": customer.multiplicity}
                          for customer in self.customers],
            "players": self.players,
        }

    @classmethod
    def from_dict(cls, obj: Mapping[str, Any]) -> "Instance":
        try:
            return cls(tuple(obj["topics"]),
                       tuple(CustomerType(frozenset(item["topics"]),
                                          item.get("multiplicity", 1))
                             for item in obj["customers"]), obj["players"])
        except (KeyError, TypeError) as exc:
            raise ValueError("invalid customer-attraction instance schema") from exc

    @classmethod
    def from_topic_sets(cls, coverage: Iterable[Iterable[Any]], players: int,
                        labels: Sequence[str] | None = None) -> "Instance":
        """Build unit customers from themes given as sets of customer labels.

        Only customer labels appearing in a theme are created. To include
        uninterested customers, use a CustomerType with an empty topics set.
        """
        coverage = tuple(frozenset(customers) for customers in coverage)
        signatures: dict[frozenset[int], int] = {}
        customers = set().union(*coverage) if coverage else set()
        for customer in customers:
            signature = frozenset(topic for topic, covered in enumerate(coverage)
                                  if customer in covered)
            signatures[signature] = signatures.get(signature, 0) + 1
        labels = tuple(labels) if labels is not None else tuple(
            f"T{topic}" for topic in range(len(coverage)))
        if len(labels) != len(coverage):
            raise ValueError("labels and theme coverage have different lengths")
        return cls(labels, tuple(CustomerType(signature, multiplicity)
                                 for signature, multiplicity in sorted(
                                     signatures.items(), key=lambda item: tuple(sorted(item[0])))),
                   players)


def big_theme_lower_bound(players: int) -> Instance:
    """m common big-theme clients and m-1 disjoint singleton-theme clients.

    The all-big path has welfare m, while optimum coverage is 2m-1. This function
    provides the finite instance family; it does not assert a universal bound.
    """
    _integer(players, "players", 1)
    return Instance(("B",) + tuple(f"S{i}" for i in range(1, players)),
                    (CustomerType(frozenset({0}), players),) + tuple(
                        CustomerType(frozenset({topic}))
                        for topic in range(1, players)), players)
