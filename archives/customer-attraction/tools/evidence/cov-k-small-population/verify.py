"""Exact column certificates for scaled actual load in COV-K, m=2 or 3."""
from fractions import Fraction
from itertools import product
import json

MULTIPLIERS = {
    2: (Fraction(6, 5), Fraction(4, 5)),
    3: (Fraction(1, 20), Fraction(1, 2), Fraction(4, 5), Fraction(17, 10), Fraction(31, 30)),
}
MAX_PAID = {2: Fraction(-7, 15), 3: Fraction(-1, 15)}


def certificate(players):
    weights = MULTIPLIERS[players]
    results = {}
    covered_residuals = []
    for bits in product((0, 1), repeat=players + 1):
        actions, query = bits[:-1], bits[-1]
        load = sum(actions)
        actual_payoffs = [Fraction(a, load) if load else Fraction(0) for a in actions]
        past = sum(actions[:-2])
        penultimate, last = actions[-2:]
        scaled_load = Fraction((players - 1) * load, players)
        difference = (players * query + scaled_load) / (1 + scaled_load) - 2 * bool(load)
        last_row = actual_payoffs[-1] - Fraction(query, 1 + sum(actions[:-1]))
        tax_row = (
            actual_payoffs[-2] + actual_payoffs[-1]
            - Fraction(last, 1 + past)
            - Fraction(query, 1 + past + last)
            + Fraction(penultimate, (1 + past) * (2 + past))
        )
        rows = [last_row, tax_row]
        if players == 3:
            rows[:0] = [actual_payoffs[0] - Fraction(a, 3) for a in bits[1:]]
        residual = difference + sum(weight * row for weight, row in zip(weights, rows))
        results["".join(map(str, bits))] = str(residual)
        if load:
            covered_residuals.append(residual)
        else:
            assert residual == 0
    assert max(covered_residuals) == MAX_PAID[players]
    return {
        "multipliers": list(map(str, weights)),
        "column_residuals": results,
        "scaled_actual_load_bound": str(2 + MAX_PAID[players]),
    }


if __name__ == "__main__":
    print(json.dumps({m: certificate(m) for m in MULTIPLIERS}, indent=2))
