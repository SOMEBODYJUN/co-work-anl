"""Exact audit of parity closure and its Gram boundary.

Signed witnesses are never called customer instances or half counterexamples.
The mathematical claims are in parity_symmetric_difference.md.
"""
from collections import defaultdict
from functools import lru_cache
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import argparse
import json


def masks(p, maximum):
    return [s for s in range(1 << p) if s.bit_count() <= maximum]


def chi(s, b):
    return -1 if (s & b).bit_count() % 2 else 1


def parity_mass(w, s):
    return sum(v for b, v in w.items() if (b & s).bit_count() % 2)


def cover(w, s):
    return sum(v for b, v in w.items() if b & s)


def subsets(s):
    t = s
    while t:
        yield t
        t = (t - 1) & s


def coverage_expansion(w, s):
    return sum((-1) ** (s.bit_count() + t.bit_count())
               * (1 << (t.bit_count() - 1)) * cover(w, t)
               for t in subsets(s))


def all_projections(w, p, maximum):
    checked = 0
    least = None
    for d in masks(p, maximum):
        projected = defaultdict(int)
        for b, mass in w.items():
            projected[b & d] += mass
        value = min(projected.values(), default=0)
        least = value if least is None else min(least, value)
        assert value >= 0, (d, dict(projected))
        checked += 1
    return {"supports": checked, "minimum_recorded_cell": least}


def all_visible_triangles(w, p, maximum):
    visible = masks(p, maximum)
    pm = {e: parity_mass(w, e) for e in visible}
    checked = 0
    least = None
    for e in visible:
        for f in visible:
            d = e ^ f
            if d not in pm:
                continue
            slack = pm[e] + pm[f] - pm[d]
            assert slack >= 0, (e, f, d, slack)
            least = slack if least is None else min(least, slack)
            checked += 1
    return {"ordered_triangles": checked, "minimum_slack": least}


def original_parity(m):
    p = 2 * m
    x = (1 << (m - 1)) - 1
    y = x << (m - 1)
    u, v = 1 << (p - 2), 1 << (p - 1)
    es = [x | u, x | v, y | u, y | v]
    w = {b: 1 + chi(es[0], b) + chi(es[1], b)
         + chi(es[2], b) - chi(es[3], b) for b in range(1 << p)}
    return p, es, u ^ v, w


def original_audit(m):
    p, es, symmetric, w = original_parity(m)
    total = 1 << p
    assert sum(w.values()) == total
    assert set(w.values()) == {-1, 3}
    pe, pf, pd = [parity_mass(w, e) for e in [es[0], es[1], symmetric]]
    assert (pe, pf, pd) == (0, 0, total // 2)
    row = sum(mass * (1 - chi(es[0], b)) * (1 - chi(es[1], b))
              for b, mass in w.items())
    assert row == -total
    nonempty = {b: mass for b, mass in w.items() if b}
    assert sum(mass * (1 - chi(es[0], b)) * (1 - chi(es[1], b))
               for b, mass in nonempty.items()) == row
    for e in masks(p, m):
        assert coverage_expansion(w, e) == parity_mass(w, e)
    opt = max(cover(w, e) for e in masks(p, m))
    assert cover(w, es[3]) == opt == total
    uniform = {b: 1 for b in range(1 << p)}
    assert cover(uniform, es[3]) == total - (1 << m)
    return {"m": m, "p": p, "signed_total": total,
            "parity_directions": [pe, pf, pd], "new_row": row,
            "signed_root_and_opt": opt,
            "uniform_root_and_opt": total - (1 << m),
            "projections": all_projections(w, p, m)}


def base_witness():
    w = {b: 0 for b in range(16)}
    w[0] = 3
    for a in range(4):
        w[1 << a] = -1
    for a, b in [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3)]:
        w[(1 << a) | (1 << b)] = 1
    return w


def lifted_witness(m):
    assert m == 2 or m >= 4
    d = m // 2
    blocks = [((1 << d) - 1) << (j * d) for j in range(4)]
    base = base_witness()
    w = {}
    for b in range(1 << (4 * d)):
        virtual = sum(((b & block).bit_count() % 2) << j
                      for j, block in enumerate(blocks))
        w[b] = base[virtual]
    return 4 * d, blocks, w


