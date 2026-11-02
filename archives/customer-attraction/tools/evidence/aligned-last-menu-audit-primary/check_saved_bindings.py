"""Bind three frozen primary files to already certified, same-byte evidence.

No original entry/import, payoff coefficient construction, LP, or SPE solver.
The new finite checks concern record identity, pairing cardinalities, and the
44 saved zero-row names, not a repeated 2396/1326 matrix certification.
"""
from collections import Counter
from fractions import Fraction as F
from math import comb
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
inputs = []


def read(path):
    raw = path.read_bytes()
    inputs.append(dict(path=str(path.relative_to(ROOT)), size=len(raw),
                       sha256=hashlib.sha256(raw).hexdigest()))
    return json.loads(raw)


manifest = read(HERE / "primary-manifest.json")
for entry in manifest:
    raw = (ROOT / entry["preserved_repo_path"]).read_bytes()
    assert len(raw) == entry["size"]
    assert hashlib.sha256(raw).hexdigest() == entry["sha256"]

audit = read(HERE / "original/independent_aligned_menu_audit.json")
tight = read(HERE / "original/tight_rows.json")
base = ROOT / "archives/customer-attraction/tools/evidence"
point = read(base / "added-six-boss3/original/enhanced_2396_exact_obstruction.json")
old = read(base / "global-indexed-reviews-boss3/input-and-exclusion-review.json")
old_event = read(base / "global-indexed-reviews-boss3/input-review-event.json")
internals = read(base / "added-six-boss3/replay/recovery-internals.json")
recovery_event = read(base / "added-six-boss3/replay/execution-record.json")
review = read(base / "global-indexed-reviews-boss3/replay/review_2396/output.json")

assert inputs[3]["sha256"] == "ce1f9d8b1036256b7e40e1eb5c990fdcc4f33c7fed3f2aa796bdf8245b9d0c4f"
assert old["inputs"][0]["sha256"] == inputs[3]["sha256"] == review["source_sha256"]
assert old_event["exit_code"] == 0 and old_event["output_sha256"] == inputs[4]["sha256"]
assert recovery_event["exit_code"] == 0 and recovery_event["output_file_bytes_equal"] is True
assert point["rows"] == review["rows"] == internals["rows"] == 2396
assert set(audit) == {"scope", "independence", "source", "true_history", "actual_reply",
                      "compared_legal_topic", "slack", "compatible_pairings_checked", "records"}
assert audit["source"] == "next_credible/enhanced_2396_exact_obstruction.json"
assert audit["true_history"] == ["A", "B", "E", "T_i"]
assert audit["actual_reply"] == "L_i^2" and audit["compared_legal_topic"] == "L_i^1"
assert audit["slack"] == old["later_L2_vs_L1"]["value"] and F(audit["slack"]) < 0
assert len(audit["records"]) == len(point["atom_masses"]) == 38
assert old["later_L2_vs_L1"]["negative"] and old["later_L2_vs_L1"]["projection_preserves_value"]

record_bindings = []
for i, (atom, record, saved) in enumerate(zip(point["atom_masses"], audit["records"],
                                            old["later_L2_vs_L1"]["all38_summands"])):
    assert set(record) == {"atom", "prefix_load", "optimal_membership_count", "coefficient",
                           "mass", "term", "compatible_pairings_checked"}
    assert record["atom"] == saved["atom"] == i
    assert record["mass"] == saved["mass"] == atom["mass"]
    assert record["prefix_load"] == saved["past_ABE_load"]
    assert record["coefficient"] == saved["coefficient"]
    assert record["term"] == saved["weighted"]
    # Count all compatible pairs; do not repeat their payoff evaluations.
    d = sum(atom["AB_hist"][4:])
    count = 1
    for ell, h in [atom["menus_lh"][2], atom["menus_lh"][1]]:
        assert 0 <= h <= d and 0 <= ell-h <= 5-d
        count *= comb(d, h) * comb(5-d, ell-h)
    assert record["optimal_membership_count"] == d
    assert record["compatible_pairings_checked"] == count
    record_bindings.append(dict(atom=i, d=d, compatible_pairings=count,
                                coefficient=record["coefficient"],
                                same_mass_coefficient_and_term_as_prior_exact_event=True))
assert sum(x["compatible_pairings"] for x in record_bindings) == audit["compatible_pairings_checked"] == 38

names = internals["row_names"]
slacks = internals["all_original_computed_slacks"]
assert len(names) == len(set(names)) == len(slacks) == 2396 and list(slacks) == names
assert len(tight) == len(set(tight)) == review["zero_slack_count"] == point["zero_slacks"] == 44
assert min(map(F, slacks.values())) == 0
zeros = [name for name, value in slacks.items() if F(value) == 0]
assert tight == zeros
boundaries = [(437, "old437"), (464, "off27"), (534, "cross70"),
              (1920, "full-tax1386"), (2196, "aligned-tax276"), (2396, "triple200")]
row_bindings = []
for name in tight:
    index = names.index(name)
    category = next(label for stop, label in boundaries if index < stop)
    row_bindings.append(dict(name=name, zero_based_row_index=index, category=category,
                             saved_exact_slack=slacks[name]))

result = dict(
    scope="saved-source/result binding; no new coefficient or original-entry replay",
    inputs=inputs, primary_files=3, primary_bytes=sum(x["size"] for x in manifest),
    records=dict(count=38, all_match_prior_exact_event=True, bindings=record_bindings,
                 pairing_total=38, all_d_equal_one=all(x["d"] == 1 for x in record_bindings),
                 all_pairings_unique=all(x["compatible_pairings"] == 1 for x in record_bindings),
                 coefficient_sign_counts=dict(Counter("negative" if F(r["coefficient"]) < 0 else
                     "positive" if F(r["coefficient"]) > 0 else "zero" for r in audit["records"]))),
    tight_rows=dict(count=44, order_and_set_equal_prior_exact_zero_rows=True,
                    category_counts=dict(Counter(r["category"] for r in row_bindings)),
                    bindings=row_bindings, list_has_no_numeric_coefficients_or_multipliers=True),
    reused_negative_slack=audit["slack"],
    not_claimed=["historical producer of tight_rows identified", "44 linearly independent rows",
                 "dual optimality", "complete SPE", "real OPT", "six-provider half"],
    original_aligned_audit_runs=0, original_recovery_runs=0,
    additional_2396_or1326_coefficient_replays=0, LP_or_SPE_solver_calls=0)
(HERE / "binding-check.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(dict(status="passed", primary_files=3, records=38, pairing_total=38,
                     tight_rows=44, categories=result["tight_rows"]["category_counts"],
                     original_entry_runs=0, coefficient_replays=0), ensure_ascii=False))
