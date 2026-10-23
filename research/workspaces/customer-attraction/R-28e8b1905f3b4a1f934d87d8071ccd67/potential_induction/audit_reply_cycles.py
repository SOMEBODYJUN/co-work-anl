"""Direct unit-customer audit of two reply-cycle diagnostics.

No SPE solver, LP, or canonical verifier is imported. The 34-customer case is
the existing CA-INDIVIDUAL-SECURITY-NO instance, not a new counterexample.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement, product
import json
from pathlib import Path


def audit(name, labels, type_weights, policy):
    clients = [frozenset(t) for t, w in type_weights for _ in range(w)]
    d = len(labels)

    def outcome(h):
        while len(h) < 3:
            h += (policy(h),)
        return h

    def payoff(z, i):
        return sum((F(1, sum(a in t for a in z))
                    for t in clients if z[i] in t), F())

    def rent(a, tail):
        return sum((F(1, 1 + sum(b in t for b in tail))
                    for t in clients if a in t), F())

    def potential(z):
        return sum((sum((F(1, j) for j in range(1, 1 + sum(a in t for a in z))), F())
                    for t in clients), F())

    slacks = []
    for depth in range(3):
        for h in product(range(d), repeat=depth):
            current = payoff(outcome(h), depth)
            for a in range(d):
                gap = current - payoff(outcome(h + (a,)), depth)
                assert gap >= 0, (name, h, a, gap)
                slacks.append(gap)

    a, b = ((1, 2) if name == "seven_customers" else (2, 5))
    za, zb = outcome((a,)), outcome((b,))
    qa, qb = za[1:], zb[1:]
    own = rent(a, qa) + rent(b, qb)
    cross = rent(a, qb) + rent(b, qa)
    vectors = [tuple(payoff(z, i) for i in range(3)) for z in (za, zb)]
    all_tails = list(combinations_with_replacement(range(d), 2))
    regrets = [max(potential((x,) + q) for q in all_tails)
               - potential(z) for x, z in ((a, za), (b, zb))]
    return {
        "customers": len(clients), "decision_histories": sum(d**j for j in range(3)),
        "action_comparisons_including_self": len(slacks),
        "minimum_SPE_slack": str(min(slacks)),
        "actual": [labels[x] for x in outcome(())],
        "actual_welfare": len({x for x, t in enumerate(clients) if any(y in t for y in outcome(()))}),
        "queries": [labels[a], labels[b]],
        "query_branch_outcomes": [[labels[x] for x in z] for z in (za, zb)],
        "query_branch_profit_vectors": [[str(v) for v in vector] for vector in vectors],
        "cross_branch_tail_profit_difference": [str(vectors[1][j] - vectors[0][j]) for j in (1, 2)],
        "root_query_own_rents": [str(rent(a, qa)), str(rent(b, qb))],
        "cross_rents": [str(rent(a, qb)), str(rent(b, qa))],
        "cycle_difference": str(own - cross),
        "two_point_parent_slack_repair": str(2 * max(rent(a, qa), rent(b, qb)) - cross),
        "tail_potential_regrets": [str(v) for v in regrets],
        "actual_tail_surplus_above_root": str(sum(payoff(outcome(()), j) - payoff(outcome(()), 0) for j in (1, 2))),
    }


def policy7(h):
    if len(h) == 0:
        return 2
    if len(h) == 1:
        return 2 if h[0] == 2 else 1
    return 0 if h == (2, 2) else 1


def policy34(h):
    if len(h) == 0:
        return 0
    if len(h) == 1:
        return 3 if h[0] < 3 else 0
    group = range(3) if h[1] < 3 else range(3, 6)
    return next(x for x in group if x not in h)


def main():
    w34 = {4: 1, 27: 4, 29: 3, 30: 3, 31: 2, 32: 1, 43: 3,
           45: 3, 46: 3, 51: 3, 53: 3, 54: 3, 59: 2}
    t34 = [(tuple(j for j in range(6) if mask >> j & 1), w) for mask, w in w34.items()]
    result = {
        "scope": "Finite direct policy verification and exact diagnostics only; Q-CAG-HALF remains OPEN.",
        "seven_customers": audit("seven_customers", ("A", "B", "C"),
                                  [((0,), 1), ((0, 1), 1), ((1, 2), 3), ((0, 1, 2), 2)], policy7),
        "existing_thirty_four_customers": audit("existing_thirty_four_customers",
                                                ("X0", "X1", "X2", "Y0", "Y1", "Y2"), t34, policy34),
    }
    assert result["seven_customers"]["cycle_difference"] == "-1/6"
    assert result["existing_thirty_four_customers"]["cycle_difference"] == "-2"
    assert result["existing_thirty_four_customers"]["cross_branch_tail_profit_difference"] == ["0", "0"]
    path = Path(__file__).with_name("reply_cycle_audit.json")
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
