#!/usr/bin/env python3
"""Finite audit for the scoped ternary palette tensor obstruction.

This is not a solver for q on arbitrary trees.  It checks the algebraic G_k
bound, the local 2^k palette product bound, and exactly enumerates the small
ordinary tree-machine matrices used as sanity instances of OPT=2-q/d.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path


def gap(k: int) -> Fraction:
    return (Fraction(2) - Fraction(1, 3**k)) / (Fraction(2) - Fraction(2**k, 3**k))


def local_palette_bound(k: int) -> bool:
    # Enumerate all subsets of the ternary palette {0,1,2} of size <=2.
    palettes = [frozenset(c) for n in (0, 1, 2) for c in combinations(range(3), n)]
    for cs in product(palettes, repeat=k):
        tuples = {tuple(x) for x in product(*[sorted(c) for c in cs])}
        if len(tuples) > 2**k:
            return False
    return True


def tree_edges(colors_by_parent: list[list[int]]):
    # Root = (), three depth-1 children, then depth-2 leaves.
    edges = []
    for i, colors in enumerate(colors_by_parent):
        mid = (i,)
        edges.append(((), mid, None))
        for j, color in enumerate(colors):
            edges.append((mid, (i, j), color))
    return edges


def q_height_two(colors_by_parent: list[list[int]], d: int = 3) -> int:
    # Exact q for this height-two tree by enumerating r-child choices.
    best = 1
    for r in range(1, d + 1):
        for root_children in combinations(range(d), r):
            for choices in product(list(combinations(range(d), r)), repeat=r):
                leaves = []
                for i, selected in zip(root_children, choices):
                    leaves.extend(colors_by_parent[i][j] for j in selected)
                if len(set(leaves)) == len(leaves):
                    best = max(best, r)
    return best


def brute_opt(colors_by_parent: list[list[int]], d: int = 3) -> Fraction:
    # Each edge job is assigned to its parent (small time 1/d) or its true
    # lower endpoint (unit time).  Root pin is fixed on root.
    edges = tree_edges(colors_by_parent)
    best = Fraction(99)
    for lower_flags in product((False, True), repeat=len(edges)):
        loads: dict[object, Fraction] = {(): Fraction(1)}  # root pin
        for (parent, child, color), to_lower in zip(edges, lower_flags):
            if to_lower:
                endpoint = child if color is None else ("color", color)
                loads[endpoint] = loads.get(endpoint, Fraction(0)) + 1
            else:
                loads[parent] = loads.get(parent, Fraction(0)) + Fraction(1, d)
        best = min(best, max(loads.values()))
    return best


def main() -> None:
    gaps = [gap(k) for k in range(1, 31)]
    assert gaps[0] == Fraction(5, 4)
    assert all(gaps[i] > gaps[i + 1] for i in range(len(gaps) - 1))
    assert all(gap(k) <= Fraction(5, 4) for k in range(1, 31))
    assert all(2**k < 3**k - 1 for k in range(2, 31))
    assert all(local_palette_bound(k) for k in range(1, 5))

    instances = {
        "binary_palette_height2": [[0, 1, 0], [2, 3, 2], [4, 5, 4]],
        "monochrome_palette_height2": [[0, 0, 0], [1, 1, 1], [2, 2, 2]],
    }
    rows = []
    for name, colors in instances.items():
        q = q_height_two(colors)
        opt = brute_opt(colors)
        expected = Fraction(2) - Fraction(q, 3)
        assert opt == expected, (name, q, opt, expected)
        rows.append({
            "name": name,
            "d": 3,
            "height": 2,
            "q": q,
            "opt": str(opt),
            "expected_2_minus_q_over_d": str(expected),
            "all_bottom_parents_at_most_two_colors": all(len(set(c)) <= 2 for c in colors),
        })

    result = {
        "status": "pass",
        "scope": {
            "gap_k": "1..30",
            "local_palette_k": "1..4",
            "tree_matrix": "two explicit d=3, h=2 trees; all 2^9 edge assignments",
        },
        "G_values": {str(k): str(gap(k)) for k in range(1, 6)},
        "tree_instances": rows,
        "checks": [
            "G_1=5/4 and G_k strictly decreases through k=30",
            "G_k<=5/4 through k=30",
            "2^k < 3^k-1 for k>=2 through k=30",
            "all products of k palettes of size at most two have at most 2^k tuples for k<=4",
            "finite ordinary tree-machine enumeration matches OPT=2-q/d on both instances",
        ],
        "limitations": [
            "finite checks do not prove the all-height identity or any complexity theorem",
            "no arbitrary recoloring, non-aligned tensor, padding, or altered task interface is tested",
        ],
    }
    out = Path(__file__).with_name("audit.json")
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
