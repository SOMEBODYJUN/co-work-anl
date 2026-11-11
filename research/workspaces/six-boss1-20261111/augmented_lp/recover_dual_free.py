"""Recover an exact dual on the whole zero-reduced-cost face.

Positive primal columns alone can leave dual multipliers underdetermined.
Use all numerically zero reduced-cost columns, then choose remaining free
variables close to the floating dual. Exact feasibility, not proximity,
certifies the result.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import gzip
import json
import sys
import time
import traceback

import numpy as np

HERE = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent


def affine_solve(equations, n, seed):
    basis = {}
    for equation in equations:
        row = {j: F(value) for j, value in enumerate(equation) if value}
        while True:
            variables = [j for j in row if j < n]
            if not variables:
                assert not row.get(n, F()), ("inconsistent", row)
                break
            pivot = min(variables)
            if pivot not in basis:
                scale = row[pivot]
                basis[pivot] = {j: value / scale for j, value in row.items()}
                break
            scale = row[pivot]
            for j, value in basis[pivot].items():
                updated = row.get(j, F()) - scale * value
                if updated:
                    row[j] = updated
                else:
                    row.pop(j, None)
    free = sorted(set(range(n)) - set(basis))
    answer = [F()] * n
    for j in free:
        answer[j] = F(float(seed[j])).limit_denominator(10**12)
    for pivot in sorted(basis, reverse=True):
        row = basis[pivot]
        answer[pivot] = row.get(n, F()) - sum((value * answer[j] for j, value in row.items() if pivot < j < n), F())
    return answer, {"rank": len(basis), "variables": n, "free_variables": free,
                    "free_values": [[j, str(answer[j])] for j in free]}


def main():
    started = time.time()
    with gzip.open(HERE / "exact_matrix.json.gz", "rt") as stream:
        matrix = json.load(stream)
    point = json.loads((HERE / "augmented_lp_exact.json").read_text())
    rows = [{j: F(value) for j, value in row} for row in matrix["rows"]]
    norm, obj = list(map(F, matrix["normalization"])), list(map(F, matrix["objective"]))
    floats = np.load(HERE / "floating_solver_arrays.npz")
    multipliers = -floats["inequality_marginals"] / floats["scales"]
    keep = [i for i, value in enumerate(multipliers) if value > 1e-9]
    zero_columns = [j for j, value in enumerate(floats["lower_marginals"]) if abs(value) < 1e-9]
    equations = [[rows[i].get(j, F()) for i in keep] + [norm[j], obj[j]] for j in zero_columns]
    equations.append([F()] * len(keep) + [F(1), F(point["W"])])
    unique = list(dict.fromkeys(tuple(eq) for eq in equations if any(eq)))
    seed = [multipliers[i] for i in keep] + [float(F(point["W"]))]
    weights, recovery = affine_solve(unique, len(keep)+1, seed)
    lam, lower = weights[:-1], weights[-1]
    assert min(lam) >= 0
    residuals = [a-lower*b for a,b in zip(obj, norm)]
    for i, weight in zip(keep, lam):
        for j, coefficient in rows[i].items():
            residuals[j] -= weight*coefficient
    assert min(residuals) >= 0, (residuals.index(min(residuals)), str(min(residuals)))
    assert lower == F(point["W"])
    certificate = {"verified": True, "normalization_multiplier": str(lower),
                   "row_multipliers": [[i, str(weight)] for i,weight in zip(keep,lam) if weight],
                   "minimum_coefficient_residual": str(min(residuals)), "residuals": list(map(str,residuals)),
                   "equality_to_primal": True,
                   "identity": "obj = lower * norm + sum_i lambda_i * row_i + nonnegative residual; lambda >= 0",
                   "recovery": {**recovery, "zero_reduced_cost_columns": len(zero_columns), "unique_nonzero_equations": len(unique)},
                   "matrix_sha256": sha256((HERE / "exact_matrix.json.gz").read_bytes()).hexdigest(),
                   "seconds": time.time()-started}
    (HERE / "exact_dual_certificate.json").write_text(json.dumps(certificate,indent=2)+"\n")
    status_path = HERE / "status.json"
    status = json.loads(status_path.read_text())
    old_W = F(json.loads((HERE / "old_point_audit.json").read_text())["W"])
    status.update({"exact_optimum_verified": True, "strictly_above_old_W": lower > old_W,
                   "exact_optimum_increase": str(lower-old_W), "dual_recovery": certificate["recovery"]})
    status_path.write_text(json.dumps(status,indent=2)+"\n")
    print(json.dumps({k:v for k,v in certificate.items() if k not in {"row_multipliers","residuals"}},indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        (HERE / "dual_free_failure.json").write_text(json.dumps({"traceback": traceback.format_exc()},indent=2)+"\n")
        raise
