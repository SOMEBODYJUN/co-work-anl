"""Exact output-sensitive search compiler, NOT a general boxed-NE solver.

Source: player i excludes one site a_i in A_i and uses all other sites in A_i;
site t has background B_t and latency (B_t + selected weight)/q_t.
Target: an actual common-catalog facility instance on its canonical greedy layout.
Site/client indices are zero-based. Rational inputs must not be floats.
Runtime counts the explicitly output sum(q)+1 labeled facilities. With binary
unbounded speeds this need not be polynomial in compact source input length.
The bounded-complement import does not expand q. Default ties agree with the
repository's canonical greedy; reverse_ties is a diagnostic alternative rule.
"""
from __future__ import annotations
from fractions import Fraction as F
from typing import Any, Sequence

# Reuse exact numeric I/O only; no equal-weight optimizer is invoked.
from .equal_light_flow import _fraction_text, _rational


def rational(x: Any) -> F:
    return _rational(x)


def normalize(q, B, u, A):
    q, B, u = tuple(q), tuple(map(rational, B)), tuple(map(rational, u))
    if not q or len(B) != len(q) or len(A) != len(u):
        raise ValueError("Nonempty resource list and matching dimensions required.")
    if any(type(x) is not int or x < 1 for x in q):
        raise ValueError("Speeds must be positive integers.")
    if any(x < 0 for x in B) or any(x <= 0 for x in u):
        raise ValueError("Backgrounds must be nonnegative; weights positive.")
    rows = []
    for row in A:
        row = tuple(row)
        if not row or any(type(t) is not int or not 0 <= t < len(q) for t in row):
            raise ValueError("Invalid or empty allowed set.")
        rows.append(tuple(sorted(set(row))))
    return q, B, u, tuple(rows)


def canonical_greedy(weights, allowed, sites: int, k: int, *, reverse_ties=False):
    """Literal fixed-first-pool greedy; returns labeled insertion order and pools."""
    cover = [[] for _ in range(sites)]
    for i, row in enumerate(allowed):
        for t in row:
            cover[t].append(i)
    owner = [None] * len(weights)
    count, pool, layout, scores, opening = [0] * sites, [F(0)] * sites, [], [], []
    for _ in range(k):
        values = [pool[t] / (count[t] + 1) if count[t] else
                  sum((weights[i] for i in cover[t] if owner[i] is None), F(0))
                  for t in range(sites)]
        best = max(values)
        candidates = [t for t, value in enumerate(values) if value == best]
        t = candidates[-1] if reverse_ties else candidates[0]
        if not count[t]:
            opening.append(t)
            for i in cover[t]:
                if owner[i] is None:
                    owner[i] = t
                    pool[t] += weights[i]
        count[t] += 1
        layout.append(t)
        scores.append(best)
    return count, pool, owner, layout, scores, opening


def compile_game(q, B, u, A, eta="1/2", *, reverse_ties=False) -> dict:
    """Compile source data. All target assignments satisfy full box and strict H."""
    q, B, u, A = normalize(q, B, u, A)
    eta = rational(eta)
    if not 0 < eta <= F(1, 2):
        raise ValueError("eta must lie in (0,1/2].")
    m, n, Q = len(q), len(u), max(q)
    M = max(B) + sum(u, F(0)) + 1
    delta = eta / (Q * M)
    eligible = [F(0)] * m
    for i, row in enumerate(A):
        for t in row:
            eligible[t] += u[i]
    private = [q[t] + delta * (q[t] * M - B[t] - eligible[t]) for t in range(m)]
    weights = [delta * x for x in u] + private + [F(1)]
    allowed = list(A) + [(t,) for t in range(m)] + [(m,)]
    k = sum(q) + 1
    count, pool, owner, layout, scores, opening = canonical_greedy(
        weights, allowed, m + 1, k, reverse_ties=reverse_ties)
    if count != list(q) + [1] or layout[-1] != m or scores[-1] != 1:
        raise AssertionError("Greedy multiplicity/last-score certificate failed.")
    if any(score <= 1 for score in scores[:-1]):
        raise AssertionError("A premature score at or below one occurred.")
    if any(not q[t] < pool[t] < q[t] + 1 for t in range(m)):
        raise AssertionError("First-opening pool certificate failed.")
    rank = {old: new for new, old in enumerate(opening)}
    aq = [count[t] for t in opening]
    ac = [pool[t] - count[t] for t in opening]
    aA = [sorted(rank[t] for t in row) for row in A]
    if any(aq[t] < aq[t + 1] for t in range(m)):
        raise AssertionError("First-opening order is not nonincreasing in q.")
    if any(rank[owner[i]] != min(aA[i]) for i in range(n)):
        raise AssertionError("Home-order certificate failed.")
    return {
        "kind": "search reduction; not a general NE solver",
        "source": {"q": list(q), "B": list(map(_fraction_text, B)),
                   "u": list(map(_fraction_text, u)), "A": [list(x) for x in A]},
        "eta": _fraction_text(eta), "M": _fraction_text(M), "delta": _fraction_text(delta),
        "target": {"k": k, "site_count": m + 1,
                   "weights": list(map(_fraction_text, weights)), "A": [list(x) for x in allowed]},
        "greedy": {"layout": layout, "multiplicities": count,
                   "pools": list(map(_fraction_text, pool)), "owners": owner,
                   "insertion_scores": list(map(_fraction_text, scores)), "gamma": "1"},
        "abstract": {"q": aq, "c": list(map(_fraction_text, ac)),
                     "w": list(map(_fraction_text, weights[:n])), "A": aA},
        "abstract_to_source_site": opening,
    }


