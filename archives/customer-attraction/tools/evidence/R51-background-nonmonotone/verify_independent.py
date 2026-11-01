"""Exhaust all 4**5 complete two-player pure strategies in two backgrounds.

The 18 unit customers are expanded individually. No canonical solver, count
recursion, optimization, randomness, or external package is used.
"""
from fractions import Fraction
from hashlib import sha256
from itertools import product
from pathlib import Path
import json


HERE = Path(__file__).resolve().parent
raw = (HERE / "background_nonmonotone.json").read_bytes()
assert len(raw) == 1142
assert sha256(raw).hexdigest() == "d39c34ac24c04ffb5bc321b4d41b6915bc9703e3cb72c3776a293f7e6c7c439e"
source = json.loads(raw)
instance = source["instance"]
assert instance["topics"] == ["0", "1", "2", "3"]
assert instance["players"] == 3
assert source["base"] == [1, 0, 0, 0] and source["add"] == 3 and source["r"] == 2
types = [(tuple(c["topics"]), c["multiplicity"]) for c in instance["customers"]]
assert types == [((0,), 3), ((0, 1), 3), ((2,), 3), ((1, 2), 2),
                 ((0, 3), 1), ((0, 1, 3), 2), ((2, 3), 3), ((1, 2, 3), 1)]
customers = tuple(frozenset(c["topics"]) for c in instance["customers"]
                  for _ in range(c["multiplicity"]))
assert len(customers) == 18
actions = tuple(range(4))


def counts(history):
    return tuple(history.count(a) for a in actions)


def terminal_info(prefix, first, last):
    history = prefix + (first, last)
    loads = tuple(sum(a in customer for a in history) for customer in customers)
    payoffs = tuple(sum((Fraction(1, load) for customer, load in zip(customers, loads)
                         if a in customer), Fraction()) for a in (first, last))
    active_profit = sum((Fraction(int(first in c) + int(last in c), load)
                         for c, load in zip(customers, loads) if load), Fraction())
    assert sum(payoffs) == active_profit
    welfare = sum(load > 0 for load in loads)
    return {"terminal_counts": counts(history), "payoffs": payoffs,
            "active_profit": active_profit, "total_welfare": welfare}


def examine(prefix):
    table = {(a, b): terminal_info(prefix, a, b) for a, b in product(actions, repeat=2)}
    best = {a: tuple(b for b in actions if table[a, b]["payoffs"][1] ==
                    max(table[a, c]["payoffs"][1] for c in actions)) for a in actions}
    strategies = []
    candidates_examined = 0
    for first, b0, b1, b2, b3 in product(actions, repeat=5):
        candidates_examined += 1
        replies = (b0, b1, b2, b3)
        if any(replies[a] not in best[a] for a in actions):
            continue
        current_values = tuple(table[a, replies[a]]["payoffs"][0] for a in actions)
        if current_values[first] < max(current_values):
            continue
        info = table[first, replies[first]]
        strategies.append({"first_action": first, "last_replies": replies,
                           "ordered_suffix": (first, replies[first]),
                           "terminal_counts": info["terminal_counts"],
                           "payoffs": tuple(map(str, info["payoffs"])),
                           "active_profit": str(info["active_profit"]),
                           "total_welfare": info["total_welfare"],
                           "first_action_payoffs_with_these_replies": tuple(map(str, current_values))})
    assert candidates_examined == 1024
    attainable = {(Fraction(s["active_profit"]), tuple(s["terminal_counts"])) for s in strategies}
    minimum = min(attainable)
    selected = next(s for s in strategies if (Fraction(s["active_profit"]), tuple(s["terminal_counts"])) == minimum)
    rows = [{"first_action": a, "last_action": b,
             "payoffs": tuple(map(str, table[a, b]["payoffs"])),
             "active_profit": str(table[a, b]["active_profit"]),
             "total_welfare": table[a, b]["total_welfare"]} for a, b in table]
    return {"past_ordered_history": prefix, "past_topic_counts": counts(prefix),
            "total_players": len(prefix) + 2,
            "fixed_remaining_players": 2,
            "unit_customer_count": len(customers),
            "complete_pure_strategies_examined": candidates_examined,
            "last_best_replies_at_all_four_first_action_children": best,
            "complete_pure_spe_count": len(strategies),
            "complete_pure_spes": strategies,
            "all_spe_terminal_count_profit_pairs": [[str(v), c] for v, c in sorted(attainable)],
            "lexicographic_minimum_profit_and_terminal_counts": [str(minimum[0]), minimum[1]],
            "selected_minimizing_spe": selected,
            "all_spe_welfares": sorted({s["total_welfare"] for s in strategies}),
            "all_sixteen_terminal_payoff_rows": rows}


before, after = examine((0,)), examine((0, 3))
assert before["complete_pure_spe_count"] == 3
assert after["complete_pure_spe_count"] == 1
assert before["lexicographic_minimum_profit_and_terminal_counts"] == [source["original"][0], tuple(source["original"][1])]
assert after["lexicographic_minimum_profit_and_terminal_counts"] == [source["added"][0], tuple(source["added"][1])]
assert before["all_spe_welfares"] == after["all_spe_welfares"] == [18]
assert [tuple(s["terminal_counts"]) for s in after["complete_pure_spes"]] == [(2, 0, 1, 1)]
assert before["selected_minimizing_spe"]["last_replies"] == (2, 2, 2, 2)
assert after["selected_minimizing_spe"]["last_replies"] == (2, 2, 0, 2)
assert before["selected_minimizing_spe"]["first_action"] == after["selected_minimizing_spe"]["first_action"] == 2
assert all(Fraction(after["all_sixteen_terminal_payoff_rows"][i]["active_profit"]) <=
           Fraction(before["all_sixteen_terminal_payoff_rows"][i]["active_profit"]) for i in range(16))
output = {"check_kind": "exhaustive-definition-level-complete-two-player-strategy-enumeration",
          "canonical_package_imported": False,
          "count_cached_outcome_recursion_used": False,
          "arithmetic": "fractions.Fraction on 18 expanded unit customers",
          "primary_bytes": len(raw), "primary_sha256": sha256(raw).hexdigest(),
          "source_semantic_fields_match": True,
          "before": before, "after": after,
          "pointwise_same_suffix_active_profit_nonincreasing_for_all_16_suffixes": True,
          "minimum_spe_active_profit_strictly_increases": "9 < 11",
          "backgrounds_are_legal_topic_prefixes": True,
          "past_players_root_incentives_checked": False,
          "full_root_spe_claimed": False,
          "six_player_half_claimed": False,
          "all_checks_passed": True}
print(json.dumps(output, ensure_ascii=False, indent=2))
