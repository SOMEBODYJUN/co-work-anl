#!/usr/bin/env python3
"""Full complementarity face, never just the returned point support; no optimizer."""
from fractions import Fraction as F
import json
import sys

sys.dont_write_bytecode = True
from contract import HERE, N, M, digest, load_released, read_json, require, write_new


def main():
    bundle = load_released()
    certificate = read_json(HERE / "exact_certificate.json")
    verified = read_json(HERE / "independent_check_result.json")
    require(verified["status"] == "PASS_FULL1586_RAW_FRACTION_VERIFICATION"
            and verified["certificate_sha256"] == digest(HERE / "exact_certificate.json"),
            "Exact certificate must be fully verified before face analysis")
    require(certificate["input_sha256"] == bundle["release"]["input_sha256"],
            "Face input binding mismatch")
    import sympy as sp

    sr = lambda value: sp.Rational(value.numerator, value.denominator)
    fr = lambda value: F(int(value.p), int(value.q))
    z = list(map(F, certificate["primal"]))
    residual = list(map(F, certificate["dual"]["nonnegative_column_residual"]))
    allowed = [j for j, value in enumerate(residual) if value == 0]
    excluded = [j for j, value in enumerate(residual) if value > 0]
    positive = certificate["dual"]["positive_raw_indices"]
    equation_vectors = bundle["E"] + [bundle["A"][i] for i in positive]
    equation_rhs = bundle["h"] + [bundle["b"][i] for i in positive]
    equation_names = [row["name"] for row in bundle["data"]["equalities"]]
    equation_names += [bundle["rows"][i]["name"] for i in positive]
    matrix = sp.Matrix([[sr(row.get(j, F(0))) for j in allowed]
                        for row in equation_vectors])
    rhs = sp.Matrix([sr(value) for value in equation_rhs])
    rref, pivots = matrix.row_join(rhs).rref()
    require(len(allowed) not in pivots, "Inconsistent complementarity equalities")
    free_positions = [j for j in range(len(allowed)) if j not in pivots]
    free_columns = [allowed[j] for j in free_positions]
    count = len(free_positions)
    constants = [F(0)] * len(allowed)
    coefficients = [[F(0)] * count for _ in allowed]
    for k, j in enumerate(free_positions):
        coefficients[j][k] = F(1)
    for i, j in enumerate(pivots):
        constants[j] = fr(rref[i, -1])
        for k, free in enumerate(free_positions):
            coefficients[j][k] = -fr(rref[i, free])
    point_parameters = [z[j] for j in free_columns]
    require(all(
        constants[k] + sum((coefficients[k][t] * point_parameters[t] for t in range(count)), F(0)) == z[j]
        for k, j in enumerate(allowed)), "Returned exact point does not reconstruct on full face")
    require(all(z[j] == 0 for j in excluded), "Positive residual column has positive mass")

    def restrict(vector, subtracted_rhs=F(0)):
        values = [vector.get(j, F(0)) for j in allowed]
        base = sum((value * constant for value, constant in zip(values, constants)), F(0))
        cs = [sum((values[k] * coefficients[k][t] for k in range(len(allowed))), F(0))
              for t in range(count)]
        return base - subtracted_rhs, cs

    def pack(base, cs):
        return {"constant": str(base), "parameter_coefficients": [str(value) for value in cs]}

    def functional(name, vector, subtracted_rhs=F(0)):
        base, cs = restrict(vector, subtracted_rhs)
        result = {"name": name, **pack(base, cs), "fixed": not any(cs)}
        if not any(cs):
            solution = next(iter(sp.linsolve((matrix.T, sp.Matrix(
                [sr(vector.get(j, F(0))) for j in allowed])))))
            free_symbols = set().union(*(value.free_symbols for value in solution))
            weights = [fr(value.subs({symbol: 0 for symbol in free_symbols})) for value in solution]
            require(sum((weight * value for weight, value in zip(weights, equation_rhs)), F(0))
                    - subtracted_rhs == base, "Fixed functional affine constant mismatch")
            zero_column_weights = {}
            for j in range(N):
                remainder = vector.get(j, F(0)) - sum((
                    weight * row.get(j, F(0)) for weight, row in zip(weights, equation_vectors)
                ), F(0))
                require(j in excluded or remainder == 0, "Fixed identity fails an allowed column")
                if remainder:
                    zero_column_weights[str(j)] = str(remainder)
            result.update(
                signed_equation_weights=[str(value) for value in weights],
                signed_forced_zero_column_weights=zero_column_weights,
                subtracted_rhs=str(subtracted_rhs), all513_identity_columns_checked=N,
                identity_scope="Signed face-equality identity, not a universal nonnegative payment.",
            )
        return result

    restrictions = []
    for i, row in enumerate(bundle["rows"]):
        base, cs = restrict(bundle["A"][i], bundle["b"][i])
        value = base + sum((v * p for v, p in zip(cs, point_parameters)), F(0))
        require(value == F(certificate["raw_row_slacks"][i]) and value >= 0,
                "A raw face restriction differs at the exact point")
        restrictions.append({"raw_index": i, "name": row["name"], **pack(base, cs)})
    objective_base, objective_coefficients = restrict(bundle["cost"])
    require(not any(objective_coefficients) and objective_base == F(certificate["objective"]),
            "The characterized face does not have the exact optimum")
    atoms = bundle["data"]["atom_columns"]
    functionals = [functional("objective_W", bundle["cost"]), functional("K", {512: F(1)})]
    for i in range(6):
        u = {atom["index"]: F(atom["a"][i], sum(atom["a"]))
             for atom in atoms if atom["a"][i]}
        functionals.append(functional("u" + str(i + 1), u))
    for label, getbit in [
        ("size_C", lambda atom: atom["c"]), ("size_X", lambda atom: atom["x"]),
        ("C_outside_O_mass", lambda atom: atom["c"] * (1 - atom["o"])),
    ]:
        functionals.append(functional(label, {
            atom["index"]: F(getbit(atom)) for atom in atoms if getbit(atom)
        }))
    gap = {atom["index"]: F(atom["a"][1], sum(atom["a"]))
           for atom in atoms if atom["a"][1]}
    gap[512] = F(-1, 5)
    functionals.append(functional("u2_minus_K_over5_diagnostic_only", gap))
    face = {
        "status": "EXACT_FULL_COMPLEMENTARITY_OPTIMAL_FACE",
        "input_sha256": certificate["input_sha256"],
        "certificate_sha256": digest(HERE / "exact_certificate.json"),
        "optimizer_calls_in_face_analysis": 0,
        "objective": certificate["objective"], "zero_residual_columns": allowed,
        "forced_zero_columns": excluded, "positive_dual_raw_indices": positive,
        "equation_names": equation_names, "equation_rhs": [str(value) for value in equation_rhs],
        "restricted_equation_rank": len(pivots),
        "unconstrained_affine_parameter_count": count,
        "parameters": [{"position": i, "name": "z" + str(j), "column": j}
                       for i, j in enumerate(free_columns)],
        "coordinates": [{"column": j, **pack(constants[k], coefficients[k])}
                        for k, j in enumerate(allowed)],
        "nonnegative_coordinates_required": allowed,
        "all1586_raw_inequality_restrictions": restrictions,
        "point_parameters": [str(value) for value in point_parameters],
        "diagnostic_functionals": functionals,
        "characterization": (
            "Exactly the optimal face after imposing every raw inequality and nonnegative "
            "coordinate on this affine parametrization. It is not the whole unconstrained "
            "affine space and is not restricted to the returned primal support."
        ),
        "true_branch_boundary": (
            "No old equality exclusion or new-source zero-state pattern is presumed. "
            "True-SPE deductions require the actually positive raw payment and its own "
            "fully checked source proof; all weak zero states must remain."
        ),
    }
    write_new(HERE / "optimal_face.json", face)
    write_new(HERE / "positive_payment_diagnostic_queue.json", {
        "status": "EXACT_CERT_ESTABLISHED_SOURCE_DIAGNOSTICS_REQUIRED",
        "input_sha256": certificate["input_sha256"],
        "certificate_sha256": digest(HERE / "exact_certificate.json"),
        "face_sha256": digest(HERE / "optimal_face.json"),
        "positive_raw_rows": certificate["dual"]["positive_raw_rows"],
        "known_candidates_to_inspect_if_applicable": [
            "true-C ROOT270 remainder", "original P25 equality",
            "NS5 equality including the0010 weak state",
            "Each actually positive new536 row at its own exact source weights",
        ],
        "new_rows_have_numerical_divisor25_not_a_uniform_source_weight": True,
        "phaseI_or_fixedC_binding_authorized": False,
        "no_new_inequality_added_to_input": True,
        "optimizer_calls": 0,
    })
    print(json.dumps({
        "status": face["status"], "zero_residual_columns": allowed,
        "equation_rank": len(pivots), "free_columns": free_columns,
        "all_raw_restrictions": M, "optimizer_calls": 0,
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
