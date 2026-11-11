#!/usr/bin/env python3
"""Exact source-4 cone certificate; no optimizer, no SPE enumeration.

All writes stay beside this file.  The only numerical LP was the discovery
call recorded in discovery_lp.json; this checker uses fractions throughout.
"""

from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
NAMES = ("alpha", "safe_Y", "safe_T", "max_Y", "max_T", "last_avg")
EXTRA = ("last_X", "last_Y", "pair_avg_X", "pair_avg_diag", "pair_X_X")
ATOMS = tuple(product(range(1, 5), range(2), range(2), range(2), range(2)))
THETA = F(1, 6)


def core_row(atom, theta=THETA):
    n, k, x, y, t = atom
    D = n + 2
    coeff = (
        F(x, n + y + t) - F(x, D),
        F(y - x, D),
        F(t - x, D),
        -F(x - y, n + k),
        -F(x - t, n + k),
        -F(t - theta, n + x + y),
    )
    const = F(x, D) - theta * (F(x, D) + F(1 - x, n))
    return coeff, const


def extra_budgets(atom, theta=THETA):
    n, k, x, y, t = atom
    z = n + x
    wallet = F(y, z + t) + F(t, z + y) + F(y, z * (z + 1))
    return (
        F(t - x, z + y),
        F(t - y, z + y),
        wallet - F(theta + x, z) + F(theta * x, z * (z + 1)),
        wallet - F(2 * theta, z) + F(theta, z * (z + 1)),
        wallet - F(2 * x, z) + F(x, z * (z + 1)),
    )


def full_row(atom, theta=THETA):
    coeff, const = core_row(atom, theta)
    return coeff + tuple(-v for v in extra_budgets(atom, theta)), const


def residual(atom, weights, theta=THETA):
    coeff, const = core_row(atom, theta) if len(weights) == 6 else full_row(atom, theta)
    return const + sum((a * w for a, w in zip(coeff, weights)), F(0))


WEIGHTS = {
    "LP_lower_endpoint": tuple(map(F, (10, 0, 0, F(1, 6), 2, 1))),
    "H3_universal": tuple(map(F, (10, 0, 0, 1, 2, 1))),
    "fixed_theta_upper_endpoint": tuple(map(F, (10, 0, 0, F(11, 9), 2, 1))),
}

BASE_DUAL = {
    (1, 0, 0, 0, 0): F(64),
    (1, 0, 1, 1, 0): F(3),
    (1, 1, 0, 0, 1): F(27, 2),
    (4, 0, 1, 1, 0): F(15),
}
EXTENDED_DUAL = dict(BASE_DUAL)
EXTENDED_DUAL[(1, 0, 0, 0, 0)] += F(41, 4)
EXTENDED_DUAL[(1, 0, 1, 1, 1)] = F(123, 20)
ZERO_COST_RAY = {(1, 0, 0, 0, 0): F(5), (1, 0, 1, 1, 1): F(3)}


def sum_rows(dual, extended=False):
    total = [F(0)] * (11 if extended else 6)
    constant = F(0)
    for atom, weight in dual.items():
        assert weight >= 0
        coeff, const = full_row(atom) if extended else core_row(atom)
        total = [u + weight * v for u, v in zip(total, coeff)]
        constant += weight * const
    return total, constant


def sum_new_budgets(dual):
    return [sum((w * extra_budgets(a)[j] for a, w in dual.items()), F(0)) for j in range(5)]


def jsonable(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(v) for v in value]
    return value


def emit_json(name, value):
    (HERE / name).write_text(json.dumps(jsonable(value), ensure_ascii=False, indent=2) + "\n")


