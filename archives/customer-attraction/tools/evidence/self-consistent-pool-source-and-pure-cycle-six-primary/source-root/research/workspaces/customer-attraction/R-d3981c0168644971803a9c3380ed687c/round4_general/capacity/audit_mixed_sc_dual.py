"""Solver-free exact verification of the saved fixed-query SC dual.

This verifies a certificate for one fixed policy cone. It does not assert
anything about other policies, other p, or the general HALF conjecture.
"""
from fractions import Fraction as F
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def move(h):
    if len(h) == 0:
        return 0
    if len(h) == 1:
        return (3, 3, 3, 0, 0, 0)[h[0]]
    choices = (0, 1, 2) if h[1] <= 2 else (3, 4, 5)
    return next(a for a in choices if a not in h)


def end(h):
    h = list(h)
    while len(h) < 3:
        h.append(move(h))
    return tuple(h)


def income(mask, z, who):
    if not (mask & (1 << z[who])):
        return F(0)
    return F(1, sum(bool(mask & (1 << a)) for a in z))


def verify():
    stored = json.loads((HERE / "mixed_sc_fixed_query_probe.json").read_text())
    dual = stored["reconstructed_dual"]
    terms = [(tuple(t["history"]), t["deviation"], F(t["coefficient"]))
             for t in dual["IC_terms"]]
    gamma = F(dual["SC_equality_coefficient"])
    assert all(v >= 0 for _, _, v in terms)
    assert F(dual["normalization_coefficient"]) == 0
    # At p=(e2+e5)/2 the pool equals (5,2,0,4,1,0)/12.
    pool = tuple(map(F, ("5/12", "1/6", "0", "1/3", "1/12", "0")))
    assert sum(pool) == 1
    residuals = {}
    for mask in range(1, 64):
        mu = 2 * sum(pool[a] for a in range(6) if mask & (1 << a))
        g2 = F(bool(mask & 4), 1) / (1 + mu)
        g5 = F(bool(mask & 32), 1) / (1 + mu)
        w = F(any(mask & (1 << a) for a in end(())))
        rhs_ic = F(0)
        for h, a, coefficient in terms:
            who = len(h)
            gap = income(mask, end(h), who) - income(mask, end(h + (a,)), who)
            rhs_ic += coefficient * gap
        residual = w - 3 * g2 - rhs_ic - gamma * (g2 - g5)
        assert residual >= 0, (mask, residual)
        expected = F(dual["type_residuals"].get(str(mask), "0"))
        assert residual == expected
        residuals[mask] = residual
    return {
        "status": "exact dual identity verified without optimizer",
        "scope": "one fixed complete policy, p=(e2+e5)/2, all nonnegative customer-type multiplicities satisfying its SPE inequalities",
        "client_type_columns": len(residuals),
        "nonnegative_IC_multipliers": len(terms),
        "SC_equality_coefficient": str(gamma),
        "minimum_type_residual": str(min(residuals.values())),
        "positive_type_residuals": sum(v > 0 for v in residuals.values()),
        "conditional_conclusion": "g2=g5 implies 3 G(p)<=W within this fixed policy cone",
        "not_established": ["other self-consistent p", "other policies", "all-m SC payment", "OPT_5<=2W", "general HALF"],
    }


if __name__ == "__main__":
    report = verify()
    (HERE / "mixed_sc_dual_audit.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
