#!/usr/bin/env python3
"""Independent exact audit of the fixed 19-weight nested-price nonseparation witness.

Reads only data; imports neither the discovery program nor earlier pricing code.
Rebuilds customer masses, both source budgets, outer injection, discounted flow,
and every coordinate of the occupation cost from the mathematical formulas.
This checks a full-cone lower-bound certificate, not all 448 Bellman tables or
the validity of a purported complete SPE.
"""

from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


BASE = Path(__file__).resolve().parent.parent
POINT = BASE / "peer_augmented_lp/augmented_lp_exact.json"
CERT = BASE / "main_nested_price/one_case_exact.json"
OUT = Path(__file__).resolve().parent / "independent_one_case_audit.json"
POINT_SHA = "d70c26065d42fd73dedc94183e4533dd6f8608d5841f7a6018ff180dc77e2f9f"
NAMES = [
    "sigma", "alpha_m", "alpha_l", "beta_m", "beta_l",
    "mu_A1", "mu_A2", "mu_A3", "mu_A4", "mu_A5", "mu_A6",
    "mu_mean_T", "mu_current", "mu_previous",
    "outer_source", "outer_alpha_m", "outer_alpha_l", "outer_beta_m", "outer_beta_l",
]
STATES = [(a, t) for a in range(2) for t in range(2)]


def check(condition, description):
    if not condition:
        raise AssertionError(description)


def share(numerator, denominator):
    # A zero numerator contributes zero, including at a zero denominator.
    return Q(numerator, denominator) if numerator else Q(0)


def probability_row(values, width, label):
    row = [Q(value) for value in values]
    check(len(row) == width, label + ": width")
    check(all(value >= 0 for value in row), label + ": nonnegative")
    check(sum(row) == 1, label + ": mass one")
    return row


