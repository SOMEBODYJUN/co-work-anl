"""Independent exact endpoint-rank audit; no author audit is imported.

This is finite evidence for the resource and deviation inequalities, not a
proof of their universal real-parameter statements or of WC-TARGET.
"""
from fractions import Fraction as F
from itertools import combinations
import hashlib,platform,sys
import json
from pathlib import Path
import random


SEED = 20261015
RNG = random.Random(SEED)
COUNTS = {"rank_pairs": 0, "raw_marginals": 0, "mixed_marginals": 0,
          "deviation_bounds": 0, "closed_walks": 0}


def ranks(weights, sets):
    arcs = set()
    for users in sets:
        for i, j in combinations(users, 2):
            if weights[i] != weights[j]:
                arcs.add((i, j) if weights[i] > weights[j] else (j, i))
    depth = {i: 1 for i in weights}
    for i in sorted(weights, key=lambda x: -weights[x]):
        for u, v in arcs:
            if u == i:
                depth[v] = max(depth[v], depth[u] + 1)
    for users in sets:
        for i, j in combinations(users, 2):
            assert depth[i] != depth[j] or weights[i] == weights[j]
            if depth[i] < depth[j]:
                assert weights[i] >= weights[j]
            if depth[j] < depth[i]:
                assert weights[j] >= weights[i]
            COUNTS["rank_pairs"] += 1
    return depth, max(depth.values(), default=0), arcs


def cost(coeff, x):
    return sum(a * x ** p for p, a in coeff.items())


def shifted(coeff, background):
    from math import comb
    return {r: sum(a * comb(p, r) * background ** (p-r)
                   for p, a in coeff.items() if p >= r)
            for r in range(max(coeff, default=0) + 1)}


def ordered(users, weights, depth, k, b, coeff):
    permutation = list(range(k, b, -1)) + list(range(1, b+1))
    position = {r: j for j, r in enumerate(permutation)}
    load = F(0)
    result = F(0)
    for i in sorted(users, key=lambda i: (position[depth[i]], i)):
        load += weights[i]
        result += weights[i] * cost(coeff, load)
    return result


def raw_checks(weights, depth, k, before, i, coeff, d):
    after = before | {i}
    y = sum((weights[j] for j in after), F(0))
    unit = weights[i] * cost(coeff, y)
    for b in range(1, k+1):
        delta = (ordered(after, weights, depth, k, b, coeff)
                 - ordered(before, weights, depth, k, b, coeff))
        lo, hi = ((unit, d * unit) if b < depth[i]
                  else (unit, unit) if b == depth[i]
                  else (F(0), unit))
        assert lo <= delta <= hi, (weights, depth, before, i, b, delta, lo, hi)
        COUNTS["raw_marginals"] += 1


def mixed(users, weights, depth, k, coeff, a, t):
    return sum(t**(b-1) / a * ordered(users, weights, depth, k, b, coeff)
               for b in range(1, k+1))


def mixed_check(weights, depth, k, before, i, coeff, a, t):
    after = before | {i}
    y = sum((weights[j] for j in after), F(0))
    h = weights[i] * sum(t**(b-1) / a for b in range(1, depth[i]+1))
    delta = (mixed(after, weights, depth, k, coeff, a, t)
             - mixed(before, weights, depth, k, coeff, a, t))
    assert h * cost(coeff, y) <= delta <= a * h * cost(coeff, y)
    COUNTS["mixed_marginals"] += 1


def test_supports(weights, supports):
    depth, k, arcs = ranks(weights, supports)
    for t in (F(1), F(2)):
        a = sum(t**j for j in range(k))
        d = int(1 + t*a)
        assert a == sum(((d-1)/a)**j for j in range(k))
        assert 1 <= a < d
        assert sum(t**(b-1)/a for b in range(1, k+1)) == 1
        for support in supports:
            ids = list(support)
            for mask in range(1 << len(ids)):
                before = {ids[j] for j in range(len(ids)) if (mask >> j) & 1}
                for i in support - before:
                    for base, background in (({0: F(0)}, F(0)),
                                             ({0: F(1)}, F(0)),
                                             ({d: F(1)}, F(2, 3)),
                                             ({0: F(1, 5), 1: F(2), d: F(1, 3)}, F(7, 4))):
                        coeff = shifted(base, background)
                        raw_checks(weights, depth, k, before, i, coeff, d)
                        mixed_check(weights, depth, k, before, i, coeff, a, t)
    return depth, k, arcs


