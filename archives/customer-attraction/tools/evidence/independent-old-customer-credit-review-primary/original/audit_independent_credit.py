"""Independent exact arithmetic for the three credit-obstruction families.

The new AB complete strategy is defined here from scratch. No discovery script,
LP, CAG solver, or canonical certificate verifier is imported.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import json

N = 64


def action(a, b, r):
    assert r > 0
    if a:
        return 'B'
    k = b+r
    if k <= 31:
        return 'B'
    if k == 32:
        return 'A' if r == 1 else 'B'
    return 'A'


@lru_cache(None)
def outcome(a, b, r):
    if not r:
        return a, b
    chosen = action(a, b, r)
    return outcome(a+(chosen == 'A'), b+(chosen == 'B'), r-1)


def ab_strategy():
    states = comparisons = 0
    minimum_prescribed = None
    for r in range(1, N+1):
        for a in range(N-r+1):
            for b in range(N-r-a+1):
                chosen = action(a, b, r)
                ca, cb = outcome(a, b, r)
                payoff = F(2, ca) if chosen == 'A' else F(63, cb)
                minimum_prescribed = payoff if minimum_prescribed is None else min(minimum_prescribed, payoff)
                aa, ab = outcome(a+1, b, r-1)
                ba, bb = outcome(a, b+1, r-1)
                assert payoff >= F(2, aa)
                assert payoff >= F(63, bb)
                # Every one of the 62 singleton deviations gives at most one;
                # this covers each possible history-specific singleton load.
                assert payoff >= 1
                states += 1
                comparisons += 64
    assert outcome(0, 0, 64) == (1, 63)
    best, args = F(-1), []
    for a in range(64):
        for b in range(64-a):
            single_slots = 63-a-b
            value = F(2*a, 1+a)+63*int(b > 0)+min(62, single_slots)
            if value > best:
                best, args = value, [(a,b,single_slots)]
            elif value == best:
                args.append((a,b,single_slots))
    assert best == 125
    return dict(all_count_states=states, topic_choices_covered_by_exact_bounds=comparisons,
                singleton_deviations_checked_by_uniform_bound=True,
                minimum_prescribed_payoff=minimum_prescribed,
                actual_counts=(1,63), F63=best, F63_argmax_representatives=args,
                P63=63, forced_f63_1_0=(best-126)/2)


def all_big():
    values = [F(64*k,k+1)+63-k for k in range(64)]
    best = max(values)
    assert best == 112
    lower = (best-126)/64
    assert lower == F(-7,32)
    return dict(F63=best, P63=63, argmax_A_counts=[k for k,v in enumerate(values) if v == best],
                forced_f63_1_63=lower)


def overlap():
    # Ordinary leaves have private block 62, B-only block 62, A block 1.
    # At fixed a,b,special multiplicity, moving any repeated ordinary leaf to
    # an untouched one gains >=62 and loses <=1/6. Thus all q ordinary copies
    # can be placed on different leaves, because q <= 63 = their number.
    best = F(-1)
    args = []
    evaluations = 0
    for a in range(64):
        for b in range(64-a):
            for special in range(64-a-b):
                q = 63-a-b-special
                baseline = 63*(62*int(b > 0)+F(a,a+1))
                fresh_increment = 62*(1+int(b == 0))+F(1,(a+1)*(a+2))
                ordinary = baseline+q*fresh_increment
                distinguished = 62*int(special > 0)+62*int(b+special > 0)
                distinguished += 63*F(a+b+special,1+a+b+special)
                value = ordinary+distinguished
                evaluations += 1
                if value > best:
                    best,args = value,[(a,b,special,q)]
                elif value == best:
                    args.append((a,b,special,q))
    root = 2*N*N-2*N-2
    u = F(N*N-1,N)
    delta = root-best
    upper = (2*u-delta)/63
    assert best == F(15769,2)
    assert root == 8062 and delta == F(355,2)
    assert u == F(4095,64) and upper == F(-1585,2016)
    return dict(canonical_profiles_evaluated=evaluations, F63=best, F64=root,
                F63_argmax_representatives=args, root_u=u, root_delta=delta,
                forced_sum_f63_1_63_and_f63_1_0=upper)


if __name__ == '__main__':
    report = dict(status='independent exact review of explicit families',
                  AB=ab_strategy(), all_big=all_big(), overlap=overlap())
    lower = report['AB']['forced_f63_1_0']+report['all_big']['forced_f63_1_63']
    upper = report['overlap']['forced_sum_f63_1_63_and_f63_1_0']
    assert lower == F(-1449,2016) and lower-upper == F(17,252)
    report['contradiction'] = dict(forced_lower=lower, forced_upper=upper, positive_gap=lower-upper)
    histogram_shared = 63*64
    histogram_uncovered = 2016*2
    assert histogram_shared == histogram_uncovered == 64*63 == 4032
    product_lower = 63*(report['all_big']['F63']-126)+2016*(report['AB']['F63']-126)
    product_upper = 64*(2*report['overlap']['root_u']-report['overlap']['root_delta'])
    assert product_lower == -2898 and product_upper == -3170
    assert product_lower-product_upper == 272
    report['nonadditive_product'] = dict(histogram_shared_1_63=histogram_shared,
        histogram_old_only_1_0=histogram_uncovered,
        forced_lower=product_lower, forced_upper=product_upper,
        positive_gap=product_lower-product_upper)
    path = Path(__file__).with_name('independent_credit_audit.json')
    path.write_text(json.dumps(report,indent=2,default=str)+'\n')
    print(json.dumps(report,indent=2,default=str))
