"""Independent audit of the exact frozen v2 input, outputs, and policy.

The full-tree solver below expands ordered original-label histories and does not
memoize attainable sets by counts. Fractions check the exported DAG separately.
This is a finite verification and does not prove a parametric q=5 statement.
"""
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import product, combinations
from pathlib import Path
import hashlib
import importlib.util
import json
import sys
import time

# Keep reproduction writes confined to this review's records directory.
sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[5]
WORK = ROOT / "research/workspaces/n6-boss3-20261118"
OUT = WORK / "records/review-q5-v2"
SRC = WORK / "informed-b"
FREEZE = ROOT / "research/runs/n6-boss3-20261118/studio/freezes/boss3-q5-prefix-v2/ef3e50bd1a37352d6de6dbe941547094d245e20c68555df728a7205eab1fe23b.json"

def read_json(path):
    return json.loads(path.read_text())

freeze = read_json(FREEZE)
ledger = []
for ref in freeze["content_refs"]:
    raw = (ROOT / ref["path"]).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == ref["sha256"], ref["path"]
    ledger.append({**ref, "actual_sha256": digest, "bytes": len(raw), "match": True})

data = read_json(SRC / "q5-cyclic-K6-v2-input.json")
old_output = read_json(SRC / "q5-cyclic-K6-v2-output.json")
bundle = read_json(SRC / "q5-cyclic-K6-v2-policy.json")
assert bundle["input"] == data
cov = tuple(frozenset(t["clients"]) for t in data["labels"])
A = len(cov)
K = data["K"]
anchors = frozenset(cov[:6])
extra = frozenset(c for c in cov if c and c not in anchors)
assert len(anchors) == 6
assert all(len(c) == K for c in cov[:6])
assert all(cov[a].isdisjoint(cov[b]) for a in range(6) for b in range(a))
assert max(map(len, cov)) == K
assert set().union(*cov[:6]) == set(range(data["clients"]))
prefix_names = data["prefix_labels"]
label_names = [t["name"] for t in data["labels"]]
assert len(set(label_names)) == A
prefix = tuple(label_names.index(n) for n in prefix_names)
assert len(extra) == 5 and len(set(cov)) == 11
assert all(c not in anchors for c in cov[6:])
prefix_counts = tuple(prefix.count(a) for a in range(A))
assert list(prefix_counts) == data["prefix_counts"]

@lru_cache(None)
def utilities(y):
    load = [sum(y[a] for a in range(A) if x in cov[a])
            for x in range(data["clients"])]
    values = tuple(sum((Fraction(1, load[x]) for x in c if load[x]), Fraction())
                   for c in cov)
    return values, sum(bool(v) for v in load)

# Independent, exact direct check of every reachable exported policy node.
cert = bundle["policy"]
nodes = cert["nodes"]
assert tuple(nodes[cert["root"]]["counts"]) == prefix_counts
seen = set()
edge_count = 0
state_goals = defaultdict(set)
tail_nodes_checked = 0
def check_node(i):
    global edge_count, tail_nodes_checked
    if i in seen:
        return
    node = nodes[i]
    q = tuple(node["counts"])
    y = tuple(node["terminal"])
    assert len(q) == len(y) == A
    assert all(type(v) is int and v >= 0 for v in (*q, *y))
    assert sum(q) <= 6 and sum(y) == 6
    assert all(u <= v for u, v in zip(q, y))
    state_goals[q].add(y)
    seen.add(i)
    if sum(q) == 6:
        assert q == y
        assert node["action"] is None and node["children"] == []
        return
    a = node["action"]
    assert type(a) is int and 0 <= a < A
    assert len(node["children"]) == A
    assert tuple(nodes[node["children"][a]]["terminal"]) == y
    own = utilities(y)[0][a]
    if len(prefix) <= sum(q) and sum(q) >= 4:
        assert own >= Fraction(7*K, 12)
        assert cov[a] and all(not q[b] or cov[b] != cov[a] for b in range(A))
        tail_nodes_checked += 1
    for b, k in enumerate(node["children"]):
        qb = list(q)
        qb[b] += 1
        assert nodes[k]["counts"] == qb
        check_node(k)
        z = tuple(nodes[k]["terminal"])
        assert own >= utilities(z)[0][b]
        edge_count += 1
check_node(cert["root"])
assert len(seen) == len(nodes)

# Independent explicit ordered-history recursion. It caches only utilities,
# never E(h), and therefore visits all 1+11+...+11^6 ordered nodes at the root.
tree_nodes = Counter()
def ordered_tree(history, counts):
    depth = len(history)
    tree_nodes[depth] += 1
    if depth == 6:
        return frozenset((counts,)), None
    children = []
    for a in range(A):
        q = list(counts)
        q[a] += 1
        children.append(ordered_tree(history + (a,), tuple(q))[0])
    lower = tuple(min(utilities(y)[0][a] for y in child)
                  for a, child in enumerate(children))
    threshold = max(lower)
    selected = tuple((utilities(y)[0][a], a, y)
                     for a, child in enumerate(children) for y in child
                     if utilities(y)[0][a] >= threshold)
    return frozenset(y for _, _, y in selected), {
        "lower": lower, "threshold": threshold, "minimum": min(selected)}

