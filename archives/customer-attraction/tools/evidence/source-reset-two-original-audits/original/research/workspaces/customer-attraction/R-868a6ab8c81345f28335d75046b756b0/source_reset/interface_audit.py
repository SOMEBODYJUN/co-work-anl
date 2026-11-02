"""Exact boundary diagnostic: scalar flow != coordinatewise query cover.

The parameter family and its all-t proof are in scalar_financial_law.md.
This script only checks exact arithmetic at t=0 and one positive t.
It is not a test of Q-CAG-HALF or a positive fixed-size research task.
"""
from fractions import Fraction as F
import json


def audit(t):
    topics = (frozenset(range(t + 2)),
              frozenset(tuple(range(t)) + (t + 2,)))
    policy = {(): 0, (0,): 0, (1,): 0}

    def finish(history):
        history = tuple(history)
        while len(history) < 2:
            history += (policy[history],)
        return history

    def payoff(path, role):
        return sum((F(1, sum(x in topics[a] for a in path))
                    for x in topics[path[role]]), F(0))

    ic = []
    for history in ((), (0,), (1,)):
        role = len(history)
        prescribed = finish(history)
        incumbent = payoff(prescribed, role)
        for action in range(len(topics)):
            deviation = finish(history + (action,))
            other = payoff(deviation, role)
            assert incumbent >= other
            ic.append(dict(history=history, action=action,
                           prescribed=str(incumbent), deviation=str(other)))

    actual = finish(())
    actual_union = set().union(*(topics[a] for a in actual))
    optimal_union = set().union(*topics)
    omitted = optimal_union - actual_union
    assert omitted == {t + 2}
    x = t + 2
    query = finish((1,))
    r = F(1, sum(x in topics[a] for a in query))
    d = payoff(query, 0)
    u = payoff(actual, 0)
    absorbed = r
    w = absorbed / d
    scalar_cost = w * u
    coordinate_coverage = w * r
    assert (r, d, u, absorbed, w, scalar_cost, coordinate_coverage) == (
        F(1), F(t + 2, 2), F(t + 2, 2), F(1),
        F(2, t + 2), F(1), F(2, t + 2))
    assert (coordinate_coverage < 1) == (t > 0)
    # Both B queries have coordinate r=1 and role cost u;
    # A queries have omitted coordinate zero, so COORD minimum is u.
    assert payoff(finish((0, 1)), 1) == u
    return dict(t=t, topics=[sorted(a) for a in topics], actual=actual,
                W=len(actual_union), OPT=len(optimal_union),
                R=sorted(omitted), G=0, ic=ic, query=query,
                D=str(d), r=str(r), absorption=str(absorbed),
                scalar_weight=str(w), scalar_min_cost=str(scalar_cost),
                mapped_coordinate_coverage=str(coordinate_coverage),
                independent_coordinate_LP_min_cost=str(u))


if __name__ == "__main__":
    result = dict(
        status="PASS: exact all-history boundary arithmetic",
        scope="scalar-flow-to-coordinate-cover interface; not Q-CAG-HALF",
        general_formula="scalar min=1; coordinate min=(t+2)/2; all t>=0",
        audits=[audit(t) for t in (0, 7)])
    print(json.dumps(result, indent=2))
