"""Exact arithmetic for a conditional replicated complete-root menu.

This does not claim that the menu is SPE-realizable for n>2.
No prior audit matrices or model/BI implementations are imported.
"""
from fractions import Fraction as F
import json


TYPES = (({0}, 2), ({1, 3}, 4), ({0, 2}, 6), ({2, 3}, 3), ({0, 1, 2, 3}, 1))
Q0 = (2, 1, 1, 0)
COLS = ((2, 0, 1, 1), (1, 1, 1, 1), (1, 0, 2, 1), (1, 0, 1, 2))


def payoff(topic, counts, extra):
    ans = F(0)
    for interested, multiplicity in TYPES:
        if topic in interested:
            denominator = sum(counts[a] for a in interested) + extra
            assert denominator > 0
            ans += F(multiplicity, denominator)
    return ans


def main():
    local = [[payoff(s, q, 1) for q in COLS] for s in range(4)]
    baseline = [payoff(s, Q0, 1) for s in range(4)]
    own = [payoff(a, COLS[a], 0) for a in range(4)]
    assert own == [F(13, 4), F(9, 4), F(13, 4), F(13, 4)]
    assert baseline == [F(71, 30), F(11, 5), F(16, 5), F(37, 10)]
    assert min(local[3]) == local[3][3] == F(137, 60)
    assert max(local[s][0] for s in range(4)) == F(16, 5)
    # A freely chosen 4n-slot profile, outside the prescribed root-menu family.
    free_cap = max(payoff(s, COLS[1], 1) for s in range(4))
    assert free_cap == F(16, 5) < F(13, 4)
    examples = {}
    for n in range(3, 101):
        # Uniform root D_j (primal); uniform independent D_i queries (dual).
        primal = [((n - 1) * baseline[s] + local[s][3]) / n for s in range(4)]
        dual = [((n - 1) * baseline[3] + local[3][t]) / n for t in range(4)]
        value = F(37, 10) - F(17, 12*n)
        assert max(primal) == min(dual) == primal[3] == value
        assert value - F(13, 4) == F(27*n - 85, 60*n)
        if n <= 5:
            examples[str(n)] = {"value": str(value), "primal": list(map(str, primal)),
                                "dual": list(map(str, dual)), "gap_over_root": str(value - F(13, 4))}
    assert examples["3"]["value"] == "581/180"
    assert examples["4"]["value"] == "803/240"
    assert examples["4"]["gap_over_root"] == "23/240"
    # Arithmetic only for the displayed true-subtree diagnostic profiles.
    # Admissibility and maximality over SPE continuations are not checked here.
    qe = (1, 1, 2, 0)
    assert payoff(3, qe, 1) == F(16, 5)
    diagnostic = [(local[3][t] + payoff(3, qe, 1) + baseline[3]) / 3 for t in range(4)]
    assert diagnostic == [F(101,30), F(283,90), F(197,60), F(551,180)]
    print(json.dumps({"status": "PASS", "scope": "conditional menu matrix only; SPE realization not checked",
                      "local_L": [[str(v) for v in row] for row in local],
                      "baseline_h": list(map(str, baseline)), "root_own_payoffs": list(map(str, own)),
                      "free_4n_slot_cap": str(free_cap), "examples": examples,
                      "displayed_n3_diagnostic_profile_query_values": list(map(str, diagnostic))}, indent=2))


if __name__ == "__main__":
    main()
