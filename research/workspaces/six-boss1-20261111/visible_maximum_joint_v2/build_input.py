#!/usr/bin/env python3
"""Prepare exactly one full-domain row extension; standard-library exact arithmetic only."""
from copy import deepcopy
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import shutil

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
REPO = HERE.parents[3]
OLD = BASE / "visible_maximum_joint"
RESULT = BASE / "visible_maximum_joint_solve"
MAIN = BASE / "main_source2_maximum_nested_safe"
OLD_SHA = "b0610bb00298a4ee953423a8066dab050cb9d515fd6d5dde41f5117116f2ba33"
CERT_SHA = "8dd66c5c1cd3d729d262b64d6874ca9c7090952f0100c97d5ccc5397c6465347"
ROW_SHA = "a852e9f8c16fa8fd8a2785034d220de1b90193036d1d4ceb9d0fe431481cd4ba"
MAIN_MANIFEST_SHA = "3bdfeadb2ad2a48a2f9e0452bdb35dc4fe9002ec86d5aa9679950ca49188f269"
NAME = "SOURCE2_MAXIMUM_C_NESTED_SOURCE5_SAFE"
sha = lambda p: sha256(p.read_bytes()).hexdigest()

def dump(name, value):
    target = HERE / name
    assert not target.exists(), (name, "Preserve preparation outputs; do not overwrite.")
    target.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")

assert not (HERE / "freeze_manifest.json").exists()
assert sha(OLD / "exact_input.json") == OLD_SHA
assert sha(RESULT / "exact_certificate.json") == CERT_SHA
assert sha(MAIN / (NAME + ".json")) == ROW_SHA
assert sha(MAIN / "manifest.json") == MAIN_MANIFEST_SHA
old = json.loads((OLD / "exact_input.json").read_text())
row = json.loads((MAIN / (NAME + ".json")).read_text())
scaling = json.loads((OLD / "numerical_scaling.json").read_text())
assert old["variables"] == 513 and len(old["raw_rows"]) == 1002
assert len(old["equalities"]) == 2 and old["nonnegative_columns"] == list(range(513))
assert row["name"] == NAME and row["rhs"] == "0" and row["numerical_divisor"] == "300"
assert len(row["a"]) == 513 and set(row["a"]) == set(map(str, range(513)))

source_pins = json.loads((OLD / "source_pins.json").read_text())["sources"]
additional = [OLD / n for n in ["exact_input.json", "numerical_scaling.json", "source_review.md", "freeze_manifest.json", "independent_precheck_result.json", "column_routing.json", "column_routing.tsv"]]
additional += [RESULT / n for n in ["exact_certificate.json", "optimal_face.json", "freeze_manifest.json", "proof.md", "independent_check_result.json"]]
additional += [BASE / n for n in ["main_visible_c_certificate_check.py", "main_visible_c_certificate_check.json"]]
additional += list(sorted(MAIN.iterdir()))
for path in additional:
    assert path.is_file()
    source_pins[str(path.relative_to(REPO))] = sha(path)
for relative, expected in source_pins.items():
    assert sha(REPO / relative) == expected, relative
source_manifest = json.loads((MAIN / "manifest.json").read_text())
for filename, expected in source_manifest["artifacts"].items():
    assert sha(MAIN / filename) == expected, filename
for entry in source_manifest["sources"]:
    assert sha(REPO / entry["path"]) == entry["sha256"]
dump("source_pins.json", {"status": "PREPARED_NO_OPTIMIZER", "sources": source_pins,
     "pinned_by_assignment": {"baseline_full1002_input": OLD_SHA, "baseline_certificate": CERT_SHA,
                              "new_universal_raw_row": ROW_SHA, "Main_new_proof_manifest": MAIN_MANIFEST_SHA}})

# Independent literal reconstruction of all 128 state costs and all eight minima.
theta = F(5, 12)
state_checks, minimum_checks = [], []
source_states = json.loads((MAIN / "hidden_state_checks.json").read_text())
source_minima = json.loads((MAIN / "minimum_table.json").read_text())
by_state = {(x["p"], x["c"], x["o"], tuple(x["r"])): x for x in source_states}
by_type = {(x["p"], x["c"], x["o"]): x for x in source_minima}
assert len(by_state) == 128 and len(by_type) == 8
for p, c, o in product([0, 1], repeat=3):
    B, M, N = F(c, p + 5), F(o, 6 * (p + 4*c + 1)), F(o, 6 * (p + 3*c + 2))
    expected = F(5*c, 2) + 24*B + M + theta*(N - F(c, 5))
    values, zeros = [], []
    for rr in product([0, 1], repeat=4):
        r3, r4, r5, r6 = rr
        load = p + c + r3 + r4 + r5 + r6
        numerator = 25*c - r6 - theta*r5
        assert load or numerator == 0
        part = numerator / load if load else F(0)
        cost = part + F(r3+r4+r5, 2) + r6 + F(o, 6*(p+c+r3+r4+r5+1)) + F(5*o, 72*(p+c+r3+r4+2))
        residual = cost - expected
        assert residual >= 0
        frozen = by_state[(p, c, o, rr)]
        assert cost == F(frozen["cost"]) and expected == F(frozen["minimum"]) and residual == F(frozen["residual"])
        state_checks.append({"p": p, "c": c, "o": o, "r": list(rr), "cost": str(cost), "minimum": str(expected), "residual": str(residual)})
        values.append(cost)
        if residual == 0:
            zeros.append(list(rr))
    assert min(values) == expected
    assert expected == F(by_type[(p,c,o)]["minimum"]) and zeros == by_type[(p,c,o)]["zero_states"]
    minimum_checks.append({"p": p, "c": c, "o": o, "minimum": str(expected), "zero_states": zeros})

