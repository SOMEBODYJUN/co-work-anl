"""Exact boundary check for one discarded robust-floor-only candidate.

This terminal is NOT a SPE.  The script checks the exact necessary floors,
a genuine static-security primal lower certificate, and the failed true
penultimate IC.  No finite result is used as a universal proof.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement
import json
from pathlib import Path


def run():
    m, k = 4, 5
    # A=0 contains x_1,...,x_4; B_i={x_i}+two private customers.
    customers = [(frozenset((i,)), 2) for i in range(1, k)]
    customers += [(frozenset((0, i)), 1) for i in range(1, k)]
    z = (0, 0, 0, 1)

    def payoff(a, terminal):
        return sum((F(w, sum(t in S for t in terminal))
                    for S, w in customers if a in S), F(0))

    pay = tuple(payoff(a, z) for a in z)
    welfare = sum(w for S, w in customers if any(a in S for a in z))
    assert pay == (F(5, 4), F(5, 4), F(5, 4), F(9, 4))
    assert sum(pay) == welfare == 6
    floors = []
    for i in range(m):
        floor = max(sum((F(w, sum(t in S for t in z[:i]) + m - i)
                         for S, w in customers if a in S), F(0))
                    for a in range(k))
        assert pay[i] >= floor
        floors.append(floor)

    # Uniform querying of all five legal themes guarantees 8/5 against every
    # static four-slot integer background.  This is a lower bound, not an
    # assertion that the query is uniquely optimal.
    values = []
    for q in combinations_with_replacement(range(k), m):
        value = sum((sum((F(w, 1 + sum(t in S for t in q))
                          for S, w in customers if a in S), F(0))
                     for a in range(k)), F(0)) / k
        values.append((value, q))
    static_lower, worst = min(values)
    assert static_lower == F(8, 5)
    assert m * static_lower - welfare == F(2, 5)

    # At history (0,0), force current action 2.  Every true last best reply
    # produces a current payoff strictly above 5/4.  Thus no SPE completion
    # can make z the actual terminal.
    h = (0, 0, 2)
    replies = [(payoff(a, h + (a,)), a) for a in range(k)]
    last_best = max(v for v, a in replies)
    br = [a for v, a in replies if v == last_best]
    deviation_payoffs = [payoff(2, h + (a,)) for a in br]
    assert last_best == F(7, 3)
    assert br == [1, 3, 4]
    assert min(deviation_payoffs) == F(7, 3) > pay[2]

    return {
        'status': 'DISCARDED NECESSARY-CONDITION RELAXATION; NOT A SPE',
        'terminal': z,
        'payoffs': [str(v) for v in pay],
        'welfare': welfare,
        'robust_floors': [str(v) for v in floors],
        'static_backgrounds_checked': len(values),
        'uniform_query_static_lower': str(static_lower),
        'one_worst_background': worst,
        'extra_one_aggregate_gap': str(m * static_lower - welfare),
        'violated_node': [0, 0],
        'deviation': 2,
        'true_last_best_replies': br,
        'deviating_player_payoff_under_every_best_reply': str(min(deviation_payoffs)),
        'penultimate_IC_violation': str(min(deviation_payoffs) - pay[2]),
        'conclusion': 'Robust floors alone do not pay extra-one aggregate security; full IC remains necessary.'
    }


if __name__ == '__main__':
    result = run()
    path = Path(__file__).with_name('floor_relaxation_audit.json')
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