def solve_rational(matrix, rhs):
    n = len(rhs)
    augmented = [[Q(x) for x in matrix[j]] + [Q(rhs[j])] for j in range(n)]
    for column in range(n):
        pivot = next(row for row in range(column, n) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [x / scale for x in augmented[column]]
        for row in range(n):
            if row != column and augmented[row][column]:
                scale = augmented[row][column]
                augmented[row] = [
                    x - scale * y for x, y in zip(augmented[row], augmented[column])
                ]
    return [augmented[row][-1] for row in range(n)]


def inner_features(bits, d, source, state, action):
    a, t = state
    c, s = action
    p = sum(bits[:source - 1])
    ell = sum(bits[:5])
    real_denominator = p + t + s + c
    query_denominator = p + t + s + 1
    last_share = share(c, real_denominator)
    features = [
        share(t, real_denominator), Q(s, ell + 1), Q(c, ell + 1), Q(s), Q(c)
    ]
    for membership in [*bits, Q(d, 6), Q(t), Q(a)]:
        features.append(Q(membership) / query_denominator - last_share)
    check(len(features) == 14, "inner feature count")
    return features


def outer_features(bits, source, y, action):
    c, s = action
    p = sum(bits[:source - 1])
    ell = sum(bits[:5])
    return [
        share(y, p + y + s + c), Q(s, ell + 1), Q(c, ell + 1), Q(s), Q(c)
    ]


def main():
    point_bytes = POINT.read_bytes()
    cert_bytes = CERT.read_bytes()
    check(sha256(point_bytes).hexdigest() == POINT_SHA, "exact point SHA")
    point, cert = json.loads(point_bytes), json.loads(cert_bytes)
    check(cert["point_sha256"] == POINT_SHA, "certificate point binding")
    check(cert["parameter_names"] == NAMES, "parameter names and order")
    check(cert["parameter_count"] == 19, "nineteen parameters")
    source_i, source_r, seed = cert["inner_source"], cert["outer_source"], cert["seed"]
    theta = Q(cert["theta"])
    check((source_i, source_r, seed, theta) == (2, 1, 6, Q(1, 4)), "one fixed case")
    delta = 1 - theta
    k_i, k_r = 7 - source_i, 7 - source_r
    inner_actions = [(c, s) for c in range(2) for s in range(k_i - 1)]
    outer_actions = [(c, s) for c in range(2) for s in range(k_r - 1)]
    check(cert["inner_actions_c_s"] == [list(a) for a in inner_actions], "inner action domain")
    check(cert["outer_actions_c_s"] == [list(a) for a in outer_actions], "outer action domain")

    masses = defaultdict(Q)
    k_values = []
    hist_columns = 0
    for column in point["columns"]:
        mass = Q(column["weight"])
        check(mass >= 0, "nonnegative point coordinate")
        if column["kind"] == "K":
            k_values.append(mass)
        elif column["kind"] == "hist":
            hist_columns += 1
            bits_text, d = column["actual_bits"], column["d"]
            check(len(bits_text) == 6 and set(bits_text) <= {"0", "1"}, "literal actual bits")
            check(isinstance(d, int) and 0 <= d <= 6, "comparison count domain")
            masses[(bits_text, d)] += mass
    check(len(k_values) == 1, "single K coordinate")
    K = k_values[0]
    masses = {key: mass for key, mass in masses.items() if mass > 0}
    incomes = [Q(0) for _ in range(6)]
    coverage = Q(0)
    for (bits_text, d), mass in masses.items():
        bits = [int(x) for x in bits_text]
        load = sum(bits)
        if load:
            coverage += mass
            for j, bit in enumerate(bits):
                incomes[j] += mass * Q(bit, load)
    check(coverage == Q(point["W"]) == sum(incomes), "actual coverage/income reconstruction")
    budget = [
        incomes[source_i - 1], (k_i - 2) * incomes[5], incomes[5],
        (k_i - 2) * K, K, *([Q(0)] * 9),
        incomes[source_r - 1], (k_r - 2) * incomes[5], incomes[5],
        (k_r - 2) * K, K,
    ]
    check(len(budget) == 19, "nineteen budget coordinates")
    check(budget == [Q(value) for value in cert["wallet"]], "all budgets agree")

    occupied_cost = [Q(0) for _ in range(19)]
    type_reports = []
    seen = set()
    for witness in cert["occupation_witnesses"]:
        key = (witness["actual_bits"], witness["d"])
        check(key not in seen and key in masses, "unique positive type witness")
        seen.add(key)
        mass = masses[key]
        check(mass == Q(witness["mass"]), "witness mass from original point")
        bits, d = [int(x) for x in key[0]], key[1]
        y_mass = [1 - Q(d, 6), Q(d, 6)]
        check(len(witness["outer_action_probabilities"]) == 2, "outer y rows")
        check(len(witness["inner_action_probabilities"]) == 4, "inner state rows")
        outer_prob = [
            probability_row(row, len(outer_actions), "outer probability")
            for row in witness["outer_action_probabilities"]
        ]
        inner_prob = [
            probability_row(row, len(inner_actions), "inner probability")
            for row in witness["inner_action_probabilities"]
        ]

        # The same outer terminal bit c becomes the inner previous bit.
        # This injection is derived, never accepted as independent input.
        initial = [Q(0) for _ in STATES]
        outer_cost = [Q(0) for _ in range(5)]
        for y in range(2):
            for probability, action in zip(outer_prob[y], outer_actions):
                c, s = action
                atom_mass = y_mass[y] * probability
                initial[2 * c + bits[seed - 1]] += atom_mass
                features = outer_features(bits, source_r, y, action)
                for j in range(5):
                    outer_cost[j] += atom_mass * features[j]
        check(initial == [Q(value) for value in witness["inner_initial_distribution"]], "outer-to-inner coupling")
        check(sum(initial) == 1 and all(value >= 0 for value in initial), "inner initial distribution")

        transition = [[Q(0) for _ in STATES] for _ in STATES]
        for q, (a, t) in enumerate(STATES):
            for probability, (c, s) in zip(inner_prob[q], inner_actions):
                transition[q][2 * t + c] += probability
        # Re-solve D = (1-theta)*initial + theta*P^T D exactly.
        flow_matrix = [
            [Q(q == predecessor) - theta * transition[predecessor][q] for predecessor in range(4)]
            for q in range(4)
        ]
        flow = solve_rational(flow_matrix, [delta * value for value in initial])
        check(flow == [Q(value) for value in witness["inner_discounted_flow"]], "exact independently solved flow")
        check(sum(flow) == 1 and all(value >= 0 for value in flow), "normalized nonnegative inner flow")
        for q in range(4):
            check(
                flow[q] - theta * sum(flow[p] * transition[p][q] for p in range(4)) == delta * initial[q],
                "discounted state conservation",
            )

        inner_cost = [Q(0) for _ in range(14)]
        for q, state in enumerate(STATES):
            for probability, action in zip(inner_prob[q], inner_actions):
                atom_mass = flow[q] * probability
                features = inner_features(bits, d, source_i, state, action)
                for j in range(14):
                    inner_cost[j] += atom_mass * features[j]
        for j, value in enumerate(inner_cost + outer_cost):
            occupied_cost[j] += mass * value
        type_reports.append({
            "actual_bits": key[0], "d": d, "mass": str(mass),
            "derived_inner_initial_distribution": [str(x) for x in initial],
            "independently_solved_inner_discounted_flow": [str(x) for x in flow],
            "inner_feature_expectations": [str(x) for x in inner_cost],
            "outer_feature_expectations": [str(x) for x in outer_cost],
            "flow_equations_exact": 4,
        })
    check(seen == set(masses), "complete positive mass type coverage")
    residual = [b - cost for b, cost in zip(budget, occupied_cost)]
    check(
        residual == [Q(cert["all_parameter_residuals"][name]) for name in NAMES],
        "all nineteen independently reconstructed residuals",
    )
    epsilon = min(residual)
    check(epsilon == Q(cert["normalized_cone_lower_bound"]), "exact full-cone lower bound")
    check(epsilon > 0, "strict positive lower bound")
    check(cert["nonseparation_certified"] is True, "certificate conclusion")
    check(cert["lp_variables"] == 19 + 6 * len(masses), "reported LP variable count")
    check(
        cert["lp_inequalities"] == len(masses) * (4 * len(inner_actions) + 2 * len(outer_actions)),
        "reported LP inequality count",
    )

    weights = [Q(x) for x in cert["parameters_full"]]
    check(len(weights) == 19 and all(x >= 0 for x in weights) and sum(weights) == 1, "reported weights normalized")
    report = {
        "scope": "Independent exact audit of one fixed 19-weight cone occupation witness; no SPE claim and no all-448 Bellman or full sparse-cut audit.",
        "point_path": str(POINT.relative_to(BASE)),
        "point_sha256": POINT_SHA,
        "certificate_path": str(CERT.relative_to(BASE)),
        "certificate_sha256": sha256(cert_bytes).hexdigest(),
        "inner_source": source_i, "outer_source": source_r, "seed": seed, "theta": str(theta),
        "point_verified_rows_as_reported": point["verified_rows"],
        "point_columns": len(point["columns"]),
        "hist_columns_reaggregated": hist_columns,
        "positive_customer_types": len(masses),
        "all_448_types_mathematically_allowed": True,
        "absent_or_zero_mass_types_need_no_dual_flow": True,
        "actual_incomes": [str(x) for x in incomes],
        "K": str(K), "actual_coverage": str(coverage),
        "parameter_names": NAMES,
        "recomputed_budgets": [str(x) for x in budget],
        "recomputed_occupation_cost": [str(x) for x in occupied_cost],
        "recomputed_residuals": {name: str(value) for name, value in zip(NAMES, residual)},
        "residuals_all_strictly_positive": True,
        "normalized_cone_slack_lower_bound": str(epsilon),
        "normalized_cone_slack_lower_bound_float": float(epsilon),
        "minimum_coordinates": [name for name, value in zip(NAMES, residual) if value == epsilon],
        "type_audits": type_reports,
        "exact_flow_equations_checked": 4 * len(masses),
        "exact_residual_coordinates_checked": len(residual),
        "passed": True,
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "passed": True, "positive_types": len(masses), "exact_flow_equations": 4 * len(masses),
        "residual_coordinates": len(residual), "lower_bound_float": float(epsilon),
        "output": str(OUT),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
