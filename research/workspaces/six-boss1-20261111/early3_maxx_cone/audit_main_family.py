#!/usr/bin/env python3
"""Independent audit of Main's r=4,5,6 proof; no Main script import.

Only the fixed displayed parameters are entered below. Residuals are rebuilt
as target minus actual per-customer share budgets, at two formal u values.
No optimizer and no game-point file is read by this audit.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import csv
import json

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
PARAMETERS = {4: (F(15), F(2, 3), F(1), F(61, 3), F(23)),
              5: (F(20), F(7, 4), F(3, 5), F(121, 4), F(65, 2)),
              6: (F(25), F(51, 20), F(3, 8), F(206, 5), F(43))}
SOURCE_MD = WORK / "main_prefix_safety_maxx_family.md"
SOURCE_JSON = WORK / "main_prefix_safety_maxx_family.json"
source_hashes = {path.name: sha256(path.read_bytes()).hexdigest() for path in (SOURCE_MD, SOURCE_JSON)}
main_data = json.loads(SOURCE_JSON.read_text())
main_atoms = {(entry["r"], entry["b"], entry["k"], tuple(entry["bits"])): entry for entry in main_data["atoms"]}
assert len(main_atoms) == len(main_data["atoms"]) == 1440
local = json.loads((HERE / "local_table_288.json").read_text())
local_values = {tuple(row["type"]): F(row["optimal_E"]) for row in local["rows"]}


def from_shares(r, b, k, bits, formal_u):
    alpha, s, a, C, old_C = PARAMETERS[r]
    x, terminal, query = bits[0], bits[-2], bits[-1]
    middle = bits[1:-2]
    assert len(middle) == r - 2
    branch_load = b + sum(bits[:-1])
    anchor_share = F(1, branch_load) if x else F(0)
    terminal_share = F(1, branch_load) if terminal else F(0)
    query_share = F(query, b + x + sum(middle) + 1)
    kappa_share = F(x, b + r)
    quote_share = query * (F(x, b + r) + F(1 - x, b + 1))
    target = C * formal_u - (C - 1) * kappa_share - quote_share
    anchor_ic = alpha * (formal_u - anchor_share)
    intermediate_safety = sum((s * (formal_u - F(bit, b + r)) for bit in middle), F(0))
    terminal_safety = r * (formal_u - F(terminal, b + r))
    maximum_budgets = sum((a * F(x - bit, b + k + 1) for bit in middle), F(0))
    terminal_ic = terminal_share - query_share
    return target - anchor_ic - intermediate_safety - terminal_safety - maximum_budgets - terminal_ic


def from_displayed_formula(r, n, k, bits):
    alpha, s, a, C, old_C = PARAMETERS[r]
    x, terminal, query = bits[0], bits[-2], bits[-1]
    j = sum(bits[1:-2])
    D = n + r - 1
    return (alpha * F(x, n + j + terminal) + F(s * j + r * terminal, D)
            - (C - 1) * F(x, D) - query * (F(x, D) + F(1 - x, n))
            - a * F((r - 2) * x - j, n + k) - F(terminal - query, n + x + j))


all_records, summaries, checked_keys = [], [], set()
for r, (alpha, s, a, C, old_C) in PARAMETERS.items():
    assert min(alpha, s, a) >= 0 and C == alpha + (r - 2) * s + r
    assert alpha == 5 * (r - 1) and s / r + a / (r - 1) == F(1, 2)
    upper_n = 7 - r

    def G(n):
        return (n + r - 2) * (s + a * F(n + r - 1, n))

    endpoints = [G(1), G(upper_n)]
    assert max(endpoints) <= alpha - 1
    values = []
    for n, k in product(range(1, upper_n + 1), range(r - 1)):
        b, D, d = n - 1, n + r - 1, n + r - 2
        assert G(n) == (s + a) * n + s * (r - 2) + a * (2 * r - 3) + a * F((r - 2) * (r - 1), n)
        assert G(n) <= max(endpoints)
        assert s / D + a / d >= F(r - 1, 2 * d) >= F(1, n * (n + 1))
        assert F((r - 1) * (n - 1), n * D) == F(r, D) - F(1, n) >= 0
        for bits in product(range(2), repeat=r + 1):
            x, terminal, query = bits[0], bits[-2], bits[-1]
            j = sum(bits[1:-2])
            deficit = r - 2 - j
            E = from_shares(r, b, k, bits, F(0))
            assert E == from_shares(r, b, k, bits, F(1))
            assert E == from_displayed_formula(r, n, k, bits) >= 0
            worst_bits = list(bits)
            worst_bits[-1] = 1 - x
            worst_k = 0 if x else r - 2
            H = from_shares(r, b, worst_k, tuple(worst_bits), F(0))
            if x == 0:
                correction_k = a * j * (F(1, n + k) - F(1, n + r - 2))
                correction_q = (1 - query) * F(j, n * (n + j))
                if terminal == 0:
                    analytic_corner = j * (s / D + a / d - F(1, n * (n + j)))
                else:
                    analytic_corner = j * (s / D + a / d) + F(r, D) - F(1, n)
            else:
                correction_k = a * deficit * (F(1, n) - F(1, n + k))
                correction_q = query * F(deficit, (n + 1 + j) * D)
                if terminal == 1:
                    analytic_corner = deficit * (F(alpha - 1, (n + j + 1) * D) - s / D - a / n)
                else:
                    B = s + a * F(D, n)
                    analytic_corner = (F(alpha * (deficit + 1), d - deficit) - (r - 1) - deficit * B) / D
                    base_DH = alpha / d - (r - 1)
                    increment = deficit * (alpha * F(d + 1, d * (d - deficit)) - B)
                    assert analytic_corner * D == base_DH + increment
                    assert min(base_DH, increment) >= 0
                    assert alpha * F(d + 1, d * (d - deficit)) - B >= F(alpha + d, d * d) > 0
            assert H == analytic_corner >= 0
            assert min(correction_k, correction_q) >= 0 and E == H + correction_k + correction_q
            key = (r, b, k, bits)
            checked_keys.add(key)
            reference = main_atoms[key]
            assert E == F(reference["remainder"]) and H == F(reference["corner_remainder"])
            if r == 4:
                assert E == local_values[(n, k, *bits)]
            values.append(E)
            all_records.append({"r": r, "b": b, "n": n, "k": k, "bits": list(bits), "remainder": str(E),
                                "corner_remainder": str(H), "k_correction": str(correction_k), "q_correction": str(correction_q),
                                "from_shares_matches_displayed_formula": True, "payment_u_coefficient_exact": True})
    zero_count = sum(value == 0 for value in values)
    summary = {"r": r, "actual_player": 7 - r, "types": len(values), "C": str(C), "old_C": str(old_C),
               "improvement": str(old_C - C), "negative": sum(value < 0 for value in values),
               "zero": zero_count, "positive": len(values) - zero_count,
               "minimum_positive": str(min(value for value in values if value > 0)),
               "G_endpoints": list(map(str, endpoints)), "alpha_minus_one": str(alpha - 1)}
    main_summary = next(entry for entry in main_data["summaries"] if entry["r"] == r)
    for key in ("r", "actual_player", "types", "C", "old_C", "negative", "zero", "positive", "G_endpoints"):
        assert summary[key] == main_summary[key]
    assert summary["minimum_positive"] == main_summary["min_positive"]
    summaries.append(summary)
assert len(all_records) == 1440 and checked_keys == set(main_atoms)
assert source_hashes == {path.name: sha256(path.read_bytes()).hexdigest() for path in (SOURCE_MD, SOURCE_JSON)}
with (HERE / "audit_main_family_1440.csv").open("w", newline="") as stream:
    writer = csv.writer(stream)
    writer.writerow(["r", "b", "n", "k", "bits_x_middle_t_q", "E", "corner_E", "k_correction", "q_correction"])
    for record in all_records:
        writer.writerow([record["r"], record["b"], record["n"], record["k"], "".join(map(str, record["bits"])),
                         record["remainder"], record["corner_remainder"], record["k_correction"], record["q_correction"]])
result = {"status": "PASS_INDEPENDENT_MAIN_FAMILY_AUDIT", "source_sha256": source_hashes,
          "main_script_imported": False, "optimizer_calls": 0, "game_point_files_read_by_this_audit": 0,
          "raw_ordered_boolean_types": 1440, "actual_share_payment_checks": 2880,
          "displayed_residual_checks": 1440, "corner_plus_corrections_checks": 1440,
          "all_Main_atoms_compared": True, "r4_agrees_with_prior_frozen_288_table": True,
          "summaries": summaries, "claim": "All three constants are valid; no optimality claim for r5 or r6."}
(HERE / "audit_main_family.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
print(json.dumps(result, indent=2, ensure_ascii=False))
