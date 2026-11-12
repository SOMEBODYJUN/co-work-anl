#!/usr/bin/env python3
"""Fresh v5 positive-source equality audit; exact algebra only, no optimizer.

Written after the sole solve. Source-specific indices below are this run's actual
positive rows, not inherited from v4. Every weak local state remains in output.
"""
from fractions import Fraction as F
from itertools import product
import json
import sys

sys.dont_write_bytecode = True
from contract import (HERE, REPO, N, M, Q, FACE_CHECK_STATUS, digest, relative,
                      load_verified_certificate, read_json, require, write_new)

CURRENT_NEW_POSITIVE = [1803, 2563, 2564, 2606]
C_ONLY, C_GENERAL = 1803, 2606


def solve_signed(matrix, target, variables):
    a = [list(row) + [value] for row, value in zip(matrix, target)]
    pivots, row_index = [], 0
    for column in range(variables):
        pivot = next((i for i in range(row_index, len(a)) if a[i][column]), None)
        if pivot is None:
            continue
        a[row_index], a[pivot] = a[pivot], a[row_index]
        divisor = a[row_index][column]
        a[row_index] = [value / divisor for value in a[row_index]]
        for i in range(len(a)):
            if i != row_index and a[i][column]:
                multiplier = a[i][column]
                a[i] = [x - multiplier * y for x, y in zip(a[i], a[row_index])]
        pivots.append(column)
        row_index += 1
        if row_index == len(a):
            break
    require(all(any(row[:variables]) or row[-1] == 0 for row in a), "No signed row-space identity")
    weights = [F(0)] * variables
    for i, column in enumerate(pivots):
        weights[column] = a[i][-1]
    return weights


