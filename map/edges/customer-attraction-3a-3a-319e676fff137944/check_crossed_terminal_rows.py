"""Recompute specified terminal rows by literal label-preserving matching.

Run from any directory and capture stdout for the exact comparison JSON.
The previously certified base matrices and whole-domain pricing are reused.
"""

from fractions import Fraction as F
from itertools import product, permutations
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[3]
base = ROOT / "archives/customer-attraction/tools/evidence"
POINTS = {
    "717": (
        "round5-terminal-pricing-resumed-boss2/original/exact_optimum_primal_cross_pair.json",
        "27bc7b955495d9bb9041bfde7c3ec963d945a0d839f475c16fb498b1bf19230d",
        "round5-terminal-pricing-resumed-boss2/original/exact_dual_cross_pair.json",
        "bb7bb2047a5f4e77e3c91688da3a0476b269174c33a609bcfef4952e273a3e51",
        61,
    ),
    "727": (
        "load-signature-pricing-and-727-primal-primary/original/research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round5_pricing/exact_optimum_primal_terminal_cross.json",
        "e2caa8f504da61dd41c6980671f2ce3d0c715f5d4dcce4b16dd656af25363acb",
        "round5-terminal-pricing-resumed-boss2/original/exact_dual_terminal_cross.json",
        "5f94ca13805c654cd29f10ed8d75a942caad95a9e826bf49ce311676d6c3d18c",
        69,
    ),
    "728": (
        "round5-shared-matching-resumed-boss2/new-728-run/related/research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round5_pricing/exact_optimum_primal_joint_terminal.json",
        "b5ec102366191aea06e4a7a93073a7913bd625101c743cc5ccc8f9132d744b05",
        "round5-terminal-pricing-resumed-boss2/original/exact_dual_joint_terminal.json",
        "84ce8ccdcfec49c2c1cf50894f13710fb96fbd0be7e82810b8db5f4589239430",
        65,
    ),
    "737": (
        "dual-terminal-exact-resumed-boss2/original/exact_optimum_primal_dual_terminal.json",
        "1c7b256ee4e72c686bb8bb7db4ac2d199cc2890463bf7138cd2761f8756c62fd",
        "dual-terminal-exact-resumed-boss2/original/exact_dual_dual_terminal.json",
        "ad85b8a1aad07e9e2a5630fff0bd166e785440bb57d5d91f4f716c74725e122c",
        76,
    ),
}


def expand(hist, arity):
    assert len(hist) == 2**arity and all(type(n) is int and n >= 0 for n in hist)
    return [bits for bits, count in zip(product((0, 1), repeat=arity), hist) for _ in range(count)]

def decode(atom):
    assert set(atom) == {"bits", "AB_hist", "AE_hist", "second_hist", "menus_lh", "exact_mass"}
    bits = tuple(map(int, atom["bits"]))
    assert len(bits) == 10 and set(bits) <= {0, 1}
    fams = {name: expand(atom[name + "_hist"], arity)
            for name, arity in (("AB", 3), ("AE", 3), ("second", 4))}
    assert {len(family) for family in fams.values()} == {5}
    counts = {sum(t[0] for t in family) for family in fams.values()}
    assert len(counts) == 1
    d = counts.pop()
    assert len(atom["menus_lh"]) == 3
    assert all(0 <= h <= d and 0 <= ell-h <= 5-d for ell, h in atom["menus_lh"])
    mass = F(atom["exact_mass"])
    assert mass > 0
    return bits, fams, d, mass

def cross_row(bits, fams, source, target, components):
    prefix = bits[0] + bits[1 if source == "AB" else 4]
    src, tgt = fams[source], fams[target]
    denominator = [prefix + t + r + 1 for t, r, s in src]
    menu_sizes = {pos: sum(row[pos] for row in tgt) for pos, kind in components}
    total = F(0)
    for label in (0, 1):
        group = [i for i, row in enumerate(src) if row[0] == label]
        target_group = [row for row in tgt if row[0] == label]
        assert len(group) == len(target_group)
        coefficients = []
        for order in set(permutations(target_group)):
            score = F(0)
            for i, menu in zip(group, order):
                for pos, kind in components:
                    if kind == "D":
                        score += F(src[i][-1] - menu[pos], denominator[i])
                    else:
                        score += F(4*src[i][-1] - (menu_sizes[pos] - menu[pos]), denominator[i])
            coefficients.append(score)
        total += max(coefficients)
    return total

def name(source, target, pos, kind):
    return f"crossfinal:{source}:{'Sbranch' if target == 'second' else target}:{pos}{kind}"

