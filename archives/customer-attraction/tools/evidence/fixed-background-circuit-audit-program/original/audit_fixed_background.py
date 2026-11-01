#!/usr/bin/env python3
"""Definition-level Fraction audit of fixed-background circuit slices.

No optimization, canonical CAG solver, or earlier circuit code is imported.
The general conclusions are proved in the accompanying manuscript.
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def rank(rows):
    a = [[F(x) for x in row] for row in rows]
    if not a:
        return 0
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        z = a[r][c]
        a[r] = [x / z for x in a[r]]
        for i in range(r + 1, len(a)):
            if a[i][c]:
                z = a[i][c]
                a[i] = [x - z * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def payoff(count, topic, interest):
    if not interest[topic]:
        return F(0)
    load = sum(x * y for x, y in zip(count, interest))
    assert load > 0
    return F(1, load)


def rows_from_customers(M, background):
    patterns = list(product((0, 1), repeat=2 + len(background)))
    arows = []
    zrows = []
    for j in range(1, M + 1):
        qa = (j, M-j, *background)
        qz = (M-j, j, *background)
        assert sum(qa) == M + sum(background) == sum(qz)
        arows.append([payoff(qa, 0, b) for b in patterns])
        zrows.append([payoff(qz, 1, b) for b in patterns])
    return patterns, arows + zrows


def residue_vector(M, loads, support):
    out = [F(0)] * M
    for j in support:
        numerator = denominator = 1
        for t in loads:
            numerator *= j + t
        for ell in support:
            if ell != j:
                denominator *= j - ell
        out[j-1] = F(numerator, denominator)
    return out


def verify_case(M, bg):
    patterns, rows = rows_from_customers(M, bg)
    loads = sorted({sum(v*c for v, c in zip(bg, p))
                    for p in product((0, 1), repeat=len(bg))})
    assert loads[0] == 0
    d = len(loads)
    expected = min(2*M, 2*d+1)
    actual = rank(rows)
    assert actual == expected, (M, bg, loads, actual, expected)
    circuits = []
    if d < M:
        j0 = list(range(1, d+2))
        h0 = residue_vector(M, loads, j0)
        assert sum(h0) == 1
        circuits.append(h0 + [-x for x in h0])
        for r in range(d+2, M+1):
            h = residue_vector(M, loads, j0 + [r])
            assert sum(h) == 0
            circuits.extend((h + [F(0)]*M, [F(0)]*M + h))
    assert len(circuits) == 2*M - actual
    assert rank(circuits) == len(circuits)
    for circuit in circuits:
        assert any(x > 0 for x in circuit) and any(x < 0 for x in circuit)
        for column in zip(*rows):
            assert sum(x*y for x, y in zip(circuit, column)) == 0
    return {"M": M, "background": list(bg), "m": M+sum(bg),
            "loads": loads, "d": d, "customer_patterns": len(patterns),
            "rank": actual, "complete_basis_size": len(circuits)}


def verify_four(r, s, bg):
    assert r > s >= 1 and bg
    M = r + s
    patterns = list(product((0, 1), repeat=2+len(bg)))
    slots = (((r, s, *bg), 0), ((s, r, *bg), 1),
             ((s, r, *bg), 0), ((0, M, *bg), 1))
    rows = [[payoff(q, a, b) for b in patterns] for q, a in slots]
    assert rank(rows) == 4, (r, s, bg)
    return 1


def aggregate_rows(M, bg):
    patterns, rows = rows_from_customers(M, bg)
    for j in range(M+1):
        q = (j, M-j, *bg)
        rows.append([sum(v * payoff(q, c+2, b)
                         for c, v in enumerate(bg)) for b in patterns])
    return patterns, rows


def aggregate_coefficients(M, x, y, gamma):
    assert sum(x) + sum(y) == 0
    assert gamma[0] == sum(x[j-1] / j for j in range(1, M+1))
    assert gamma[M] == sum(y[j-1] / j for j in range(1, M+1))
    assert sum(gamma) == 0
    alpha = [x[j-1] + j*gamma[j] for j in range(1, M+1)]
    beta = [y[j-1] + j*gamma[M-j] for j in range(1, M+1)]
    return alpha + beta + gamma


def verify_aggregate(M, bg):
    patterns, rows = aggregate_rows(M, bg)
    loads = sorted({sum(v*c for v, c in zip(bg, p))
                    for p in product((0, 1), repeat=len(bg))})
    d = len(loads)
    assert d >= 2 and M >= 2
    expected = min(2*d+2, 2*M+3)
    actual = rank(rows)
    assert actual == expected, (M, bg, actual, expected)
    circuits = []
    zero = [F(0)] * M
    for j in range(2, M):
        gamma = [F(0)]*(M+1)
        gamma[j], gamma[1] = F(1), F(-1)
        circuits.append(aggregate_coefficients(M, zero, zero, gamma))
    if d <= M:
        j0 = list(range(1, d+1))
        h0 = residue_vector(M, loads[1:], j0)
        assert sum(h0) == 1
        c0 = sum(h0[j-1]/j for j in range(1, M+1))
        gamma = [c0] + [F(0)]*(M-1) + [-c0]
        circuits.append(aggregate_coefficients(M, h0, [-x for x in h0], gamma))
        for r in range(d+1, M+1):
            h = residue_vector(M, loads[1:], j0+[r])
            assert sum(h) == 0
            ch = sum(h[j-1]/j for j in range(1, M+1))
            gamma = [ch, -ch] + [F(0)]*(M-1)
            circuits.append(aggregate_coefficients(M, h, zero, gamma))
            gamma = [F(0), -ch] + [F(0)]*(M-2) + [ch]
            circuits.append(aggregate_coefficients(M, zero, h, gamma))
    assert len(circuits) == 3*M+1-actual
    assert rank(circuits) == len(circuits)
    for circuit in circuits:
        for column in zip(*rows):
            assert sum(x*y for x, y in zip(circuit, column)) == 0
    return {"M": M, "background": list(bg), "d": d,
            "rows": len(rows), "rank": actual, "complete_basis_size": len(circuits)}


def verify_all_unit(M, k):
    bg = (1,)*k
    patterns, rows = rows_from_customers(M, bg)
    for j in range(M+1):
        q = (j, M-j, *bg)
        for c in range(k):
            rows.append([payoff(q, c+2, b) for b in patterns])
    actual = rank(rows)
    assert actual == len(rows)-(M-2), (M, k, actual)
    return {"M": M, "k": k, "rows": len(rows), "rank": actual,
            "kernel_dimension": M-2}


def verify_six(k):
    for b in product((0, 1), repeat=3):
        left = (2*(k+1)*payoff((1,1,k), 0, b)
                + 4*(k+1)*payoff((0,2,k), 1, b)
                + k*k*payoff((0,2,k), 2, b))
        right = (2*(k+1)*payoff((1,1,k), 1, b)
                 + 4*(k+1)*payoff((2,0,k), 0, b)
                 + k*k*payoff((2,0,k), 2, b))
        assert left == right, (k, b, left, right)
    return 1


def main():
    backgrounds = [(), (1,), (2,), (5,), (1,1), (1,2), (2,2),
                   (1,3), (1,1,1), (1,2,4), (2,3,5), (1,1,1,1)]
    cases = [verify_case(M, bg) for bg in backgrounds for M in range(1,9)]
    four = sum(verify_four(r, s, bg) for bg in backgrounds if bg
               for r in range(2,7) for s in range(1,r))
    aggregate = [verify_aggregate(M, bg) for bg in backgrounds if bg
                 for M in range(2,9)]
    all_unit = [verify_all_unit(M, k) for M in range(2,6) for k in range(M,7)]
    six = sum(verify_six(k) for k in range(1,9))
    report = {"status": "passed", "identity": "FB-RANK / FB-BASIS / FB-FOUR",
              "scope": "Finite definition-level audit; general proof is in manuscript.",
              "cases": cases, "case_count": len(cases),
              "four_slot_cases": four,
              "circuit_vectors_checked": sum(c["complete_basis_size"] for c in cases),
              "all_backgrounds_include_zero_load": True,
              "aggregate_cases": aggregate, "aggregate_case_count": len(aggregate),
              "aggregate_circuit_vectors_checked": sum(c["complete_basis_size"] for c in aggregate),
              "all_unit_cases": all_unit, "all_unit_case_count": len(all_unit),
              "six_row_parameter_cases": six}
    target = Path(__file__).with_name("fixed_background_audit.json")
    target.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items()
                      if k not in ("cases", "aggregate_cases", "all_unit_cases")}))


if __name__ == "__main__":
    main()
