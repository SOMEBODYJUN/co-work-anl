#!/usr/bin/env python3
"""Standard-library Fraction verifier, independent of recovery and face code."""
from fractions import Fraction as F
import json
import sys

sys.dont_write_bytecode = True
from contract import HERE, N, M, Q, digest, load_released, read_json, require, write_new


def vector(value, length, label):
    require(isinstance(value, list) and len(value) == length, label + " dimension mismatch")
    require(all(isinstance(item, str) for item in value), label + " must be exact strings")
    return [F(item) for item in value]


def main():
    bundle = load_released()
    certificate = read_json(HERE / "exact_certificate.json")
    require(certificate["input_sha256"] == bundle["release"]["input_sha256"],
            "Certificate does not match the released input")
    require(certificate["optimizer_calls"] == 1, "Unexpected discovery call count")
    require((certificate["variables"], certificate["raw_inequalities"], certificate["equality_count"])
            == (N, M, Q), "Certificate full-domain dimensions changed")
    require(certificate["discovery_sha256"] == digest(HERE / "discovery_output.json"),
            "Actual discovery output changed")
    require(read_json(HERE / "source_pins_at_solve.json") == bundle["pins"],
            "Frozen source map changed since the solve")
    z = vector(certificate["primal"], N, "primal")
    y = vector(certificate["dual"]["raw_row_weights"], M, "raw weights")
    eta = vector(certificate["dual"]["equality_multipliers"], Q, "free equality weights")
    require(all(value >= 0 for value in z) and all(value >= 0 for value in y),
            "Negative primal or raw inequality payment")
    dot = lambda row: sum((value * z[j] for j, value in row.items()), F(0))
    slack = [dot(row) - rhs for row, rhs in zip(bundle["A"], bundle["b"])]
    eqres = [dot(row) - rhs for row, rhs in zip(bundle["E"], bundle["h"])]
    require(all(value >= 0 for value in slack), "A raw inequality is violated")
    require(eqres == [F(0)] * Q, "An equality is violated")
    residual = [bundle["cost"].get(j, F(0)) for j in range(N)]
    for i in range(M):
        for j, coefficient in bundle["A"][i].items():
            residual[j] -= y[i] * coefficient
    for k in range(Q):
        for j, coefficient in bundle["E"][k].items():
            residual[j] -= eta[k] * coefficient
    require(all(value >= 0 for value in residual), "A full-column dual residual is negative")
    require(slack == vector(certificate["raw_row_slacks"], M, "stored raw slacks"),
            "Stored row slack differs")
    require(eqres == vector(certificate["equality_residuals"], Q, "stored equality residual"),
            "Stored equality residual differs")
    require(residual == vector(certificate["dual"]["nonnegative_column_residual"], N,
                               "stored column residual"), "Stored column residual differs")
    primal_objective = dot(bundle["cost"])
    row_rhs = sum((weight * rhs for weight, rhs in zip(y, bundle["b"])), F(0))
    eq_rhs = sum((weight * rhs for weight, rhs in zip(eta, bundle["h"])), F(0))
    dual_objective = row_rhs + eq_rhs
    require(primal_objective == dual_objective == F(certificate["objective"])
            == F(certificate["dual"]["objective"]), "Nonzero exact duality gap")
    require(row_rhs == F(certificate["dual"]["affine_inequality_rhs_payment"])
            and eq_rhs == F(certificate["dual"]["equality_rhs_payment"]),
            "Affine RHS accounting mismatch")
    row_products = [weight * value for weight, value in zip(y, slack)]
    column_products = [value * mass for value, mass in zip(residual, z)]
    require(all(value == 0 for value in row_products + column_products),
            "Exact complementarity fails")
    # Global coefficient identity, including every affine raw RHS and both free equalities.
    identity_rhs = sum(row_products, F(0)) + sum(column_products, F(0))
    identity_rhs += sum((weight * value for weight, value in zip(eta, eqres)), F(0))
    require(primal_objective - dual_objective == identity_rhs, "Full affine identity fails")
    require(certificate["dual"]["positive_raw_indices"] == [i for i, weight in enumerate(y) if weight > 0],
            "Positive payment catalogue differs from exact weights")
    result = {
        "status": "PASS_FULL1586_RAW_FRACTION_VERIFICATION",
        "input_sha256": bundle["release"]["input_sha256"],
        "certificate_sha256": digest(HERE / "exact_certificate.json"),
        "discovery_sha256": digest(HERE / "discovery_output.json"),
        "source_pins_verified": len(bundle["pins"]),
        "all_raw_inequalities_checked": M, "all_nonnegative_columns_checked": N,
        "free_equality_multipliers_checked": Q, "objective": str(primal_objective),
        "affine_raw_rhs_payment": str(row_rhs), "equality_rhs_payment": str(eq_rhs),
        "duality_gap": "0", "all_complementarity_products_zero": True,
        "minimum_primal": str(min(z)), "minimum_raw_slack": str(min(slack)),
        "minimum_raw_weight": str(min(y)), "minimum_column_residual": str(min(residual)),
        "all_raw_row_slacks": [str(value) for value in slack],
        "all_column_residuals": [str(value) for value in residual],
        "equality_residuals": [str(value) for value in eqres],
        "optimizer_calls_by_verifier": 0,
        "old_solver_or_recovery_imported": False,
        "scope": "Necessary-cone exact optimality only; no full ordered SPE realization.",
    }
    write_new(HERE / "independent_check_result.json", result)
    print(json.dumps({key: result[key] for key in [
        "status", "objective", "all_raw_inequalities_checked",
        "all_nonnegative_columns_checked", "free_equality_multipliers_checked",
        "optimizer_calls_by_verifier",
    ]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
