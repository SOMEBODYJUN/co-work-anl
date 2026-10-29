"""Independent definition-level Fraction audit of CA-FIVE-REPLY-UPPER.

This file does not import the author's coefficient function, any LP code,
or any SPE solver.  The 24 rows are rebuilt below from the manuscript's
individual terminal shares and legally specified comparison histories.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = ROOT / "evidence/certificates/customer_attraction/five_player_reply_bound.json"
MANUSCRIPT = ROOT / "research/current/customer_attraction/five_player_reply_bound.md"
BOUND = F(493266145873827, 234749688354196)
DENOMINATOR = 1173748441770980
LABELS = tuple("ABCDEUVWXY")
PATH_INDICES = ((0, 1, 2, 3, 4), (0, 4, 5, 6, 7), (0, 1, 4, 8, 9))
NAMES = (
    "actual:1:K:D", "actual:1:K:V", "actual:1:K:W", "actual:1:K:X",
    "actual:2:K:V", "actual:2:K:W", "actual:2:K:X", "actual:2:K:Y",
    "actual:5:K:U", "actual:5:K:X", "actual:5:K:Y",
    "actual:5:O", "actual:reply:S+V", "actual:reply:Z", "actual:2:sum-L-actual",
    "second:5:O", "second:reply:S+V", "second:reply:Z", "second:3:sum-L-second",
    "third:5:O", "third:reply:S+V", "third:reply:Z", "F:second", "F:third",
)
NUMERATORS = (
    1010775320864075, 203305644703550, 203734050769100, 119470340624425,
    19790064200, 6247927899920, 132636459795280, 317937396273980,
    30987053899920, 238453047205485, 238453047205485,
    600700880375520, 89759346533228, 1970066568299, 171638426793260,
    7941762097920, 1415808183528, 519996327840, 563723291772,
    58516085203800, 10142788101992, 5071394050996, 418992950206260,
    1525319287645720,
)
EXPECTED_MINIMA = (
    0, 0, 0, 33787799191020600, 35644333391981100, 26312270041902900, 0,
    39570994049198600, 18352830214258200, 1062579276463200, 0,
    20085137676333200, 9885320187038200, 15597170349671800,
    870090456771950, 29256266152440950, 41060538182699400,
    7735274982211200, 8995605516109920, 21324995575968120,
    18880925703148120, 16837028249306720, 6240740486985270,
    28528711039627970, 6081507332903600, 0, 0, 15686380873567330,
    0, 8499737116717530, 1301205546691780, 22158447840456840,
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def terminal_shares(memberships):
    """One customer's five actual shares, including zero own membership."""
    load = sum(memberships)
    return tuple(F(bit, load) if bit else F(0) for bit in memberships)


def background_share(own, prefix_load, other):
    return F(own, prefix_load + own + other) if own else F(0)


def audit_raw_reply_rows():
    """Expand every one of the 20 ordered cross-reply comparisons explicitly."""
    cases = individual_cross_rows = 0
    for p in range(4):
        for bits in product((0, 1), repeat=10):
            chosen, replies = bits[:5], bits[5:]
            d, ell = sum(chosen), sum(replies)
            h = sum(t * reply for t, reply in zip(chosen, replies))
            den = (p + 1) * (p + 2)
            deviation_total = sum(
                (background_share(t, p, reply) for t, reply in zip(chosen, replies)), F(0)
            )
            cross_total = sum(
                (background_share(replies[i], p, chosen[i])
                 - background_share(replies[j], p, chosen[i])
                 for i in range(5) for j in range(5) if i != j), F(0)
            )
            require(deviation_total == F(d, p + 1) - F(h, den), "S expansion")
            require(cross_total == F(d * ell - 5 * h, den), "20-row V expansion")
            for fourth, fifth in product((0, 1), repeat=2):
                v4 = background_share(fourth, p, fifth)
                v5 = background_share(fifth, p, fourth)
                S = 5 * v4 - deviation_total
                require(5 * S + cross_total == 25 * v4 - F(5 * d, p + 1)
                        + F(d * ell, den), "N=5S+V cancellation")
                Z = 5 * v5 - sum(
                    (background_share(reply, p, fourth) for reply in replies), F(0)
                )
                require(Z == 5 * v5 - F(ell, p + fourth + 1), "Z expansion")
                cases += 1
            individual_cross_rows += 20
    return cases, individual_cross_rows


def rebuild_affine_rows(bits, optimal_count):
    """Explicitly reconstruct 24 rows; return their values at ell=(0,0,0).

    Also return the three exact slopes of their weighted sum.  This independently
    records why ell dependence is affine instead of assuming a corner contract.
    """
    paths = tuple(tuple(bits[i] for i in indices) for indices in PATH_INDICES)
    shares = tuple(terminal_shares(path) for path in paths)
    actual, second, third = shares
    a, b, c, fourth, e, u, v, w, x, y = bits
    opt = int(optimal_count > 0)
    prefixes = tuple(sum(path[:3]) for path in paths)
    before_last = tuple(sum(path[:4]) for path in paths)
    rows = [
        actual[0] - F(fourth, 5), actual[0] - F(v, 5),
        actual[0] - F(w, 5), actual[0] - F(x, 5),
        actual[1] - F(v, a + 4), actual[1] - F(w, a + 4),
        actual[1] - F(x, a + 4), actual[1] - F(y, a + 4),
        actual[4] - F(u, before_last[0] + 1),
        actual[4] - F(x, before_last[0] + 1),
        actual[4] - F(y, before_last[0] + 1),
        5 * actual[4] + F(before_last[0], before_last[0] + 1) - opt,
        25 * actual[3] - F(5 * optimal_count, prefixes[0] + 1),
        5 * actual[4], 5 * actual[1],
        5 * second[4] + F(before_last[1], before_last[1] + 1) - opt,
        25 * second[3] - F(5 * optimal_count, prefixes[1] + 1),
        5 * second[4], 5 * second[2],
        5 * third[4] + F(before_last[2], before_last[2] + 1) - opt,
        25 * third[3] - F(5 * optimal_count, prefixes[2] + 1),
        5 * third[4], actual[1] - second[1], actual[2] - third[2],
    ]
    coefficients = tuple(F(v, DENOMINATOR) for v in NUMERATORS)
    weighted_base = sum((coef * row for coef, row in zip(coefficients, rows)), F(0))
    slopes = []
    for r, (N_index, Z_index) in enumerate(((12, 13), (16, 17), (20, 21))):
        p = prefixes[r]
        slope = coefficients[N_index] * F(optimal_count, (p + 1) * (p + 2))
        slope -= coefficients[Z_index] * F(1, before_last[r] + 1)
        if r == 0:
            slope -= coefficients[14] * F(1, a + 4)
        elif r == 1:
            slope -= coefficients[18] * F(1, a + e + 3)
        slopes.append(slope)
    return weighted_base, tuple(slopes)


