"""Exact algebra audit for the disjoint big-topic zero-regret family.

No canonical solver is imported.  The all-history SPE claim is analytic:
continuing B gives m/(past_B+remaining)>=1, every singleton gives <=1.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


def compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for x in range(total + 1):
        for tail in compositions(total - x, parts - 1):
            yield (x,) + tail


def audit(m, leaves):
    den = 2 * leaves + m + 1
    p = (F(m + 1, den),) + (F(2, den),) * leaves
    v = 1 - F(1, den)
    min_value = None
    backgrounds = 0
    active = []
    for counts in compositions(m, leaves + 1):
        b, *z = counts
        j = sum(z)
        insertion = (F(m, b + 1),) + tuple(F(1, a + 1) for a in z)
        value = sum((a * b for a, b in zip(p, insertion)), F(0))
        remainder = F(j * (j - 1), b + 1) + sum(
            (F(a * (a - 1), a + 1) for a in z), F(0))
        assert den * (value - v) == remainder >= 0
        assert (value == v) == (j <= 1)
        if value == v:
            active.append(counts)
        min_value = value if min_value is None else min(min_value, value)
        backgrounds += 1
    assert min_value == v
    assert len(active) == leaves + 1

    # Matching static adversary Q is precisely the forced full-terminal menu
    # pushed forward by p.  All pure queries have the same expected payoff.
    menu = [(m,) + (0,) * leaves]
    for a in range(leaves):
        menu.append((m - 1,) + tuple(int(a == b) for b in range(leaves)))
    pure_values = []
    for query in range(leaves + 1):
        size = m if query == 0 else 1
        value = sum((mass * F(size, counts[query] + 1)
                     for mass, counts in zip(p, menu)), F(0))
        assert value == v
        pure_values.append(value)
    for d, q in enumerate(menu):
        size = m if d == 0 else 1
        nu = F(size, q[d] + 1)
        rho = F(size, q[d] * (q[d] + 1))
        delta = v - nu
        assert delta > 0 and delta - rho == -F(1, den)
    # Every legal history, up to count compression only for this explicit
    # constant policy, has an all-B payoff at least every deviation payoff.
    incentive_checks = 0
    for depth in range(m):
        remaining = m - depth
        for h in compositions(depth, leaves + 1):
            own = F(m, h[0] + remaining)
            for topic in range(leaves + 1):
                dev = own if topic == 0 else F(1, h[topic] + 1)
                assert own >= dev
                incentive_checks += 1
    return {'m': m, 'leaves': leaves, 'backgrounds': backgrounds,
            'count_representative_incentive_checks': incentive_checks,
            'p': list(map(str, p)), 'v': str(v), 'welfare': m,
            'aggregate_G': str(m * v), 'aggregate_slack': str(F(m, den)),
            'static_active_backgrounds': len(active)}


if __name__ == '__main__':
    cases = [audit(m, leaves) for m, leaves in product(range(1, 7), range(1, 8))]
    out = {'status': 'exact finite audit passed; general proof is in companion note',
           'cases': cases}
    target = Path(__file__).with_name('safe_zero_regret_family_audit.json')
    with target.open('x') as handle:
        json.dump(out, handle, indent=2)
        handle.write('\n')
    print(json.dumps({'cases': len(cases), 'last_case': cases[-1]}, indent=2))
