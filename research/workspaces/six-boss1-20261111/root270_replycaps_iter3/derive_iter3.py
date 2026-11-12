#!/usr/bin/env python3
"""Exact ROOT3 binding and ROOT3-to-ROOT4 true-budget reweighting."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import os

P = Path(__file__).resolve().parent
INPUT = Path(os.environ.get("ROOT270_FROZEN_INPUT_ROOT", "/workspace/scratch/b0fef5ec503f"))
OLD = INPUT / "root270_equality_stage"
PREV = INPUT / "root270_replycaps_iter2_stage"
AGENT = "/root/high_lambda_closure"
RUN = "six-boss1-20261111"
H = list(product((0, 1), repeat=7))
TAILS = list(product((0, 1), repeat=3))
PTAILS = list(product((0, 1), repeat=2))
EPS = F(215, 3)
B = F(37482242363557, 1875285984658080)
ETA = F(1087978231314917, 84387869309613600)
A2 = F(66400039579513467522586981249, 633435930915908109658396979040)
ZSTAR = F(64038719369580574756325, 56305416081414054191857509248)
A3 = F(265603424292741718699660497571, 2533743723663632438633587916160)
YSTAR = F(214288412699877216115223075, 102518086330234639169824559963296)
A4 = F(644801865488859242734539976772381, 6151085179814078350189473597797760)
NAMES = ["ROOT_IC", "CAP_B2", "CAP_B3", "CAP_B4", "CAP_B5", "CAP_B6",
         "SAFE6_OMEAN", "PAIR30", "C30_CAP_R4", "P25_4_B6_OMEAN"]
KCOL = [F(0)] + [F(1)] * 5 + [F(0), F(0), EPS, F(3, 2)]
DZ = list(map(F, [0, 0, 0, 0])) + [-F(4, 3), F(1), F(2), -F(1), F(0), F(0)]
DY = [F(0), F(0), F(0), F(299, 12), -F(17, 12), -F(169, 18),
      F(1), -F(1), F(0), F(1)]
BCZ = F(4, 5)
BCY = F(721, 45)
GZ = F(17, 15)
GY = F(37, 90)
EXPECTED_MANIFESTS = {
    "root270_equality_stage": "45ec2e50dadfad5a1e238714ddddddf496d4fccd2ff87f4c190f1a71bcf4afd1",
    "root270_replycaps_iter2_stage": "cdbccee0390148a83e4aa4ee2b03694c10ad0a3e02d1bba2254522d157a0e6f8",
}
SOURCE_NAMES = {
    "root270_equality_stage": ["proof.md", "freeze_manifest.json", "all128_root_remainders.json",
                              "ROOT270_C30_R4_CAP_STRICT.json"],
    "root270_replycaps_iter2_stage": ["proof.md", "freeze_manifest.json", "root270_reply_cap_erratum.md",
                                     "parameter_family.json", "direction_certificate.json",
                                     "true_state_tables.json", "ROOT270_REPLY_CAP_REWEIGHTED.json"],
}


def enc(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): enc(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [enc(v) for v in x]
    return x


def save(name, value):
    (P / name).write_text(json.dumps(enc(value), ensure_ascii=False, indent=2) + "\n")


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_and_pin_sources():
    checks = 0
    for stage, expected in EXPECTED_MANIFESTS.items():
        root = INPUT / stage
        assert sha(root / "freeze_manifest.json") == expected
        for item in read(root / "freeze_manifest.json")["artifacts"]:
            assert sha(root / item["path"]) == item["sha256"]
            checks += 1
    pins = [{"stage": stage, "path": name, "sha256": sha(INPUT / stage / name)}
            for stage, names in SOURCE_NAMES.items() for name in names]
    artifact = {"input_root": str(INPUT), "sources": pins,
                "frozen_manifest_sha256": EXPECTED_MANIFESTS,
                "verified_old_artifact_hashes": checks,
                "scope": "Only the two previously frozen local mathematical packages."}
    if (P / "source_pins.json").exists():
        assert read(P / "source_pins.json") == artifact
    else:
        save("source_pins.json", artifact)
    return checks


def phi(h, q, r, y, z):
    c, b2, b3, b4, b5, b6, o = h
    s = c + b2
    D = 1 + s + q + r
    return (F(126000 * q, s + 1 + r + y + z)
            + F(43 * r + 31218 * y + 34458 * z, s + b3 + 3)
            + F(1654 * (r + y + z), s + b3 + b4 + b5 + 1)
            + 5400 * F(F(o, 6) - z, D + y)
            + 7740 * (F(o, 3 * D) - F(y, D + z) - F(z, D + y) - F(y, D * (D + 1)))
            + EPS * r)


def true_state(h):
    costs = [[phi(h, q, *tail) for tail in TAILS] for q in (0, 1)]
    aq = list(map(min, costs))
    weak = [[tail for tail, value in zip(TAILS, vals) if value == low]
            for vals, low in zip(costs, aq)]
    assert aq[1] > aq[0]
    m = aq[0] + F(h[6], 6) * (aq[1] - aq[0])
    p = sum(h[:3])
    t = h[5]
    pcosts = []
    for r, z in PTAILS:
        den = p + t + r + z
        first = F(25 * t - z, den) if den else F(0)
        pcosts.append(first + F(r, 2) + z + F(h[6], 6 * (p + t + r + 1)))
    pm = min(pcosts)
    pweak = [tail for tail, value in zip(PTAILS, pcosts) if value == pm]
    L = sum(h[:6])
    v = [F(bit, L) if L else F(0) for bit in h[:6]]
    D = 1 + sum(h[:4])
    rows = [-v[0]] + [-F(bit) for bit in h[1:6]] + [
        v[5] - F(h[6], 6 * (sum(h[:5]) + 1)),
        v[4] + v[5] + F(h[4], D * (D + 1)) - F(h[6], 3 * D),
        126000 * v[2] + 65719 * v[3] + 4962 * v[5] - m,
        25 * v[3] - pm,
    ]
    return {
        "bits": h, "C30_CAP_m": m, "C30_a0_a1": aq,
        "C30_all_costs_by_q": costs, "C30_all_attaining_tails": weak,
        "P25_min": pm, "P25_all_costs": pcosts, "P25_all_attaining_tails": pweak,
        "ten_real_budget_customer_coefficients": rows,
    }


def equality_basis(states, bases, symbols):
    result = []
    for symbol, masses in zip(symbols, bases):
        K = sum(F(mass) * H[code][0] for code, mass in masses.items())
        size = [sum(F(mass) * H[code][j] for code, mass in masses.items()) for j in range(7)]
        shares = [sum((F(mass * H[code][j], sum(H[code][:6]))
                       for code, mass in masses.items() if sum(H[code][:6])), F(0))
                  for j in range(6)]
        budgets = [sum(F(mass) * states[code]["ten_real_budget_customer_coefficients"][j]
                       for code, mass in masses.items()) + K * KCOL[j]
                   for j in range(1, 10)]
        assert size[:6] == [K] * 6
        result.append({"symbol": symbol, "masses": masses, "K": K, "sizes_c_to_o": size,
                       "branch_incomes_v1_to_v6": shares,
                       "budgets_CAP2_to_P25": budgets})
    return result


def affine_columns(base, slope, bc, dbc, rho, direction, ak, gain, states):
    ans = []
    for h, state, r, d in zip(H, states, rho, direction):
        row = state["ten_real_budget_customer_coefficients"]
        left = [-ETA * h[0] * (1 - h[6]), F(0)]
        right = [sum(w * x for w, x in zip(base, row)) + r + bc * h[0] + B * h[6],
                 sum(w * x for w, x in zip(slope, row)) + d + dbc * h[0]]
        assert left == right
        ans.append({"column": len(ans), "left_constant_and_slope": left,
                    "right_constant_and_slope": right})
    for column, left, right in [
        ("actual_u1", [F(1), F(0)], [base[0], slope[0]]),
        ("independent_K", [-ak, -gain],
         [sum(w * k for w, k in zip(base, KCOL)) - bc,
          sum(w * k for w, k in zip(slope, KCOL)) - dbc]),
        ("independent_O", [-B, F(0)], [-B, F(0)]),
    ]:
        assert left == right
        ans.append({"column": column, "left_constant_and_slope": left,
                    "right_constant_and_slope": right})
    assert len(ans) == 131
    return ans


def family(base, slope, bc, dbc, ak, gain, endpoint, rho, direction, newrho, tag):
    row_bounds = [{"h": h, "upper_bound": rho[h] / (-direction[h])}
                  for h in range(128) if direction[h] < 0]
    budget_bounds = [{"budget": NAMES[j], "upper_bound": base[j] / (-slope[j])}
                     for j in range(10) if slope[j] < 0]
    all_bounds = [x["upper_bound"] for x in row_bounds + budget_bounds]
    assert min(all_bounds) == endpoint
    weights = [x + endpoint * y for x, y in zip(base, slope)]
    assert min(weights) > 0
    assert all(x >= 0 for x in rho) and all(x >= 0 for x in newrho)
    return {
        "parameter": tag, "complete_nonnegative_domain": [F(0), endpoint],
        "K_coefficient_constant": ak, "K_coefficient_slope": gain,
        "K_coefficient_endpoint": ak + endpoint * gain,
        "budgets": NAMES, "weights_constant": base, "weights_slope": slope,
        "weights_at_endpoint": weights,
        "C_equality_constant": bc, "C_equality_slope": dbc,
        "C_equality_endpoint": bc + endpoint * dbc, "O_equality_constant": B,
        "all_negative_direction_bounds": row_bounds, "all_decreasing_budget_bounds": budget_bounds,
        "first_limiting_customer_types": [x["h"] for x in row_bounds if x["upper_bound"] == endpoint],
        "limiting_budgets": [x["budget"] for x in budget_bounds if x["upper_bound"] == endpoint],
        "complete_for_this_fixed_payment_path_only": True,
    }


def main():
    old_hashes = check_and_pin_sources()
    prev = read(PREV / "parameter_family.json")
    w2 = list(map(F, prev["normalized_weights_at_endpoint"]))
    bc2 = F(prev["C_equality_constant"]) + F(prev["s_star"]) * F(prev["C_equality_slope"])
    assert F(prev["new_K_coefficient"]) == A2
    frozen_states = read(PREV / "true_state_tables.json")["all128_types"]
    frozen_rho = {x["h"]: F(x["endpoint_rho"])
                  for x in read(PREV / "direction_certificate.json")["all128"]}
    assert A3 == A2 + GZ * ZSTAR
    assert A4 == A3 + GY * YSTAR
    states = []
    rho2 = []
    rho3 = []
    rho4 = []
    d2 = []
    d3 = []
    cert = []
    for code, h in enumerate(H):
        state = {"h": code, **true_state(h)}
        assert enc(state) == frozen_states[code]
        row = state["ten_real_budget_customer_coefficients"]
        r2 = -sum(w * x for w, x in zip(w2, row)) - bc2 * h[0] - B * h[6] - ETA * h[0] * (1 - h[6])
        assert r2 == frozen_rho[code] >= 0
        dz = row[7] - 2 * row[6] + h[5] - F(4, 3) * h[4] - F(4, 5) * h[0]
        dy = (row[7] - row[6] - row[9] + F(299, 12) * h[3]
              - F(17, 12) * h[4] - F(169, 18) * h[5] - F(721, 45) * h[0])
        assert dz == -sum(w * x for w, x in zip(DZ, row)) - BCZ * h[0]
        assert dy == -sum(w * x for w, x in zip(DY, row)) - BCY * h[0]
        r3 = r2 + ZSTAR * dz
        r4 = r3 + YSTAR * dy
        assert r3 >= 0 and r4 >= 0
        states.append(state)
        rho2.append(r2)
        rho3.append(r3)
        rho4.append(r4)
        d2.append(dz)
        d3.append(dy)
        cert.append({"h": code, "bits": h, "rho2": r2, "D2": dz, "rho3": r3,
                     "D3": dy, "rho4": r4,
                     "D2_upper_bound_if_negative": r2 / (-dz) if dz < 0 else None,
                     "D3_upper_bound_if_negative": r3 / (-dy) if dy < 0 else None})
    zeros = [[h for h in range(128) if r[h] == 0] for r in (rho2, rho3, rho4)]
    assert zeros == [[0, 1, 3, 5, 9, 17, 123], [0, 1, 3, 5, 9, 17, 123, 125],
                     [0, 1, 3, 5, 9, 17, 103, 123]]
    w3 = [x + ZSTAR * y for x, y in zip(w2, DZ)]
    bc3 = bc2 + ZSTAR * BCZ
    w4 = [x + YSTAR * y for x, y in zip(w3, DY)]
    bc4 = bc3 + YSTAR * BCY
    families = {
        "ROOT2_to_ROOT3": family(w2, DZ, bc2, BCZ, A2, GZ, ZSTAR, rho2, d2, rho3, "z"),
        "ROOT3_to_ROOT4": family(w3, DY, bc3, BCY, A3, GY, YSTAR, rho3, d3, rho4, "y"),
    }
    assert families["ROOT2_to_ROOT3"]["first_limiting_customer_types"] == [125]
    assert families["ROOT3_to_ROOT4"]["first_limiting_customer_types"] == [103]
    assert len(families["ROOT2_to_ROOT3"]["all_negative_direction_bounds"]) == 90
    assert len(families["ROOT3_to_ROOT4"]["all_negative_direction_bounds"]) == 71
    cols = {
        "ROOT2_to_ROOT3": affine_columns(w2, DZ, bc2, BCZ, rho2, d2, A2, GZ, states),
        "ROOT3_to_ROOT4": affine_columns(w3, DY, bc3, BCY, rho3, d3, A3, GY, states),
    }
    root3_basis = equality_basis(states, [{123: 1, 5: 1}, {125: 1, 3: 1}, {1: 1}, {0: 1}],
                                 ["E", "F", "X", "N"])
    root4_basis = equality_basis(states, [{103: 1, 17: 1, 9: 1}, {123: 1, 5: 1}, {1: 1}, {0: 1}],
                                 ["A", "E", "X", "N"])
    for j, record in enumerate(root3_basis):
        S, PAIR, C30, T = record["budgets_CAP2_to_P25"][5:]
        assert PAIR - S - T == [F(37, 90), F(25, 8), F(0), F(0)][j]
    for j, record in enumerate(root4_basis):
        S, PAIR, C30, T = record["budgets_CAP2_to_P25"][5:]
        assert PAIR - 2 * S == [F(1, 18), F(17, 15), F(0), F(0)][j]
    oldrow = read(PREV / "ROOT270_REPLY_CAP_REWEIGHTED.json")
    visible = {}
    visible_checks = []
    for col, atom in enumerate(list(product((0, 1), repeat=9)) + [None]):
        if atom is None:
            c2, c3, c4 = -A2, -A3, -A4
            sz, sy = -GZ, -GY
        else:
            inc = F(atom[0], sum(atom[:6])) if sum(atom[:6]) else F(0)
            c2 = c3 = c4 = inc - B * atom[7] - ETA * atom[8] * (1 - atom[7])
            sz = sy = F(0)
        assert c2 == F(oldrow["a"][str(col)])
        assert c3 == c2 + ZSTAR * sz and c4 == c3 + YSTAR * sy
        visible[str(col)] = c4
        visible_checks.append({"column": col, "ROOT2": c2, "ROOT3": c3, "ROOT4": c4,
                               "ROOT2_to_ROOT3_slope": sz, "ROOT3_to_ROOT4_slope": sy})
    save("ROOT270_REPLY_CAP_ITER4.json", {
        "name": "ROOT270_REPLY_CAP_ITER4", "family": "EXISTING_TRUE_ROOT_BUDGET_REWEIGHTING",
        "a": visible, "rhs": "0", "numerical_divisor": "1", "variables": 513,
        "independent_K_column": 512, "bit_order": ["a1", "a2", "a3", "a4", "a5", "a6", "x", "o", "c"],
        "K_coefficient": A4, "O_coefficient": B, "C_outside_coefficient": ETA,
        "K_gain_over_ROOT3": GY * YSTAR, "K_gain_over_ROOT2": A4 - A2,
        "y_parameter": YSTAR, "z_parameter": ZSTAR, "new_true_budgets_added": False,
        "root_income_is_actual_u1_only": True, "all_513_columns_preserved": True,
        "model": "Every complete ordered-history pure SPE; six players; finite unit customers; finite nonempty labelled common catalogue; C a genuine maximum; O any union of six legal queries.",
        "actual_agent_id": AGENT, "run": RUN,
    })
    save("inputs.json", {
        "actual_agent_id": AGENT, "run": RUN, "frozen_input_root": str(INPUT),
        "fixed_C30_CAP_epsilon": EPS, "ROOT2_K": A2, "ROOT3_K": A3, "ROOT4_K": A4,
        "O_coefficient": B, "C_outside_coefficient": ETA,
        "D2_budget_slopes": DZ, "D2_C_equality_slope": BCZ,
        "D3_budget_slopes": DY, "D3_C_equality_slope": BCY,
        "z_star": ZSTAR, "y_star": YSTAR, "no_optimizer_or_global_candidate_inputs": True,
    })
    save("true_state_tables.json", {"all128_types": states, "all_weak_ties_retained": True,
                                    "reconstructed_from_literal_true_costs": True})
    save("all128_direction_certificate.json", {
        "all128": cert, "ROOT2_zero_types": zeros[0], "ROOT3_zero_types": zeros[1],
        "ROOT4_zero_types": zeros[2],
        "D2_formula": "PAIR_coeff-2*SAFE_coeff+b6-4*b5/3-4*c/5",
        "D3_formula": "PAIR_coeff-SAFE_coeff-P25_coeff+299*b4/12-17*b5/12-169*b6/18-721*c/45",
    })
    save("parameter_families.json", families)
    save("all131_affine_column_identities.json", {
        "families": cols, "total_formal_scalar_coefficients": 524,
        "actual_u1_independent_K_independent_O_not_substituted": True,
    })
    save("all513_visible_column_checks.json", visible_checks)
    equality = {
        "ROOT3": {
            "zero_types": zeros[1], "symbols": ["E", "F", "X", "N"],
            "complete_CAP_structure": {"w123": "E", "w125": "F", "w5": "E", "w3": "F",
                                       "w9": "0", "w17": "0", "w1": "X", "w0": "N",
                                       "K": "E+F", "O": "X+2E+2F"},
            "formal_basis_coefficients": root3_basis,
            "positive_budget_identity": "PAIR30-SAFE6-P25=37E/90+25F/8",
            "equality_iff_K_zero": True,
        },
        "ROOT4": {
            "zero_types": zeros[2], "symbols": ["A", "E", "X", "N"],
            "complete_CAP_structure": {"w103": "A", "w123": "E", "w17": "A", "w9": "A",
                                       "w5": "E", "w3": "0", "w1": "X", "w0": "N",
                                       "K": "A+E", "O": "X+3A+2E"},
            "formal_basis_coefficients": root4_basis,
            "positive_budget_identity": "PAIR30-2*SAFE6=A/18+17E/15",
            "equality_iff_K_zero": True,
            "next_specific_obligation": "Turn this endpoint identity into another full-128 coefficient payment, checking existing weight reserves; no next uniform improvement is claimed here.",
        },
        "h0_scope": "Uncovered by C, B2,...,B6 and the selected O only; other legal labels may cover these customers until K=0 has been proved.",
        "all_equality_statements_are_necessary_structure_before_contradiction": True,
        "no_positive_K_projection_point_is_called_an_SPE": True,
    }
    save("equality_structures.json", equality)
    union = sorted(set(zeros[1] + zeros[2]))
    save("equality_weak_tails.json", {
        "types": [{"h": h, "bits": H[h], "C30_all_attaining_tails": states[h]["C30_all_attaining_tails"],
                   "P25_all_attaining_tails": states[h]["P25_all_attaining_tails"]} for h in union],
        "epsilon": EPS, "actual_menu_equality": "d=o",
        "same_k_real_R4_R5_R6_retained": True,
        "o0_q1_formal_states_retained_but_actual_mass_zero": True,
    })
    assert old_hashes == check_and_pin_sources()
    result = {
        "status": "PASS_ROOT3_BINDING_AND_ROOT4_UNIFORM_TRUE_PAYMENT",
        "actual_agent_id": AGENT, "run": RUN, "optimizer_calls": 0,
        "all128_true_types": 128, "C30_CAP_true_costs": 2048, "P25_true_costs": 512,
        "D2_negative_types": 90, "D2_first_limit": [125, ZSTAR],
        "D3_negative_types": 71, "D3_first_limit": [103, YSTAR],
        "all_outer_budget_weights_remain_strictly_positive": min(w4) > 0,
        "formal_scalar_coefficients_checked": 524, "visible_columns_per_root": 513,
        "ROOT3_K": A3, "ROOT4_K": A4, "uniform_K_gain_over_ROOT3": GY * YSTAR,
        "ROOT3_zero_types": zeros[1], "ROOT4_zero_types": zeros[2],
        "ROOT3_equality_iff_K_zero": True, "ROOT4_equality_iff_K_zero": True,
        "no_new_true_budget_added": True, "old_frozen_artifacts_unchanged": old_hashes,
        "global_welfare_combination_performed": False, "full_SPE_construction_claimed": False,
    }
    save("generator_output.json", result)
    print(json.dumps(enc(result), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
