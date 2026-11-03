"""Exact local identities; not finite evidence for the general Q-CAG-HALF."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


def local_rows(location, t, r):
    # location: A, H, D or outside.  A and H have one actual early provider.
    a, h, d = (int(location == x) for x in ("A", "H", "D"))
    actual_r = F(r, 1 + a + h) if r else F(0)
    branch_r = F(r, 1 + t + h) if r else F(0)
    branch_t = F(t, 1 + h + r) if t else F(0)
    branch_d = F(d, 1 + h + t) if d else F(0)
    gi = F(a) - branch_t
    gr = branch_r - branch_d
    gd = F(d) - actual_r
    target = F(t) if location in ("A", "outside") else F(t, 2)
    lhs = F(3*a, 2) - target
    rhs = gi + gr + gd + F(a*(1-r), 2)
    return lhs, rhs


def audit():
    entries = []
    for location, t, r in product(("A", "H", "D", "outside"), (0, 1), (0, 1)):
        lhs, rhs = local_rows(location, t, r)
        assert lhs == rhs, (location, t, r, lhs, rhs)
        entries.append({"location": location, "T": t, "R": r, "both_sides": str(lhs)})
    convex = []
    for k in range(1, 101):
        lam = F(2*k*k+k, 2*(k+1)**2)
        beta = F(8*k*k+11*k+4, 4*(k+1)**2)
        coeff_p = lam * F(2*k+1, k) + (1-lam)*F(1, 2)
        coeff_l = lam*F(1, 2) + (1-lam)*(k+1)
        assert 0 < lam < 1
        assert coeff_p == coeff_l == beta, (k, lam, coeff_p, coeff_l, beta)
        assert 2-beta == F(5*k+4, 4*(k+1)**2) > 0
        convex.append({"k": k, "lambda": str(lam), "beta": str(beta)})
    return {"scope": "16 exact customer membership identities; 100 exact coefficient checks; general claim relies on symbolic proof", "membership_rows": entries, "convex_checks": convex}


if __name__ == "__main__":
    result = audit()
    path = Path(__file__).with_suffix(".json")
    if path.exists():
        raise FileExistsError(path)
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"membership_rows": len(result["membership_rows"]), "convex_checks": len(result["convex_checks"]), "status": "exact assertions passed"}))