def main():
    audit = []
    for atom in ATOMS:
        coeff, const = core_row(atom)
        values = {name: residual(atom, weights) for name, weights in WEIGHTS.items()}
        assert min(values.values()) >= 0
        audit.append({"atom_n_k_x_y_t": atom, "coefficients": coeff,
                      "constant": const, "residuals": values,
                      "extra_budget_values": extra_budgets(atom),
                      "base_dual_weight": BASE_DUAL.get(atom, F(0)),
                      "extended_dual_weight": EXTENDED_DUAL.get(atom, F(0))})

    base_coeff, base_const = sum_rows(BASE_DUAL)
    assert base_coeff == list(map(F, (1, 0, 1, 0, 0, 0)))
    assert base_const == -10
    ext_coeff, ext_const = sum_rows(EXTENDED_DUAL, True)
    assert ext_coeff == list(map(F, (1, 0, 1, 0, 0, 0, -10, -10, -1, 0, -11)))
    assert ext_const == -10
    ray_coeff, ray_const = sum_rows(ZERO_COST_RAY)
    assert ray_coeff == [F(0)] * 6 and ray_const == 0
    assert sum_new_budgets(BASE_DUAL) == list(map(F, (10, 10, 1, F(-41, 24), 11)))
    assert sum_new_budgets(ZERO_COST_RAY) == list(map(F, (0, 0, 0, F(5, 6), 0)))
    assert sum_new_budgets(EXTENDED_DUAL) == list(map(F, (10, 10, 1, 0, 11)))

    # The original H3 multipliers are feasible for every theta in [0,1],
    # because each coefficient is affine in theta and both endpoints pass.
    universal = []
    for theta in (F(0), F(1)):
        for atom in ATOMS:
            val = residual(atom, WEIGHTS["H3_universal"], theta)
            assert val >= 0
            universal.append({"theta": theta, "atom": atom, "residual": val})

    # The union version only requires theta in {0,1/6}.  Its optimal max_Y
    # interval is [1/6,6/5], slightly smaller than at fixed theta=1/6.
    union = []
    for theta in (F(0), THETA):
        for atom in ATOMS:
            values = {name: residual(atom, WEIGHTS[name], theta)
                      for name in ("LP_lower_endpoint", "H3_universal")}
            values["union_upper_endpoint"] = residual(atom, (F(10), F(0), F(0), F(6, 5), F(2), F(1)), theta)
            # The fixed-theta high endpoint 11/9 is not a union certificate.
            assert values["H3_universal"] >= 0
            assert values["LP_lower_endpoint"] >= 0
            assert values["union_upper_endpoint"] >= 0
            union.append({"theta": theta, "atom": atom, "residuals": values})

    # Exact arbitrary-d correction for the lower LP endpoint only.
    # It is unnecessary for H3_universal but records why d>1 cannot be
    # silently inserted into the reduced max_Y=1/6 certificate.
    corrections = []
    for n, k, x, d in product(range(1, 5), range(2), range(2), range(7)):
        theta = F(d, 6)
        penalty = (1 - x) * max(F(0), F(d, 6 * n * (n + 1)) - F(1, 6 * (n + k)))
        hidden_values = [residual((n, k, x, y, t), WEIGHTS["LP_lower_endpoint"], theta)
                         for y, t in product(range(2), range(2))]
        assert penalty == max(F(0), -min(hidden_values))
        assert all(v + penalty >= 0 for v in hidden_values)
        corrections.append({"n_k_x_d": (n, k, x, d), "minimal_nonnegative_penalty": penalty,
                            "hidden_residuals_00_01_10_11": hidden_values})

    # Scalar query coefficients for weakening a true six-query average
    # d/6 to o/6, o=indicator of their union, are all strictly positive.
    union_monotonicity = []
    for n, x, y in product(range(1, 5), range(2), range(2)):
        z = n + x
        coeffs = (F(1, z + y), F(1, z) - F(x, z * (z + 1)),
                  F(2, z) - F(1, z * (z + 1)))
        assert min(coeffs) > 0
        union_monotonicity.append({"n_x_y": (n, x, y),
                                   "last_pairQX_pairQQ_positive_query_coefficients": coeffs})

    sources = [
        "archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md",
        "research/workspaces/six-boss1-20261111/maxb_h3_bridge.md",
        "research/workspaces/six-boss1-20261111/main_averaged_menu_prefix.md",
    ]
    source_hashes = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in sources}
    summary = {
        "status": "PASS", "coefficient": F(10), "cone": "six nonnegative weights; eleven-weight true-tail extension",
        "fixed_theta": THETA, "fixed_theta_atom_count": len(ATOMS),
        "universal_theta_endpoint_checks": len(universal), "union_domain_checks": len(union),
        "arbitrary_d_correction_checks": len(corrections) * 4,
        "zero_counts": {name: sum(row["residuals"][name] == 0 for row in audit) for name in WEIGHTS},
        "weights": WEIGHTS, "base_dual": [{"atom": a, "weight": w} for a, w in BASE_DUAL.items()],
        "extended_dual": [{"atom": a, "weight": w} for a, w in EXTENDED_DUAL.items()],
        "base_dual_summed_coefficients": base_coeff, "base_dual_constant": base_const,
        "extended_dual_summed_coefficients": ext_coeff, "extended_dual_constant": ext_const,
        "base_dual_new_budget_sums": sum_new_budgets(BASE_DUAL),
        "zero_cost_ray_new_budget_sums": sum_new_budgets(ZERO_COST_RAY),
        "extended_dual_new_budget_sums": sum_new_budgets(EXTENDED_DUAL),
        "fixed_theta_optimal_maxY_interval": [F(1, 6), F(11, 9)],
        "union_domain_optimal_maxY_interval": [F(1, 6), F(6, 5)],
        "fixed_theta_upper_rejected_on_union_domain": {
            "theta": F(0), "atom": (4, 0, 1, 0, 1),
            "residual": residual((4, 0, 1, 0, 1), WEIGHTS["fixed_theta_upper_endpoint"], F(0))},
        "all_other_optimal_weights": {"alpha": 10, "safe_Y": 0, "safe_T": 0,
                                       "max_T": 2, "last_avg": 1, "all_five_extension_weights": 0},
        "discovery_optimizer_calls": 1, "optimizer_called_by_checker": False,
        "full_SPE_sharpness_claimed": False, "global_optimizer_called": False,
        "existing_points_read_or_evaluated": False, "source_sha256_at_verification": source_hashes,
    }
    emit_json("atom_audit_64.json", {"variable_order": NAMES, "extra_order": EXTRA, "rows": audit})
    emit_json("theta_endpoint_audit_128.json", universal)
    emit_json("union_domain_audit_128.json", union)
    emit_json("lower_endpoint_correction.json", corrections)
    emit_json("union_monotonicity.json", union_monotonicity)
    emit_json("certificate.json", summary)

    lines = ["# 全部 64 型精确余项", "", "固定 θ=1/6；所有值由 Fraction 生成。", "",
             "| n | k | x | y | t | aY=1/6 | aY=1（H3） | aY=11/9 | 六权对偶 | 扩展对偶 |",
             "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for row in audit:
        vals = list(row["atom_n_k_x_y_t"]) + list(row["residuals"].values())
        vals += [row["base_dual_weight"], row["extended_dual_weight"]]
        lines.append("| " + " | ".join(map(str, vals)) + " |")
    (HERE / "atom_table.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(jsonable({k: summary[k] for k in (
        "status", "coefficient", "fixed_theta_atom_count", "universal_theta_endpoint_checks",
        "union_domain_checks", "arbitrary_d_correction_checks", "zero_counts",
        "optimizer_called_by_checker", "global_optimizer_called")}), ensure_ascii=False))


if __name__ == "__main__":
    main()
