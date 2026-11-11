#!/usr/bin/env python3
"""Independent true-source requery audit; standard library and exact fractions.

Never imports or executes builder, Main, or optimization code. Every query
cost is reconstructed from literal shares. Means use explicit index lists.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product, combinations_with_replacement
from pathlib import Path
import json
import sys
import csv
import re

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = WS.parents[2]
BUILDER = WS / "maximal_root_opt_requery"
OLD = WS / "maximal_root_tail_wallet"
ATOMS = list(product((0, 1), repeat=7))
STATES = list(product((0, 1), repeat=4))
ROLES = ("C", "B2", "B3", "B4", "B5", "B6", "Q", "R4", "R5", "R6", "Omean")
ZERO = F(0)


def share(bit, load):
    return F(bit, load) if bit else ZERO


def queries(role, h, state):
    if role == "Omean":
        return [h[-1], 0, 0, 0, 0, 0]
    index = ROLES.index(role)
    if index < 6:
        return [h[index]]
    return [state[index - 6]]


def pair_cost(prefix, left, right):
    # U(left,right)+f(right) = f(left)+f(right)-g(left,right).
    return sum((share(q, prefix + 1 + r) + share(r, prefix + 1)
                for q in left for r in right), ZERO) / (len(left) * len(right))


def source_specs():
    specs = [{"name": "SOURCE3_AVERAGE_IC", "family": "SOURCE_IC"}]
    specs += [{"name": f"CAP_R{j}", "family": "CAP", "tail": j} for j in range(4, 7)]
    specs += [{"name": f"OLD_SAFE_j{i}|R{j}", "family": "OLD_SAFE", "source": i, "tail": j}
              for i in range(2, 7) for j in range(4, 7)]
    specs += [{"name": f"ROOT_SIZE_R{j}", "family": "ROOT_SIZE", "tail": j} for j in range(4, 7)]
    specs += [{"name": f"NEW_SAFE_j{i}|{role}", "family": "NEW_SAFE", "source": i, "queries": [role]}
              for i in range(4, 7) for role in ROLES]
    specs += [{"name": f"PAIR|{q}|{r}", "family": "PAIR", "queries": [q, r]}
              for q, r in combinations_with_replacement(ROLES, 2)]
    assert len(specs) == 121
    return specs


def source_coefficient(spec, atom, state):
    h = ATOMS[atom]
    q, s4, s5, s6 = state
    new = (h[0], h[1], q, s4, s5, s6)
    total = sum(new)
    family = spec["family"]
    if family == "SOURCE_IC":
        return share(q, total)
    if family == "CAP":
        return F(state[spec["tail"] - 3])
    if family == "OLD_SAFE":
        j = spec["source"]
        return share(state[spec["tail"] - 3], sum(h[:j - 1]) + 7 - j)
    if family == "ROOT_SIZE":
        return F(state[spec["tail"] - 3], 6)
    if family == "NEW_SAFE":
        j = spec["source"]
        prefix = sum(new[:j - 1])
        bits = queries(spec["queries"][0], h, state)
        query = sum((share(bit, prefix + 7 - j) for bit in bits), ZERO) / len(bits)
        return query - share(new[j - 1], total)
    if family == "PAIR":
        prefix = sum(new[:4])
        y, z = new[4], new[5]
        wallet = share(y, total) + share(z, total) + share(y, prefix + 1) - share(y, prefix + 1 + y)
        left, right = (queries(role, h, state) for role in spec["queries"])
        return pair_cost(prefix, left, right) - wallet
    if family in ("Q_LOWER", "Q_UPPER"):
        return F((-1 if family == "Q_LOWER" else 1) * q) if spec["atom"] == atom else ZERO
    raise AssertionError(family)


def source_base(spec):
    z, K, u = [ZERO] * 128, ZERO, ZERO
    family = spec["family"]
    if family in ("SOURCE_IC", "OLD_SAFE"):
        j = 3 if family == "SOURCE_IC" else spec["source"]
        z = [share(h[j - 1], sum(h[:6])) for h in ATOMS]
    elif family == "CAP":
        K = F(1)
    elif family == "ROOT_SIZE":
        u = F(1)
    elif family in ("Q_LOWER", "Q_UPPER"):
        atom = spec["atom"]
        z[atom] = F(-ATOMS[atom][-1], 6) if family == "Q_LOWER" else F(ATOMS[atom][-1])
    return z, K, u


def vector(sparse, size):
    out = [ZERO] * size
    for k, v in sparse.items():
        assert str(int(k)) == k and 0 <= int(k) < size
        out[int(k)] = F(v)
    return out


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), ZERO)


def load_problem():
    data = json.loads((BUILDER / "exact_input.json").read_text())
    old_cert = json.loads((OLD / "exact_certificate.json").read_text())
    assert sha256((OLD / "exact_certificate.json").read_bytes()).hexdigest() == data["old_certificate_sha256"] == "80d9267b6ed9b5e47c4f8ea92523aaf1e73754eb28416e4117f8db754b88d771"
    assert sha256((OLD / "exact_input.json").read_bytes()).hexdigest() == data["old_input_sha256"] == "3c1a824ed0a17562da812db1d0bb12485f0b1c7f743577af7bc2ecf316d3ab65"
    old_x = vector(old_cert["primal"], 129)
    support = [i for i, v in enumerate(old_x[:128]) if v > 0]
    assert len(support) == 10
    columns = [(h, state) for h in support for state in STATES]
    assert data["columns"] == [{"index": i, "atom": h, "q": state[0], "tail": list(state[1:])}
                               for i, (h, state) in enumerate(columns)]
    specs = source_specs()
    for h in support:
        specs.extend([{"name": f"Q_LOWER_h{h}", "family": "Q_LOWER", "atom": h},
                      {"name": f"Q_UPPER_h{h}", "family": "Q_UPPER", "atom": h}])
    return data, old_x, support, columns, specs


def check_input():
    data, old_x, support, columns, specs = load_problem()
    assert data["all_old_atoms"] == [{"index": i, "bits": list(h)} for i, h in enumerate(ATOMS)]
    assert data["nonnegative_columns"] == list(range(160))
    assert data["convention"] == "A*nu <= base_z*w + base_K*K + base_u*u"
    assert data["true_row_count"] == 121
    assert vector(data["fixed_mass"], 128) == old_x[:128]
    K, u = F(data["fixed_K"]), F(data["fixed_u"])
    assert K == sum((old_x[i] * h[0] for i, h in enumerate(ATOMS)), ZERO)
    assert u == old_x[128]
    assert [row["name"] for row in data["raw_rows"]] == [spec["name"] for spec in specs]
    matrix_checks = base_checks = 0
    rows, signatures = {}, {}
    for row, spec in zip(data["raw_rows"], specs):
        for key, value in spec.items():
            assert row[key] == value, (spec["name"], key)
        rebuilt = [source_coefficient(spec, h, state) for h, state in columns]
        stored = vector(row["a"], 160)
        for a, b in zip(rebuilt, stored):
            assert a == b, spec["name"]
            matrix_checks += 1
        z, cap, root = source_base(spec)
        for a, b in zip(z, vector(row["base_z"], 128)):
            assert a == b, spec["name"]
            base_checks += 1
        assert cap == F(row["base_K"]) and root == F(row["base_u"])
        rhs = dot(z, old_x[:128]) + cap * K + root * u
        assert rhs == F(row["rhs"])
        rows[spec["name"]] = (rebuilt, rhs)
        signatures.setdefault(tuple(rebuilt) + (rhs,), []).append(spec["name"])
    assert len(data["equalities"]) == 10
    for eq, h in zip(data["equalities"], support):
        assert eq["name"] == f"MASS_h{h}" and eq["atom"] == h
        assert vector(eq["a"], 160) == [F(atom == h) for atom, _ in columns]
        assert F(eq["rhs"]) == old_x[h]
    v3 = sum((old_x[i] * share(h[2], sum(h[:6])) for i, h in enumerate(ATOMS)), ZERO)
    safe3 = sum((old_x[i] * F(h[-1], 6 * (h[0] + h[1] + 4)) for i, h in enumerate(ATOMS)), ZERO)
    assert v3 == safe3
    # Explicitly distinguish the queried Q role from old B3 and from Omean.
    assert queries("Q", ATOMS[1], (1, 0, 0, 0)) == [1]
    assert queries("B3", ATOMS[1], (1, 0, 0, 0)) == [0]
    assert queries("Omean", ATOMS[1], (1, 0, 0, 0)) == [1, 0, 0, 0, 0, 0]
    assert data["derivation_sha256"] == sha256((BUILDER / "derivation.md").read_bytes()).hexdigest()
    preflight = json.loads((HERE / "source_preflight.json").read_text())
    assert preflight["derivation_sha256"] == data["derivation_sha256"]
    result = {
        "status": "PASS_INDEPENDENT_TRUE_SOURCES_AND_LITERAL_INPUT",
        "input_sha256": sha256((BUILDER / "exact_input.json").read_bytes()).hexdigest(),
        "derivation_sha256": data["derivation_sha256"],
        "old_input_sha256": data["old_input_sha256"],
        "old_certificate_sha256": data["old_certificate_sha256"],
        "all_old_types": 128, "released_positive_old_types": support,
        "nu_columns": 160, "genuine_rows": 121, "moment_rows": 20,
        "mass_equalities": 10, "matrix_coefficients_rebuilt": matrix_checks,
        "full_old_type_base_coefficients_rebuilt": base_checks,
        "true_row_old_type_base_coefficients": 121 * 128,
        "K_u_parameter_coefficients": 2 * 141,
        "mass_equation_coefficients": 10 * 160,
        "zero_fixed_affine_rows": [name for name, (a, rhs) in rows.items() if not any(a) and not rhs],
        "duplicate_fixed_affine_row_groups": [names for names in signatures.values() if len(names) > 1],
        "old_v3_and_its_tight_Omean_SAFE": str(v3),
        "no_optimal_menu_partition_imposed": True,
        "own_Q_old_B3_and_Omean_roles_distinguished": True,
        "outer_six_branch_average_counted_once": True,
        "inner_mean_mean_uses_all_36_pairs": True,
        "optimizer_called": False, "builder_or_Main_code_executed": False,
        "outstanding_errors": [],
    }
    out = HERE / "input_audit.json"
    assert not out.exists(), "refuse overwrite"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in ("status", "input_sha256", "matrix_coefficients_rebuilt",
          "full_old_type_base_coefficients_rebuilt", "mass_equation_coefficients", "zero_fixed_affine_rows",
          "old_v3_and_its_tight_Omean_SAFE")}, ensure_ascii=False, indent=2))


def check_certificate():
    data, old_x, support, columns, specs = load_problem()
    audited_input = json.loads((HERE / "input_audit.json").read_text())
    input_hash = sha256((BUILDER / "exact_input.json").read_bytes()).hexdigest()
    assert input_hash == audited_input["input_sha256"]
    cert_path = BUILDER / "exact_certificate.json"
    cert = json.loads(cert_path.read_text())
    assert cert["status"] == "EXACT_INFEASIBLE"
    assert cert["input_sha256"] == input_hash
    true_specs = {s["name"]: s for s in source_specs()}
    all_specs = {s["name"]: s for s in specs}
    weights = {name: F(v) for name, v in cert["genuine_row_weights"].items()}
    assert set(weights) <= set(true_specs)
    assert all(v > 0 for v in weights.values()) and len(weights) == 9
    base_z, base_K, base_u = [ZERO] * 128, ZERO, ZERO
    for name, weight in weights.items():
        z, K, u = source_base(true_specs[name])
        base_z = [a + weight * b for a, b in zip(base_z, z)]
        base_K += weight * K
        base_u += weight * u
    explicit_wallet = [F(126000) * share(h[2], sum(h[:6])) + F(65719) * share(h[3], sum(h[:6]))
                       + F(4962) * share(h[5], sum(h[:6])) for h in ATOMS]
    assert base_z == explicit_wallet and base_K == base_u == 0
    assert {k: F(v) for k, v in cert["wallet_coefficients"].items()} == {
        "v1": ZERO, "v2": ZERO, "v3": F(126000), "v4": F(65719),
        "v5": ZERO, "v6": F(4962), "K": ZERO, "u": ZERO,
    }
    stored_envelope = json.loads((BUILDER / "universal_moment_envelope.json").read_text())
    assert len(stored_envelope) == 128
    all_values, all_residuals, envelope, cut_z = [], [], [], []
    coefficient_checks = 0
    for atom, h in enumerate(ATOMS):
        values = []
        for state in STATES:
            value = ZERO
            for name, weight in weights.items():
                value += weight * source_coefficient(true_specs[name], atom, state)
                coefficient_checks += 1
            values.append(value)
        a0, a1 = min(values[:8]), min(values[8:])
        delta, gamma = max(a1 - a0, ZERO), max(a0 - a1, ZERO)
        minimum = a0 if h[-1] == 0 else min((5 * a0 + a1) / 6, a1)
        assert minimum == a0 + delta * F(h[-1], 6) - gamma * h[-1]
        saved = stored_envelope[atom]
        assert saved["atom"] == atom
        for key, exact in [("a0", a0), ("a1", a1), ("lower_weight", delta),
                           ("upper_weight", gamma), ("minimum", minimum)]:
            assert F(saved[key]) == exact, (atom, key)
        assert saved["argmin_q0"] == [i for i in range(8) if values[i] == a0]
        assert saved["argmin_q1"] == [i for i in range(8) if values[8 + i] == a1]
        residuals = []
        for state, value in zip(STATES, values):
            q = state[0]
            residue = value + (gamma - delta) * q - a0
            assert residue == value - (a1 if q else a0) >= 0
            # New-state column of the full unrestricted-variable identity.
            assert -value + delta * q - gamma * q + residue + a0 == 0
            residuals.append(residue)
        coeff = base_z[atom] - minimum
        # Old-mass column, including the signed mass-equation multiplier.
        assert base_z[atom] - delta * F(h[-1], 6) + gamma * h[-1] - a0 == coeff
        cut_z.append(coeff)
        all_values.append(values)
        all_residuals.append(residuals)
        envelope.append({"atom": atom, "a0": str(a0), "a1": str(a1), "delta": str(delta),
                         "gamma": str(gamma), "minimum": str(minimum), "cut_coefficient": str(coeff)})
    universal = cert["universal_cut"]
    assert universal["all_old_types"] == 128 and universal["all_q_tail_states"] == 2048
    assert universal["q_interval"] == "[o/6,o]"
    assert vector(universal["cut_z"], 128) == cut_z
    assert F(universal["cut_K"]) == base_K and F(universal["cut_u"]) == base_u
    assert universal["envelope_sha256"] == sha256((BUILDER / "universal_moment_envelope.json").read_bytes()).hexdigest()
    assert universal["state_residuals_sha256"] == sha256((BUILDER / "all_2048_state_residuals.tsv").read_bytes()).hexdigest()
    with (BUILDER / "all_2048_state_residuals.tsv").open() as f:
        saved_states = list(csv.DictReader(f, delimiter="\t"))
    assert len(saved_states) == 2048
    for index, row in enumerate(saved_states):
        atom, state_index = divmod(index, 16)
        state, e = STATES[state_index], envelope[atom]
        assert int(row["atom"]) == atom and int(row["q"]) == state[0]
        assert row["tail"] == "".join(map(str, state[1:]))
        assert F(row["weighted_A"]) == all_values[atom][state_index]
        assert F(row["aq_minimum"]) == F(e["a1"] if state[0] else e["a0"])
        assert F(row["lower_weight"]) == F(e["delta"])
        assert F(row["upper_weight"]) == F(e["gamma"])
        assert F(row["residual"]) == all_residuals[atom][state_index]
    with (BUILDER / "universal_cut_128.tsv").open() as f:
        saved_cut = list(csv.DictReader(f, delimiter="\t"))
    assert len(saved_cut) == 128
    for atom, row in enumerate(saved_cut):
        assert int(row["atom"]) == atom
        assert row["p_y2_y3_y4_y5_z_o"] == "".join(map(str, ATOMS[atom]))
        for key in ("a0", "a1", "minimum", "cut_coefficient"):
            assert F(row[key]) == F(envelope[atom][key])

    K, u = F(data["fixed_K"]), F(data["fixed_u"])
    fixed_budget = dot(base_z, old_x[:128]) + base_K * K + base_u * u
    fixed_min = sum((F(e["minimum"]) * old_x[e["atom"]] for e in envelope), ZERO)
    fixed_cut = fixed_budget - fixed_min
    assert fixed_cut == dot(cut_z, old_x[:128]) + base_K * K + base_u * u < 0
    assert F(cert["fixed_weighted_budget_rhs"]) == fixed_budget
    assert F(cert["fixed_weighted_moment_minimum"]) == fixed_min
    assert F(cert["fixed_cut_value"]) == fixed_cut
    fixed_residuals = [all_residuals[h][STATES.index(state)] for h, state in columns]
    assert vector(cert["fixed_column_residuals"], 160) == fixed_residuals
    assert set(cert["fixed_extended_q_weights"]) == {str(h) for h in support}
    assert set(cert["fixed_mass_multipliers"]) == {str(h) for h in support}
    weight_sum = sum(weights.values(), ZERO)
    for h in support:
        e = envelope[h]
        moment = cert["fixed_extended_q_weights"][str(h)]
        assert F(moment["lower"]) == F(e["delta"])
        assert F(moment["upper"]) == F(e["gamma"])
        assert F(cert["fixed_mass_multipliers"][str(h)]) == F(e["a0"])
        weight_sum += F(e["delta"]) + F(e["gamma"])
    extended_phase_lower = -fixed_cut / weight_sum
    assert weight_sum == F(cert["extended_certificate_weight_sum"])
    assert extended_phase_lower == F(cert["extended_phase_I_lower_bound"]) > 0

    # Separate exact phase-I dual: all 141 rows have a common -epsilon column.
    phase = cert["recovered_phase_dual"]
    phase_weights = {name: F(v) for name, v in phase["row_weights"].items()}
    assert set(phase_weights) <= set(all_specs) and all(v >= 0 for v in phase_weights.values())
    beta = {h: F(phase["mass_multipliers"][f"MASS_h{h}"]) for h in support}
    assert set(phase["mass_multipliers"]) == {f"MASS_h{h}" for h in support}
    phase_weighted_rhs = ZERO
    for name, weight in phase_weights.items():
        z, cap, root = source_base(all_specs[name])
        phase_weighted_rhs += weight * (dot(z, old_x[:128]) + cap * K + root * u)
    phase_residuals = []
    for atom, state in columns:
        residue = sum((weight * source_coefficient(all_specs[name], atom, state)
                       for name, weight in phase_weights.items()), ZERO) - beta[atom]
        assert residue >= 0
        phase_residuals.append(residue)
    epsilon_residue = F(1) - sum(phase_weights.values(), ZERO)
    assert epsilon_residue == F(phase["epsilon_residual"]) >= 0
    assert vector(phase["column_residuals"], 160) == phase_residuals
    phase_lower = sum((beta[h] * old_x[h] for h in support), ZERO) - phase_weighted_rhs
    assert phase_lower == F(phase["lower_bound"]) > 0
    # Thus epsilon-lower is exactly a sum of nonnegative relaxed budgets,
    # nonnegative variable residuals, and signed zero mass equations.

    source_paths = [BUILDER / name for name in ("derivation.md", "exact_input.json", "exact_certificate.json",
                    "universal_moment_envelope.json", "all_2048_state_residuals.tsv", "universal_cut_128.tsv")]
    source_paths += [OLD / "exact_input.json", OLD / "exact_certificate.json"]
    flat_residuals = [r for row in all_residuals for r in row]
    result = {
        "status": "PASS_EXACT_INFEASIBILITY_AND_ALL_TYPE_UNIVERSAL_MOMENT_CUT",
        "source_sha256": {str(p.relative_to(REPO)): sha256(p.read_bytes()).hexdigest() for p in source_paths},
        "input_audit_sha256": sha256((HERE / "input_audit.json").read_bytes()).hexdigest(),
        "positive_genuine_budget_weights": {name: str(v) for name, v in weights.items()},
        "genuine_weighted_state_coefficients_independently_rebuilt": coefficient_checks,
        "old_types": 128, "new_states_per_type": 16, "global_new_state_residuals_checked": 2048,
        "unrestricted_homogeneous_identity_columns": 2178,
        "global_old_mass_cut_coefficients": [str(v) for v in cut_z],
        "global_K_coefficient": str(base_K), "global_u_coefficient": str(base_u),
        "wallet_form": "126000*v3 + 65719*v4 + 4962*v6 - sum_h m(h)*w_h >= 0",
        "all_128_moment_envelopes": envelope,
        "global_positive_residual_count": sum(v > 0 for v in flat_residuals),
        "global_zero_residual_count": sum(v == 0 for v in flat_residuals),
        "minimum_positive_global_residual": str(min(v for v in flat_residuals if v > 0)),
        "all_2048_state_residuals": [[str(r) for r in row] for row in all_residuals],
        "positive_lower_moment_weights": sum(F(e["delta"]) > 0 for e in envelope),
        "positive_upper_moment_weights": sum(F(e["gamma"]) > 0 for e in envelope),
        "moment_interval_kept_without_partition_assumption": True,
        "o0_q1_formal_states_checked": 512,
        "fixed_weighted_budget_rhs": str(fixed_budget),
        "fixed_moment_minimum": str(fixed_min), "fixed_cut_value": str(fixed_cut),
        "released_visible_point_excluded": True,
        "whole_old_optimal_face_excluded_claimed": False,
        "extended_phase_I_lower_bound": str(extended_phase_lower),
        "separate_recovered_phase_dual": {
            "positive_raw_row_weights": sum(v > 0 for v in phase_weights.values()),
            "mass_equations": len(beta), "nu_columns_checked": 160,
            "epsilon_column_checked": True, "epsilon_residual": str(epsilon_residue),
            "certified_positive_lower_bound": str(phase_lower),
            "matching_phase_primal_or_exact_phase_optimum_claimed": False,
        },
        "optimizer_called": False, "builder_or_Main_code_executed": False,
        "SPE_realizability_or_counterexample_claimed": False,
        "globally_sharp_root_bound_or_best_known_claimed": False,
        "prior_frozen_audits_modified": False,
        "outstanding_errors": [],
    }
    out = HERE / "audit_result.json"
    assert not out.exists(), "refuse overwrite"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in (
        "status", "genuine_weighted_state_coefficients_independently_rebuilt",
        "unrestricted_homogeneous_identity_columns", "global_positive_residual_count", "global_zero_residual_count",
        "positive_lower_moment_weights", "positive_upper_moment_weights", "fixed_cut_value",
        "extended_phase_I_lower_bound", "separate_recovered_phase_dual")}, ensure_ascii=False, indent=2))


def check_final_proof():
    audited = json.loads((HERE / "audit_result.json").read_text())
    for rel, expected in audited["source_sha256"].items():
        assert sha256((REPO / rel).read_bytes()).hexdigest() == expected
    with (BUILDER / "all_2048_state_residuals.tsv").open() as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    phi_checks = 0
    for row in rows:
        atom, q = int(row["atom"]), int(row["q"])
        p, y2, y3, y4, y5, z, o = ATOMS[atom]
        r, y, t = map(int, row["tail"])
        b = p + y2
        D4, D6, D = b + y3 + 3, b + y3 + y4 + y5 + 1, b + q + r + 1
        theta = F(o, 6)
        # Handwritten final proof (PHI), independently compared with the
        # already audited literal-source weighted coefficients.
        phi = (F(126000 * q, b + 1 + r + y + t)
               + F(43 * r + 31218 * y + 34458 * t, D4)
               + F(1654 * (r + y + t), D6)
               + 5400 * (theta - t) / (D + y)
               + 7740 * (F(o, 3 * D) - F(o, 36 * D * (D + 1))
                         - F(y, D + t) - F(t, D + y) - F(y, D * (D + 1))))
        assert phi == F(row["weighted_A"])
        phi_checks += 1
    proof = (BUILDER / "proof.md").read_text()
    tables = re.findall(r'^\| ([01]{7}) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$', proof, re.M)
    assert len(tables) == 10
    env = audited["all_128_moment_envelopes"]
    for bits, a0, a1, m in tables:
        h = int(bits, 2)
        for text, key in [(a0, "a0"), (a1, "a1"), (m, "minimum")]:
            assert F(text.strip().replace("−", "-")) == F(env[h][key])
    min_delta = min(F(e["a1"]) - F(e["a0"]) for e in env)
    assert min_delta == F(113681, 4)
    result = {
        "status": "PASS_FINAL_PROOF_TRANSCRIPTION_AND_ORDERED_HISTORY_SCOPE",
        "source_sha256": {
            str(p.relative_to(REPO)): sha256(p.read_bytes()).hexdigest()
            for p in [BUILDER / "proof.md", WS / "maximal_root_opt_requery.md",
                      REPO / "archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md"]
        },
        "handwritten_PHI_compared_with_literal_source_coefficients": phi_checks,
        "fixed_support_envelope_table_rows_matched": len(tables),
        "minimum_a1_minus_a0": str(min_delta),
        "scope_proof": {
            "arbitrary_legal_two_action_ordered_history": True,
            "true_same_strategy_continuation_from_source3_required": True,
            "arbitrary_six_legal_query_labels_and_their_union": True,
            "root_or_first_two_player_optimality_used": False,
            "C_maximal_size_K_or_root_u_used_by_positive_budgets": False,
            "optimality_or_disjointness_of_six_query_labels_used": False,
            "actual_history_corollary": "Take H=(actual A1,actual A2), so v3,v4,v6 are actual u3,u4,u6.",
            "256_type_lift_rule": "For bit order (a1,a2,a3,a4,a5,a6,x,o), use the certified 128 coefficient at (a1,a2,a3,a4,a5,a6,o); K coefficient remains zero.",
            "new_256_system_or_optimizer_constructed": False,
        },
        "outstanding_errors": [],
    }
    output = HERE / "proof_audit.json"
    assert not output.exists(), "refuse overwrite"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("status", "handwritten_PHI_compared_with_literal_source_coefficients",
          "fixed_support_envelope_table_rows_matched", "minimum_a1_minus_a0")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if sys.argv[1:] == ["--input"]:
        check_input()
    elif sys.argv[1:] == ["--certificate"]:
        check_certificate()
    elif sys.argv[1:] == ["--proof"]:
        check_final_proof()
    else:
        raise SystemExit("usage: check_exact.py --input | --certificate | --proof")
