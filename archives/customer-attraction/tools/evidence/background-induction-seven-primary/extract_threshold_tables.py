"""Export exact explanatory root/actual-prefix threshold tables only.

This does not repeat certificate construction, full-tree IC verification or
random discovery. The full audit is performed by verify_three_fixed_inputs.py.
"""
import json
from verify_three_fixed_inputs import BASE, FixedGame, dump

result = {}
for stem, mode in (("aggregate_entry_threshold_counterexample", "aggregate"),
                   ("last_payoff_counterexample", "last"),
                   ("threshold_monotonicity_counterexample", "threshold")):
    source = json.loads((BASE / "original" / (stem + ".json")).read_text())
    game = FixedGame(source)
    audit = json.loads((BASE / (mode + "-fixed-exact-audit.json")).read_text())
    counts = {game.zero}
    for length in range(game.m):
        count = tuple(audit["actual_ordered_path"][:length].count(a) for a in range(game.q))
        counts.add(count)
    if mode == "threshold":
        for count, action, _, _ in source["bad"]:
            counts.add(tuple(count))
            counts.add(game.next_count(tuple(count), action))
    tables = []
    for count in sorted(counts, key=lambda c: (sum(c), c)):
        floors = [min(game.payoff(t, a) for t in game.menus(game.next_count(count, a)))
                  for a in range(game.q)]
        witnesses = [min(game.menus(game.next_count(count, a)), key=lambda t: (game.payoff(t, a), t))
                     for a in range(game.q)]
        tables.append({"count": count, "action_floor_vector": list(map(str, floors)),
                       "threshold": str(max(floors)), "minimizing_child_targets": witnesses,
                       "all_credible_terminal_counts": sorted(game.menus(count))})
    result[mode] = tables
dump("threshold-explanatory-tables.json", result)
print(json.dumps({mode: {"tables": len(tables), "root_action_floors": tables[0]["action_floor_vector"],
                         "root_threshold": tables[0]["threshold"]}
                  for mode, tables in result.items()}, indent=2))
