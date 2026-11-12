#!/usr/bin/env python3
"""Independent Fraction checks of actual positive-source states and SAFE contradiction.

Does not import the source diagnostic, symbolic algebra, or any optimizer.
"""
from fractions import Fraction as F
from itertools import product
import json
import sys

sys.dont_write_bytecode = True
from contract import HERE, N, digest, load_verified_certificate, read_json, require, write_new


def main():
    bundle, cert, cert_check = load_verified_certificate()
    face = read_json(HERE / "optimal_face.json")
    face_check = read_json(HERE / "optimal_face_check_result.json")
    require(face_check["face_sha256"] == digest(HERE / "optimal_face.json"), "Face check binding changed")
    states = read_json(HERE / "current_positive_source_state_checks.json")
    diagnosed = read_json(HERE / "true_branch_equality_diagnostic.json")
    functions = read_json(HERE / "true_branch_face_functionals.json")
    require(diagnosed["source_state_artifact_sha256"] == digest(HERE / "current_positive_source_state_checks.json")
            and diagnosed["face_functionals_sha256"] == digest(HERE / "true_branch_face_functionals.json")
            and diagnosed["input_sha256"] == cert["input_sha256"], "Diagnostic artifact binding differs")
    indices = [1803, 2563, 2564, 2606]
    require(diagnosed["actual_positive_new_indices"] == indices
            and all(F(cert["dual"]["raw_row_weights"][i]) > 0 for i in indices), "Actual positive source condition fails")
    parameter = {}
    for i in indices:
        row = bundle["rows"][i]
        tau = list(map(F, row["tau3_tau4_tau5"])) if i == 1803 else [F(row["tau_by_true_source"][str(j)]) for j in [3, 4, 5]]
        cap = [F(1, 12)+tau[0]+tau[1]/72+tau[2]/36,
               F(1, 12)+tau[1]+tau[2]/36, F(1, 12)+tau[2]]
        s, a, S = F(row["s"]), F(25)+sum(tau)-F(row["s"]), F(1)+sum(cap)
        require(a == F(row["source_IC_weight"]) and a > 0 and all(v > 0 for v in cap), "Current budget positivity differs")
        parameter[i] = tau, cap, s, a, S

    computed, seen = {}, set()
    for item in states["all512_local_state_checks"]:
        i, p, t, o, tail = item["raw_index"], item["p"], item["t"], item["o"], tuple(item["tail"])
        key = i, p, t, o, tail
        require(key not in seen, "Duplicate local state record")
        seen.add(key)
        tau, cap, s, a, S = parameter[i]
        r3, r4, r5, r6 = tail
        L = p+t+r3+r4+r5+r6
        share = lambda member: F(member, L) if L else F(0)
        value = a*share(t)-share(r6)
        value -= sum((tau[k]*share(tail[k]) for k in range(3)), F(0))
        value += sum((cap[k]*tail[k] for k in range(3)), F(0))+r6
        denominators = [p+t+r3+r4+r5+1, p+t+4, p+t+r3+3, p+t+r3+r4+2]
        value += sum((weight*F(o, 6*d) for weight, d in zip([F(1)]+tau, denominators)), F(0))
        lower = S*t+F(24*t, p+5)-s*F(t, 5)
        lower += F(o, 6*(p+4*t+1))
        lower += sum((tau[k]*F(o, 6*(p+(k+1)*t+4-k)) for k in range(3)), F(0))
        require(value == F(item["cost"]) and lower == F(item["minimum"])
                and value-lower == F(item["remainder"]) and value >= lower and item["load"] == L,
                "Independent true-share local check failed")
        computed[key] = value, lower
    expected = {(i, p, t, o, tail) for i in indices for p, t, o in product([0, 1], repeat=3)
                for tail in product([0, 1], repeat=4)}
    require(seen == expected and len(seen) == 512, "Complete weak local-state coverage differs")
    zero = {}
    require(len(states["all32_minimum_tables"]) == 32, "Incomplete minimum tables")
    for table in states["all32_minimum_tables"]:
        i, p, t, o = table["raw_index"], table["p"], table["t"], table["o"]
        tail_values = [(tail, computed[(i, p, t, o, tail)][0]) for tail in product([0, 1], repeat=4)]
        lower = min(value for tail, value in tail_values)
        tails = [tail for tail, value in tail_values if value == lower]
        require(F(table["minimum"]) == lower and table["all_weak_minimizing_tails"] == [list(t) for t in tails],
                "A weak minimizing state was omitted")
        zero[i, p, t, o] = set(tails)
    require(len(zero) == 32, "Duplicated minimum-table cell")
    patterns = list(product([0, 1], repeat=6))
    require(states["all64_six_query_patterns"] == [list(menu) for menu in patterns], "Six-query pattern domain differs")
    menu_seen = set()
    for item in states["all256_menu_contexts"]:
        i, p, t, tail = item["raw_index"], item["p"], item["t"], tuple(item["tail"])
        require((i, p, t, tail) not in menu_seen, "Repeated menu context")
        menu_seen.add((i, p, t, tail))
        tau = parameter[i][0]
        r3, r4, r5, _ = tail
        d = [p+t+r3+r4+r5+1, p+t+4, p+t+r3+3, p+t+r3+r4+2]
        kernel = sum((weight/F(6*denominator) for weight, denominator in zip([F(1)]+tau, d)), F(0))
        gaps = [(sum(menu)-int(any(menu)))*kernel for menu in patterns]
        require(kernel > 0 and F(item["strictly_positive_kernel"]) == kernel
                and list(map(F, item["all64_menu_gaps"])) == gaps, "Exact menu-gap check failed")
    require(menu_seen == {(i, p, t, tail) for i in indices for p, t in product([0, 1], repeat=2)
                          for tail in product([0, 1], repeat=4)}, "Incomplete real-query menu domain")
    intersections = []
    for p, c, o in product([0, 1], repeat=3):
        tails = sorted(zero[1803, p, c, o] & zero[2606, p, c, o])
        intersections.append({"p": p, "c": c, "o": o, "all_common_weak_zero_tails": [list(tail) for tail in tails]})
    require(intersections == diagnosed["all_common_C_branch_weak_zero_states"], "Common weak zero table differs")
    for p in [0, 1]:
        require(zero[1803, p, 1, 1] == {(1, 1, 1, 1-p)}, "Single actual C-only row does not force all middle C members")
    tau_C, cap_C, s_C, a_C, S_C = parameter[1803]
    require(0 < s_C < 9 and tau_C[1] > 0 and tau_C[2] > 0, "The actual SAFE4/5 positivity conditions differ")

    atoms = bundle["data"]["atom_columns"]
    allowed, excluded = face["zero_residual_columns"], set(face["forced_zero_columns"])
    require(all(not (atoms[j]["c"] and not atoms[j]["o"]) for j in allowed if j < 512),
            "Current full face does not force C contained in O")
    positive = cert["dual"]["positive_raw_indices"]
    equations = bundle["E"]+[bundle["A"][i] for i in positive]
    rhs = bundle["h"]+[bundle["b"][i] for i in positive]
    names = [row["name"] for row in bundle["data"]["equalities"]]+[bundle["rows"][i]["name"] for i in positive]
    require(functions["equation_names"] == names, "Face identity equation order differs")
    values = {}
    for item in functions["functionals"]:
        vector = {int(j): F(value) for j, value in item["full_coefficients"].items()}
        require(item["fixed"] is True and not any(map(F, item["parameter_coefficients"])), "Unexpected nonfixed diagnostic")
        weights = list(map(F, item["signed_face_equation_weights"]))
        forced = {int(j): F(value) for j, value in item["signed_forced_zero_column_weights"].items()}
        require(len(weights) == len(equations) and set(forced).issubset(excluded), "Signed identity domain differs")
        for j in range(N):
            require(vector.get(j, F(0)) == sum((weight*row.get(j, F(0)) for weight, row in zip(weights, equations)), F(0))
                    + forced.get(j, F(0)), "A diagnostic identity fails a full column")
        constant = sum((weight*value for weight, value in zip(weights, rhs)), F(0))
        require(constant == F(item["constant"]), "Diagnostic identity affine constant differs")
        name = item["name"]
        if name.startswith("K_over5_minus_N"):
            internal = int(name[-1])
            expected_vector = {atom["index"]: -F(atom["o"], 6*(atom["a"][0]+(internal-2)*atom["c"]+7-internal))
                               for atom in atoms if atom["o"]}
            expected_vector[512] = F(1, 5)
            require(vector == expected_vector, "Internal SAFE functional is not its true branch formula")
        values[name] = constant
    require(values["C_outside_O_mass"] == values["u2_minus_K_over5_from_new_C_pair"] == 0,
            "Basic complete-face implications fail")
    require(values["K_over5_minus_N3"] > 0 and values["K_over5_minus_N4"] < 0
            and values["K_over5_minus_N5"] < 0, "Actual SAFE deficit signs differ")
    K = values["K"]
    require(0 < K < 1, "Current face K does not give strict O outside C mass")
    difference_checks = []
    for atom in atoms:
        p, c, o = atom["a"][0], atom["c"], atom["o"]
        difference = F(o, 6*(p+3*c+2))-F(o, 6*(p+2*c+3))
        stated = F(o*(1-c), 6*(p+2)*(p+3))
        require(difference == stated, "The structural N5-N4 identity fails")
        difference_checks.append(str(difference-stated))
    difference_checks.append("0")  # Both functionals have zero K coefficient.
    difference_value = values["K_over5_minus_N4"]-values["K_over5_minus_N5"]
    require(difference_value >= (1-K)/72 > 0, "Structural true-SAFE separation is not strict")
    # The actual complete face has no p=1,o=1,c=0 zero-residual column.
    require(all(not (atoms[j]["a"][0] and atoms[j]["o"] and not atoms[j]["c"])
                for j in allowed if j < 512), "A p1 outside-C O column survives")
    require(difference_value == (1-K)/36, "Actual full-face SAFE separation differs")
    result = {
        "status": "PASS_INDEPENDENT_CURRENT_SOURCE_STATES_AND_FULL_FACE_SAFE_CONTRADICTION",
        "input_sha256": cert["input_sha256"], "certificate_sha256": digest(HERE / "exact_certificate.json"),
        "face_sha256": digest(HERE / "optimal_face.json"),
        "diagnostic_sha256": digest(HERE / "true_branch_equality_diagnostic.json"),
        "current_source_state_sha256": digest(HERE / "current_positive_source_state_checks.json"),
        "face_functionals_sha256": digest(HERE / "true_branch_face_functionals.json"),
        "all_local_states_independently_checked": len(seen),
        "all_six_query_menu_patterns_independently_checked": len(menu_seen)*64,
        "all_common_weak_zero_states_independently_checked": intersections,
        "current_C_only_single_row_suffices_after_C_subset_O": True,
        "actual_positive_CAP3_CAP4_CAP5": [str(value) for value in cap_C],
        "actual_positive_SAFE4_SAFE5": [str(tau_C[1]), str(tau_C[2])],
        "all513_signed_functional_columns_checked": len(values)*N,
        "functional_values": {name: str(value) for name, value in values.items()},
        "N5_minus_N4_all513_identity_residuals": difference_checks,
        "N5_minus_N4": str(difference_value), "N5_minus_N4_decimal": float(difference_value),
        "structural_positive_lower_bound": str((1-K)/72), "O_outside_C_mass": str(1-K),
        "actual_full_face_identity": "N5-N4=(1-K)/36>0",
        "Main_structural_proof_checked": "The actual positive C budget forces middle covers C, true v4=v5=K/5, and tight positive SAFE4/5 forces N4=N5. The strictly positive N5-N4 contradicts this on the entire face.",
        "additional_direct_contradiction": "The actual full-face K/5-N4 and K/5-N5 constants are each negative; K/5-N3 is positive and is not a contradiction.",
        "optimizer_calls_by_independent_diagnostic_verifier": 0,
        "source_diagnostic_program_imported": False, "half_status": "OPEN",
    }
    write_new(HERE / "true_branch_independent_check.json", result)
    print(json.dumps({key: result[key] for key in ["status", "functional_values", "N5_minus_N4", "N5_minus_N4_decimal",
                                                "O_outside_C_mass", "optimizer_calls_by_independent_diagnostic_verifier"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
