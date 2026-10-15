#!/usr/bin/env python3
"""独立逐负载审计：奇环缺陷 selector 的完整签名 dual 与支撑边界。

All inputs are in this source; no repository module, solver, random seed,
floating-point tolerance, or author implementation is used.  This finite audit
checks identities and explicit certificates, not the infinite mathematical
quantifiers in the accompanying proof.
"""

from fractions import Fraction
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import platform
import sys


def states(n):
    return tuple(product((0, 1), repeat=n))


def defects(s):
    return tuple(i for i in range(len(s)) if s[i] == s[(i + 1) % len(s)])


def flipped(s, i):
    t = list(s)
    t[i] = 1 - t[i]
    return tuple(t)


def one_defect_cycle(n):
    q = tuple(s for s in states(n) if len(defects(s)) == 1)
    assert len(q) == 2 * n
    s = q[0]
    orbit = []
    while s not in orbit:
        orbit.append(s)
        s = flipped(s, defects(s)[0])
    assert s == orbit[0] and len(orbit) == 2 * n and set(orbit) == set(q)
    for i in range(n):
        for b in (0, 1):
            assert sum(defects(s)[0] == i and s[i] == b for s in orbit) == 1
    return tuple(orbit)


def is_proper(mask, n):
    return all(((mask >> (2 * i)) & 3) != 3 for i in range(n))


def current_cost(s, i, mask, k, weight):
    if not ((mask >> (2 * i + s[i])) & 1):
        return Fraction(0)
    users = sum((mask >> (2 * j + s[j])) & 1 for j in range(len(s)))
    # In particular k=0 is evaluated only for a user, hence no 0/0 or 0^0.
    return (weight * users) ** k


def margin(s, i, mask, k, alpha, weight):
    return current_cost(s, i, mask, k, weight) - alpha * current_cost(
        flipped(s, i), i, mask, k, weight
    )


def edge_pair_mask(i, b, n):
    return (1 << (2 * i + b)) | (1 << (2 * ((i + 1) % n) + b))


def audit_local_rows():
    cases = []
    for n in (3, 5, 7):
        for d in (1, 2, 4):
            p = 2**d
            for alpha in (Fraction(1), Fraction(3, 2), Fraction(p) - Fraction(1, 3)):
                assert 1 <= alpha < p
                for weight in (Fraction(1), Fraction(2, 3)):
                    checks = 0
                    for s in states(n):
                        ds = defects(s)
                        assert ds
                        # Enumerate every allowed move, not only a chosen selector.
                        for mover in ds:
                            for edge in range(n):
                                pair = sum(
                                    margin(s, mover, edge_pair_mask(edge, b, n), d, alpha, weight)
                                    for b in (0, 1)
                                )
                                if mover == edge:
                                    expected = weight**d * (p - alpha)
                                elif mover == (edge + 1) % n:
                                    expected = weight**d * (
                                        p - alpha if s[edge] == s[(edge + 1) % n] else 1 - alpha * p
                                    )
                                    assert pair >= weight**d * (1 - alpha * p)
                                else:
                                    expected = 0
                                assert pair == expected
                                checks += 1
                            # Both singleton degree-zero direction constraints.
                            for b in (0, 1):
                                got = margin(s, mover, 1 << (2 * mover + b), 0, alpha, weight)
                                assert got == (1 if s[mover] == b else -alpha)
                                checks += 1
                    r = Fraction(p - alpha, alpha * p - 1)
                    beta = r ** (n - 1) / sum(r**j for j in range(n))
                    assert 0 < r <= 1 and 0 < beta <= Fraction(1, n)
                    assert 1 / sum(r ** (-j) for j in range(n)) == beta
                    # Uniform cycle masses obey the lower bound, equality at alpha=1.
                    assert Fraction(1, 2 * n) >= beta / (1 + alpha)
                    if alpha == 1:
                        assert beta == Fraction(1, n)
                    cases.append({"n": n, "d": d, "alpha": str(alpha), "common_weight": str(weight), "checks": checks})
    return cases


