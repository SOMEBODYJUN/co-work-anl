#!/usr/bin/env python3
"""Exact whole-face true-C equality diagnostics; no optimizer or new input row."""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import sys

sys.dont_write_bytecode = True
from contract import HERE, REPO, N, M, digest, load_released, read_json, require, write_new


def main():
    import sympy as sp

    bundle = load_released()
    base = HERE.parent
    data = bundle["data"]
    cert = read_json(HERE / "exact_certificate.json")
    face = read_json(HERE / "optimal_face.json")
    checked = read_json(HERE / "independent_check_result.json")
    require(checked["certificate_sha256"] == digest(HERE / "exact_certificate.json"),
            "Certificate verification binding changed")
    require(face["certificate_sha256"] == digest(HERE / "exact_certificate.json"),
            "Face binding changed")
    rows = data["raw_rows"]
    atoms = data["atom_columns"]
    z = list(map(F, cert["primal"]))
    positive = cert["dual"]["positive_raw_indices"]
    allowed = face["zero_residual_columns"]
    excluded = face["forced_zero_columns"]
    coords = face["coordinates"]
    count = face["unconstrained_affine_parameter_count"]
    require([entry["column"] for entry in coords] == allowed, "Face coordinate order differs")
    constants = [F(entry["constant"]) for entry in coords]
    coefficients = [[F(value) for value in entry["parameter_coefficients"]] for entry in coords]
    equation_vectors = bundle["E"] + [bundle["A"][i] for i in positive]
    equation_rhs = bundle["h"] + [bundle["b"][i] for i in positive]
    sr = lambda value: sp.Rational(value.numerator, value.denominator)
    fr = lambda value: F(int(value.p), int(value.q))
    matrix = sp.Matrix([[sr(row.get(j, F(0))) for j in allowed] for row in equation_vectors])

    def restrict(vector, rhs=F(0)):
        av = [vector.get(j, F(0)) for j in allowed]
        constant = sum((a * value for a, value in zip(av, constants)), F(0)) - rhs
        cs = [sum((av[k] * coefficients[k][t] for k in range(len(allowed))), F(0))
              for t in range(count)]
        return constant, cs

    def fixed(name, vector, rhs=F(0)):
        constant, cs = restrict(vector, rhs)
        require(not any(cs), name + " is not fixed on the whole affine face")
        solution = next(iter(sp.linsolve((matrix.T, sp.Matrix(
            [sr(vector.get(j, F(0))) for j in allowed])))))
        symbols = set().union(*(value.free_symbols for value in solution))
        weights = [fr(value.subs({symbol: 0 for symbol in symbols})) for value in solution]
        require(sum((a * value for a, value in zip(weights, equation_rhs)), F(0)) - rhs
                == constant, "Wrong signed identity constant: " + name)
        forced = {}
        for j in range(N):
            remainder = vector.get(j, F(0)) - sum((
                weight * row.get(j, F(0)) for weight, row in zip(weights, equation_vectors)
            ), F(0))
            require(j in excluded or remainder == 0, "Signed identity fails column " + str(j))
            if remainder:
                forced[str(j)] = str(remainder)
        require(sum((value * z[j] for j, value in vector.items()), F(0)) - rhs == constant,
                "Fixed value differs from exact representative")
        return {
            "name": name, "value": str(constant), "decimal": float(constant),
            "functional": {str(j): str(value) for j, value in vector.items() if value},
            "subtracted_rhs": str(rhs), "parameter_coefficients": [str(value) for value in cs],
            "signed_face_equation_weights": [str(value) for value in weights],
            "signed_forced_zero_column_weights": forced,
            "all513_coefficient_identities_checked": N,
            "scope": "Identity on the entire complementarity face, not a universal nonnegative payment.",
        }

    by_name = {row["name"]: i for i, row in enumerate(rows)}
    i0 = by_name["ALL_SOURCE_JOINT_REWEIGHTED_SAFE_I2_V08_TC"]
    i9 = by_name["ALL_SOURCE_JOINT_REWEIGHTED_SAFE_I2_V09_TC"]
    old9 = by_name["SOURCE2_MAXIMUM_C_REWEIGHTED_INTERNAL_SAFE_V111_S9"]
    require(i0 == 1433 and i9 == 1441 and old9 == 1018, "Unexpected literal raw routing")
    require(i0 in positive and old9 in positive, "Both source-C budgets must have positive payment")
    theta = {int(j): F(value) for j, value in rows[i0]["theta_by_true_source"].items()}
    require(theta == {3: F(12425, 31104), 4: F(175, 432), 5: F(5, 12)},
            "Actual positive-source parameters changed")
    require({int(j): F(value) for j, value in rows[i9]["theta_by_true_source"].items()} == theta,
            "The two C histories use different internal parameters")
    require(all(value > 0 for value in theta.values()), "All three internal SAFE weights must be positive")
    source_minimum_path = base / "all_source_joint_reweighted_safe/minimum_tables.json"
    source_tables = read_json(source_minimum_path)
    source_lookup = {(entry["vertex"], entry["p"], entry["t"], entry["o"]): entry
                     for entry in source_tables}

    # New s9 is exactly old1018 minus7/10 times the C-size equality, all513 columns.
    E_C = bundle["E"][1]
    comparison = []
    for j in range(N):
        difference = bundle["A"][i9].get(j, F(0)) - bundle["A"][old9].get(j, F(0))
        expected = F(-7, 10) * E_C.get(j, F(0))
        require(difference == expected, "C endpoint equality routing fails")
        comparison.append(str(difference - expected))
    require(bundle["b"][i9] == bundle["b"][old9] == 0, "C endpoint RHS differs")

    def minimum(p, t, o, s):
        return (F(5 * t, 2) + F(24 * t, p + 5) - F(s * t, 5)
                + F(o, 6 * (p + 1 + 4 * t))
                + sum((weight * F(o, 6 * (p + (j - 2) * t + 7 - j))
                       for j, weight in theta.items()), F(0)))

    def cost(p, t, d, tail, s):
        r3, r4, r5, r6 = tail
        load = p + t + sum(tail)
        a = 25 + sum(theta.values(), F(0)) - s
        numerator = a * t - r6 - sum((theta[j] * tail[j - 3] for j in theta), F(0))
        require(load or numerator == 0, "Zero-load numerator is nonzero")
        share = numerator / load if load else F(0)
        return (share + F(r3 + r4 + r5, 2) + r6
                + F(d, 6 * (p + t + r3 + r4 + r5 + 1))
                + theta[3] * F(d, 6 * (p + t + 4))
                + theta[4] * F(d, 6 * (p + t + r3 + 3))
                + theta[5] * F(d, 6 * (p + t + r3 + r4 + 2)))

    states = []
    minima = []
    zeros = {0: {}, 9: {}}
    raw_column_rechecks = 0
    menu_checks = 0
    for s, index, vertex in [(0, i0, "I2_V08"), (9, i9, "I2_V09")]:
        a = 25 + sum(theta.values(), F(0)) - s
        require(a == F(rows[index]["source_IC_weight"]), "Source IC weight changed")
        for atom in atoms:
            j = atom["index"]
            actual = atom["a"]
            u2 = F(actual[1], sum(actual)) if actual[1] else F(0)
            coefficient = a * u2 - minimum(actual[0], atom["c"], atom["o"], s)
            require(coefficient == bundle["A"][index].get(j, F(0)), "Full C row formula differs")
            raw_column_rechecks += 1
        require(bundle["A"][index][512] == F(5, 2), "New raw K column changed")
        raw_column_rechecks += 1
        for p, t, o in product([0, 1], repeat=3):
            target = minimum(p, t, o, s)
            tails = []
            values = []
            for tail in product([0, 1], repeat=4):
                value = cost(p, t, o, tail, s)
                excess = value - target
                require(excess >= 0, "True endpoint cost is below the frozen minimum")
                load = p + t + sum(tail)
                record = {
                    "s": s, "vertex": vertex, "p": p, "c": t, "o": o,
                    "tail": list(tail), "load": load, "cost": str(value),
                    "minimum": str(target), "excess": str(excess),
                    "forced_source_share": str(F(t, load) if load else F(0)),
                }
                states.append(record)
                values.append(value)
                if excess == 0:
                    tails.append(list(tail))
            require(min(values) == target, "Minimum not attained")
            expected = source_lookup[(vertex, p, t, o)]
            require(target == F(expected["minimum"]) and tails == expected["all_attaining_tails"],
                    "Frozen all-attaining-tail table differs")
            zeros[s][(p, t, o)] = tails
            minima.append({
                "s": s, "vertex": vertex, "p": p, "c": t, "o": o,
                "minimum": str(target), "all_zero_tails": tails,
            })
        for p, t in product([0, 1], repeat=2):
            for tail in product([0, 1], repeat=4):
                r3, r4, r5, r6 = tail
                coefficient = (F(1, p + t + r3 + r4 + r5 + 1)
                               + theta[3] / (p + t + 4)
                               + theta[4] / (p + t + r3 + 3)
                               + theta[5] / (p + t + r3 + r4 + 2))
                for menu in product([0, 1], repeat=6):
                    d = sum(menu)
                    o = int(d > 0)
                    gap = cost(p, t, d, tail, s) - cost(p, t, o, tail, s)
                    require(gap == F(d - o, 6) * coefficient and gap >= 0,
                            "Literal same-menu weakening differs")
                    menu_checks += 1
    require(len(states) == 256 and len(minima) == 16 and raw_column_rechecks == 1026,
            "Incomplete endpoint checks")
    intersections = []
    for p, t, o in product([0, 1], repeat=3):
        common = sorted(set(map(tuple, zeros[0][(p, t, o)]))
                        & set(map(tuple, zeros[9][(p, t, o)])))
        require(common, "The common zero set is empty unexpectedly")
        for tail in common:
            load = p + t + sum(tail)
            share = F(t, load) if load else F(0)
            require(share == F(t, 5), "Common zero state does not have source share c/5")
            if t:
                require(tail[:3] == (1, 1, 1), "A C client loses an intermediate cover")
        # Even either endpoint separately has all three middles on C.
        require(not t or all(tail[:3] == [1, 1, 1]
                             for s in [0, 9] for tail in zeros[s][(p, t, o)]),
                "Single-endpoint middle-cover condition differs")
        intersections.append({
            "p": p, "c": t, "o": o, "all_common_zero_tails": [list(tail) for tail in common],
            "common_forced_source_share": str(F(t, 5)),
        })
    require(sum(len(entry["all_common_zero_tails"]) for entry in intersections) == 13,
            "A weak common zero state was dropped")

    u2vec = {atom["index"]: F(atom["a"][1], sum(atom["a"]))
             for atom in atoms if atom["a"][1]}
    gapvec = dict(u2vec)
    gapvec[512] = F(-1, 5)
    # The two positive raw rows directly fix u2=K/5, without any support argument.
    direct_identity_residual = []
    for j in range(N):
        payment = (bundle["A"][i0].get(j, F(0)) - bundle["A"][old9].get(j, F(0))) / 9
        payment += F(5, 18) * E_C.get(j, F(0))
        require(payment == gapvec.get(j, F(0)), "Direct s0/s9 identity fails")
        direct_identity_residual.append(str(gapvec.get(j, F(0)) - payment))
    functionals = [
        fixed("K", {512: F(1)}), fixed("u2_minus_K_over5", gapvec),
        fixed("size_A1", {atom["index"]: F(atom["a"][0]) for atom in atoms if atom["a"][0]}),
        fixed("C_outside_O_mass", {atom["index"]: F(1) for atom in atoms if atom["c"] and not atom["o"]}),
        fixed("O_outside_C_mass", {atom["index"]: F(1) for atom in atoms if atom["o"] and not atom["c"]}),
    ]
    Nvecs = {}
    for j in [3, 4, 5]:
        Nvecs[j] = {atom["index"]: F(atom["o"], 6 * (atom["a"][0] + (j - 2) * atom["c"] + 7 - j))
                   for atom in atoms if atom["o"]}
        vector = {index: -value for index, value in Nvecs[j].items()}
        vector[512] = F(1, 5)
        functionals.append(fixed("K_over5_minus_N" + str(j), vector))
    delta = {j: Nvecs[5].get(j, F(0)) - Nvecs[3].get(j, F(0)) for j in range(512)}
    functionals.append(fixed("N5_minus_N3", delta))
    for index in [868, 927, 1002, i0, i9, old9]:
        functionals.append(fixed("raw_slack_" + str(index), bundle["A"][index], bundle["b"][index]))
    values = {entry["name"]: F(entry["value"]) for entry in functionals}
    require(values["u2_minus_K_over5"] == 0, "Whole-face source identity is nonzero")
    require(all(values["K_over5_minus_N" + str(j)] < 0 for j in [3, 4, 5]),
            "The advertised whole-face SAFE contradiction is absent")
    require(values["K"] < 1 and values["C_outside_O_mass"] == 0
            and values["O_outside_C_mass"] == 1 - values["K"], "C/O face quantities differ")
    require(values["N5_minus_N3"] == (1 - values["K"]) / 24 > 0,
            "Whole-face mean SAFE difference differs")

    # Known ROOT270 remainder: verify its actual128 residuals, never add a new row.
    root_input_path = base / "maximal_root_tail_wallet_v3/exact_input.json"
    root_cert_path = base / "maximal_root_tail_wallet_v3/exact_certificate.json"
    root_input = read_json(root_input_path)
    root_cert = read_json(root_cert_path)
    require(root_input["semantic_bit_order"] == ["C", "B2", "B3", "B4", "B5", "B6", "o"],
            "Root source routing changed")
    eta = F(1087978231314917, 84387869309613600)
    root_checks = []
    outside = []
    for atom in root_input["atoms"]:
        j = atom["index"]
        indicator = atom["bits"][0] * (1 - atom["bits"][-1])
        old_residual = F(root_cert["dual"]["column_residuals"][str(j)])
        reduced = old_residual - eta * indicator
        require(reduced >= 0, "Known root remainder fails")
        root_checks.append({"column": j, "bits": atom["bits"],
                            "old_residual": str(old_residual), "reduced_residual": str(reduced)})
        if indicator:
            outside.append(old_residual)
    require(len(root_checks) == 128 and len(outside) == 32 and min(outside) == eta,
            "Incomplete root remainder check")
    require(values["raw_slack_868"] == values["C_outside_O_mass"] == 0,
            "The known root remainder unexpectedly separates the face")

    old_certificate_path = base / "visible_maximum_joint_v2_solve/exact_certificate.json"
    require(digest(old_certificate_path) == "b9c1d5339b21823b5f448f8c8242bf8b1394b181c099c2bf7d87c68d3f227aea",
            "Previous actually solved certificate changed")
    old_certificate = read_json(old_certificate_path)
    old_positive = {entry["name"]: entry for entry in old_certificate["dual"]["positive_raw_rows"]}
    new_positive = {entry["name"]: entry for entry in cert["dual"]["positive_raw_rows"]}
    changes = {
        "status": "EXACT_COMPARISON_WITH_PREVIOUS_ACTUALLY_SOLVED1003_SYSTEM",
        "prior_certificate_sha256": digest(old_certificate_path),
        "new_certificate_sha256": digest(HERE / "exact_certificate.json"),
        "prior_objective": old_certificate["objective"], "new_objective": cert["objective"],
        "objective_improvement": str(F(cert["objective"]) - F(old_certificate["objective"])),
        "objective_improvement_decimal": float(F(cert["objective"]) - F(old_certificate["objective"])),
        "entered": [new_positive[name] for name in sorted(new_positive.keys() - old_positive.keys())],
        "exited": [old_positive[name] for name in sorted(old_positive.keys() - new_positive.keys())],
        "retained": [{"name": name, "old": old_positive[name], "new": new_positive[name]}
                     for name in sorted(new_positive.keys() & old_positive.keys())],
        "unsolved1050_has_no_numerical_comparison": True,
        "prior_primal_used_for_new_solve_or_recovery": False,
        "optimizer_calls": 0,
    }
    source_paths = [
        source_minimum_path, base / "all_source_joint_reweighted_safe/proof.md",
        base / "all_source_joint_reweighted_safe/exact_family.json",
        root_input_path, root_cert_path, old_certificate_path,
    ]
    write_new(HERE / "diagnostic_source_pins.json",
              {str(path.relative_to(REPO)): digest(path) for path in source_paths})
    write_new(HERE / "positive_payment_changes.json", changes)
    write_new(HERE / "true_branch_face_functionals.json", {
        "status": "PASS_EXACT_WHOLE_FACE_FIXED_FUNCTIONALS_ALL513",
        "input_sha256": cert["input_sha256"], "certificate_sha256": digest(HERE / "exact_certificate.json"),
        "face_sha256": digest(HERE / "optimal_face.json"), "equation_names": face["equation_names"],
        "functionals": functionals, "optimizer_calls": 0,
    })
    write_new(HERE / "root_strengthening_column_check.json", {
        "status": "PASS_KNOWN_ROOT_REMAINDER_NO_SEPARATION",
        "eta": str(eta), "all128_checks": root_checks, "C_outside_O_columns": 32,
        "whole_face_ROOT270_slack": str(values["raw_slack_868"]),
        "whole_face_C_outside_O": str(values["C_outside_O_mass"]),
        "new_input_row_added": False, "optimizer_calls": 0,
    })
    diagnostic = {
        "status": "WHOLE1586_OPTIMAL_FACE_EXCLUDED_BY_TRUE_C_INTERMEDIATE_SAFE",
        "input_sha256": cert["input_sha256"], "certificate_sha256": digest(HERE / "exact_certificate.json"),
        "face_sha256": digest(HERE / "optimal_face.json"),
        "fixed_functionals_sha256": digest(HERE / "true_branch_face_functionals.json"),
        "positive_C_raw_indices": [old9, i0],
        "s0_raw_index": i0, "s9_equivalent_new_raw_index": i9,
        "raw_s9_equivalence": {
            "formula": "raw1441 = raw1018 -(7/10)*E_C",
            "all513_coefficient_residuals": comparison,
        },
        "direct_whole_face_source_identity": {
            "formula": "u2-K/5 = (raw1433-raw1018)/9 +(5/18)*E_C",
            "all513_coefficient_residuals": direct_identity_residual,
        },
        "theta_by_internal_source": {str(j): str(value) for j, value in theta.items()},
        "source_IC_weights": {"s0": str(F(rows[i0]["source_IC_weight"])),
                              "s9": str(F(rows[i9]["source_IC_weight"]))},
        "all256_endpoint_states": states, "all16_endpoint_minimum_tables": minima,
        "all8_common_zero_tables": intersections, "all_common_zero_states_count": 13,
        "literal_menu_checks": menu_checks, "new_raw_column_rechecks": raw_column_rechecks,
        "all_weak_zero_states_preserved_before_intersection": True,
        "s9_p0_c1_1110_not_deleted": True,
        "s0_p1_c1_1111_not_deleted": True,
        "c0_o1_single_middle_zero_states_preserved": True,
        "equality_argument": [
            "Both actual positive C raw rows are zero at every optimum; raw1441 equals raw1018 modulo the true C-size equality.",
            "They apply to the same exact forced label C at actual history(A1), so the given complete SPE supplies the same ordered successors to both budgets.",
            "Each nonnegative true-budget payment and each positive client's local residual must be zero for both endpoints. Retain every weak endpoint zero before intersecting.",
            "The common zero states put every C client in R3,R4,R5 and give forced-source share c/5. All three positive size caps then give cov(R3)=cov(R4)=cov(R5)=cov(C), without identifying labels.",
            "Thus v2=v3=v4=v5=K/5. Tight source IC gives actual u2=K/5, in agreement with the raw signed identity.",
            "At the genuine internal node j, the six-query SAFE budget gives vj>=Nj with Nj=sum o/[6(a1+(j-2)c+7-j)]. Actual deviations use their own true continuations.",
            "The entire face has K/5-N3<0 (and also K/5-N4<0,K/5-N5<0), with full513 signed identities. Therefore no point on this optimum face is a genuine complete ordered pure SPE projection.",
        ],
        "additional_single_endpoint_observation": [
            "Already every C-client zero of the positive s9 endpoint covers all three middles; their positive caps give each middle exactly C.",
            "Hence v3=v5=v2. Its positive theta3/theta5 true SAFE means both take equality.",
            "Their mean query cost difference is sum d*(1-c)/[3(a1+2)(a1+4)], strictly positive for any queried client outside C.",
            "Equality therefore forces O subset C; the whole face instead has |O outside C|=1-K>0. This uses the same six legal queries and no new input row.",
        ],
        "whole_face_contradiction_gaps": {
            str(j): str(values["K_over5_minus_N" + str(j)]) for j in [3, 4, 5]
        },
        "whole_face_N5_minus_N3": str(values["N5_minus_N3"]),
        "whole_face_O_outside_C_mass": str(values["O_outside_C_mass"]),
        "old_P25_C_Omean_slack": str(values["raw_slack_927"]),
        "old_NS5_slack": str(values["raw_slack_1002"]),
        "old_P25_and_NS5_equality_arguments_used": False,
        "unfrozen_ordered_menu_rows_used": False,
        "fixed_C_734_bound": False, "phaseI_calls": 0, "optimizer_calls": 0,
        "scope": "Exact nonattainment of the necessary-cone optimum, not a quantified larger universal epsilon or the six-player half theorem.",
    }
    write_new(HERE / "true_branch_equality_diagnostic.json", diagnostic)
    print(json.dumps({
        "status": diagnostic["status"], "endpoint_states": len(states),
        "common_zero_states": 13, "menu_checks": menu_checks,
        "fixed_gaps": diagnostic["whole_face_contradiction_gaps"],
        "O_outside_C": diagnostic["whole_face_O_outside_C_mass"],
        "improvement_over_previous_solved1003": changes["objective_improvement_decimal"],
        "optimizer_calls": 0,
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
