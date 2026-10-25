"""Exact attacks on specified general signed-price candidates, not random sampling.

Targets: lambda=1, 3/2, 2 and B+C(g)>=0, for every last-BR path.
Uses the canonical complete-history outcome-set recursion; no Markov selector.
The named examples are stress inputs, never positive evidence for all inputs.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT))
from customer_attraction.exact import ExactSPESolver
from customer_attraction.model import CustomerType, Instance


def signed_cost(g):
    pos = [max(x, 0) for x in g]
    neg = [max(-x, 0) for x in g]
    return 2 * sum(pos) - sum(neg) + max(pos, default=0) + max(neg, default=0)


def examine(instance):
    solver = ExactSPESolver(instance)
    solver.outcomes()
    opt = instance.optimal_welfare()
    best = {"signed": None, "lambda1": None, "lambda3/2": None, "lambda2": None}
    n_br = 0
    for path in product(range(instance.topic_count), repeat=instance.players):
        final = instance.counts(path, terminal=True)
        prefix = instance.counts(path[:-1])
        if instance.topic_payoff(path[-1], final) != solver.threshold(prefix):
            continue
        n_br += 1
        u = instance.player_payoffs(path)
        ms = [solver.threshold(instance.counts(path[:i])) for i in range(instance.players - 1)]
        g = [a - b for a, b in zip(ms, u)]
        welfare = instance.welfare(final)
        b = 2 * welfare - opt
        vals = {"signed": b + signed_cost(g), "lambda1": b + sum(g),
                "lambda3/2": b + F(3, 2) * sum(g), "lambda2": b + 2 * sum(g)}
        record = {"path": path, "W": welfare, "OPT": opt, "B": b,
                  "u": list(map(str, u)), "M_early": list(map(str, ms)),
                  "g": list(map(str, g)), "C": str(signed_cost(g))}
        for key, val in vals.items():
            if best[key] is None or val < best[key][0]:
                best[key] = val, dict(record, value=str(val))
    return {"instance": instance.to_dict(), "last_BR_paths": n_br,
            "stats": solver.stats.__dict__, "minima": {k: v[1] for k, v in best.items()}}


def main():
    base = ROOT / "examples/customer_attraction"
    out = {}
    # Explicit named targets: a rich root-tax stress input and its m=5 substitution.
    data = json.loads((base / "root_tax_failure.json").read_text())
    for m in (4, 5):
        out[f"root_tax_m{m}"] = examine(Instance.from_dict(dict(data, players=m)))
    # The old saturated core used in the all-parameter padding construction.
    core = [({0}, 3), ({1}, 4), ({2, 3}, 6), ({2, 4}, 6),
            ({0, 3, 4}, 2), ({1, 3, 4}, 2)]
    instance = Instance(tuple(map(str, range(5))),
                        tuple(CustomerType(frozenset(s), n) for s, n in core), 5)
    out["old_core_m5"] = examine(instance)
    target = Path(__file__).with_name("designated_seed_attack.json")
    target.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({name: {key: value["value"] for key, value in item["minima"].items()}
                      for name, item in out.items()}, indent=2))


if __name__ == "__main__":
    main()
