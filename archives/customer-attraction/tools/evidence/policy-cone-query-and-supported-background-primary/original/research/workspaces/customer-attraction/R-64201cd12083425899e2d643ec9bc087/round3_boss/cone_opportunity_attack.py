"""Fixed complete-policy attacks, not an enumeration of all SPEs.

Reweight every nonempty customer-interest type while retaining every ordered
history incentive.  A positive optimum gives only a candidate until exact
reconstruction; an unsuccessful LP has no general mathematical implication.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import linprog


def policies(obj, label):
    if isinstance(obj, dict):
        if isinstance(obj.get("actions"), list) and "terminal_counts" in obj:
            yield label, obj
        for key, value in obj.items():
            if key != "actions":
                yield from policies(value, label + "/" + key)
    elif isinstance(obj, list):
        for j, value in enumerate(obj):
            if isinstance(value, (dict, list)):
                yield from policies(value, label + "/" + str(j))


def prepare(cert):
    p = len(cert["terminal_counts"])
    m = sum(cert["terminal_counts"])
    actions = {tuple(a["history"]): a["action"] for a in cert["actions"]}
    if m < 2 or m > 5 or p > 8 or p < 2:
        return None
    expected = sum(p**i for i in range(m))
    if len(actions) != expected:
        return None
    terminal = {}

    def walk(h):
        if len(h) == m:
            out = tuple(h.count(a) for a in range(p))
        else:
            for a in range(p):
                walk(h + (a,))
            out = terminal[h + (actions[h],)]
        terminal[h] = out
        return out

    root = walk(())
    masks = np.arange(1, 1 << p, dtype=np.int64)
    member = np.array([[(mask >> a) & 1 for mask in masks]
                       for a in range(p)], dtype=np.int64)
    values = {}

    def payoff(q, a):
        key = q, a
        if key not in values:
            den = np.array(q, dtype=np.int64) @ member
            values[key] = np.divide(member[a], den,
                                    out=np.zeros(len(masks)), where=den > 0)
        return values[key]

    rows = []
    for h, a in actions.items():
        chosen = payoff(terminal[h], a)
        for b in range(p):
            if a != b:
                rows.append(payoff(terminal[h + (b,)], b) - chosen)
    a_ub = np.array(rows)
    coverage = ((np.array(root) @ member) > 0).astype(float)
    root_path = []
    h = ()
    while len(h) < m:
        root_path.append(actions[h])
        h = h + (actions[h],)
    return p, m, masks, member, actions, terminal, root, root_path, payoff, a_ub, coverage


def attack(label, cert, mode):
    data = prepare(cert)
    if data is None:
        return None
    p, m, masks, member, actions, terminal, root, path, payoff, a_ub, w = data
    best = {"max_violation": -math.inf}
    supports = list(itertools.combinations(range(p), min(m, p)))
    b_ub = np.zeros(len(a_ub))
    # Normalizing total customers avoids unbounded objectives on unused types.
    eq = np.ones((1, len(masks)))
    for support in supports:
        opt = (member[list(support)].sum(axis=0) > 0).astype(float)
        targets = []
        if mode == "individual":
            for a in sorted(set(path)):
                targets.append((str(a), opt - w - m * payoff(root, a)))
        else:
            if len(support) != m:
                continue
            query = np.zeros(len(masks))
            for i in range(m):
                for a in support:
                    query += payoff(terminal[tuple(path[:i]) + (a,)], a) / m
            targets.append(("uniform_real", opt - w - query))
        for which, target in targets:
            ans = linprog(-target, A_ub=a_ub, b_ub=b_ub,
                          A_eq=eq, b_eq=[1], bounds=(0, None), method="highs")
            if ans.success and -ans.fun > best["max_violation"] + 1e-12:
                best = {"max_violation": float(-ans.fun),
                        "comparison": support, "target": which,
                        "weights": {str(mask): float(v) for mask, v in zip(masks, ans.x)
                                    if v > 1e-9}}
    return {"source": label, "players": m, "topics": p,
            "histories": len(actions), "mode": mode, **best}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("individual", "uniform"), default="individual")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    reports = []
    for source in sorted(Path("evidence/certificates/customer_attraction").glob("*.json")):
        for label, cert in policies(json.loads(source.read_text()), str(source)):
            report = attack(label, cert, args.mode)
            if report:
                reports.append(report)
                print(json.dumps({k: v for k, v in report.items() if k != "weights"}), flush=True)
    args.output.write_text(json.dumps({"scope": "fixed complete policies only; numerical discovery",
                                      "reports": reports}, indent=2) + "\n")


if __name__ == "__main__":
    main()
