#!/usr/bin/env python3
"""Exact optimum for two catalogs with at most one shared client per cross pair.

Input JSON: {weights: [...], locations: [[client indices],...], U1:[site indices],
             U2:[site indices]}.
All numbers are interpreted as exact rationals; decimal strings are allowed.
"""
from fractions import Fraction as Q
import argparse
import json


def ratio(v, z):
    if not v:
        return Q(0)
    return v / z if z else None


def local(weights, sites, s, t):
    common = sorted(sites[s] & sites[t])
    if len(common) > 1:
        raise ValueError(f"cross pair {(s,t)} has {len(common)} shared customers")
    a = sum((weights[i] for i in sites[s] - sites[t]), Q(0))
    b = sum((weights[i] for i in sites[t] - sites[s]), Q(0))
    w = weights[common[0]] if common else Q(0)
    total = a + b + w
    if not common:
        lo = hi = a
    elif a < b:
        lo = hi = a + w
    elif a > b:
        lo = hi = a
    else:
        lo, hi = a, a + w
    return {"A": a, "B": b, "w": w, "common": common,
            "V": total, "lo": lo, "hi": hi}


def witness(s, t, data, first):
    p = [] if not data["common"] else [(first - data["A"]) / data["w"]]
    return {"layout": [s,t], "common": data["common"], "prob_first": p,
            "loads": [first, data["V"] - first]}


def solve(instance):
    weights = [Q(str(v)) for v in instance["weights"]]
    if any(v <= 0 for v in weights):
        raise ValueError("weights must be positive")
    sites = [set(v) for v in instance["locations"]]
    u1, u2 = list(dict.fromkeys(instance["U1"])), list(dict.fromkeys(instance["U2"]))
    if not u1 or not u2:
        raise ValueError("both catalogs must be nonempty")
    data = {(s,t):local(weights,sites,s,t) for s in u1 for t in u2}
    d1 = {t:max(data[s,t]["lo"] for s in u1) for t in u2}
    d2 = {s:max(data[s,t]["V"]-data[s,t]["hi"] for t in u2) for s in u1}
    best = None
    for (s,t), rec in data.items():
        denom = d1[t] + d2[s]
        target = rec["V"] * d1[t]/denom if denom else rec["lo"]
        first = min(rec["hi"],max(rec["lo"],target))
        r1,r2 = ratio(d1[t],first),ratio(d2[s],rec["V"]-first)
        if r1 is None or r2 is None:
            continue
        alpha = max(Q(1),r1,r2)
        if best is None or alpha < best[0]:
            best = alpha,s,t,first
    if best is None:
        return {"finite_factor_exists": False}
    alpha,s,t,first = best
    off = []
    for r in u1:
        if r != s:
            off.append({"deviator":1,"witness":witness(r,t,data[r,t],data[r,t]["lo"])})
    for r in u2:
        if r != t:
            off.append({"deviator":2,"witness":witness(s,r,data[s,r],data[s,r]["hi"])})
    result = {"finite_factor_exists":True,"alpha":alpha,
              "on_path":witness(s,t,data[s,t],first),"deviations":off,
              "default_continuation":"apply the one-shared-customer formulas at the requested legal pair"}
    verify(instance,result)
    return result


def verify(instance,result):
    """Verify attainment directly; optimality is supplied by solve's formulas."""
    if not result["finite_factor_exists"]:
        return
    weights = [Q(str(v)) for v in instance["weights"]]
    sites = [set(v) for v in instance["locations"]]
    def check(rec):
        s,t = rec["layout"]
        common = sorted(sites[s]&sites[t])
        assert common == rec["common"]
        assert len(common) == len(rec["prob_first"])
        x = sum((weights[i] for i in sites[s]-sites[t]),Q(0))
        y = sum((weights[i] for i in sites[t]-sites[s]),Q(0))
        for i,p in zip(common,rec["prob_first"]):
            assert 0 <= p <= 1
            x += weights[i]*p
            y += weights[i]*(1-p)
        assert [x,y] == rec["loads"]
        for i,p in zip(common,rec["prob_first"]):
            diff = x-y+weights[i]*(1-2*p)
            assert (p == 0 or diff <= 0) and (p == 1 or diff >= 0)
        return x,y
    x,y = check(result["on_path"])
    s,t = result["on_path"]["layout"]
    expected = {(1,r,t) for r in instance["U1"] if r != s}
    expected |= {(2,s,r) for r in instance["U2"] if r != t}
    observed = set()
    for rec in result["deviations"]:
        a,b = check(rec["witness"])
        ds,dt = rec["witness"]["layout"]
        observed.add((rec["deviator"],ds,dt))
        assert (a if rec["deviator"] == 1 else b) <= result["alpha"]*(x if rec["deviator"] == 1 else y)
    assert observed == expected


def serial(value):
    if isinstance(value,Q):
        return str(value)
    if isinstance(value,list):
        return [serial(v) for v in value]
    if isinstance(value,dict):
        return {k:serial(v) for k,v in value.items()}
    return value


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    args = parser.parse_args()
    with open(args.input) as f:
        instance = json.load(f)
    print(json.dumps(serial(solve(instance)),ensure_ascii=False,indent=2))
