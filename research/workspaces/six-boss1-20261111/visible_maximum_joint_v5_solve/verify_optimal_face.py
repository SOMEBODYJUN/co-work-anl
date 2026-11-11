#!/usr/bin/env python3
"""Independent Fraction RREF and complete parameter-inequality verification; no optimizer."""
from fractions import Fraction as F
import json
import sys

sys.dont_write_bytecode = True
from contract import HERE, N, M, Q, FACE_CHECK_STATUS, digest, load_verified_certificate, read_json, require, write_new


def sparse(value):
    return {int(j): F(coefficient) for j, coefficient in value.items()}


def rref(matrix, coefficient_columns):
    a = [list(row) for row in matrix]
    pivot_columns, row_index = [], 0
    for column in range(coefficient_columns):
        pivot = next((i for i in range(row_index, len(a)) if a[i][column]), None)
        if pivot is None:
            continue
        a[row_index], a[pivot] = a[pivot], a[row_index]
        scale = a[row_index][column]
        a[row_index] = [value / scale for value in a[row_index]]
        for i in range(len(a)):
            if i != row_index and a[i][column]:
                scale = a[i][column]
                a[i] = [x - scale * y for x, y in zip(a[i], a[row_index])]
        pivot_columns.append(column)
        row_index += 1
        if row_index == len(a):
            break
    require(all(any(row[:coefficient_columns]) or row[-1] == 0 for row in a), "Inconsistent affine equations")
    return a, pivot_columns


