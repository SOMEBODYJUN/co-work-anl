"""Exact definition-level audit of the root's swap-ascent candidate counterexample.

No game solver or repository verifier is imported.  The two payoff implementations
use, respectively, distinct expanded unit customers and compressed interest types.
Finite parameter checks support implementation only; the Markdown proof is general.
"""

from fractions import Fraction
from itertools import product
import json
from pathlib import Path


LABELS = "ABCD"
RESPONSE = (1, 2, 3, 2)


def audit(name, types, expected=None):
    customers = [mask for mask, count in types.items() for _ in range(count)]
    sets = [{x for x, mask in enumerate(customers) if mask & (1 << a)}
            for a in range(4)]
    assert len({frozenset(s) for s in sets}) == 4

    def unit_payoff(a, outcome):
        return sum((Fraction(1, sum(x in sets[t] for t in outcome))
                    for x in sets[a]), Fraction())

    def type_payoff(a, outcome):
        return sum((Fraction(count, sum(bool(mask & (1 << t)) for t in outcome))
                    for mask, count in types.items() if mask & (1 << a)), Fraction())

    for outcome in product(range(4), repeat=2):
        for a in outcome:
            assert unit_payoff(a, outcome) == type_payoff(a, outcome)

    last_rows = []
    comparisons = []
    for first in range(4):
        row = [unit_payoff(last, (first, last)) for last in range(4)]
        last_rows.append(row)
        selected = row[RESPONSE[first]]
        for last in range(4):
            assert selected >= row[last]
            comparisons.append({"history": LABELS[first], "deviation": LABELS[last],
                                "gap": str(selected - row[last])})

    root_profits = [unit_payoff(first, (first, RESPONSE[first])) for first in range(4)]
    alpha = root_profits[0]
    for first in range(4):
        assert alpha >= root_profits[first]
        comparisons.append({"history": "", "deviation": LABELS[first],
                            "gap": str(alpha - root_profits[first])})
    beta = unit_payoff(1, (0, 1))
    mu_b = max(last_rows[1])
    delta = max(Fraction(), mu_b - alpha)
    welfare = len(sets[0] | sets[1])
    opt = max(len(sets[a] | sets[b]) for a, b in product(range(4), repeat=2))
    b_best_endpoints = [{"outcome": "B" + LABELS[last],
                         "old_B_profit": str(unit_payoff(1, (1, last))),
                         "new_last_profit": str(unit_payoff(last, (1, last))),
                         "W": len(sets[1] | sets[last])}
                        for last in range(4) if last_rows[1][last] == mu_b]
    assert alpha < beta < mu_b
    assert delta > beta - alpha
    if expected:
        actual = (alpha, beta, mu_b, delta, welfare, opt)
        assert actual == expected, (name, actual, expected)

    return {
        "name": name,
        "unit_customers": len(customers),
        "types": [{"mask": mask, "count": count} for mask, count in sorted(types.items())],
        "strategy": {"root": "A", "after": dict(zip(LABELS, map(LABELS.__getitem__, RESPONSE)))},
        "last_payoffs": [[str(v) for v in row] for row in last_rows],
        "root_profits": list(map(str, root_profits)),
        "alpha": str(alpha), "beta": str(beta), "mu_B": str(mu_b),
        "swap_defect": str(delta), "actual_ascent": str(beta - alpha),
        "defect_over_ascent": str(delta / (beta - alpha)),
        "W": welfare, "OPT_2": opt,
        "all_SPE_endpoints_after_fixed_B": b_best_endpoints,
        "decision_histories": 5,
        "comparisons_including_prescribed": comparisons,
    }


def main():
    reports = [audit("ten_unit_customers", {2: 2, 6: 1, 10: 1, 12: 1, 13: 4, 14: 1},
                     (Fraction(4), Fraction(5), Fraction(6), Fraction(2), 9, 10))]
    for k, e in ((3, 1), (4, 1), (10, 1), (10, 3), (100, 1)):
        assert k > 2 * e > 0
        # X has interest A,C,D; Y has B,C; Z has B,D; E has B.
        report = audit(f"parameter_k{k}_e{e}", {13: 2*k, 6: k, 10: k, 2: e},
                       (Fraction(2*k), Fraction(2*k+e), Fraction(5*k, 2),
                        Fraction(k, 2), 4*k+e, 4*k+e))
        for endpoint in report["all_SPE_endpoints_after_fixed_B"]:
            assert endpoint["W"] == 4*k+e
            assert Fraction(endpoint["old_B_profit"]) == Fraction(3*k, 2) + e
        reports.append(report)
    result = {"claim_tested": "alpha<beta implies mu_B<=beta",
              "status": "FALSE: complete pure SPE counterexamples",
              "half_status": "not refuted; parameter family has W=OPT_2",
              "reports": reports}
    output = Path(__file__).with_name("swap_ascent_counterexample_audit.json")
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"verified_instances": len(reports),
                      "ten_customer_values": {key: reports[0][key] for key in
                                              ("alpha", "beta", "mu_B", "swap_defect", "W", "OPT_2")},
                      "largest_checked_defect_over_ascent": reports[-1]["defect_over_ascent"],
                      "output": str(output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
