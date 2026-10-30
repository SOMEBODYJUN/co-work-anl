"""Exact finite checks accompanying a symbolic all-m induction obstruction.

The proof for arbitrary m is in the Markdown object. These checks verify
the displayed rational identities and an unbounded-n quantifier correction.
"""
from fractions import Fraction as F
import json


def main():
    out = []
    for m in range(3, 21):
        # Every possible prefix has a <= t prior A's. Choosing A and following
        # the all-A policy yields m/(a+m-t) >= 1; a singleton deviation yields
        # 1/(prior_same_singleton+1) <= 1. This checks all feasible counts.
        for t in range(m):
            for a in range(t + 1):
                actual = F(m, a + m - t)
                for j in range(t - a + 1):
                    assert actual >= F(1, j + 1)
        r, n = m, m
        L, L_after = F(2 * m - 1), F(3 * m, 2) - 1
        u, P_tail, Q1 = F(1), F(m - 1), F(m)
        root_slack = F(m - 1) * m + m * m - m * L
        tail_slack = F(m * (m - 2) + m * (m - 1)) - (m - 1) * L_after
        local_slack = Q1 + F(n * (r - 1), r) * u + F(n, r * (r - 1)) * P_tail - L - (r - 1) * (L - L_after)
        assert root_slack == 0
        assert tail_slack == F((m - 2) * (m + 1), 2) > 0
        assert local_slack == -tail_slack
        out.append({"m": m, "root_UP_slack": str(root_slack),
                    "tail_BG_UP_slack": str(tail_slack),
                    "local_slack": str(local_slack)})
    # One nonempty singleton topic, r remaining players, n=1 comparison.
    # All histories choose the only action, so L=P=Q=1 and the literal
    # unrestricted-n BG-UP has slack (r-1)/r+1-r < 0 for every r>=2.
    bad = [{"r": r, "n": 1, "L": "1", "P": "1", "Q": "1",
            "literal_BG_UP_slack": str(F(r - 1, r) + 1 - r)}
           for r in range(2, 10)]
    assert all(F(row["literal_BG_UP_slack"]) < 0 for row in bad)
    print(json.dumps({"all_big_family_checks": out,
                      "unrestricted_n_quantifier_correction": bad,
                      "arbitrary_m_proof": "See the companion Markdown object; finite runs are supplementary."}, indent=2))


if __name__ == "__main__":
    main()
