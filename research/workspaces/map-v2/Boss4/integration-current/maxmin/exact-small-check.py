"""Two tiny rational checks; no LP solver, no claim of exhaustive validation."""

from fractions import Fraction as F
from itertools import product
import json

items = ("a", "b", "c", "d", "e")
small_value = dict(zip(items, (F(9, 10), F(4, 5), F(7, 10), F(3, 5), F(0))))
big_value = dict(zip(items, (F(1), F(0), F(0), F(0), F(1))))
fraction_big = {"a": F(1, 2), "e": F(1, 2)}
fraction_small = {"a": F(1, 2), "b": F(1), "c": F(1), "d": F(1)}
for j in items:
    assert fraction_big.get(j, F(0)) + fraction_small.get(j, F(0)) <= 1
assert sum(fraction_big.values()) == 1
fractional_utility = sum(small_value[j] * x for j, x in fraction_small.items())
first_slot_utility = F(1, 2) * small_value["a"] + F(1, 2) * small_value["b"]
assert fractional_utility == F(51, 20) >= 2
assert first_slot_utility == F(17, 20) < 1

# Slot B: a/2,e/2; S1: a/2,b/2; S2: b/2,c/2; S3: c/2,d/2.
# The remaining half of d is a tail and is not required to be matched.
supports = (("a", "e"), ("a", "b"), ("b", "c"), ("c", "d"))
matchings = []
for picked in product(*supports):
    if len(set(picked)) != len(picked):
        continue
    big_utility = big_value[picked[0]]
    small_utility = sum(small_value[j] for j in picked[1:])
    assert big_utility >= 1
    assert small_utility >= fractional_utility - first_slot_utility
    assert small_utility >= 1
    assert len(set(items) - set(picked)) == 1
    matchings.append({"slots_B_S1_S2_S3": picked, "small_value": str(small_utility)})

# One small player, three unit-valued items: qualifications jump after T=2.
# At integer T=1,2 all items are forbidden on a small row; at T=3 all qualify.
thresholds = []
for threshold in (1, 2, 3, 4):
    allowed_value = 3 if F(1) < F(threshold, 2) else 0
    thresholds.append({"T": threshold, "feasible": allowed_value >= threshold})
assert [row["feasible"] for row in thresholds] == [False, False, True, False]

print(json.dumps({
    "purpose": "Tiny exact arithmetic illustrations, not replacement proofs or old-check reruns",
    "T": 2,
    "fractional_small_value": str(fractional_utility),
    "first_slot_value": str(first_slot_utility),
    "loss_lower_bound": str(fractional_utility - first_slot_utility),
    "full_joint_matchings": matchings,
    "global_feasibility_nonmonotone_example": thresholds,
}, indent=2, ensure_ascii=False))
