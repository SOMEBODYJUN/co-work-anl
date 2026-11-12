"""Boss2 W5 CA-PIVOT: bounded independent rational substitution only.

No source module is imported. No LP, recovery, pricing, allrows, or SPE audit is
run. The old 2396 coefficient proof and the historical all-2408 exact check are
reused; this checks the twelve new formulas, saved identities, and provenance.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[3]
PKG = ROOT / "archives/customer-attraction/tools/evidence/common-pivot-sixty-five-primary"
OUT = Path(__file__).with_name("compare_exact.json")


def read(path):
    data = path.read_bytes()
    return json.loads(data), hashlib.sha256(data).hexdigest()


new, new_sha = read(PKG / "new-exact-event/new_exact_2408_point.json")
frozen, frozen_sha = read(PKG / "original/reopt_common_pivot.json")
hist, hist_sha = read(PKG / "related/common_pivot_2408_exact_obstruction.json")
old, old_sha = read(ROOT / "archives/customer-attraction/tools/evidence/R486-same-query-clique-20261101/enhanced_2396_exact_obstruction.json")
old_float, old_float_sha = read(ROOT / "archives/customer-attraction/tools/evidence/added-six-boss3/original/reopt_added_triple.json")
same_hist, same_hist_sha = read(ROOT / "archives/customer-attraction/tools/evidence/common-pivot-2408-primary/original/common_pivot_2408_exact_obstruction.json")
assert hist == same_hist and hist_sha == same_hist_sha
atoms = frozen["atoms"]
assert len(atoms) == len(new["point"]) == len(old["point"]) == 65
assert old_float["atoms"] == atoms
assert frozen["names"][:2396] == old_float["names"]
assert len(frozen["names"]) == len(set(frozen["names"])) == 2408
assert len(old_float["names"]) == 2396
assert new["frozen_input_sha256"] == frozen_sha
types3 = list(product((0, 1), repeat=3))
types4 = list(product((0, 1), repeat=4))
paths = ("ABCDE", "AEUVW", "ABEXY")
old_path_names = ("actual", "second", "third")
mass_new = list(map(F, new["point"]))
mass_old = list(map(F, old["point"]))
coefficients = []
for atom in atoms:
    assert len(atom["bits"]) == 10 and set(atom["bits"]) <= {"0", "1"}
    bits = dict(zip("ABCDEUVWXY", map(int, atom["bits"])))
    ds = []
    for key, types in (("AB_hist", types3), ("AE_hist", types3), ("second_hist", types4)):
        h = atom[key]
        assert len(h) == len(types) and sum(h) == 5
        assert all(isinstance(n, int) and n >= 0 for n in h)
        ds.append(sum(n * ty[0] for n, ty in zip(h, types)))
    assert ds[0] == ds[1] == ds[2]
    d = ds[0]
    assert len(atom["menus_lh"]) == 3
    for ell, h in atom["menus_lh"]:
        assert isinstance(ell, int) and isinstance(h, int)
        assert 0 <= h <= d and 0 <= ell - h <= 5 - d
    row = {}
    for r, path in enumerate(paths):
        p = sum(bits[k] for k in path[:3])
        den = (p + 1) * (p + 2)
        ell_r, h_r = atom["menus_lh"][r]
        for s in range(3):
            if r == s:
                continue
            ell_s, h_s = atom["menus_lh"][s]
            diag = F(ell_r - ell_s, p + 1) - F(h_r - h_s, den)
            off = F(4 * (ell_r - ell_s), p + 1) + F(d * ell_s - 4 * h_r - h_s, den)
            all_pairs = F(5 * (ell_r - ell_s), p + 1) + F(d * ell_s - 5 * h_r, den)
            assert diag + off == all_pairs
            row[f"common-pivot:{r}:diag-menu:{s}"] = diag
            row[f"common-pivot:{r}:off-menu:{s}"] = off
    coefficients.append(row)

names = list(coefficients[0])
assert frozen["names"][2396:] == names
old_sums = {n: sum((c[n] * x for c, x in zip(coefficients, mass_old)), F()) for n in names}
new_sums = {n: sum((c[n] * x for c, x in zip(coefficients, mass_new)), F()) for n in names}
assert new_sums == {n: F(x) for n, x in new["common_pivot_slacks"].items()}
assert new_sums == {n: F(x) for n, x in hist["new_row_slacks"].items()}
assert old_sums["common-pivot:2:diag-menu:1"] == -F(33962942532321286037391724417608677893, 2370629578513027021549656484975223155224)
assert old_sums["common-pivot:2:off-menu:1"] == -old_sums["common-pivot:2:diag-menu:1"]
assert [n for n in names if old_sums[n] < 0] == ["common-pivot:2:diag-menu:1"]
assert [n for n in names if new_sums[n] == 0] == ["common-pivot:2:diag-menu:1"]
assert all(v >= 0 for v in new_sums.values())
for mass, cert, target_field in ((mass_new, new, "objective"), (mass_old, old, "objective")):
    assert min(mass) == 0 and sum(x > 0 for x in mass) == 38
    w = sum(x for atom, x in zip(atoms, mass) if any(map(int, atom["bits"][:5])))
    o = sum(x for atom, x in zip(atoms, mass) if any(atom["AB_hist"][4:]))
    assert w == 1 and o == F(cert[target_field]) and o - 2 == F(cert["gap_above_two"])
    assert o > 2
assert [{**a, "mass": str(x)} for a, x in zip(atoms, mass_new) if x] == hist["atom_masses"]
assert [{**a, "mass": str(x)} for a, x in zip(atoms, mass_old) if x] == old["atom_masses"]
support_old = [i for i, x in enumerate(mass_old) if x]
support_new = [i for i, x in enumerate(mass_new) if x]
assert support_old == support_new == new["support_indices"]
assert sum(x != y for x, y in zip(mass_old, mass_new)) == 38
saved_slacks = {n: F(v) for n, v in new["all_slacks"].items()}
assert list(saved_slacks) == frozen["names"]
assert len(saved_slacks) == 2408 and min(saved_slacks.values()) == 0
assert sum(v == 0 for v in saved_slacks.values()) == 44
assert new["rows"] == hist["rows"] == 2408
assert new["normalization"] == hist["W"] == "1"
assert new["objective"] == hist["O"]
assert new["gap_above_two"] == hist["gap_above_two"]

# Read and pin every layout dependency without importing its potentially active
# top-level code. The old 437 primal is an import dependency, not the new mass.
deps, dep_manifest_sha = read(PKG / "dependency-manifest.json")
dependency_checks = []
for dep in deps:
    path = ROOT / dep["repo_saved_path"] if "repo_saved_path" in dep else PKG / dep["package_saved_path"]
    b = path.read_bytes()
    sha = hashlib.sha256(b).hexdigest()
    assert sha == dep["sha256"] and len(b) == dep["size"]
    dependency_checks.append({"path": str(path.relative_to(ROOT)), "sha256": sha, "bytes": len(b)})

report = {
    "task": "customer-attraction-3a-3a-d04519300404ec0e",
    "method": "standard-library-only independent twelve-formula substitution and complete saved-field/provenance checks",
    "original_program_calls": 0,
    "LP_calls": 0,
    "recovery_calls": 0,
    "allrows_calls": 0,
    "SPE_audit_calls": 0,
    "old_2396_coefficients_rederived": False,
    "saved_2408_slacks_recomputed": False,
    "saved_2408_slacks_parsed_and_checked": 2408,
    "twelve_new_slacks_recomputed_old_and_new": True,
    "old_float_atoms_equal_new_float_atoms": True,
    "old_names_are_exact_prefix_of_new": True,
    "candidate_columns": 65,
    "same_support_indices": support_new,
    "changed_positive_masses": 38,
    "zero_coordinates": 27,
    "new_O": new["objective"],
    "new_O_minus_2W": new["gap_above_two"],
    "new_W": "1",
    "new_saved_zero_slacks": 44,
    "new_slacks": {n: str(v) for n, v in new_sums.items()},
    "old_slacks": {n: str(v) for n, v in old_sums.items()},
    "old_allpairs_2_1": str(old_sums["common-pivot:2:diag-menu:1"] + old_sums["common-pivot:2:off-menu:1"]),
    "new_allpairs_2_1": str(new_sums["common-pivot:2:diag-menu:1"] + new_sums["common-pivot:2:off-menu:1"]),
    "old_2396_sha256": old_sha,
    "new_2408_point_sha256": new_sha,
    "historical_2408_sha256": hist_sha,
    "float_2408_sha256": frozen_sha,
    "float_2396_sha256": old_float_sha,
    "dependency_manifest_sha256": dep_manifest_sha,
    "dependency_checks": dependency_checks,
    "note": "Historical all-2408 coefficient verification is reused after reading its source and event. Parsing nonnegative saved slacks is not a new all-2408 coefficient audit."
}
OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({k: v for k, v in report.items() if k not in {"dependency_checks", "same_support_indices", "old_slacks", "new_slacks"}}, ensure_ascii=False, indent=2))
