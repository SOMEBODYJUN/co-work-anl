"""Inspect four frozen m5 inputs; this does not recheck positive-depth IC or OPT.

Only stdlib is used.  The new mathematical evaluations are the four actual
leaves and seven root-forced leaves per plan.  All 2801 original actions per
file are retained and compared, including different orders of one count state.
Run in this directory.  Nothing outside this evidence directory is written.
"""
from collections import defaultdict
from fractions import Fraction
from itertools import product
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED = {
    "seed_source_m5_v0_0.json": "a6ea6522a286248ec3a7303b53a13caa05e2e01a085401f7bf6123d6f2f1295a",
    "seed_source_m5_v0_1.json": "1b25505064dbf0aaa69d400030454c9af28c3711dfcd90709962ec729a2f05aa",
    "seed_source_m5_v1_0.json": "0a74b373a9c1db9a02a4304473c234b2a596a828fa0d23bdaa646719c3ffde3b",
    "seed_source_m5_v1_1.json": "9b664c4b3fbe63cbde46e1a69b1ba6b459701be07bbb9db7157a658d7419b209",
}


def inspect(name, expected_sha):
    raw = (HERE / "original" / name).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == expected_sha
    obj = json.loads(raw)
    inst = obj["instance"]
    assert inst["players"] == 5 and inst["topics"] == list(map(str, range(7)))
    assert all(type(c["multiplicity"]) is int and c["multiplicity"] > 0
               and c["topics"] and len(c["topics"]) == len(set(c["topics"]))
               and all(type(t) is int and 0 <= t < 7 for t in c["topics"])
               for c in inst["customers"])
    actions = {tuple(h): a for h, a in obj["actions"]}
    histories = {h for depth in range(5) for h in product(range(7), repeat=depth)}
    assert len(actions) == len(obj["actions"]) == 2801
    assert set(actions) == histories
    assert all(type(a) is int and 0 <= a < 7 for a in actions.values())
    assert [tuple(h) for h, _ in obj["actions"]] == sorted(histories)

    # Expanding multiplicities makes the finite unit-client interpretation explicit.
    clients = [frozenset(c["topics"]) for c in inst["customers"]
               for _ in range(c["multiplicity"])]
    signatures = [frozenset(i for i, c in enumerate(clients) if a in c)
                  for a in range(7)]
    assert len(set(signatures)) == 7

    def leaf(history):
        while len(history) < 5:
            history += (actions[history],)
        return history

    def utility(action, terminal):
        return sum((Fraction(1, sum(b in c for b in terminal))
                    for c in clients if action in c), Fraction(0))

    def welfare(terminal):
        return sum(bool(set(terminal) & c) for c in clients)

    actual = leaf(())
    root_leaves = [leaf((a,)) for a in range(7)]
    root_values = [utility(a, root_leaves[a]) for a in range(7)]
    root_action = actions[()]
    delta = max(root_values) - root_values[root_action]
    assert list(actual) == obj["actual"]
    assert list(map(str, root_values)) == obj["root_deviation_payoffs"]
    assert str(root_values[root_action]) == obj["actual_root_payoff"]
    assert str(delta) == obj["root_regret"]
    assert welfare(actual) == obj["W"]

    by_counts = defaultdict(list)
    for history, action in sorted(actions.items()):
        by_counts[tuple(history.count(a) for a in range(7))].append((history, action))
    order_sensitive_groups = [values for values in by_counts.values()
                              if len({action for _, action in values}) > 1]
    missed = [{"original_customer_row": i, **c}
              for i, c in enumerate(inst["customers"])
              if not set(actual).intersection(c["topics"])]
    report = {
        "file": name, "sha256": expected_sha, "bytes": len(raw),
        "all_original_top_level_fields": list(obj),
        "ordered_actions": len(actions), "depth_counts": [7 ** d for d in range(5)],
        "positive_depth_IC_checked_now": 0, "OPT_enumerations_now": 0,
        "unit_customers": len(clients), "root_action": root_action,
        "actual": actual,
        "actual_player_payoffs": [str(utility(a, actual)) for a in actual],
        "actual_W": welfare(actual),
        "root_forced_leaves": root_leaves,
        "root_forced_coverages": [welfare(z) for z in root_leaves],
        "root_forced_payoffs": list(map(str, root_values)),
        "root_regret": str(delta),
        "best_root_actions": [a for a, v in enumerate(root_values) if v == max(root_values)],
        "actual_uncovered_customer_rows": missed,
        "order_sensitive_count_groups": order_sensitive_groups,
        "original_OPT_metadata_not_recomputed": obj["OPT_m"],
        "repair_margin_using_saved_exact_OPT": str(Fraction(obj["OPT_m"] - 2 * welfare(actual)) - 3 * delta),
    }
    reading = ["FILE " + name, "ALL_NON_ACTION_FIELDS " + json.dumps(
        {k: v for k, v in obj.items() if k != "actions"}, ensure_ascii=False, separators=(",", ":")),
        "ENCODING: depths 0..3: all histories in product(range(7), repeat=depth);",
        "depth 4: fixed first-two-digit prefix; last two digits in lexicographic order."]
    reconstruction = {}
    for depth in range(4):
        hs = list(product(range(7), repeat=depth))
        word = "".join(str(actions[h]) for h in hs)
        reading.append(f"depth {depth}: {word}")
        reconstruction.update(zip(hs, map(int, word)))
    for prefix in product(range(7), repeat=2):
        hs = [prefix + tail for tail in product(range(7), repeat=2)]
        word = "".join(str(actions[h]) for h in hs)
        reading.append("depth 4 prefix " + "".join(map(str, prefix)) + ": " + word)
        reconstruction.update(zip(hs, map(int, word)))
    assert reconstruction == actions
    return obj, actions, report, "\n".join(reading)


def main():
    data = {name: inspect(name, sha) for name, sha in EXPECTED.items()}
    pairs = []
    for left, right in [("seed_source_m5_v0_0.json", "seed_source_m5_v0_1.json"),
                        ("seed_source_m5_v1_0.json", "seed_source_m5_v1_1.json")]:
        lobj, la, _, _ = data[left]
        robj, ra, _, _ = data[right]
        pairs.append({"left": left, "right": right,
                      "instances_identical": lobj["instance"] == robj["instance"],
                      "all_action_differences": [
                          {"history": h, "left_action": a, "right_action": ra[h]}
                          for h, a in sorted(la.items()) if a != ra[h]]})
    output = {"contract": "Identity, lossless reading, whole-table comparison, and actual/root leaves only; no new positive-depth IC or OPT scan.",
              "sources": [values[2] for values in data.values()], "pairs": pairs}
    (HERE / "inspection.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    (HERE / "full-reading.txt").write_text("\n\n".join(values[3] for values in data.values()) + "\n")
    print(json.dumps({"sources": len(data), "original_ordered_actions": 4 * 2801,
                      "actual_leaves_evaluated": 4, "root_forced_leaves_evaluated": 28,
                      "new_positive_depth_IC_comparisons": 0, "new_OPT_enumerations": 0,
                      "action_differences": [p["all_action_differences"] for p in pairs]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
