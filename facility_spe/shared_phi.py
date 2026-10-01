#!/usr/bin/env python3
"""Polynomial exact-client-NE phi-SPE construction for a shared site catalog.

The algorithm minimizes over an explicit polynomial witness menu, never over
the entire Nash correspondence. See common_phi_algorithm.md for the proof
transfer and asym_research/common_phi_menu_quantifier_audit.md for its audit.
"""
from fractions import Fraction as Q
from itertools import combinations
import argparse
import json

from facility_spe.local.pure import guarded_repair, load_pair
from facility_spe.local.strong_chord import construct as strong_chord, qcmp


def exact_ne(a, b, weights, probabilities):
    """Check individual independent mixed Nash conditions, including endpoints."""
    p = tuple(map(Q, probabilities))
    if len(p) != len(weights) or not all(0 <= z <= 1 for z in p):
        raise ValueError("Invalid customer probability vector")
    x, y = load_pair(a, b, weights, p)
    for w, z in zip(weights, p):
        difference = x-y+w*(1-2*z)
        if (z != 0 and difference > 0) or (z != 1 and difference < 0):
            raise ValueError("Customer profile is not an exact Nash equilibrium")
    return x, y


def menu(a, b, weights):
    """Static menu at a pair with private loads a,b and common weights.

    Every pure repair has the guard and first-reversal stopping rule used in
    the proof. Unqualified seeds are discarded, never repaired unrestrictedly.
    """
    a, b = Q(a), Q(b)
    ws = tuple(map(Q, weights))
    k = len(ws)
    entries = {}

    def add(probabilities, family):
        p = tuple(map(Q, probabilities))
        loads = exact_ne(a, b, ws, p)
        if p not in entries:
            entries[p] = {"prob_first": list(p), "loads": list(loads),
                          "family": family}

    for side in (0, 1):
        seeds = [(side,)*k]
        for h in range(k):
            p = [1-side]*k
            p[h] = side
            seeds.append(tuple(p))
        for seed in seeds:
            repaired = guarded_repair(a, b, ws, seed)
            if repaired is not None:
                add(repaired, "guarded_pure")

    common = sum(ws, Q(0))
    first_reach, second_reach = a+common, b+common
    if a == b:
        add([Q(1, 2)]*k, "equal_reach_half")

    # Section 7: all other common customers are at the higher-reach site;
    # h and j mix toward the lower-reach site with signed contribution D.
    lower_sides = (0, 1) if a == b else ((0,) if a < b else (1,))
    for h, j in combinations(range(k), 2):
        other_mass = common-ws[h]-ws[j]
        for lower in lower_sides:
            difference = abs(a-b)+other_mass
            if difference > min(ws[h], ws[j]):
                continue
            p = [Q(lower)]*k  # when lower=0, the high site is second
            p[h] = (1+difference/ws[h])/2
            p[j] = (1+difference/ws[j])/2
            if lower == 1:
                p[h], p[j] = 1-p[h], 1-p[j]
            add(p, "two_designated_mixers")

    high, low = max(first_reach, second_reach), min(first_reach, second_reach)
    # The exact sufficient theorem regime. qcmp uses rational polynomial signs.
    if (low > 0 and qcmp(2*low/high-1) > 0
            and qcmp(common/low) < 0
            and (not ws or qcmp(1-max(ws)/high) >= 0)):
        output = strong_chord(high, low, ws)
        if output["probabilities"] is None:
            raise RuntimeError("Strong-chord constructor returned no witness")
        p = output["probabilities"]
        if first_reach < second_reach:
            p = [1-z for z in p]
        add(p, "strong_chord_"+output["branch"])
        # Label symmetry at equal reaches, including diagonal physical layouts.
        if a == b:
            add([1-z for z in p], "strong_chord_reflection")

    if not entries or not any(all(z in (0, 1) for z in p) for p in entries):
        raise RuntimeError("Static menu lacks a pure equilibrium")
    return list(entries.values())


def parsed(instance):
    if any(isinstance(value, float) for value in instance["weights"]):
        raise TypeError("Use exact decimal/rational strings or integers for weights")
    weights = [Q(str(value)) for value in instance["weights"]]
    if any(w <= 0 for w in weights):
        raise ValueError("All customer weights must be positive")
    sites = [set(site) for site in instance["locations"]]
    if not sites:
        raise ValueError("The shared catalog must be nonempty")
    if any(any(i < 0 or i >= len(weights) for i in site) for site in sites):
        raise ValueError("Invalid customer index")
    if "U1" in instance or "U2" in instance:
        u1 = instance.get("U1", list(range(len(sites))))
        u2 = instance.get("U2", list(range(len(sites))))
        if set(u1) != set(u2):
            raise ValueError("This theorem requires one shared action set")
        catalog = list(dict.fromkeys(u1))
    else:
        catalog = list(range(len(sites)))
    if not catalog or any(s < 0 or s >= len(sites) for s in catalog):
        raise ValueError("Invalid shared action set")
    return weights, sites, catalog


def witness(s, t, common, entry):
    return {"layout": [s, t], "common": common,
            "prob_first": entry["prob_first"], "loads": entry["loads"],
            "family": entry["family"]}


