"""Exact onset of 9/5-PNE for the fixed-weight fourteen-resource family.

For d >= 35, each of the four deviation margins at 0111 is bounded
above by its constant term plus its positive decay terms at d = 35.
Complement symmetry transfers the bounds to 1000. The finite checks
separately cover d = 32, 33, 34, 40 and the fixed-weight limit.
"""

from collections import defaultdict
from fractions import Fraction
from itertools import product


ALPHA = Fraction(9, 5)
WEIGHTS = (100, 10, 5, 2)
MASKS = ("0101", "0112", "1022", "1100", "1120", "1122", "1211")
AMPLITUDES = (127, 231, 145, 139, 28, 41, 289)
STATES = tuple("".join(bits) for bits in product("01", repeat=4))
PLAYERS = range(len(WEIGHTS))
WITNESSES = ("0111", "1000")


def flip(state, player):
    return state[:player] + str(1 - int(state[player])) + state[player + 1 :]


def cost_expression(state, player):
    """Return the constant and the terms (amplitude, normalized load)."""
    constant = Fraction(0)
    decay = []
    for pair, (mask, amplitude) in enumerate(zip(MASKS, AMPLITUDES)):
        support = [i for i in PLAYERS if mask[i] != "0"]
        if player not in support:
            continue
        first_side = [i for i in support if int(mask[i]) == 1 + int(state[i])]
        users = first_side if player in first_side else [i for i in support if i not in first_side]
        load = Fraction(sum(WEIGHTS[i] for i in users), sum(WEIGHTS[i] for i in support))
        assert 0 < load <= 1
        if pair == len(MASKS) - 1:
            constant += amplitude * load**2
        elif load == 1:
            constant += amplitude
        else:
            decay.append((amplitude, load))
    return constant, decay


def cost(state, player, degree):
    constant, decay = cost_expression(state, player)
    if degree is None:
        return constant
    return constant + sum(amplitude * load**degree for amplitude, load in decay)


def factors(degree):
    costs = {s: tuple(cost(s, i, degree) for i in PLAYERS) for s in STATES}
    assert all(c > 0 for row in costs.values() for c in row)
    return {
        s: max(Fraction(1), *(costs[s][i] / costs[flip(s, i)][i] for i in PLAYERS))
        for s in STATES
    }


def margin_expression(state, player):
    current, current_decay = cost_expression(state, player)
    changed, changed_decay = cost_expression(flip(state, player), player)
    coefficients = defaultdict(Fraction)
    for amplitude, load in current_decay:
        coefficients[load] += amplitude
    for amplitude, load in changed_decay:
        coefficients[load] -= ALPHA * amplitude
    return current - ALPHA * changed, dict(coefficients)


def main():
    for degree in (32, 33, 34, 40, None):
        state_factors = factors(degree)
        best = min(state_factors.values())
        minimizers = tuple(s for s in STATES if state_factors[s] == best)
        if degree in (32, 33):
            assert all(value > ALPHA for value in state_factors.values())
        else:
            assert best < ALPHA
            assert minimizers == WITNESSES
        if degree is None:
            assert best == Fraction(5235403, 2930833)
        print(f"d={degree if degree is not None else 'limit'} B={float(best):.16f} states={minimizers}")

    rational_caps = (-276, Fraction(-3, 100), -350, -617)
    for player, cap in zip(PLAYERS, rational_caps):
        margin = margin_expression(WITNESSES[0], player)
        assert margin == margin_expression(WITNESSES[1], player)
        constant, coefficients = margin
        assert all(0 < load < 1 for load in coefficients)
        # For all d >= 35, nonpositive terms can be dropped and every
        # remaining load**d is at most load**35.
        upper = constant + sum(
            coefficient * load**35
            for load, coefficient in coefficients.items()
            if coefficient > 0
        )
        assert upper < cap < 0
        print(f"d>=35 player {player + 1}: margin <= {upper} < {cap}")


if __name__ == "__main__":
    main()
