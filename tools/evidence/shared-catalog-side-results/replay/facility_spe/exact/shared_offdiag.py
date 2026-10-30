"""Exact shared-catalog SPE optimization without diagonal support enumeration.

Input uses ``weights`` and ``locations``. Optional ``U1`` and ``U2`` must be
provided together and describe the same nonempty set of sites; otherwise all
locations are permitted. All numbers are exact positive rationals.

Only distinct-site layouts call the local support enumerator. If their maximum
overlap is k, the solver uses O(N**2 * (n + k * 3**k)) rational operations, even
when a single site covers arbitrarily many customers. Its result is an exact
optimal factor and a compact attainment certificate. ``verify`` checks only
attainment, not the assertion of optimality.
"""

import argparse
import json
from fractions import Fraction as Q

from facility_spe.exact.bounded_overlap import (
    local,
    parse,
    ratio,
    serial,
    verify as verify_attainment,
    witness,
)
from facility_spe.exact.mitm import greedy_pair


def _parse_shared(instance):
    if not isinstance(instance, dict):
        raise ValueError("instance must be an object")
    if ("U1" in instance) != ("U2" in instance):
        raise ValueError("shared catalogs U1 and U2 must be provided together")
    normalized = dict(instance)
    if "U1" not in instance:
        locations = instance.get("locations")
        size = len(locations) if isinstance(locations, (list, tuple)) else 0
        normalized["U1"] = list(range(size))
        normalized["U2"] = list(range(size))
    weights, sites, u1, u2 = parse(normalized)
    if set(u1) != set(u2):
        raise ValueError("this solver requires identical facility catalogs")
    return normalized, weights, sites, u1


def _reflect(record):
    s, t = record["layout"]
    return {
        "layout": [t, s],
        "shared": list(record["shared"]),
        "prob_first": [1 - p for p in record["prob_first"]],
        "loads": list(reversed(record["loads"])),
    }


def _balanced(weights, sites, site):
    shared = sorted(sites[site])
    half = sum((weights[i] for i in shared), Q(0)) / 2
    return {
        "layout": [site, site],
        "shared": shared,
        "prob_first": [Q(1, 2)] * len(shared),
        "loads": [half, half],
    }


def solve(instance):
    """Return the exact optimum with balanced continuations on every diagonal.

    Let H(t) be the largest minimum deviator load over destinations distinct
    from t, and let R(t) be its reach. A balanced diagonal candidate has factor
    max(1, 2 H(t)/R(t)). Start with the best such candidate. An off-diagonal
    candidate can replace it only at a strictly smaller factor a. Then every
    H(t) > a R(t)/2, so diagonal minima are dominated by H(t), and balanced
    diagonal punishments are safe. This strict replacement rule also covers
    ties without needing any diagonal coordinate-extremum witness.
    """
    normalized, weights, sites, catalog = _parse_shared(instance)
    reach = {
        t: sum((weights[i] for i in sites[t]), Q(0)) for t in catalog
    }
    h = {t: Q(0) for t in catalog}
    pairs = {}
    punish = {}
    overlap = 0
    for index, s in enumerate(catalog):
        for t in catalog[index + 1 :]:
            rec = local(weights, sites, s, t)
            pairs[s, t] = rec
            overlap = max(overlap, len(rec["shared"]))
            lo = rec["min_piece"]
            hi = rec["max_piece"]
            punish[s, t] = witness(s, t, rec, lo, lo["lo"])
            punish[t, s] = _reflect(witness(s, t, rec, hi, hi["hi"]))
            h[t] = max(h[t], punish[s, t]["loads"][0])
            h[s] = max(h[s], punish[t, s]["loads"][0])

    diagonal = None
    for t in catalog:
        value = ratio(2 * h[t], reach[t])
        if value is None:
            continue
        alpha = max(Q(1), value)
        if diagonal is None or alpha < diagonal[0]:
            diagonal = alpha, t
    # A maximum-reach site gives a finite factor <= 2; all-zero reach gives 1.
    if diagonal is None:
        raise AssertionError("a shared-catalog balanced candidate must exist")
    best_alpha, site = diagonal
    on_path = _balanced(weights, sites, site)
    for (s, t), rec in pairs.items():
        den = h[t] + h[s]
        for piece in rec["pieces"]:
            target = rec["total"] * h[t] / den if den else piece["lo"]
            x = max(piece["lo"], min(piece["hi"], target))
            r1 = ratio(h[t], x)
            r2 = ratio(h[s], rec["total"] - x)
            if r1 is None or r2 is None:
                continue
            alpha = max(Q(1), r1, r2)
            # Preserve the balanced diagonal on ties. Strict improvement makes
            # all possible balanced diagonal deviation loads safe.
            if alpha < best_alpha:
                best_alpha = alpha
                on_path = witness(s, t, rec, piece, x)

    s, t = on_path["layout"]
    deviations = []
    for r in catalog:
        if r != s:
            rec = _balanced(weights, sites, t) if r == t else punish[r, t]
            deviations.append({"deviator": 1, "witness": rec})
    for r in catalog:
        if r != t:
            rec = _balanced(weights, sites, s) if r == s else _reflect(punish[r, s])
            deviations.append({"deviator": 2, "witness": rec})
    result = {
        "finite_factor_exists": True,
        "alpha": best_alpha,
        "distinct_overlap": overlap,
        "local_calls": len(pairs),
        "on_path": on_path,
        "deviations": deviations,
        "default_continuation": (
            "balanced on every co-located layout; on other unspecified layouts "
            "assign common customers in decreasing weight to the currently "
            "less loaded facility, breaking ties toward facility 1"
        ),
    }
    verify_attainment(normalized, result)
    return result


def verify(instance, result):
    """Verify a finite attainment certificate without enumerating supports."""
    normalized, _, _, _ = _parse_shared(instance)
    verify_attainment(normalized, result)


def continuation(instance, result, s, t):
    """Materialize a layout of the complete rule after verifying ``result``.

    The on-path and actual-deviation records override the deterministic
    defaults. Every unspecified diagonal is balanced, and the descending-weight
    assignment on an unspecified off-diagonal is a pure customer NE.
    """
    _, weights, sites, catalog = _parse_shared(instance)
    if type(s) is not int or type(t) is not int or s not in catalog or t not in catalog:
        raise ValueError("layout is outside the shared catalog")
    if tuple(result["on_path"]["layout"]) == (s, t):
        return result["on_path"]
    for rec in result["deviations"]:
        if tuple(rec["witness"]["layout"]) == (s, t):
            return rec["witness"]
    if s == t:
        return _balanced(weights, sites, s)
    shared = sorted(sites[s] & sites[t])
    a = sum((weights[i] for i in sites[s] - sites[t]), Q(0))
    b = sum((weights[i] for i in sites[t] - sites[s]), Q(0))
    ans = greedy_pair(a, b, [weights[i] for i in shared])
    return {
        "layout": [s, t],
        "shared": shared,
        "prob_first": ans["prob_first"],
        "loads": list(ans["loads"]),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input")
    parser.add_argument("--output")
    args = parser.parse_args()
    with open(args.input) as source:
        instance = json.load(source, parse_float=str)
    text = json.dumps(serial(solve(instance)), indent=2) + "\n"
    if args.output:
        with open(args.output, "w") as target:
            target.write(text)
    else:
        print(text, end="")
