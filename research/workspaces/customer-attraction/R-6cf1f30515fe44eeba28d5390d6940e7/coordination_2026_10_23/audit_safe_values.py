#!/usr/bin/env python3
"""Independent definition-level checks for coordination claims, no project imports."""
from fractions import Fraction as F
from functools import cache
import json
from pathlib import Path


def compositions(total, parts):
    if parts == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for tail in compositions(total - first, parts - 1):
                yield (first,) + tail


def add(z, a):
    return tuple(v + (i == a) for i, v in enumerate(z))


def payoff(z, a):
    return F(1, z[(a-1) % 5] + z[a]) + F(1, z[a] + z[(a+1) % 5])


@cache
def interval(b):
    if sum(b) == 6:
        return frozenset([b]), F(0), F(0)
    children = [interval(add(b, a)) for a in range(5)]
    floor = max(min(payoff(z, a) for z in children[a][0]) for a in range(5))
    allowed = [a for a in range(5) if max(payoff(z, a) for z in children[a][0]) >= floor]
    terms = frozenset().union(*(children[a][0] for a in allowed))
    return terms, floor, floor + min(children[a][2] for a in allowed)


def query_against(z, a):
    return F(1, 1 + z[(a-1) % 5] + z[a]) + F(1, 1 + z[a] + z[(a+1) % 5])


root_backgrounds = list(compositions(6, 5))
uniform_root_min = min(sum((query_against(z, a) for a in range(5)), F(0))/5
                       for z in root_backgrounds)
optimal_mix = [tuple(1 + (i == heavy) for i in range(5)) for heavy in range(5)]
upper_values = [sum((query_against(z, a) for z in optimal_mix), F(0))/5 for a in range(5)]
assert uniform_root_min == F(3, 5)
assert upper_values == [F(3, 5)] * 5

child_minima = []
for fixed in range(5):
    backgrounds = [add(z, fixed) for z in compositions(5, 5)]
    lower = min(sum((query_against(z, a) for a in range(5)), F(0))/5 for z in backgrounds)
    assert lower == F(3, 5)
    assert all(z[fixed] >= 1 for z in optimal_mix)
    child_minima.append(str(lower))

_, floor, total_floor = interval((0,) * 5)
drift = floor + 5 * F(3, 5) - 6 * F(3, 5)
assert floor == F(1, 2) and total_floor == F(23, 6) and drift == -F(1, 10)


def singleton_values(r, n):
    a, s = divmod(r, n)
    return F(n, n+r-1), (F(n-s, a+1) + F(s, a+2))/n


examples = []
for r, n in [(3, 3), (3, 7)]:
    t, v = singleton_values(r, n)
    examples.append(dict(r=r, n=n, t_r=str(t), v_extra_one=str(v), v_minus_t=str(v-t)))
assert singleton_values(3, 3) == (F(3, 5), F(1, 2))
assert singleton_values(3, 7) == (F(7, 9), F(11, 14))

result = dict(status="Exact checks of specified bridges only; no general-half proof",
              root_static_backgrounds=len(root_backgrounds), child_static_backgrounds_each=126,
              c5_v7=str(uniform_root_min), c5_child_v6=child_minima,
              c5_interval_states=interval.cache_info().currsize,
              c5_LI=str(floor), c5_GI=str(total_floor), c5_local_drift=str(drift),
              singleton_examples=examples)
out = Path(__file__).with_name("safe_value_audit.json")
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(result, ensure_ascii=False))