def test_closed_walk(weights, path, resources):
    moving = {i for left, right in zip(path, path[1:])
              for i in weights if left[i] != right[i]}
    active_weights = {i: weights[i] for i in moving}
    endpoint_sets = [{i for i in moving if e in state[i]}
                     for state in path for e in resources]
    depth, k, arcs = ranks(active_weights, endpoint_sets)
    if not moving:
        return
    a = F(k)  # t=1 is an exact rational root at d=k+1.
    t, d = F(1), k+1
    base = {0: F(1, 3), d: F(2, 5)}
    backgrounds = {e: sum((weights[i] for i in weights
                           if i not in moving and e in path[0][i]), F(0))
                   for e in resources}
    coeffs = {e: shifted(base, backgrounds[e]) for e in resources}
    potentials = [sum(mixed({i for i in moving if e in state[i]}, active_weights,
                            depth, k, coeffs[e], a, t) for e in resources)
                  for state in path]
    assert path[0] == path[-1]
    for step, (left, right) in enumerate(zip(path, path[1:])):
        movers = [i for i in weights if left[i] != right[i]]
        assert len(movers) == 1
        i = movers[0]
        old = sum(cost(base, sum((weights[j] for j in weights if e in left[j]), F(0)))
                  for e in left[i])
        new = sum(cost(base, sum((weights[j] for j in weights if e in right[j]), F(0)))
                  for e in right[i])
        common = sum(cost(base, sum((weights[j] for j in weights if e in left[j]), F(0)))
                     for e in left[i] & right[i])
        h = weights[i] * F(depth[i], k)
        assert potentials[step+1] - potentials[step] <= h*(a*new-old-(a-1)*common)
        COUNTS["deviation_bounds"] += 1
        for e in left[i] ^ right[i]:
            before = {j for j in moving if j != i and e in left[j]}
            raw_checks(active_weights, depth, k, before, i, coeffs[e], d)
            mixed_check(active_weights, depth, k, before, i, coeffs[e], a, t)
    assert sum(potentials[j+1]-potentials[j] for j in range(len(path)-1)) == 0
    COUNTS["closed_walks"] += 1
    return depth, k, arcs


def main():
    # Same rank / unequal weights, and equal weights / different ranks,
    # including equal weights sharing a resource across those different ranks.
    weights = dict(enumerate(map(F, (9, 7, 3, 2, 1, 3))))
    supports = [{0, 2}, {1, 3}, {2, 4}, {2, 5}]
    depth, k, arcs = test_supports(weights, supports)
    assert depth[0] == depth[1] and weights[0] != weights[1]
    assert depth[2] != depth[5] and weights[2] == weights[5]
    assert k == 3 and len(set(weights.values())) == 5
    fixture = {"weights": {i: str(w) for i, w in weights.items()},
               "ranks": depth, "height": k, "distinct_weights": 5,
               "supports": [sorted(u) for u in supports]}

    # The potential support graph has height 3, but the visited endpoint graph
    # has height 2. All three players move; a fourth player stays as background.
    weights = {0: F(9), 1: F(3), 2: F(1), 3: F(5, 2)}
    path = []
    for users in (set(), {0}, {0, 2}, {2}, set(), {1}, set()):
        path.append({i: ({0} if i in users or i == 3 else set()) for i in weights})
    actual_depth, actual_k, actual_arcs = test_closed_walk(weights, path, {0})
    assert actual_k == 2
    assert ranks({i: weights[i] for i in range(3)}, [{0, 1, 2}])[1] == 3
    closed_fixture = {"height": actual_k, "ranks": actual_depth,
                      "arcs": sorted(actual_arcs), "potential_height": 3}

    for trial in range(35):
        n = RNG.randrange(1, 6)
        weights = {i: F(RNG.randrange(1, 10), RNG.randrange(1, 4)) for i in range(n)}
        supports = [{i for i in weights if RNG.randrange(2)} for _ in range(3)]
        test_supports(weights, supports)
    for trial in range(80):
        weights = {i: F(RNG.randrange(1, 10), RNG.randrange(1, 4)) for i in range(5)}
        current = {i: {e for e in range(3) if RNG.randrange(2)} for i in weights}
        initial = {i: set(s) for i, s in current.items()}
        path = [{i: set(s) for i, s in current.items()}]
        # Player 4 is intentionally fixed, while active players make arbitrary
        # legal subset changes. Restore each coordinate for an actual closed walk.
        for _ in range(8):
            i = RNG.randrange(4)
            e = RNG.randrange(3)
            current[i] ^= {e}
            path.append({i: set(s) for i, s in current.items()})
        for i in range(4):
            if current[i] != initial[i]:
                current[i] = set(initial[i])
                path.append({j: set(s) for j, s in current.items()})
        test_closed_walk(weights, path, set(range(3)))
    result = {"python_version":platform.python_version(),"command":" ".join(sys.argv),"status": "all exact assertions passed", "seed": SEED,
              "arithmetic": "fractions.Fraction, no floating-point comparisons",
              "counts": COUNTS, "heterogeneous_rank_fixture": fixture,
              "endpoint_only_fixture": closed_fixture,
              "scope": "finite resource/multi-resource endpoint inequalities only; not a universal proof"}
    result["audit_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
