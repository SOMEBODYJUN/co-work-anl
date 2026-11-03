"""One finite missing-F check and one local certificate transfer; no SPE solver.

Inputs are the frozen strict instance, author's complete strategy and 777B
report, plus the already audited independent full strategy in its old report.
The old full-SPE audit is reused as evidence; this script does not repeat it.
"""
import argparse
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from pathlib import Path
import json


def main():
    ap = argparse.ArgumentParser()
    for name in ("input", "strategy", "author_report", "old_report", "output"):
        ap.add_argument("--" + name.replace("_", "-"), type=Path, required=True)
    args = ap.parse_args()
    raw = json.loads(args.input.read_text())
    inst = raw["instance"]
    m, n = inst["players"], len(inst["topics"])
    customers = [frozenset(c["topics"]) for c in inst["customers"]
                 for _ in range(c.get("multiplicity", 1))]
    sets = [frozenset(x for x, c in enumerate(customers) if a in c)
            for a in range(n)]
    maxima = [a for a in range(n)
              if not any(sets[a] < sets[b] for b in range(n))
              and sets[a] not in sets[:a]]
    target = tuple(raw["path"])
    coverage = frozenset().union(*(sets[a] for a in target))
    private = {a: sets[a] - frozenset().union(
        *(sets[b] for b in maxima if b != a)) for a in maxima}
    omitted = {a: private[a] - coverage for a in maxima}
    old_slots = sorted((F(len(omitted[a]), k) + F(len(sets[a] - omitted[a]), m)
                        for a in maxima for k in range(1, m + 1)), reverse=True)
    background = [0] * len(customers)
    rows = []
    slots = candidates = admissible = 0
    for i, act in enumerate(target):
        r = m - i
        f_by, g_by = {}, {}
        for a in maxima:
            fv, gv = [], []
            for k in range(1, r + 1):
                slots += 1
                values = []
                for others in combinations_with_replacement(range(n), r - 1):
                    candidates += 1
                    if sum(bool(sets[t] & omitted[a]) for t in others) > k - 1:
                        continue
                    admissible += 1
                    values.append(sum((F(1, background[x] + 1 +
                        sum(x in sets[t] for t in others)) for x in sets[a]), F()))
                assert values
                f = min(values)
                g = F(len(omitted[a]), k) + sum((
                    F(1, background[x] + r) for x in sets[a] - omitted[a]), F())
                assert f >= g
                fv.append(f)
                gv.append(g)
            f_by[str(a)], g_by[str(a)] = list(map(str, fv)), list(map(str, gv))
        fs = sorted((F(v) for values in f_by.values() for v in values), reverse=True)
        gs = sorted((F(v) for values in g_by.values() for v in values), reverse=True)
        direct = max(sum((F(1, background[x] + r) for x in sets[a]), F())
                     for a in maxima)
        rows.append({"i": i + 1, "remaining": r,
                     "F_by_topic": f_by, "G_by_topic": g_by,
                     "F_threshold": str(fs[r - 1]), "G_threshold": str(gs[r - 1]),
                     "old_rank": str(old_slots[r - 1]), "direct": str(direct)})
        for x in sets[act]:
            background[x] += 1
    author = json.loads(args.author_report.read_text())
    for a, b in zip(rows, author["rows"], strict=True):
        assert [a["i"], a["remaining"], a["F_threshold"], a["G_threshold"],
                a["old_rank"], a["direct"]] == [b["i"], b["remaining"],
                b["F_spectrum"], b["G_spectrum"], b["old_spectrum"], b["direct"]]
    fsum = sum((F(r["F_threshold"]) for r in rows), F())
    gsum = sum((F(r["G_threshold"]) for r in rows), F())
    osum = sum((max(F(r["old_rank"]), F(r["direct"])) for r in rows), F())
    assert str(fsum) == author["F_sum"]
    assert str(gsum) == author["G_sum"] == raw["new"]
    assert str(osum) == author["old_combined_sum"] == raw["old_combined"]
    assert str(gsum - osum) == author["strict_gap"] == raw["gap"]
    cert = json.loads(args.strategy.read_text())
    old_report = json.loads(args.old_report.read_text())
    new_actions = {tuple(x["history"]): x["action"] for x in cert["actions"]}
    old_actions = {tuple(x["history"]): x["action"] for x in old_report["actions"]}
    expected = {h for d in range(m) for h in product(range(n), repeat=d)}
    assert len(new_actions) == len(cert["actions"]) == len(expected)
    assert len(old_actions) == len(old_report["actions"]) == len(expected)
    assert set(new_actions) == set(old_actions) == expected
    differences = [(h, old_actions[h], new_actions[h]) for h in sorted(expected)
                   if old_actions[h] != new_actions[h]]
    assert differences == [((3, 2), 0, 4)]
    assert target == tuple(old_report["actual_path"])
    assert cert["terminal_counts"] == [target.count(a) for a in range(n)]

    def utility(i, z):
        return sum((F(1, sum(a in c for a in z)) for c in customers if z[i] in c), F())

    old_z, new_z = (3, 2, 0), (3, 2, 4)
    last = (utility(2, old_z), utility(2, new_z))
    parent = (utility(1, old_z), utility(1, new_z))
    assert last == (F(65, 2), F(65, 2))
    assert parent == (F(32), F(32))
    assert old_actions[(3,)] == new_actions[(3,)] == 0
    # Only the changed last node and its parent IC vector can be affected.
    # Parent uses action 0, so its prescribed branch and the root branch stay.
    report = {"scope": "30 exact static F/G slots plus one local strategy transfer; old full SPE audit reused",
              "unit_customers": len(customers), "static_slots": slots,
              "candidate_backgrounds_before_filter": candidates,
              "admissible_backgrounds": admissible, "rows": rows,
              "F_sum": str(fsum), "G_sum": str(gsum), "old_sum": str(osum),
              "strict_gap": str(gsum - osum),
              "strategy_difference": {"history": [3, 2], "old_action": 0, "new_action": 4},
              "last_player_old_new": list(map(str, last)),
              "parent_deviator_old_new": list(map(str, parent)),
              "parent_prescribed_action": 0,
              "new_SPE_tree_sweeps": 0, "original_entry_calls": 0,
              "canonical_solver_calls": 0, "random_inputs_generated": 0,
              "status": "all limited checks passed"}
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ("static_slots", "candidate_backgrounds_before_filter",
        "admissible_backgrounds", "F_sum", "G_sum", "strict_gap", "status")}))


if __name__ == "__main__":
    main()
