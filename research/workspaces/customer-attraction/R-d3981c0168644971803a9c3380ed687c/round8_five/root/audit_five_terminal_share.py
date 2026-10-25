"""Parent's independent, non-blind full ordered-history replay.

Reads only the explicit certificate data; no canonical solver/verifier or
author audit is imported. Unit clients are physically expanded.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction
import json

BASE = Path(__file__).resolve().parent.parent
raw = (BASE / "tree/terminal_share_padding_exact.json").read_bytes()
data = json.loads(raw)
topics = data["instance"]["topics"]
n = data["instance"]["players"]
clients = [set(t["topics"]) for t in data["instance"]["customers"]
           for _ in range(t["multiplicity"])]
policy = {tuple(t["history"]): t["action"]
          for t in data["certificate"]["actions"]}
expected = {h for d in range(n) for h in product(range(len(topics)), repeat=d)}
assert set(policy) == expected
assert len(policy) == len(data["certificate"]["actions"])


def resolve(prefix):
    out = prefix
    while len(out) < n:
        assert policy[out] in range(len(topics))
        out += (policy[out],)
    return out


def profits(out):
    ans = [Fraction(0) for _ in range(n)]
    for client in clients:
        interested = [j for j, action in enumerate(out) if action in client]
        for j in interested:
            ans[j] += Fraction(1, len(interested))
    return ans


comparisons = 0
minimum = None
for prefix in sorted(expected, key=lambda h: (len(h), h)):
    role = len(prefix)
    obey = profits(resolve(prefix))[role]
    for deviation in range(len(topics)):
        gain = obey - profits(resolve(prefix + (deviation,)))[role]
        assert gain >= 0, (prefix, deviation, gain)
        comparisons += 1
        minimum = gain if minimum is None else min(minimum, gain)

actual = resolve(())
u = profits(actual)
W = sum(any(a in c for a in actual) for c in clients)
opt = max(sum(any(a in c for a in out) for c in clients)
          for out in product(range(len(topics)), repeat=n))
assert sum(u) == W
assert actual == (4, 4, 0, 1, 3)
assert u == list(map(Fraction, ("3/2", "3/2", "3/2", "2", "7/2")))
assert W == opt == 10
assert 6*u[-1]-2*W == 1

# The proposed general DD lifting already fails at its prescribed last node.
# Base game tail (1,3,3), first payoff 7/3, last payoff 4/3; D=2*(7/3).
# With two old D providers and the last provider joining D, the payoff is 14/9.
padding_deviation = Fraction(14, 3) / 3
assert padding_deviation == Fraction(14, 9) > Fraction(4, 3)

report = {"status": "PASS", "review": "independent non-blind parent replay",
          "unit_clients": len(clients), "histories": len(policy),
          "action_comparisons_including_self": comparisons,
          "minimum_ic_slack": str(minimum), "path": actual,
          "payoffs": list(map(str, u)), "W": W, "OPT5": opt,
          "C2_violation": "1", "original_half_slack": 2*W-opt,
          "generic_DD_last_BR_failure": {"prescribed": "4/3", "deviation": "14/9"}}
Path(__file__).with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n")
print(json.dumps(report))
