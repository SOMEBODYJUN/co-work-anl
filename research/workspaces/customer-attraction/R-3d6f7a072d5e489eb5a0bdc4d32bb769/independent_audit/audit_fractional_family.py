"""Independent construction and full-tree unit audit of the analytic family."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json
from audit_fractional_weak import audit


@lru_cache(None)
def bonus(r, q, e):
    """Finite BI for two unit-reward singleton resources; returns action/endloads."""
    if r == 0:
        return None, (q, e)
    _, end_q = bonus(r-1, q+1, e)
    _, end_d = bonus(r-1, q, e+1)
    if F(1, end_q[0]) >= F(1, end_d[1]):
        return 2, end_q
    return 3, end_d


def construct(m):
    game = {"topics": ["A", "B", "Q", "D"], "players": m,
            "customers": [{"topics": [0], "multiplicity": m-1},
                          {"topics": [2], "multiplicity": 1},
                          {"topics": [0, 3], "multiplicity": 1},
                          {"topics": [1, 2, 3], "multiplicity": m*(m-1)}]}
    rows = []
    for t in range(m):
        for h in product(range(4), repeat=t):
            a, b, q, d = (h.count(j) for j in range(4))
            if b == t:
                chosen = 1 if t < m-1 else 0
            else:
                chosen, _ = bonus(m-t, q, a+d)
            rows.append({"history": list(h), "action": chosen})
    return game, {"terminal_counts": [1, m-1, 0, 0], "actions": rows}


if __name__ == "__main__":
    results = []
    for m in range(2, 8):
        game, certificate = construct(m)
        result = audit(game, certificate)
        result.pop("all_history_rows")
        denominator = m*m-m+1
        predicted_M = 1 + F(m*m*(m-1), denominator)
        predicted_gap = F(m**3-4*m*m+3*m-1, 2*denominator)
        assert F(result["M"]) == predicted_M
        assert F(result["weak_bridge_gap"]) == predicted_gap
        assert result["W"] == m*m and result["OPT"] == m*m+1
        # Reverse check the displayed polynomial numerator against exact query data.
        assert 2*denominator*F(result["weak_bridge_gap"]) == m*m*(m-4)+3*m-1
        results.append(result)
        print(json.dumps(result), flush=True)
    Path(__file__).with_name("fractional_family_audit.json").write_text(
        json.dumps(results, indent=2) + "\n")
