"""Independent materialized HI and exact pure-SPE recursion for the C5 case.

Uses only the five unit customers and Fraction. It imports no project model,
solver, interval implementation, discovery code, or numerical optimizer.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import json


def main():
    labels, players = 5, 6
    masks = (3, 6, 12, 24, 17)
    root = (0,)*labels
    floor_i, eligible, floor_s = {}, {}, {}

    def step(b,a):
        return b[:a]+(b[a]+1,)+b[a+1:]

    @lru_cache(None)
    def payoff(q):
        answer = []
        for a in range(labels):
            u = F(0)
            if q[a]:
                for mask in masks:
                    if mask>>a&1:
                        count = sum(q[t] for t in range(labels) if mask>>t&1)
                        u += F(1,count)
            answer.append(u)
        return tuple(answer)

    def welfare(q):
        return sum(any(q[t] and mask>>t&1 for t in range(labels)) for mask in masks)

    @lru_cache(None)
    def interval(b):
        if sum(b)==players:
            return frozenset((b,))
        children = [interval(step(b,a)) for a in range(labels)]
        bound = max(min(payoff(z)[a] for z in children[a]) for a in range(labels))
        allowed = tuple(a for a in range(labels) if max(payoff(z)[a] for z in children[a])>=bound)
        floor_i[b], eligible[b] = bound, allowed
        return frozenset(z for a in allowed for z in children[a])

    @lru_cache(None)
    def exact(b):
        if sum(b)==players:
            return frozenset((b,))
        children = [exact(step(b,a)) for a in range(labels)]
        bound = max(min(payoff(z)[a] for z in children[a]) for a in range(labels))
        floor_s[b] = bound
        return frozenset(z for a in range(labels) for z in children[a] if payoff(z)[a]>=bound)

    @lru_cache(None)
    def cost(b):
        if sum(b)==players:
            return F(0)
        interval(b)
        return floor_i[b]+min(cost(step(b,a)) for a in eligible[b])

    hi, spe = interval(root), exact(root)
    static = F(10,17)  # Uniform theme mass 6/5, two acceptable labels per unit customer.
    assert floor_i[root]==F(1,2)<static<F(2,3)==floor_s[root]
    assert cost(root)==F(23,6)
    assert len(hi)==60 and len(spe)==20
    assert min(map(welfare,spe))==max(map(welfare,spe))==5
    target = (3,1,0,1,1)
    path = (0,0,0,1,4,3)
    b = root
    trace = []
    for a in path:
        assert a in eligible[b] and target in interval(step(b,a))
        trace.append(dict(prefix=b, action=a, floor=str(floor_i[b]), actual_terminal_payoff=str(payoff(target)[a])))
        b = step(b,a)
    assert b==target
    leak_prefix = (1,0,0,0,0)
    high = (2,0,1,2,1)
    assert high in interval(step(leak_prefix,0))
    assert payoff(high)[0]==F(5,6)>=floor_i[leak_prefix]==F(2,3)>payoff(target)[0]==F(1,2)
    lows = []
    for a in range(labels):
        child = interval(step(root,a))
        lo = min(payoff(z)[a] for z in child)
        hi_value = max(payoff(z)[a] for z in child)
        assert lo==F(1,2) and hi_value==1
        lows.append(dict(action=a, minimum=str(lo), maximum=str(hi_value),
                         low_terminal=min(z for z in child if payoff(z)[a]==lo),
                         high_terminal=min(z for z in child if payoff(z)[a]==hi_value)))
    report = dict(instance=dict(players=players, topic_count=labels, unit_customer_masks=masks),
                  interval_root_floor=str(floor_i[root]), exact_root_floor=str(floor_s[root]),
                  fractional_extra_one_threshold=str(static), gap=str(static-floor_i[root]),
                  root_interval_payment=str(cost(root)), optimum=5,
                  min_interval_welfare=min(map(welfare,hi)), root_HI_outcomes=len(hi),
                  root_SPE_outcomes=len(spe), count_states=interval.cache_info().currsize,
                  root_low_high=lows, allowed_fake_path=path, trace=trace,
                  leak_high_witness=high,
                  scope="Refutes only LI>=extra-one fractional threshold; true SPE threshold exceeds it and all SPE welfare is optimal.",
                  status="definition-level independent exact reconstruction passed")
    Path(__file__).with_name('interval_c5_independent_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('root_low_high','trace')},indent=2))


if __name__=='__main__':
    main()
