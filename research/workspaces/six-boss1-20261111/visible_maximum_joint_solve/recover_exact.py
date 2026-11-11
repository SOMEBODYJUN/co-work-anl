#!/usr/bin/env python3
"""Recover exact certificates from the sole numerical support; never optimize."""
from fractions import Fraction as F
from hashlib import sha256
from math import lcm
from pathlib import Path
import json
import sympy as sp

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "visible_maximum_joint"
INPUT_SHA = "b0610bb00298a4ee953423a8066dab050cb9d515fd6d5dde41f5117116f2ba33"
N, M, Q = 513, 1002, 2
sha = lambda p: sha256(p.read_bytes()).hexdigest()
dump = lambda p, v: p.write_text(json.dumps(v, indent=2) + "\n")
sr = lambda f: sp.Rational(f.numerator, f.denominator)
fr = lambda s: F(int(s.p), int(s.q))
assert sha(SOURCE / "exact_input.json") == INPUT_SHA
inp = json.loads((SOURCE / "exact_input.json").read_text())
disc = json.loads((HERE / "discovery_output.json").read_text())
assert disc["success"] and disc["optimizer_calls"] == 1 and disc["input_sha256"] == INPUT_SHA
rows = inp["raw_rows"]
assert len(rows) == M and len(inp["equalities"]) == Q and inp["variables"] == N
A = [{int(j): F(a) for j, a in r["a"].items()} for r in rows]
b = [F(r["rhs"]) for r in rows]
E = [{int(j): F(a) for j, a in e["a"].items()} for e in inp["equalities"]]
h = [F(e["rhs"]) for e in inp["equalities"]]
c = [F(inp["objective"].get(str(j), "0")) for j in range(N)]
dot = lambda row, vector: sum((a * vector[j] for j, a in row.items()), F(0))
support = [j for j, v in enumerate(disc["x"]) if v > 1e-9]
tight = [i for i, s in enumerate(disc["inequality_residual_scaled"]) if abs(s) < 1e-8]
dual_support = [i for i, v in enumerate(disc["inequality_marginals_scaled"]) if -v > 1e-9]
pm = sp.Matrix([[sr(e.get(j, F(0))) for j in support] for e in E] +
               [[sr(A[i].get(j, F(0))) for j in support] for i in tight])
pb = sp.Matrix([sr(v) for v in h] + [sr(b[i]) for i in tight])
pset = sp.linsolve((pm, pb))
assert len(pset) == 1, "Numerical primal support does not admit the exact active equations."
psol = next(iter(pset))
assert all(v.is_Rational and not v.free_symbols for v in psol), "Exact primal support is not uniquely determined."
z = [F(0)] * N
for j, v in zip(support, psol):
    z[j] = fr(v)
assert all(v >= 0 for v in z)
slacks = [dot(row, z) - br for row, br in zip(A, b)]
eqres = [dot(e, z) - eh for e, eh in zip(E, h)]
assert all(s >= 0 for s in slacks), [(i, str(s)) for i, s in enumerate(slacks) if s < 0]
assert eqres == [F(0)] * Q
W = sum((cj * zj for cj, zj in zip(c, z)), F(0))

dm = sp.Matrix([[sr(A[i].get(j, F(0))) for i in dual_support] +
                [sr(e.get(j, F(0))) for e in E] for j in support])
db = sp.Matrix([sr(c[j]) for j in support])
dset = sp.linsolve((dm, db))
assert len(dset) == 1, "Numerical dual support does not admit exact stationarity."
dsol = next(iter(dset))
assert all(v.is_Rational and not v.free_symbols for v in dsol), "Exact dual on returned support is not unique."
y = [F(0)] * M
for i, v in zip(dual_support, dsol[:len(dual_support)]):
    y[i] = fr(v)
eta = [fr(v) for v in dsol[len(dual_support):]]
assert len(eta) == Q and all(v >= 0 for v in y)
residual = [c[j] - sum((y[i] * A[i].get(j, F(0)) for i in dual_support), F(0))
            - sum((eta[k] * E[k].get(j, F(0)) for k in range(Q)), F(0)) for j in range(N)]
assert all(r >= 0 for r in residual), [(j, str(r)) for j, r in enumerate(residual) if r < 0]
dualobj = sum((yi * bi for yi, bi in zip(y, b)), F(0)) + sum((v * eh for v, eh in zip(eta, h)), F(0))
assert dualobj == W
assert all(s * yi == 0 for s, yi in zip(slacks, y))
assert all(r * zj == 0 for r, zj in zip(residual, z))

atoms = inp["atom_columns"]
payoffs = [sum((z[v["index"]] * F(v["a"][i], sum(v["a"])) for v in atoms if sum(v["a"])), F(0)) for i in range(6)]
sizes = [sum((z[v["index"]] * (v["a"] + [v["x"], v["c"]])[i] for v in atoms), F(0)) for i in range(8)]
FX = sum((z[v["index"]] * F(v["x"], 1 + sum(v["a"][:4])) for v in atoms), F(0))
den = lcm(*(v.denominator for v in z))
baseline = F(688930071678645080978179164614013566510285979581569,
             1564818589840432726302471545016752331710657348785374)
assert W >= baseline
scales = [F(v) for v in disc["raw_row_divisors"]]
normalization_checks = [
    {"raw_index": i, "name": rows[i]["name"], "positive_divisor": str(scales[i]),
     "exact_raw_weight": str(y[i]), "exact_scaled_weight": str(y[i] * scales[i]),
     "returned_scaled_weight": -disc["inequality_marginals_scaled"][i],
     "scaled_weight_numeric_error": float(y[i] * scales[i]) + disc["inequality_marginals_scaled"][i]}
    for i in dual_support]
