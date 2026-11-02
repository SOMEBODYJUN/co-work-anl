"""Bounded replay of the unmodified frozen simple_search source.

The numerical failures are reported as numerical failures, not exact Farkas
certificates.  The exact positive fixture is the already known P3 certificate.
"""
from fractions import Fraction as F
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
from pathlib import Path
import json
import platform
import scipy
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "source.py"
EXPECTED_SHA = "058d349814061f75df9e94b5d18482f3659ab91c6182942e26715593c362fec9"


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def independent_rows(bits, d, ell):
    """Reconstruct the 43 exact columns from the real-IC formulas."""
    p, a, b = sum(bits[:4]), bits[4], bits[5]
    c = sum(bits)
    actual = [F(e, c) if e else F(0) for e in bits]
    alpha, beta = actual[4:]
    denominator = (p + 1) * (p + 2)
    # Recover G from S, Z, V at every feasible same-index overlap.
    values = set()
    for overlap in range(max(0, d + ell - 6), min(d, ell) + 1):
        S = 6 * alpha - F(d, p + 1) + F(overlap, denominator)
        Z = 6 * beta - F(ell, p + a + 1)
        V = F(d * ell - 6 * overlap, denominator)
        values.add(S + Z / 12 + V / 6)
    check(len(values) == 1, "G did not eliminate the overlap")
    result = [values.pop()]
    for position in range(1, 6):
        safe_denominator = sum(bits[:position - 1]) + 7 - position
        result.extend(actual[position - 1] - F(bits[j], safe_denominator)
                      for j in range(6))
    for position in range(1, 6):
        safe_denominator = sum(bits[:position - 1]) + 7 - position
        result.append(6 * actual[position - 1] - F(d, safe_denominator))
    result.extend(beta - F(bits[j], p + a + 1) for j in range(6))
    result.append(6 * beta - F(d, p + a + 1))
    return result


def main():
    check(sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED_SHA, "source SHA mismatch")
    spec = spec_from_file_location("frozen_simple_search", SOURCE)
    source = module_from_spec(spec)
    spec.loader.exec_module(source)
    expected_names = (["G"] +
                      [f"safe_{i}_{j}" for i in range(5) for j in range(6)] +
                      [f"safe_{i}_opt" for i in range(5)] +
                      [f"last_{j}" for j in range(6)] + ["last_opt"])
    all_names, _, _, all_metas = source.build(0)
    check(all_names == expected_names and len(all_names) == 43, "column contract mismatch")
    checked = 0
    for bits, d, ell, exact in all_metas:
        check(exact == independent_rows(bits, d, ell), "exact coefficient mismatch")
        checked += 1
    check(checked == 3136, "unrestricted domain mismatch")

    report = {
        "source_sha256": EXPECTED_SHA,
        "python": platform.python_version(),
        "scipy": scipy.__version__,
        "column_count": len(all_names),
        "column_names": all_names,
        "independently_checked_exact_rows": checked,
        "numerical_searches": [],
        "known_P3_certificate_checks": [],
        "exact_infeasibility_certificate_produced": False,
    }
    certificate = {"G": F(1), "safe_0_4": F(1, 3), "safe_1_4": F(1, 2),
                   "safe_2_4": F(1, 2), "safe_3_4": F(2, 3), "last_4": F(3, 2)}
    expected_counts = {0: 3136, 1: 3038, 2: 2646, 3: 2058}
    for pmin in range(4):
        names, rows, rhs, metas = source.build(pmin)
        expected_states = [(bits, d, ell) for bits in product((0, 1), repeat=6)
                           if not bits[4] or sum(bits[:4]) >= pmin
                           for d, ell in product(range(7), repeat=2)]
        check([(bits, d, ell) for bits, d, ell, _ in metas] == expected_states,
              "restricted domain mismatch")
        check(len(rows) == expected_counts[pmin], "unexpected row count")
        for float_row, target, (bits, d, ell, exact) in zip(rows, rhs, metas):
            check(float_row == list(map(float, exact)), "float conversion mismatch")
            check(target == 2 * int(sum(bits) > 0) - int(d > 0), "target mismatch")
        if pmin < 3:
            result = linprog([0] * len(names), A_ub=rows, b_ub=rhs,
                             bounds=[(0, None)] * len(names), method="highs")
            report["numerical_searches"].append({
                "pmin": pmin, "row_count": len(rows),
                "success": bool(result.success), "status": int(result.status),
                "message": str(result.message),
            })
            check(not result.success and result.status == 2,
                  "historical numerical infeasibility was not reproduced")
        multipliers = [certificate.get(name, F(0)) for name in names]
        residuals = [F(target) - sum(weight * coefficient
                                   for weight, coefficient in zip(multipliers, exact))
                     for target, (_, _, _, exact) in zip(rhs, metas)]
        report["known_P3_certificate_checks"].append({
            "pmin": pmin, "state_count": len(residuals),
            "minimum": str(min(residuals)),
            "negative_count": sum(value < 0 for value in residuals),
        })
        if pmin == 3:
            check(min(residuals) == 0 and all(value >= 0 for value in residuals),
                  "known P3 certificate did not pass its exact domain")
    report["known_P3_certificate"] = {name: str(value) for name, value in certificate.items()}
    check(sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED_SHA, "source changed during replay")
    report["status"] = "exact-coefficients-and-known-P3-passed; numerical-P0-P1-P2-infeasible"
    (HERE / "replay_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