def audit_optimum_charging_and_guarantees():
    checks = 0
    for p in range(5):
        for d in range(6):
            require(F(d, p + 1) >= int(d > 0) - F(p, p + 1),
                    "last-node optimum charging")
            checks += 1
    # After a deviation there are k future/current players, at most k of whom
    # can cover this customer's chosen theme; the actual count is 1,...,k.
    for position in range(5):
        k = 5 - position
        for prefix_load in range(position + 1):
            for additional_load in range(1, k + 1):
                require(F(1, prefix_load + additional_load)
                        >= F(1, prefix_load + k), "worst final denominator")
                checks += 1
    return checks


def check():
    certificate = json.loads(CERTIFICATE.read_text())
    expected_weights = {name: F(n, DENOMINATOR) for name, n in zip(NAMES, NUMERATORS)}
    require(F(certificate["bound"]) == BOUND, "bound differs from reviewed fraction")
    require({name: F(v) for name, v in certificate["multipliers"].items()}
            == expected_weights, "certificate differs from independently transcribed 24 rows")
    require(certificate["claim"] == "CA-FIVE-REPLY-UPPER", "claim ID")
    require(certificate["labels"] == list(LABELS), "labels")
    require(certificate["paths"] == {name: [LABELS[i] for i in path]
            for name, path in zip(("actual", "second", "third"), PATH_INDICES)}, "paths")
    require(all(n >= 0 for n in NUMERATORS), "negative multiplier")
    require(2 < BOUND < F(211, 100), "scope: this is strictly above two")

    raw_cases, cross_rows = audit_raw_reply_rows()
    charging_checks = audit_optimum_charging_and_guarantees()
    minima = [None] * 32
    corners = zeros = integer_points = 0
    scale = 120 * DENOMINATOR
    # No author's coefficient core is read: every Fraction base and slope
    # comes from the individual-share reconstruction above.
    for bits in product((0, 1), repeat=10):
        actual_index = sum(bit << (4 - i) for i, bit in enumerate(bits[:5]))
        coverage = int(any(bits[:5]))
        for d in range(6):
            base_G, slopes_G = rebuild_affine_rows(bits, d)
            base_rho = BOUND * coverage - int(d > 0) - base_G
            slopes_rho = tuple(-s for s in slopes_G)
            scaled = (base_rho * scale,) + tuple(s * scale for s in slopes_rho)
            require(all(v.denominator == 1 for v in scaled), "exact integer residual scale")
            integer_base, s0, s2, s3 = (int(v) for v in scaled)
            for ell in product((0, 5), repeat=3):
                rho = base_rho + sum((l * slope for l, slope in zip(ell, slopes_rho)), F(0))
                require(rho >= 0, f"negative corner: {bits}, d={d}, ell={ell}")
                require(rho * scale == integer_base + ell[0] * s0 + ell[1] * s2 + ell[2] * s3,
                        "Fraction/integer residual disagreement")
                value = int(rho * scale)
                minima[actual_index] = value if minima[actual_index] is None else min(minima[actual_index], value)
                corners += 1
                zeros += rho == 0
            # Exhaust actual integer ell ranges as an extra exact check of
            # the proved affine extension; correlated menus are included.
            for ell in product(range(6), repeat=3):
                require(integer_base + ell[0] * s0 + ell[1] * s2 + ell[2] * s3 >= 0,
                        "negative interior menu multiplicity")
                integer_points += 1
    require(tuple(minima) == EXPECTED_MINIMA, "manuscript's 32-case table")
    require(corners == 49152 and zeros == 157, "complete corner counts")
    return {
        "claim": "CA-FIVE-REPLY-UPPER", "exact_bound": str(BOUND),
        "independent_definition_reconstruction": True,
        "imports_author_coefficient_core": False,
        "raw_reply_membership_cases": raw_cases,
        "explicit_ordered_cross_reply_rows": cross_rows,
        "optimum_charging_and_denominator_checks": charging_checks,
        "corner_residual_checks": corners, "zero_corner_residuals": zeros,
        "integer_menu_residual_checks": integer_points,
        "minimum_scaled_residual_by_actual_ABCDE": minima,
        "residual_scale": scale,
        "all_checks_passed": True,
        "certificate_sha256": sha256(CERTIFICATE.read_bytes()).hexdigest(),
        "manuscript_sha256": sha256(MANUSCRIPT.read_bytes()).hexdigest(),
        "independent_script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "scope": "Universal per-customer algebra and raw reply identities; ordered-node legality is separately reviewed. Exactly five root players, no prior background. The bound is above two; no half-coverage conclusion or SPE counterexample.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(check(), ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
