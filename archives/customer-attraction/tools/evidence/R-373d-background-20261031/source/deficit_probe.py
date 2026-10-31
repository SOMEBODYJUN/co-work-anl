"""Finite exact search of OPT-W <= m*min_i u_i; exploratory, no general proof."""
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction.model import CustomerType, Instance
from customer_attraction.exact import ExactSPESolver


def run(seed=343734, trials=1000, topics=4, players=4):
    rng = random.Random(seed)
    closest = None
    for it in range(trials):
        mult = [rng.randrange(0, 9) if rng.randrange(3) else 0
                for _ in range(2 ** topics - 1)]
        ins = Instance(tuple(f"T{i}" for i in range(topics)), tuple(
            CustomerType(frozenset(i for i in range(topics) if mask & (1 << i)), r)
            for mask, r in enumerate(mult, 1) if r), players)
        sol = ExactSPESolver(ins)
        opt = ins.optimal_welfare()
        for counts in sol.outcomes():
            w = ins.welfare(counts)
            minimum = min(v for v, c in zip(ins.topic_payoffs(counts), counts) if c)
            gap = opt - w - players * minimum
            if closest is None or gap > closest[0]:
                closest = (gap, mult, counts, opt, w, minimum)
            if gap > 0:
                result = {"status": "counterexample", "seed": seed,
                          "iteration": it, "instance": ins.to_dict(),
                          "counts": counts, "OPT": opt, "W": w,
                          "minimum_payoff": str(minimum), "gap": str(gap),
                          "ordered_path": next(sol.ordered_outcomes(counts))}
                print(json.dumps(result, indent=2), flush=True)
                return result
        if it % 100 == 99:
            print(f"completed={it+1} best_gap={closest[0]}", flush=True)
    return {"status": "no_counterexample", "seed": seed, "trials": trials,
            "topics": topics, "players": players, "max_gap": str(closest[0])}


if __name__ == "__main__":
    trials, topics, players = map(int, sys.argv[1:]) if len(sys.argv) == 4 else (1000, 4, 4)
    result = run(trials=trials, topics=topics, players=players)
    Path(__file__).with_name(f"deficit_probe_{topics}_{players}.json").write_text(
        json.dumps(result, indent=2) + "\n")
