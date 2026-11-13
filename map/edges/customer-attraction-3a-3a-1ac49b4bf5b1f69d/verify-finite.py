"""Exact, small audit of the assigned two relaxation points, not an SPE search.

The 235 baseline rows are rebuilt from the displayed CAP/COPY/SAFE/LAST/PAIR
formulae. No author generator or whole-cube verifier is imported. The second
point is used only for its explicit masses and five scalar cuts; its 3889 old
relations are deliberately not certified by this script.
"""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
BASE = ROOT / "archives/customer-attraction/tools/evidence/R-3002-batch-20261031"


def read(relative):
    return json.loads((BASE / relative).read_text())


def ref(relative):
    p = BASE / relative
    return {"path": str(p.relative_to(ROOT)),
            "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}


def main():
    point = read("source/baseline_exact_primal.json")
    certificate_names = ["baseline_o4.2", "o4.2", "third_L_o4.2",
                         "branch_D_o4.2", "L_D_o4.34514"]
    relatives = [f"research_4/root_requery_{s}_exact.json" for s in certificate_names]
    certificates = [read(s) for s in relatives]
    base = certificates[0]
    names, paths = base["names"], base["paths"]
    weights = {int(k): F(v) for k, v in point["weights"].items()}
    K, O = F(point["verification"]["K"]), F(point["verification"]["O"])
    assert all(w > 0 for w in weights.values())

    def bit(mask, label):
        return (mask >> names.index(label)) & 1

    def load(mask, path, end=6):
        return sum(bit(mask, a) for a in path[:end])

    def profit(path, position):
        return sum((w * bit(m, path[position]) / load(m, path)
                    for m, w in weights.items() if load(m, path)), F(0))

    def mass(label):
        return sum((w * bit(m, label) for m, w in weights.items()), F(0))

    v_T = profit(paths[0], 0)
    assert mass("T") == K
    assert v_T == F(point["verification"]["r"])
    row_slacks = {}
    for label in names[1:]:
        row_slacks[f"CAP:{label}"] = K - mass(label)
    for s, i, t in base["copy_edges"]:
        row_slacks[f"COPY:{s}:{i}:{t}"] = profit(paths[s], i) - profit(paths[t], i)
    for j, path in enumerate(paths):
        for i in range(base["first_genuine"][j], 6):
            for label in names:
                quote = sum((w * bit(m, label) / (load(m, path, i) + 6 - i)
                             for m, w in weights.items()), F(0))
                row_slacks[f"SAFE:{j}:{i}:{label}"] = profit(path, i) - quote
        last_tax = sum((w * load(m, path, 5) / (load(m, path, 5) + 1)
                        for m, w in weights.items()), F(0))
        row_slacks[f"LASTO:{j}"] = 6 * profit(path, 5) + last_tax - O
        pair_tax = sum((w * bit(m, path[4]) /
                        ((load(m, path, 4) + 1) * (load(m, path, 4) + 2))
                        for m, w in weights.items()), F(0))
        prefix_tax = sum((w * load(m, path, 4) / (load(m, path, 4) + 1)
                         for m, w in weights.items()), F(0))
        row_slacks[f"PAIRO:{j}"] = 3 * (profit(path, 4) + profit(path, 5) + pair_tax) + prefix_tax - O
    assert len(row_slacks) == 235 and min(row_slacks.values()) >= 0
    baseline_cuts = []
    for relative, certificate in zip(relatives, certificates):
        nu, D = certificate["multipliers_numerators"], certificate["denominator"]
        assert D > 0 and all(type(v) is int and v >= 0 for v in nu.values())
        alpha = F(sum(v for k, v in nu.items() if k.startswith(("LASTO:", "PAIRO:"))), D)
        beta = F(certificate["equality_numerator"] -
                 sum(v for k, v in nu.items() if k.startswith("CAP:")), D)
        assert alpha == F(certificate["verification"]["a"])
        assert beta == F(certificate["verification"]["beta"])
        baseline_cuts.append({"certificate": ref(relative), "alpha": str(alpha),
                              "beta": str(beta), "baseline_v_T_slack": str(v_T - alpha * O - beta * K)})
    assert baseline_cuts[2]["baseline_v_T_slack"] == point["verification"]["new_QL_row_residual"]

    joint = read("deps/root_rows_joint_point.json")
    cols = joint["certificate"]["columns"]
    assert all(F(c["weight"]) >= 0 for c in cols)
    lifted_K = sum((F(c["weight"]) for c in cols if c["kind"] == "K"), F(0))
    hist = [c for c in cols if c["kind"] == "hist"]
    lifted_W = sum((F(c["weight"]) for c in hist if "1" in c["actual_bits"]), F(0))
    lifted_r = sum((F(c["weight"]) * int(c["actual_bits"][0]) / c["actual_bits"].count("1")
                    for c in hist if "1" in c["actual_bits"]), F(0))
    assert lifted_W == F(joint["certificate"]["W"])
    lifted_slacks = [str(lifted_r - F(c["alpha"]) * F(joint["certificate"]["O"]) - F(c["beta"]) * lifted_K)
                     for c in baseline_cuts]
    assert lifted_slacks == joint["exact_verification"]["new_root_slacks"]
    assert 1 - 2 * lifted_W == F(joint["certificate"]["strict_half_gap"])
    families = Counter(k.split(":")[0] for k in row_slacks)
    zero_by_family = Counter(k.split(":")[0] for k, v in row_slacks.items() if v == 0)
    output = {
        "scope": "Exact arithmetic only on the specified 36 baseline types and the explicit lifted point; no SPE search, no whole membership cube rerun, no old 3889-row generator replay.",
        "baseline": {"input": ref("source/baseline_exact_primal.json"), "K": str(K), "O": str(O),
                     "types": len(weights), "T_mass_equals_K": True,
                     "v_T": str(v_T), "field_r_meaning": "formal baseline r equals forced-P0 first-player profit v_T; no original equilibrium root is supplied",
                     "row_count": len(row_slacks), "rows_by_family": dict(families),
                     "minimum_slack": str(min(row_slacks.values())),
                     "zero_rows": sum(v == 0 for v in row_slacks.values()),
                     "zero_rows_by_family": dict(zero_by_family),
                     "row_slacks": {k: str(v) for k, v in row_slacks.items()},
                     "scalar_cuts": baseline_cuts},
        "augmented": {"input": ref("deps/root_rows_joint_point.json"),
                      "columns_read": len(cols), "hist_mass_columns": len(hist),
                      "all_weights_nonnegative": True, "K": str(lifted_K),
                      "r_from_actual_bits": str(lifted_r), "W": str(lifted_W),
                      "one_half_minus_W": str(F(1, 2) - lifted_W),
                      "source_strict_half_gap_equals_one_minus_2W": str(1 - 2 * lifted_W),
                      "new_root_slacks": lifted_slacks,
                      "old_3889_rows_reverified": False, "full_SPE_verified": False},
        "logical_boundary": "The baseline point refutes only old-235-row implication of the QL scalar. It is not a counterexample to any bound quantified over complete pure SPE."
    }
    (HERE / "finite-audit.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"235_rows_nonnegative": True, "zero_rows": output["baseline"]["zero_rows"],
                      "baseline_cut_slacks": [x["baseline_v_T_slack"] for x in baseline_cuts],
                      "augmented_scalar_slacks_match": True}, indent=2))


if __name__ == "__main__":
    main()