def audit_column_certificates():
    cases = []
    for n, cone, max_d in ((3, "full", 4), (5, "full", 3), (7, "proper", 2)):
        q = one_defect_cycle(n)
        masks = tuple(mask for mask in range(1, 1 << (2 * n)) if cone == "full" or is_proper(mask, n))
        for weight in (Fraction(1), Fraction(2, 3)):
            for d in range(1, max_d + 1):
                alpha = Fraction(2**d) - Fraction(1, 3)
                cycle_checks = endpoint_checks = singleton_checks = 0
                u = (0,) * n
                v = (1, 1) + (0,) * (n - 2)
                assert min(defects(u)) == min(defects(v)) == 0
                for mask in masks:
                    for k in range(d + 1):
                        # Evaluate actual state costs; no potential formula used here.
                        at_one = sum(margin(s, defects(s)[0], mask, k, Fraction(1), weight) for s in q)
                        interior = sum(margin(s, defects(s)[0], mask, k, alpha, weight) for s in q)
                        assert at_one == 0 and interior <= 0
                        cycle_checks += 2
                        for endpoint_alpha in (Fraction(2**d), Fraction(2**d) + Fraction(5, 7)):
                            endpoint_sum = margin(u, 0, mask, k, endpoint_alpha, weight) + margin(v, 0, mask, k, endpoint_alpha, weight)
                            assert endpoint_sum <= 0
                            endpoint_checks += 1
                # No point mass is a dual for a no-self-loop selector: a current-action singleton attacks it.
                for s in states(n):
                    mover = min(defects(s))
                    witness = 1 << (2 * mover + s[mover])
                    assert is_proper(witness, n)
                    assert margin(s, mover, witness, 0, Fraction(2**d), weight) == 1
                    singleton_checks += 1
                cases.append({"n": n, "cone": cone, "d": d, "common_weight": str(weight), "signatures": len(masks), "cycle_states": len(q), "cycle_column_checks": cycle_checks, "endpoint_column_checks": endpoint_checks, "point_mass_attacks": singleton_checks})
    return cases


def audit_excluded_boundaries():
    even = []
    for n in (2, 4, 6, 8):
        alternating = tuple(i % 2 for i in range(n))
        assert defects(alternating) == ()
        assert defects(tuple(1 - b for b in alternating)) == ()
        even.append({"n": n, "alternating_states_without_defect": 2})
    degree_zero = []
    for n in (3, 5):
        u = (0,) * n
        v = (1, 1) + (0,) * (n - 2)
        assert min(defects(u)) == min(defects(v)) == 0
        checks = 0
        for mask in range(1, 1 << (2 * n)):
            # d=0 has endpoint 2^d=1, and already admits a single-mover dual.
            assert margin(u, 0, mask, 0, Fraction(1), Fraction(1)) + margin(v, 0, mask, 0, Fraction(1), Fraction(1)) == 0
            checks += 1
        degree_zero.append({"n": n, "d": 0, "alpha": "1", "full_signature_checks": checks, "dual_mover_support": 1})
    return {"even_n": even, "degree_zero": degree_zero}


def main():
    local = audit_local_rows()
    columns = audit_column_certificates()
    boundaries = audit_excluded_boundaries()
    print(json.dumps({
        "audit": "奇环缺陷择证的独立逐负载核验",
        "status": "passed",
        "python": platform.python_version(),
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "command": sys.argv,
        "arithmetic": "fractions.Fraction; exact; no tolerance",
        "inputs": "Fully embedded deterministic states, degrees, alpha values, common weights and signature cones in this source",
        "random_seed": None,
        "scope": "Finite row identities, explicit full/proper cycle duals, endpoint two-point duals, quantitative bound algebra and point-mass obstructions only; not an infinite-quantifier proof",
        "local_cases": local,
        "column_cases": columns,
        "excluded_boundaries": boundaries,
        "totals": {
            "local_cases": len(local),
            "local_row_checks": sum(x["checks"] for x in local),
            "column_cases": len(columns),
            "cycle_column_checks": sum(x["cycle_column_checks"] for x in columns),
            "endpoint_column_checks": sum(x["endpoint_column_checks"] for x in columns),
            "point_mass_attacks": sum(x["point_mass_attacks"] for x in columns),
            "degree_zero_full_signature_checks": sum(x["full_signature_checks"] for x in boundaries["degree_zero"]),
        },
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
