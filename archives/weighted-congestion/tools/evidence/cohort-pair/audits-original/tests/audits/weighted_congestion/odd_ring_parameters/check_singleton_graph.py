#!/usr/bin/env python3
"""Exact checks of the single-conflict state graph and its player costs."""

from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import random


def polynomial(coeffs: list[int], z: Fraction) -> Fraction:
    return sum((c * z**k for k, c in enumerate(coeffs)), Fraction(0))


def defects(bits: tuple[int, ...], m: int) -> list[int]:
    positions = []
    for i in range(m):
        if bits[2*i] == bits[2*i+1]:
            positions.append(2*i)
        if bits[2*i+1] != bits[2*((i+1) % m)]:
            positions.append(2*i+1)
    return positions


def costs(bits: tuple[int, ...], weights: list[Fraction],
          shapes: list[list[int]], m: int) -> list[Fraction]:
    result = [Fraction(0)] * (2*m)
    conflicted = set(defects(bits, m))
    for i in range(m):
        h, light, next_h = 2*i, 2*i+1, 2*((i+1) % m)
        for position, left, right in ((2*i, h, light), (2*i+1, light, next_h)):
            if position in conflicted:
                fee = polynomial(shapes[position], weights[left] + weights[right])
                result[left] += fee
                result[right] += fee
            else:
                result[left] += polynomial(shapes[position], weights[left])
                result[right] += polynomial(shapes[position], weights[right])
    return result


def verify(m: int, d: int, rng: random.Random) -> dict[str, object]:
    weights = [Fraction(rng.randrange(1, 8), rng.randrange(1, 6)) for _ in range(2*m)]
    shapes = [[rng.randrange(4) for _ in range(d+1)] for _ in range(2*m)]
    # Include a zero-fee resource to check that no positive-cost assumption is hidden.
    shapes[0] = [0] * (d+1)
    states = {}
    for tail in product((0, 1), repeat=2*m-1):
        bits = (0,) + tail
        conflict = defects(bits, m)
        if len(conflict) == 1:
            assert conflict[0] not in states
            states[conflict[0]] = bits
    assert len(states) == 2*m
    arcs = set()
    equilibria = 0
    reverse_map_checked = 0
    for position, bits in states.items():
        current = costs(bits, weights, shapes, m)
        assert current == costs(tuple(1-b for b in bits), weights, shapes, m)
        outgoing = 0
        for player in range(2*m):
            flipped = list(bits)
            flipped[player] ^= 1
            changed = tuple(flipped)
            after = costs(changed, weights, shapes, m)
            other_defects = defects(changed, m)
            if len(other_defects) != 1:
                assert len(other_defects) == 3
                assert current[player] <= after[player]
                continue
            target = other_defects[0]
            assert (target-position) % (2*m) in (1, 2*m-1)
            target_current = costs(states[target], weights, shapes, m)
            assert target_current[player] == after[player]
            if current[player] > d * after[player]:
                outgoing += 1
                arcs.add((position, target))
            reverse_map_checked += 1
        equilibria += outgoing == 0
    assert all((b, a) not in arcs for a, b in arcs)
    assert equilibria > 0
    # Reverse ring order, exchange player classes, and exchange B-copy labels.
    for bits in states.values():
        new = []
        new_weights = []
        new_shapes = []
        for j in range(m):
            i = (-j) % m
            new.extend((bits[2*i+1], bits[2*i]))
            new_weights.extend((weights[2*i+1], weights[2*i]))
            new_shapes.extend((shapes[2*i], shapes[2*((i-1) % m)+1]))
        old_cost = costs(bits, weights, shapes, m)
        new_cost = costs(tuple(new), new_weights, new_shapes, m)
        assert new_cost == [old_cost[p] for j in range(m)
                            for p in (2*((-j) % m)+1, 2*((-j) % m))]
        assert len(defects(tuple(new), m)) == 1
    return {
        "odd_ring_length": m,
        "degree": d,
        "alpha": d,
        "single_conflict_states_mod_global_exchange": len(states),
        "single_conflict_alpha_PNE_count": equilibria,
        "neighbor_cost_swap_checks": reverse_map_checked,
        "nonincident_players_cannot_improve": True,
        "opposite_arcs_mutually_exclusive": True,
        "reverse_ring_player_and_resource_map_exact": True,
        "zero_fee_resource_included": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    seed = 20261014
    rng = random.Random(seed)
    result = {"arithmetic": "integers and fractions only", "seed": seed,
              "scope": "finite checks of SINGLETON_NOTE.md; no n_i > 1 claim",
              "cases": [verify(m, d, rng) for m, d in ((3, 2), (3, 4), (5, 2), (5, 4))]}
    body = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(body, encoding="utf-8")
    print(body, end="")


if __name__ == "__main__":
    main()
