"""Verify both two-provider counterexamples using exact integer comparisons."""
from fractions import Fraction
from itertools import product
import json

LABELS = "STUXZAB"
REPLY = dict(zip(LABELS, "TABABBA"))
TYPES = {
    "compact": (
        "X:1 TUX:1 Z:2 SXZ:2 UXA:1 STUZA:2 STXB:2 ZB:1 "
        "SXAB:2 TUXAB:2 STUXAB:3 TUZAB:2 STUZAB:5"
    ),
    "strict": (
        "X:5 TUX:3 Z:8 SZ:1 SXZ:2 UXA:1 SZA:1 SUZA:1 SXB:2 TUZB:1 "
        "SXAB:3 STXAB:4 TUXAB:5 STUXAB:10 TUZAB:5 STUZAB:15"
    ),
}


def verify(types, strict):
    customers = []
    for word in types.split():
        interests, count = word.split(":")
        customers.extend(set(interests) for _ in range(int(count)))
    cover = {t: {i for i, interests in enumerate(customers) if t in interests} for t in LABELS}

    def doubled_payoff(t, rival):
        return 2 * len(cover[t]) - len(cover[t] & cover[rival])

    choices = [[doubled_payoff(t, rival) for t in LABELS] for rival in LABELS]
    root = [doubled_payoff(t, REPLY[t]) for t in LABELS]
    for rival, row in zip(LABELS, choices):
        best_replies = [t for t, u in zip(LABELS, row) if u == max(row)]
        assert REPLY[rival] in best_replies
        if strict:
            assert best_replies == [REPLY[rival]]
    assert root[0] == max(root)
    if strict:
        assert all(u < root[0] for u in root[1:])

    welfare_matrix = [[len(cover[a] | cover[b]) for b in LABELS] for a in LABELS]
    opt = max(map(max, welfare_matrix))
    menu = [a for a, row in zip(LABELS, welfare_matrix) if max(row) == opt]
    optimizers = [a + b for a, b in product(LABELS, repeat=2) if len(cover[a] | cover[b]) == opt]
    fresh = [len(cover[a] - cover["S"]) for a in LABELS]
    final_menu = [a for a, value in zip(LABELS, fresh) if value == max(fresh)]
    assert menu == ["X", "Z"] and optimizers == ["XZ", "ZX"] and final_menu == ["U"]
    terms = {}
    for a in menu:
        A = cover[a]
        tail = cover[REPLY[a]]
        new = A - cover["S"]
        terms[a] = Fraction(doubled_payoff(a, REPLY[a]) - len(new) - len(new - tail), 2)
    terms["U"] = Fraction(doubled_payoff("U", "S"), 2) - len(cover["U"] - (cover["S"] | cover["T"]))
    total = min(terms["X"], terms["Z"]) + terms["U"]
    welfare = len(cover["S"] | cover["T"])
    slack = 2 * welfare - opt
    assert opt == len(customers)
    assert total - slack == Fraction(1, 2) and slack > 0
    return {
        "customers": len(customers),
        "topic_order": LABELS,
        "ordered_reply": REPLY,
        "doubled_last_payoff_rows": choices,
        "doubled_root_payoffs": root,
        "coverage_rows": welfare_matrix,
        "coverage_optimal_root_menu": menu,
        "coverage_optimal_last_menu": final_menu,
        "last_fresh_coverages": fresh,
        "unique_full_SPE": strict,
        "payoff_comparisons_including_chosen_actions": len(root) + sum(map(len, choices)),
        "eta_terms": {k: str(v) for k, v in terms.items()},
        "W": welfare,
        "OPT": opt,
        "eta_total": str(total),
        "half_slack": slack,
        "candidate_violation": str(total - slack),
    }


if __name__ == "__main__":
    print(json.dumps({k: verify(v, k == "strict") for k, v in TYPES.items()}, indent=2))
