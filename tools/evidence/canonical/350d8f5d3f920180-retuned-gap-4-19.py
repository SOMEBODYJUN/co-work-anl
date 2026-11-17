#!/usr/bin/env python3
"""Check the finite gap for the retuned fourteen-resource family exactly."""

from itertools import product
from math import lcm

MASKS = (
    (0, 1, 0, 1), (0, 1, 1, 2), (1, 0, 2, 2), (1, 1, 0, 0),
    (1, 1, 2, 0), (1, 1, 2, 2), (1, 2, 1, 1),
)
AMPLITUDE_NUMERATORS = (49, 110, 49, 60, 2, 3, 100)
STATES = tuple(product((0, 1), repeat=4))
WITNESSES = (2, 2, 3, 0, 3, 2, 3, 1)


def check(m):
    weights = (100 * m, 10, 5, 2)
    degrees = (32 * m * m,) * 6 + (2,)
    supports = [tuple(i for i, bit in enumerate(mask) if bit) for mask in MASKS]
    denominators = [
        sum(weights[i] for i in support) ** degree
        for support, degree in zip(supports, degrees)
    ]
    common = lcm(*denominators)

    # Every cost below is scaled by the same positive integer 100 * common.
    fees = []
    for support, amplitude, denominator, degree in zip(
        supports, AMPLITUDE_NUMERATORS, denominators, degrees
    ):
        loads = {
            sum(weights[i] for i, used in zip(support, bits) if used)
            for bits in product((0, 1), repeat=len(support))
        }
        scale = amplitude * (common // denominator)
        fees.append({load: scale * load**degree for load in loads})

    costs = {}
    for state in STATES:
        row = [0] * len(weights)
        for mask, fee in zip(MASKS, fees):
            for side in (0, 1):
                users = [
                    i for i, label in enumerate(mask)
                    if label and (state[i] ^ side) == label - 1
                ]
                resource_cost = fee[sum(weights[i] for i in users)]
                for i in users:
                    row[i] += resource_cost
        costs[state] = row

    best_margins = []
    witness_margins = []
    for state in STATES:
        margins = []
        for i in range(len(weights)):
            deviation = state[:i] + (1 - state[i],) + state[i + 1:]
            margins.append(costs[state][i] - 2 * costs[deviation][i])
        best_margins.append(max(margins))
        b, c, d = (bit ^ state[0] for bit in state[1:])
        witness_margins.append(margins[WITNESSES[4 * b + 2 * c + d]])

    best = min(best_margins)
    witness = min(witness_margins)
    denominator = 100 * common
    return best > 0, witness > 0, best * 10**6 // denominator, witness * 10**6 // denominator


if __name__ == '__main__':
    for m in range(4, 20):
        all_states_strict, fixed_witnesses_strict, best_floor, fixed_floor = check(m)
        if not all_states_strict or not fixed_witnesses_strict:
            raise ArithmeticError(f'Strict all-state coverage failed at m={m}')
        print(m, all_states_strict, fixed_witnesses_strict, best_floor, fixed_floor, flush=True)
