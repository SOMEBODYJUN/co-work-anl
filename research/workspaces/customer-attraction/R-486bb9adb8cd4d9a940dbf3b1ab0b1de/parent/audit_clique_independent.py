#!/usr/bin/env python3
"""Independent definition-level audit; no author or CAG imports."""
from fractions import Fraction as F
from itertools import product, combinations
from collections import defaultdict
import hashlib
import json
from pathlib import Path


def choose2(n):
    return n * (n - 1) // 2


def audit():
    checked = groups = 0
    for q, families in [(1, 6), (2, 5), (3, 4), (4, 3)]:
        observed = defaultdict(lambda: 10**9)
        for bits in product((0, 1), repeat=q * families):
            rows = [bits[r*q:(r+1)*q] for r in range(families)]
            counts = tuple(map(sum, rows))
            intersections = sum(sum(a*b for a, b in zip(rows[r], rows[s]))
                                for r, s in combinations(range(families), 2))
            columns = tuple(sum(rows[r][i] for r in range(families)) for i in range(q))
            assert intersections == sum(map(choose2, columns))
            t, rem = divmod(sum(counts), q)
            lower = q * choose2(t) + rem * t
            frechet = sum(max(0, counts[r]+counts[s]-q)
                          for r, s in combinations(range(families), 2))
            assert intersections >= lower >= frechet
            observed[counts] = min(observed[counts], intersections)
            checked += 1
        for counts, minimum in observed.items():
            t, rem = divmod(sum(counts), q)
            assert minimum == q * choose2(t) + rem * t
            # Independent constructive audit: assign consecutive residues.
            offset = 0
            rows = []
            for count in counts:
                row = [0] * q
                for j in range(offset, offset+count):
                    assert row[j % q] == 0
                    row[j % q] = 1
                rows.append(row)
                offset += count
            actual = sum(sum(rows[r][i]*rows[s][i] for i in range(q))
                         for r, s in combinations(range(families), 2))
            assert actual == minimum
            groups += 1

    # Rebuild actual off-index BR coefficients literally, not by row formula.
    row_checks = 0
    q, families = 2, 3
    edges = [(0, 1), (2, 0), (1, 2)]
    backgrounds = [0, 2, 4]
    weights = [F(2, 3), F(7, 5), F(3, 2)]
    for bits in product((0, 1), repeat=2*q*families):
        z = [bits[r*q:(r+1)*q] for r in range(families)]
        f = [bits[q*families+r*q:q*families+(r+1)*q] for r in range(families)]
        counts = list(map(sum, z))
        exact_total = envelope = F(0)
        for edge, weight in zip(edges, weights):
            r, s = edge
            b = backgrounds[r]
            direct = sum((F(f[r][i]-z[s][j], b+1+z[r][i])
                          for i in range(q) for j in range(q) if j != i), F(0))
            ar, gr = F(1, b+1), F(1, (b+1)*(b+2))
            actor = sum((F(f[r][i], b+1+z[r][i]) for i in range(q)), F(0))
            inter = sum(a*c for a, c in zip(z[r], z[s]))
            formula = (q-1)*actor-(q-1)*ar*counts[s]+gr*(counts[r]*counts[s]-inter)
            assert direct == formula
            ell = max(0, counts[r]+counts[s]-q)
            envelope += weight*((q-1)*actor-(q-1)*ar*counts[s]
                                + gr*(counts[r]*counts[s]-ell))
            exact_total += weight*direct
            row_checks += 1
        t, rem = divmod(sum(counts), q)
        chi = q*choose2(t)+rem*t-sum(max(0, counts[r]+counts[s]-q) for r, s in edges)
        omega = min(weight/F((backgrounds[r]+1)*(backgrounds[r]+2))
                    for (r, s), weight in zip(edges, weights))
        assert exact_total <= envelope-omega*chi

    # All simple odd cycles have >=3 edges; edge-capacity total is 10.
    triangles = list(combinations(range(5), 3))
    for edge in combinations(range(5), 2):
        assert sum(F(1, 3) for tri in triangles if set(edge) <= set(tri)) == 1
    cycle_best = len(triangles)*F(1, 3)
    clique_exact = 4
    assert cycle_best == F(10, 3) < clique_exact
    return {
        "status": "passed",
        "matrix_assignments": checked,
        "prescribed_row_count_groups": groups,
        "direct_BR_coefficient_checks": row_checks,
        "K5_exact_defect": clique_exact,
        "K5_all_cycle_fractional_packing": str(cycle_best),
        "scope": "finite audit of formulas and construction; general proof is in clique_alignment_review.md",
        "no_SPE_claim": True,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
