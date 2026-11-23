"""Exact sign-fan certificate for a three-parameter rational Voronoi cone."""

import argparse
import itertools
import json
from pathlib import Path

import sympy as sp


def coordinates(v):
    return [int(entry) for entry in v]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", required=True, type=Path)
    args = parser.parse_args()
    f = (sp.Matrix([1, 0]), sp.Matrix([1, 1]), sp.Matrix([0, 1]))
    forms = tuple(v * v.T for v in f)
    names = ("a", "b", "c")
    a, b, c = sp.symbols("a b c", nonnegative=True)
    coeffs = (a, b, c)
    total = sum((t * M for t, M in zip(coeffs, forms)), sp.zeros(2))
    assert total == sp.Matrix([[a + b, b], [b, b + c]])
    assert sp.expand(total.det() - a * b - b * c - c * a) == 0
    rays = [
        sp.Matrix([1, 0]), sp.Matrix([0, 1]), sp.Matrix([-1, 1]),
        sp.Matrix([-1, 0]), sp.Matrix([0, -1]), sp.Matrix([1, -1]),
    ]
    # The sign chambers are cut out by the three zero lines of the f_j.
    assert set(map(tuple, rays)) == {
        tuple(sign * sp.Matrix([-v[1], v[0]]))
        for v in f for sign in (-1, 1)
    }
    coeff1, coeff2 = sp.symbols("i j", integer=True, nonnegative=True)
    sectors = []
    for left, right in zip(rays, rays[1:] + rays[:1]):
        basis = sp.Matrix.hstack(left, right)
        assert basis.det() == 1
        assert all(entry.is_Integer for entry in basis.inv())
        monomial = coeff1 * left + coeff2 * right
        signs = []
        for functional, form in zip(f, forms):
            sl, sr = functional.dot(left), functional.dot(right)
            assert sl * sr >= 0
            # Each term on the RHS is nonnegative for integral i,j >= 0.
            difference = ((monomial.T * form * monomial)[0]
                          - coeff1 * sl**2 - coeff2 * sr**2)
            identity = (coeff1 * (coeff1 - 1) * sl**2
                        + 2 * coeff1 * coeff2 * sl * sr
                        + coeff2 * (coeff2 - 1) * sr**2)
            assert sp.expand(difference - identity) == 0
            signs.append([int(sl), int(sr)])
        sectors.append({
            "generators": [coordinates(left), coordinates(right)],
            "determinant": 1,
            "integer_coordinates_inverse": [coordinates(row) for row in basis.inv().tolist()],
            "functional_values_on_generators": signs,
        })
    displayed = [sp.Matrix([1, 0]), sp.Matrix([0, 1]), sp.Matrix([1, -1])]
    rhs = [sp.expand((h.T * total * h)[0]) for h in displayed]
    assert rhs == [a + b, b + c, a + c]
    faces = []
    for size in range(4):
        for positive in itertools.combinations(range(3), size):
            # All positive weights on this face have the same kernel by PSD.
            M = sum((forms[i] for i in positive), sp.zeros(2))
            active = [h for h in rays if all(f[i].dot(h) == 0 for i in positive)]
            span_rank = sp.Matrix.hstack(*active).rank() if active else 0
            assert span_rank == 2 - M.rank()
            assert all(M * h == sp.zeros(2, 1) for h in active)
            faces.append({
                "positive_parameters": [names[i] for i in positive],
                "rank": M.rank(),
                "zero_width_normals": [coordinates(h) for h in active],
                "kernel_basis": [coordinates(v) for v in M.nullspace()],
            })
    certificate = {
        "claim": "Exact finite description for this rank-two lattice pencil",
        "pencil": [[str(x) for x in row] for row in total.tolist()],
        "weights": list(names),
        "nonnegative_rank_one_functionals": [coordinates(v) for v in f],
        "unimodular_complete_sign_fan": sectors,
        "paired_voronoi_inequalities": [
            {"normal": coordinates(h), "bound_for_abs_twice_pairing": str(z)}
            for h, z in zip(displayed, rhs)
        ],
        "all_relative_face_kernels": faces,
        "scope": "Uniform symbolic identities on all lattice points and all nonnegative weights for the displayed pencil; no geometric realization claimed.",
    }
    args.certificate.write_text(json.dumps(certificate, indent=2) + "\n")
    print("Certified 6 unimodular sign sectors, 18 polynomial identities, "
          "3 paired Voronoi inequalities, and the kernels on all 8 parameter faces.")


if __name__ == "__main__":
    main()