def decode_ne(compiled: dict, abstract_assignment: Sequence[int]) -> list[int]:
    """Verify an oracle's station-pure output; return the source exclusions.

    The oracle is NOT provided by this module. No exponential fallback is used.
    For a two-choice source scheduling game, the selected machine is the other
    allowed site, not the returned exclusion.
    """
    source, target = compiled["source"], compiled["target"]
    q, B, u, A = normalize(**source)
    n, m = len(u), len(q)
    mapping = compiled["abstract_to_source_site"]
    if len(abstract_assignment) != n:
        raise ValueError("Oracle returned the wrong number of mobile clients.")
    a = []
    for i, v in enumerate(abstract_assignment):
        if type(v) is not int or not 0 <= v < len(mapping) or mapping[v] not in A[i]:
            raise ValueError("Oracle returned an illegal assignment.")
        a.append(mapping[v])
    weights = list(map(rational, target["weights"]))
    W = weights[n:n + m].copy()
    Y = list(B)
    for i, s in enumerate(a):
        W[s] += weights[i]
        for t in A[i]:
            if t != s:
                Y[t] += u[i]
    for t in range(m):
        if not q[t] <= W[t] <= q[t] + 1:
            raise ValueError("Oracle output fails the full box.")
    for i, s in enumerate(a):
        external = (W[s] - weights[i]) / q[s]
        for t in A[i]:
            if external > W[t] / q[t]:
                raise ValueError("Oracle output is not a target exact NE.")
            if t != s and (Y[s] + u[i]) / q[s] < Y[t] / q[t]:
                raise AssertionError("Source NE correspondence failed.")
    return a


def to_bounded_complement(q, c, w, A) -> dict:
    """General abstract F -> nonnegative co-singleton loads with exact bands.

    This is an import interface, not a solver: an oracle must return an NE
    satisfying the reported load bands, not just an arbitrary unbounded NE.
    At least one site is required. An empty customer list is allowed.
    """
    q, _, w, A = normalize(q, [0] * len(q), w, A)
    c = tuple(map(rational, c))
    if len(c) != len(q) or any(not 0 <= x <= 1 for x in c):
        raise ValueError("c must have one entry in [0,1] per site.")
    if any(q[t] < q[t + 1] for t in range(len(q) - 1)):
        raise ValueError("Abstract q must be nonincreasing.")
    if any(x >= 1 for x in w):
        raise ValueError("Abstract movable weights must be below one.")
    h, b, eligible = [row[0] for row in A], list(c), [F(0)] * len(q)
    for i, row in enumerate(A):
        b[h[i]] -= w[i]
        for t in row:
            eligible[t] += w[i]
    M = 1 + max((b[t] + eligible[t]) / q[t] for t in range(len(q)))
    B = [q[t] * M - b[t] - eligible[t] for t in range(len(q))]
    assert all(B[t] >= q[t] for t in range(len(q)))
    return {
        "kind": "bounded co-singleton import interface; not an NE solver",
        "source": {"q": list(q), "B": list(map(_fraction_text, B)),
                   "u": list(map(_fraction_text, w)), "A": [list(row) for row in A]},
        "M": _fraction_text(M), "initial_exclusions": h,
        "lower_load": [_fraction_text(qt * M - 1) for qt in q],
        "upper_load": [_fraction_text(qt * M) for qt in q],
    }


def as_facility_instance(compiled: dict):
    """Return the actual target in the existing canonical MF-MODEL API.

    No equilibrium is computed. compiled must be the output of compile_game.
    """
    from .two_exists import Instance
    target = compiled["target"]
    return Instance(tuple(map(rational, target["weights"])),
                    tuple(frozenset(row) for row in target["A"]),
                    target["site_count"], target["k"])


def main():
    import argparse
    import json
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Refusing to overwrite an existing output; choose a new path")
    try:
        data = json.loads(args.source.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("Source input must be a JSON object")
        result = compile_game(**data)
    except (ValueError, TypeError, KeyError, ZeroDivisionError) as exc:
        parser.error(str(exc))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n",
                           encoding="utf-8")
    print("Search interface written; no equilibrium solver was invoked.")


if __name__ == "__main__":
    main()
