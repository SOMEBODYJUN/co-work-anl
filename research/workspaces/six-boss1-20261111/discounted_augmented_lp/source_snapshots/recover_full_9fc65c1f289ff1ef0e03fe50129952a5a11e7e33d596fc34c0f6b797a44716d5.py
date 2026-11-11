"""Exact sparse recovery with both canonical positive parts and minima.

Primal elimination has only positive original columns as variables.  Auxiliary
values are then recomputed as exact positive parts, and every full row is
checked.  Dual elimination orders threshold multipliers first so each simple
auxiliary-column equation is eliminated before original-column equations.
No full dense Fraction matrix is formed.
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import gzip
import json
import time
import traceback

import numpy as np

from solve_full import HERE, BASE, write, log, dot


def sparse_affine_solve(equations, n, seed, label):
    basis = {}
    processed = 0
    last_log = time.time()
    largest_basis_row = 0
    for encoded in equations:
        row = {j: value for j, value in encoded.items() if value}
        processed += 1
        while row:
            pivot = min(row)
            if pivot == n:
                raise AssertionError(("inconsistent exact equations", label, processed, str(row[n])))
            if pivot not in basis:
                scale = row[pivot]
                basis[pivot] = {j: value/scale for j, value in row.items()}
                largest_basis_row = max(largest_basis_row, len(row))
                break
            scale = row[pivot]
            for j, value in basis[pivot].items():
                updated = row.get(j, F()) - scale*value
                if updated:
                    row[j] = updated
                else:
                    row.pop(j, None)
        if time.time()-last_log > 15:
            log("sparse_elimination_progress", label=label, processed=processed, rank=len(basis), variables=n)
            last_log = time.time()
    free = sorted(set(range(n))-set(basis))
    answer = [F()] * n
    for j in free:
        answer[j] = F(float(seed[j])).limit_denominator(10**12)
    for pivot in sorted(basis, reverse=True):
        row = basis[pivot]
        answer[pivot] = row.get(n, F()) - sum((value*answer[j] for j, value in row.items() if pivot < j < n), F())
    return answer, {"variables": n, "rank": len(basis), "processed_equations": processed,
                    "largest_sparse_basis_row": largest_basis_row, "free_variables": free,
                    "free_values": [[j, str(answer[j])] for j in free]}


def load():
    with gzip.open(HERE / "exact_matrix.json.gz", "rt", encoding="utf-8") as stream:
        matrix = json.load(stream)
    rows = [{j: F(v) for j, v in row} for row in matrix["rows"]]
    norm, obj = list(map(F, matrix["normalization"])), list(map(F, matrix["objective"]))
    structure = json.loads((HERE / "epigraph_structure.json").read_text())
    floats = np.load(HERE / "floating_solver_arrays.npz")
    zz_structure = json.loads((HERE / "zz_envelope_structure.json").read_text())
    return matrix, rows, norm, obj, structure, zz_structure, floats


def recover_primal(matrix, rows, norm, obj, structure, zz_structure, floats):
    started = time.time()
    n, original_n = len(matrix["columns"]), structure["original_columns"]
    numerical = floats["canonical"]
    keep = [j for j in range(original_n) if numerical[j] > 1e-9]
    local = {j: k for k, j in enumerate(keep)}
    thresholds = dict(structure["thresholds"])
    threshold_indices = set(thresholds.values()) | set(zz_structure["upper_rows"])
    budget_indices = set(structure["budget_rows"]) | set(zz_structure["budget_rows"])
    support_values = numerical[keep]
    equations = []
    descriptions = []
    seen = set()

    def maybe_add(row, description):
        restricted = {local[j]: v for j, v in row.items() if j in local and v}
        if not restricted:
            return
        scale = max(float(abs(v)) for v in restricted.values())
        slack = sum(float(v)*support_values[j] for j, v in restricted.items())
        if abs(slack) >= 1e-10*scale:
            return
        signature = tuple(sorted(restricted.items()))
        if signature not in seen:
            seen.add(signature)
            equations.append(restricted)
            descriptions.append(description)

    positive_parts = {}
    zero_hinges = 0
    for j, i in thresholds.items():
        hinge = {k: -v for k, v in rows[i].items() if k < original_n}
        positive_parts[j] = hinge if numerical[j] > 1e-9 else {}
        before = len(equations)
        maybe_add(hinge, {"kind": "canonical_hinge_zero", "auxiliary": j, "threshold_row": i})
        zero_hinges += len(equations)-before
    min_ties = 0
    for record in zz_structure["auxiliaries"]:
        j = record["column"]
        q = {k: v for k, v in rows[record["q_upper_row"]].items() if k < original_n}
        v = {k: value for k, value in rows[record["v_upper_row"]].items() if k < original_n}
        qvalue = sum(float(value)*numerical[k] for k, value in q.items())
        vvalue = sum(float(value)*numerical[k] for k, value in v.items())
        positive_parts[j] = q if qvalue <= vvalue else v
        difference = defaultdict(F, q)
        for k, value in v.items():
            difference[k] -= value
        before = len(equations)
        maybe_add(dict(difference), {"kind": "canonical_min_tie", "auxiliary": j})
        min_ties += len(equations)-before
    for i, row in enumerate(rows):
        if i in threshold_indices:
            continue
        if i in budget_indices:
            projected = defaultdict(F, {j: v for j, v in row.items() if j < original_n})
            for j, coefficient in row.items():
                if j >= original_n:
                    for k, value in positive_parts[j].items():
                        projected[k] += coefficient*value
            projected = {j: v for j, v in projected.items() if v}
            maybe_add(projected, {"kind": "canonical_budget_active", "row": i})
        else:
            assert all(j < original_n for j in row)
            maybe_add(row, {"kind": "original_active_row", "row": i})
    equations.append({**{local[j]: norm[j] for j in keep if norm[j]}, len(keep): F(1)})
    descriptions.append({"kind": "normalization"})
    log("exact_primal_recovery_started", original_positive_columns=len(keep),
        unique_equations=len(equations), unique_hinge_equations=zero_hinges,
        unique_min_tie_equations=min_ties, eliminated_auxiliary_columns=n-original_n)
    answer, recovery = sparse_affine_solve(equations, len(keep), support_values, "primal_original_prefix")
    full = [F()] * n
    for j, value in zip(keep, answer):
        full[j] = value
    assert min(full) >= 0, ("negative original mass", str(min(full)))
    for j, i in thresholds.items():
        full[j] = max(F(), -dot({k: v for k, v in rows[i].items() if k < original_n}, full))
    for record in zz_structure["auxiliaries"]:
        full[record["column"]] = min(dot({k: v for k, v in rows[i].items() if k < original_n}, full)
                                      for i in (record["q_upper_row"], record["v_upper_row"]))
    assert sum((a*b for a, b in zip(norm, full)), F()) == 1
    slacks = [dot(row, full) for row in rows]
    assert min(slacks) >= 0, ("negative full-row slack", slacks.index(min(slacks)), str(min(slacks)))
    W = sum((a*b for a, b in zip(obj, full)), F())
    recovery.update({"method": "sparse exact original-prefix active-face elimination followed by canonical max and min auxiliaries",
                     "support": keep, "active_equations": descriptions,
                     "original_positive_columns": sum(v > 0 for v in full[:original_n]),
                     "auxiliary_positive_columns": sum(v > 0 for v in full[original_n:]),
                     "old_max_positive_columns": sum(v > 0 for v in full[original_n:zz_structure["prior_columns"]]),
                     "new_min_positive_columns": sum(v > 0 for v in full[zz_structure["prior_columns"]:]),
                     "min_tie_equations": min_ties,
                     "seconds": time.time()-started})
    point = {"scope": "exact feasible fixed16hist necessary relaxation; not SPE or game counterexample",
             "O": "1", "W": str(W), "strict_half_gap": str(1-2*W),
             "verified_rows": len(rows), "minimum_slack": str(min(slacks)),
             "positive_columns": sum(v > 0 for v in full), "exact_verified": True,
             "completion": "old auxiliary values are exact canonical positive parts; new envelope values are exact canonical minima",
             "original_columns": original_n,
             "columns": [{**col, "weight": str(v)} for col, v in zip(matrix["columns"], full)]}
    write("augmented_lp_exact.json", point)
    write("primal_exact_audit.json", {"W": str(W), "W_float": float(W), "minimum_slack": str(min(slacks)),
                                     "row_slacks": list(map(str, slacks)), "recovery": recovery})
    status = json.loads((HERE / "status.json").read_text())
    baseline_W = F(json.loads((HERE / "old_point_audit.json").read_text())["W"])
    status.update({"exact_verified": True, "W_exact": str(W), "below_half": W < F(1, 2),
                   "exact_point_difference_from_baseline": str(W-baseline_W),
                   "positive_exact_original_columns": recovery["original_positive_columns"],
                   "positive_exact_auxiliary_columns": recovery["auxiliary_positive_columns"]})
    write("status.json", status)
    log("exact_primal_saved", W=str(W), W_float=float(W), below_half=W < F(1, 2),
        original_positive_columns=recovery["original_positive_columns"],
        auxiliary_positive_columns=recovery["auxiliary_positive_columns"],
        recovery_rank=recovery["rank"], free_variables=len(recovery["free_variables"]))
    return full, W


def carried_lower_bound(rows, norm, obj, W):
    path = BASE / "exact_dual_certificate.json"
    old = json.loads(path.read_text())
    lower = F(old["normalization_multiplier"])
    residuals = [c-lower*a for c, a in zip(obj, norm)]
    for i, weight in old["row_multipliers"]:
        weight = F(weight)
        assert weight >= 0
        for j, value in rows[i].items():
            residuals[j] -= weight*value
    assert min(residuals) >= 0
    write("inherited_dual_lower_bound.json", {"verified": True, "normalization_multiplier": str(lower),
          "source_sha256": sha256(path.read_bytes()).hexdigest(), "source": str(path),
          "row_multipliers": old["row_multipliers"], "residuals": list(map(str, residuals)),
          "upper_bound": str(W), "gap": str(W-lower),
          "scope": "rigorous inherited lower bound for this enlarged finite necessary LP"})
    status = json.loads((HERE / "status.json").read_text())
    status.update({"certified_lower_bound": str(lower), "certified_upper_bound": str(W),
                   "certified_bound_gap": str(W-lower)})
    write("status.json", status)
    return lower


def recover_dual(matrix, rows, norm, obj, structure, zz_structure, floats, full, W):
    started = time.time()
    multipliers = -floats["inequality_marginals"] / floats["scales"]
    threshold_indices = set(dict(structure["thresholds"]).values()) | set(zz_structure["upper_rows"])
    keep = [i for i, value in enumerate(multipliers) if value > 1e-9]
    keep.sort(key=lambda i: (i not in threshold_indices, i))
    local = {i: k for k, i in enumerate(keep)}
    n = len(keep)+1
    lower_index, rhs_index = n-1, n
    zero_columns = [j for j, reduced in enumerate(floats["lower_marginals"])
                    if abs(reduced) < 1e-9 or full[j] > 0]
    zero_columns.sort(key=lambda j: (j < structure["original_columns"], j))
    transpose = {j: {} for j in zero_columns}
    for i in keep:
        for j, value in rows[i].items():
            if j in transpose:
                transpose[j][local[i]] = value
    equations = []
    seen = set()
    for j in zero_columns:
        equation = transpose[j]
        if norm[j]:
            equation[lower_index] = norm[j]
        if obj[j]:
            equation[rhs_index] = obj[j]
        if not equation:
            continue
        signature = tuple(sorted(equation.items()))
        if signature not in seen:
            seen.add(signature)
            equations.append(equation)
    equations.append({lower_index: F(1), rhs_index: W})
    del transpose, seen
    seed = [multipliers[i] for i in keep] + [float(W)]
    log("exact_dual_recovery_started", positive_numerical_row_multipliers=len(keep),
        zero_reduced_cost_columns=len(zero_columns), unique_nonzero_equations=len(equations),
        threshold_multipliers_first=sum(i in threshold_indices for i in keep))
    weights, recovery = sparse_affine_solve(equations, n, seed, "dual_thresholds_first")
    lam, lower = weights[:-1], weights[-1]
    assert min(lam) >= 0, ("negative dual weight", str(min(lam)))
    residuals = [c-lower*a for c, a in zip(obj, norm)]
    for i, weight in zip(keep, lam):
        for j, value in rows[i].items():
            residuals[j] -= weight*value
    assert min(residuals) >= 0, ("negative dual residual", residuals.index(min(residuals)), str(min(residuals)))
    assert lower == W
    certificate = {"verified": True, "normalization_multiplier": str(lower),
                   "row_multipliers": [[i, str(weight)] for i, weight in zip(keep, lam) if weight],
                   "minimum_coefficient_residual": str(min(residuals)), "residuals": list(map(str, residuals)),
                   "equality_to_primal": True,
                   "identity": "obj = lower * norm + sum_i lambda_i * row_i + nonnegative residual; lambda >= 0",
                   "recovery": {**recovery, "zero_reduced_cost_columns": len(zero_columns),
                                "unique_nonzero_equations": len(equations),
                                "method": "fully sparse exact elimination, auxiliary-column equations first"},
                   "matrix_sha256": sha256((HERE / "exact_matrix.json.gz").read_bytes()).hexdigest(),
                   "seconds": time.time()-started}
    write("exact_dual_certificate.json", certificate)
    status = json.loads((HERE / "status.json").read_text())
    old_W = F(json.loads((HERE / "old_point_audit.json").read_text())["W"])
    status.update({"exact_optimum_verified": True, "strictly_above_old_W": lower > old_W,
                   "exact_optimum_increase": str(lower-old_W), "dual_recovery": certificate["recovery"],
                   "certified_lower_bound": str(lower), "certified_upper_bound": str(W), "certified_bound_gap": "0"})
    write("status.json", status)
    log("exact_optimum_verified", W=str(W), W_float=float(W), below_half=W < F(1, 2),
        positive_dual_rows=sum(weight > 0 for weight in lam), recovery_rank=recovery["rank"],
        free_variables=len(recovery["free_variables"]))


def main():
    log("recovery_start")
    matrix, rows, norm, obj, structure, zz_structure, floats = load()
    write("recovery_inputs.json", {"sha256": {name: sha256((HERE / name).read_bytes()).hexdigest()
          for name in ("recover_full.py", "solve_full.py", "exact_matrix.json.gz", "floating_solver_arrays.npz", "epigraph_structure.json", "zz_envelope_structure.json")}})
    full, W = recover_primal(matrix, rows, norm, obj, structure, zz_structure, floats)
    lower = carried_lower_bound(rows, norm, obj, W)
    if lower == W:
        inherited = json.loads((HERE / "inherited_dual_lower_bound.json").read_text())
        certificate = {"verified": True, "normalization_multiplier": str(lower),
                       "row_multipliers": inherited["row_multipliers"], "residuals": inherited["residuals"],
                       "minimum_coefficient_residual": str(min(map(F, inherited["residuals"]))),
                       "equality_to_primal": True,
                       "identity": "obj = lower * norm + sum_i lambda_i * row_i + nonnegative residual; lambda >= 0",
                       "recovery": {"method": "inherited exact dual extended by zero new-row weights and zero new-column residuals",
                                    "source_sha256": inherited["source_sha256"]},
                       "matrix_sha256": sha256((HERE / "exact_matrix.json.gz").read_bytes()).hexdigest()}
        write("exact_dual_certificate.json", certificate)
        status = json.loads((HERE / "status.json").read_text())
        status.update({"exact_optimum_verified": True, "strictly_above_old_W": False,
                       "exact_optimum_increase": "0", "certified_lower_bound": str(W), "certified_upper_bound": str(W),
                       "certified_bound_gap": "0", "dual_recovery": certificate["recovery"]})
        write("status.json", status)
        log("exact_optimum_verified", W=str(W), W_float=float(W), below_half=W < F(1, 2),
            positive_dual_rows=len(certificate["row_multipliers"]), recovery="inherited_zero_extension")
        return
    try:
        recover_dual(matrix, rows, norm, obj, structure, zz_structure, floats, full, W)
    except Exception:
        failure = traceback.format_exc()
        status = json.loads((HERE / "status.json").read_text())
        status["exact_dual_failure"] = failure
        write("status.json", status)
        write("exact_dual_failure.json", {"traceback": failure})
        log("exact_dual_failed", detail=failure)
        raise


if __name__ == "__main__":
    try:
        main()
    except Exception:
        write("recovery_failure.json", {"traceback": traceback.format_exc()})
        raise
