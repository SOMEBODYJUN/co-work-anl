"""Exploratory complete-policy-cone attack on OPT-W <= m u_i.

Uses every ordered SPE row of a fixed policy and every customer incidence type.
LP results alone are numerical evidence, never a universal theorem.
"""
from __future__ import annotations

import argparse
import gzip
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent


def cases():
    directory = ROOT / "evidence/certificates/customer_attraction"
    for path in sorted(directory.glob("*.json")):
        data = json.loads(path.read_text())
        if not isinstance(data, dict):
            continue
        strategy = data.get("strategy", data)
        if (isinstance(strategy, dict) and "actions" in strategy
                and isinstance(strategy["actions"], list)
                and all(isinstance(row,dict) and "history" in row and "action" in row for row in strategy["actions"])):
            yield path.stem, strategy["actions"]
    for filename in ("selected_security_cones.json", "new_policy_security_cones.json.gz"):
        path = directory / filename
        data = json.loads(gzip.decompress(path.read_bytes()) if path.suffix == ".gz" else path.read_text())
        for case in data["cases"]:
            yield filename.split(".")[0] + ":" + case["name"], case["policy"]


def build(actions):
    policy = {tuple(row["history"]): row["action"] for row in actions}
    m = 1 + max(map(len, policy))
    k = 1 + max(max(h, default=-1) for h in policy)
    k = max(k, 1 + max(policy.values()))
    assert len(policy) == sum(k**j for j in range(m))
    scale = math.lcm(*range(1, m + 1))
    masks = np.arange(1, 1 << k)
    membership = ((masks[:, None] >> np.arange(k)) & 1).astype(np.int16)
    terminal = {}

    def play(h):
        if h not in terminal:
            z = h
            while len(z) < m:
                z += (policy[z],)
            terminal[h] = z
        return terminal[h]

    payoff = {}

    def vector(z, a):
        key = (tuple(z.count(j) for j in range(k)), a)
        if key not in payoff:
            count = membership @ np.array(key[0])
            payoff[key] = np.where(membership[:, a], scale // np.maximum(count, 1), 0).astype(np.int16)
        return payoff[key]

    seen = set()
    rows = []
    for h, chosen in policy.items():
        base = vector(play(h), chosen)
        for a in range(k):
            if a == chosen:
                continue
            row = base - vector(play(h + (a,)), a)
            key = row.tobytes()
            if key not in seen and row.any():
                seen.add(key)
                rows.append(row)
    gamma = np.array(rows, dtype=np.int16)
    z = play(())
    covered = (membership @ np.array([z.count(j) for j in range(k)]) > 0).astype(np.int16)
    return m, k, scale, membership, gamma, z, covered, vector


def attack(name, actions, max_topics=8):
    if len(actions) > 50000:
        return {"case": name, "skipped": "more than 50000 nodes"}
    largest_topic = max(max(row["history"], default=-1) for row in actions)
    largest_topic = max(largest_topic, max(row["action"] for row in actions))
    if largest_topic + 1 > max_topics:
        return {"case": name, "skipped": f"topics {largest_topic+1}>{max_topics}"}
    m, k, scale, membership, gamma, z, covered, vector = build(actions)
    if k > max_topics:
        return {"case": name, "skipped": f"topics {k}>{max_topics}"}
    # Normalization by total clients makes a compact polytope even on unplayed types.
    result = {"case": name, "players": m, "topics": k, "rows": len(gamma), "path": z,
              "numerical_only": True, "tested": 0, "largest_defect": -1e100}
    early_actions = sorted(set(z[:max(0, m - 2)]))
    for support in itertools.combinations(range(k), min(m, k)):
        optimum = membership[:, support].any(axis=1).astype(np.int16)
        for a in early_actions:
            objective = (optimum - covered).astype(float) - m * vector(z, a) / scale
            lp = linprog(-objective, A_ub=-gamma.astype(float), b_ub=np.zeros(len(gamma)),
                         A_eq=np.ones((1, len(covered))), b_eq=[1.0], bounds=(0, None), method="highs")
            assert lp.success, lp.message
            defect = -float(lp.fun)
            result["tested"] += 1
            if defect > result["largest_defect"]:
                result.update(largest_defect=defect, largest_support=support, largest_action=a)
            if defect > 1e-8:
                weights = [Fraction(float(x)).limit_denominator(10**7) for x in lp.x]
                exact_slacks = [sum(Fraction(int(c))*w for c,w in zip(row, weights)) for row in gamma]
                exact_obj = sum((Fraction(int(optimum[j]-covered[j]))-Fraction(m*int(vector(z,a)[j]),scale))*w
                                for j,w in enumerate(weights))
                result.update(candidate_weights={str(j+1):str(w) for j,w in enumerate(weights) if w},
                              candidate_objective=str(exact_obj), exact_min_slack=str(min(exact_slacks,default=0)),
                              exact_feasible=min(exact_slacks,default=0)>=0 and exact_obj>0)
                return result
    return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--match", default="")
    parser.add_argument("--max-topics", type=int, default=8)
    parser.add_argument("--output", default="individual_defect_cone_scan.json")
    args=parser.parse_args()
    report=[]
    for name,actions in cases():
        if args.match not in name:
            continue
        r=attack(name,actions,args.max_topics)
        report.append(r)
        print(json.dumps(r,ensure_ascii=False),flush=True)
        (HERE/args.output).write_text(json.dumps(report,ensure_ascii=False,indent=2))
        if r.get("exact_feasible"):
            break


if __name__=="__main__":
    main()
