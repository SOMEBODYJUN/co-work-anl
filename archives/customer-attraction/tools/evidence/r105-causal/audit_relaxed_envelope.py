#!/usr/bin/env python3
"""Finite exact formula audit; no catalogue, policy or SPE is constructed."""
from fractions import Fraction as Q
import json


def envelope(b, r, q):
    return q * (1 - q) / (b + 1) + q * q / (b + r + 1) - q / (b + r)


cases = 0
parameter_points = 0
for b in range(6):
    for r in range(1, 9):
        parameter_points += 1
        for j in range(13):
            q = Q(j, 12)
            observed = []
            for k0 in range(r):
                for k1 in range(r):
                    f0, f1 = Q(1, b + 1 + k0), Q(1, b + 1 + k1)
                    ef = (1 - q) * f0 + q * f1
                    d = q * f1
                    c = q * ((1 - q) * f0 + q * Q(1, b + 2 + k1))
                    covariance = q * f1 - q * ef
                    insertion_credit = q * q / ((b + 1 + k1) * (b + 2 + k1))
                    assert d - c == covariance + insertion_credit
                    assert c - d <= envelope(b, r, q)
                    observed.append(c - d)
                    cases += 1
            assert max(observed) == envelope(b, r, q)
        if r == 1:
            assert envelope(b, r, Q(0)) == 0
        else:
            qstar = Q((r - 1) * (b + r + 1), 2 * r * (b + r))
            emax = Q((r - 1) ** 2 * (b + r + 1), 4 * r * (b + 1) * (b + r) ** 2)
            a = Q(r - 1, (b + 1) * (b + r))
            d = Q(r, (b + 1) * (b + r + 1))
            assert 0 < qstar < Q(1, 2)
            assert qstar == a / (2 * d)
            assert envelope(b, r, qstar) == emax == a * a / (4 * d)
            for j in range(13):
                q = Q(j, 12)
                assert envelope(b, r, q) == emax - d * (q - qstar) ** 2

assert envelope(0, 5, Q(12, 25)) == Q(24, 125)
assert envelope(0, 2, Q(3, 8)) == Q(3, 32)
print(json.dumps({
    "status": "PASS",
    "scope": "finite scalar conditional-load relaxation; no SPE realization or half result",
    "parameter_domain": {"b": [0, 5], "r": [1, 8], "q": "j/12 for j=0,...,12", "k0_k1": "0,...,r-1"},
    "deterministic_conditional_law_cases": cases,
    "parameter_points_for_exact_vertex_substitution": parameter_points,
    "checks": ["reciprocal covariance plus insertion identity", "upper envelope", "enumerated endpoint maximum", "quadratic vertex and completed square"],
    "source_m5_substitution": {"qstar": "12/25", "maximum": "24/125"},
    "two_player_relaxation_substitution": {"qstar": "3/8", "maximum": "3/32"},
    "limitation": "The universal theorem follows from the proof, not this finite arithmetic audit. No original research program was run."
}, ensure_ascii=False, indent=2))
