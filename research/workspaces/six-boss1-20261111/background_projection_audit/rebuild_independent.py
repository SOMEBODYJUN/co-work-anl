#!/usr/bin/env python3
"""Independent rational audit; reads frozen inputs, writes only this directory.

No optimizer, old oracle, Main builder import, Git, registry, or network access.
The conditional hidden-domain lower bounds are inherited from the source proof.
This script checks their stored finite projection arithmetic independently.
"""

from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


OUT = Path(__file__).resolve().parent
REPO = OUT.parents[3]
WS_REL = "research/workspaces/six-boss1-20261111"
KAPPA = Q(226487, 10**21)
PINS = {
    "owner": (
        "archives/customer-attraction/state/引理/一位背景五人利润的独占客户收费--引理.md",
        "aa6cff0f7e8f9eafafba6a8135adf8c45debc7a665d1f87fb69f6dbf738e03d8",
    ),
    "b0": (
        WS_REL + "/background_five_bridge/fixed53_b0_profit.json",
        "0e5ab5156e98eda9e967e8227e760c7181e77d4db78540aee8b367b1769861ed",
    ),
    "b1": (
        WS_REL + "/background_five_bridge/fixed53_b1_profit.json",
        "ece4ff20dfd3fc6f7a33c2efd6a7b4af4f21fb2089523a13517246746aabfa64",
    ),
    "main_projection": (
        WS_REL + "/main_background_projection/exact_projection.json",
        "f39ae91167d96f015c188159e3efb9dcbf7436640e058467b0ead1386c4744cc",
    ),
    "v3": (
        WS_REL + "/universal_union_wallet_v3/exact_certificate.json",
        "1d9a898e3ca429b6af3611f01ada831ad50cf7f0708f14d7c518478573f0a9e3",
    ),
    "v4": (
        WS_REL + "/universal_union_wallet_v4/exact_certificate.json",
        "290f90feba9bf7ec8232e16e59f02b7f4e05dc41413f14510592c3d16ef28819",
    ),
}


def check(condition, description):
    if not condition:
        raise AssertionError(description)


def read_pinned(name, as_json=True):
    relative_path, expected = PINS[name]
    content = (REPO / relative_path).read_bytes()
    actual = sha256(content).hexdigest()
    check(actual == expected, f"Input pin mismatch: {name}")
    return json.loads(content) if as_json else content


def decimal(value):
    with localcontext() as context:
        context.prec = 65
        return str(Decimal(value.numerator) / Decimal(value.denominator))


def write_json(filename, value):
    (OUT / filename).write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def bits_of(number, length):
    return format(number, f"0{length}b")


def comparison_share(background, multiplicity):
    check(0 <= multiplicity <= 5, "Five-slot table accessed outside 0..5")
    return Q(multiplicity, background + multiplicity) if multiplicity else Q(0)


read_pinned("owner", as_json=False)

