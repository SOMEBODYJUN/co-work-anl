"""Definition-level unit-customer replay; no canonical solver or verifier imports."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def case(k, t):
    topics = ("A", "B", "U", "V")
    A = {("a", j) for j in range(2 * k)}
    B = {("b", j) for j in range(2 * k)}
    U = {("a", j) for j in range(k)} | {("b", j) for j in range(k)}
    V = {("v", j) for j in range(t)}
    sets = dict(zip(topics, (A, B, U, V)))
    actions = {(): "U", ("A",): "B", ("B",): "A",
               ("U",): "V", ("V",): "A"}

    def terminal(h):
        h = tuple(h)
        while len(h) < 2:
            h += (actions[h],)
        return h

    def payoff(path, pos):
        return sum((F(1, sum(x in sets[a] for a in path))
                    for x in sets[path[pos]]), F(0))

    comparisons = []
    for h, selected in actions.items():
        baseline = payoff(terminal(h), len(h))
        for a in topics:
            other = payoff(terminal(h + (a,)), len(h))
            assert baseline >= other, (k, t, h, a, baseline, other)
            comparisons.append({"history": list(h), "selected": selected,
                                "alternative": a, "slack": str(baseline - other)})
    path = terminal(())
    welfare = len(set().union(*(sets[a] for a in path)))
    optimum = max(len(sets[a] | sets[b]) for a, b in product(topics, repeat=2))
    assert path == ("U", "V")
    assert payoff(path, 0) == 2*k and payoff(path, 1) == t
    assert welfare == 2*k+t < 4*k == optimum
    assert all(len(sets[a]) == 2*k for a in ("A", "B", "U"))
    assert not (A & B) and len(A | B | U | V) == 4*k+t
    assert len(set(map(frozenset, sets.values()))) == 4
    return {"k": k, "t": t, "lambda": 2*k, "customers": 4*k+t,
            "ordered_decision_histories": len(actions), "comparisons": len(comparisons),
            "proper_deviations": sum(c["selected"] != c["alternative"] for c in comparisons),
            "actual": list(path), "payoffs": [str(payoff(path, i)) for i in (0, 1)],
            "W": welfare, "OPT": optimum, "half_slack": 2*welfare-optimum,
            "W_minus_m_lambda": welfare-4*k, "details": comparisons}


def main():
    main_case = case(2, 3)
    parameters = [case(k, t) for k in range(2, 31)
                  for t in range((3*k+1)//2, 2*k)]
    report = {"claim_scope": "Weak outside size boundary refutes individual lambda floor and W>=m*lambda only",
              "Q_CAG_HALF": "OPEN", "weak_boundary_half": "not settled",
              "eleven_customer_case": main_case,
              "parameter_checks": len(parameters),
              "all_parameter_checks_passed": True}
    path = Path(__file__).with_suffix(".json")
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "eleven_customer_case"},
                     ensure_ascii=False))
    print(json.dumps({k: v for k, v in main_case.items() if k != "details"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
