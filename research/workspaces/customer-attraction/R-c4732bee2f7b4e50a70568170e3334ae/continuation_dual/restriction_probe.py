"""All-history independent-row cone versus explicit history/action restrictions.

Floating LPs are exploratory. Exact rational primal separation witnesses are
verified for the restriction, then every omitted genuine SPE row is inspected.
Nothing here promotes a restricted cone witness to a genuine SPE.
"""
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import importlib.util
import json
import sys

import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]
spec = importlib.util.spec_from_file_location("strategy_lp", ROOT / "tests/audits/customer_attraction_strategy_lp.py")
lp = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lp
spec.loader.exec_module(lp)


def rows_for(cone, portfolio, mode):
    rows, labels = [], []
    J = set(portfolio)
    root_path = tuple(a for a, count in enumerate(cone.root) for _ in range(count))
    actual_history = ()
    actual_prefixes = set()
    while len(actual_history) < cone.players:
        actual_prefixes.add(actual_history)
        actual_history += (cone.actions[actual_history],)
    for h, action in cone.actions.items():
        if mode == "permutation_prefix" and (len(set(h)) != len(h) or not set(h) <= J):
            continue
        if mode == "comparator_prefix" and not set(h) <= J:
            continue
        if mode == "onpath" and h not in actual_prefixes:
            continue
        actual = lp.payoff_row(cone.topics, cone.terminals[h], action)
        for alternative in range(cone.topics):
            if mode != "full" and alternative not in J:
                continue
            if mode == "permutation_prefix" and alternative in h:
                continue
            row = tuple(x-y for x,y in zip(actual, lp.payoff_row(cone.topics, cone.terminals[h+(alternative,)], alternative)))
            if any(row):
                rows.append(row)
                labels.append((h, alternative))
    return rows, labels


def probe(cone, portfolio, mode):
    rows, labels = rows_for(cone, portfolio, mode)
    C = lp.StrategyCone.__new__(lp.StrategyCone)
    C.__dict__.update(cone.__dict__)
    C.rows = tuple(rows)
    C.matrix = np.asarray(rows, dtype=float)
    if not rows:
        C.matrix = np.zeros((0, len(cone.welfare)))
    result = C.optimize(portfolio)
    if not result["certified"]:
        return {"status": result["status"]}
    exact = result["values"]
    omitted = []
    for h, action in cone.actions.items():
        actual = lp.payoff_row(cone.topics, cone.terminals[h], action)
        for alternative in range(cone.topics):
            row = tuple(x-y for x,y in zip(actual, lp.payoff_row(cone.topics, cone.terminals[h+(alternative,)], alternative)))
            value = lp.dot(row, exact)
            if value < 0:
                omitted.append({"history": h, "alternative": alternative, "slack": value})
    return {"value": result["value"], "dual_bound": result["dual_bound"],
            "point": exact, "negative_genuine_rows": omitted,
            "dual": [{"history": labels[i][0], "alternative": labels[i][1], "weight": w}
                     for i,w in result["dual_support"]]}


def main():
    source = json.loads((ROOT / "evidence/runs/2026-10-09/customer_attraction_strategy_lp_m4p5_certified.json").read_text())
    best = {}
    failures = {}
    for ci, saved in enumerate(source["cone_proofs"]):
        cone = lp.StrategyCone(5,4,{tuple(x["history"]):x["action"] for x in saved["actions"]})
        for portfolio in combinations(range(5),4):
            for mode in ["full", "portfolio_actions", "comparator_prefix", "permutation_prefix", "onpath"]:
                result = probe(cone,portfolio,mode)
                if "value" not in result:
                    continue
                if result["value"] > best.get(mode,0):
                    best[mode] = result["value"]
                    print(mode,ci,portfolio,result["value"],flush=True)
                if result["value"] > 2 and mode not in failures:
                    failures[mode] = {"cone":ci,"portfolio":portfolio,"actions":saved["actions"],**result}
        if len(failures) == 4:
            break
    out = {"scope":"finite sample; restrictions' witnesses are not necessarily SPE", "best":best,"failures":failures}
    Path(__file__).with_suffix(".json").write_text(json.dumps(lp.serializable(out),indent=2))


if __name__ == "__main__":
    main()
