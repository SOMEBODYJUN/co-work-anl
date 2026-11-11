#!/usr/bin/env python3
"""Build the fresh exact-payment diagnostic queue; never infer a true-branch theorem.

Concrete source formulas and all weak minimizing states must be reviewed after
Main releases them. This first-stage scaffold deliberately contains no inherited
row IDs, internal SAFE weights, zero-state table or fixed utility/K relation.
"""
from fractions import Fraction as F
import json
import sys

sys.dont_write_bytecode = True
from contract import (HERE, M, N, Q, FACE_CHECK_STATUS, PLANNED_ROW_BLOCKS,
                      canonical_digest, digest, load_verified_certificate, read_json, require, status, write_new)


def main():
    if len(sys.argv) == 1 or sys.argv[1:] == ["--status"]:
        message = status()
        message["diagnostic_scope"] = "Fresh exact positive-payment queue only; source-specific mathematical diagnostics remain pending."
        print(json.dumps(message, ensure_ascii=False, indent=2))
        return 0
    require(sys.argv[1:] == ["--queue"], "This static stage supports --queue after exact verification only")
    bundle, certificate, checked = load_verified_certificate()
    face = read_json(HERE / "optimal_face.json")
    face_check = read_json(HERE / "optimal_face_check_result.json")
    require(face_check["status"] == FACE_CHECK_STATUS
            and face_check["input_sha256"] == certificate["input_sha256"]
            and face_check["face_sha256"] == digest(HERE / "optimal_face.json")
            and face_check["certificate_sha256"] == digest(HERE / "exact_certificate.json"),
            "The entire zero-residual face must be independently checked first")
    y = list(map(F, certificate["dual"]["raw_row_weights"]))
    positive = [i for i, value in enumerate(y) if value > 0]
    require(positive == certificate["dual"]["positive_raw_indices"] == face["positive_dual_raw_indices"],
            "Fresh exact positive payment domains differ")
    entries = []
    for i in positive:
        row = bundle["rows"][i]
        block = next(block for block in PLANNED_ROW_BLOCKS if block["start"] <= i < block["stop"])
        metadata = {key: value for key, value in row.items() if key not in {"a", "rhs"}}
        entries.append({
            "raw_index": i, "name": row["name"], "family": row["family"],
            "source_block": block["label"], "literal_raw_row_sha256": canonical_digest(row),
            "raw_weight": str(y[i]), "rhs": str(bundle["b"][i]),
            "numerical_divisor": str(bundle["divisors"][i]),
            "scaled_weight": str(y[i] * bundle["divisors"][i]),
            "actual_K_coefficient": str(bundle["A"][i].get(512, F(0))),
            "source_metadata_verbatim": metadata,
            "source_specific_status": "PENDING_CURRENT_SOURCE_FORMULA_AND_ALL_WEAK_STATE_REVIEW",
            "required_obligations": [
                "Identify this exact row's true IC weight a, history, source players and ordered query/tau parameters.",
                "Recheck the row's source proof and coefficient routing over every original column; retain K where uneliminated.",
                "Re-enumerate every actual weak equality/minimum state, including ties and zero-customer cases.",
                "Use positivity of this exact raw payment and its own nonnegative true-branch decomposition.",
                "For C-only equality rewrites, keep the signed free C-size multiplier unrestricted.",
                "Extend any conclusion to the entire independently checked face, including every original parameter inequality.",
                "State any surviving obstruction or missing source obligation; do not infer full SPE existence from a primal point.",
            ],
        })
    queue = {
        "status": "FRESH_EXACT_POSITIVE_PAYMENTS_IDENTIFIED_TRUE_BRANCH_DIAGNOSTICS_PENDING",
        "input_sha256": certificate["input_sha256"], "certificate_sha256": digest(HERE / "exact_certificate.json"),
        "face_sha256": digest(HERE / "optimal_face.json"), "face_check_sha256": digest(HERE / "optimal_face_check_result.json"),
        "all_raw_inequalities": M, "all_columns": N, "free_equalities": Q,
        "fresh_positive_raw_indices": positive, "positive_raw_rows": entries,
        "free_equality_multipliers": certificate["dual"]["equality_multipliers"],
        "zero_residual_columns": face["zero_residual_columns"],
        "old_positive_row_or_zero_state_assumptions_used": False,
        "numerical_divisor_used_as_true_IC_weight": False, "optimizer_calls_by_diagnostic_queue": 0,
        "source_specific_deductions_produced": 0, "SPE_existence_claim": False,
        "scope": "A complete source-review obligation queue, not a source-validity certificate or true-SPE face exclusion.",
        "continuation": "Main must release any additional current source formulas before source-specific diagnostics are implemented/read. No second LP or strengthened input is authorized.",
    }
    write_new(HERE / "positive_payment_diagnostic_queue.json", queue)
    print(json.dumps({key: queue[key] for key in ["status", "fresh_positive_raw_indices", "source_specific_deductions_produced",
                                               "optimizer_calls_by_diagnostic_queue"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
