"""Exploratory finite cone search; floating LP output is not a proof."""
from __future__ import annotations

import argparse
import itertools as it
import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog


def data(k, n):
    masks = np.arange(1, 1 << k)
    members = ((masks[None, :] >> np.arange(k)[:, None]) & 1).astype(float)
    backgrounds = list(it.combinations_with_replacement(range(k), n - 1))
    loads = np.array([members[list(b)].sum(axis=0) for b in backgrounds])
    static = members[None, :, :] / (1 + loads[:, None, :])
    return members, static


def random_spe(members, n, w, rng):
    """Build a complete ordered-history strategy by ordinary BI."""
    k = len(members)
    policy = {}
    terminals = {}

    def solve(h):
        if len(h) == n:
            terminals[h] = h
            return h
        ends = [solve(h + (a,)) for a in range(k)]
        values = []
        for a, z in enumerate(ends):
            load = members[list(z)].sum(axis=0)
            values.append(np.dot(members[a] / np.maximum(load, 1), w))
        best = max(values)
        candidates = [a for a in range(k) if values[a] >= best - 1e-10]
        action = int(rng.choice(candidates))
        policy[h] = action
        terminals[h] = ends[action]
        return ends[action]

    solve(())
    return policy, terminals


def cone(members, policy, terminals):
    rows = []
    node_rows = []
    for h, a0 in policy.items():
        z0 = terminals[h]
        v0 = members[a0] / np.maximum(members[list(z0)].sum(axis=0), 1)
        for a in range(len(members)):
            if a == a0:
                continue
            z = terminals[h + (a,)]
            va = members[a] / np.maximum(members[list(z)].sum(axis=0), 1)
            rows.append(v0 - va)
            node_rows.append((h, a))
    c = (members[list(terminals[()])].sum(axis=0) > 0).astype(float)
    return np.array(rows), c, node_rows


def safety(static, w):
    matrix = np.einsum("bkt,t->bk", static, w)
    k = matrix.shape[1]
    obj = np.zeros(k + 1)
    obj[-1] = -1
    ub = np.column_stack((-matrix, np.ones(len(matrix))))
    ans = linprog(obj, A_ub=ub, b_ub=np.zeros(len(ub)),
                  A_eq=[np.r_[np.ones(k), 0]], b_eq=[1],
                  bounds=[(0, None)] * (k + 1), method="highs")
    if not ans.success:
        raise RuntimeError(ans.message)
    return ans.x[:-1], ans.x[-1]


def optimize(members, static, gamma, c, p, factor):
    beta = np.einsum("k,bkt->bt", p, static)
    a_ub = np.vstack((np.column_stack((-gamma, np.zeros(len(gamma)))),
                      np.column_stack((-beta, np.ones(len(beta))))))
    obj = np.r_[c, -factor]
    ans = linprog(obj, A_ub=a_ub, b_ub=np.zeros(len(a_ub)),
                  A_eq=[np.r_[np.ones(len(c)), 0]], b_eq=[1],
                  bounds=[(0, None)] * (len(c) + 1), method="highs")
    if not ans.success:
        raise RuntimeError(ans.message)
    return ans


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topics", type=int, default=6)
    ap.add_argument("--players", type=int, default=3)
    ap.add_argument("--trials", type=int, default=100)
    ap.add_argument("--seed", type=int, default=33141)
    ap.add_argument("--factor", type=float)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)
    members, static = data(args.topics, args.players)
    factor = args.factor or args.players
    summary = {"kind": "floating exploration, not proof", "args": vars(args).copy(),
               "best_objective": 0.0, "trials": []}
    summary["args"]["output"] = str(args.output)
    for trial in range(args.trials):
        # Both sparse integer-like populations and fully supported ones.
        w = rng.exponential(size=members.shape[1])
        w[rng.random(len(w)) < 0.6] = 0
        w /= w.sum()
        policy, terminals = random_spe(members, args.players, w, rng)
        gamma, c, node_rows = cone(members, policy, terminals)
        p0, v0 = safety(static, w)
        distributions = [p0, np.ones(args.topics) / args.topics,
                         rng.dirichlet(np.ones(args.topics))]
        record = {"trial": trial, "root": terminals[()], "initial_W": float(c @ w),
                  "initial_v": float(v0), "objectives": []}
        for p in distributions:
            ans = optimize(members, static, gamma, c, p, factor)
            record["objectives"].append(float(ans.fun))
            if ans.fun < summary["best_objective"] - 1e-9:
                summary["best_objective"] = float(ans.fun)
                summary["best_witness"] = {
                    "policy": {",".join(map(str, h)): a for h, a in policy.items()},
                    "p": p.tolist(), "w": ans.x[:-1].tolist(), "t": float(ans.x[-1]),
                    "root": terminals[()]}
        summary["trials"].append(record)
        if trial % 10 == 0:
            print(json.dumps({"trial": trial, "best": summary["best_objective"]}), flush=True)
            args.output.write_text(json.dumps(summary, indent=2) + "\n")
        if summary["best_objective"] < -1e-7:
            break
    args.output.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({"completed": len(summary["trials"]),
                      "best": summary["best_objective"]}), flush=True)


if __name__ == "__main__":
    main()
