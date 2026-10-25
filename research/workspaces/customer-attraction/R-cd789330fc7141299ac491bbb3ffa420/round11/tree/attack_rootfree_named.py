"""Exact, named-packet pressure for the all-m root-free netROW candidate.

The prescribed root is allowed to be any legal action; strict-descendant
choices must remain the original packet's complete SPE. No policy, customer,
or parameter search is performed. Every comparator multiset of m slots is
examined in each explicitly named old packet. This is finite pressure only.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, combinations_with_replacement
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
OLD = HERE.parent.parent / "round10"


def normalize(path, form):
    raw = path.read_bytes()
    data = json.loads(raw)
    if form == "endpoint":
        ins, cert = data["endpoint"], data["strategy"]
        m, names = ins["players"], ins["topics"]
        types = [(frozenset(row["topics"]), row["multiplicity"])
                 for row in ins["customers"]]
        policy = {tuple(row["history"]): row["action"]
                  for row in cert["actions"]}
    elif form == "instance":
        ins, cert = data["instance"], data["certificate"]
        m, names = ins["players"], ins["topics"]
        types = [(frozenset(row["topics"]), row["multiplicity"])
                 for row in ins["customers"]]
        policy = {tuple(row["history"]): row["action"]
                  for row in cert["actions"]}
    elif form == "compact":
        names = data["topic_order"]
        m = 3
        types = [(frozenset(row), 1) for row in data["customers"]]
        lookup = {v: i for i, v in enumerate(names)}
        policy = {(): lookup[data["root"]]}
        policy.update({(a,): lookup[data["second"][a]]
                       for a in range(len(names))})
        policy.update({(a, b): lookup[data["terminal"][a][b]]
                       for a, b in product(range(len(names)), repeat=2)})
    else:
        raise ValueError(form)
    return raw, m, names, types, policy


def audit(path, form):
    raw, m, names, types, policy = normalize(path, form)
    k = len(names)
    histories = {h for depth in range(m)
                 for h in product(range(k), repeat=depth)}
    assert set(policy) == histories

    @lru_cache(None)
    def finish(h):
        return h if len(h) == m else finish(h + (policy[h],))

    @lru_cache(None)
    def utility(profile, role):
        action = profile[role]
        return sum((F(w, sum(a in S for a in profile))
                    for S, w in types if action in S), F(0))

    def cover(profile):
        used = set(profile)
        return sum(w for S, w in types if used & S)

    descendant_ic = []
    for h in histories:
        if not h:
            continue
        j = len(h)
        for action in range(k):
            descendant_ic.append(utility(finish(h), j)
                                 - utility(finish(h + (action,)), j))
    assert descendant_ic and min(descendant_ic) >= 0
    leaves = [finish((a,)) for a in range(k)]
    branch_W = [cover(z) for z in leaves]
    d = [utility(z, 0) for z in leaves]
    minimum_W = min(branch_W)
    best = None
    checked = 0
    for T in combinations_with_replacement(range(k), m):
        O = cover(T)
        lhs = sum((d[a] for a in T), F(0))
        gap = F(minimum_W) + lhs - O
        item = (gap, T, O, lhs)
        if best is None or item < best:
            best = item
        checked += 1
    gap, T, O, lhs = best
    return dict(source=str(path.relative_to(HERE.parents[5])),
                sha256=hashlib.sha256(raw).hexdigest(),
                players=m, topics=k, descendant_IC=len(descendant_ic),
                minimum_descendant_IC=str(min(descendant_ic)),
                root_branch_W=branch_W,
                root_branch_minimum_W=minimum_W,
                minimum_W_actions=[a for a, W in enumerate(branch_W)
                                   if W == minimum_W],
                root_query_payoffs=list(map(str, d)),
                comparator_multisets_checked=checked,
                tightest_comparator=list(T), tightest_O=O,
                tightest_query_sum=str(lhs),
                rootfree_minimum_gap=str(gap), refuted=gap < 0)


reports = [
    audit(OLD / "tree/compact_strongA_independent.json", "compact"),
    audit(OLD / "credible/strong_adjacent_gap_attack.json", "endpoint"),
    audit(OLD / "parent/root_standalone_helper_exact_counterexample.json", "instance"),
]
report = dict(candidate="Root-free netROW: W(actual arbitrary root)+sum_j d_root(T_j)>=|union T_j| for every m-slot comparator; original policy is SPE at every strict descendant.",
              scope="Three explicitly named old complete-policy packets; finite exact pressure only. No universal theorem or no-counterexample inference.",
              reports=reports)
HERE.joinpath("rootfree_named_pressure.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
