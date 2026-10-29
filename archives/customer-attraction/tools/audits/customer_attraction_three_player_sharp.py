"""Independent exact audit of the universal three-player sharp 5/3 proof.

The 2048 cases are all per-customer membership patterns, not sampled games.
The mathematical proof reduces arbitrary inputs to these finite binary cases.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path


def share(own: int, other: int, final: int) -> F:
    return F(own, own + other + final) if own else F(0)


def residue(a: int, b: int, c: int, p: int, r: int, d: int, ell: int) -> F:
    return (50 * int(a + b + c > 0) - 30 * int(d > 0)
            - 29 * share(a, b, c) - 36 * share(b, a, c) - 57 * share(c, a, b)
            + 2 * p + 3 * r + F(17 * d + 2 * ell, 1 + a + b)
            + F(12 * d, 1 + a) - F(4 * d * ell, (1 + a) * (2 + a))
            + 14 * share(c, p, r) - 3 * share(r, c, p) + F(d, 1 + c + p))


TABLE = {
    "000": ["0", "0", "3/2", "3"],
    "001": ["13/2", "1", "4/3", "1"],
    "010": ["5/2", "5/2", "4", "11/2"],
    "011": ["11/2", "0", "1/3", "0"],
    "100": ["13/2", "13/2", "8", "19/2"],
    "101": ["6", "1/2", "5/6", "1/2"],
    "110": ["1/6", "1/6", "5/3", "19/6"],
    "111": ["11/2", "0", "1/3", "0"],
}


def check() -> dict[str, object]:
    patterns = expansion_checks = corner_checks = lower_checks = 0
    minima: dict[tuple[int, int, int, int, int], F] = {}
    for bits in product((0, 1), repeat=11):
        a, b, c = bits[:3]
        ts, ls = bits[3:6], bits[6:9]
        p, r = bits[9:]
        d, ell = sum(ts), sum(ls)
        h = sum(t * l for t, l in zip(ts, ls))
        den = (1 + a) * (2 + a)
        assert sum((share(t, a, b) for t in ts), F(0)) == F(d, 1 + a + b)
        assert sum((share(l, a, b) for l in ls), F(0)) == F(ell, 1 + a + b)
        assert sum((share(t, a, l) for t, l in zip(ts, ls)), F(0)) == F(d, 1 + a) - F(h, den)
        assert sum((share(l, a, t) for t, l in zip(ts, ls)), F(0)) == F(ell, 1 + a) - F(h, den)
        assert sum((share(ls[j], a, ts[i]) for i in range(3) for j in range(3) if i != j), F(0)) == F(2 * ell, 1 + a) - F(d * ell - h, den)
        assert sum((share(t, c, p) for t in ts), F(0)) == F(d, 1 + c + p)
        expansion_checks += 6

        u1, u2, u3 = share(a, b, c), share(b, a, c), share(c, a, b)
        weighted = (2 * (3 * u1 - p) + 3 * (3 * u1 - r)
                    + 17 * sum((u3 - share(t, a, b) for t in ts), F(0))
                    + 2 * sum((u3 - share(l, a, b) for l in ls), F(0))
                    + 12 * sum((u2 - share(t, a, l) for t, l in zip(ts, ls)), F(0))
                    + 4 * sum((share(ls[i], a, ts[i]) - share(ls[j], a, ts[i]) for i in range(3) for j in range(3) if i != j), F(0))
                    + 14 * (u1 - share(c, p, r))
                    + sum((share(r, c, p) - share(t, c, p) for t in ts), F(0)))
        expanded = (29 * u1 + 36 * u2 + 57 * u3 - 2 * p - 3 * r
                    - F(17 * d + 2 * ell, 1 + a + b) - F(12 * d, 1 + a)
                    + F(4 * d * ell, den) - 14 * share(c, p, r)
                    + 3 * share(r, c, p) - F(d, 1 + c + p))
        assert weighted == expanded
        rho = residue(a, b, c, p, r, d, ell)
        assert 50 * int(a + b + c > 0) - 30 * int(d > 0) == weighted + rho
        assert rho >= 0, bits
        key = a, b, c, p, r
        minima[key] = min(minima.get(key, rho), rho)
        patterns += 1

    corners = ((0, 0), (1, 0), (1, 3), (3, 0), (3, 3))
    for a, b, c, p, r in product((0, 1), repeat=5):
        values = [residue(a, b, c, p, r, d, ell) for d, ell in corners]
        corner_checks += len(values)
        delta = min(values)
        assert delta == minima[a, b, c, p, r]
        assert delta >= 0
        assert delta == F(TABLE[f"{a}{b}{c}"][2 * p + r])
        # The d=0 dependence on ell is nondecreasing.
        assert residue(a, b, c, p, r, 0, 1) - residue(a, b, c, p, r, 0, 0) == F(2, 1 + a + b)
        # For d>=1 every point is its bilinear corner interpolation.
        for d, ell in product((1, 2, 3), (0, 1, 2, 3)):
            xd, xl = F(d - 1, 2), F(ell, 3)
            interp = ((1 - xd) * (1 - xl) * values[1] + (1 - xd) * xl * values[2]
                      + xd * (1 - xl) * values[3] + xd * xl * values[4])
            assert residue(a, b, c, p, r, d, ell) == interp

    # Matching lower instance: three disjoint topics, of sizes (3,1,1),
    # three players, with the complete strategy 'always choose topic 0'.
    for length in range(3):
        for history in product(range(3), repeat=length):
            actual_final = history + (0,) * (3 - length)
            actual_payoff = F(3, actual_final.count(0))
            for deviation in range(3):
                alternate_final = history + (deviation,) + (0,) * (2 - length)
                alternate_payoff = F((3, 1, 1)[deviation], alternate_final.count(deviation))
                assert actual_payoff >= alternate_payoff
                lower_checks += 1
    assert sum((3, 1, 1)) == 5
    assert F(5, 3) == F(50, 30)
    return {
        "claim": "CA-THREE-SHARP-5-3",
        "upper_bound": "5/3",
        "matching_lower_bound": {"topic_sizes": [3, 1, 1], "players": 3, "spe_strategy": "always choose topic 0", "welfare": 3, "optimum": 5},
        "checks": {
            "complete_membership_patterns": patterns,
            "individual_expansion_checks": expansion_checks,
            "bilinear_corner_values": corner_checks,
            "lower_bound_complete_history_action_comparisons": lower_checks,
        },
        "background_corner_minimum_table": TABLE,
        "all_checks_passed": True,
        "scope": "Exact complete per-customer algebra audit and a matching complete-history SPE; no sampled-game inference.",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    encoded = json.dumps(check(), ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
