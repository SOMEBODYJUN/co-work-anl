#!/usr/bin/env python3
"""Exact root-C equality and fifth-source audit. No optimizer or old LP replay.

The existing certificate is read only to extract its already certified u1,K,O.
Every output stays in this new audit directory; prior frozen audits are untouched.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = WORK.parents[2]


def share(bit, total):
    return F(1, total) if bit else F(0)


def transfer(p, n, z, theta):
    total = p + n + z
    v, w = share(p, total), share(z, total)
    left = theta / (1 + 5 * p) - theta / (1 + p + n) + w - v
    right = F(n - 4 * p, 2) + z - p + 24 * (v - F(p, 6))
    return right - left


def closed_transfer(p, n, z, theta):
    if p == 0 and z == 0:
        return F(n, 2) - theta * F(n, n + 1)
    if p == 0 and z == 1:
        return F(n, 2) + (1 - theta) * F(n, n + 1)
    base = F((4 - n) * (9 - n), 2 * (n + 1)) if z == 0 else F((4 - n) * (6 - n), 2 * (n + 2))
    return base + theta * F(4 - n, 6 * (n + 2))


def main():
    entries = []
    equality_zero_states = []
    ratio = F(0)
    ratio_states = []
    identities = 0
    for bits in product((0, 1), repeat=7):
        p, y2, y3, y4, y5, z, o = bits
        ys = (y2, y3, y4, y5)
        n, theta = sum(ys), F(o, 6)
        total = p + n + z
        v, s, w = share(p, total), share(y5, total), share(z, total)
        tau = transfer(p, n, z, theta)
        assert tau == closed_transfer(p, n, z, theta) >= 0
        if not tau:
            assert all(y == p for y in ys)
            equality_zero_states.append(list(bits))
        else:
            assert any(y != p for y in ys)
        delta = v - s + theta / (p + n - y5 + 2) - F(o, 12) + F(p, 18)
        rho = delta + F(12, 5) * tau
        assert rho >= 0, (bits, tau, delta, rho)
        if p:
            assert delta >= 0
        if not p and n:
            assert tau >= F(5 * n, 12)
        if not p and not y5:
            assert delta == -F(o * n, 12 * (n + 2))
        if delta < 0:
            assert tau > 0
            needed = -delta / tau
            if needed > ratio:
                ratio, ratio_states = needed, [list(bits)]
            elif needed == ratio:
                ratio_states.append(list(bits))

        # Check formal scalar coefficients by substituting two arbitrary u values.
        # Capacity differences are globally nonnegative budgets, not atomwise signs.
        middle_caps = sum(F(p - y) for y in ys)
        terminal_cap = F(p - z)
        missing = F(p * (1 - o))
        B = w - theta / (1 + p + n)
        G = s - theta / (p + n - y5 + 2)
        for u in (F(0), F(1)):
            I = u - v
            H = 150 * u - F(139 * p, 6) - o
            H_paid = 150 * I + 3 * middle_caps + 6 * terminal_cap + 6 * B + 6 * tau + F(5, 6) * missing
            T = u - F(o, 12) + F(p, 18)
            assert H == H_paid
            assert T == I + G + delta
            new_paid = (61 * I + G + F(6, 5) * middle_caps + F(12, 5) * terminal_cap
                        + F(12, 5) * B + F(1, 3) * missing + rho)
            assert new_paid == T + F(2, 5) * H
            assert 180 * new_paid == 10980 * u - 1658 * p - 87 * o
            identities += 4
        entries.append({"bits_p_y2_y3_y4_y5_z_o": list(bits), "n": n,
                        "tau": str(tau), "delta": str(delta), "rho": str(rho)})
    assert len(entries) == 128
    assert ratio == F(12, 5)
    assert ratio_states == [[0, 0, 0, 0, 1, 0, 1]]

    # Actual six-query multiplicity d, then union weakening. This also checks
    # the separate positive slack that forces d=o in the equality argument.
    average_states = 0
    average_identities = 0
    for p, n, z, d in product((0, 1), range(5), (0, 1), range(7)):
        o, theta = int(d > 0), F(d, 6)
        total = p + n + z
        v, w = share(p, total), share(z, total)
        tau = transfer(p, n, z, theta)
        assert tau == closed_transfer(p, n, z, theta) >= 0
        literal_tau = sum((transfer(p, n, z, F(k < d)) for k in range(6)), F()) / 6
        assert tau == literal_tau
        average_states += 1
        B_d = w - theta / (1 + p + n)
        menu_slack = F(d - o, 1 + 5 * p)
        assert menu_slack >= 0 and ((menu_slack == 0) == (d == o))
        for u in (F(0), F(1)):
            H = 150 * u - F(139 * p, 6) - o
            expanded = (150 * (u - v) + 3 * (4 * p - n) + 6 * (p - z)
                        + 6 * B_d + 6 * tau + menu_slack + F(5 * p * (1 - o), 6))
            assert H == expanded
            average_identities += 1

    # Already certified point: only extract u1,K,O and evaluate the new claims.
    certificate = WORK / "universal_union_wallet_lp/exact_certificate.json"
    cert_sha = sha256(certificate.read_bytes()).hexdigest()
    assert cert_sha == "ccc085060427e2999a8e4f00ac3414d7e20a1c6e66aeba8d3e658ae34cb16c85"
    cert = json.loads(certificate.read_text())
    u, K, O = F(cert["derived"]["u1_u6"][0]), F(cert["K"]), F(cert["normalization"])
    H = 150 * u - F(139, 6) * K - O
    J = (41 * K - 6 * O) / 30
    penultimate_floor = (3 * O - 2 * K) / 36
    gap = F(23, 63) * O - K
    new_value = 10980 * u - 1658 * K - 87 * O
    assert H == 0 and O == 1 and gap > 0 and new_value < 0
    assert u == K / 5 - J / 30 == (139 * K + 6 * O) / 900
    assert K - F(5, 6) * J == O / 6 - F(5, 36) * K
    assert u < penultimate_floor
    assert new_value == F(3, 5) * (63 * K - 23 * O)
    assert (1658 * K + 87 * O) / 10980 - (139 * K + 6 * O) / 900 == (23 * O - 63 * K) / 18300

    source_files = [
        REPO / "archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md",
        REPO / "archives/customer-attraction/state/引理/任意人数近饱和根主题刚性--引理.md",
        REPO / "archives/customer-attraction/state/推论/最大主题根近饱和的覆盖阈值--推论.md",
        WORK / "main_root_near_strengthening.md", certificate,
    ]
    result = {
        "status": "PASS_ROOT_NEAR_EQUALITY_AND_QUANTITATIVE_FIFTH_SOURCE_AUDIT",
        "source_sha256": {str(p.relative_to(REPO)): sha256(p.read_bytes()).hexdigest() for p in source_files},
        "universal_quantitative_row": "10980*u1 - 1658*K - 87*O >= 0",
        "scope": "Any six legal query labels and their coverage union; a genuine globally largest legal root label; complete ordered-history pure SPE. No optimality of the forced root action is assumed.",
        "boolean_types_checked": 128,
        "mean_transfer_types_checked": average_states,
        "all_formal_affine_identity_checks": identities + average_identities,
        "tau_zero_iff_middle_bits_equal_C": True,
        "zero_tau_boolean_types": equality_zero_states,
        "rho_zero_count": sum(F(e["rho"]) == 0 for e in entries),
        "rho_positive_count": sum(F(e["rho"]) > 0 for e in entries),
        "minimum_positive_rho": str(min(F(e["rho"]) for e in entries if F(e["rho"]) > 0)),
        "sharp_single_residual_multiplier": str(ratio),
        "sharp_single_residual_witness_types": ratio_states,
        "single_residual_sharpness_scope": "Only delta+lambda*tau>=0 on the specified full Boolean domain; no claim about all proof budgets or SPE sharpness.",
        "all_128_exact_residuals": entries,
        "current_certified_point": {
            "u1": str(u), "K": str(K), "O": str(O), "H": str(H),
            "forced_equality_J": str(J), "required_penultimate_SAFE_floor": str(penultimate_floor),
            "penultimate_SAFE_shortfall": str(penultimate_floor - u),
            "threshold_23O_over_63_minus_K": str(gap),
            "new_integer_row_value": str(new_value),
            "new_root_lower_bound_minus_old": str((23 * O - 63 * K) / 18300),
            "point_excluded_from_full_SPE": True,
            "entire_217_optimal_face_checked_in_this_stage": False,
        },
        "optimizer_calls": 0,
        "old_LP_replayed_or_recomputed": False,
        "frozen_prior_audits_modified": False,
        "outstanding_errors": [],
        "subsequent_whole_face_and_new_dual_result": "face_audit_result.json",
    }
    output = HERE / "audit_result.json"
    assert not output.exists(), "refuse overwrite"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in (
        "status", "boolean_types_checked", "mean_transfer_types_checked", "all_formal_affine_identity_checks",
        "rho_zero_count", "rho_positive_count", "minimum_positive_rho", "sharp_single_residual_multiplier",
        "current_certified_point")}, ensure_ascii=False, indent=2))


def audit_face():
    """Replay Main's two signed identities and the new dual, not Main's script."""
    face_path = WORK / "main_universal_wallet_face.json"
    input_path = WORK / "universal_union_wallet_lp/exact_input.json"
    certificate_path = WORK / "universal_union_wallet_lp/exact_certificate.json"
    face = json.loads(face_path.read_text())
    data = json.loads(input_path.read_text())
    cert = json.loads(certificate_path.read_text())
    assert sha256(input_path.read_bytes()).hexdigest() == face["input_sha256"] == cert["input_sha256"]
    assert sha256(certificate_path.read_bytes()).hexdigest() == face["certificate_sha256"]
    atoms = tuple(product((0, 1), repeat=8))
    names = list(cert["dual"]["row_weights"])
    old_weights = {k: F(v) for k, v in cert["dual"]["row_weights"].items()}
    assert names == face["positive_dual_row_names"] and len(names) == 13
    assert min(old_weights.values()) > 0

    # Reconstitute only the 13 source-proved positive rows; no imported checker.
    rows = {}
    for name in names:
        values = []
        tokens = name.split("_")
        for atom in atoms:
            a, x, o = atom[:6], atom[6], atom[7]
            c, P = sum(a), sum(a[:4])
            u = [share(b, c) for b in a]
            if name in ("SAFE_2_5", "SAFE_2_6"):
                q = a[int(tokens[-1]) - 1]
                value = u[1] - F(q, a[0] + 5)
            elif name == "SAFE_6_8":
                value = u[5] - F(o, 6 * (P + a[4] + 1))
            elif tokens[0] == "UP":
                i = int(tokens[1])
                b, r, C = sum(a[:i - 1]), 7 - i, {2: 25, 3: 19, 4: 10}[i]
                value = C * u[i - 1] - (C - 1) * F(x, b + r)
                value -= F(o, 6) * (F(1, b + r) if x else F(1, b + 1))
            elif name == "MX_8":
                value = u[4] - F(o, 6 * (P + 1 + x))
            elif name == "RC_8_8":
                value = u[4] + F(x, P + 1) - F(o, 3 * (P + 1)) + F(o, 36 * (P + 1) * (P + 2))
            elif name == "ROOT_NEAR":
                value = 150 * u[0] - o
            elif name.startswith("ROOT_RIG_"):
                anchor, query = map(int, tokens[-2:])
                t, q = atom[anchor - 1], atom[query - 1]
                value = 25 * u[0] - 7 * t - F(q, 1 + 5 * t)
            else:
                raise AssertionError(name)
            values.append(F(value))
        K_coefficient = -F(139, 6) if name == "ROOT_NEAR" else F(3) if name.startswith("ROOT_RIG_") else F(0)
        rows[name] = tuple(values + [K_coefficient])
    sparse = lambda v: {str(j): str(q) for j, q in enumerate(v) if q}
    raw = {r["name"]: r for r in data["raw_rows"]}
    for name, row in rows.items():
        assert sparse(row) == raw[name]["a"] and F(raw[name]["rhs"]) == 0
    norm = tuple(F(a[7]) for a in atoms) + (F(0),)
    obj = tuple(F(any(a[:6])) for a in atoms) + (F(0),)
    K_row = (F(0),) * 256 + (F(1),)
    new_row = tuple(10980 * share(a[0], sum(a[:6])) - 87 * a[7] for a in atoms) + (F(-1658),)
    assert sparse(new_row) == face["new_row"]
    alpha = F(cert["objective"])
    old_residuals = tuple(obj[j] - alpha * norm[j] - sum(
        (old_weights[name] * rows[name][j] for name in names), F()) for j in range(257))
    assert min(old_residuals) >= 0
    assert sparse(old_residuals) == cert["dual"]["nonnegative_column_residual"]
    zero_cols = [j for j, q in enumerate(old_residuals) if not q]
    assert zero_cols == face["zero_residual_columns"]

    identity_results = {}
    for key, target in (("K_identity", K_row), ("new_row_face_identity", new_row)):
        identity = face[key]
        constant = F(identity["normalization_coefficient"])
        beta = {k: F(v) for k, v in identity["row_coefficients"].items()}
        extra = tuple(F(identity["column_coefficients"].get(str(j), "0")) for j in range(257))
        assert set(beta) == set(names)
        assert all(extra[j] == 0 for j in zero_cols)
        for j in range(257):
            assert target[j] == constant * norm[j] + sum(
                (beta[name] * rows[name][j] for name in names), F()) + extra[j]
        identity_results[key] = {
            "normalization_coefficient": str(constant), "full_columns_checked": 257,
            "row_coefficients": {k: str(v) for k, v in beta.items()},
            "extra_column_support_subset_of_positive_old_residual": True,
        }
    assert F(face["K_identity"]["normalization_coefficient"]) == F(cert["K"])
    new_constant = F(face["new_row_face_identity"]["normalization_coefficient"])
    assert new_constant == F(face["constant_new_row_on_normalized_face"]) < 0

    # Optimality in the old system forces positive-weight slacks and
    # positive-residual columns to vanish. Signed coefficients are legal only
    # for this equality argument; the new universal dual is checked separately.
    fresh = face["constructive_strict_bound"]
    gamma = F(fresh["gamma"])
    beta = {k: F(v) for k, v in face["new_row_face_identity"]["row_coefficients"].items()}
    extra = tuple(F(face["new_row_face_identity"]["column_coefficients"].get(str(j), "0")) for j in range(257))
    updated = {name: old_weights[name] - gamma * beta[name] for name in names}
    bound = alpha - gamma * new_constant
    remainder = tuple(old_residuals[j] - gamma * extra[j] for j in range(257))
    assert gamma > 0 and min(updated.values()) >= 0 and min(remainder) >= 0
    assert updated["ROOT_NEAR"] == 0
    assert {k: str(v) for k, v in updated.items() if v} == fresh["old_row_weights"]
    assert bound == F(fresh["bound"]) == F(366720231019228542915, 860670652474859546101) > alpha
    assert gamma == F(fresh["new_root_row_weight"]) == F(89213252833200687, 3442682609899438184404)
    assert sparse(remainder) == fresh["nonnegative_column_residual"]
    for j in range(257):
        assert obj[j] - bound * norm[j] == sum(
            (updated[name] * rows[name][j] for name in names), F()) + gamma * new_row[j] + remainder[j]
    assert F(fresh["improvement"]) == bound - alpha
    assert fresh["matching_primal_claimed"] is False and fresh["best_known_bound_claimed"] is False
    result = {
        "status": "PASS_WHOLE_OLD_OPTIMAL_FACE_AND_CONSTRUCTIVE_NEW_UNIVERSAL_DUAL",
        "source_sha256": {str(p.relative_to(REPO)): sha256(p.read_bytes()).hexdigest()
                          for p in (face_path, input_path, certificate_path)},
        "critical_old_rows_independently_rebuilt": 13,
        "critical_old_coefficient_checks": 13 * 257,
        "old_dual_columns_replayed_for_face_support": 257,
        "zero_old_residual_columns": zero_cols,
        "full_signed_identities": identity_results,
        "whole_old_optimal_face_excluded_by_true_new_row": True,
        "new_row_value_everywhere_on_old_normalized_optimal_face": str(new_constant),
        "new_valid_universal_bound": str(bound),
        "old_valid_bound": str(alpha), "improvement": str(bound - alpha),
        "new_row_multiplier": str(gamma),
        "updated_old_budget_weights": {k: str(v) for k, v in updated.items()},
        "new_all_257_column_residuals": [str(v) for v in remainder],
        "new_positive_column_residual_count": sum(v > 0 for v in remainder),
        "new_zero_column_residual_count": sum(v == 0 for v in remainder),
        "new_ROOT_NEAR_weight": str(updated["ROOT_NEAR"]),
        "all_new_budget_weights_nonnegative": True,
        "all_new_column_residuals_nonnegative": True,
        "matching_primal_or_new_optimum_claimed": False,
        "best_known_bound_claimed": False,
        "Main_script_executed": False,
        "optimizer_called": False,
        "outstanding_errors": [],
    }
    output = HERE / "face_audit_result.json"
    assert not output.exists(), "refuse overwrite"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in (
        "status", "critical_old_coefficient_checks", "whole_old_optimal_face_excluded_by_true_new_row",
        "new_row_value_everywhere_on_old_normalized_optimal_face", "new_valid_universal_bound",
        "new_row_multiplier", "new_positive_column_residual_count", "new_zero_column_residual_count",
        "new_ROOT_NEAR_weight")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    audit_face() if "--face" in sys.argv[1:] else main()
