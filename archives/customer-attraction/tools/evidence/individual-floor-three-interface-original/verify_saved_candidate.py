"""Replay the saved finite policy from the unit-customer definition, exactly.

No original solver or LP code is imported. This verifies a particular input,
not universal validity or invalidity of any welfare bound.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations
from functools import cache
import hashlib
import json

HERE = Path(__file__).resolve().parent


def main():
    source = HERE / "original/candidate_near_kplus_0_kplus_3.json"
    raw = source.read_bytes()
    data = json.loads(raw)
    assert set(data) == {"name", "type", "a", "path", "portfolio", "value", "clones", "actions"}
    assert data["name"] == "near_kplus_0" and data["type"] == "kplus"
    counts = data["clones"]
    topics = (len(counts) + 1).bit_length() - 1
    players = len(data["path"])
    assert len(counts) == (1 << topics) - 1
    assert all(type(v) is int and v >= 0 for v in counts)
    blocks = [(s, v) for s, v in enumerate(counts, 1) if v]
    actions = {}
    for item in data["actions"]:
        assert set(item) == {"history", "action"}
        history, action = tuple(item["history"]), item["action"]
        assert history not in actions
        assert type(action) is int and action in range(topics)
        assert all(type(a) is int and a in range(topics) for a in history)
        actions[history] = action
    required = {h for depth in range(players) for h in product(range(topics), repeat=depth)}
    assert set(actions) == required

    @cache
    def finish(history):
        return history if len(history) == players else finish(history + (actions[history],))

    @cache
    def utility(terminal, action):
        return sum((F(v, sum(bool((s >> a) & 1) for a in terminal))
                    for s, v in blocks if (s >> action) & 1), F())

    def coverage(support):
        mask = sum(1 << a for a in set(support))
        return sum(v for s, v in blocks if s & mask)

    per_depth = []
    for depth in range(players):
        slacks = []
        for history in product(range(topics), repeat=depth):
            action = actions[history]
            actual = utility(finish(history), action)
            for alternative in range(topics):
                slack = actual - utility(finish(history + (alternative,)), alternative)
                assert slack >= 0, (history, action, alternative, slack)
                slacks.append(slack)
        per_depth.append({"depth": depth, "histories": topics**depth,
                          "comparisons_with_self": len(slacks),
                          "zero_slacks": sum(s == 0 for s in slacks),
                          "positive_slacks": sum(s > 0 for s in slacks),
                          "minimum_positive_slack": str(min(s for s in slacks if s > 0))})

    path = finish(())
    assert path == tuple(data["path"])
    profits = [utility(path, action) for action in path]
    welfare = coverage(path)
    assert sum(profits) == welfare
    sizes = [sum(v for s, v in blocks if (s >> a) & 1) for a in range(topics)]
    largest = max(sizes)
    witnesses = []
    for a, b in combinations(range(topics), 2):
        witness = next(s for s, v in blocks if bool((s >> a) & 1) != bool((s >> b) & 1))
        witnesses.append({"topics": [a, b], "positive_distinguishing_type": witness})
    portfolios = [{"support": support, "coverage": coverage(support)}
                  for support in combinations(range(topics), min(topics, players))]
    optimum = max(row["coverage"] for row in portfolios)
    ordered_optimum = max(coverage(terminal) for terminal in product(range(topics), repeat=players))
    assert ordered_optimum == optimum == sum(counts)
    assert coverage(data["portfolio"]) == optimum
    attacked_profit = utility(path, data["a"])
    gap = optimum - largest - players * attacked_profit
    assert gap > 0 and gap / welfare == F(data["value"])
    report = {
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "players": players, "topics": topics, "all_incidence_entries_checked": len(counts),
        "positive_types": blocks, "unit_customers": sum(counts),
        "ordered_histories": len(required), "comparisons_with_self": sum(r["comparisons_with_self"] for r in per_depth),
        "per_depth": per_depth, "topic_distinctness_witnesses": witnesses,
        "path": path, "profits": list(map(str, profits)), "W": welfare,
        "topic_sizes": sizes, "K": largest, "OPT": optimum,
        "support_portfolios": portfolios, "ordered_portfolios_checked": topics**players,
        "attacked_topic": data["a"], "attacked_positions_one_based": [i + 1 for i, a in enumerate(path) if a == data["a"]],
        "attacked_profit": str(attacked_profit), "OPT_minus_K_minus_m_u": str(gap),
        "normalized_K_gap": str(gap / welfare),
        "each_OPT_minus_2m_u": [str(optimum - 2 * players * u) for u in profits],
        "each_OPT_minus_W_minus_m_u": [str(optimum - welfare - players * u) for u in profits],
        "twice_W_minus_OPT": 2 * welfare - optimum,
        "conclusion": "saved complete pure SPE refutes only the K-plus-m-times-individual auxiliary bridge among these tests",
        "LP_generation_reproduced": False,
    }
    target = HERE / "new-definition-replay.json"
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"report": str(target.relative_to(HERE)), "histories": len(required),
                      "comparisons": report["comparisons_with_self"], "K_gap": str(gap),
                      "normalized_gap": str(gap / welfare)}))


if __name__ == "__main__":
    main()
