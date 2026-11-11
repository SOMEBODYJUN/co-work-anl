#!/usr/bin/env python3
"""Whole optimal face and true-branch diagnostics by exact algebra only."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json
import sympy as sp

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "visible_maximum_joint"
sha = lambda p: sha256(p.read_bytes()).hexdigest()
dump = lambda p, v: p.write_text(json.dumps(v, indent=2) + "\n")
sr = lambda f: sp.Rational(f.numerator, f.denominator)
fr = lambda s: F(int(s.p), int(s.q))
inp = json.loads((SOURCE / "exact_input.json").read_text())
cert = json.loads((HERE / "exact_certificate.json").read_text())
assert sha(SOURCE / "exact_input.json") == cert["input_sha256"]
rows = inp["raw_rows"]
atoms = inp["atom_columns"]
zpoint = list(map(F, cert["primal"]))
residual = list(map(F, cert["dual"]["nonnegative_column_residual"]))
allowed = [j for j, r in enumerate(residual) if r == 0]
positive_rows = cert["dual"]["positive_raw_indices"]
equations = inp["equalities"] + [rows[i] for i in positive_rows]
equation_names = [e["name"] for e in inp["equalities"]] + [rows[i]["name"] for i in positive_rows]
matrix = sp.Matrix([[sp.Rational(e["a"].get(str(j), "0")) for j in allowed] for e in equations])
rhs = sp.Matrix([sp.Rational(e["rhs"]) for e in equations])
rref, pivots = matrix.row_join(rhs).rref()
assert len(allowed) not in pivots
free_positions = [k for k in range(len(allowed)) if k not in pivots]
free_columns = [allowed[k] for k in free_positions]
P = len(free_positions)
constant = [F(0)] * len(allowed)
coeff = [[F(0)] * P for _ in allowed]
for k, f in enumerate(free_positions):
    coeff[f][k] = F(1)
for row, pivot in enumerate(pivots):
    constant[pivot] = fr(rref[row, -1])
    for k, f in enumerate(free_positions):
        coeff[pivot][k] = -fr(rref[row, f])
point_parameters = [zpoint[j] for j in free_columns]
assert all(constant[k] + sum((coeff[k][t] * point_parameters[t] for t in range(P)), F(0)) == zpoint[j]
           for k, j in enumerate(allowed))

def restrict(row, rhs_value=F(0)):
    av = [F(row.get(str(j), "0")) for j in allowed]
    base = sum((a * x for a, x in zip(av, constant)), F(0)) - rhs_value
    cs = [sum((a * coeff[k][t] for k, a in enumerate(av)), F(0)) for t in range(P)]
    return base, cs

def packed(base, cs):
    return {"constant": str(base), "parameter_coefficients": [str(v) for v in cs]}

raw_constraints = []
for i, row in enumerate(rows):
    b, cs = restrict(row["a"], F(row["rhs"]))
    assert b + sum((v * p for v, p in zip(cs, point_parameters)), F(0)) >= 0
    raw_constraints.append({"raw_index": i, "name": row["name"], **packed(b, cs)})

def fixed_identity(name, vector):
    base, cs = restrict(vector)
    assert all(v == 0 for v in cs), (name, cs)
    target = sp.Matrix([sp.Rational(vector.get(str(j), "0")) for j in allowed])
    solutions = sp.linsolve((matrix.T, target))
    assert len(solutions) == 1
    solution = next(iter(solutions))
    assert all(v.is_Rational for v in solution)
    weights = list(map(fr, solution))
    assert sum((v * F(e["rhs"]) for v, e in zip(weights, equations)), F(0)) == base
    return {"name": name, "value": str(base), "decimal": float(base),
            "signed_equation_weights": [str(v) for v in weights],
            "domain": "Only on the complementarity support; a signed equality identity, not a universal nonnegative payment."}

actual_size_vectors = [{str(v["index"]): str(v["a"][i]) for v in atoms if v["a"][i]} for i in range(6)]
Xvector = {str(v["index"]): str(v["x"]) for v in atoms if v["x"]}
Cvector = {str(v["index"]): str(v["c"]) for v in atoms if v["c"]}
U2vector = {str(v["index"]): str(F(v["a"][1], sum(v["a"]))) for v in atoms if sum(v["a"]) and v["a"][1]}
fixed = [fixed_identity("K", {"512": "1"}), fixed_identity("size_A1", actual_size_vectors[0]),
         fixed_identity("size_X", Xvector), fixed_identity("u2", U2vector)]
safe2index = next(i for i, row in enumerate(rows) if row["name"] == "SAFE_2_C")
fixed.append(fixed_identity("SAFE_2_C_slack", rows[safe2index]["a"]))
values = {x["name"]: F(x["value"]) for x in fixed}
K, A1, X, U2 = [values[key] for key in ["K", "size_A1", "size_X", "u2"]]
gapvector = {str(j): str(F(Xvector.get(str(j), "0")) / 4
                       + F(actual_size_vectors[0].get(str(j), "0")) / 20
                       - F(U2vector.get(str(j), "0")) - (F(1, 20) if j == 512 else F(0)))
             for j in range(513)}
gapidentity = fixed_identity("source3_X_uniform_strict_gap", gapvector)
fixed.append(gapidentity)
gap = F(gapidentity["value"])
assert gap > 0

support_implications = {
    "all_visible_roles_inside_O": all(v["o"] or not (sum(v["a"]) or v["x"] or v["c"]) for v in atoms if v["index"] in allowed),
    "A1_subset_C": all(not v["a"][0] or v["c"] for v in atoms if v["index"] in allowed),
    "A1_disjoint_X": all(not (v["a"][0] and v["x"]) for v in atoms if v["index"] in allowed),
    "X_subset_A5_union_A6": all(not v["x"] or v["a"][4] or v["a"][5] for v in atoms if v["index"] in allowed),
    "A5_disjoint_A6": all(not (v["a"][4] and v["a"][5]) for v in atoms if v["index"] in allowed),
    "A2_subset_A1_intersect_A3_intersect_C": all(not v["a"][1] or (v["a"][0] and v["a"][2] and v["c"]) for v in atoms if v["index"] in allowed),
}
assert all(support_implications.values())

face = {
    "status": "EXACT_WHOLE_OPTIMAL_FACE_PARAMETERIZATION", "input_sha256": cert["input_sha256"],
    "certificate_sha256": sha(HERE / "exact_certificate.json"), "optimizer_calls_in_this_script": 0,
    "objective": cert["objective"],
    "characterization": "A point is optimal iff columns outside zero_residual_columns are zero, positive-dual rows are tight, both equalities hold, and every original nonnegativity/raw inequality holds. The parameterization below solves all equality conditions exactly; all remaining inequalities are supplied, with no omission.",
    "zero_residual_columns": allowed, "forced_zero_columns": [j for j in range(513) if j not in allowed],
    "positive_dual_raw_indices": positive_rows, "equation_names": equation_names,
    "equation_rhs": [e["rhs"] for e in equations], "restricted_equation_rank": len(pivots),
    "unconstrained_affine_parameter_count": P,
    "parameters": [{"position": t, "name": "z" + str(j), "column": j} for t, j in enumerate(free_columns)],
    "coordinates": [{"column": j, **packed(constant[k], coeff[k])} for k, j in enumerate(allowed)],
    "nonnegative_coordinates_required": allowed,
    "raw_inequality_restrictions": raw_constraints,
    "nonconstant_raw_indices": [x["raw_index"] for x in raw_constraints if any(F(c) for c in x["parameter_coefficients"])],
    "point_parameters": [str(v) for v in point_parameters],
    "fixed_functionals": fixed, "support_implications": support_implications,
    "scope_note": "Rank gives a seven-parameter affine containing space. The exact feasible optimal face is that affine space intersected with all explicitly supplied inequalities; no claim that seven is its final affine dimension is needed."
}
dump(HERE / "optimal_face.json", face)

envelope = []
for p in [0, 1]:
    for q in [0, 1]:
        rho = F(5, 2) + F(24, p + 5) + F(q, p + 5)
        states = []
        for s in range(4):
            for last in [0, 1]:
                phi = F(25 - last, p + 1 + s + last) + F(s, 2) + last + F(q, p + s + 2)
                assert phi >= rho
                states.append({"s": s, "last": last, "Phi": str(phi), "rho": str(rho), "excess": str(phi - rho)})
        zeros = [[v["s"], v["last"]] for v in states if F(v["excess"]) == 0]
        assert zeros == ([[3, 1]] if p == 0 else [[3, 0], [3, 1]])
        envelope.append({"p": p, "q": q, "c": 1, "states": states, "zero_states": zeros})

delta = 30 * values["SAFE_2_C_slack"]
H = A1 - delta
terminalpay = (K - A1) / 5 + H / 6 + delta
assert 0 <= delta <= A1 and H >= 0
diagnostics = []
for i, vec in enumerate(actual_size_vectors + [Xvector, Cvector]):
    potential = {str(v["index"]): str(F(vec.get(str(v["index"]), "0")) / (v["a"][0] + 4 * v["c"] + 1)) for v in atoms}
    pb, pcs = restrict(potential)
    diagnostics.append({"target": "A" + str(i + 1) if i < 6 else ["X", "C"][i - 6],
                        "terminal_BR_slack": packed(terminalpay - pb, [-v for v in pcs]),
                        "point_slack": str(terminalpay - sum((F(a) * zpoint[int(j)] for j, a in potential.items()), F(0)))})

source_safe = []
for source, c_mult, free_count in [(3, 1, 4), (4, 2, 3), (5, 3, 2)]:
    for i, vec in enumerate(actual_size_vectors + [Xvector]):
        potential = {str(v["index"]): str(F(vec.get(str(v["index"]), "0")) / (v["a"][0] + c_mult * v["c"] + free_count)) for v in atoms}
        pb, pcs = restrict(potential)
        source_safe.append({"true_source": source, "target": "A" + str(i + 1) if i < 6 else "X",
                            "required_u2_minus_SAFE": packed(U2 - pb, [-v for v in pcs]),
                            "point_slack": str(U2 - sum((F(a) * zpoint[int(j)] for j, a in potential.items()), F(0)))})

diagnostic = {
    "status": "WHOLE_OPTIMAL_FACE_EXCLUDED_BY_TRUE_SOURCE3_X", "optimizer_calls_in_diagnostic": 0,
    "input_sha256": cert["input_sha256"], "certificate_sha256": sha(HERE / "exact_certificate.json"),
    "face_sha256": sha(HERE / "optimal_face.json"),
    "positive_row": {"raw_index": 927, "name": "PORTFOLIO25_i2_TC_QOmean", "weight": cert["dual"]["raw_row_weights"][927]},
    "literal_C_envelope_checks": envelope,
    "weak_tie_preserved": "For a1=1 and c=1, s=3 permits last=0 and last=1; no all-four-tail claim is made.",
    "equality_consequences": [
        "Positive P25C row is tight at every cone optimum.",
        "Its nonnegative real payments force source2 true IC equality, all three intermediate size caps tight, terminal size cap tight, all local minimum-envelope terms zero, and menu union weakening zero.",
        "Every C client has s=3, so B3,B4,B5 cover C. Since each has size K=|C|, their coverage equals C (their labels need not equal C).",
        "Hence at history (A1,C), true player3 chooses a label covering exactly C and has the same final payoff as forced player2, namely actual u2.",
        "Its legal deviation to X gives u2 >= sum_X 1/(a1+c+4).",
        "Optimal-face support forces A1 subset C and A1 disjoint X, so this is at least |X|/4-(K-|A1|)/20.",
        "The latter exceeds u2 by the positive exact gap below, uniformly across the entire face."
    ],
    "fixed_values": {key: str(value) for key, value in values.items()},
    "delta_A1_C_omitted_by_last": str(delta), "H_A1_C_retained_by_last": str(H),
    "terminal_payoff": str(terminalpay), "visible_terminal_BR_diagnostics": diagnostics,
    "true_intermediate_source_SAFE_diagnostics": source_safe,
    "uniform_strict_gap": str(gap), "uniform_strict_gap_decimal": float(gap),
    "universal_conclusion": "Every genuine finite-instance complete ordered pure SPE with OPT6>0 has W/OPT6 strictly greater than this cone optimum. This excludes exact attainment only; no quantified larger universal infimum follows from this face argument alone. Six-player half remains OPEN.",
    "no_model_mutation": "The new source3 inequality is used only under cone-equality consequences; it is not appended to or solved as a new numerical LP."
}
dump(HERE / "true_branch_equality_diagnostic.json", diagnostic)
print(json.dumps({"face_rank": len(pivots), "face_columns": len(allowed), "free_columns": free_columns,
                  "nonconstant_raw_constraints": len(face["nonconstant_raw_indices"]),
                  "strict_source3_X_gap": str(gap), "strict_gap_decimal": float(gap),
                  "fixed_values": {x["name"]: x["value"] for x in fixed}}, indent=2))
