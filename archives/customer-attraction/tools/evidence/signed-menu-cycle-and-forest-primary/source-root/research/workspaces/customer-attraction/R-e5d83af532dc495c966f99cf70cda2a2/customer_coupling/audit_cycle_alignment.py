#!/usr/bin/env python3
"""Exact self-contained checks for the arbitrary-menu cycle alignment budget.

No canonical game solver or optimizer is imported. Finite checks validate the
implementation and constructions; the note's symbolic proof bears all sizes.
"""
from fractions import Fraction as F
from itertools import product, permutations
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def kapp(q, ks, signs):
    if sum(signs) % 2 == 0:
        return 0
    loss = sum(abs(q - ks[r] - ks[(r + 1) % len(ks)]) if signs[r]
               else abs(ks[r] - ks[(r + 1) % len(ks)])
               for r in range(len(ks)))
    assert (q - loss) % 2 == 0
    return max(0, (q - loss) // 2)


def deficits(q, masks, signs):
    ks = tuple(a.bit_count() for a in masks)
    out = []
    for r, sign in enumerate(signs):
        s = (r + 1) % len(masks)
        h = (masks[r] ^ masks[s]).bit_count()
        if sign:
            val = q - h - abs(q - ks[r] - ks[s])
        else:
            val = h - abs(ks[r] - ks[s])
        assert val >= 0 and val % 2 == 0
        out.append(val // 2)
    return tuple(out)


def construct(q, ks, signs, debt_edge):
    """Attain all required debt at debt_edge (odd signs), or zero (even)."""
    ell = len(ks)
    order = [(debt_edge + 1 + j) % ell for j in range(ell)]
    flip = {order[0]: 0}
    for u, v in zip(order, order[1:]):
        assert v == (u + 1) % ell
        flip[v] = flip[u] ^ signs[u]
    transformed = [q - ks[r] if flip[r] else ks[r] for r in order]
    full = (1 << q) - 1
    transformed_masks = []
    if sum(signs) % 2 == 0:
        transformed_masks = [(1 << k) - 1 for k in transformed]
    else:
        anchor = (1 << transformed[0]) - 1
        current = anchor
        transformed_masks.append(current)
        for k in transformed[1:]:
            old = current.bit_count()
            if k > old:
                preferred = [i for i in range(q)
                             if not current >> i & 1 and not anchor >> i & 1]
                preferred += [i for i in range(q)
                              if not current >> i & 1 and anchor >> i & 1]
                for i in preferred[:k - old]:
                    current |= 1 << i
            elif k < old:
                preferred = [i for i in range(q)
                             if current >> i & 1 and anchor >> i & 1]
                preferred += [i for i in range(q)
                              if current >> i & 1 and not anchor >> i & 1]
                for i in preferred[:old - k]:
                    current &= ~(1 << i)
            assert current.bit_count() == k
            transformed_masks.append(current)
    out = [None] * ell
    for r, mask in zip(order, transformed_masks):
        out[r] = full ^ mask if flip[r] else mask
    assert tuple(x.bit_count() for x in out) == tuple(ks)
    ds = deficits(q, out, signs)
    target = kapp(q, ks, signs)
    assert all(d == (target if r == debt_edge else 0)
               for r, d in enumerate(ds)), (q, ks, signs, debt_edge, ds, target)
    return tuple(out)


def audit_br_rows():
    checks = 0
    for q in range(1, 5):
        for src, tgt, actual in product(range(1 << q), repeat=3):
            zs = [(src >> i) & 1 for i in range(q)]
            zt = [(tgt >> i) & 1 for i in range(q)]
            fs = [(actual >> i) & 1 for i in range(q)]
            kr, ks = sum(zs), sum(zt)
            c = sum(a * b for a, b in zip(zs, zt))
            for b in (0, 2, 7):
                a, g = F(1, b + 1), F(1, (b + 1) * (b + 2))
                aval = sum(F(f, b + z + 1) for f, z in zip(fs, zs))
                diagonal = sum(F(fs[i] - zt[i], b + zs[i] + 1)
                               for i in range(q))
                offdiag = sum(F(fs[i] - zt[j], b + zs[i] + 1)
                              for i in range(q) for j in range(q) if i != j)
                assert diagonal == aval - a * ks + g * c
                assert offdiag == (q - 1) * aval - (q - 1) * a * ks + g * (kr * ks - c)
                checks += 2
    return checks


def audit_unrestricted_masks():
    coefficient_checks = optimum_checks = 0
    # Complete mask universes for each displayed q,L; no frozen type support.
    for q, ell in [(1, 3), (2, 3), (3, 3), (4, 3), (1, 4), (2, 4), (3, 4)]:
        tuples = list(product(range(1 << q), repeat=ell))
        weight_patterns = [tuple(1 for _ in range(ell)),
                           tuple(1 + (3 * r + 1) % 7 for r in range(ell)),
                           tuple(0 if r == 1 else r + 2 for r in range(ell))]
        for signs in product((0, 1), repeat=ell):
            minima = [dict() for _ in weight_patterns]
            for masks in tuples:
                ks = tuple(a.bit_count() for a in masks)
                ds = deficits(q, masks, signs)
                target = kapp(q, ks, signs)
                for t, weights in enumerate(weight_patterns):
                    cost = sum(w * d for w, d in zip(weights, ds))
                    bound = min(weights) * target
                    assert cost >= bound
                    coefficient_checks += 1
                    minima[t][ks] = min(minima[t].get(ks, cost), cost)
            for t, weights in enumerate(weight_patterns):
                for ks, cost in minima[t].items():
                    assert cost == min(weights) * kapp(q, ks, signs)
                    optimum_checks += 1
    return coefficient_checks, optimum_checks


def audit_construction():
    checks = 0
    for q, ell in [(q, 3) for q in range(1, 8)] + [(3, 4), (2, 5)]:
        for ks in product(range(q + 1), repeat=ell):
            for signs in product((0, 1), repeat=ell):
                for edge in range(ell):
                    construct(q, ks, signs, edge)
                    checks += 1
    return checks


def audit_forest():
    checks = 0
    for q, labels in [(3, (0, 0, 0)), (4, (0, 0, 1, 1))]:
        ps = [p for p in permutations(range(q))
              if all(labels[i] == labels[p[i]] for i in range(q))]
        root = tuple(range(q))
        for edges in [((0, 1), (1, 2), (2, 3)),
                      ((0, 1), (0, 2), (0, 3))]:
            costs = {e: [[((13 * a + 7 * b + 5 * e[0] + 3 * e[1]) % 17) - 8
                          for b in range(q)] for a in range(q)] for e in edges}
            independent = sum(max(sum(costs[e][i][p[i]] for i in range(q)) for p in ps)
                              for e in edges)
            joint = max(sum(sum(costs[e][perms[e[0]][i]][perms[e[1]][i]]
                                for i in range(q)) for e in edges)
                        for tail in product(ps, repeat=3)
                        for perms in [(root,) + tail])
            assert joint == independent
            checks += 1
    return checks


def main():
    br = audit_br_rows()
    all_types, optima = audit_unrestricted_masks()
    constructions = audit_construction()
    forest = audit_forest()
    # q=2,L=3 local histograms (z,f)=(0,0),(1,1), b=0.
    assert kapp(2, (1, 1, 1), (0, 0, 1)) == 1
    report = {
        'scope': 'Exact formula/construction self-audit; arbitrary-size proof is in cycle_alignment_budget.md; no root welfare bridge or SPE counterexample',
        'literal_BR_identity_checks': br,
        'full_mask_weighted_lower_bound_checks': all_types,
        'full_mask_exact_weighted_optimum_checks': optima,
        'constructive_every_cardinality_every_sign_every_debt_edge_checks': constructions,
        'generic_forest_gluing_checks': forest,
        'strict_pairwise_but_not_joint_example': {
            'q': 2, 'families': 3, 'signs_D0_O1': [0, 0, 1],
            'local_histogram_each': [[0, 0], [1, 1]],
            'background_each': 0, 'A_each': '1/2',
            'independent_edge_envelope_each': '0',
            'exact_joint_cycle_envelope': '-1/2',
            'identity': 'local alignment marginal witness only, not a SPE instance'
        },
        'all_passed': True,
    }
    (HERE / 'cycle_alignment_audit.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