def main():
    bundle, cert, checked = load_verified_certificate()
    require(cert["input_sha256"] == "12f456dfbc789a5c1826d248e4851b84f66b428554d181b7ba12cbfdb920f3ac",
            "This diagnostic is bound to the actual released v5 solve")
    face = read_json(HERE / "optimal_face.json")
    face_check = read_json(HERE / "optimal_face_check_result.json")
    require(face_check["status"] == FACE_CHECK_STATUS
            and face_check["face_sha256"] == digest(HERE / "optimal_face.json")
            and face_check["certificate_sha256"] == digest(HERE / "exact_certificate.json"),
            "Entire optimal face must be independently verified first")
    positive = cert["dual"]["positive_raw_indices"]
    require([i for i in positive if i >= 1586] == CURRENT_NEW_POSITIVE, "Actual new positive payments changed")
    source_pins = {}
    for filename in ["all_source_minimal_cap_safe/proof.md", "source2_minimal_cap_safe/proof.md"]:
        path = HERE.parent / filename
        name = relative(path)
        require(name in bundle["pins"] and digest(path) == bundle["pins"][name], "Unreleased current source proof")
        source_pins[name] = bundle["pins"][name]
    rows, atoms = bundle["rows"], bundle["data"]["atom_columns"]
    all_states, minima, menu_checks, row_checks, parameters, zero_sets = [], [], [], [], {}, {}
    menu_patterns = list(product([0, 1], repeat=6))

    for index in CURRENT_NEW_POSITIVE:
        metadata = rows[index]
        require(metadata["source"] == 2, "Unexpected actual source")
        if index == C_ONLY:
            tau = {j: F(value) for j, value in zip([3, 4, 5], metadata["tau3_tau4_tau5"])}
            target_name = "C"
        else:
            tau = {int(j): F(value) for j, value in metadata["tau_by_true_source"].items()}
            target_name = metadata["forced_target"]
        s = F(metadata["s"])
        a = F(25) + sum(tau.values(), F(0)) - s
        beta = {j: F(1, 12) + tau[j] + sum((tau[k] / (6 * (7-k) * (8-k)) for k in range(j+1, 6)), F(0))
                for j in [3, 4, 5]}
        S = F(1) + sum(beta.values(), F(0))
        require(a == F(metadata["source_IC_weight"]) and a > 0 and all(value > 0 for value in beta.values()),
                "Actual source or CAP positivity differs")
        stored_caps = metadata["middle_CAP_weights"]
        stored_caps = {j: F(v) for j, v in zip([3, 4, 5], stored_caps)} if isinstance(stored_caps, list) else {
            int(j): F(v) for j, v in stored_caps.items()}
        require(beta == stored_caps and metadata["terminal_CAP_weight"] == metadata["terminal_BR_average_weight"] == "1",
                "Actual positive-source budget weights differ")
        parameters[index] = {"tau": tau, "s": s, "a": a, "beta": beta, "S": S, "target": target_name}

        def cost(p, t, membership, tail):
            load = p + t + sum(tail)
            numerator = a*t - tail[3] - sum((tau[j]*tail[j-3] for j in [3, 4, 5]), F(0))
            require(load != 0 or numerator == 0, "Zero-load numerator differs")
            value = numerator / load if load else F(0)
            value += sum((beta[j]*tail[j-3] for j in [3, 4, 5]), F(0)) + tail[3]
            value += F(membership, 6*(p+t+sum(tail[:3])+1))
            value += sum((tau[j]*F(membership, 6*(p+t+sum(tail[:j-3])+7-j)) for j in [3, 4, 5]), F(0))
            return value

        def minimum(p, t, o):
            return (S*t + F(24*t, p+5) - s*F(t, 5) + F(o, 6*(p+4*t+1))
                    + sum((tau[j]*F(o, 6*(p+(j-2)*t+7-j)) for j in [3, 4, 5]), F(0)))

        zero_sets[index] = {}
        for p, t, o in product([0, 1], repeat=3):
            lower = minimum(p, t, o)
            values, zeros = [], []
            for tail in product([0, 1], repeat=4):
                actual = cost(p, t, o, tail)
                excess = actual - lower
                require(excess >= 0, "Actual source has negative local remainder")
                values.append(actual)
                if excess == 0:
                    zeros.append(tail)
                load = p+t+sum(tail)
                all_states.append({"raw_index": index, "p": p, "t": t, "o": o, "tail": list(tail),
                                   "load": load, "cost": str(actual), "minimum": str(lower), "remainder": str(excess)})
            require(min(values) == lower, "Frozen local minimum is not attained")
            zero_sets[index][(p, t, o)] = set(zeros)
            minima.append({"raw_index": index, "p": p, "t": t, "o": o,
                           "minimum": str(lower), "all_weak_minimizing_tails": [list(tail) for tail in zeros]})

        for p, t in product([0, 1], repeat=2):
            for tail in product([0, 1], repeat=4):
                kernel = F(1, 6*(p+t+sum(tail[:3])+1))
                kernel += sum((tau[j]*F(1, 6*(p+t+sum(tail[:j-3])+7-j)) for j in [3, 4, 5]), F(0))
                require(kernel > 0, "Terminal mean must keep the true menu gap kernel strictly positive")
                gaps = []
                for menu in menu_patterns:
                    d, o = sum(menu), int(any(menu))
                    direct_query = sum((F(bit, 6*(p+t+sum(tail[:3])+1)) for bit in menu), F(0))
                    direct_query += sum((tau[j] * sum((F(bit, 6*(p+t+sum(tail[:j-3])+7-j))
                                                       for bit in menu), F(0)) for j in [3, 4, 5]), F(0))
                    union_query = o*kernel
                    gap = direct_query-union_query
                    require(gap == (d-o)*kernel and gap >= 0 and (gap == 0) == (d == o),
                            "True six-menu weakening identity or weak equality states differ")
                    require(cost(p, t, d, tail)-cost(p, t, o, tail) == gap, "True and union costs differ")
                    gaps.append(str(gap))
                menu_checks.append({"raw_index": index, "p": p, "t": t, "tail": list(tail),
                                    "strictly_positive_kernel": str(kernel), "all64_menu_gaps": gaps})

        expected_row = {}
        for atom in atoms:
            j, actual_bits = atom["index"], atom["a"]
            p, o = actual_bits[0], atom["o"]
            t = atom["c"] if target_name == "C" else actual_bits[int(target_name[1:])-1]
            u2 = F(actual_bits[1], sum(actual_bits)) if actual_bits[1] else F(0)
            coefficient = a*u2-minimum(p, t, o)
            if index == C_ONLY:
                coefficient += (S-s/5)*t
            expected_row[j] = coefficient
        expected_row[512] = s/5 if index == C_ONLY else S
        checks = [expected_row[j]-bundle["A"][index].get(j, F(0)) for j in range(N)]
        require(not any(checks) and bundle["b"][index] == 0, "Actual full row does not match its own source formula")
        row_checks.append({"raw_index": index, "name": metadata["name"], "true_source_IC_weight": str(a),
                           "original_raw_payment": cert["dual"]["raw_row_weights"][index],
                           "all513_coefficient_residuals": [str(value) for value in checks],
                           "numerical_divisor": str(bundle["divisors"][index])})

    left, right = parameters[C_ONLY], parameters[C_GENERAL]
    require(left["tau"] == right["tau"] and right["s"] == 0 and left["s"] > 0, "Current C pair has different branch parameters")
    E_C = bundle["E"][1]
    u2 = {atom["index"]: F(atom["a"][1], sum(atom["a"])) for atom in atoms if atom["a"][1]}
    pair_residuals = []
    for j in range(N):
        actual = bundle["A"][C_ONLY].get(j, F(0))-bundle["A"][C_GENERAL].get(j, F(0))
        expected = left["s"]*(F(1, 5) if j == 512 else -u2.get(j, F(0))) + left["S"]*E_C.get(j, F(0))
        pair_residuals.append(actual-expected)
    require(not any(pair_residuals), "Fresh two-row C identity fails")
    intersections = []
    for p, c, o in product([0, 1], repeat=3):
        tails = sorted(zero_sets[C_ONLY][(p, c, o)] & zero_sets[C_GENERAL][(p, c, o)])
        intersections.append({"p": p, "c": c, "o": o, "all_common_weak_zero_tails": [list(tail) for tail in tails]})
        if c:
            require(tails and all(tail[0] == 1 and p+c+sum(tail) == 5 for tail in tails),
                    "Current C equality states do not force R3 coverage and total load five")
            if o:
                require(tails == [(1, 1, 1, 1-p)], "C intersect O has an unexpected middle-tail zero state")

    allowed, excluded = face["zero_residual_columns"], face["forced_zero_columns"]
    coords = face["coordinates"]
    count = face["unconstrained_affine_parameter_count"]
    require([item["column"] for item in coords] == allowed, "Face coordinate routing differs")
    eqs = bundle["E"] + [bundle["A"][i] for i in positive]
    rhs = bundle["h"] + [bundle["b"][i] for i in positive]
    z = list(map(F, cert["primal"]))
    constants = [F(item["constant"]) for item in coords]
    coefficients = [[F(value) for value in item["parameter_coefficients"]] for item in coords]

    def functional(name, vector):
        base = sum((vector.get(j, F(0))*constants[k] for k, j in enumerate(allowed)), F(0))
        cs = [sum((vector.get(j, F(0))*coefficients[k][t] for k, j in enumerate(allowed)), F(0))
              for t in range(count)]
        record = {"name": name, "full_coefficients": {str(j): str(value) for j, value in vector.items()},
                  "constant": str(base), "parameter_coefficients": [str(value) for value in cs],
                  "fixed": not any(cs), "value_at_representative": str(sum((value*z[j] for j, value in vector.items()), F(0)))}
        if not any(cs):
            weights = solve_signed([[row.get(j, F(0)) for row in eqs] for j in allowed],
                                   [vector.get(j, F(0)) for j in allowed], len(eqs))
            forced = {j: vector.get(j, F(0))-sum((weight*row.get(j, F(0)) for weight, row in zip(weights, eqs)), F(0))
                      for j in range(N)}
            require(all(value == 0 for j, value in forced.items() if j not in excluded), "Signed face identity fails on an allowed column")
            require(sum((weight*value for weight, value in zip(weights, rhs)), F(0)) == base, "Signed face identity has wrong affine constant")
            record.update(signed_face_equation_weights=[str(value) for value in weights],
                          signed_forced_zero_column_weights={str(j): str(value) for j, value in forced.items() if value},
                          all513_identity_coefficients_checked=N, decimal=float(base))
        return record

    c_outside = {atom["index"]: F(atom["c"]*(1-atom["o"])) for atom in atoms if atom["c"]*(1-atom["o"])}
    u2_gap = dict(u2)
    u2_gap[512] = F(-1, 5)
    functionals = [functional("C_outside_O_mass", c_outside), functional("u2_minus_K_over5_from_new_C_pair", u2_gap),
                   functional("K", {512: F(1)})]
    for internal in [3, 4, 5]:
        vector = {atom["index"]: -F(atom["o"], 6*(atom["a"][0]+(internal-2)*atom["c"]+7-internal))
                  for atom in atoms if atom["o"]}
        vector[512] = F(1, 5)
        functionals.append(functional("K_over5_minus_N" + str(internal), vector))
    by_name = {item["name"]: item for item in functionals}
    require(by_name["C_outside_O_mass"]["fixed"] and F(by_name["C_outside_O_mass"]["constant"]) == 0,
            "Complete current face does not force C contained in O")
    require(by_name["u2_minus_K_over5_from_new_C_pair"]["fixed"]
            and F(by_name["u2_minus_K_over5_from_new_C_pair"]["constant"]) == 0, "New C-pair equality identity failed on the full face")
    violated = [name for name in ["K_over5_minus_N3", "K_over5_minus_N4", "K_over5_minus_N5"]
                if by_name[name]["fixed"] and F(by_name[name]["constant"]) < 0]
    require(violated, "These fresh branch conditions do not exclude the whole face; report remaining obstruction")
    source_metadata = [{"raw_index": index, "parameters": {
        "tau": {str(j): str(value) for j, value in parameters[index]["tau"].items()},
        "s": str(parameters[index]["s"]), "source_IC_weight": str(parameters[index]["a"]),
        "middle_CAP_weights": {str(j): str(value) for j, value in parameters[index]["beta"].items()},
        "true_K_budget": str(parameters[index]["S"]), "forced_target": parameters[index]["target"],
    }} for index in CURRENT_NEW_POSITIVE]
    state_output = {"status": "PASS_ALL_CURRENT_POSITIVE_SOURCE_WEAK_STATES_AND_FULL_COLUMNS",
                    "input_sha256": cert["input_sha256"], "parameters": source_metadata,
                    "all512_local_state_checks": all_states, "all32_minimum_tables": minima,
                    "all64_six_query_patterns": [list(menu) for menu in menu_patterns],
                    "all256_menu_contexts": menu_checks, "all_four_full513_row_checks": row_checks}
    write_new(HERE / "current_positive_source_state_checks.json", state_output)
    write_new(HERE / "true_branch_face_functionals.json", {
        "status": "PASS_FRESH_FULL_FACE_SIGNED_IDENTITIES", "input_sha256": cert["input_sha256"],
        "face_sha256": digest(HERE / "optimal_face.json"), "equation_names": face["equation_names"],
        "functionals": functionals, "optimizer_calls": 0,
    })
    result = {
        "status": "PASS_FRESH_TRUE_SOURCE_EXCLUSION_OF_ENTIRE_V5_OPTIMAL_FACE",
        "input_sha256": cert["input_sha256"], "certificate_sha256": digest(HERE / "exact_certificate.json"),
        "face_sha256": digest(HERE / "optimal_face.json"), "face_check_sha256": digest(HERE / "optimal_face_check_result.json"),
        "source_proof_pins": source_pins, "actual_positive_new_indices": CURRENT_NEW_POSITIVE,
        "new_C_pair": [C_ONLY, C_GENERAL], "C_pair_identity": "A1803-A2606 = s*(K/5-u2) + S*(|C|-K)",
        "C_pair_all513_coefficient_residuals": [str(value) for value in pair_residuals],
        "all_common_C_branch_weak_zero_states": intersections,
        "local_state_checks": len(all_states), "true_six_menu_pattern_checks": len(menu_checks)*len(menu_patterns),
        "full_raw_coefficient_checks": len(row_checks)*N,
        "source_state_artifact_sha256": digest(HERE / "current_positive_source_state_checks.json"),
        "face_functionals_sha256": digest(HERE / "true_branch_face_functionals.json"),
        "logical_chain": [
            "Both actual positive C budgets are tight on every optimum; use this run's exact C-pair identity and each source's own nonnegative decomposition.",
            "Exhaustive common weak zero states force R3 to contain C and C loads to equal five; o=0 alternatives are retained.",
            "Every current zero-residual C column has o=1, so C outside O has zero mass on the entire face.",
            "For c=o=1, common weak states are exactly 1111 at p=0 and 1110 at p=1; hence R3,R4,R5 all contain C.",
            "All three current CAP weights are strictly positive. Equality of their size caps and |C|=K force each middle tail coverage to equal C, including no outside-C mass.",
            "Each C customer has load five. Thus true branch v3=v4=v5=K/5; these are new branch deductions, not imported actual-utility assumptions.",
            "The genuine internal SAFE at j=4 has exact visible lower bound N4 after R3=C; similarly j=3 and j=5 have their own bounds.",
            "A full-face signed identity makes a required K/5-Nj strictly negative, contradicting genuine weak optimality. The entire optimum face is unattainable by complete pure SPE.",
        ],
        "fixed_violated_internal_SAFE_functionals": violated,
        "functional_summary": [{key: item[key] for key in ["name", "constant", "parameter_coefficients", "fixed"]} for item in functionals],
        "old_zero_state_or_utility_relation_imported": False,
        "new_LP_rows_added": 0, "optimizer_calls_in_diagnostics": 0,
        "scope": "Exact necessary-system optimum and exclusion of its entire optimum face. No uniform positive improvement epsilon, half proof, or SPE construction is claimed; half remains OPEN.",
    }
    write_new(HERE / "true_branch_equality_diagnostic.json", result)
    print(json.dumps({key: result[key] for key in ["status", "all_common_C_branch_weak_zero_states", "functional_summary",
                                                "fixed_violated_internal_SAFE_functionals", "optimizer_calls_in_diagnostics"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
