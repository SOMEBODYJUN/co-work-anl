#!/usr/bin/env python3
"""Exact certificate for the prescribed 128-row, seven-variable H3 cone.

Only the Python standard library is used.  No LP solver, frozen matrix, old
point, query orbit, remote service, or repository state is read or changed.
All outputs stay in this script's directory.  The two mathematical input
pages are read only to record their SHA256 identities.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent
VARIABLES = ("C", "alpha", "beta", "gamma", "eta_QX", "eta_QQ", "eta_XX")
PRIMAL = tuple(map(F, (10, 1, 2, 1, 0, 0, 0)))
PRIMAL_UPPER = (F(10), F(6, 5), F(2), F(1), F(0), F(0), F(0))
OBJECTIVE = (F(1),) + (F(0),) * 6
ATOM_NAMES = ("b", "a", "x", "y", "z", "q")

# Each atom is ordered (b,a,x,y,z,q).  These are rows of E >= 0.
DUAL_SUPPORT = {
    (0, 0, 0, 0, 0, 1): F(14),  # A
    (0, 1, 0, 0, 1, 0): F(12),  # B
    (0, 0, 1, 1, 0, 0): F(6),   # D
    (0, 0, 1, 1, 1, 0): F(6),   # H
}
EXPECTED_REDUCED = (F(0), F(0), F(0), F(0), F(1), F(0), F(11))


def dot(left, right):
    return sum((u * v for u, v in zip(left, right)), F(0))


def budgets_and_row(atom):
    """Return E = coeff dot weights + constant directly from the budgets."""
    b, a, x, y, z, q = atom
    n = b + 1
    d = n + x
    kappa = F(x, n + 2)
    v = F(x, n + y + z)
    target_query = F(q * x, n + 2) + F(q * (1 - x), n)
    maximum_y = F(x - y, n + a)
    maximum_z = F(x - z, n + a)
    br_z_q = F(z - q, d + y)
    pair_base = F(y, d + z) + F(z, d + y) + F(y, d * (d + 1))
    tp_qx = pair_base - F(q + x, d) + F(q * x, d * (d + 1))
    tp_qq = pair_base - F(2 * q, d) + F(q, d * (d + 1))
    tp_xx = pair_base - F(2 * x, d) + F(x, d * (d + 1))
    coefficients = (
        v - kappa,
        -maximum_y,
        -maximum_z,
        -br_z_q,
        -tp_qx,
        -tp_qq,
        -tp_xx,
    )
    constant = kappa - target_query
    return {
        "coefficients": coefficients,
        "constant": constant,
        "tp_qx": tp_qx,
        "tp_qq": tp_qq,
        "tp_xx": tp_xx,
    }


def direct_remainder(atom, weights):
    """A second direct target-minus-budgets evaluation of the same row."""
    b, a, x, y, z, q = atom
    C, alpha, beta, gamma, eta_qx, eta_qq, eta_xx = weights
    n = b + 1
    m = b + x
    value = C * F(x, b + 1 + y + z) - (C - 1) * F(x, b + 3)
    value -= F(q * x, b + 3) + F(q * (1 - x), b + 1)
    value -= alpha * F(x - y, b + a + 1)
    value -= beta * F(x - z, b + a + 1)
    value -= gamma * F(z - q, b + x + y + 1)
    for eta, first, second in ((eta_qx, q, x), (eta_qq, q, q), (eta_xx, x, x)):
        pair_value = F(y, m + 1 + z) + F(z, m + 1 + y)
        pair_value += F(y, (m + 1) * (m + 2))
        pair_value -= F(first + second, m + 1)
        pair_value += F(first * second, (m + 1) * (m + 2))
        value -= eta * pair_value
    return value


def as_strings(values):
    return [str(value) for value in values]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    input_paths = (WORKSPACE / "maxb_h3_bridge.md", WORKSPACE / "maxb_h3_audit.md")
    input_hashes = {path.name: digest(path) for path in input_paths}
    atoms = list(product(range(4), *([range(2)] * 5)))
    assert len(atoms) == 128 and len(set(atoms)) == 128
    rows = {atom: budgets_and_row(atom) for atom in atoms}
    slacks = {}
    upper_slacks = {}

    # Verify every row by exact rational arithmetic, at both endpoints of
    # the complete optimal alpha interval.  This is not an optimization or
    # a parameter grid: feasibility in between follows by convexity.
    for atom in atoms:
        row = rows[atom]
        slacks[atom] = dot(row["coefficients"], PRIMAL) + row["constant"]
        upper_slacks[atom] = dot(row["coefficients"], PRIMAL_UPPER) + row["constant"]
        assert slacks[atom] == direct_remainder(atom, PRIMAL)
        assert upper_slacks[atom] == direct_remainder(atom, PRIMAL_UPPER)
        assert slacks[atom] >= 0 and upper_slacks[atom] >= 0
        # Verify every affine coefficient via the defining identity,
        # using the zero vector and each of the seven coordinate vectors.
        zero = (F(0),) * 7
        assert direct_remainder(atom, zero) == row["constant"]
        for index in range(7):
            unit = tuple(F(k == index) for k in range(7))
            assert direct_remainder(atom, unit) - row["constant"] == row["coefficients"][index]

    # Standard dual: min e_C^T w, M w >= -c, w >= 0.
    # max (-c)^T lambda, M^T lambda <= e_C, lambda >= 0.
    dual_coefficients = tuple(
        sum((weight * rows[atom]["coefficients"][index] for atom, weight in DUAL_SUPPORT.items()), F(0))
        for index in range(7)
    )
    dual_constant = sum((weight * rows[atom]["constant"] for atom, weight in DUAL_SUPPORT.items()), F(0))
    reduced_cost = tuple(c - d for c, d in zip(OBJECTIVE, dual_coefficients))
    dual_objective = -dual_constant
    assert reduced_cost == EXPECTED_REDUCED
    assert all(weight >= 0 for weight in DUAL_SUPPORT.values())
    assert all(cost >= 0 for cost in reduced_cost)
    assert dot(OBJECTIVE, PRIMAL) == dual_objective == 10
    assert all(slacks[atom] == 0 for atom in DUAL_SUPPORT)
    assert dot(PRIMAL, reduced_cost) == 0

    # The first and fourth rows force eta_QQ = 0 in every feasible point:
    # E_A + 3 E_H = -eta_QQ.
    atom_A = (0, 0, 0, 0, 0, 1)
    atom_H = (0, 0, 1, 1, 1, 0)
    annihilator_coefficients = tuple(
        rows[atom_A]["coefficients"][index] + 3 * rows[atom_H]["coefficients"][index]
        for index in range(7)
    )
    annihilator_constant = rows[atom_A]["constant"] + 3 * rows[atom_H]["constant"]
    assert annihilator_coefficients == (F(0), F(0), F(0), F(0), F(0), F(-1), F(0))
    assert annihilator_constant == 0

    # Two additional rows identify the sharp alpha endpoints once the
    # dual equalities have fixed C,beta,gamma and all three eta values.
    alpha_lower_atom = (0, 1, 0, 1, 0, 1)
    alpha_upper_atom = (3, 0, 1, 0, 1, 0)
    assert slacks[alpha_lower_atom] == 0
    assert upper_slacks[alpha_upper_atom] == 0
    assert rows[alpha_lower_atom]["coefficients"][1] == F(1, 2)
    assert rows[alpha_upper_atom]["coefficients"][1] == F(-1, 4)

    payload = {
        "schema": "maxb-h3-pair-strength-exact-v1",
        "variables": list(VARIABLES),
        "row_convention": "E = coefficients dot weights + constant >= 0",
        "input_sha256": input_hashes,
        "primal": dict(zip(VARIABLES, as_strings(PRIMAL))),
        "optimal_face_upper_endpoint": dict(zip(VARIABLES, as_strings(PRIMAL_UPPER))),
        "dual": {
            "standard_primal": "min e_C^T w subject to M w >= -c and w >= 0",
            "standard_dual": "max (-c)^T lambda subject to M^T lambda <= e_C and lambda >= 0",
            "support": [{"atom": list(atom), "weight": str(weight)} for atom, weight in DUAL_SUPPORT.items()],
            "weighted_coefficients": as_strings(dual_coefficients),
            "weighted_constant": str(dual_constant),
            "reduced_cost": as_strings(reduced_cost),
            "objective": str(dual_objective),
            "identity": "C - 10 = 14 E_A + 12 E_B + 6 E_D + 6 E_H + eta_QX + 11 eta_XX",
        },
        "eta_QQ_zero_identity": "E_A + 3 E_H = -eta_QQ",
        "atoms": [
            {
                "atom": dict(zip(ATOM_NAMES, atom)),
                "coefficients": as_strings(rows[atom]["coefficients"]),
                "constant": str(rows[atom]["constant"]),
                "tp_qx": str(rows[atom]["tp_qx"]),
                "tp_qq": str(rows[atom]["tp_qq"]),
                "tp_xx": str(rows[atom]["tp_xx"]),
                "primal_slack": str(slacks[atom]),
                "upper_endpoint_slack": str(upper_slacks[atom]),
            }
            for atom in atoms
        ],
    }
    certificate_path = HERE / "exact_certificate.json"
    certificate_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# 指定七权锥的全部 128 型有理系数与余项",
        "",
        "每行 `E=d_C C+d_α α+d_β β+d_γ γ+d_1 η1+d_2 η2+d_3 η3+c`。",
        "`E₁` 对应 `(10,1,2,1,0,0,0)`；`E₆/₅` 对应 `(10,6/5,2,1,0,0,0)`。",
        "三份 TP 依次为 TP(Q,X)、TP(Q,Q)、TP(X,X)。所有数均为精确有理数。",
        "",
        "| (b,a,x,y,z,q) | d_C | d_α | d_β | d_γ | d_1 | d_2 | d_3 | c | E₁ | E₆/₅ |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for atom in atoms:
        coefficients = as_strings(rows[atom]["coefficients"])
        label = "(" + ",".join(map(str, atom)) + ")"
        values = [label, *coefficients, str(rows[atom]["constant"]), str(slacks[atom]), str(upper_slacks[atom])]
        lines.append("| " + " | ".join(values) + " |")
    (HERE / "atom_table.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    assert input_hashes == {path.name: digest(path) for path in input_paths}
    report = {
        "status": "PASS",
        "rows": len(atoms),
        "variables": len(VARIABLES),
        "optimum_C": "10",
        "primal_zero_rows": sum(value == 0 for value in slacks.values()),
        "primal_positive_rows": sum(value > 0 for value in slacks.values()),
        "primal_negative_rows": sum(value < 0 for value in slacks.values()),
        "primal_smallest_positive_slack": str(min(value for value in slacks.values() if value > 0)),
        "upper_endpoint_zero_rows": sum(value == 0 for value in upper_slacks.values()),
        "upper_endpoint_positive_rows": sum(value > 0 for value in upper_slacks.values()),
        "upper_endpoint_negative_rows": sum(value < 0 for value in upper_slacks.values()),
        "upper_endpoint_smallest_positive_slack": str(min(value for value in upper_slacks.values() if value > 0)),
        "dual_support_rows": len(DUAL_SUPPORT),
        "dual_objective": str(dual_objective),
        "duality_gap": "0",
        "eta_QQ_identically_forced_zero": True,
        "complete_optimal_face": "C=10; beta=2; gamma=1; eta_QX=eta_QQ=eta_XX=0; 1<=alpha<=6/5",
        "optimizer_called": False,
        "optimizer_invocations": 0,
        "frozen_matrix_read": False,
        "old_point_read_or_evaluated": False,
        "query_orbit_scan": False,
        "remote_computation": False,
        "input_sha256_unchanged": input_hashes,
        "exact_certificate_sha256": digest(certificate_path),
    }
    (HERE / "verification.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
