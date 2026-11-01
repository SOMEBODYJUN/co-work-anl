#!/usr/bin/env python3
"""Exact, package-independent regression for the clique alignment proof.

Finite checks do not prove the unrestricted theorem in the accompanying note.
"""
import argparse
import itertools
import json
from fractions import Fraction as F
from math import comb


def chi(q, ks):
    t, s = divmod(sum(ks), q)
    return q * comb(t, 2) + s * t - sum(
        max(0, a + b - q) for a, b in itertools.combinations(ks, 2)
    )


def loss(q, masks):
    ks = tuple(x.bit_count() for x in masks)
    return sum(
        (a & b).bit_count() - max(0, ka + kb - q)
        for (a, ka), (b, kb) in itertools.combinations(zip(masks, ks), 2)
    )


def balanced_masks(q, ks):
    p = 0
    masks = []
    for k in ks:
        masks.append(sum(1 << (j % q) for j in range(p, p + k)))
        p += k
    return masks


def enumerate_cliques(q, length):
    best = {}
    assignments = 0
    for masks in itertools.product(range(1 << q), repeat=length):
        ks = tuple(x.bit_count() for x in masks)
        value = loss(q, masks)
        assert value >= chi(q, ks) >= 0
        best[ks] = min(best.get(ks, value), value)
        assignments += 1
    for ks, value in best.items():
        assert value == chi(q, ks)
        target = balanced_masks(q, ks)
        assert tuple(x.bit_count() for x in target) == ks
        assert loss(q, target) == value
        degrees = [sum((x >> i) & 1 for x in target) for i in range(q)]
        assert max(degrees) - min(degrees) <= 1
    return {"q": q, "families": length, "assignments": assignments,
            "cardinality_profiles": len(best)}


def literal_comparisons():
    # Derive each edge from literal q(q-1) queries rather than importing rows.
    checked = 0
    for q in range(1, 5):
        for b in range(5):
            a, g = F(1, b + 1), F(1, (b + 1) * (b + 2))
            for zmask, fmask, ymask in itertools.product(range(1 << q), repeat=3):
                zs = [(zmask >> i) & 1 for i in range(q)]
                fs = [(fmask >> i) & 1 for i in range(q)]
                ys = [(ymask >> i) & 1 for i in range(q)]
                A = sum(F(fs[i], b + zs[i] + 1) for i in range(q))
                k, l = sum(zs), sum(ys)
                c = sum(x * y for x, y in zip(zs, ys))
                direct_d = sum(F(fs[i] - ys[i], b + zs[i] + 1)
                               for i in range(q))
                direct_o = sum(F(fs[i] - ys[j], b + zs[i] + 1)
                               for i in range(q) for j in range(q) if i != j)
                row_d = A - a * l + g * c
                row_o = (q - 1) * A - (q - 1) * a * l + g * (k * l - c)
                assert direct_d == row_d
                assert direct_o == row_o
                envelope_d = A - a * l + g * min(k, l)
                envelope_o = ((q - 1) * A - (q - 1) * a * l
                              + g * (k * l - max(0, k + l - q)))
                assert envelope_d - row_d == g * (min(k, l) - c)
                assert envelope_o - row_o == g * (c - max(0, k + l - q))
                checked += 1
    return checked


def weighted_and_type_representation():
    checked = 0
    q, length = 3, 4
    edges = list(itertools.combinations(range(length), 2))
    # Use distinct b and fixed edge lambda, including zero weights.
    for count, masks in enumerate(itertools.product(range(1 << q), repeat=length)):
        ks = tuple(x.bit_count() for x in masks)
        columns = {}
        for i in range(q):
            family_mask = sum(((masks[r] >> i) & 1) << r for r in range(length))
            columns[family_mask] = columns.get(family_mask, 0) + 1
        assert sum(columns.values()) == q
        for r in range(length):
            assert sum(n for mask, n in columns.items() if (mask >> r) & 1) == ks[r]
        for seed in range(3):
            weighted_loss = F(0)
            weights = []
            graph_loss = F(0)
            represented_graph_loss = F(0)
            for index, (r, s) in enumerate(edges):
                src = r if (index + seed) % 2 else s
                b = (count + 2 * src + seed) % 5
                lam = F((index + seed) % 4, (index % 3) + 1)
                w = lam / ((b + 1) * (b + 2))
                c = (masks[r] & masks[s]).bit_count()
                ell = max(0, ks[r] + ks[s] - q)
                weights.append(w)
                weighted_loss += w * (c - ell)
                c_from_columns = sum(n for mask, n in columns.items()
                                     if (mask >> r) & 1 and (mask >> s) & 1)
                assert c_from_columns == c
                if (index + seed) % 2:
                    graph_loss += w * (c - ell)
                    represented_graph_loss += w * (c_from_columns - ell)
                else:
                    graph_loss += w * (min(ks[r], ks[s]) - c)
                    represented_graph_loss += w * (min(ks[r], ks[s]) - c_from_columns)
                # Vertex complementation switches D and O deficiencies.
                complement = ((1 << q) - 1) ^ masks[s]
                new_c = (masks[r] & complement).bit_count()
                new_ell = max(0, ks[r] + q - ks[s] - q)
                assert min(ks[r], ks[s]) - c == new_c - new_ell
            assert weighted_loss >= min(weights) * chi(q, ks)
            assert graph_loss == represented_graph_loss
            checked += 1
    return checked


