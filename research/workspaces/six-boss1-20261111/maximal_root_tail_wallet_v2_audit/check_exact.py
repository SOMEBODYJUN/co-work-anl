#!/usr/bin/env python3
"""Independent root72 source/column audit. No builder/Main imports or solver.

The old 71 rows are regenerated from literal true shares and explicit mean
query lists. The added cut is reconstructed on all128 types from its already
proved nine-budget formula and the full [o/6,o] moment interval.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product, combinations_with_replacement
from pathlib import Path
import json
import sys
import re

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = WS.parents[2]
BUILDER = WS / "maximal_root_tail_wallet_v2"
OLD = WS / "maximal_root_tail_wallet"
REQUERY = WS / "maximal_root_opt_requery"
ATOMS = list(product((0, 1), repeat=7))
TAILS = list(product((0, 1), repeat=3))
ROLES = ("C", "B2", "B3", "B4", "B5", "B6", "Omean")
ZERO = F(0)
KNEW = F(1125421575458286230366665, 6570307807568935468436467)


def share(bit, load):
    return F(bit, load) if bit else ZERO


def queries(role, h):
    return [h[-1], 0, 0, 0, 0, 0] if role == "Omean" else [h[ROLES.index(role)]]


def pair_cost(prefix, qs, rs):
    return sum((share(q, prefix + 1 + r) + share(r, prefix + 1)
                for q in qs for r in rs), ZERO) / (len(qs) * len(rs))


def phi(h, q, tail):
    p, y2, y3, y4, y5, z, o = h
    r, y, t = tail
    b = p + y2
    D4, D6, D = b + y3 + 3, b + y3 + y4 + y5 + 1, b + q + r + 1
    return (F(126000 * q, b + 1 + r + y + t)
            + F(43 * r + 31218 * y + 34458 * t, D4)
            + F(1654 * (r + y + t), D6)
            + 5400 * (F(o, 6) - t) / (D + y)
            + 7740 * (F(o, 3 * D) - F(o, 36 * D * (D + 1))
                      - F(y, D + t) - F(t, D + y) - F(y, D * (D + 1))))


def requery_cut():
    cut, minima = [], []
    for h in ATOMS:
        a0, a1 = [min(phi(h, q, tail) for tail in TAILS) for q in (0, 1)]
        m = a0 if h[-1] == 0 else min((5 * a0 + a1) / 6, a1)
        old_wallet = 126000 * share(h[2], sum(h[:6])) + 65719 * share(h[3], sum(h[:6])) + 4962 * share(h[5], sum(h[:6]))
        cut.append(old_wallet - m)
        minima.append(m)
    return cut, minima


def source_rows():
    rows = {}

    def add(name, family, a, bK=ZERO, bO=ZERO, u=ZERO):
        rows[name] = {"family": family, "a": list(a) + [F(u)], "bK": F(bK), "bO": F(bO)}

    add("ROOT_IC", "ROOT_IC", [-share(h[0], sum(h[:6])) for h in ATOMS], u=1)
    for j in range(2, 7):
        add(f"CAP_B{j}", "CAP", [-F(h[j - 1]) for h in ATOMS], bK=-1)
    add("BRANCH_UNION_OPT", "UNION", [-F(int(any(h[:6]))) for h in ATOMS], bO=-1)
    add("ROOT_K_FLOOR", "FLOOR", [ZERO] * 128, bK=F(1, 6), u=1)
    for j in range(2, 7):
        for role in ROLES:
            values = []
            for h in ATOMS:
                qs = queries(role, h)
                query = sum((share(q, sum(h[:j - 1]) + 7 - j) for q in qs), ZERO) / len(qs)
                values.append(share(h[j - 1], sum(h[:6])) - query)
            add(f"SAFE_j{j}|{role}", "SAFE", values)
    for left, right in combinations_with_replacement(ROLES, 2):
        values = []
        for h in ATOMS:
            prefix, y, z = sum(h[:4]), h[4], h[5]
            wallet = share(y, sum(h[:6])) + share(z, sum(h[:6])) + share(y, prefix + 1) - share(y, prefix + 1 + y)
            values.append(wallet - pair_cost(prefix, queries(left, h), queries(right, h)))
        add(f"PAIR|{left}|{right}", "PAIR", values)
    assert len(rows) == 71
    cut, _ = requery_cut()
    add("OPT_SOURCE3_REQUERY_CUT", "REQUERY_CUT", cut)
    assert len(rows) == 72
    return rows


def vector(sparse, n=129):
    out = [ZERO] * n
    for k, v in sparse.items():
        assert str(int(k)) == k and 0 <= int(k) < n
        out[int(k)] = F(v)
    return out


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), ZERO)


def source_pins(data):
    assert data["old_input_sha256"] == sha256((OLD / "exact_input.json").read_bytes()).hexdigest() == "3c1a824ed0a17562da812db1d0bb12485f0b1c7f743577af7bc2ecf316d3ab65"
    assert data["cut_certificate_sha256"] == sha256((REQUERY / "exact_certificate.json").read_bytes()).hexdigest() == "209959db4dfce6ba4fe796eeb168b8ab71f186f795e0599f9148d08ceaa8b13e"
    assert data["source_review_sha256"] == sha256((BUILDER / "source_review.md").read_bytes()).hexdigest()
    preflight = json.loads((HERE / "source_preflight.json").read_text())
    assert preflight["source_review_sha256"] == data["source_review_sha256"]


def check_input():
    path = BUILDER / "exact_input.json"
    data = json.loads(path.read_text())
    source_pins(data)
    assert data["bit_order"] == ["p", "y2", "y3", "y4", "y5", "z", "o"]
    assert data["atoms"] == [{"index": i, "bits": list(h)} for i, h in enumerate(ATOMS)]
    assert data["root_u_column"] == 128 and data["nonnegative_columns"] == list(range(129))
    assert data["convention"] == "A*x >= bK*K+bO*O"
    assert F(data["fixed_K"]) == KNEW and F(data["fixed_O"]) == 1
    assert vector(data["objective"]) == [ZERO] * 128 + [F(1)]
    rows = source_rows()
    assert [r["name"] for r in data["raw_rows"]] == list(rows)
    old = json.loads((OLD / "exact_input.json").read_text())
    for old_row, new_row in zip(old["raw_rows"], data["raw_rows"][:71]):
        for key in ("name", "family", "a", "bK", "bO"):
            assert new_row[key] == old_row[key], (old_row["name"], key)
    checks = 0
    divisors = {}
    for stored in data["raw_rows"]:
        row = rows[stored["name"]]
        assert stored["family"] == row["family"]
        for a, b in zip(vector(stored["a"]), row["a"]):
            assert a == b, stored["name"]
            checks += 1
        assert F(stored["bK"]) == row["bK"] and F(stored["bO"]) == row["bO"]
        assert F(stored["rhs"]) == row["bK"] * KNEW + row["bO"]
        divisor = F(stored["numerical_divisor"])
        assert divisor == (126000 if row["family"] == "REQUERY_CUT" else 1)
        divisors[stored["name"]] = divisor
    new = data["raw_rows"][-1]
    assert F(new["source_cut_u"]) == F(new["source_cut_K"]) == 0
    assert new["source_certificate_sha256"] == data["cut_certificate_sha256"]
    cut_cert = json.loads((REQUERY / "exact_certificate.json").read_text())
    assert rows["OPT_SOURCE3_REQUERY_CUT"]["a"][:128] == vector(cut_cert["universal_cut"]["cut_z"], 128)
    assert len(data["equalities"]) == 2
    Ep, Eo = [F(h[0]) for h in ATOMS] + [ZERO], [F(h[-1]) for h in ATOMS] + [ZERO]
    for saved, expected, par, rhs in zip(data["equalities"], [Ep, Eo], ["K", "O"], [KNEW, F(1)]):
        assert vector(saved["a"]) == expected and saved["parameter"] == par
        assert F(saved["rhs"]) == rhs
    result = {
        "status": "PASS_ROOT72_SOURCE_COMPOSITION_LITERAL_INPUT_AND_POSITIVE_SCALING",
        "input_sha256": sha256(path.read_bytes()).hexdigest(),
        "source_review_sha256": data["source_review_sha256"],
        "old_input_sha256": data["old_input_sha256"],
        "cut_certificate_sha256": data["cut_certificate_sha256"],
        "fixed_K": str(KNEW), "fixed_O": "1",
        "all_128_atoms_including_o0_and_allzero": True,
        "old_71_symbolic_rows_unchanged": True,
        "raw_rows": 72, "nonnegative_columns": 129,
        "unscaled_matrix_coefficients_rebuilt": checks,
        "requery_cut_source_states_rebuilt": 2048,
        "full_requery_cut_coefficients_rebuilt": 128,
        "independent_K_O_row_parameters_checked": 144,
        "normalization_coefficients_checked": 258,
        "numerical_divisors": {name: str(v) for name, v in divisors.items()},
        "correct_unscaled_cut_dual_rule": "lambda_original=lambda_scaled/126000",
        "arbitrary_history_cut_applies_to_root_C_branch": True,
        "whole_72_row_system_requires_O_is_OPT6": True,
        "optimizer_called": False, "builder_or_Main_code_executed": False,
        "outstanding_errors": [],
    }
    output = HERE / "input_audit.json"
    assert not output.exists(), "refuse overwrite"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("status", "input_sha256", "fixed_K",
          "unscaled_matrix_coefficients_rebuilt", "requery_cut_source_states_rebuilt",
          "old_71_symbolic_rows_unchanged")}, ensure_ascii=False, indent=2))


def check_certificate():
    data_path = BUILDER / "exact_input.json"
    cert_path = BUILDER / "exact_certificate.json"
    data, cert = json.loads(data_path.read_text()), json.loads(cert_path.read_text())
    input_audit = json.loads((HERE / "input_audit.json").read_text())
    assert sha256(data_path.read_bytes()).hexdigest() == input_audit["input_sha256"] == cert["input_sha256"]
    source_pins(data)
    assert cert["status"] == "EXACT_PRIMAL_UNSCALED_DUAL_MATCH"
    rows = source_rows()
    Ep, Eo = [F(h[0]) for h in ATOMS] + [ZERO], [F(h[-1]) for h in ATOMS] + [ZERO]
    x = vector(cert["primal"])
    assert all(v >= 0 for v in x)
    assert dot(Ep, x) == KNEW and dot(Eo, x) == 1
    assert set(cert["raw_unscaled_row_slacks"]) == set(rows)
    slacks = {}
    for name, row in rows.items():
        slack = dot(row["a"], x) - row["bK"] * KNEW - row["bO"]
        assert slack >= 0, name
        assert slack == F(cert["raw_unscaled_row_slacks"][name]), name
        slacks[name] = slack
    dual = cert["dual"]
    original = dual["original_unscaled_row_weights"]
    scaled = dual["scaled_solver_form_weights"]
    assert set(original) == set(scaled) <= set(rows)
    weights = {name: F(original.get(name, 0)) for name in rows}
    assert all(v >= 0 for v in weights.values())
    divisors = {r["name"]: F(r["numerical_divisor"]) for r in data["raw_rows"]}
    for name in rows:
        assert F(scaled.get(name, 0)) == weights[name] * divisors[name]
    pi_p, pi_o = F(dual["equality_C_size"]), F(dual["equality_OPT_union"])
    a = pi_p + sum((weights[name] * row["bK"] for name, row in rows.items()), ZERO)
    b = pi_o + sum((weights[name] * row["bO"] for name, row in rows.items()), ZERO)
    objective = [ZERO] * 128 + [F(1)]
    residues = []
    for j in range(129):
        residue = objective[j] - sum((weights[name] * row["a"][j] for name, row in rows.items()), ZERO) - pi_p * Ep[j] - pi_o * Eo[j]
        assert residue >= 0, j
        residues.append(residue)
    assert vector(dual["column_residuals"]) == residues
    assert all(weights[name] * slack == 0 for name, slack in slacks.items())
    assert all(v * r == 0 for v, r in zip(x, residues))
    assert x[128] == F(cert["objective"]) == a * KNEW + b
    line = cert["universal_root_line"]
    assert F(line["a"]) == a and F(line["b"]) == b
    assert F(line["root_u_residual"]) == residues[128] == 0
    N, AK, BO = [int(line["integer_line"][key]) for key in ("u", "K", "O")]
    assert N == 229185173551068 and AK == 23463022015563 and BO == 4570807634338
    assert a * N == AK and b * N == BO
    D = int(dual["common_budget_denominator"])
    assert D == 458370347102136 == 2 * N
    assert set(dual["integer_original_row_weights"]) == {name for name, v in weights.items() if v > 0}
    for name, integer in dual["integer_original_row_weights"].items():
        assert weights[name] * D == int(integer)
    assert [pi_p * D, pi_o * D] == [F(v) for v in dual["integer_equality_multipliers"]]
    # Verify the full identity before substituting either mass equation.
    rhs = [ZERO] * 131
    for name, row in rows.items():
        for j, coeff in enumerate(row["a"] + [-row["bK"], -row["bO"]]):
            rhs[j] += weights[name] * coeff
    for j, residue in enumerate(residues):
        rhs[j] += residue
    for pi, equation in [(pi_p, Ep + [-F(1), ZERO]), (pi_o, Eo + [ZERO, -F(1)])]:
        for j, coeff in enumerate(equation):
            rhs[j] += pi * coeff
    assert rhs == objective + [-a, -b]
    assert [D * t for t in rhs] == [D * t for t in objective] + [-F(2 * AK), -F(2 * BO)]
    assert weights["OPT_SOURCE3_REQUERY_CUT"] == F(2312374, 6366254820863) > 0
    assert weights["BRANCH_UNION_OPT"] == weights["ROOT_K_FLOOR"] == 0
    # Therefore this supporting line does not require the sole OPT-only row.

    previous = json.loads((OLD / "exact_certificate.json").read_text())["universal_root_line"]
    old_a, old_b = F(previous["a"]), F(previous["b"])
    comparison = cert["comparison_previous_root_line"]
    old_value = old_a * KNEW + old_b
    improvement = x[128] - old_value
    slope, intercept = a - old_a, b - old_b
    crossing = -intercept / slope
    diff_equal_KO = slope + intercept
    assert F(comparison["previous_value_at_same_K"]) == old_value
    assert F(comparison["improvement_at_same_K"]) == improvement > 0
    assert F(comparison["difference_slope"]) == slope < 0
    assert F(comparison["difference_intercept"]) == intercept > 0
    assert F(comparison["crossing_K_over_O"]) == crossing > 1
    assert F(comparison["difference_at_K_equals_O"]) == diff_equal_KO > 0
    # For OPT6, repeat C in all six slots to obtain K<=O; hence this proves
    # strict pointwise dominance over the previous line for every O>0.

    source_paths = [BUILDER / "source_review.md", data_path, cert_path,
                    OLD / "exact_input.json", OLD / "exact_certificate.json",
                    REQUERY / "exact_certificate.json"]
    result = {
        "status": "PASS_ALL72_PRIMAL_UNSCALED_DUAL_AND_UNIVERSAL_ROOT_LINE",
        "source_sha256": {str(p.relative_to(REPO)): sha256(p.read_bytes()).hexdigest() for p in source_paths},
        "fixed_K": str(KNEW), "fixed_O": "1",
        "raw_unscaled_primal_rows_checked": 72,
        "mass_equations_checked": 2,
        "nonnegative_primal_variables_checked": 129,
        "positive_primal_atoms": [i for i, v in enumerate(x[:128]) if v > 0],
        "primal_all_unscaled_row_slacks": {name: str(v) for name, v in slacks.items()},
        "exact_finite_cone_optimum": str(x[128]),
        "positive_original_unscaled_dual_weights": {name: str(v) for name, v in weights.items() if v > 0},
        "free_equality_multipliers": {"pi_p": str(pi_p), "pi_o": str(pi_o)},
        "all_129_unscaled_column_residuals": [str(v) for v in residues],
        "positive_atom_residual_count": sum(v > 0 for v in residues[:128]),
        "zero_atom_residuals": [i for i, v in enumerate(residues[:128]) if v == 0],
        "u_column_residual": str(residues[128]),
        "homogeneous_identity_columns": 131,
        "universal_root_line": {"a": str(a), "b": str(b), "integer_u": N, "integer_K": AK, "integer_O": BO},
        "integer_budget_denominator": D,
        "integer_budget_identity_is_primitive_line_times": 2,
        "integer_original_budget_weights": dual["integer_original_row_weights"],
        "integer_equality_multipliers": dual["integer_equality_multipliers"],
        "scaled_to_original_cut_weight": {"divisor": "126000", "original_weight": str(weights["OPT_SOURCE3_REQUERY_CUT"]), "scaled_weight": str(F(scaled["OPT_SOURCE3_REQUERY_CUT"]))},
        "branch_union_cap_weight": str(weights["BRANCH_UNION_OPT"]),
        "root_K_floor_weight": str(weights["ROOT_K_FLOOR"]),
        "certified_line_valid_for_arbitrary_six_legal_query_union": True,
        "whole72_cone_scope_still_requires_O_equals_OPT6": True,
        "comparison_previous_line": {"old_value_at_same_K": str(old_value), "improvement_at_same_K": str(improvement),
                                    "difference_slope": str(slope), "difference_intercept": str(intercept),
                                    "crossing_K_over_O": str(crossing), "difference_at_K_equals_O": str(diff_equal_KO),
                                    "strictly_stronger_for_all_0_le_K_le_OPT6_when_OPT6_positive": True},
        "optimizer_called": False, "builder_or_Main_code_executed": False,
        "recovery_rank_independently_claimed": False,
        "full_SPE_realizability_or_global_sharpness_claimed": False,
        "best_known_bound_claimed": False,
        "prior_frozen_audits_modified": False,
        "outstanding_errors": [],
    }
    output = HERE / "audit_result.json"
    assert not output.exists(), "refuse overwrite"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in ("status", "exact_finite_cone_optimum", "universal_root_line",
          "positive_atom_residual_count", "zero_atom_residuals", "homogeneous_identity_columns",
          "scaled_to_original_cut_weight", "branch_union_cap_weight", "integer_budget_identity_is_primitive_line_times")}, ensure_ascii=False, indent=2))


def check_final_proof():
    audited = json.loads((HERE / "audit_result.json").read_text())
    for rel, h in audited["source_sha256"].items():
        assert sha256((REPO / rel).read_bytes()).hexdigest() == h
    cert = json.loads((BUILDER / "exact_certificate.json").read_text())
    proof = (BUILDER / "proof.md").read_text()
    E = int(re.findall(r'E=([0-9]+)', proof)[0])
    masses = re.findall(r'^\| ([01]{7}) \| ([0-9]+) \|$', proof, re.M)
    parsed = {str(int(bits, 2)): F(int(value), E) for bits, value in masses}
    expected = {col: F(value) for col, value in cert["primal"].items() if int(col) < 128 and F(value) > 0}
    assert len(parsed) == 10 and parsed == expected
    u_numerator = int(re.findall(r'u=([0-9]+)/E', proof)[0])
    assert F(u_numerator, E) == F(cert["objective"])
    numeric_tables = re.findall(r'^\| ([^|]+) \| ([0-9]+) \|$', proof, re.M)
    budget_weights = [int(value) for label, value in numeric_tables if not re.fullmatch('[01]{7}', label.strip())]
    assert budget_weights == [int(value) for value in cert["dual"]["integer_original_row_weights"].values()]
    assert sum(budget_weights[1:6]) == 104792583342110
    assert audited["integer_budget_denominator"] == 2 * audited["universal_root_line"]["integer_u"]
    result = {
        "status": "PASS_FINAL_PROOF_POINT_TABLE_AND_TWO_INTEGER_SCALES",
        "source_sha256": {str(p.relative_to(REPO)): sha256(p.read_bytes()).hexdigest()
                          for p in [BUILDER / "proof.md", WS / "maximal_root_tail_wallet_v2.md"]},
        "point_table_rows_matched": len(parsed),
        "point_table_denominator": str(E),
        "root_u_transcription_matched": True,
        "integer_budget_table_weights_matched": len(budget_weights),
        "five_integer_CAP_weights_sum": "104792583342110",
        "budget_integer_identity_is_primitive_line_times": 2,
        "proof_and_summary_scope_reviewed": True,
        "union_cap_zero_weight_allows_any_six_legal_query_union": True,
        "dominance_over_previous_line_uses_K_le_OPT6": True,
        "new_30_distinct_index_pair_budget_included": False,
        "outstanding_errors": [],
    }
    output = HERE / "proof_audit.json"
    assert not output.exists(), "refuse overwrite"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("status", "point_table_rows_matched", "integer_budget_table_weights_matched",
          "budget_integer_identity_is_primitive_line_times")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if sys.argv[1:] == ["--input"]:
        check_input()
    elif sys.argv[1:] == ["--certificate"]:
        check_certificate()
    elif sys.argv[1:] == ["--proof"]:
        check_final_proof()
    else:
        raise SystemExit("usage: check_exact.py --input | --certificate | --proof")
