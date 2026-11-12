#!/usr/bin/env python3
"""Independent standard-library Fraction recomputation of every original constraint."""
from fractions import Fraction as F
import json
import sys

sys.dont_write_bytecode = True
from contract import (HERE, N, M, Q, CERT_STATUS, CHECK_STATUS, canonical_digest,
                      digest, load_discovery, read_json, require, write_new)


def vector(value, length, label):
    require(isinstance(value, list) and len(value) == length, label + " dimension mismatch")
    require(all(isinstance(item, str) for item in value), label + " requires exact strings")
    return [F(item) for item in value]


def own_sparse(value, label):
    require(isinstance(value, dict), label + " requires sparse JSON")
    result = {}
    for key, item in value.items():
        j = int(key)
        require(str(j) == key and 0 <= j < N and isinstance(item, str), label + " invalid exact coefficient")
        result[j] = F(item)
    return result


def main():
    bundle, discovery = load_discovery()
    data = bundle["data"]
    certificate = read_json(HERE / "exact_certificate.json")
    require(certificate["status"] == CERT_STATUS and certificate["input_sha256"] == bundle["release"]["input_sha256"],
            "Certificate does not match the released input")
    require(certificate["optimizer_calls"] == 1 and certificate["optimizer_calls_in_recovery"] == 0,
            "Unexpected optimization count")
    require((certificate["variables"], certificate["raw_inequalities"], certificate["equality_count"])
            == (N, M, Q), "Certificate full-domain dimensions changed")
    require(certificate["discovery_sha256"] == digest(HERE / "discovery_output.json"), "Actual sole discovery changed")
    require(certificate["row_catalog_sha256"] == bundle["release"]["row_catalog_sha256"]
            and certificate["source_pins_at_solve_sha256"] == digest(HERE / "source_pins_at_solve.json")
            and certificate["consumption_marker_sha256"] == digest(HERE / "single_lp_consumed.json"),
            "Exact certificate lost actual metadata, source-pins or one-call lineage")
    # Reparse exact coefficient strings independently; no recovery vectors or residuals are trusted.
    A = [own_sparse(row["a"], "raw " + str(i)) for i, row in enumerate(data["raw_rows"])]
    b = [F(row["rhs"]) for row in data["raw_rows"]]
    E = [own_sparse(row["a"], "equality " + str(k)) for k, row in enumerate(data["equalities"])]
    h = [F(row["rhs"]) for row in data["equalities"]]
    cost = own_sparse(data["objective"], "objective")
    z = vector(certificate["primal"], N, "primal")
    y = vector(certificate["dual"]["raw_row_weights"], M, "raw weights")
    eta = vector(certificate["dual"]["equality_multipliers"], Q, "free equality weights")
    # eta is deliberately signed and unrestricted, including the C-size equality multiplier.
    require(all(value >= 0 for value in z) and all(value >= 0 for value in y), "Negative primal or inequality multiplier")
    dot = lambda row: sum((coefficient * z[j] for j, coefficient in row.items()), F(0))
    slack = [dot(row) - rhs for row, rhs in zip(A, b)]
    eqres = [dot(row) - rhs for row, rhs in zip(E, h)]
    require(all(value >= 0 for value in slack), "A raw inequality fails")
    require(eqres == [F(0)] * Q, "An original affine equality fails")
    residual = [cost.get(j, F(0)) for j in range(N)]
    for i in range(M):
        for j, coefficient in A[i].items():
            residual[j] -= y[i] * coefficient
    for k in range(Q):
        for j, coefficient in E[k].items():
            residual[j] -= eta[k] * coefficient
    require(all(value >= 0 for value in residual), "A full-column dual residual is negative")
    require(slack == vector(certificate["raw_row_slacks"], M, "stored raw slacks"), "Stored slack mismatch")
    require(eqres == vector(certificate["equality_residuals"], Q, "stored equality residuals"), "Stored equality mismatch")
    require(residual == vector(certificate["dual"]["nonnegative_column_residual"], N, "stored dual residuals"),
            "Stored dual residual mismatch")
    primal_objective = dot(cost)
    row_rhs = sum((y[i] * b[i] for i in range(M)), F(0))
    eq_rhs = sum((eta[k] * h[k] for k in range(Q)), F(0))
    dual_objective = row_rhs + eq_rhs
    require(primal_objective == dual_objective == F(certificate["objective"])
            == F(certificate["dual"]["objective"]), "Exact primal-dual gap is nonzero")
    require(row_rhs == F(certificate["dual"]["affine_inequality_rhs_payment"])
            and eq_rhs == F(certificate["dual"]["equality_rhs_payment"]), "Affine RHS accounting differs")
    require(sum(value == -1 for value in b) == 30, "A rhs=-1 affine row was omitted")
    require(F(certificate["K"]) == z[512], "Certificate K differs from the independent nonnegative column")
    row_products = [y[i] * slack[i] for i in range(M)]
    column_products = [residual[j] * z[j] for j in range(N)]
    require(all(value == 0 for value in row_products + column_products), "Exact complementarity fails")
    identity_rhs = sum(row_products, F(0)) + sum(column_products, F(0))
    identity_rhs += sum((eta[k] * eqres[k] for k in range(Q)), F(0))
    require(primal_objective - dual_objective == identity_rhs, "Full affine dual identity fails")
    positive = [i for i, weight in enumerate(y) if weight > 0]
    require(certificate["dual"]["positive_raw_indices"] == positive, "Positive raw payment catalogue changed")
    expected_positive_rows = [{
        "index": i, "name": data["raw_rows"][i]["name"], "family": data["raw_rows"][i]["family"],
        "weight": str(y[i]), "rhs": str(b[i]),
        "prepared_positive_divisor": str(bundle["divisors"][i]),
        "source_metadata": {key: value for key, value in data["raw_rows"][i].items() if key not in {"a", "rhs"}},
    } for i in positive]
    require(certificate["dual"]["positive_raw_rows"] == expected_positive_rows,
            "Actual positive-row IDs, literal source metadata or original scales changed")
    require(certificate["primal_support"] == [j for j, value in enumerate(z) if value > 0], "Primal support list differs")
    require(certificate["active_raw_indices"] == [i for i, value in enumerate(slack) if value == 0], "Active row catalogue differs")
    require(certificate["dual"]["equality_names"] == [row["name"] for row in data["equalities"]], "Free equalities reordered")
    row_checks = [{
        "raw_index": i, "name": data["raw_rows"][i]["name"], "family": data["raw_rows"][i]["family"],
        "rhs": str(b[i]), "primal_slack": str(slack[i]), "raw_dual_weight": str(y[i]),
        "complementarity": str(row_products[i]),
        "literal_raw_row_sha256": canonical_digest(data["raw_rows"][i]),
        "source_metadata_verbatim": {key: value for key, value in data["raw_rows"][i].items() if key not in {"a", "rhs"}},
    } for i in range(M)]
    column_checks = [{
        "column": j, "bits_or_K": format(j, "09b") if j < 512 else "K",
        "primal": str(z[j]), "objective_coefficient": str(cost.get(j, F(0))),
        "dual_residual": str(residual[j]), "complementarity": str(column_products[j]),
    } for j in range(N)]
    require(read_json(HERE / ("all" + str(M) + "_raw_row_checks.json")) == row_checks, "Stored all-row report differs")
    require(read_json(HERE / "all513_column_checks.json") == column_checks, "Stored all-column report differs")
    scales = certificate["recovery"]["all_raw_weight_scaling_checks"]
    require(len(scales) == M, "Incomplete original-scale bookkeeping")
    for i, item in enumerate(scales):
        divisor = F(bundle["scaling"]["raw_scales"][data["raw_rows"][i]["name"]])
        require(item["raw_index"] == i and item["name"] == data["raw_rows"][i]["name"]
                and F(item["positive_divisor"]) == divisor
                and F(item["exact_raw_weight"]) == y[i]
                and F(item["exact_scaled_weight"]) == y[i] * divisor
                and item["returned_scaled_weight"] == -discovery["inequality_marginals_scaled"][i]
                and item["returned_raw_weight"] == -discovery["inequality_marginals_scaled"][i] / float(divisor),
                "Original numerical-to-raw scale accounting differs at row " + str(i))
    result = {
        "status": CHECK_STATUS, "input_sha256": bundle["release"]["input_sha256"],
        "certificate_sha256": digest(HERE / "exact_certificate.json"),
        "discovery_sha256": digest(HERE / "discovery_output.json"),
        "all_raw_inequalities_checked": M, "all_nonnegative_columns_checked": N,
        "free_equality_multipliers_checked": Q, "free_equality_multipliers_signed": [str(v) for v in eta],
        "affine_rhs_minus_one_rows_checked": 30, "all_original_scales_checked": M,
        "objective": str(primal_objective), "affine_raw_rhs_payment": str(row_rhs), "equality_rhs_payment": str(eq_rhs),
        "duality_gap": "0", "all_complementarity_products_zero": True,
        "minimum_primal": str(min(z)), "minimum_raw_slack": str(min(slack)),
        "minimum_raw_weight": str(min(y)), "minimum_column_residual": str(min(residual)),
        "all_raw_row_slacks": [str(value) for value in slack],
        "all_column_residuals": [str(value) for value in residual],
        "all_raw_complementarity_products": [str(value) for value in row_products],
        "all_column_complementarity_products": [str(value) for value in column_products],
        "equality_residuals": [str(value) for value in eqres], "source_pins_verified": len(bundle["pins"]),
        "optimizer_calls_by_verifier": 0, "recovery_or_solver_imported": False,
        "all_actual_raw_metadata_records_checked": M, "source_builder_imported": False,
        "scope": "Exact frozen necessary-system optimality. Universal use also requires the released original-model source proofs. No SPE realization follows from this primal.",
    }
    write_new(HERE / "independent_check_result.json", result)
    print(json.dumps({key: result[key] for key in [
        "status", "objective", "all_raw_inequalities_checked", "all_nonnegative_columns_checked",
        "free_equality_multipliers_checked", "affine_rhs_minus_one_rows_checked", "optimizer_calls_by_verifier",
    ]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
