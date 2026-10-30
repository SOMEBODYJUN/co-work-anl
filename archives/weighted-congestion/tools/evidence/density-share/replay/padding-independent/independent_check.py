#!/usr/bin/env python3
"""Independent definition-level exact audit of potential-user padding.

Only Python's standard library is used.  Equilibria are found by enumerating
all profiles and all unilateral deviations, without a forced-empty shortcut.
The mathematical universal statement is proved in review.md, not by this run.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
import json

if not __debug__:
    raise RuntimeError("Do not use -O: audit assertions must stay enabled.")


@dataclass(frozen=True)
class Player:
    weight: F
    strategies: tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class Game:
    polynomials: tuple[tuple[F, ...], ...]
    players: tuple[Player, ...]


def validate(game):
    assert game.polynomials and game.players
    for coefficients in game.polynomials:
        assert coefficients and all(a >= 0 for a in coefficients)
    for player in game.players:
        assert player.weight > 0 and player.strategies
        assert len(set(player.strategies)) == len(player.strategies)
        for strategy in player.strategies:
            assert len(strategy) == len(set(strategy))
            assert all(0 <= e < len(game.polynomials) for e in strategy)


def latency(coefficients, load):
    # Direct monomial evaluation, independently of the parent verifier.
    return sum((coefficient * load**degree
                for degree, coefficient in enumerate(coefficients)), F(0))


def costs(game, profile):
    loads = [F(0) for _ in game.polynomials]
    for player, choice in zip(game.players, profile):
        for e in player.strategies[choice]:
            loads[e] += player.weight
    values = [latency(coefficients, load)
              for coefficients, load in zip(game.polynomials, loads)]
    return tuple(sum((values[e] for e in player.strategies[choice]), F(0))
                 for player, choice in zip(game.players, profile))


def profiles(game):
    return product(*(range(len(player.strategies)) for player in game.players))


def unilateral(profile, player_index, strategy_index):
    return profile[:player_index] + (strategy_index,) + profile[player_index + 1:]


def equilibria(game, alpha):
    answer = set()
    for profile in profiles(game):
        actual = costs(game, profile)
        valid = True
        for i, player in enumerate(game.players):
            for alternative in range(len(player.strategies)):
                changed = unilateral(profile, i, alternative)
                if actual[i] > alpha * costs(game, changed)[i]:
                    valid = False
                    break
            if not valid:
                break
        if valid:
            answer.add(profile)
    return answer


def add_players(game, pairs):
    additions = tuple(Player(weight, ((), (resource,))) for resource, weight in pairs)
    augmented = Game(game.polynomials, game.players + additions)
    validate(augmented)
    assert augmented.polynomials is game.polynomials
    assert augmented.players[:len(game.players)] == game.players
    return augmented


def potential_weight_counts(game):
    result = [{} for _ in game.polynomials]
    for player in game.players:
        resource_union = set(e for strategy in player.strategies for e in strategy)
        for e in resource_union:
            result[e][player.weight] = result[e].get(player.weight, 0) + 1
    return result


def minimum_class_padding(game, target):
    assert isinstance(target, int) and target >= 1
    counts = potential_weight_counts(game)
    pairs = []
    for e, classes in enumerate(counts):
        for weight, multiplicity in classes.items():
            pairs.extend([(e, weight)] * max(0, target - multiplicity))
    return add_players(game, pairs)


def audit_class_padding(game, target):
    old = potential_weight_counts(game)
    augmented = minimum_class_padding(game, target)
    new = potential_weight_counts(augmented)
    for e, old_classes in enumerate(old):
        assert set(new[e]) == set(old_classes)
        for weight, multiplicity in old_classes.items():
            assert new[e][weight] == max(target, multiplicity)
        # Every possible interval cuts a contiguous block of weight classes.
        # We check all nonempty contiguous blocks, including ones which no
        # fixed-R interval can realize; the checked finite property is stronger.
        weights = sorted(new[e])
        for first in range(len(weights)):
            for last in range(first, len(weights)):
                assert sum(new[e][v] for v in weights[first:last+1]) >= target
    return len(augmented.players) - len(game.players)


def cases():
    all_zero = Game(
        ((F(0),), (F(0),)),
        (Player(F(1), ((), (0,))), Player(F(2), ((), (1,)))),
    )
    mixed = Game(
        ((F(0), F(0), F(1)), (F(0),), (F(3, 2),)),
        (Player(F(1), ((), (0, 1), (2,))),
         Player(F(2, 3), ((0,), (1, 2)))),
    )
    degree_zero = Game(
        ((F(2),), (F(0),)),
        (Player(F(3, 5), ((), (0,))), Player(F(7, 5), ((0,), (1,)))),
    )
    # Literal n=1, d=2, k=1, w=1/2, beta=9/20 two-column source gadget.
    # Its original game has no exact PNE; this is checked below, not assumed.
    source_gadget = Game(
        ((F(0), F(1)), (F(0), F(0), F(9, 20)),
         (F(0), F(1)), (F(0), F(0), F(9, 20)), (F(0),)),
        (Player(F(1), ((0, 1), (2, 3))),
         Player(F(1, 2), ((0, 3), (2, 1)))),
    )
    unused_resources = Game(
        ((F(1), F(0), F(2)), (F(0),)),
        (Player(F(1), ((),)),),
    )
    return [
        ("all_zero", all_zero, [(0, F(1, 2)), (0, F(1, 2)), (1, F(2))]),
        ("mixed_polynomial_zero_constant", mixed,
         [(0, F(1)), (1, F(1, 3)), (2, F(3, 2))]),
        ("degree_zero_empty_strategy", degree_zero,
         [(0, F(3, 5)), (0, F(2)), (1, F(1))]),
        ("source_gadget_no_exact_PNE", source_gadget,
         [(0, F(1, 2)), (0, F(1, 2)), (2, F(1)), (4, F(1)), (4, F(2))]),
        ("unused_resources", unused_resources,
         [(0, F(1)), (0, F(2)), (1, F(1)), (1, F(2))]),
    ]


def audit_case(name, original, pairs, factors):
    validate(original)
    augmented = add_players(original, pairs)
    original_n = len(original.players)
    records = []
    zero_active_witness = False
    for alpha in factors:
        eq_original = equilibria(original, alpha)
        eq_augmented = equilibria(augmented, alpha)
        projected = {profile[:original_n] for profile in eq_augmented}
        assert projected == eq_original
        for profile in eq_original:
            assert profile + (0,) * len(pairs) in eq_augmented
        for profile in eq_augmented:
            projected_profile = profile[:original_n]
            assert costs(augmented, profile)[:original_n] == costs(original, projected_profile)
            for i, player in enumerate(original.players):
                for alternative in range(len(player.strategies)):
                    lhs = costs(augmented, unilateral(profile, i, alternative))[i]
                    rhs = costs(original, unilateral(projected_profile, i, alternative))[i]
                    assert lhs == rhs
            for j, (resource, weight) in enumerate(pairs, original_n):
                nonzero = any(coefficient > 0 for coefficient in original.polynomials[resource])
                if nonzero:
                    assert profile[j] == 0
                elif profile[j] == 1:
                    zero_active_witness = True
        if name == "all_zero":
            assert len(eq_augmented) == 32
        if name == "source_gadget_no_exact_PNE" and alpha == 1:
            assert not eq_original and not eq_augmented
        records.append({"alpha": str(alpha), "original_equilibria": len(eq_original),
                        "augmented_equilibria": len(eq_augmented)})
    assert zero_active_witness
    padding_sizes = {str(target): audit_class_padding(original, target)
                     for target in [1, 2, 4, 17]}
    profile_count = 1
    for player in augmented.players:
        profile_count *= len(player.strategies)
    return {"case": name, "augmented_profiles_per_factor": profile_count,
            "factors": records, "zero_resource_active_equilibrium_witness": True,
            "class_padding_added_players": padding_sizes}


def check_step_boundary(factors):
    # Outside G_d: c_shared(x)=0 for x<=1 and 1 for x>1.
    # Original weight-1 player: {private} versus {shared}, private cost=1/2.
    # A new weight-1 player has empty/shared strategies.
    def step(load):
        return F(0) if load <= 1 else F(1)
    for alpha in factors:
        original_private_cost = F(1, 2)
        original_shared_deviation = step(F(1))
        assert original_private_cost > alpha * original_shared_deviation
        # In (original private, new shared), new player's current cost is zero.
        assert step(F(1)) <= alpha * F(0)
        # Original player's shared deviation creates load 2, cost 1.
        assert F(1, 2) <= alpha * step(F(2))
    return "VERIFIED outside-model step-cost obstruction to weakening strict positivity"


def main():
    factors = [F(1), F(101, 100), F(89, 50), F(2), F(17)]
    results = [audit_case(name, game, pairs, factors) for name, game, pairs in cases()]
    checked = sum(record["augmented_profiles_per_factor"] for record in results) * len(factors)
    result = {"result": "PASS", "arithmetic": "exact Fraction, no floats",
              "game_cases": len(results), "finite_factors": len(factors),
              "augmented_profile_factor_pairs_checked": checked,
              "checks": ["complete equilibrium projection sets equal",
                         "all-new-empty lift of every original equilibrium",
                         "original current and every unilateral-deviation cost equal",
                         "nonzero-resource new players empty at every equilibrium",
                         "zero-resource new players can be active",
                         "all occupied potential-weight blocks have requested minimum"],
              "step_boundary": check_step_boundary(factors), "cases": results}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