def solve(instance):
    weights, sites, catalog = parsed(instance)
    menus, commons = {}, {}
    for ix, s in enumerate(catalog):
        for t in catalog[ix:]:
            shared = sorted(sites[s] & sites[t])
            a = sum((weights[i] for i in sites[s]-sites[t]), Q(0))
            b = sum((weights[i] for i in sites[t]-sites[s]), Q(0))
            entries = menu(a, b, [weights[i] for i in shared])
            menus[s, t], commons[s, t] = entries, shared
            if s != t:
                menus[t, s] = [{"prob_first": [1-z for z in e["prob_first"]],
                                "loads": e["loads"][::-1], "family": e["family"]}
                               for e in entries]
                commons[t, s] = shared

    punishment = {pair: min(entries, key=lambda e: e["loads"][0])
                  for pair, entries in menus.items()}
    best_response = {t: max(catalog, key=lambda s: punishment[s, t]["loads"][0])
                     for t in catalog}
    threat = {t: punishment[best_response[t], t]["loads"][0] for t in catalog}
    node, path, seen = catalog[0], [], {}
    while node not in seen:
        seen[node] = len(path)
        path.append(node)
        node = best_response[node]
    cycle = path[seen[node]:]

    best = None
    # The cycle proves that a phi witness exists; scanning the full catalog
    # also finds better instance-specific factors without changing the bound.
    for s in catalog:
        for t in catalog:
            for entry in menus[s, t]:
                x, y = entry["loads"]
                if (x == 0 and threat[t]) or (y == 0 and threat[s]):
                    continue
                factor = max(Q(1), threat[t]/x if x else Q(0),
                             threat[s]/y if y else Q(0))
                if best is None or factor < best[0]:
                    best = factor, s, t, entry
    if best is None:
        raise RuntimeError("No feasible witness found on the response cycle")
    factor, s, t, on_path = best
    if factor*factor-factor-1 > 0:
        raise RuntimeError("Static phi-menu theorem failed")
    deviations = []
    for r in catalog:
        if r != s:
            deviations.append({"deviator": 1,
                "witness": witness(r, t, commons[r, t], punishment[r, t])})
        if r != t:
            e = punishment[r, s]
            reflected = {"prob_first": [1-z for z in e["prob_first"]],
                         "loads": e["loads"][::-1], "family": e["family"]}
            deviations.append({"deviator": 2,
                "witness": witness(s, r, commons[s, r], reflected)})
    certificate = {"guarantee": "phi=(1+sqrt(5))/2", "factor": factor,
        "on_path": witness(s, t, commons[s, t], on_path),
        "deviations": deviations, "response_cycle": cycle,
        "menu_threats": {str(s): threat[s] for s in catalog},
        "ordered_pair_count": len(menus),
        "ordered_menu_entry_count": sum(map(len, menus.values())),
        "default_continuation": "guarded_repair of all common customers at facility 1"}
    verify(instance, certificate)
    return certificate


def verify(instance, certificate):
    """Independent direct certificate check; no menus, minima, or proof oracle."""
    weights, sites, catalog = parsed(instance)
    factor = Q(str(certificate["factor"]))
    if factor < 1 or factor*factor-factor-1 > 0:
        raise ValueError("Claimed approximation factor exceeds phi")

    def check(record):
        s, t = record["layout"]
        if s not in catalog or t not in catalog:
            raise ValueError("Witness uses a site outside the shared catalog")
        common = sorted(sites[s] & sites[t])
        if common != record["common"]:
            raise ValueError("Witness has an incorrect common-customer list")
        a = sum((weights[i] for i in sites[s]-sites[t]), Q(0))
        b = sum((weights[i] for i in sites[t]-sites[s]), Q(0))
        result = exact_ne(a, b, [weights[i] for i in common],
                          [Q(str(p)) for p in record["prob_first"]])
        if list(result) != [Q(str(z)) for z in record["loads"]]:
            raise ValueError("Witness has incorrect facility loads")
        return result

    x, y = check(certificate["on_path"])
    s, t = certificate["on_path"]["layout"]
    expected = {(1, r, t) for r in catalog if r != s}
    expected |= {(2, s, r) for r in catalog if r != t}
    observed = set()
    for deviation in certificate["deviations"]:
        who = deviation["deviator"]
        if who not in (1, 2):
            raise ValueError("Invalid deviating facility label")
        record = deviation["witness"]
        a, b = check(record)
        observed.add((who, *record["layout"]))
        if (a if who == 1 else b) > factor*(x if who == 1 else y):
            raise ValueError("A facility deviation violates the factor")
    if observed != expected or len(observed) != len(certificate["deviations"]):
        raise ValueError("Missing or duplicated unilateral deviations")
    return True


def serial(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, dict):
        return {str(k): serial(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serial(v) for v in value]
    return value


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input")
    parser.add_argument("--output")
    args = parser.parse_args()
    with open(args.input) as stream:
        instance = json.load(stream, parse_float=str)
    rendered = json.dumps(serial(solve(instance)), indent=2)+"\n"
    if args.output:
        with open(args.output, "w") as stream:
            stream.write(rendered)
    else:
        print(rendered, end="")