# Construct all 384 minima directly from the 12288 conditional values.
# The saved 192-entry summaries are used only after the reconstruction.
minima = {}
group_output = []
source_checks = []
for background in (0, 1):
    table = read_pinned(f"b{background}")
    check(table["background"] == background, "Background mode mismatch")
    check(table["mode"] == "profit", "Profit/coverage mode mismatch")
    check(table["positive_outer_multipliers"] == 53, "Wrong source row count")
    check(Q(table["K_residual"]) == KAPPA, "Wrong source K residual sign/value")
    scale = int(table["residual_scale"])
    check(scale > 0, "Nonpositive residual scale")
    conditional = {}
    for entry in table["all_6144_conditional_residuals"]:
        bits = entry["bits"]
        k = entry["d"]
        check(
            isinstance(bits, str) and len(bits) == 10 and set(bits) <= {"0", "1"},
            "Malformed ABCDEUVWXY type",
        )
        check(type(k) is int and 0 <= k <= 5, "Malformed five-slot multiplicity")
        key = (bits, k)
        check(key not in conditional, "Duplicate conditional type")
        rho = Q(entry["rho"])
        check(rho * scale == int(entry["scaled_integer"]), "Scaled rho mismatch")
        conditional[key] = rho
    expected_keys = {
        (bits_of(number, 10), k) for number in range(1024) for k in range(6)
    }
    check(set(conditional) == expected_keys, "Incomplete conditional domain")
    check(len(conditional) == 6144, "Wrong conditional domain cardinality")
    check(min(conditional.values()) == Q(table["min_rho"]), "Global rho mismatch")
    check(
        sum(value < 0 for value in conditional.values())
        == table["negative_conditional_cases"],
        "Negative conditional count mismatch",
    )

    source_summary = {}
    for saved in table["min_by_actual_and_d"]:
        key = (saved["actual"], saved["d"])
        check(key not in source_summary, "Duplicate source minimum key")
        source_summary[key] = saved
    expected_summary_keys = {
        (bits_of(number, 5), k) for number in range(32) for k in range(6)
    }
    check(set(source_summary) == expected_summary_keys, "Incomplete saved minima")

    negative_minima = 0
    for number in range(32):
        actual = bits_of(number, 5)
        for k in range(6):
            members = [
                (bits_of(hidden, 5), conditional[(actual + bits_of(hidden, 5), k)])
                for hidden in range(32)
            ]
            minimum = min(value for _, value in members)
            minima[(background, actual, k)] = minimum
            negative_minima += minimum < 0
            saved = source_summary[(actual, k)]
            check(minimum == Q(saved["min_rho"]), "Rebuilt minimum differs")
            witness = saved["witness"]
            check(witness["bits"][:5] == actual, "Minimum witness actual mismatch")
            check(witness["d"] == k, "Minimum witness multiplicity mismatch")
            check(Q(witness["rho"]) == minimum, "Minimum witness rho mismatch")
            check(
                conditional[(witness["bits"], k)] == minimum,
                "Witness does not attain the conditional minimum",
            )
            group_output.append(
                {
                    "background": background,
                    "actual_ABCDE": actual,
                    "five_slot_multiplicity": k,
                    "conditional_count": len(members),
                    "minimum": str(minimum),
                    "attaining_UVWXY": [
                        hidden for hidden, value in members if value == minimum
                    ],
                    "all_32_conditionals": [
                        {"UVWXY": hidden, "rho": str(value)}
                        for hidden, value in members
                    ],
                }
            )
    source_checks.append(
        {
            "background": background,
            "mode": table["mode"],
            "unique_conditionals": len(conditional),
            "groups": len(source_summary),
            "conditionals_per_group": 32,
            "scaled_integer_checks": len(conditional),
            "source_minimum_matches": len(source_summary),
            "negative_conditionals": sum(v < 0 for v in conditional.values()),
            "negative_minima": negative_minima,
            "global_minimum": str(min(conditional.values())),
            "K_residual": str(Q(table["K_residual"])),
        }
    )
check(len(minima) == 384, "Wrong rebuilt minimum count")

# Average the six literal deleted indices. These are indexed slots, so repeated
# labels remain repeated. Then check the closed two-term formula independently.
averages = {}
average_output = []
literal_pattern_checks = 0
for background in (0, 1):
    for number in range(32):
        actual = bits_of(number, 5)

        def term(k):
            return comparison_share(background, k) + minima[(background, actual, k)]

        for d in range(7):
            canonical_pattern = [1] * d + [0] * (6 - d)
            remaining = [sum(canonical_pattern) - bit for bit in canonical_pattern]
            check(all(0 <= k <= 5 for k in remaining), "Invalid deleted count")
            direct = sum((term(k) for k in remaining), Q(0)) / 6
            formula = Q(0)
            if d != 6:
                formula += Q(6 - d, 6) * term(d)
            if d != 0:
                formula += Q(d, 6) * term(d - 1)
            check(direct == formula, "Six-deletion/formula mismatch")
            averages[(background, actual, d)] = direct
            average_output.append(
                {
                    "background": background,
                    "actual_ABCDE": actual,
                    "six_slot_multiplicity": d,
                    "canonical_six_slot_membership": canonical_pattern,
                    "remaining_count_after_each_deletion": remaining,
                    "remaining_count_frequencies": {
                        str(k): count for k, count in sorted(Counter(remaining).items())
                    },
                    "six_literal_terms": [str(term(k)) for k in remaining],
                    "literal_average": str(direct),
                    "closed_formula_average": str(formula),
                }
            )
        for pattern in product((0, 1), repeat=6):
            d = sum(pattern)
            direct = sum((term(d - bit) for bit in pattern), Q(0)) / 6
            check(
                direct == averages[(background, actual, d)],
                "Deleting a noncanonical slot pattern changed the mean",
            )
            literal_pattern_checks += 1
check(len(averages) == 448, "Wrong deletion average count")
check(literal_pattern_checks == 4096, "Wrong literal six-slot pattern count")

