"""Exact local row generator for arbitrary-horizon common-catalogue CAG.

This implements a proved necessary inequality, not a half-coverage solver.
All input prices are nonnegative rationals. Zero-numerator shares are zero.
"""

from fractions import Fraction
from itertools import product


def _rational(value):
    if isinstance(value, float):
        raise TypeError("Use an exact rational, not a float")
    return Fraction(value)


def _inputs(p, ell, t, q, alpha, beta, mu):
    if not isinstance(p, int) or not isinstance(ell, int) or min(p, ell) < 0:
        raise ValueError("Background loads must be nonnegative integers")
    if t not in (0, 1) or q not in (0, 1):
        raise ValueError("Memberships must be binary")
    alpha, beta = tuple(map(_rational, alpha)), tuple(map(_rational, beta))
    mu = _rational(mu)
    if not alpha or len(alpha) != len(beta):
        raise ValueError("Specify equally many nonempty follower coefficients")
    if min((*alpha, *beta, mu)) < 0:
        raise ValueError("Legal row multipliers must be nonnegative")
    return alpha, beta, mu


def _share(numerator, denominator):
    return Fraction(numerator, denominator) if numerator else Fraction(0)


def branch_value(p, ell, t, q, hidden, alpha, beta, mu):
    """Literal coefficient before eliminating the actual hidden memberships."""
    alpha, beta, mu = _inputs(p, ell, t, q, alpha, beta, mu)
    hidden = tuple(hidden)
    if len(hidden) != len(alpha) or any(f not in (0, 1) for f in hidden):
        raise ValueError("Specify one binary membership per follower")
    z = p + t + sum(hidden)
    return (_share(t, z)
            + sum((b + a / (ell + 1)) * f
                  for a, b, f in zip(alpha, beta, hidden))
            - mu * _share(hidden[-1], z)
            + mu * Fraction(q, p + t + sum(hidden[:-1]) + 1))


def projected(p, ell, t, q, alpha, beta, mu):
    """Reference binary enumeration; exponential in the number of followers."""
    alpha, beta, mu = _inputs(p, ell, t, q, alpha, beta, mu)
    return min(branch_value(p, ell, t, q, f, alpha, beta, mu)
               for f in product((0, 1), repeat=len(alpha)))


def projected_by_count(p, ell, t, q, alpha, beta, mu):
    """Exact minimum using sorted costs and 2r candidates for r followers.

    This compression applies to the stated source IC, last reply IC, and
    separate price/capacity rows. Extra identity-sensitive rows need a new proof.
    """
    alpha, beta, mu = _inputs(p, ell, t, q, alpha, beta, mu)
    costs = tuple(b + a / (ell + 1) for a, b in zip(alpha, beta))
    prefix = [Fraction(0)]
    for cost in sorted(costs[:-1]):
        prefix.append(prefix[-1] + cost)
    return min(_share(t, p + t + s + g)
               - mu * _share(g, p + t + s + g)
               + prefix[s] + costs[-1] * g
               + mu * Fraction(q, p + t + s + 1)
               for s in range(len(alpha)) for g in (0, 1))
