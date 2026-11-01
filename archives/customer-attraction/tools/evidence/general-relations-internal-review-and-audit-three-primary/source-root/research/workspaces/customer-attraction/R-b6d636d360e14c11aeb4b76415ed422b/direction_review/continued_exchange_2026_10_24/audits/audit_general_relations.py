#!/usr/bin/env python3
"""Reproduce the original 250-case / 570-identity BG and fixed tax checks.

Standard-library, exact Fraction arithmetic only. This does not certify a full
SPE or prove an arbitrary-input theorem. The fixed seed and sample count are
identical to the initial in-session check; no sample expansion is performed.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from math import prod
from pathlib import Path
from random import Random


def tax_and_product() -> dict:
    """Recompute from customer memberships and the single actual ordered leaf."""
    types = [
        ({"A"}, 2), ({"B"}, 2), ({"T"}, 1),
        ({"T", "D"}, 1), ({"T", "E"}, 1),
        ({"A", "D", "E"}, 3), ({"B", "D", "E"}, 1),
        ({"P"}, 25),
    ]
    leaf = ["P"] * 10 + ["A", "A", "B"]
    m = len(leaf)
    alpha = Q(m - 1, m)
    loads = [sum(t in membership for t in leaf) for membership, _ in types]
    queries = {
        topic: sum(
            (Q(n, 1) / (1 + alpha * c)
             for (membership, n), c in zip(types, loads)
             if topic in membership), Q()
        )
        for topic in "ABTDEP"
    }
    covered_tax = sum(
        (Q(n, 1) / (1 + alpha * c)
         for (_, n), c in zip(types, loads) if c), Q()
    )
    welfare = sum(n for (_, n), c in zip(types, loads) if c)
    gap = m * max(queries.values()) - welfare - covered_tax
    f5 = 1 - prod(1 - Q(1, 5 * r) for r in range(1, 6))
    assert tuple(queries.values()) == (
        Q(65, 37), Q(39, 25), Q(3), Q(2381, 925), Q(2381, 925), Q(325, 133)
    )
    assert welfare == 33 and covered_tax == Q(708669, 123025)
    assert gap == Q(29481, 123025) and f5 == Q(6049, 15625)
    return {
        "customer_type_count": len(types),
        "unit_customer_count": sum(n for _, n in types),
        "players": m,
        "alpha": str(alpha),
        "actual_leaf": leaf,
        "tax_queries": {k: str(v) for k, v in queries.items()},
        "W": welfare,
        "G": str(covered_tax),
        "tax_gap_mM_minus_W_minus_G": str(gap),
        "F_5(5)": str(f5),
        "scope": "fixed actual-leaf arithmetic only; full SPE is not re-audited here",
    }


def bg_checks() -> dict:
    """Exactly the original random-call order, seed and 250 base cases."""
    seed, cases = 26741, 250
    rng = Random(seed)
    checked = 0
    transcript = sha256()
    for case in range(cases):
        n = 8
        catalogue = rng.sample(range(1 << n), rng.randint(1, 4))
        past = [rng.choice(catalogue) for _ in range(rng.randrange(4))]
        r = rng.randint(1, 4)
        covered = 0
        for topic in past:
            covered |= topic

        def union(topics):
            result = 0
            for topic in topics:
                result |= topic
            return result

        def completion(k, base):
            return max((base | union(topics)).bit_count()
                       for topics in product(catalogue, repeat=k))

        tails = {
            action: [rng.choice(catalogue) for _ in range(r - 1)]
            for action in catalogue
        }

        def payoff(action, tail):
            return sum(
                (Q(1, sum((topic >> x) & 1 for topic in past + [action] + tail))
                 for x in range(n) if (action >> x) & 1), Q()
            )

        deviations = {action: payoff(action, tails[action]) for action in catalogue}
        prescribed = max(catalogue, key=lambda action: deviations[action])
        u = deviations[prescribed]
        best = completion(r, covered)
        after_prescribed = completion(r - 1, covered | prescribed)
        delta = best - after_prescribed
        for action in catalogue:
            if completion(r - 1, covered | action) != best:
                continue
            tail_union = union(tails[action])
            d = deviations[action]
            rho = best - (covered | action | tail_union).bit_count()
            new = (action & ~(covered | prescribed)).bit_count()
            theta = new - delta
            t = (action & ~(covered | prescribed | tail_union)).bit_count()
            f = (prescribed & ~(covered | action | tail_union)).bit_count()
            xi = after_prescribed - (covered | prescribed | tail_union).bit_count()
            eta = r * d - new - (r - 1) * t
            gamma = u - d
            assert min(rho, theta, t, f, xi, eta, gamma) >= 0
            lhs = r * (delta - u)
            rhs = (r - 1) * rho - theta - (r - 1) * (f + xi) - eta - r * gamma
            assert lhs == rhs
            transcript.update(json.dumps(
                [case, catalogue, past, r, prescribed, action, tails[action],
                 *map(str, (rho, theta, t, f, xi, eta, gamma, lhs, rhs))],
                separators=(",", ":"),
            ).encode())
            transcript.update(b"\n")
            checked += 1
    assert checked == 570
    return {
        "seed": seed,
        "base_case_count": cases,
        "customers_per_case": 8,
        "catalogue_size_range": [1, 4],
        "past_length_range": [0, 3],
        "remaining_players_range": [1, 4],
        "BG_exact_identity_checks": checked,
        "all_nonnegative_terms_pass": True,
        "all_identity_checks_pass": True,
        "transcript_sha256": transcript.hexdigest(),
        "scope": "arbitrary legal tails with true current-node IC; not full SPE certification or general proof",
        "sample_expansion": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_suffix(".json"))
    args = parser.parse_args()
    result = {
        "schema": 1,
        "status": "pass",
        "arithmetic": "fractions.Fraction only",
        "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "tax_and_product": tax_and_product(),
        "BG": bg_checks(),
    }
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": result["status"],
                      "BG_exact_checks": result["BG"]["BG_exact_identity_checks"],
                      "tax_gap": result["tax_and_product"]["tax_gap_mM_minus_W_minus_G"],
                      "output": str(args.output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
