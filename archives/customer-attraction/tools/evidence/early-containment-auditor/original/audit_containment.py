"""Independent coefficient audit of the existing two-early-containment proof.

This audits a complete coefficient domain, not a bounded collection of games.
The nonnegative global rows still require the SPE semantics in the source note.
"""
from fractions import Fraction as Q
from itertools import product
import json


def share(numerator, denominator):
    return Q(numerator, denominator) if numerator else Q(0)


def audit():
    reduced_count = expanded_count = 0
    smallest = None
    nonzero_smallest = None
    for early in product((0, 1), repeat=4):
        p = sum(early)
        for a, b in product((0, 1), repeat=2):
            if a and not (early[2] and early[3]):
                continue
            total = p + a + b
            actual = [share(e, total) for e in early]
            actual += [share(a, total), share(b, total)]
            assert sum(actual) == int(total > 0)
            for d, ell in product(range(7), repeat=2):
                reduced_count += 1
                # Counts of pairs (t_i,r_i)=(1,1) attain exactly this interval.
                for overlap in range(max(0, d + ell - 6), min(d, ell) + 1):
                    expanded_count += 1
                    both_den = (p + 1) * (p + 2)
                    # Reconstruct the three different true nonnegative row families.
                    S = 6 * actual[4] - Q(d, p + 1) + Q(overlap, both_den)
                    Z = 6 * actual[5] - Q(ell, p + a + 1)
                    V = Q(d * ell - 6 * overlap, both_den)
                    H = [actual[j] - Q(a, 6) for j in (0, 1)]
                    L = actual[5] - Q(a, p + a + 1)
                    rhs = S + Z / 12 + V / 6 + Q(5, 4) * sum(H) + L
                    residual = 2 * int(total > 0) - int(d > 0) - rhs
                    assert residual >= 0, (early, a, b, d, ell, overlap, residual)
                    if smallest is None or residual < smallest:
                        smallest = residual
                    if total or d or ell:
                        if nonzero_smallest is None or residual < nonzero_smallest:
                            nonzero_smallest = residual
    # Independent exact arithmetic for the multiplicity interface.
    product_value = Q(1)
    for r in range(1, 7):
        product_value *= 1 - Q(1, 6 * r)
    factor = 1 - product_value
    beta = 1 / factor
    assert factor == Q(2352949, 6718464)
    assert beta * factor == 1
    assert (1 + beta) / 2 == Q(9071413, 4705898) < 2
    assert 3 - beta == Q(340383, 2352949) > 0
    return {
        "status": "passed",
        "scope": "existing conditional coefficient theorem; no unrestricted HALF-6 claim",
        "reduced_states": reduced_count,
        "states_with_feasible_overlap": expanded_count,
        "minimum_residual": str(smallest),
        "nonzero_state_minimum_residual": str(nonzero_smallest),
        "F6": str(factor),
        "beta": str(beta),
        "multiplicity_two_bound": str((1 + beta) / 2),
        "necessary_single_omission_fraction": str(3 - beta),
    }


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
