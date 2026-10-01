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


def _rational(value, name):
    if type(value) not in (int, str, Q):
        raise ValueError(f"{name} must be an exact rational, not a bool or float")
    try:
        return Q(str(value))
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        raise ValueError(f"{name} must be a rational number") from exc


def _sequence(value, name):
    if not isinstance(value, (list, tuple)):
        raise ValueError(f"{name} must be a sequence")
    return value


def _indices(value, limit, name):
    items = _sequence(value, name)
    if any(type(i) is not int or not 0 <= i < limit for i in items):
        raise ValueError(f"{name} contains an invalid integer index")
    return items


def parse(instance):
    """Validate the full input, including pairs absent from a certificate."""
    try:
        weights = [_rational(v, "weight") for v in
                   _sequence(instance["weights"], "weights")]
        if any(v <= 0 for v in weights):
            raise ValueError("weights must be positive")
        sites = [set(_indices(v, len(weights), "location")) for v in
                 _sequence(instance["locations"], "locations")]
        u1 = list(dict.fromkeys(_indices(instance["U1"], len(sites), "U1")))
        u2 = list(dict.fromkeys(_indices(instance["U2"], len(sites), "U2")))
        if not u1 or not u2:
            raise ValueError("both catalogs must be nonempty")
        for s in u1:
            for t in u2:
                if len(sites[s] & sites[t]) > 1:
                    raise ValueError(f"cross pair {(s,t)} has more than one shared customer")
        return weights, sites, u1, u2
    except (KeyError, TypeError) as exc:
        raise ValueError("malformed instance") from exc


def solve(instance):
    weights, sites, u1, u2 = parse(instance)
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
    """Verify a finite attainment certificate, without trusting solver metadata."""
    weights, sites, u1, u2 = parse(instance)
    try:
        if result["finite_factor_exists"] is not True:
            raise ValueError("a finite attainment certificate is required")
        alpha = _rational(result["alpha"], "alpha")
        if alpha < 1:
            raise ValueError("alpha must be at least one")

        def check(rec):
            layout = _indices(rec["layout"], len(sites), "layout")
            if len(layout) != 2:
                raise ValueError("layout must contain two site indices")
            s, t = layout
            if s not in u1 or t not in u2:
                raise ValueError("witness layout is outside the allowed catalogs")
            common = sorted(sites[s] & sites[t])
            recorded = _indices(rec["common"], len(weights), "common")
            if common != list(recorded):
                raise ValueError("incorrect common-customer list")
            probs = [_rational(p, "probability") for p in
                     _sequence(rec["prob_first"], "prob_first")]
            if len(common) != len(probs) or any(not 0 <= p <= 1 for p in probs):
                raise ValueError("invalid customer probabilities")
            x = sum((weights[i] for i in sites[s]-sites[t]), Q(0))
            y = sum((weights[i] for i in sites[t]-sites[s]), Q(0))
            for i, p in zip(common, probs):
                x += weights[i]*p
                y += weights[i]*(1-p)
            loads = [_rational(v, "load") for v in _sequence(rec["loads"], "loads")]
            if [x,y] != loads:
                raise ValueError("incorrect facility loads")
            for i, p in zip(common, probs):
                diff = x-y+weights[i]*(1-2*p)
                if not ((p == 0 or diff <= 0) and (p == 1 or diff >= 0)):
                    raise ValueError("customer assignment is not a Nash equilibrium")
            return x, y

        x, y = check(result["on_path"])
        s, t = result["on_path"]["layout"]
        expected = {(1,r,t) for r in u1 if r != s}
        expected |= {(2,s,r) for r in u2 if r != t}
        observed = set()
        for rec in _sequence(result["deviations"], "deviations"):
            who = rec["deviator"]
            if type(who) is not int or who not in (1,2):
                raise ValueError("invalid deviating facility")
            a, b = check(rec["witness"])
            ds, dt = rec["witness"]["layout"]
            key = (who, ds, dt)
            if key not in expected or key in observed:
                raise ValueError("illegal or duplicated unilateral deviation")
            observed.add(key)
            if (a if who == 1 else b) > alpha*(x if who == 1 else y):
                raise ValueError("facility deviation violates the claimed factor")
        if observed != expected:
            raise ValueError("missing unilateral deviations")
    except (KeyError, TypeError, IndexError) as exc:
        raise ValueError("malformed certificate") from exc


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
        instance = json.load(f, parse_float=str)
    print(json.dumps(serial(solve(instance)),ensure_ascii=False,indent=2))
