"""Exact full-history verification of a non-factorizing Cartesian SPE."""
from fractions import Fraction as F
from itertools import product
import json


def main():
    # A=0..2, B=3..4, C=5..6, D=7.
    topics = [frozenset(range(3)) | frozenset((5, 6)),
              frozenset(range(3)) | frozenset((7,)),
              frozenset((3, 4, 5, 6)), frozenset((3, 4, 7))]
    policy = {(): 2, (0,): 2, (1,): 2, (2,): 1, (3,): 0}

    def terminal(h):
        while len(h) < 2:
            h = h + (policy[h],)
        return h

    def utility(z, i):
        return sum((F(1, sum(x in topics[a] for a in z))
                    for x in topics[z[i]]), F(0))

    comparisons = 0
    for h in policy:
        own = utility(terminal(h), len(h))
        for a in range(4):
            assert own >= utility(terminal(h+(a,)), len(h))
            comparisons += 1
    actual = terminal(())
    assert actual == (2, 1)
    assert sum(utility(actual, i) for i in range(2)) == 8
    assert max(len(topics[a] | topics[b]) for a, b in product(range(4), repeat=2)) == 8
    assert [utility(terminal((a,)), 0) for a in range(4)] == [4, 4, 4, 3]
    # Fixed second-component first action C, first component chooses A or B.
    projected_payoff_A = sum((F(1, sum(x in topics[a] for a in (0, 2)))
                              for x in range(3)), F(0))
    projected_payoff_B = sum((F(1, sum(x in topics[a] for a in (2, 1)))
                              for x in (3, 4)), F(0))
    assert projected_payoff_A == 3 and projected_payoff_B == 2
    print(json.dumps({"status": "exact audit passed; not a welfare counterexample",
                      "decision_nodes": len(policy), "action_comparisons": comparisons,
                      "actual": actual, "W": 8, "OPT_2": 8,
                      "projected_improvement": str(projected_payoff_A-projected_payoff_B)},
                     indent=2))


if __name__ == "__main__":
    main()
