#!/usr/bin/env python3
"""Exact pure-SPE enumeration, retaining arbitrary history-dependent tie-breaking.

Requirements: Python 3.10+, NumPy.
Weights mean numbers of distinct UNIT customers with identical topic interests.
This program does NOT prove the one-half welfare conjecture.
"""
from functools import lru_cache
from fractions import Fraction
from itertools import combinations_with_replacement, product
from pathlib import Path
import json
import math
import random
import numpy as np


def profiles(m, n):
    for actions in combinations_with_replacement(range(m), n):
        yield tuple(actions.count(a) for a in range(m))


class Game:
    def __init__(self, m, n, weights):
        if type(m) is not int or m < 1 or type(n) is not int or n < 0:
            raise ValueError("Require integer m >= 1 and n >= 0.")
        for mask, value in weights.items():
            if type(mask) is not int or not 0 < mask < (1 << m):
                raise ValueError("Invalid customer-interest mask.")
            if type(value) is not int or value < 0:
                raise ValueError("Customer multiplicities must be nonnegative integers.")
        self.m, self.n = m, n
        self.weights = {k: v for k, v in weights.items() if v}
        self.Q = math.lcm(*range(1, n + 1)) if n else 1
        if sum(self.weights.values()) * max(n, 1) * self.Q >= 2**62:
            raise OverflowError("Instance exceeds this implementation's safe int64 range.")
        self.terminals = list(profiles(m, n))
        self.index = {c: i for i, c in enumerate(self.terminals)}
        masks = sorted(self.weights)
        # Guard memory before constructing the dense exact-integer payoff table.
        if len(masks) * len(self.terminals) > 20_000_000:
            raise MemoryError("Dense table too large; use a sparse/on-demand implementation.")
        bits = np.array(
            [[(mask >> a) & 1 for a in range(m)] for mask in masks],
            dtype=np.int64,
        ).reshape(len(masks), m)
        weights_array = np.array([self.weights[k] for k in masks], dtype=np.int64)
        loads = bits @ np.array(self.terminals, dtype=np.int64).T
        inverse = np.array([0] + [self.Q // k for k in range(1, n + 1)], dtype=np.int64)
        self.pay = bits.T @ (weights_array[:, None] * inverse[loads])
        self.cover = weights_array @ (loads > 0)
        for c in self.terminals:
            assert sum(c[a] * self.score(c, a) for a in range(m)) == self.Q * self.welfare(c)

        @lru_cache(None)
        def outcomes(h):
            if sum(h) == n:
                return frozenset((h,))
            children = [outcomes(self.add(h, a)) for a in range(m)]
            threshold = max(min(self.score(c, a) for c in children[a]) for a in range(m))
            return frozenset(
                c for a in range(m) for c in children[a]
                if self.score(c, a) >= threshold
            )
        self.outcomes = outcomes

    def add(self, h, a):
        return tuple(h[b] + int(a == b) for b in range(self.m))

    def score(self, c, a):
        """Exact utility multiplied by Q; query only an action used in c."""
        return int(self.pay[a, self.index[c]])

    def welfare(self, c):
        return int(self.cover[self.index[c]])

    def optimum(self):
        return max(map(self.welfare, self.terminals))

    def last_floor(self):
        if not self.n:
            return Fraction(0)
        value = min(
            max(self.score(self.add(h, a), a) for a in range(self.m))
            for h in profiles(self.m, self.n - 1)
        )
        return Fraction(value, self.Q)

    def certificate(self, target):
        """Build a full ordered-history SPE policy supporting target."""
        if target not in self.outcomes((0,) * self.m):
            raise ValueError("Target is not an SPE outcome.")
        policy = {}

        def build(history, counts, desired):
            if len(history) == self.n:
                assert counts == desired
                return
            children = [self.outcomes(self.add(counts, a)) for a in range(self.m)]
            minima = [min(self.score(c, a) for c in children[a]) for a in range(self.m)]
            threshold = max(minima)
            chosen = next(
                a for a in range(self.m)
                if desired in children[a] and self.score(desired, a) >= threshold
            )
            policy[history] = chosen
            for a in range(self.m):
                child_target = desired if a == chosen else min(
                    children[a], key=lambda c: (self.score(c, a), c)
                )
                build(history + (a,), self.add(counts, a), child_target)

        build((), (0,) * self.m, target)
        return policy

    def verify(self, policy):
        """Check optimality at EVERY ordered history, including off-path ones."""
        expected = sum(self.m**d for d in range(self.n))
        assert len(policy) == expected

        def visit(history, counts):
            if len(history) == self.n:
                return counts
            a = policy[history]
            assert 0 <= a < self.m
            children = [
                visit(history + (b,), self.add(counts, b))
                for b in range(self.m)
            ]
            terminal = children[a]
            own = self.score(terminal, a)
            assert all(own >= self.score(children[b], b) for b in range(self.m))
            return terminal

        return visit((), (0,) * self.m)


SMALL = {
    (3,0,0):-17, (2,1,0):-14, (2,0,1):10, (1,2,0):20, (1,1,1):-15,
    (1,0,2):-20, (0,3,0):-16, (0,2,1):-6, (0,1,2):9, (0,0,3):20,
}
BIG = {
    (4,0,0):6, (3,1,0):-13, (3,0,1):-19, (2,2,0):-19, (2,1,1):-8,
    (2,0,2):-1, (1,3,0):9, (1,2,1):5, (1,1,2):4, (1,0,3):4,
    (0,4,0):-13, (0,3,1):2, (0,2,2):-16, (0,1,3):-18, (0,0,4):6,
}


def auxiliary_counterexample():
    """Deterministic integer construction. NOT a counterexample to welfare >= OPT/2."""
    m = 12
    desired = [0] * (1 << m)
    for mask in range(1 << m):
        counts = tuple(((mask >> (4*g)) & 15).bit_count() for g in range(3))
        if mask.bit_count() == 3:
            desired[mask] = SMALL[counts]
        elif mask.bit_count() == 4:
            desired[mask] = BIG[counts]

    # Subset Mobius transform: multilinear coefficients of the desired potential.
    coefficients = desired.copy()
    for a in range(m):
        for mask in range(1 << m):
            if (mask >> a) & 1:
                coefficients[mask] -= coefficients[mask ^ (1 << a)]
    sums = [0] + [
        (-1)**(mask.bit_count()+1) * mask.bit_count() * coefficients[mask]
        for mask in range(1, 1 << m)
    ]
    # Superset Mobius inversion recovers signed customer multiplicities.
    signed = sums.copy()
    for a in range(m):
        for mask in range(1 << m):
            if not ((mask >> a) & 1):
                signed[mask] -= signed[mask | (1 << a)]
    offset = 1 - min(signed[1:])
    weights = {mask: signed[mask] + offset for mask in range(1, 1 << m)}
    assert min(weights.values()) > 0

    # Independently check the harmonic-potential transform on all subsets
    # of three and four distinct labels.
    harmonic_scaled = (0, 12, 18, 22, 25)
    for k in (3, 4):
        for c in profiles(m, k):
            if max(c) > 1:
                continue
            active = sum(1 << a for a in range(m) if c[a])
            actual = sum(
                signed[mask] * harmonic_scaled[(active & mask).bit_count()]
                for mask in range(1, 1 << m)
            )
            assert actual == 12 * desired[active]
    return Game(m, 4, weights), offset


def self_test():
    # Empty-customer and zero-provider boundary cases.
    for n in (0, 1, 3):
        g = Game(2, n, {})
        assert g.optimum() == 0
        assert g.outcomes((0, 0))
    g = Game(1, 3, {1: 6})
    assert g.score((3,), 0) == 2 * g.Q

    # Published lower-bound family, including n = 1.
    for n in range(1, 6):
        weights = {1: n, **{1 << a: 1 for a in range(1, n)}}
        g = Game(n, n, weights)
        target = (n,) + (0,) * (n - 1)
        assert target in g.outcomes((0,) * n)
        assert g.welfare(target) == n and g.optimum() == 2*n - 1
        assert g.verify(g.certificate(target)) == target

    # Independent exhaustive full-policy enumeration: 27 games, 128 policies each.
    exhaustive_games = 0
    for values in product(range(3), repeat=3):
        g = Game(2, 3, dict(zip((1, 2, 3), values)))
        histories = [h for d in range(3) for h in product(range(2), repeat=d)]
        found = set()
        for choices in product(range(2), repeat=len(histories)):
            policy = dict(zip(histories, choices))
            try:
                found.add(g.verify(policy))
            except AssertionError:
                pass
        assert found == set(g.outcomes((0, 0)))
        assert (2*g.n - 1) * g.last_floor() >= g.optimum()
        exhaustive_games += 1
    rng = random.Random(6137)
    for _ in range(100):
        m, n = rng.choice(((3,2), (3,3), (4,3), (4,4), (5,3)))
        weights = {mask: rng.randrange(20)
                   for mask in range(1, 1 << m) if rng.random() < 0.5}
        game = Game(m, n, weights)
        optimum = game.optimum()
        largest = max(sum(v for mask, v in weights.items() if (mask >> a) & 1)
                      for a in range(m))
        theta = game.last_floor()
        assert theta >= Fraction(optimum, 2*n - 1)
        assert theta >= Fraction(2*optimum - (n-1)*largest, 2*n)
        for terminal in game.outcomes((0,) * m):
            assert game.welfare(terminal) * n * (2*n-1) >= 4*(n-1)*optimum
    return exhaustive_games


def main(directory):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    exhaustive_games = self_test()
    game, offset = auxiliary_counterexample()
    target = tuple(int(a in (0, 4, 5, 8)) for a in range(12))
    policy = game.certificate(target)
    assert game.verify(policy) == target
    history = ()
    while len(history) < game.n:
        history += (policy[history],)
    utilities = [Fraction(game.score(target, a), game.Q) for a in history]
    theta = game.last_floor()
    assert utilities[0] < theta
    assert theta - utilities[0] == 1
    assert sum(utilities) == game.welfare(target)
    assert 2 * game.welfare(target) >= game.optimum()

    certificate = {
        "status": "Refutes an auxiliary payoff-floor lemma, NOT the one-half conjecture.",
        "m": game.m, "n": game.n,
        "weights": {str(k): v for k, v in game.weights.items()},
        "target": target,
        "policy": [{"history": list(h), "action": a}
                   for h, a in sorted(policy.items(), key=lambda item: (len(item[0]), item[0]))],
    }
    report = {
        "main_conjecture": "UNRESOLVED BY THIS WORK",
        "git_sync": "NOT COMPLETED; anonymous git clone failed DNS; no remote writes.",
        "exhaustive_crosscheck_games": exhaustive_games,
        "policies_per_crosscheck_game": 128,
        "proved_bound_random_crosschecks": 100,
        "proved_three_provider_bound": "W >= (8/15) OPT",
        "providers": game.n, "topics": game.m, "offset": offset,
        "unit_customers": sum(game.weights.values()),
        "minimum_mask_multiplicity": min(game.weights.values()),
        "maximum_mask_multiplicity": max(game.weights.values()),
        "verified_ordered_histories": len(policy),
        "on_path_actions_zero_based": list(history),
        "on_path_utilities": [str(x) for x in utilities],
        "last_player_floor": str(theta),
        "spe_coverage": game.welfare(target),
        "optimal_coverage": game.optimum(),
        "twice_spe_coverage_minus_optimum": 2*game.welfare(target)-game.optimum(),
        "root_spe_outcome_count": len(game.outcomes((0,) * game.m)),
    }
    (directory / "auxiliary_counterexample.json").write_text(
        json.dumps(certificate, indent=2), encoding="utf-8")
    (directory / "verification_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main(Path(__file__).resolve().parent)
