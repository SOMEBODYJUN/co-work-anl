#!/usr/bin/env python3
"""A single explicitly released complete LP. Default invocation only reports status."""
from datetime import datetime, timezone
from math import isfinite
import json
import sys

sys.dont_write_bytecode = True
from contract import (HERE, N, M, Q, OWNER, RUN, AGENT, PROFILE, SOLVER_OPTIONS,
                      digest, load_released, require, status, write_new)

OPTIONS = {
    "time_limit": 60.0, "presolve": False,
    "primal_feasibility_tolerance": 1e-9, "dual_feasibility_tolerance": 1e-9,
}


def now():
    return datetime.now(timezone.utc).isoformat()


def numerical_value(value):
    """Lossless JSON conventions for the solver's unbounded-upper residuals."""
    if value is None:
        return None
    if isinstance(value, list):
        return [numerical_value(item) for item in value]
    if isinstance(value, float) and not isfinite(value):
        return "NaN" if value != value else ("Infinity" if value > 0 else "-Infinity")
    return value


def main():
    if len(sys.argv) == 1 or sys.argv[1:] == ["--status"]:
        print(json.dumps(status(), ensure_ascii=False, indent=2))
        return 0
    require(sys.argv[1:] == ["--run-released-once"], "Only --status or --run-released-once is supported")
    for name in ["single_lp_consumed.json", "discovery_output.json", "source_pins_at_solve.json"]:
        require(not (HERE / name).exists(), "Existing call record; no retry: " + name)
    bundle = load_released()
    require(OPTIONS == SOLVER_OPTIONS, "The released numerical settings and one-call entry differ")
    # Import only after final input, source closure, full model and Main release pass.
    import numpy as np
    import scipy
    from scipy.optimize import linprog

    rows, divisors = bundle["rows"], bundle["divisors"]
    A = np.array([[-float(row.get(j, 0) / divisor) for j in range(N)]
                  for row, divisor in zip(bundle["A"], divisors)])
    b = np.array([-float(rhs / divisor) for rhs, divisor in zip(bundle["b"], divisors)])
    E = np.array([[float(row.get(j, 0)) for j in range(N)] for row in bundle["E"]])
    h = np.array([float(value) for value in bundle["h"]])
    cost = np.array([float(bundle["cost"].get(j, 0)) for j in range(N)])
    require(A.shape == (M, N) and E.shape == (Q, N), "Complete unpruned numerical matrices required")
    require(all(np.isfinite(item).all() for item in [A, b, E, h, cost]), "Nonfinite full numerical conversion")
    release = bundle["release"]
    write_new(HERE / "source_pins_at_solve.json", bundle["pins"])
    record = {
        "authorized_by": "/root", "owner": OWNER, "RUN": RUN, "agent": AGENT, "profile": PROFILE,
        "input_sha256": release["input_sha256"],
        "preparation_manifest_sha256": release["preparation_manifest_sha256"],
        "scaling_sha256": release["scaling_sha256"],
        "row_catalog_sha256": release["row_catalog_sha256"],
        "release_sha256": digest(HERE / "main_release.json"),
        "solver_script_sha256": digest(HERE / "solve_once.py"),
        "contract_script_sha256": digest(HERE / "contract.py"),
        "source_pins_sha256": digest(HERE / "source_pins_at_solve.json"),
        "optimizer_calls_consumed": 1, "status": "CONSUMED_BEFORE_OPTIMIZER_ENTRY",
        "raw_inequalities": M, "nonnegative_columns": N, "equalities": Q,
        "solver": "scipy.optimize.linprog/highs-ds", "scipy_version": scipy.__version__,
        "numpy_version": np.__version__, "options": OPTIONS,
        "model_policy": "Every raw row and all 513 columns, original equalities and objective; no model restriction.",
        "consumption_policy": "Exclusive durable marker is permanent even after an exception or process interruption.",
        "start_utc": now(),
    }
    # The durable exclusive creation must finish before the only optimizer call.
    write_new(HERE / "single_lp_consumed.json", record)
    marker_sha256 = digest(HERE / "single_lp_consumed.json")
    try:
        result = linprog(cost, A_ub=A, b_ub=b, A_eq=E, b_eq=h,
                         bounds=(0, None), method="highs-ds", options=OPTIONS)
    except BaseException as error:
        write_new(HERE / "discovery_output.json", dict(
            record, optimizer_calls=1, success=False, status="EXCEPTION",
            consumption_marker_sha256=marker_sha256,
            exception_type=type(error).__name__, message=str(error), finish_utc=now()))
        raise

    def array(value):
        return None if value is None else numerical_value(value.tolist())

    def result_field(group, key):
        container = getattr(result, group, None)
        return None if container is None else array(getattr(container, key, None))

    output = dict(
        record, optimizer_calls=1, status=int(result.status), success=bool(result.success),
        consumption_marker_sha256=marker_sha256,
        message=str(result.message), iterations=int(result.nit),
        crossover_iterations=getattr(result, "crossover_nit", None),
        objective=None if result.fun is None else numerical_value(float(result.fun)), x=array(result.x),
        raw_row_order=[row["name"] for row in rows], raw_row_divisors=[str(d) for d in divisors],
        raw_row_blocks=release["expected_row_blocks"],
        inequality_residual_scaled=result_field("ineqlin", "residual"),
        inequality_marginals_scaled=result_field("ineqlin", "marginals"),
        equality_residual=result_field("eqlin", "residual"),
        equality_marginals=result_field("eqlin", "marginals"),
        lower_residual=result_field("lower", "residual"),
        lower_marginals=result_field("lower", "marginals"),
        upper_residual=result_field("upper", "residual"),
        upper_marginals=result_field("upper", "marginals"), finish_utc=now(),
        nonfinite_numeric_encoding="Infinity/-Infinity/NaN strings, reversibly preserving original special values",
    )
    write_new(HERE / "discovery_output.json", output)
    summary = {key: output[key] for key in [
        "success", "status", "objective", "iterations", "raw_inequalities",
        "nonnegative_columns", "equalities", "input_sha256",
    ]}
    summary["positive_columns"] = [] if result.x is None else [
        [j, numerical_value(float(value))] for j, value in enumerate(result.x) if value > 0
    ]
    marginals = output["inequality_marginals_scaled"]
    summary["positive_raw_rows"] = [] if marginals is None else [
        {"raw_index": i, "name": rows[i]["name"], "family": rows[i]["family"],
         "returned_scaled_weight": -value, "positive_divisor": str(divisors[i]),
         "raw_weight_numeric": -value / float(divisors[i]),
         "source_metadata_verbatim": {key: item for key, item in rows[i].items() if key not in {"a", "rhs"}}}
        for i, value in enumerate(marginals) if isinstance(value, (int, float)) and value < 0
    ]
    summary["scope"] = "Numerical discovery only; exact recovery, independent verification and fresh source diagnostics remain."
    write_new(HERE / "numerical_summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=False))
    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