ab_specs = [(name("AB", t, p, k), "AB", t, ((p,k),)) for t, arity in (("AE",3),("second",4))
            for p in range(1,arity) for k in ("D","O")]
ae_specs = [(name("AE", t, p, k), "AE", t, ((p,k),)) for t, arity in (("AB",3),("second",4))
            for p in range(1,arity) for k in ("D","O")]
joint_spec = ("jointfinal:AB:Sbranch:2O+3O", "AB", "second", ((2,"O"),(3,"O")))
ab_ae_joint_spec = ("AB:AE:1O+2O", "AB", "AE", ((1,"O"),(2,"O")))


def read_frozen(relative_path, sha):
    raw = (base / relative_path).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == sha, relative_path
    return json.loads(raw)


def main():
    reports = {}
    row_orders = {}
    objective = {}
    for n, (point_path, point_sha, dual_path, dual_sha, count) in POINTS.items():
        point = read_frozen(point_path, point_sha)
        dual = read_frozen(dual_path, dual_sha)
        atoms = [decode(atom) for atom in point["atoms"]]
        stored = {name: F(value) for name, value in point["slacks"].items()}
        assert len(atoms) == count
        assert len(stored) == point["row_count"] == dual["row_count"] == int(n)
        assert min(stored.values()) >= 0
        w = sum(mass * bool(any(bits[:5])) for bits, families, d, mass in atoms)
        o = sum(mass * bool(d) for bits, families, d, mass in atoms)
        assert w == F(point["welfare"]) == 1
        assert o == F(point["comparison_cover"]) == F(dual["dual_beta"]) > 2
        assert point["source_sha256"] == dual["source_sha256"]
        D = int(dual["common_denominator"])
        assert o == F(int(dual["beta_numerator"]), D)
        weights = {key: F(value) for key, value in dual["multipliers"].items()}
        assert weights == {key: F(int(value), D)
                           for key, value in dual["integer_multipliers"].items()}
        assert weights and min(weights.values()) > 0
        assert all(stored[key] == 0 for key in weights)
        assert dual["full_pricing_nonnegative"] and not dual["negative_columns"]
        assert F(dual["minimum_scaled_integer_residual"]) == 0

        values = {}
        for row_name, source, target, components in ab_specs + ae_specs + [joint_spec, ab_ae_joint_spec]:
            values[row_name] = sum(mass * cross_row(bits, families, source, target, components)
                                   for bits, families, d, mass in atoms)
            if row_name in stored:
                assert values[row_name] == stored[row_name], row_name
        row_orders[n] = list(stored)
        objective[n] = o
        reports[n] = {
            "point_path": str((base / point_path).relative_to(ROOT)),
            "point_sha256": point_sha,
            "dual_path": str((base / dual_path).relative_to(ROOT)),
            "dual_sha256": dual_sha,
            "discovery_sha256": point["source_sha256"],
            "positive_atoms": len(atoms),
            "welfare": str(w),
            "comparison_cover": str(o),
            "stored_zero_rows": sum(value == 0 for value in stored.values()),
            "positive_dual_weights": len(weights),
            "new_exact_row_totals": {key: str(value) for key, value in values.items()},
        }

    assert row_orders["717"] == row_orders["727"][:717]
    assert row_orders["727"] == row_orders["728"][:727] == row_orders["737"][:727]
    assert row_orders["727"][717:] == [spec[0] for spec in ab_specs]
    assert row_orders["728"][727:] == [joint_spec[0]]
    assert row_orders["737"][727:] == [spec[0] for spec in ae_specs]
    assert objective["717"] > objective["727"] > objective["737"] > objective["728"] > 2
    assert F(reports["728"]["new_exact_row_totals"]["crossfinal:AE:AB:2O"]) < 0
    assert F(reports["737"]["new_exact_row_totals"][joint_spec[0]]) < 0
    assert F(reports["728"]["new_exact_row_totals"][ab_ae_joint_spec[0]]) < 0

    print(json.dumps({
        "scope": "Frozen normalized necessary templates. New literal matching only for the 20 single rows and 2 common OO rows. Stored base coefficients and whole-domain certificates are reused.",
        "primal_dual_value_matches": reports,
        "strict_order": ["717", "727", "737", "728", "2"],
        "positive_consecutive_differences": [
            str(objective[left] - right) for left, right in (
                ("717", objective["727"]), ("727", objective["737"]),
                ("737", objective["728"]), ("728", 2),
            )
        ],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