def main():
    bundle, certificate, checked = load_verified_certificate()
    face = read_json(HERE / "optimal_face.json")
    require(face["status"] == "EXACT_FULL_COMPLEMENTARITY_OPTIMAL_FACE"
            and face["input_sha256"] == certificate["input_sha256"]
            and face["certificate_sha256"] == digest(HERE / "exact_certificate.json"), "Face binding differs")
    require((face["raw_inequality_count"], face["nonnegative_column_count"], face["equality_count"])
            == (M, N, Q), "Incomplete face domain")
    data = bundle["data"]
    A = [sparse(row["a"]) for row in data["raw_rows"]]
    b = [F(row["rhs"]) for row in data["raw_rows"]]
    E = [sparse(row["a"]) for row in data["equalities"]]
    h = [F(row["rhs"]) for row in data["equalities"]]
    cost = sparse(data["objective"])
    z = list(map(F, certificate["primal"]))
    y = list(map(F, certificate["dual"]["raw_row_weights"]))
    residual = list(map(F, checked["all_column_residuals"]))
    allowed = [j for j in range(N) if residual[j] == 0]
    excluded = [j for j in range(N) if residual[j] > 0]
    positive = [i for i in range(M) if y[i] > 0]
    require(face["zero_residual_columns"] == allowed and face["forced_zero_columns"] == excluded
            and face["positive_dual_raw_indices"] == positive, "Face omitted a zero column or changed actual positive rows")
    eq = E + [A[i] for i in positive]
    rhs = h + [b[i] for i in positive]
    names = [row["name"] for row in data["equalities"]] + [data["raw_rows"][i]["name"] for i in positive]
    require(face["equation_names"] == names and list(map(F, face["equation_rhs"])) == rhs, "Face equality catalogue differs")
    reduced, pivots = rref([[row.get(j, F(0)) for j in allowed] + [value]
                            for row, value in zip(eq, rhs)], len(allowed))
    free = [j for j in range(len(allowed)) if j not in pivots]
    free_columns = [allowed[j] for j in free]
    count = len(free)
    require(face["restricted_equation_rank"] == len(pivots)
            and face["unconstrained_affine_parameter_count"] == count, "Face rank or parameter count differs")
    require(face["parameters"] == [{"position": k, "name": "z" + str(j), "column": j}
                                   for k, j in enumerate(free_columns)], "Free coordinates changed")
    constants, coefficients = [F(0)] * len(allowed), [[F(0)] * count for _ in allowed]
    for k, j in enumerate(free):
        coefficients[j][k] = F(1)
    for i, j in enumerate(pivots):
        constants[j] = reduced[i][-1]
        for k, position in enumerate(free):
            coefficients[j][k] = -reduced[i][position]

    def pack(constant, coeff):
        return {"constant": str(constant), "parameter_coefficients": [str(value) for value in coeff]}

    def restrict(vector, rhs_value=F(0)):
        constant = sum((vector.get(j, F(0)) * constants[k] for k, j in enumerate(allowed)), F(0)) - rhs_value
        coeff = [sum((vector.get(j, F(0)) * coefficients[k][t] for k, j in enumerate(allowed)), F(0))
                 for t in range(count)]
        return constant, coeff

    expected_coords = [{"column": j, **pack(constants[k], coefficients[k])} for k, j in enumerate(allowed)]
    require(face["coordinates"] == expected_coords, "Face parameterization is not the full exact RREF solution")
    point_parameters = [z[j] for j in free_columns]
    require(list(map(F, face["point_parameters"])) == point_parameters, "Representative parameter values differ")
    for k, j in enumerate(allowed):
        require(constants[k] + sum((coefficient * value for coefficient, value in zip(coefficients[k], point_parameters)), F(0))
                == z[j], "Exact representative does not reconstruct")
    require(all(z[j] == 0 for j in excluded), "Forced-zero column carries mass")
    for row, value in zip(eq, rhs):
        constant, coeff = restrict(row, value)
        require(constant == 0 and not any(coeff), "An affine equality fails identically on the face")
    raw_conditions = face["all_raw_inequality_restrictions"]
    require(len(raw_conditions) == M, "All original raw inequalities are mandatory")
    for i in range(M):
        constant, coeff = restrict(A[i], b[i])
        expected = {"raw_index": i, "name": data["raw_rows"][i]["name"],
                    "family": data["raw_rows"][i]["family"], "original_rhs": str(b[i]), **pack(constant, coeff)}
        require(raw_conditions[i] == expected, "Raw parameter inequality differs at " + str(i))
        require(constant + sum((a * value for a, value in zip(coeff, point_parameters)), F(0))
                == F(checked["all_raw_row_slacks"][i]), "Raw inequality disagrees at the representative")
    coords_by_column = {entry["column"]: {k: v for k, v in entry.items() if k != "column"} for entry in expected_coords}
    all_nonnegative = [{"column": j, "forced_zero": j in excluded,
                        **coords_by_column.get(j, pack(F(0), [F(0)] * count))} for j in range(N)]
    require(face["all513_nonnegative_coordinate_restrictions"] == all_nonnegative
            and face["nonnegative_coordinates_required"] == allowed, "Full nonnegativity domain differs")
    objective_constant, objective_coeff = restrict(cost)
    require(not any(objective_coeff) and objective_constant == F(certificate["objective"])
            == F(face["objective"]), "The complete face objective is not constant at the exact optimum")
    atoms = data["atom_columns"]
    expected_functions = [("objective_W", cost), ("K", {512: F(1)})]
    for i in range(6):
        expected_functions.append(("u" + str(i + 1), {
            atom["index"]: F(atom["a"][i], sum(atom["a"])) for atom in atoms if atom["a"][i]
        }))
    for name, bit in [("size_C", lambda atom: atom["c"]), ("size_X", lambda atom: atom["x"]),
                      ("C_outside_O_mass", lambda atom: atom["c"] * (1 - atom["o"]))]:
        expected_functions.append((name, {atom["index"]: F(bit(atom)) for atom in atoms if bit(atom)}))
    functionals = face["diagnostic_functionals"]
    require(len(functionals) == len(expected_functions), "Unexpected inherited or missing diagnostic functional")
    fixed_count = 0
    for item, (name, expected_vector) in zip(functionals, expected_functions):
        vector = sparse(item["full_coefficients"])
        subtracted = F(item["subtracted_rhs"])
        require(item["name"] == name and vector == expected_vector and subtracted == 0, "Basic diagnostic functional differs")
        constant, coeff = restrict(vector, subtracted)
        require(item["constant"] == str(constant) and item["parameter_coefficients"] == [str(v) for v in coeff]
                and item["fixed"] is (not any(coeff)), "Diagnostic affine restriction differs")
        if not any(coeff):
            fixed_count += 1
            weights = list(map(F, item["signed_equation_weights"]))
            forced_weights = sparse(item["signed_forced_zero_column_weights"])
            require(len(weights) == len(eq) and set(forced_weights).issubset(excluded), "Invalid signed face identity domain")
            for j in range(N):
                require(vector.get(j, F(0)) == sum((weight * row.get(j, F(0)) for weight, row in zip(weights, eq)), F(0))
                        + forced_weights.get(j, F(0)), "Signed face identity fails a full column")
            require(sum((weight * value for weight, value in zip(weights, rhs)), F(0)) - subtracted == constant,
                    "Signed face identity affine RHS differs")
    result = {
        "status": FACE_CHECK_STATUS, "input_sha256": certificate["input_sha256"],
        "certificate_sha256": digest(HERE / "exact_certificate.json"),
        "independent_certificate_check_sha256": digest(HERE / "independent_check_result.json"),
        "face_sha256": digest(HERE / "optimal_face.json"), "all_zero_residual_columns": allowed,
        "all_forced_zero_columns": excluded, "actual_positive_raw_indices": positive,
        "exact_restricted_rank": len(pivots), "unconstrained_affine_parameter_count": count,
        "all_raw_parameter_inequalities_checked": M, "all_nonnegative_coordinate_conditions_checked": N,
        "all_original_equalities_checked": Q, "fixed_functional_full_column_identities_checked": fixed_count,
        "objective": str(objective_constant), "optimizer_calls_by_face_verifier": 0,
        "face_or_recovery_program_imported": False,
        "scope": "Exact full optimal face with every raw inequality and all nonnegativity conditions. Affine parameter count does not assert relative feasible dimension or SPE attainability.",
    }
    write_new(HERE / "optimal_face_check_result.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
