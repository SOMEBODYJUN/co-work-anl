"""Full ordered-history SPE discovery MILP; numerical proposals require exact audit.

Every node carries all players' eventual utilities. Chosen-edge equalities and
one-step best responses enforce the entire tree. Normalize one actual utility
to one; its true deviation guarantees |T| <= m for every common topic T, hence
all terminal utility variables lie in [0,m]. This gives a valid finite big-M.
No count-Markov selector and no finite off-path truncation are imposed.
"""
from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_array

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))


def build(m, p, player, objective="gap"):
    if not (m >= 1 and p >= 1 and 0 <= player < m):
        raise ValueError("positive m,p and 0 <= player < m required")
    masks = list(range(1, 1 << p))
    histories = [h for d in range(m + 1) for h in itertools.product(range(p), repeat=d)]
    internal = [h for h in histories if len(h) < m]
    types = {b: j for j, b in enumerate(masks)}
    utilities = {(h, i): len(masks) + k * m + i
                 for k, h in enumerate(histories) for i in range(m)}
    offset = len(masks) + len(histories) * m
    choices = {(h, a): offset + k * p + a
               for k, h in enumerate(internal) for a in range(p)}
    n = offset + len(internal) * p
    lower = np.zeros(n)
    upper = np.full(n, float(m))
    upper[offset:] = 1
    # Fix root action to 0 by common-topic relabeling; the comparison portfolio
    # is NOT fixed relative to action 0, so both root-in and root-out cases run.
    lower[choices[(), 0]] = upper[choices[(), 0]] = 1
    integrality = np.zeros(n, dtype=np.uint8)
    integrality[offset:] = 1
    rows, cols, values, lbs, ubs = [], [], [], [], []

    def add(items, lo=-np.inf, hi=np.inf):
        row = len(lbs)
        for j, v in items:
            if v:
                rows.append(row); cols.append(j); values.append(float(v))
        lbs.append(lo); ubs.append(hi)

    for a in range(p):
        add(((types[b], 1) for b in masks if b & (1 << a)), hi=m)
    for h in histories:
        if len(h) != m:
            continue
        for i, a in enumerate(h):
            terms = [(utilities[h, i], 1)]
            for b in masks:
                if b & (1 << a):
                    terms.append((types[b], -1 / sum(bool(b & (1 << c)) for c in h)))
            add(terms, 0, 0)
    for h in internal:
        add(((choices[h, a], 1) for a in range(p)), 1, 1)
        for a in range(p):
            child = h + (a,)
            add([(utilities[h, len(h)], 1), (utilities[child, len(h)], -1)], 0)
            for i in range(m):
                # |v_h - v_child| <= m(1-x_ha).
                add([(utilities[h, i], 1), (utilities[child, i], -1), (choices[h, a], m)], hi=m)
                add([(utilities[h, i], -1), (utilities[child, i], 1), (choices[h, a], m)], hi=m)
    add([(utilities[(), player], 1)], 1, 1)
    matrix = coo_array((values, (rows, cols)), shape=(len(lbs), n)).tocsc()
    return dict(m=m, p=p, player=player, objective=objective, masks=masks,
                utilities=utilities, choices=choices, lower=lower, upper=upper,
                integrality=integrality, constraint=LinearConstraint(matrix, lbs, ubs),
                n=n, rows=len(lbs))


def solve(model, portfolio, seconds):
    c = np.zeros(model["n"])
    if model["objective"] == "terminal":
        c[model["utilities"][(), model["m"] - 1]] = -1
    else:
        for j, b in enumerate(model["masks"]):
            c[j] = -int(any(b & (1 << a) for a in portfolio))
    if model["objective"] == "gap":
        for i in range(model["m"]):
            c[model["utilities"][(), i]] = 1
    result = milp(c, integrality=model["integrality"],
                  bounds=Bounds(model["lower"], model["upper"]),
                  constraints=model["constraint"],
                  options={"time_limit": seconds, "mip_rel_gap": 1e-9})
    out = {"status": int(result.status), "message": str(result.message),
           "portfolio": portfolio, "variables": model["n"], "constraints": model["rows"],
           "limitation": "numerical MILP proposal, not an exact or general theorem"}
    for name in ["fun", "mip_gap", "mip_node_count", "mip_dual_bound"]:
        value = getattr(result, name, None)
        out[name] = None if value is None else float(value)
    if result.x is not None:
        x = result.x
        actions = {}
        for h, a in model["choices"]:
            if x[model["choices"][h, a]] > .5:
                actions[h] = a
        assert len(actions) * model["p"] == len(model["choices"])
        out.update(types=x[:len(model["masks"])].tolist(),
                   actions=[{"history": h, "action": a} for h, a in actions.items()],
                   root_utilities=[float(x[model["utilities"][(), i]]) for i in range(model["m"])],
                   objective_proposal=-float(result.fun))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--players", type=int, default=3)
    ap.add_argument("--topics", type=int, default=4)
    ap.add_argument("--player", type=int, default=0)
    ap.add_argument("--objective", choices=["gap", "individual", "terminal"], default="gap")
    ap.add_argument("--seconds", type=float, default=30)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    if args.out.exists():
        raise FileExistsError(args.out)
    model = build(args.players, args.topics, args.player, args.objective)
    k = min(args.players, args.topics)
    portfolios = [tuple(range(k))]
    if k < args.topics and args.objective != "terminal":
        portfolios.append(tuple(range(1, k + 1)))
    results = []
    for portfolio in portfolios:
        start = time.monotonic()
        record = solve(model, portfolio, args.seconds)
        record["elapsed_seconds"] = time.monotonic() - start
        results.append(record)
        print(json.dumps({k: v for k, v in record.items() if k not in {"actions", "types"}}), flush=True)
    args.out.write_text(json.dumps({"parameters": vars(args) | {"out": str(args.out)},
                                    "results": results}, indent=2) + "\n")


if __name__ == "__main__":
    main()
