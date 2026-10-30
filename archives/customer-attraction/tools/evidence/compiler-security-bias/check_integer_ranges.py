"""Python-integer bounds for every int64 reduction in the frozen finite audit.

This checks the actual finite inputs' range contract. It does not repeat the
security computations or enlarge their mathematical validation domain.
"""
from pathlib import Path
import hashlib
import json
import math
import random


def main():
    limit = 2**63-1
    reports = []
    for p in range(2, 9):
        for n in range(2, p+1):
            rng = random.Random(100*p+n)
            x = [rng.randint(-4, 4) for _ in range((1 << p)-1)]
            M = sum(map(abs, x))
            K = 4*M+1
            r = [v+K for v in x]
            D = math.lcm(*range(1, n+1))
            L = math.comb(p, n-1)
            # mem@q <= n; each scaled payoff coefficient <= D;
            # a sum of L backgrounds has coefficient <= L*D;
            # its dot product with positive r <= L*D*sum(r).
            bounds = {"denominator": n, "absolute_signed_mass": M,
                      "largest_multiplicity": max(r),
                      "background_coefficient": L*D,
                      "sum_of_background_coefficients": ((1 << p)-1)*L*D,
                      "largest_weighted_reduction": L*D*sum(r)}
            assert min(r) > 0
            assert max(bounds.values()) < limit
            reports.append({"p": p, "n": n, "bounds": bounds})
    source = (Path(__file__).resolve().parent.parent / "continuation-security" /
              "history/source/notes/customer_attraction/uploaded_2026-10-10/auxiliary_counterexample.json")
    data = json.loads(source.read_text())
    weights = list(data["weights"].values())
    p, n = data["m"], data["n"]
    assert (p, n) == (12, 4) and min(weights) > 0
    D = math.lcm(*range(1, n+1))
    L = math.comb(p, n-1)
    certificate_bound = D*L*sum(weights)
    assert certificate_bound < limit
    result = {
        "status": "PASS", "int64_max": limit, "formula_cases": reports,
        "largest_formula_reduction_bound": max(r["bounds"]["largest_weighted_reduction"] for r in reports),
        "certificate": {"p": p, "n": n, "scaled_single_payoff_bound": D*sum(weights),
                        "sum_over_backgrounds_bound": certificate_bound,
                        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest()},
        "scope": "Only the finite frozen audit inputs. Bounds use unbounded Python integers and positivity; arbitrary future p,n or multiplicities need a new range argument."
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
