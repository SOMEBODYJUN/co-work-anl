"""Independent exact reconstruction of the two fractional-cover certificates.

Inputs are the mathematical row definitions and printed rational multipliers.
No original replay code, game solver, LP solver or floating-point arithmetic is
imported.  The 128-type checks are exhaustive coefficient checks, not a search
over finite SPE instances.  Global row validity remains a mathematical proof.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent


def actual_shares(bits):
    count = sum(bits)
    return [Q(bit, count) if bit else Q(0) for bit in bits]


def certificate(tau, floors, fourth, fifth=Q(0), pair=Q(0), endpoint=Q(0)):
    residuals, zeros, records = [], [], []
    for bits in product((0, 1), repeat=6):
        pay = actual_shares(bits)
        before = [sum(bits[:i]) for i in range(6)]
        p = before[4]
        kernel_den = (p + 1) * (p + 2)
        for member in (0, 1):
            safe = [tau * pay[i] - Q(member, before[i] + 6 - i)
                    for i in range(6)]
            to_last_4 = pay[3] - Q(bits[5], before[3] + 3)
            to_last_5 = pay[4] - Q(bits[5], before[4] + 2)
            pair_row = (pay[4] + pay[5] + Q(bits[4], kernel_den)
                        - member * (Q(2, 1) / (tau * (p + 1))
                                    - Q(1, 1) / (tau**2 * kernel_den)))
            endpoint_row = (tau * pay[4] + pay[5] / 2 - Q(member, p + 1)
                            + Q(member * bits[4] * (p == 0), 4))
            paid = sum(weight * row for weight, row in zip(floors, safe))
            paid += fourth * to_last_4 + fifth * to_last_5
            paid += pair * pair_row + endpoint * endpoint_row
            residual = 2 * bool(sum(bits)) - member - paid
            assert residual >= 0, (tau, bits, member, residual)
            residuals.append(residual)
            records.append({"actual_bits": bits, "comparison_bit": member,
                            "residual": str(residual)})
            if residual == 0:
                zeros.append({"actual_bits": list(bits), "comparison_bit": member})
    return {"tau": str(tau), "state_count": len(residuals),
            "minimum_residual": str(min(residuals)),
            "minimum_positive_residual": str(min(r for r in residuals if r > 0)),
            "zero_count": len(zeros), "zero_states": zeros,
            "floor_multipliers": list(map(str, floors)),
            "actual_fourth_to_B": str(fourth),
            "actual_fifth_to_B": str(fifth), "averaged_strong_PAIR": str(pair),
            "endpoint_row": str(endpoint), "all_residuals": records}


def endpoint_projection_corners(tau):
    checked, minimum = 0, None
    for p, a, member in product(range(5), (0, 1), (0, 1)):
        den = (p + 1) * (p + 2)
        for query, reply in product((Q(member, 1) / tau, Q(1)), (Q(0), Q(1))):
            # The actual-payoff terms cancel in R_x - tau*G_x.
            real_remainder = (-tau * query / (p + 1)
                              - reply / (2 * (p + a + 1))
                              + tau * query * reply / den)
            projected_remainder = -Q(member, p + 1) + Q(member * a * (p == 0), 4)
            slack = projected_remainder - real_remainder
            assert slack >= 0, (p, a, member, query, reply, slack)
            minimum = slack if minimum is None else min(minimum, slack)
            checked += 1
    return {"complete_rectangle_corners": checked, "minimum_slack": str(minimum)}


def strong_pair_identity():
    checked = 0
    for p, a, b, t, q, r in product(range(5), (0, 1), (0, 1),
                                   (0, 1), (0, 1), (0, 1)):
        den = (p + 1) * (p + 2)
        def payoff(first, second):
            return Q(first, p + 1 + second)
        first_ic = payoff(a, b) - payoff(t, r)
        reply_ic = payoff(r, t) - payoff(q, t)
        actual_last_ic = payoff(b, a) - payoff(r, a)
        left = (payoff(a, b) + payoff(b, a) + Q(a, den)
                - Q(t + q, p + 1) + Q(t * q, den))
        right = first_ic + reply_ic + actual_last_ic + Q(a * (1 - r), den)
        assert left == right
        checked += 1
    return {"raw_IC_identity_types": checked}


def compare_history(report, filename, extra_keys):
    saved = json.loads((ROOT / "original" / filename).read_text())
    keys = ("tau", "state_count", "minimum_residual", "minimum_positive_residual",
            "floor_multipliers", "actual_fourth_to_B", "zero_states") + extra_keys
    for key in keys:
        assert report[key] == saved[key], (filename, key, report[key], saved[key])
    if "minimum_by_actual_count" in saved:
        by_count = {}
        for count in range(7):
            vals = [Q(row["residual"]) for row in report["all_residuals"]
                    if sum(row["actual_bits"]) == count]
            by_count[str(count)] = str(min(vals))
        assert by_count == saved["minimum_by_actual_count"]
    return {"historical_report": filename, "compared_fields": list(keys),
            "all_fields_matched": True}


def main():
    pair = certificate(Q(21, 5), list(map(Q, [
        "2784735/10526656", "240968825/852659136", "65773795/213164784",
        "820179895/4547515392", "14864915/252639744", "9728723/24060928"])),
        Q(99135297, 120304640), Q(9429757, 30076160), Q(8821071, 12030464))
    den = 961717337
    endpoint = certificate(Q(9, 2), [Q(n, den) for n in
        (218088780, 226476810, 236182380, 177467790, 0, 428553180)],
        Q(515142618, den), endpoint=Q(333319140, den))
    comparisons = [compare_history(pair, "fractional_cover_pair_half_audit.json",
                                  ("actual_fifth_to_B", "averaged_strong_PAIR")),
                   compare_history(endpoint, "fractional_cover_endpoint_half_audit.json",
                                   ("endpoint_row",))]
    report = {"scope": "complete local coefficients; not an unrestricted half theorem",
              "pair_21_5": pair, "endpoint_9_2": endpoint,
              "projection": endpoint_projection_corners(Q(9, 2)),
              "strong_pair": strong_pair_identity(), "historical_comparisons": comparisons}
    target = ROOT / "replay" / "independent-coefficients.json"
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"pair_types": pair["state_count"], "pair_zeros": pair["zero_count"],
                      "endpoint_types": endpoint["state_count"],
                      "endpoint_zeros": endpoint["zero_count"],
                      "projection": report["projection"], "strong_pair": report["strong_pair"],
                      "historical_reports_match": True}, indent=2))


if __name__ == "__main__":
    main()
