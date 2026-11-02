"""Definition-level exact checks for the strengthened reservation constructor.

This independently builds every ordered history and uses Fraction payoffs.
The finite checks serve only the stated general-constructor boundary tests.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json


def run(old_n, old_A_size, reserve_size):
    m, B = old_n + 1, 1
    # Every item is a distinct unit customer. Topic 0 is A, topic 1 is B.
    customers = [frozenset({0}) for _ in range(old_A_size)] + [frozenset({1}) for _ in range(reserve_size)]
    old_sigma = {h: 0 for d in range(old_n) for h in product([0], repeat=d)}
    actions = {}

    def payoff(a, terminal):
        return sum((F(1, sum(t in support for t in terminal))
                    for support in customers if a in support), F())

    @lru_cache(None)
    def terminal(h):
        if len(h) == m:
            return h
        children = [terminal(h + (a,)) for a in (0, 1)]
        b_count = h.count(B)
        if b_count == 0:
            a = B
        elif b_count == 1:
            a = old_sigma[tuple(t for t in h if t != B)]
        else:
            a = max((0, 1), key=lambda t: (payoff(t, children[t]), -t))
        actions[h] = a
        return children[a]

    actual = terminal(())
    rows = []
    violations = []
    retained = []
    for d in range(m):
        for h in product((0, 1), repeat=d):
            a = actions[h]
            own = payoff(a, terminal(h))
            for t in (0, 1):
                forced = terminal(h + (t,))
                slack = own-payoff(t, forced)
                row = dict(history=list(h), prescribed=a, deviation=t,
                           actual_terminal=list(terminal(h)), forced_terminal=list(forced),
                           own=str(own), deviation_payoff=str(payoff(t, forced)), slack=str(slack))
                rows.append(row)
                if slack < 0:
                    violations.append(row)
            if h and h[0] == B and h.count(B) == 1:
                assert a == old_sigma[h[1:]]
                retained.append(list(h))
    assert len(actions) == sum(2**d for d in range(m))
    eta = F(old_A_size, old_n)
    K = old_A_size
    L = F(old_A_size, 2)
    return dict(old_players=old_n, players=m, old_A_size=old_A_size, reserve_size=reserve_size,
                eta=str(eta), intersection_threshold=str(L),
                new_constructor_hypotheses=(F(reserve_size,2)<=eta and reserve_size>=L),
                old_strict_condition=(F(old_A_size,2)>F(reserve_size,old_n)),
                one_player_extra_condition=(reserve_size>=K),
                decision_histories=len(actions), comparisons=len(rows),
                actual=list(actual), minimum_slack=str(min(F(r['slack']) for r in rows)),
                valid=not violations, violations=violations,
                retained_after_root_B_histories=retained,
                actions=[dict(history=list(h),action=actions[h]) for h in sorted(actions,key=lambda h:(len(h),h))],
                rows=rows)


equality = run(2, 3, 3)
assert equality['new_constructor_hypotheses']
assert not equality['old_strict_condition']
assert equality['valid'] and equality['decision_histories']==7 and equality['comparisons']==14
assert equality['actual']==[1,0,0]
one_failure = run(1,3,2)
assert one_failure['new_constructor_hypotheses'] and not one_failure['one_player_extra_condition']
assert not one_failure['valid']
assert one_failure['violations'][0]['history']==[] and one_failure['violations'][0]['slack']=='-1'
one_success = run(1,3,3)
assert one_success['one_player_extra_condition'] and one_success['valid']
report = dict(status='EXACT_FINITE_BOUNDARY_CHECKS_ONLY',
              scope='General theorem rests on independent analytic proof; these are full-history constructor checks, not optimization or a fixed-player research project.',
              equality_excluded_by_old_strict_condition=equality,
              one_player_missing_condition_failure=one_failure,
              one_player_corrected_condition_success=one_success)
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:({x:v[x] for x in ('players','valid','decision_histories','comparisons','minimum_slack','old_strict_condition')} if isinstance(v,dict) else v)
                  for k,v in report.items()},indent=2))