def gram_boundary_audit(m):
    p, blocks, w = lifted_witness(m)
    factor = 1 << (p - 4)
    assert sum(w.values()) == 4 * factor
    assert 3 * (m // 2) > m
    square = sum(mass * (2 + 2 * chi(blocks[0], b)
                         + 2 * chi(blocks[1], b)
                         - 3 * chi(blocks[2], b)
                         - 3 * chi(blocks[3], b)) ** 2
                 for b, mass in w.items())
    assert square == -24 * factor
    aa = [0] + blocks
    z = [2, 2, 2, -3, -3]
    assert sum(z) == 0
    negative_type_left = sum(z[i] * z[j] * parity_mass(w, aa[i] ^ aa[j])
                             for i in range(5) for j in range(5))
    assert negative_type_left == 12 * factor
    assert square == -2 * negative_type_left
    assert max((aa[i] ^ aa[j]).bit_count()
               for i in range(5) for j in range(5)) <= m
    assert 2 + 2 + 2 - 3 - 3 == 0
    for e in masks(p, m):
        assert coverage_expansion(w, e) == parity_mass(w, e)
    return {"m": m, "p": p, "block_size": m // 2,
            "lift_factor": factor, "signed_total": 4 * factor,
            "square_value": square,
            "negative_type_left": negative_type_left,
            "projections": all_projections(w, p, m),
            "visible_parity_triangles": all_visible_triangles(w, p, m)}


def literal_full_spe_m3():
    """One actual complete count policy, expanded over all ordered histories.

    It is a SPE of the signed game and, separately, of the legal uniform game.
    This is a construction, not a restriction on admissible history dependence.
    """
    m = 3
    p, es, _, w = original_parity(m)
    uniform = {b: 1 for b in range(1 << p)}

    @lru_cache(None)
    def utility(q, a, which):
        weights = w if which == "signed" else uniform
        return sum((F(mass, sum(q[j] for j in range(p) if b >> j & 1))
                    for b, mass in weights.items() if b >> a & 1), F(0))

    policy = {}

    @lru_cache(None)
    def terminal(q):
        if sum(q) == m:
            return q
        candidates = []
        for a in range(p):
            child = list(q)
            child[a] += 1
            final = terminal(tuple(child))
            candidates.append((utility(final, a, "signed"), -a, final))
        value, minus_a, final = max(candidates)
        policy[q] = -minus_a
        return final

    terminal((0,) * p)
    minimum = {"signed": None, "uniform": None}
    rows = 0
    for depth in range(m):
        for history in product(range(p), repeat=depth):
            q = tuple(history.count(a) for a in range(p))
            chosen = policy[q]
            actual = terminal(q)
            for a in range(p):
                child = list(q)
                child[a] += 1
                alternate = terminal(tuple(child))
                for which in ["signed", "uniform"]:
                    slack = utility(actual, chosen, which) - utility(alternate, a, which)
                    assert slack >= 0, (history, a, which, slack)
                    if minimum[which] is None or slack < minimum[which]:
                        minimum[which] = slack
                rows += 1
    history = []
    while len(history) < m:
        q = tuple(history.count(a) for a in range(p))
        history.append(policy[q])
    assert history == [2, 3, 5], history
    root_support = sum(1 << a for a in history)
    assert root_support == es[3]
    return {"m": 3, "p": p, "root_path": history,
            "all_ordered_comparisons": rows,
            "minimum_slack": {k: str(v) for k, v in minimum.items()},
            "signed_W": cover(w, root_support),
            "uniform_W": cover(uniform, root_support)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--large", action="store_true",
                        help="Also audit the 12-label m=6 block lift.")
    args = parser.parse_args()
    # Literal per-customer coverage expansion independently of either witness.
    for p in range(1, 6):
        for b in range(1 << p):
            w = {b: 1}
            for e in range(1 << p):
                assert coverage_expansion(w, e) == parity_mass(w, e)
    result = {
        "status": "exact finite audit passed; general claims require the written proofs",
        "scope": "signed separation witnesses, never CAG counterexamples",
        "old_parity": [original_audit(m) for m in [3, 4, 5]],
        "old_actual_path_m3": literal_full_spe_m3(),
        "triangle_not_gram": [gram_boundary_audit(m) for m in
                              ([2, 4, 5, 6] if args.large else [2, 4, 5])],
    }
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
