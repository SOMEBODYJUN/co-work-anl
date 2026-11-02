"""Inspect a fully saved successful exact audit without re-running its matrix.

No imports from original producers/auditors, no NumPy/SciPy, no LP or SPE solver.
Checks every saved mass/slack, input bindings, complete named row set, atom domain,
W/O arithmetic, and the 9525 alignment count by binomial coefficients.
It does not independently recompute the 64 x 1284 coefficient matrix.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations_with_replacement, product
from math import comb, isfinite
from pathlib import Path
import hashlib
import json
import platform
import sys


def read(path):
    def pairs(items):
        out = {}
        for k, v in items:
            assert k not in out, f"duplicate JSON key {k}"
            out[k] = v
        return out
    def invalid(s):
        raise ValueError(s)
    return json.loads(path.read_text(), object_pairs_hook=pairs, parse_constant=invalid)


def integer(x, minimum=0):
    assert isinstance(x, int) and not isinstance(x, bool) and x >= minimum
    return x


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if len(sys.argv) != 4:
        raise SystemExit("usage: inspect_saved.py ORIGINAL_DIRECTORY EXISTING_64_ATOM_JSON OUTPUT_JSON")
    original, atom_path, output = map(Path, sys.argv[1:])
    primal_path = original / "cross_family_closure.json"
    verified_path = original / "verified_cross_family_closure.json"
    generator_path = original / "cross_family_closure.py"
    primal, verified, source = read(primal_path), read(verified_path), read(atom_path)
    assert set(primal) == {"scope", "is_SPE_counterexample", "row_count", "floating_success",
                          "floating_optimum", "exact_primal_value", "exact_reweighting",
                          "minimum_primal_slack", "exact_gap_above_two",
                          "positive_atom_count", "exact_optimality_verified"}
    assert set(verified) == {"scope", "is_SPE_counterexample", "source_atoms", "positive_atoms",
                            "row_count", "direct_cross_rows_per_atom", "conditional_rows_per_atom",
                            "enumerated_conditional_alignments", "welfare", "comparison_cover",
                            "gap_above_two", "minimum_slack", "zero_slack_count", "negative_slacks",
                            "source_sha256", "primal_sha256", "generator_sha256", "slacks"}
    assert primal["scope"] == ("fixed original 64-atom support only; old 447 rows plus "
                              "cross-family indexed-menu K and all-menu-pair last-two rows "
                              "and conditional diagonal/off-diagonal K rows")
    assert verified["scope"] == "exact obstruction to the stated 1284-row necessary-condition system only"
    assert primal["is_SPE_counterexample"] is verified["is_SPE_counterexample"] is False
    assert primal["floating_success"] is True
    assert primal["exact_optimality_verified"] is False
    assert primal["row_count"] == verified["row_count"] == 1284
    assert verified["source_sha256"] == sha(atom_path)
    assert verified["primal_sha256"] == sha(primal_path)
    assert verified["generator_sha256"] == sha(generator_path)
    atoms = source["primal"]["atoms"]
    assert len(atoms) == integer(verified["source_atoms"]) == 64
    mass = [F(x) for x in primal["exact_reweighting"]]
    assert len(mass) == 64 and min(mass) == 0
    assert sum(x > 0 for x in mass) == primal["positive_atom_count"] == verified["positive_atoms"] == 39

    # Build structural data only: no IC coefficient function is evaluated.
    total_alignments = 0
    per_atom = []
    for index, atom in enumerate(atoms):
        assert set(atom) == {"bits", "AB_hist", "AE_hist", "second_hist", "menus_lh", "mass_numerator"}
        assert len(atom["bits"]) == 10 and set(atom["bits"]) <= {"0", "1"}
        integer(atom["mass_numerator"], 1)
        family_data = {}
        marginals = []
        for tag, field, arity in [("AB", "AB_hist", 3), ("AE", "AE_hist", 3), ("S", "second_hist", 4)]:
            hist = atom[field]
            assert len(hist) == 2 ** arity and sum(map(integer, hist)) == 5
            types = tuple(product((0, 1), repeat=arity))
            data = tuple(ty for ty, n in zip(types, hist) for _ in range(n))
            assert len(data) == 5
            family_data[tag] = data
            marginals.append(sum(ty[0] for ty in data))
        assert len(set(marginals)) == 1
        d = marginals[0]
        assert len(atom["menus_lh"]) == 3
        for tag, pair in zip(("Lact", "Lsec", "Lthird"), atom["menus_lh"]):
            assert len(pair) == 2
            ell, h = map(integer, pair)
            assert h <= d and 0 <= ell - h <= 5 - d
            data = ((0, 0),) * (5 - d - ell + h) + ((0, 1),) * (ell - h)
            data += ((1, 0),) * (d - h) + ((1, 1),) * h
            assert len(data) == 5
            family_data[tag] = data
        menus = []
        for tag, data in family_data.items():
            for pos in range(1, len(data[0])):
                counts = tuple(sum(ty[pos] for ty in data if ty[0] == t) for t in (0, 1))
                menus.append((tag, counts))
        assert len(menus) == 10
        alignments = 0
        for tag, data in family_data.items():
            group_sizes = tuple(sum(ty[0] == t for ty in data) for t in (0, 1))
            for _pos in range(1, len(data[0])):
                for target, counts in menus:
                    n = 1 if target == tag else comb(group_sizes[0], counts[0]) * comb(group_sizes[1], counts[1])
                    alignments += n
        total_alignments += alignments
        per_atom.append({"index": index, "bits": atom["bits"], "shared_t_count": d,
                         "new_mass": str(mass[index]), "structural_alignments": alignments,
                         "all_atom_fields_checked": True})
    assert total_alignments == integer(verified["enumerated_conditional_alignments"]) == 9525

    W = sum((x * int(any(map(int, a["bits"][:5]))) for x, a in zip(mass, atoms)), F(0))
    O = sum((x * int(sum(n * ty[0] for n, ty in zip(a["AB_hist"], product((0, 1), repeat=3))) > 0)
             for x, a in zip(mass, atoms)), F(0))
    assert W == F(verified["welfare"]) == 1
    assert O == F(verified["comparison_cover"]) == F(primal["exact_primal_value"]) > 2
    gap = O - 2 * W
    assert gap == F(primal["exact_gap_above_two"]) == F(verified["gap_above_two"]) > 0
    assert isinstance(primal["floating_optimum"], (float, int)) and isfinite(primal["floating_optimum"])
    assert abs(float(O) - primal["floating_optimum"]) < 1e-12

    base_names = source["primal"]["rows"]
    assert len(base_names) == len(set(base_names)) == 437
    offdiag_names = [f"{tag}:5:offdiag:{pos}" for tag, arity in [("AB", 3), ("AE", 3), ("Sbranch", 4)] for pos in range(arity)]
    menus = [f"{tag}{pos}" for tag, arity in [("AB", 3), ("AE", 3), ("S", 4)] for pos in range(arity)]
    menus += ["Lact", "Lsec", "Lthird"]
    assert len(menus) == 13
    cross_names = []
    for tag, arity in [("AB", 3), ("AE", 3), ("S", 4)]:
        cross_names += [f"cross:{tag}:{pos}:K:{menu}" for pos in range(1, arity) for menu in menus]
        cross_names += [f"cross:{tag}:r2:{left}:{right}" for left, right in combinations_with_replacement(menus, 2)]
    for tag in ("actual", "second", "third"):
        cross_names += [f"cross:{tag}:r2:{left}:{right}" for left, right in combinations_with_replacement(menus, 2)]
    conditional_menus = [f"{tag}{pos}" for tag, arity in [("AB", 3), ("AE", 3), ("S", 4),
                                                         ("Lact", 2), ("Lsec", 2), ("Lthird", 2)]
                         for pos in range(1, arity)]
    conditional_names = []
    for tag, arity in [("AB", 3), ("AE", 3), ("S", 4), ("Lact", 2), ("Lsec", 2), ("Lthird", 2)]:
        for pos in range(1, arity):
            for menu in conditional_menus:
                conditional_names += [f"conditional:{tag}:{pos}:diag:{menu}",
                                      f"conditional:{tag}:{pos}:offdiag:{menu}"]
    assert len(cross_names) == verified["direct_cross_rows_per_atom"] == 637
    assert len(conditional_names) == verified["conditional_rows_per_atom"] == 200
    expected = base_names + offdiag_names + cross_names + conditional_names
    assert len(expected) == len(set(expected)) == 1284
    slacks = {key: F(value) for key, value in verified["slacks"].items()}
    assert set(slacks) == set(expected) and len(slacks) == 1284
    assert min(slacks.values()) == F(verified["minimum_slack"]) == F(primal["minimum_primal_slack"]) == 0
    assert sum(x == 0 for x in slacks.values()) == verified["zero_slack_count"] == 57
    assert verified["negative_slacks"] == {} and all(x >= 0 for x in slacks.values())
    groups = {"base": base_names, "old_offdiagonal": offdiag_names,
              "cross": cross_names, "conditional": conditional_names}
    result = {
        "scope": "Inspection and binding of an existing complete exact success; not a second matrix implementation.",
        "python": platform.python_version(),
        "primary_sha256": {q.name: sha(q) for q in sorted(original.iterdir())},
        "support_sha256": sha(atom_path),
        "source_atoms_fully_checked": 64, "rational_masses_read": 64,
        "positive_masses": 39, "zero_mass_indices": [i for i, x in enumerate(mass) if x == 0],
        "welfare": str(W), "comparison_cover": str(O), "gap_above_two": str(gap),
        "saved_rational_slacks_read": 1284, "zero_slacks": 57, "negative_saved_slacks": 0,
        "named_row_set_complete": True,
        "saved_order_matches_expected_order": list(verified["slacks"]) == expected,
        "row_groups": {key: {"rows": len(names), "zero_saved_slacks": sum(slacks[n] == 0 for n in names),
                             "minimum_saved_slack": str(min(slacks[n] for n in names))}
                       for key, names in groups.items()},
        "alignment_count_by_binomials": total_alignments,
        "atom_records": per_atom,
        "saved_report_fields_read": sorted(verified), "primal_fields_read": sorted(primal),
        "binding_checks": {"support": True, "primal": True, "generator": True},
        "historical_report_does_not_bind": ["audit-program SHA", "argv", "Python/library versions", "process stdout/stderr"],
        "reused_success": "original/verified_cross_family_closure.json",
        "coefficient_matrix_recomputed": False,
        "original_LP_runs": 0, "original_audit_entry_runs": 0, "new_optimization_calls": 0,
    }
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"atoms": 64, "positive": 39, "slacks_read": 1284, "zero_slacks": 57,
                      "alignments_by_count": total_alignments, "W": str(W), "O": str(O),
                      "input_bindings": "all_match", "original_entry_runs": 0}))


if __name__ == "__main__":
    main()
