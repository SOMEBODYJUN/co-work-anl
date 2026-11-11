#!/usr/bin/env python3
"""One future explicitly released full1586 LP; currently only a waiting scaffold."""
from datetime import datetime, timezone
import json
import sys

sys.dont_write_bytecode = True
from contract import HERE, N, M, Q, digest, load_released, require, status, write_new

OPTIONS = {
    "time_limit": 60.0, "presolve": False,
    "primal_feasibility_tolerance": 1e-9, "dual_feasibility_tolerance": 1e-9,
}


def now():
    return datetime.now(timezone.utc).isoformat()


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--status":
        print(json.dumps(status(), indent=2))
        return 0
    require(len(sys.argv) == 1, "Only --status or the explicitly released entry is supported")
    require(not (HERE / "single_lp_consumed.json").exists(), "Call budget consumed; no retry")
    require(not (HERE / "discovery_output.json").exists(), "Existing discovery; no retry")
    bundle = load_released()
    # Imports occur only after exact input/evidence/Main-release validation.
    import numpy as np
    import scipy
    from scipy.optimize import linprog

    data, rows = bundle["data"], bundle["rows"]
    divisors = bundle["divisors"]
    A = np.array([[-float(row.get(j, 0) / divisor) for j in range(N)]
                  for row, divisor in zip(bundle["A"], divisors)])
    b = np.array([-float(rhs / divisor) for rhs, divisor in zip(bundle["b"], divisors)])
    E = np.array([[float(row.get(j, 0)) for j in range(N)] for row in bundle["E"]])
    h = np.array([float(value) for value in bundle["h"]])
    cost = np.array([float(bundle["cost"].get(j, 0)) for j in range(N)])
    require(A.shape == (M, N) and E.shape == (Q, N), "Complete numerical matrix required")
    release = bundle["release"]
    write_new(HERE / "source_pins_at_solve.json", bundle["pins"])
    record = {
        "authorized_by": "/root", "owner": "Boss1", "RUN": "six-boss1-20261111",
        "input_sha256": release["input_sha256"],
        "preparation_manifest_sha256": release["preparation_manifest_sha256"],
        "scaling_sha256": release["scaling_sha256"],
        "release_sha256": digest(HERE / "main_release.json"),
        "solver_script_sha256": digest(HERE / "solve_once.py"),
        "contract_script_sha256": digest(HERE / "contract.py"),
        "source_pins_sha256": digest(HERE / "source_pins_at_solve.json"),
        "optimizer_calls_consumed": 1, "status": "CONSUMED_BEFORE_OPTIMIZER_ENTRY",
        "raw_inequalities": M, "nonnegative_columns": N, "equalities": Q,
        "solver": "scipy.optimize.linprog/highs-ds", "scipy_version": scipy.__version__,
        "options": OPTIONS,
        "model_policy": "All raw rows/all513 columns; no pruning, fixedK, support restriction or point completion.",
        "start_utc": now(),
    }
    # Exclusive creation must succeed BEFORE the only optimizer call.
    write_new(HERE / "single_lp_consumed.json", record)
    try:
        result = linprog(cost, A_ub=A, b_ub=b, A_eq=E, b_eq=h,
                         bounds=(0, None), method="highs-ds", options=OPTIONS)
    except BaseException as error:
        write_new(HERE / "discovery_output.json", dict(
            record, optimizer_calls=1, success=False, status="EXCEPTION",
            exception_type=type(error).__name__, message=str(error), finish_utc=now()))
        raise

    def array(value):
        return None if value is None else value.tolist()

    def result_field(group, key):
        container = getattr(result, group, None)
        return None if container is None else array(getattr(container, key, None))

    output = dict(
        record, optimizer_calls=1, status=int(result.status), success=bool(result.success),
        message=result.message, iterations=int(result.nit),
        objective=None if result.fun is None else float(result.fun), x=array(result.x),
        raw_row_order=[row["name"] for row in rows],
        raw_row_divisors=[str(d) for d in divisors],
        inequality_residual_scaled=result_field("ineqlin", "residual"),
        inequality_marginals_scaled=result_field("ineqlin", "marginals"),
        equality_residual=result_field("eqlin", "residual"),
        equality_marginals=result_field("eqlin", "marginals"),
        lower_residual=result_field("lower", "residual"),
        lower_marginals=result_field("lower", "marginals"),
        upper_residual=result_field("upper", "residual"),
        upper_marginals=result_field("upper", "marginals"),
        finish_utc=now(),
    )
    write_new(HERE / "discovery_output.json", output)
    summary = {key: output[key] for key in [
        "success", "status", "objective", "iterations", "raw_inequalities",
        "nonnegative_columns", "equalities", "input_sha256",
    ]}
    summary["positive_columns"] = [] if result.x is None else [
        [j, float(value)] for j, value in enumerate(result.x) if value > 0
    ]
    marginals = output["inequality_marginals_scaled"]
    summary["positive_raw_rows"] = [] if marginals is None else [
        {"raw_index": i, "name": rows[i]["name"], "family": rows[i]["family"],
         "scaled_weight": -value, "positive_divisor": str(divisors[i]),
         "raw_weight_numeric": -value / float(divisors[i])}
        for i, value in enumerate(marginals) if value < 0
    ]
    summary["warning"] = "Numerical discovery only; exact certification and true-SPE diagnostics remain separate."
    write_new(HERE / "numerical_summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