started = time.perf_counter()
prefix_set, prefix_meta = ordered_tree(prefix, prefix_counts)
prefix_node_counts = dict(tree_nodes)
tree_nodes.clear()
root_set, root_meta = ordered_tree((), (0,) * A)
root_node_counts = dict(tree_nodes)

def integer60(x):
    scaled = 60*x
    assert scaled.denominator == 1
    return scaled.numerator
assert len(prefix_set) == old_output["prefix_outcome_count"]
assert integer60(prefix_meta["minimum"][0]) == old_output["minimum_current_payoff_times_60"]
assert integer60(prefix_meta["threshold"]) == old_output["current_threshold_times_60"]
assert list(map(integer60, prefix_meta["lower"])) == old_output["child_min_payoffs_times_60"]
assert min(utilities(y)[1] for y in prefix_set) == old_output["prefix_min_terminal_welfare"]
assert max(utilities(y)[1] for y in prefix_set) == old_output["prefix_max_terminal_welfare"]
assert len(root_set) == old_output["root_outcome_count"]
assert min(utilities(y)[1] for y in root_set) == old_output["root_min_welfare"]
assert len(seen) == old_output["complete_subgame_policy_nodes"]

# Also reproduce author's runner, redirecting new artifacts into this audit dir.
spec = importlib.util.spec_from_file_location("frozen_exact_tail", SRC / "exact_tail.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
replay = module.run(data, True, OUT / "author-runner-replayed-policy.json")
assert {k: v for k, v in replay.items() if k != "elapsed_seconds"} == {
    k: v for k, v in old_output.items() if k != "elapsed_seconds"}
(OUT / "author-runner-replayed-output.json").write_text(json.dumps(replay, indent=2) + "\n")

# Independently check static relaxation by all ordered triples of genuine extras.
exposure = read_json(SRC / "q5-cyclic-K6-v2-semantic-and-exposure.json")
static_rows = []
for j in range(4):
    values = []
    distinct_values = []
    for actions in product(range(6, A), repeat=3):
        discount = sum((Fraction(sum(x in cov[a] for a in actions),
                                 1+sum(x in cov[a] for a in actions))
                        for x in cov[j]), Fraction())
        values.append(discount)
        if len(set(actions)) == 3:
            distinct_values.append(discount)
    unrestricted, distinct = max(values), max(distinct_values)
    expected = exposure["static_exposure"][j]
    assert unrestricted == Fraction(expected["max_arbitrary_loss"])
    assert distinct == Fraction(expected["max_distinct_extra_loss"])
    assert distinct > Fraction(K, 2)
    static_rows.append({"anchor": j, "maximum_all_ordered_extra_triples": str(unrestricted),
                        "maximum_distinct_ordered_extra_triples": str(distinct)})
assert [x["maximum_distinct_ordered_extra_triples"] for x in static_rows] == ["10/3", "10/3", "19/6", "19/6"]

result = {
    "freeze_revision_pin": FREEZE.stem,
    "hash_checks": ledger,
    "input_semantics": {
        "labels": A, "distinct_coverages": len(set(cov)),
        "different_nonempty_extras_outside_six_anchors": len(extra),
        "duplicate_coverage_labels": [[label_names[a], label_names[b]]
                                      for a in range(A) for b in range(a)
                                      if cov[a] == cov[b]],
        "K": K, "OPT6": 6*K,
    },
    "direct_fraction_policy_check": {
        "checked_nodes": len(seen), "checked_action_edges": edge_count,
        "tail_nodes_checked_for_7K_over_12_and_nonrepeat": tail_nodes_checked,
        "distinct_counts_with_multiple_target_leaves": sum(len(s) > 1 for s in state_goals.values()),
        "independent_of_set_recursion": True,
        "scope": "One complete subgame SPE certificate at the specified prefix; not all policies and not a root certificate",
    },
    "independent_ordered_tree": {
        "attainable_sets_memoized_by_counts": False,
        "prefix_nodes_by_depth": prefix_node_counts,
        "root_nodes_by_depth": root_node_counts,
        "root_total_nodes": sum(root_node_counts.values()),
        "prefix_outcomes": sorted(map(list, prefix_set)),
        "root_outcomes": sorted(map(list, root_set)),
        "prefix_min_current_payoff_times_60": integer60(prefix_meta["minimum"][0]),
        "prefix_welfare_values": sorted({utilities(y)[1] for y in prefix_set}),
        "root_welfare_values": sorted({utilities(y)[1] for y in root_set}),
    },
    "independent_static_exposure": static_rows,
    "author_runner_matches_except_elapsed_seconds": True,
    "elapsed_seconds": time.perf_counter() - started,
}
(OUT / "audit-results.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k:v for k,v in result.items() if k != "hash_checks"}, indent=2))
