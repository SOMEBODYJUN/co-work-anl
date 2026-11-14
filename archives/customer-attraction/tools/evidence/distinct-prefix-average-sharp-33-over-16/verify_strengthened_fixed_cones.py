"""Verify two exact strengthened-cone comparisons for the same fixed policy."""

import json
import sys
from fractions import Fraction
from functools import cache
from itertools import combinations, product
from pathlib import Path


# The companion verifier is colocated when published and kept in a sibling draft directory here.
draft_companion = Path(__file__).resolve().parent.parent / "new-theorem"
if draft_companion.is_dir():
    sys.path.insert(0, str(draft_companion))
from verify_fixed_average_33_over_16 import ACTIONS, COMPARISON, MASKS, PLAYERS, TOPICS, includes, payoff_column


def check():
    actions = {
        h: int(a)
        for depth, digits in enumerate(ACTIONS)
        for h, a in zip(product(TOPICS, repeat=depth), digits, strict=True)
    }

    @cache
    def finish(h):
        return h if len(h) == PLAYERS else finish(h + (actions[h],))

    def payoff_difference(h, alternative, mask):
        return payoff_column(mask, actions[h], finish(h)) - payoff_column(
            mask, alternative, finish(h + (alternative,))
        )

    def coverage(mask, group):
        return int(any(includes(mask, a) for a in group))

    def group_coverage(group, customers):
        return sum(coverage(mask, group) * count for mask, count in customers.items())

    def values(row, customers):
        return sum(row[mask] * count for mask, count in customers.items())

    def check_cone(label, rows, certificate, customers, bound, remainder_formula):
        w = {mask: coverage(mask, finish(())) for mask in MASKS}
        o = {mask: coverage(mask, COMPARISON) for mask in MASKS}
        rho = {
            mask: bound * w[mask] - o[mask] - sum(
                weight * rows[key][mask] for key, weight in certificate.items()
            )
            for mask in MASKS
        }
        assert all(rho[mask] == remainder_formula(mask) for mask in MASKS)
        assert min(rho.values()) >= 0
        assert min(values(row, customers) for row in rows.values()) >= 0
        assert all(values(rows[key], customers) == 0 for key in certificate)
        assert all(rho[mask] == 0 for mask in customers)
        W, O = values(w, customers), values(o, customers)
        OPT = max(group_coverage(group, customers) for group in combinations(TOPICS, PLAYERS))
        assert O == OPT
        assert Fraction(O, W) == bound and O == W * bound
        return {
            "scope": label,
            "row_count": len(rows),
            "customers": customers,
            "W": W,
            "O_J": O,
            "OPT": OPT,
            "bound": str(bound),
            "dual": [
                {"row": key, "weight": str(weight),
                 "coefficients_in_mask_order": [str(rows[key][mask]) for mask in MASKS]}
                for key, weight in certificate.items()
            ],
            "rho_in_mask_order": [str(rho[mask]) for mask in MASKS],
            "witness_slacks": [
                {"row": key, "slack": str(values(row, customers))} for key, row in rows.items()
            ],
        }

    full_history = {
        h: {
            mask: sum(payoff_difference(h, a, mask) for a in COMPARISON) / len(COMPARISON)
            for mask in MASKS
        }
        for h in actions
    }
    individual = {
        (h, a): {mask: payoff_difference(h, a, mask) for mask in MASKS}
        for h in actions
        if len(h) == len(set(h)) and COMPARISON.issuperset(h)
        for a in sorted(COMPARISON.difference(h))
    }
    assert len(full_history) == 156 and len(individual) == 64

    def full_history_remainder(mask):
        a, x, y, z = (int(includes(mask, topic)) for topic in (2, 1, 3, 4))
        return a + Fraction(x + y + z, 1 + 3 * a) - int(bool(a + x + y + z))

    def individual_remainder(mask):
        a, x, y, z = (int(includes(mask, topic)) for topic in (2, 1, 3, 4))
        return (a * (Fraction(4, 3) - Fraction(1, 3 + y))
                + Fraction(x + y, 1 + 3 * a) + Fraction(z, 1 + 2 * a + y)
                - int(bool(a + x + y + z)))

    return [
        check_cone("All histories; at each node average all four J actions.",
                   full_history, {(2, 2, 2): Fraction(4)}, {4: 20, 5: 8, 9: 21},
                   Fraction(7, 4), full_history_remainder),
        check_cone("Same distinct J prefixes; keep unused J deviations individually.",
                   individual, {((2,), 1): Fraction(1), ((2,), 3): Fraction(1),
                                ((2, 3), 4): Fraction(1)},
                   {3: 3, 5: 12, 9: 3, 17: 4}, Fraction(11, 6), individual_remainder),
    ]


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