# Make all 256 columns before reading Main's output. Integer column indices use
# lexicographic binary a1,a2,a3,a4,a5,a6,x,o; column 256 is the common K.
customer_rows = []
coefficients = {}
for index in range(256):
    bits = tuple(int(character) for character in bits_of(index, 8))
    background = bits[0]
    actual = "".join(str(bit) for bit in bits[1:6])
    allowed = [0] if bits[7] == 0 else list(range(1, 7))
    g_values = {d: averages[(background, actual, d)] for d in allowed}
    gbar = min(g_values.values())
    actual_load = sum(bits[:6])
    tail_share = Q(sum(bits[1:6]), actual_load) if actual_load else Q(0)
    coefficient = 2 * tail_share - gbar
    coefficients[index] = coefficient
    customer_rows.append(
        {
            "index": index,
            "bits_a1_a2_a3_a4_a5_a6_x_o": list(bits),
            "true_tail_profit_share": str(tail_share),
            "all_allowed_d": {str(d): str(value) for d, value in g_values.items()},
            "gbar": str(gbar),
            "attaining_d": [d for d, value in g_values.items() if value == gbar],
            "coefficient": str(coefficient),
        }
    )
coefficients[256] = -KAPPA
for index in range(256):
    check(coefficients[index] == coefficients[index ^ 2], "X invariance failed")
check(coefficients[0] == 0, "Zero type not retained correctly")
check(coefficients[256] < 0, "K coefficient sign reversed")

# Read the Main JSON only as a comparison target after independent construction.
main = read_pinned("main_projection")
check(
    set(main["all257_coefficients"]) == {str(i) for i in range(257)},
    "Main coefficient columns not exactly 0..256",
)
for index in range(257):
    check(
        coefficients[index] == Q(main["all257_coefficients"][str(index)]),
        f"Main coefficient mismatch at {index}",
    )
main_minima = {}
for entry in main["all256_d_minima"]:
    check(entry["index"] not in main_minima, "Duplicate Main customer type")
    main_minima[entry["index"]] = entry
check(set(main_minima) == set(range(256)), "Main customer domain incomplete")
allowed_value_comparisons = 0
for independent in customer_rows:
    entry = main_minima[independent["index"]]
    check(entry["bits"] == independent["bits_a1_a2_a3_a4_a5_a6_x_o"], "Bit order")
    check(Q(entry["minimum"]) == Q(independent["gbar"]), "Main gbar mismatch")
    check(entry["attaining_d"] == independent["attaining_d"], "Argmin mismatch")
    check(
        {int(d): Q(value) for d, value in entry["all_allowed_d"].items()}
        == {int(d): Q(value) for d, value in independent["all_allowed_d"].items()},
        "Main allowed multiplicity values mismatch",
    )
    allowed_value_comparisons += len(independent["all_allowed_d"])
check(allowed_value_comparisons == 896, "Wrong allowed d comparison count")

