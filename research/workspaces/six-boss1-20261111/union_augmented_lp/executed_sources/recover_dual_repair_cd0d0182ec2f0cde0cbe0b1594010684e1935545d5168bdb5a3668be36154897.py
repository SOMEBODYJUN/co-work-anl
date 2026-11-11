"""Repair exact dual recovery using exact primal complementarity.

The original 1e-9 numerical support cutoff omitted row1894, whose weight is
about3.85e-10, and simultaneously treated column907's equally small reduced
cost as zero.  Retain the original solve and exact primal.  Candidate dual
support is selected at1e-12 and then pruned by exactly positive primal slacks.
Only strictly positive exact primal columns impose zero-residual equations;
all15593 residuals and every complementary slack are checked afterwards.
"""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json
import time
import traceback

from recover_full import load, sparse_affine_solve
from solve_full import HERE, BASE, write, log, dot


def main():
    start = time.time()
    write("recovery_repair_inputs.json",{"sha256":{name:sha256((HERE/name).read_bytes()).hexdigest() for name in (
        "recover_dual_repair.py","recover_full.py","solve_full.py","exact_matrix.json.gz",
        "floating_solver_arrays.npz","augmented_lp_exact.json","primal_exact_audit.json",
        "epigraph_structure.json","zz_envelope_structure.json","exact_dual_failure.json")}})
    matrix, rows, norm, obj, structure, zz_structure, floats = load()
    point = json.loads((HERE/"augmented_lp_exact.json").read_text())
    full = [F(column["weight"]) for column in point["columns"]]
    W = F(point["W"])
    slacks = [dot(row,full) for row in rows]
    assert min(full) >= 0 and min(slacks) >= 0
    assert sum((a*b for a,b in zip(norm,full)), F()) == 1
    assert sum((a*b for a,b in zip(obj,full)), F()) == W
    numerical = -floats["inequality_marginals"]/floats["scales"]
    threshold_indices = set(dict(structure["thresholds"]).values()) | set(zz_structure["upper_rows"])
    keep = [i for i,value in enumerate(numerical) if value > 1e-12 and slacks[i] == 0]
    keep.sort(key=lambda i:(i not in threshold_indices,i))
    columns = [j for j,value in enumerate(full) if value > 0]
    columns.sort(key=lambda j:(j < structure["original_columns"],j))
    omitted_rows = [{"row":i,"name":matrix["row_names"][i],"numerical_weight":float(numerical[i]),
                     "exact_primal_slack":str(slacks[i])} for i in keep if numerical[i] <= 1e-9]
    false_zero_columns = [{"column":j,"numerical_reduced_cost":float(value),"exact_primal_weight":str(full[j])}
                          for j,value in enumerate(floats["lower_marginals"]) if 1e-12 < value < 1e-9]
    diagnostic = {"reason":"The original1e-9 cutoff omitted a small positive dual row and forced a small positive reduced cost to zero.",
                  "original_dual_row_cutoff":1e-9,"repaired_candidate_cutoff":1e-12,
                  "exact_primal_complementarity_pruning":True,"only_positive_exact_primal_columns_forced_zero":True,
                  "original_omitted_rows":omitted_rows,"original_false_zero_columns":false_zero_columns,
                  "candidate_rows":len(keep),"positive_exact_primal_columns":len(columns),
                  "numerical_optimization_calls":0}
    write("dual_repair_diagnostics.json",diagnostic)
    local = {i:k for k,i in enumerate(keep)}
    n = len(keep)+1
    lower_index, rhs_index = n-1,n
    transpose = {j:{} for j in columns}
    for i in keep:
        for j,value in rows[i].items():
            if j in transpose:
                transpose[j][local[i]] = value
    equations, descriptions, seen = [],[],set()
    for j in columns:
        equation = transpose[j]
        if norm[j]: equation[lower_index] = norm[j]
        if obj[j]: equation[rhs_index] = obj[j]
        if not equation: continue
        signature = tuple(sorted(equation.items()))
        if signature not in seen:
            seen.add(signature)
            equations.append(equation)
            descriptions.append({"positive_exact_primal_column":j})
    equations.append({lower_index:F(1),rhs_index:W})
    descriptions.append({"fixed_exact_primal_objective":str(W)})
    seed = [numerical[i] for i in keep]+[float(W)]
    log("exact_dual_complementarity_repair_started",candidate_rows=len(keep),positive_primal_columns=len(columns),
        unique_equations=len(equations),previously_omitted_rows=omitted_rows)
    answer,recovery = sparse_affine_solve(equations,n,seed,"dual_exact_primal_complementarity")
    lam,lower = answer[:-1],answer[-1]
    assert min(lam) >= 0 and lower == W
    residuals = [c-lower*a for c,a in zip(obj,norm)]
    for i,weight in zip(keep,lam):
        assert weight*slacks[i] == 0
        for j,value in rows[i].items():
            residuals[j] -= weight*value
    assert min(residuals) >= 0, ("negative exact dual residual",residuals.index(min(residuals)),str(min(residuals)))
    assert sum((a*b for a,b in zip(residuals,full)),F()) == 0
    certificate = {"verified":True,"normalization_multiplier":str(lower),
                   "row_multipliers":[[i,str(weight)] for i,weight in zip(keep,lam) if weight],
                   "minimum_coefficient_residual":str(min(residuals)),"residuals":list(map(str,residuals)),
                   "equality_to_primal":True,
                   "identity":"obj = lower * norm + sum_i lambda_i * row_i + nonnegative residual; lambda >= 0",
                   "recovery":{**recovery,"support_rows":keep,"positive_exact_primal_column_indices":columns,
                               "unique_nonzero_equations":len(equations),"active_equation_descriptions":descriptions,
                               "method":"exact primal complementarity;1e-12 candidate-row selection, then exact zero-slack pruning; zero residuals imposed only at positive exact primal columns"},
                   "matrix_sha256":sha256((HERE/"exact_matrix.json.gz").read_bytes()).hexdigest(),
                   "seconds":time.time()-start}
    write("exact_dual_certificate.json",certificate)
    old_W = F(json.loads((BASE/"augmented_lp_exact.json").read_text())["W"])
    status = json.loads((HERE/"status.json").read_text())
    status.update({"exact_optimum_verified":True,"exact_dual_failure_resolved":True,
                   "dual_repair_source_sha256":sha256(Path(__file__).read_bytes()).hexdigest(),
                   "strictly_above_old_W":W > old_W,"exact_optimum_increase":str(W-old_W),
                   "dual_recovery":certificate["recovery"],"certified_lower_bound":str(W),
                   "certified_upper_bound":str(W),"certified_bound_gap":"0"})
    write("status.json",status)
    log("exact_optimum_verified_after_complementarity_repair",W=str(W),W_float=float(W),
        positive_dual_rows=len(certificate["row_multipliers"]),recovery_rank=recovery["rank"],
        free_variables=len(recovery["free_variables"]),numerical_optimization_calls=0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        write("dual_repair_failure.json",{"traceback":traceback.format_exc()})
        raise