menu_count, menu_minimum = 0, F(0)
for p, c in product([0, 1], repeat=2):
    for rr in product([0, 1], repeat=4):
        r3, r4, r5, r6 = rr
        D6, D5 = p+c+r3+r4+r5+1, p+c+r3+r4+2
        for query in product([0, 1], repeat=6):
            d, o = sum(query), int(any(query))
            literal = sum((F(q, D6) + theta*F(q, D5) for q in query), F(0))/6
            projected = F(o, 6*D6) + theta*F(o, 6*D5)
            difference = F(d-o, 6)*(F(1, D6) + theta*F(1, D5))
            assert literal - projected == difference >= 0
            menu_count += 1
            menu_minimum = min(menu_minimum, difference)
assert menu_count == 4096

# Rebuild the new full row from the definition, without any primal/support data.
new_coefficient_checks = []
for j in range(512):
    bits = tuple((j >> bit) & 1 for bit in range(8, -1, -1))
    actual, x, o, c = bits[:6], bits[6], bits[7], bits[8]
    p, load = actual[0], sum(actual)
    u2 = F(actual[1], load) if load else F(0)
    B, M, N = F(c, p+5), F(o, 6*(p+4*c+1)), F(o, 6*(p+3*c+2))
    value = 300*u2 - 288*B - 12*M - 5*N
    minimum = F(5*c, 2) + 24*B + M + theta*(N-F(c, 5))
    assert value == 12*(25*u2-minimum) + 29*c
    assert row["a"][str(j)] == str(value)
    expected_atom = old["atom_columns"][j]
    assert expected_atom["index"] == j and expected_atom["a"] == list(actual)
    assert [expected_atom["x"], expected_atom["o"], expected_atom["c"]] == [x,o,c]
    new_coefficient_checks.append({"column": j, "bits": list(bits), "coefficient": str(value)})
assert row["a"]["512"] == "1"
new_coefficient_checks.append({"column": 512, "role": "K", "coefficient": "1"})
dump("new_row_checks.json", {"status": "PASS", "optimizer_calls": 0, "source_row_sha256": ROW_SHA,
     "hidden_state_checks": state_checks, "minimum_checks": minimum_checks,
     "literal_six_query_membership_checks": menu_count, "minimum_menu_difference": str(menu_minimum),
     "all513_new_coefficients": new_coefficient_checks,
     "C_size_elimination_identity": "new row = 12*(25u2+5K/2-sum(minPsi)) + 29*(sum(c)-K)"})

new_scaling = deepcopy(scaling)
assert new_scaling["raw_order"] == [r["name"] for r in old["raw_rows"]]
assert NAME not in new_scaling["raw_scales"]
new_scaling["raw_order"].append(NAME)
new_scaling["raw_scales"][NAME] = "300"
new_scaling["scope"] = "Unscaled exact input; all1002 inherited positive divisors literal, appended universal row divisor300. Future numeric consumer requires Main explicit release."
new_scaling["v2_append"] = {"raw_index": 1002, "name": NAME, "positive_divisor": "300"}
dump("numerical_scaling.json", new_scaling)

keys = ["variables", "bit_order", "atom_columns", "K_column", "nonnegative_columns", "objective", "equalities", "equality_count", "inequality_convention"]
new = {key: deepcopy(old[key]) for key in keys}
new.update({
    "schema": "visible_maximum_joint_v2_exact_v1", "status": "PREPARED_NO_OPTIMIZER", "optimizer_calls": 0,
    "scope": "All512 full(a1..a6,x,o,c) types and independent K; full1002 necessary cone copied literally plus exactly one universal source2 maximum-C/internal-source5 SAFE row.",
    "raw_inequality_count": 1003,
    "raw_row_policy": "Literal inherited1002 raw rows in original order, including zero/duplicate rows and all stored coefficient strings/metadata; exactly one appended frozen Main row. No pruning or scaling of exact input.",
    "raw_rows": deepcopy(old["raw_rows"]) + [deepcopy(row)],
    "source_bindings": dict(deepcopy(old["source_bindings"]),
        baseline_full1002_input=OLD_SHA, baseline_full1002_certificate=CERT_SHA,
        nested_source5_row=ROW_SHA, nested_source5_manifest=MAIN_MANIFEST_SHA),
    "source_pins_sha256": sha(HERE / "source_pins.json"),
    "source_review_sha256": sha(HERE / "source_review.md"),
    "Main_append_increment": {"old_raw_count": 1002, "new_raw_count": 1003, "raw_index": 1002, "name": NAME,
        "original_scale": "300u2+K-288B-12M-5N", "numerical_positive_divisor": "300"},
    "preparation_only": {"optimization_authorized": False, "optimizer_calls_in_this_preparation": 0,
        "old_point_used_as_input": False, "old_support_used": False, "point_completion_performed": False,
        "SPE_sufficiency_claimed": False, "half_status": "OPEN", "future_release_owner": "Main"},
})
assert new["raw_rows"][:1002] == old["raw_rows"] and new["raw_rows"][1002] == row
for key in keys:
    assert new[key] == old[key]