# Reconstruct the two point vectors independently from their exact certificates.
# Checks of W, O, individual profits and label sizes also verify the bit routing.
point_output = {}
for version in ("v3", "v4"):
    certificate = read_pinned(version)
    nonzero = {int(index): Q(value) for index, value in certificate["primal"].items()}
    check(set(nonzero) <= set(range(257)), "Certificate column outside domain")
    check(all(value >= 0 for value in nonzero.values()), "Negative point mass")
    values = [nonzero.get(index, Q(0)) for index in range(257)]
    K = values[256]
    check(K == Q(certificate["K"]), "Certificate K routing mismatch")
    common = int(certificate["common_denominator"])
    check(
        set(certificate["integer_scaled_primal"]) == set(certificate["primal"]),
        "Scaled point support mismatch",
    )
    for index, value in nonzero.items():
        check(
            value * common == int(certificate["integer_scaled_primal"][str(index)]),
            "Scaled point value mismatch",
        )
    W = Q(0)
    O = Q(0)
    u = [Q(0) for _ in range(6)]
    sizes = [Q(0) for _ in range(7)]
    gbar_sum = Q(0)
    summands = []
    for row in customer_rows:
        index = row["index"]
        mass = values[index]
        bits = row["bits_a1_a2_a3_a4_a5_a6_x_o"]
        actual_load = sum(bits[:6])
        W += mass * int(actual_load > 0)
        O += mass * bits[7]
        for i in range(6):
            u[i] += mass * (Q(bits[i], actual_load) if actual_load else Q(0))
        for i in range(7):
            sizes[i] += mass * bits[i]
        gbar_sum += mass * Q(row["gbar"])
        if mass:
            summands.append(
                {
                    "column": index,
                    "mass": str(mass),
                    "coefficient": str(coefficients[index]),
                    "product": str(mass * coefficients[index]),
                }
            )
    check(O == 1, "Point normalization is not O=1")
    check(W == Q(certificate["objective"]), "Point W routing mismatch")
    check(u == list(map(Q, certificate["derived"]["u1_u6"])), "Profit routing mismatch")
    check(
        sizes == list(map(Q, certificate["derived"]["sizes_A1_A6_X"])),
        "Label size routing mismatch",
    )
    V = sum(u[1:], Q(0))
    check(V == W - u[0], "True tail profit is not W-u1")
    value = sum((values[i] * coefficients[i] for i in range(257)), Q(0))
    check(value == 2 * V - KAPPA * K - gbar_sum, "Two point evaluations disagree")
    main_point = main["point_evaluations"]["universal_union_wallet_" + version]
    check(Q(main_point["value"]) == value, "Main point evaluation mismatch")
    check(
        main_point["certificate_sha256"] == PINS[version][1],
        "Main used a different certificate",
    )
    check(value < 0 if version == "v3" else value > 0, "Unexpected point sign")
    summands.append(
        {
            "column": 256,
            "mass": str(K),
            "coefficient": str(-KAPPA),
            "product": str(-KAPPA * K),
        }
    )
    point_output[version] = {
        "certificate_sha256": PINS[version][1],
        "positive_columns": sorted(i for i, value_i in nonzero.items() if value_i > 0),
        "W": str(W),
        "O": str(O),
        "u1": str(u[0]),
        "V_true_tail_profit": str(V),
        "K": str(K),
        "twice_V": str(2 * V),
        "minus_kappa_K": str(-KAPPA * K),
        "gbar_mass_sum": str(gbar_sum),
        "value": str(value),
        "decimal": decimal(value),
        "sign": "negative" if value < 0 else "positive",
        "all_nonzero_column_summands": summands,
        "interpretation": (
            "This representative point violates the necessary row; no whole-face claim."
            if value < 0
            else "This representative point satisfies this row; no SPE realization claim."
        ),
    }

result = {
    "status": "PASS_INDEPENDENT_EXACT_BACKGROUND_PROJECTION_AUDIT",
    "optimizer_calls": 0,
    "new_original_hidden_domain_oracle_runs": 0,
    "imports_or_executions_of_Main_builder": 0,
    "source_scope": (
        "Inherited registered full-domain 53-row one-prefix/five-tail profit identity. "
        "Independent arithmetic starts from the frozen 12288 conditional lower bounds."
    ),
    "not_claimed": [
        "No independent re-enumeration of the old hidden histogram/menu oracle.",
        "No reproof of all original 53 source IC rows.",
        "No proof of six-player half, and no complete SPE counterexample.",
        "No optimum-face exclusion inferred from a representative point.",
        "No feasibility or optimum verification of the entire v3/v4 LP systems.",
    ],
    "input_pins": {
        name: {"path": relative, "sha256": digest}
        for name, (relative, digest) in PINS.items()
    },
    "independent_code_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
    "source_checks": source_checks,
    "counts": {
        "conditional_values_reconstructed": 12288,
        "unique_minimum_groups": 384,
        "group_size": 32,
        "six_slot_multiplicity_means": 448,
        "literal_membership_patterns_checked": literal_pattern_checks,
        "literal_index_deletions_checked": 6 * literal_pattern_checks,
        "customer_types": 256,
        "common_K_columns": 1,
        "X_invariance_pairs": 128,
        "o_zero_customer_types": 128,
        "Main_coefficients_exactly_matched": 257,
        "Main_projected_minima_exactly_matched": 256,
        "Main_allowed_d_values_exactly_matched": allowed_value_comparisons,
        "certificate_points_evaluated": 2,
    },
    "K_coefficient": str(-KAPPA),
    "all257_coefficients": {str(i): str(coefficients[i]) for i in range(257)},
    "all256_customer_rows": customer_rows,
    "point_evaluations": point_output,
}
write_json("conditional_minima.json", {"source_checks": source_checks, "groups": group_output})
write_json(
    "deletion_averages.json",
    {
        "literal_membership_patterns_checked": literal_pattern_checks,
        "literal_index_deletions_checked": 6 * literal_pattern_checks,
        "all448_averages": average_output,
    },
)
write_json("audit_result.json", result)
print(result["status"])
print(json.dumps(result["counts"], ensure_ascii=False, sort_keys=True))
for version, point in point_output.items():
    print(version, point["value"], point["decimal"])