def simple_cycles(length):
    for size in range(3, length + 1):
        for vertices in itertools.combinations(range(length), size):
            first, rest = vertices[0], vertices[1:]
            for tail in itertools.permutations(rest):
                if tail[0] < tail[-1]:
                    yield (first,) + tail


def k5_separation():
    q, length = 2, 5
    assert chi(q, (1,) * length) == 4
    exact = min(loss(q, masks) for masks in itertools.product((1, 2), repeat=length))
    assert exact == 4
    cycles = list(simple_cycles(length))
    odd = [cycle for cycle in cycles if len(cycle) % 2]
    triangles = [cycle for cycle in cycles if len(cycle) == 3]
    assert len(cycles) == 37 and len(odd) == 22 and len(triangles) == 10
    for r, s in itertools.combinations(range(length), 2):
        assert sum(r in c and s in c for c in triangles) == 3
    packed_deficiency = len(triangles) * F(1, 3)
    assert packed_deficiency == F(10, 3) < 4
    # Nonnegative local histogram mixture from note section 4.
    A = F(2, 3) * F(1, 2) + F(1, 3) * 1
    edge_envelope = A - F(1, 2)
    assert edge_envelope == F(1, 6)
    weighted_cycle_checks = 0
    for cycle in cycles:
        for seed in range(6):
            weights = [F((seed + i) % 5, 1 + i % 3) for i in range(len(cycle))]
            value = sum(weights) * edge_envelope
            if len(cycle) % 2:
                value -= min(weights) * F(1, 2)
            assert value >= 0
            weighted_cycle_checks += 1
    clique_value = 10 * edge_envelope - F(1, 2) * 4
    assert clique_value == F(-1, 3)
    return {"exact_unweighted_deficiency": exact,
            "optimal_cycle_packing": str(packed_deficiency),
            "all_simple_cycles": len(cycles),
            "weighted_cycle_checks": weighted_cycle_checks,
            "local_histogram_edge_envelope": str(edge_envelope),
            "clique_separation_value": str(clique_value)}


def all_proper_subgraph_separation():
    results = []
    for q in range(2, 9):
        length = q + 1
        assert chi(q, (1,) * length) == 1
        edges = list(itertools.combinations(range(length), 2))
        for missing in edges:
            colors = {}
            colors[missing[0]] = colors[missing[1]] = 0
            for color, r in enumerate((r for r in range(length) if r not in missing), 1):
                colors[r] = color
            assert max(colors.values()) < q
            for edge in edges:
                assert (colors[edge[0]] == colors[edge[1]]) == (edge == missing)
        A = F(1, q - 1) * F(1, 2) + F(q - 2, q - 1)
        E = (q - 1) * A - (q - 1) + F(1, 2)
        assert E == 0
        results.append({"q": q, "families": length, "full_graph_deficiency": 1,
                        "each_deleted_edge_checked": len(edges),
                        "local_histogram_E": str(E), "clique_value": "-1/2"})
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args()
    result = {
        "status": "finite_exact_regression_passed",
        "scope": "Formula regression; unrestricted claims rely on accompanying proof.",
        "literal_BR_comparisons": literal_comparisons(),
        "clique_exhaustions": [enumerate_cliques(*p) for p in [(1, 6), (2, 7), (3, 5), (4, 4)]],
        "weighted_graph_and_type_checks": weighted_and_type_representation(),
        "K5": k5_separation(),
        "q_plus_one_irreducible_family": all_proper_subgraph_separation(),
    }
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        with open(args.output, "x", encoding="utf-8") as f:
            f.write(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