cert = {
    "schema": "visible_maximum_joint_exact_certificate_v1",
    "claim": "Exact optimum of the full 512-type necessary projection and a universal coverage lower bound; no SPE realization claim.",
    "input_sha256": INPUT_SHA, "optimizer_calls": 1,
    "variables": N, "raw_inequalities": M, "equality_count": Q,
    "objective": str(W), "objective_decimal": float(W), "half_gap": str(F(1, 2) - W),
    "primal": [str(v) for v in z], "K": str(z[512]),
    "common_denominator": str(den),
    "integer_scaled_primal": {str(j): str(z[j] * den) for j in support},
    "primal_support": support,
    "dual": {"convention": "raw A z >= b; E z = h; y>=0, eta free; r=c-A^T y-E^T eta>=0",
        "raw_row_weights": [str(v) for v in y],
        "equality_multipliers": [str(v) for v in eta],
        "equality_names": [e["name"] for e in inp["equalities"]],
        "objective": str(dualobj), "affine_inequality_rhs_payment": str(sum((yi * bi for yi, bi in zip(y, b)), F(0))),
        "equality_rhs_payment": str(sum((v * eh for v, eh in zip(eta, h)), F(0))),
        "nonnegative_column_residual": [str(v) for v in residual],
        "positive_raw_indices": dual_support,
        "positive_raw_rows": [{"index": i, "name": rows[i]["name"], "family": rows[i]["family"], "weight": str(y[i]), "rhs": str(b[i])} for i in dual_support]},
    "raw_row_slacks": [str(v) for v in slacks],
    "equality_residuals": [str(v) for v in eqres],
    "active_raw_indices": [i for i, v in enumerate(slacks) if not v],
    "recovery": {"method": "Exact symbolic linear solves on the sole returned positive primal/dual supports and active rows; no optimizer.",
        "positive_primal_columns": support, "numeric_active_raw_rows": tight,
        "primal_restricted_rank": int(pm.rank()), "primal_unknown_count": len(support),
        "positive_dual_raw_indices": dual_support, "dual_restricted_rank": int(dm.rank()),
        "dual_unknown_count": len(dual_support) + Q,
        "max_primal_numeric_error": max(abs(float(z[j]) - disc["x"][j]) for j in range(N)),
        "max_equality_multiplier_numeric_error": max(abs(float(eta[k]) - disc["equality_marginals"][k]) for k in range(Q)),
        "scaled_to_raw_rule": "y_raw = y_scaled / prepared_positive_divisor; y_scaled=-SciPy inequality marginal.",
        "positive_weight_scaling_checks": normalization_checks},
    "derived": {"sizes_A1_A6_X_C": [str(v) for v in sizes], "u1_u6": [str(v) for v in payoffs], "F_X": str(FX),
        "outside_O_mass": str(sum((z[v["index"]] for v in atoms if not v["o"]), F(0))),
        "actual_load_mass": {str(load): str(sum((z[v["index"]] for v in atoms if sum(v["a"]) == load), F(0))) for load in range(7)},
        "C_actual_joint_mass": {str(a) + str(cc): str(sum((z[v["index"]] for v in atoms if bool(sum(v["a"])) == bool(a) and v["c"] == cc), F(0))) for a in [0, 1] for cc in [0, 1]},
        "C_X_joint_mass": {str(x) + str(cc): str(sum((z[v["index"]] for v in atoms if v["x"] == x and v["c"] == cc), F(0))) for x in [0, 1] for cc in [0, 1]}},
    "prior_constructed_universal_bound": str(baseline), "improvement_over_prior_bound": str(W - baseline),
    "scope_boundary": "The feasible cone contains necessary projections of complete ordered pure SPEs. A rational primal point proves cone sharpness only. Original six-player half remains OPEN."
}
dump(HERE / "exact_certificate.json", cert)
with (HERE / "all1002_raw_row_checks.tsv").open("w") as out:
    out.write("raw_index\tname\tfamily\trhs\tprimal_slack\traw_dual_weight\tcomplementarity\n")
    for i, row in enumerate(rows):
        out.write(f"{i}\t{row['name']}\t{row['family']}\t{b[i]}\t{slacks[i]}\t{y[i]}\t{slacks[i] * y[i]}\n")
with (HERE / "all513_column_checks.tsv").open("w") as out:
    out.write("column\tbits_or_K\tprimal\tcost\tdual_residual\tcomplementarity\n")
    for j in range(N):
        bits = format(j, "09b") if j < 512 else "K"
        out.write(f"{j}\t{bits}\t{z[j]}\t{c[j]}\t{residual[j]}\t{residual[j] * z[j]}\n")
summary = {"status": "PASS_EXACT_PRIMAL_DUAL", "input_sha256": INPUT_SHA,
    "objective": str(W), "objective_decimal": float(W), "half_gap": str(F(1, 2) - W),
    "K": str(z[512]), "K_decimal": float(z[512]),
    "positive_atoms": len([j for j in support if j < 512]), "positive_raw_rows": len(dual_support),
    "all_raw_rows_checked": M, "all_columns_checked": N, "equalities_checked": Q,
    "primal_rank": int(pm.rank()), "dual_rank": int(dm.rank()),
    "zero_dual_residual_columns": [j for j, v in enumerate(residual) if not v],
    "positive_dual_rows": cert["dual"]["positive_raw_rows"], "equality_multipliers": cert["dual"]["equality_multipliers"],
    "improvement_over_prior_bound": str(W - baseline), "improvement_decimal": float(W - baseline),
    "optimizer_calls": 1, "new_optimizer_calls_in_recovery": 0}
dump(HERE / "exact_recovery_summary.json", summary)
print(json.dumps(summary, indent=2))
