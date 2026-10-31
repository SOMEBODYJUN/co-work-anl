#!/usr/bin/env python3
"""Exact finite audit of arbitrary sparse slots, clocks and skip premiums."""
from fractions import Fraction as F
from itertools import product
import json


def subsets(values):
    values = tuple(values)
    for bits in product((0, 1), repeat=len(values)):
        yield tuple(v for v, chosen in zip(values, bits) if chosen)


def row(path, j, slots, rho):
    # A single customer's 0/1 memberships; slots and prefixes are 1-indexed.
    prefix = [0]
    for v in path:
        prefix.append(prefix[-1] + v)
    h = prefix[j]
    selected = [t for t in slots if path[t - 1]]
    reset = h * (1 / (rho + h) - 1 / (rho + h + len(selected)))
    clock = sum((F(h) / ((rho + prefix[t - 1]) * (rho + prefix[t]))
                 for t in selected), F(0))
    premium = F(0)
    for k, t in enumerate(selected, 1):
        a, b = h + k, prefix[t]
        assert b >= a
        premium += F(h) * (b - a) * (2 * rho + a + b - 1) / (
            (rho + a - 1) * (rho + a) * (rho + b - 1) * (rho + b)
        )
    assert reset == clock + premium
    assert premium >= 0 and clock >= 0
    return reset, clock, premium


def audit_family(path, selections, weights, rho):
    m = len(path)
    congestion = [F(0)] * m
    total_clock = F(0)
    for j, slots in selections.items():
        theta = weights[j]
        total_clock += theta * row(path, j, slots, rho)[1]
        for t in slots:
            congestion[t - 1] += j * theta
    gamma = max(congestion, default=F(0))
    c = sum(path)
    credit = (1 / (rho + 1) - 1 / (rho + c)) if c else F(0)
    assert total_clock <= gamma * credit
    return total_clock


def main():
    row_cases = 0
    family_cases = 0
    reserves = (F(1, 3), F(1), F(5, 2))
    for m in range(1, 9):
        for path in product((0, 1), repeat=m):
            for j in range(1, m):
                for slots in subsets(range(j + 1, m + 1)):
                    for rho in reserves:
                        row(path, j, slots, rho)
                        row_cases += 1
            # Distinct nonuniform, noncontiguous families; the row formula
            # itself is exhaustively checked above for every sparse subset.
            for family in range(3):
                selections = {
                    j: tuple(t for t in range(j + 1, m + 1)
                             if (t + (family + 1) * j) % (family + 2) == 0)
                    for j in range(1, m)
                }
                weights = {j: F((j % 3) + 1, j * (family + 1))
                           for j in range(1, m)}
                for rho in reserves:
                    audit_family(path, selections, weights, rho)
                    family_cases += 1
    spe_family_cases = 0
    for q in range(2, 100):
        path = (1,) + (0,) * q + (1,) * (q - 1)
        reset = clock = premium = F(0)
        for j in range(1, q):
            vals = row(path, j, (q + 1 + j,), F(1))
            reset += vals[0] / j
            clock += vals[1] / j
            premium += vals[2] / j
        harmonic = sum((F(1, j) for j in range(1, q)), F(0))
        assert reset == harmonic / 6
        assert clock == F(1, 4) - F(1, 2 * q * (q + 1))
        assert premium == harmonic / 6 - F(1, 4) + F(1, 2 * q * (q + 1))
        spe_family_cases += 1
    print(json.dumps({
        "scope": "finite exact audit; adjacent proof covers arbitrary paths and m",
        "all_binary_paths_m": [1, 8],
        "all_sparse_subsets_row_cases": row_cases,
        "nonuniform_sparse_family_budget_cases": family_cases,
        "rho_values": [str(rho) for rho in reserves],
        "complete_spe_family_identity_q": [2, 99],
        "complete_spe_family_cases": spe_family_cases,
        "rho1_clock_total": "1/4 - 1/(2q(q+1))",
        "rho1_skip_premium_total": "H_(q-1)/6 - 1/4 + 1/(2q(q+1))",
        "general_target": "OPEN; no real full-tree transport established"
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
