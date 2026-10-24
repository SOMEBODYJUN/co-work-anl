"""Targeted exact attacks on TB-ANY using Cartesian catalogs.

TB-ANY alone is tested: OPT_m <= W(arbitrary path)+sum true thresholds.
Products allow cross-coordinate continuation threats, unlike dense random input.
Negative results are finite diagnostics, never positive theorems.
"""
import itertools
import json
import sys
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5]))
from customer_attraction.model import CustomerType, Instance
from customer_attraction.exact import ExactSPESolver


def product_instance(factors, players, null=True):
    labels = tuple(itertools.product(*(range(p) for p, _ in factors)))
    topics = tuple(map(str, labels)) + (("empty",) if null else ())
    customers = []
    for k, (_, types) in enumerate(factors):
        for mask, weight in types.items():
            interested = frozenset(j for j, label in enumerate(labels)
                                  if mask >> label[k] & 1)
            customers.append(CustomerType(interested, weight))
    return Instance(topics, tuple(customers), players)


def attack(instance):
    solver = ExactSPESolver(instance)
    solver.outcomes()
    p, m = instance.topic_count, instance.players

    @lru_cache(None)
    def budget(k):
        if sum(k) == m:
            return instance.welfare(k), ()
        children = []
        for a in range(p):
            kk = k[:a] + (k[a] + 1,) + k[a+1:]
            value, path = budget(kk)
            children.append((value, (a,) + path))
        value, path = min(children)
        return solver.threshold(k) + value, path

    value, path = budget((0,) * p)
    optimum = instance.optimal_welfare()
    return {"topics": p, "players": m, "clients": sum(c.multiplicity for c in instance.customers),
            "optimum": optimum, "minimum_budget": str(value), "gap": str(value-optimum),
            "path": path,
            "thresholds": [str(solver.threshold(instance.counts(path[:i]))) for i in range(m)],
            "welfare": instance.welfare(instance.counts(path)),
            "counterexample": value < optimum,
            "states": solver.stats.count_states,
            **({"instance": instance.to_dict()} if value < optimum else {})}


if __name__ == "__main__":
    five = (3, {2: 1, 5: 2, 6: 2})
    two = (2, {1: 1, 2: 1})
    asym = (3, {1: 1, 2: 2, 4: 3})
    cases = [("five_x_five", [five, five], 3),
             ("five_x_five", [five, five], 4),
             ("five_x_two", [five, two], 4),
             ("five_x_asym", [five, asym], 4),
             ("two_x_two_x_two", [two, two, two], 5)]
    reports = []
    for name, factors, m in cases:
        report = {"case": name, **attack(product_instance(factors, m))}
        reports.append(report)
        print(json.dumps(report), flush=True)
        if report["counterexample"]:
            break
    output = {"candidate": "TB-ANY", "reports": reports,
              "status": "finite exact diagnostic; no positive proof interpretation"}
    target = Path(__file__).with_name("threshold_product_diagnostic.json")
    target.write_text(json.dumps(output, indent=2) + "\n")
