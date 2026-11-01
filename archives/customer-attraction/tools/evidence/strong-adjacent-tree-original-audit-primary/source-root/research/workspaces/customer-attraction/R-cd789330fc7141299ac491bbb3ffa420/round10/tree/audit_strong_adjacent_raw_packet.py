"""Independent exact StrongA audit from raw endpoint/policy only.

No author/canonical solver imports. One explicitly supplied packet; no scan.
Customer multiplicities encode distinct unit customers. The policy is evaluated
on every complete ordered history; terminal utility caching does not merge it.
"""
from functools import lru_cache
from fractions import Fraction
from itertools import combinations_with_replacement, product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "credible" / "strong_adjacent_gap_attack.json"
DEST = HERE / "strong_adjacent_raw_independent_audit.json"
blob = SOURCE.read_bytes()
packet = json.loads(blob)
data = packet["endpoint"]
m = data["players"]
k = len(data["topics"])
assert m == packet["m"] and k == packet["topics"]
types = []
for row in data["customers"]:
    membership = frozenset(row["topics"])
    weight = row["multiplicity"]
    assert membership and membership <= set(range(k))
    assert len(membership) == len(row["topics"])
    assert isinstance(weight, int) and not isinstance(weight, bool) and weight >= 0
    types.append((membership, weight))
policy = {}
for row in packet["strategy"]["actions"]:
    h = tuple(row["history"])
    action = row["action"]
    assert h not in policy and len(h) < m
    assert all(isinstance(a, int) and 0 <= a < k for a in h)
    assert isinstance(action, int) and 0 <= action < k
    policy[h] = action
histories = [h for depth in range(m) for h in product(range(k), repeat=depth)]
assert set(policy) == set(histories)

@lru_cache(None)
def finish(h):
    if len(h) == m:
        return h
    return finish(h + (policy[h],))

@lru_cache(None)
def topic_payoffs(counts):
    result = [Fraction(0) for _ in range(k)]
    for membership, weight in types:
        load = sum(counts[a] for a in membership)
        if load:
            for a in membership:
                if counts[a]:
                    result[a] += Fraction(weight, load)
    return tuple(result)

def counts_of(profile):
    return tuple(profile.count(a) for a in range(k))

def utilities(profile):
    by_topic = topic_payoffs(counts_of(profile))
    return tuple(by_topic[a] for a in profile)

def coverage(profile):
    used = frozenset(profile)
    return sum(weight for membership, weight in types if used & membership)

minimum_slack = None
comparisons = 0
for h in histories:
    i = len(h)
    prescribed = utilities(finish(h))[i]
    for action in range(k):
        if action == policy[h]:
            continue
        slack = prescribed - utilities(finish(h + (action,)))[i]
        assert slack >= 0, (h, action, slack)
        minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)
        comparisons += 1

actual = finish(())
u = utilities(actual)
W = coverage(actual)
assert sum(u) == W
frozen_rows = []
for i in range(m):
    frozen_rows.append(tuple(utilities(actual[:i] + (a,) + actual[i+1:])[i]
                             for a in range(k)))
maxima = tuple(max(row) for row in frozen_rows)
maximizers = tuple(tuple(a for a, value in enumerate(row) if value == max(row))
                   for row in frozen_rows)
Q = sum(maxima)
Cs = [Fraction(0) for _ in range(m-1)]
for membership, weight in types:
    load = sum(a in membership for a in actual)
    if load:
        for j in range(m-1):
            if actual[j] in membership and actual[j+1] not in membership:
                Cs[j] += Fraction(weight, load*(load+1))
Csum = sum(Cs)
gap = Q - W - Csum
opt = max(coverage(t) for t in combinations_with_replacement(range(k), m))
assert actual == tuple(packet["actual_path"])
assert W == packet["W"] and opt == packet["OPT"]
assert Csum == Fraction(packet["Csum"])
assert Q == Fraction(packet["true_Q"])
assert gap == Fraction(packet["true_signed_StrongA_gap"]) and gap > 0
assert all(packet["true_maximizers"][i] in maximizers[i] for i in range(m))
assert opt < 2*W
result = {
    "scope": "One raw integer-customer full ordered-history SPE packet; StrongA only.",
    "source": str(SOURCE.relative_to(HERE.parents[5])),
    "source_sha256": hashlib.sha256(blob).hexdigest(),
    "imports": "standard library only; no author audit/model/solver imported",
    "m": m, "topic_labels": k, "customer_types": len(types),
    "unit_customers": sum(weight for _, weight in types),
    "ordered_histories": len(histories), "nonself_IC": comparisons,
    "minimum_IC_slack": str(minimum_slack),
    "actual": list(actual), "actual_payoffs": [str(v) for v in u],
    "W": W, "OPT": opt, "OPT_over_W": str(Fraction(opt, W)),
    "frozen_rows": [[str(v) for v in row] for row in frozen_rows],
    "frozen_maximizers_all_ties": [list(row) for row in maximizers],
    "frozen_maxima": [str(v) for v in maxima],
    "frozen_regrets": [str(v-w) for v, w in zip(maxima, u)],
    "Q": str(Q), "adjacent_Cs": [str(v) for v in Cs],
    "Csum": str(Csum), "StrongA_signed_gap": str(gap),
    "StrongA_refuted": True, "HALF_refuted": False,
    "weaker_optimal_assignment_tested": False,
}
DEST.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({key: result[key] for key in
                 ["ordered_histories", "nonself_IC", "minimum_IC_slack", "W", "OPT",
                  "Q", "Csum", "StrongA_signed_gap", "StrongA_refuted", "HALF_refuted"]},
                 indent=2))
