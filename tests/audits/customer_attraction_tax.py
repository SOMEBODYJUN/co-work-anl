"""Exact atomwise audit of the two-remaining-player tax identity.

This checks the independently stated algebra for every binary membership in
A,B,T,S,Q, including nonzero and huge fixed incumbent loads. It imports neither
the SPE recurrence nor the canonical payoff implementation. The universal
identity is proved by cancellation in the accompanying note, not by this run.
"""

from fractions import Fraction
from itertools import product
import hashlib
import json
from pathlib import Path
import platform
import subprocess


def run():
    checked = 0
    backgrounds = (0, 1, 2, 10, 1000, 10**40)
    for b in backgrounds:
        for a, other, t, s, q in product((0, 1), repeat=5):
            def f(x):
                return Fraction(x, b + 1)

            def g(x, y):
                return Fraction(x * y, (b + 1) * (b + 2))

            def u(x, y):
                return f(x) - g(x, y)

            def r(x, y):
                return u(x, y) + u(y, x)

            left = r(a, other) + g(a, a) - r(t, s)
            right = (u(a, other) - u(t, q)
                     + u(q, t) - u(s, t)
                     + u(other, a) - u(q, a)
                     + g(a, a) - g(a, q) + g(t, s))
            assert left == right
            assert g(a, a) - g(a, q) >= 0
            assert g(t, s) >= 0
            # Also verify the original sharing formulas in the identity.
            count = a + other
            direct = Fraction(count, b + count) if count else Fraction(0)
            assert r(a, other) == direct
            checked += 1
    root = Path(__file__).resolve().parents[2]
    return {
        "audit": "customer_attraction_two_remaining_tax",
        "arithmetic": "fractions.Fraction",
        "scope": "atomwise identity and remainder signs; not a general-m theorem",
        "python_version": platform.python_version(),
        "base_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True).strip(),
        "audit_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "background_loads": list(backgrounds),
        "membership_patterns_per_background": 32,
        "exact_checks": checked,
        "all_identity_and_remainder_checks_pass": True,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
