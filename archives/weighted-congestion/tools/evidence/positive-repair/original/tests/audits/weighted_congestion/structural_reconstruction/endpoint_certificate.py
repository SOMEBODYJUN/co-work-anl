#!/usr/bin/env python3
"""Exact local endpoint-window certificate for a nondecreasing convex power.
No all-state conclusion is computed. The general quadrature lemma requires f'>=0
as well as f''>=0; convexity alone is insufficient.
"""
from fractions import Fraction as F
from pathlib import Path
import json


def ratio_string(x):
    return f"{x.numerator}/{x.denominator}"


def certificate():
    d, R, K = 32, 256, 64
    alpha, kappa = F(24), F(101, 100)
    mass = F(K, R)
    P = (1 + mass) ** d
    X = sum(((1 + F(j, R)) ** d for j in range(1, K + 1)), F(0))
    Y = sum((F(j, R) ** d for j in range(1, K + 1)), F(0))
    H, L = P - alpha, alpha * X - Y
    A = ((1 + mass) ** (d + 1) - 1) / (d + 1)
    B = mass ** (d + 1) / (d + 1)
    D = P - alpha - kappa * (alpha * A - B)
    refined_error = (P - 1) / (2 * R) + d * ((1 + mass) ** (d - 1) - 1) / (8 * R * R)
    coarse_error = (P - 1) / R
    gamma = L / (R * H)
    normalized_amplitude = kappa * gamma
    refined_margin = (D - kappa * alpha * refined_error) / H
    coarse_margin = (D - kappa * alpha * coarse_error) / H
    heavy_margin = (kappa * L - alpha * X) / L
    S = normalized_amplitude * R
    z = (mass / (1 + mass)) ** d

    # Every conclusion below is an integer/Fraction comparison.
    checks = {
        "positive_heavy_margin_H": H > 0,
        "positive_incoming_L": L > 0,
        "amplitude_S_gt_1": S > 1,
        "exact_amplitude_gt_984_over_1000": normalized_amplitude > F(984, 1000),
        "exact_amplitude_lt_985_over_1000": normalized_amplitude < F(985, 1000),
        "exact_contraction_margin_gt_3_over_200": 1 - normalized_amplitude > F(3, 200),
        "convex_grid_error_upper_bound": X / R - A <= refined_error,
        "convex_grid_error_nonnegative": X / R >= A,
        "refined_analytic_margin_gt_3_over_200": refined_margin > F(3, 200),
        "coarse_analytic_margin_negative": coarse_margin < 0,
        "heavy_margin_gt_99_over_10000_L": heavy_margin > F(99, 10000),
        "heavy_margin_bound_from_pointwise_Y_X": Y / L <= z / (alpha - z),
        "original_mass_binding_fails_H_at_same_d": (1 + F(1, 32)) ** d < alpha,
    }
    assert all(checks.values()), checks
    values = {
        "normalized_amplitude": normalized_amplitude,
        "refined_analytic_contraction_lower_bound": refined_margin,
        "coarse_analytic_contraction_lower_bound": coarse_margin,
        "normalized_heavy_margin": heavy_margin,
        "continuous_safety_threshold": (P + kappa * B) / (1 + kappa * A),
        "finite_grid_safety_threshold": (P + kappa * Y / R) / (1 + kappa * X / R),
    }
    return {
        "scope": "local scalar window feasibility only; no all-state counterexample claim",
        "parameters": {"degree": d, "alpha": ratio_string(alpha), "kappa": ratio_string(kappa), "mass": ratio_string(mass), "R": R, "K": K},
        "exact_checks": checks,
        "values": {key: {"exact": ratio_string(value), "display_only_decimal": float(value)} for key, value in values.items()},
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    data = certificate()
    if args.output:
        with args.output.open('x') as f:
            f.write(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({"all_exact_checks_passed": all(data["exact_checks"].values()),
                      "parameters": data["parameters"],
                      "display_values_only": {key: value["display_only_decimal"] for key, value in data["values"].items()},
                      "scope": data["scope"]}, indent=2, ensure_ascii=False))
