"""Exact local payoff algebra, not a five-player SPE or counterexample audit."""

from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def share(numerator, denominator):
    return F(numerator, denominator) if numerator else F(0)


def atom(p, k, ell, emm):
    current_actual = share(k, p + k + ell)
    current_deviation = share(k, p + k + emm)
    last_actual = share(ell, p + k + ell)
    last_deviation = share(emm, p + k + emm)
    d = current_actual - current_deviation
    t = last_actual - last_deviation
    cover = int(p + k + ell > 0)
    return d, t, F(cover) - 3*d - t


def main():
    rows = []
    for p, k, ell, emm in product(range(4), range(2), range(2), range(2)):
        d, t, slack = atom(p, k, ell, emm)
        assert slack >= 0
        rows.append({"p": p, "K": k, "L": ell, "M": emm,
                     "current_loss": str(d), "last_difference": str(t),
                     "slack": str(slack)})

    # Two customers in K=M, one different customer in L, no old load.
    d1, t1, slack1 = atom(0, 1, 0, 1)
    d2, t2, slack2 = atom(0, 0, 1, 0)
    assert 2*t1+t2 == 0
    assert 2*d1+d2 == 1
    assert 2*slack1+slack2 == 0

    report = {
        "scope": "Exact local algebra for genuine equal-value last BR replies; not an SPE certificate.",
        "cases": len(rows), "all_nonnegative": True,
        "minimum_slack": str(min(F(r["slack"]) for r in rows)),
        "sharp_swing_example": {"current_loss": "1", "actual_insurance_welfare": 3,
                                 "last_reply_difference": "0", "loss_over_welfare": "1/3"},
        "five_player_cartesian_full_insurance_budget": {
            "k2_minimum_B_over_a": str(3*(1-F(1,4))),
            "k2_ratio_upper_bound": str((5+F(9,4))/(2+F(9,4))),
            "k_ge_3_ratio_upper_bound": "5/3"},
        "rows": rows,
    }
    target = Path(__file__).with_suffix(".json")
    target.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({k: v for k, v in report.items() if k != "rows"}, indent=2))


if __name__ == "__main__":
    main()
