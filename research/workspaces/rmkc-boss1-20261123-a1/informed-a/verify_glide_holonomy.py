"""Symbolic certificate for a shifted, nonsplit glide-reflection orbit in rank two."""

import argparse
import itertools
import json
from pathlib import Path

import sympy as sp


def strings(vector):
    return [str(entry) for entry in vector]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, required=True)
    out = parser.parse_args().certificate
    half, third = sp.Rational(1, 2), sp.Rational(1, 3)
    x_axis, y_axis = sp.eye(2).columnspace()
    reflection = sp.diag(1, -1)
    centre = sp.Matrix([0, third])
    shift = reflection * centre + half * x_axis - centre
    assert shift == sp.Matrix([half, -2 * third])
    assert shift + reflection * shift == x_axis

    # Every element outside the integer translations is an integer translate of
    # the glide. Its square has odd x-component, excluding a splitting.
    p, q = sp.symbols("p q", integer=True)
    odd_offset = sp.Matrix([p, q]) + shift
    square = sp.simplify(odd_offset + reflection * odd_offset)
    assert square == sp.Matrix([2 * p + 1, 0]) and sp.Mod(square[0], 2) == 1
    assert not all(entry.is_Integer for entry in -shift - shift)

    signs = tuple(itertools.product((-1, 1), repeat=2))
    axes = [x_axis, -x_axis, y_axis, -y_axis]
    glides = [sp.Matrix([sx * half, third if sy == 1 else -2 * third])
              for sx, sy in signs]
    normals = axes + glides
    a, b = sp.symbols("a b", nonnegative=True)
    operator = sp.diag(a, b)
    assert reflection * operator == operator * reflection
    assert all(all(entry.is_Integer for entry in normal - shift) for normal in glides)
    assert all(all(entry.is_Integer for entry in normal) for normal in axes)
    assert len({tuple(normal) for normal in normals}) == 8

    # The two coordinate forms are independent. For every integer point or glide
    # offset in one sign orthant, subtract its representative and then signed
    # coordinate unit vectors. The displayed difference is nonnegative on every
    # nonnegative INTEGER count (including count=0), without a bounded scan.
    i, j = sp.symbols("i j", integer=True, nonnegative=True)
    reductions = []
    for orbit in ("integer translations", "glide coset"):
        for index, (sx, sy) in enumerate(signs):
            base = sp.zeros(2, 1) if orbit == "integer translations" else glides[index]
            point = base + sp.Matrix([sx * i, sy * j])
            differences = []
            for coordinate, count in enumerate((i, j)):
                leftover = sp.expand(point[coordinate]**2 - base[coordinate]**2 - count)
                form = count * (count - 1) + 2 * abs(base[coordinate]) * count
                assert sp.expand(leftover - form) == 0
                differences.append(str(form))
            # Fractional part equals shift in each glide orthant, and the base
            # has smallest absolute coordinate on each of the two signed rays.
            if orbit == "glide coset":
                for coordinate, sign in enumerate((sx, sy)):
                    residue = sp.frac(sign * shift[coordinate])
                    assert 0 < residue < 1 and sign * base[coordinate] == residue
            reductions.append(dict(orbit=orbit, signs=[sx, sy], base=strings(base),
                                   all_points=strings(point), nonnegative_leftovers=differences))

    # A rational witness lies on each displayed facet and is strict for every
    # other competitor at the same pair of positive weights.
    inequalities = []
    for index, normal in enumerate(normals):
        weights = (1, 3) if index < 2 else (2, 1) if index < 4 else (1, 1)
        metric = sp.diag(*weights)
        witness = metric * normal / 2
        slacks = [v.dot(metric * v) - 2 * v.dot(witness) for v in normals]
        assert slacks[index] == 0 and all(s > 0 for k, s in enumerate(slacks) if k != index)
        inequalities.append(dict(normal=strings(normal), right_hand_side=str(normal.dot(operator * normal)),
                                 witness_weights=list(weights), witness_w=strings(witness),
                                 all_slacks=strings(slacks)))

    # With positive weight t along one surviving axis, the exact finite H-system
    # bounds w_surviving/t. Independently compute its one-dimensional Voronoi
    # interval from the immediately adjacent orbit centres modulo Z.
    faces = []
    for surviving in (0, 1):
        collapsed = 1 - surviving
        unit = (x_axis, y_axis)[collapsed]
        face_form = sp.diag(int(surviving == 0), int(surviving == 1))
        assert face_form.nullspace() == [unit] and unit in normals and -unit in normals
        entries = [n[surviving] for n in normals]
        lower = max(v / 2 for v in entries if v < 0)
        upper = min(v / 2 for v in entries if v > 0)
        phases = sorted({sp.Integer(0), sp.frac(shift[surviving])})
        previous = max(z - 1 for z in phases)
        following = min([sp.Integer(1), *(z for z in phases if z > 0)])
        assert (lower, upper) == (previous / 2, following / 2)
        faces.append(dict(zero_parameter=("b", "a")[surviving], collapsed_w=collapsed,
                          surviving_w=surviving, rational_phases=strings(phases),
                          neighbouring_orbit_centres=strings((previous, following)),
                          allowed_w_divided_by_surviving_weight=strings((lower, upper))))
    assert [f["allowed_w_divided_by_surviving_weight"] for f in faces] == [
        ["-1/4", "1/4"], ["-1/3", "1/6"]]
    assert sp.zeros(2).nullspace() == [x_axis, y_axis]
    assert all(n in normals for n in (x_axis, -x_axis, y_axis, -y_axis))

    data = dict(
        scope="An exact nonsplit finite-holonomy example. No claim of geometric realization.",
        lattice="Z^2", operator="diag(a,b), a,b nonnegative", centre=strings(centre),
        linear_holonomy=[list(row) for row in ((1, 0), (0, -1))],
        glide_offset=strings(shift), square_of_any_lattice_glide=strings(square),
        orbit_offsets="Z^2 union ((1/2,-2/3)+Z^2)",
        inequality_convention="w is measured from T_(a,b)c. For each m, 2 m·w ≤ m^t T_(a,b) m.",
        orthant_reductions=reductions, irredundant_competitors=inequalities,
        rank_one_faces=faces, vertex="a=b=0 forces w=(0,0) by the four signed axis inequalities.",
    )
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print("Certified nonsplitting, 8 all-parameter orthant identities in each coordinate, "
          "8 necessary inequalities, both singular-face intervals, and the origin.")


if __name__ == "__main__":
    main()