dump("exact_input.json", new)

catalog = [{"raw_index": i, "name": r["name"], "family": r["family"], "rhs": r["rhs"],
            "stored_coefficient_entries": len(r["a"]), "numerical_divisor": new_scaling["raw_scales"][r["name"]],
            "source": "inherited_literal1002" if i < 1002 else "Main_universal_nested_source5"}
           for i, r in enumerate(new["raw_rows"])]
dump("row_catalog.json", catalog)
with (HERE / "row_catalog.tsv").open("x") as out:
    out.write("raw_index\tname\tfamily\trhs\tnumerical_divisor\tsource\n")
    for r in catalog:
        out.write("\t".join(str(r[k]) for k in ["raw_index", "name", "family", "rhs", "numerical_divisor", "source"]) + "\n")
for name in ["column_routing.json", "column_routing.tsv"]:
    assert not (HERE / name).exists()
    shutil.copyfile(OLD / name, HERE / name)
    assert sha(HERE / name) == sha(OLD / name)

# Diagnostic only, after the new input has already been built independently of all old primal/support data.
cert = json.loads((RESULT / "exact_certificate.json").read_text())
face = json.loads((RESULT / "optimal_face.json").read_text())
z = [F(v) for v in cert["primal"]]
point_value = sum((F(v)*z[int(j)] for j,v in row["a"].items()), F(0)) - F(row["rhs"])
face_base = F(0)
face_coeff = [F(0)] * len(face["parameters"])
for coordinate in face["coordinates"]:
    a = F(row["a"][str(coordinate["column"])])
    face_base += a * F(coordinate["constant"])
    for k, v in enumerate(coordinate["parameter_coefficients"]):
        face_coeff[k] += a * F(v)
expected_negative = F(-15981204499895866953854050884598865236619, 86426960107246755980438461555855802597096)
assert all(v == 0 for v in face_coeff)
assert face_base == point_value == expected_negative < 0
old_p25 = old["raw_rows"][927]
assert old_p25["name"] == "PORTFOLIO25_i2_TC_QOmean"
eqc = old["equalities"][1]
for j in range(513):
    if j < 512:
        atom = old["atom_columns"][j]
        residual_term = -5*F(atom["o"], 6*(atom["a"][0]+3*atom["c"]+2))
    else:
        residual_term = F(1)
    assert F(row["a"].get(str(j), "0")) == 12*F(old_p25["a"].get(str(j), "0")) + residual_term + 30*F(eqc["a"].get(str(j), "0"))
dump("old_face_diagnostic.json", {"status": "EXACT_STRICTLY_NEGATIVE_ON_ENTIRE_OLD_FACE", "optimizer_calls": 0,
     "diagnostic_only_not_input": True, "old_certificate_sha256": CERT_SHA, "old_face_sha256": sha(RESULT / "optimal_face.json"),
     "new_raw_row_sha256": ROW_SHA, "point_value": str(point_value), "entire_face_value": str(face_base),
     "entire_face_decimal": float(face_base), "face_parameter_coefficients": [str(v) for v in face_coeff],
     "full513_identity": "new row = 12*old raw927 P25(C,Omean) + (K-5N) + 30*(sum(c)-K)",
     "scope": "This separates the whole old cone-optimal face. It is not a new solve, a support restriction, or a new optimum claim."})

for relative, expected in source_pins.items():
    assert sha(REPO / relative) == expected, relative
dump("build_result.json", {"status": "PREPARED_NO_OPTIMIZER", "input_sha256": sha(HERE / "exact_input.json"),
     "raw_inequalities": 1003, "atom_columns": 512, "nonnegative_columns": 513, "equalities": 2,
     "old_raw_rows_preserved": 1002, "new_raw_rows": 1, "new_coefficient_checks": 513,
     "hidden_state_checks": 128, "exact_minima": 8, "literal_menu_checks": 4096,
     "old_full_column_checks": 1002*513, "optimizer_calls": 0,
     "sources_checked_unchanged": len(source_pins), "old_face_value": str(face_base)})
print((HERE / "build_result.json").read_text())
