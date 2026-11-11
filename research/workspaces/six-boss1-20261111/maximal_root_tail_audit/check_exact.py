#!/usr/bin/env python3
"""Independent source-to-column audit. Standard library only; never runs a solver.

Pure final-pair query costs are reconstructed as U(Q,R)+f(R), using literal
shares. Mean descriptors are explicit six-index lists; mean/mean loops over
all 36 ordered index pairs. No builder/checker is imported or executed.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product, combinations_with_replacement
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = WS.parents[2]
BUILDER = WS / "maximal_root_tail_wallet"
ZERO = F(0)
ATOMS = list(product((0, 1), repeat=7))
COLS = 129
ROLES = ("C", "B2", "B3", "B4", "B5", "B6", "Omean")


def frac_share(bit, load):
    """Zero membership contributes zero even when the total load is zero."""
    return F(bit, load) if bit else ZERO


def query_bits(role, atom):
    # This is the d=o weak query-cost endpoint, not a synthetic legal label.
    if role == "Omean":
        return [atom[-1], 0, 0, 0, 0, 0]
    return [atom[ROLES.index(role)]]


def pure_pair_cost(prefix, q, r):
    # Literal U(Q,R)+f(R) = f(Q)+f(R)-g(Q,R).
    return frac_share(q, prefix + 1 + r) + frac_share(r, prefix + 1)


def mean_pair_cost(prefix, qs, rs):
    return sum((pure_pair_cost(prefix, q, r) for q in qs for r in rs), ZERO) / (len(qs) * len(rs))


def source_identities():
    """Audit the payment algebra and index-mean weakening independently."""
    pair_checks = 0
    for prefix in range(5):
        for y, z, q, r, reply in product((0, 1), repeat=5):
            U = lambda a, b: frac_share(a, prefix + 1 + b)
            fY = frac_share(y, prefix + 1)
            diag = fY - U(y, y)
            vY, vZ = U(y, z), U(z, y)
            lhs = vY + vZ + diag - pure_pair_cost(prefix, q, r)
            last_remainder = U(y, reply) - U(y, y)
            rhs = (vY - U(q, reply)) + (U(reply, q) - U(r, q)) + (vZ - U(reply, y)) + last_remainder
            assert lhs == rhs
            assert last_remainder >= 0
            pair_checks += 1
    safe_load_checks = 0
    for j in range(2, 7):
        for prefix in range(j):
            for q in (0, 1):
                for future_load in range(7 - j):
                    assert frac_share(q, prefix + 1 + future_load) >= frac_share(q, prefix + 7 - j)
                    safe_load_checks += 1
    mixed_checks = full36_checks = safe_mean_checks = 0
    for menu_bits in product((0, 1), repeat=6):
        d = sum(menu_bits)
        o = int(d > 0)
        reduced_bits = [o, 0, 0, 0, 0, 0]
        for prefix in range(5):
            D = prefix + 1
            exact = mean_pair_cost(prefix, menu_bits, menu_bits)
            weak = mean_pair_cost(prefix, reduced_bits, reduced_bits)
            assert exact == F(d, 3 * D) - F(d * d, 36 * D * (D + 1))
            assert weak == F(o, 3 * D) - F(o, 36 * D * (D + 1))
            assert exact >= weak
            if d:
                assert exact - weak == F((d - 1) * (12 * (D + 1) - (d + 1)), 36 * D * (D + 1))
            full36_checks += 1
            for q in (0, 1):
                exact_mixed = mean_pair_cost(prefix, [q], menu_bits)
                weak_mixed = mean_pair_cost(prefix, [q], reduced_bits)
                assert exact_mixed >= weak_mixed
                assert exact_mixed - weak_mixed == F((d - o) * (D + 1 - q), 6 * D * (D + 1))
                mixed_checks += 1
        for j in range(2, 7):
            for prefix in range(j):
                den = prefix + 7 - j
                exact = sum((frac_share(q, den) for q in menu_bits), ZERO) / 6
                assert exact >= F(o, 6 * den)
                safe_mean_checks += 1
    return {
        "literal_four_term_PAIR_payment_cases": pair_checks,
        "SAFE_future_load_cases": safe_load_checks,
        "full_36_index_pair_mean_cases": full36_checks,
        "pure_mean_index_cases": mixed_checks,
        "SAFE_six_query_mean_cases": safe_mean_checks,
    }


def source_rows():
    rows = {}

    def add(name, family, values, bK=ZERO, bO=ZERO, u=ZERO):
        assert name not in rows
        rows[name] = {"family": family, "a": list(values) + [F(u)], "bK": F(bK), "bO": F(bO)}

    add("ROOT_IC", "ROOT_IC", [-frac_share(h[0], sum(h[:6])) for h in ATOMS], u=1)
    for j in range(2, 7):
        add(f"CAP_B{j}", "CAP", [-F(h[j - 1]) for h in ATOMS], bK=-1)
    add("BRANCH_UNION_OPT", "UNION", [-F(int(any(h[:6]))) for h in ATOMS], bO=-1)
    add("ROOT_K_FLOOR", "FLOOR", [ZERO for _ in ATOMS], bK=F(1, 6), u=1)
    for j in range(2, 7):
        for role in ROLES:
            values = []
            for h in ATOMS:
                branch_payoff = frac_share(h[j - 1], sum(h[:6]))
                prefix = sum(h[:j - 1])
                qbits = query_bits(role, h)
                guaranteed_deviation = sum((frac_share(q, prefix + 7 - j) for q in qbits), ZERO) / len(qbits)
                values.append(branch_payoff - guaranteed_deviation)
            add(f"SAFE_j{j}|{role}", "SAFE", values)
    for left, right in combinations_with_replacement(ROLES, 2):
        values = []
        for h in ATOMS:
            prefix, y, z = sum(h[:4]), h[4], h[5]
            load = prefix + y + z
            payoff_y = frac_share(y, load)
            payoff_z = frac_share(z, load)
            diag_y = frac_share(y, prefix + 1) - frac_share(y, prefix + 1 + y)
            query_cost = mean_pair_cost(prefix, query_bits(left, h), query_bits(right, h))
            values.append(payoff_y + payoff_z + diag_y - query_cost)
        add(f"PAIR|{left}|{right}", "PAIR", values)
    assert len(rows) == 71
    return rows


def vector(sparse):
    result = [ZERO] * COLS
    for k, value in sparse.items():
        assert str(int(k)) == k and 0 <= int(k) < COLS
        result[int(k)] = F(value)
    return result


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), ZERO)


def main():
    algebra = source_identities()
    rebuilt = source_rows()
    input_path = BUILDER / "exact_input.json"
    cert_path = BUILDER / "exact_certificate.json"
    data = json.loads(input_path.read_text())
    cert = json.loads(cert_path.read_text())
    assert cert["input_sha256"] == sha256(input_path.read_bytes()).hexdigest()
    assert data["bit_order"] == ["p", "y2", "y3", "y4", "y5", "z", "o"]
    assert data["atoms"] == [{"index": i, "bits": list(h)} for i, h in enumerate(ATOMS)]
    assert data["root_u_column"] == 128
    assert data["nonnegative_columns"] == list(range(COLS))
    assert data["convention"] == "A*x >= bK*K+bO*O"
    assert vector(data["objective"]) == [ZERO] * 128 + [F(1)]
    K0, O0 = F(data["fixed_K"]), F(data["fixed_O"])
    assert K0 == F(24376964954228547006, 142891298915142483961)
    assert O0 == 1
    assert [r["name"] for r in data["raw_rows"]] == list(rebuilt)
    coefficient_checks = 0
    for stored in data["raw_rows"]:
        row = rebuilt[stored["name"]]
        assert stored["family"] == row["family"]
        for x, y in zip(vector(stored["a"]), row["a"]):
            assert x == y, stored["name"]
            coefficient_checks += 1
        assert F(stored["bK"]) == row["bK"]
        assert F(stored["bO"]) == row["bO"]
        assert F(stored["rhs"]) == row["bK"] * K0 + row["bO"] * O0
    E_p = [F(h[0]) for h in ATOMS] + [ZERO]
    E_o = [F(h[-1]) for h in ATOMS] + [ZERO]
    assert len(data["equalities"]) == 2
    for saved, expected, par, value in zip(data["equalities"], [E_p, E_o], ["K", "O"], [K0, O0]):
        assert vector(saved["a"]) == expected
        assert saved["parameter"] == par
        assert F(saved["rhs"]) == value

    x = vector(cert["primal"])
    assert all(t >= 0 for t in x)
    assert dot(E_p, x) == K0 and dot(E_o, x) == O0
    slacks = {}
    assert set(cert["raw_row_slacks"]) == set(rebuilt)
    for name, row in rebuilt.items():
        slack = dot(row["a"], x) - row["bK"] * K0 - row["bO"] * O0
        assert slack >= 0, name
        assert slack == F(cert["raw_row_slacks"][name])
        slacks[name] = slack
    dual = cert["dual"]
    assert set(dual["row_weights"]) <= set(rebuilt)
    weights = {name: F(dual["row_weights"].get(name, "0")) for name in rebuilt}
    assert all(weight >= 0 for weight in weights.values())
    pi_p, pi_o = F(dual["equality_C_size"]), F(dual["equality_OPT_union"])
    a = pi_p + sum((weights[name] * row["bK"] for name, row in rebuilt.items()), ZERO)
    b = pi_o + sum((weights[name] * row["bO"] for name, row in rebuilt.items()), ZERO)
    c = [ZERO] * 128 + [F(1)]
    residues = []
    for j in range(COLS):
        residue = c[j] - sum((weights[name] * row["a"][j] for name, row in rebuilt.items()), ZERO) - pi_p * E_p[j] - pi_o * E_o[j]
        assert residue >= 0, j
        residues.append(residue)
    assert residues == vector(dual["column_residuals"])
    assert x[128] == F(cert["objective"]) == a * K0 + b * O0
    assert all(weights[name] * slack == 0 for name, slack in slacks.items())
    assert all(v * r == 0 for v, r in zip(x, residues))
    line = cert["universal_root_line"]
    assert a == F(line["a"]) and b == F(line["b"])
    L = int(dual["common_budget_denominator"])
    assert L == 112944305160
    assert a * L == int(line["integer_line"]["K"]) == 11595684007
    assert b * L == int(line["integer_line"]["O"]) == 2178783435
    assert int(line["integer_line"]["u"]) == L
    assert set(dual["integer_row_weights"]) == {name for name, weight in weights.items() if weight > 0}
    for name, integer in dual["integer_row_weights"].items():
        assert weights[name] * L == int(integer)
    assert [pi_p * L, pi_o * L] == [F(t) for t in dual["integer_equality_multipliers"]]
    # Universal identity: check x[0..128], the independent K column, and O column.
    rhs = [ZERO] * 131
    for name, row in rebuilt.items():
        extended = row["a"] + [-row["bK"], -row["bO"]]
        for j, value in enumerate(extended):
            rhs[j] += weights[name] * value
    for j, value in enumerate(residues):
        rhs[j] += value
    for pi, norm in [(pi_p, E_p + [-F(1), ZERO]), (pi_o, E_o + [ZERO, -F(1)])]:
        for j, value in enumerate(norm):
            rhs[j] += pi * value
    assert rhs == c + [-a, -b]
    assert weights["BRANCH_UNION_OPT"] == 0
    assert weights["ROOT_K_FLOOR"] == 0
    # The certified line therefore does not use the sole OPT-only row.

    main_slope, main_intercept = F(1658, 10980), F(87, 10980)
    main_value = main_slope * K0 + main_intercept
    improvement = x[128] - main_value
    compare = cert["comparison_Main_NEW"]
    assert main_value == F(compare["value_at_K0"])
    assert improvement == F(compare["improvement_at_K0"]) > 0
    assert a - main_slope == F(compare["new_minus_Main_slope"])
    assert b - main_intercept == F(compare["new_minus_Main_intercept"])
    crossing = (b - main_intercept) / (main_slope - a)
    assert crossing == F(compare["crossing_K_over_O"])
    duplicates = {}
    for name, row in rebuilt.items():
        signature = tuple(row["a"] + [row["bK"], row["bO"]])
        duplicates.setdefault(signature, []).append(name)

    source_files = [
        REPO / "archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md",
        REPO / "archives/customer-attraction/state/引理/固定背景两人税界--引理.md",
        BUILDER / "derivation.md", input_path, cert_path,
    ]
    result = {
        "status": "PASS_ALL_SOURCE_ROWS_PRIMAL_DUAL_AND_UNIVERSAL_HOMOGENEOUS_IDENTITY",
        "source_sha256": {str(p.relative_to(REPO)): sha256(p.read_bytes()).hexdigest() for p in source_files},
        "source_identity_checks": algebra,
        "raw_rows": len(rebuilt),
        "all_columns": COLS,
        "all_128_atoms_including_o0_and_allzero": True,
        "row_coefficients_independently_rebuilt": coefficient_checks,
        "independent_parameter_coefficients_checked": 142,
        "normalization_coefficients_checked": 258,
        "global_homogeneous_identity_columns": 131,
        "row_families": {family: sum(r["family"] == family for r in rebuilt.values()) for family in ("ROOT_IC", "CAP", "UNION", "FLOOR", "SAFE", "PAIR")},
        "zero_affine_rows": [name for name, row in rebuilt.items() if all(v == 0 for v in row["a"] + [row["bK"], row["bO"]])],
        "duplicate_affine_rows_retained": [names for names in duplicates.values() if len(names) > 1],
        "primal_positive_columns": [i for i, v in enumerate(x) if v > 0],
        "primal_positive_atom_count": sum(v > 0 for v in x[:128]),
        "exact_cone_optimum_at_fixed_K0": str(x[128]),
        "primal_all_71_row_slacks": {name: str(v) for name, v in slacks.items()},
        "primal_norms": {"K": str(K0), "O": str(O0)},
        "positive_dual_budget_weights": {name: str(v) for name, v in weights.items() if v > 0},
        "free_equality_multipliers": {"pi_p": str(pi_p), "pi_o": str(pi_o)},
        "a_equals_pi_p_plus_sum_lambda_bK": str(a),
        "b_equals_pi_o_plus_sum_lambda_bO": str(b),
        "integer_root_line": {"u": L, "K": 11595684007, "O": 2178783435},
        "all_129_column_residuals": [str(v) for v in residues],
        "positive_column_residual_count": sum(v > 0 for v in residues),
        "zero_column_residuals": [i for i, v in enumerate(residues) if v == 0],
        "all_zero_atom_residual": str(residues[0]),
        "root_u_residual": str(residues[128]),
        "branch_union_cap_weight": str(weights["BRANCH_UNION_OPT"]),
        "root_K_floor_weight": str(weights["ROOT_K_FLOOR"]),
        "line_valid_for_arbitrary_six_legal_query_union": True,
        "full_71_row_cone_requires_O_is_OPT6": True,
        "comparison_main_root_line_at_K0": {"old_value": str(main_value), "improvement": str(improvement), "crossing_K_over_O": str(crossing)},
        "optimizer_called": False,
        "builder_or_Main_code_executed": False,
        "full_SPE_realizability_of_fractional_primal_claimed": False,
        "globally_optimal_root_bound_claimed": False,
        "best_known_bound_claimed": False,
        "prior_frozen_audits_modified": False,
        "outstanding_errors": [],
    }
    out = HERE / "audit_result.json"
    assert not out.exists(), "refuse overwrite"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in (
        "status", "row_coefficients_independently_rebuilt", "source_identity_checks",
        "global_homogeneous_identity_columns", "primal_positive_atom_count",
        "exact_cone_optimum_at_fixed_K0", "integer_root_line", "positive_column_residual_count",
        "zero_column_residuals", "line_valid_for_arbitrary_six_legal_query_union",
    )}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
