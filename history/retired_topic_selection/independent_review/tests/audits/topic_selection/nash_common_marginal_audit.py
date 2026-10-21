"""Exact finite audit, not a proof: common-marginal trembling matroid games.

Run from repository root with Python 3. No third party dependencies.
Checks direct expected costs against conditional (n-1 opponent) resource delays.
Also records a Hall obstruction to base-orderability of the K4 graphic matroid.
"""
from fractions import Fraction as F
from itertools import combinations, permutations, product
import json


def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return tuple(p)


def add(p, q):
    return trim([sum(t) for t in zip(p + (F(0),) * max(0, len(q)-len(p)),
                                  q + (F(0),) * max(0, len(p)-len(q)))])


def neg(p):
    return tuple(-a for a in p)


def sub(p, q):
    return add(p, neg(q))


def mul(p, q):
    ans = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            ans[i+j] += a*b
    return trim(ans)


def scale(p, a):
    return trim([a*b for b in p])


def sign(p):
    return next((1 if a > 0 else -1 for a in p if a), 0)


def expected_delay(probabilities, delays):
    """One deterministic user plus independent random opponents."""
    counts = [(F(1),)]
    for probability in probabilities:
        updated = [(F(0),)] * (len(counts)+1)
        for k, mass in enumerate(counts):
            updated[k] = add(updated[k], mul(mass, sub((F(1),), probability)))
            updated[k+1] = add(updated[k+1], mul(mass, probability))
        counts = updated
    ans = (F(0),)
    for k, mass in enumerate(counts):
        ans = add(ans, scale(mass, delays[k+1]))
    return ans


E = tuple(range(4))
all_pairs = tuple(frozenset(b) for b in combinations(E, 2))
bases = [tuple(b for b in all_pairs if b != frozenset({0, 1})),
         tuple(b for b in all_pairs if b != frozenset({0, 2}))]
q = [{frozenset({0,2}): F(2,20), frozenset({0,3}): F(2,20),
      frozenset({1,2}): F(4,20), frozenset({1,3}): F(7,20),
      frozenset({2,3}): F(5,20)},
     {frozenset({0,1}): F(2,20), frozenset({0,3}): F(2,20),
      frozenset({1,2}): F(4,20), frozenset({1,3}): F(5,20),
      frozenset({2,3}): F(7,20)}]
bases.append(bases[0])
q.append(q[0])
n = len(bases)
p = tuple(sum(q[0][b] for b in bases[0] if e in b) for e in E)
assert p == (F(1,5), F(11,20), F(11,20), F(7,10))
for i in range(n):
    assert sum(q[i].values()) == 1 and min(q[i].values()) > 0
    assert tuple(sum(q[i][b] for b in bases[i] if e in b) for e in E) == p


def direct_cost(profile, i, delays):
    ans = (F(0),)
    for random_profile in product(*bases):
        probability = (F(1),)
        for j, random_basis in enumerate(random_profile):
            probability = mul(probability,
                              (F(random_basis == profile[j]),
                               q[j][random_basis] - F(random_basis == profile[j])))
        cost = sum(delays[e][sum(e in b for b in random_profile)]
                   for e in random_profile[i])
        ans = add(ans, scale(probability, cost))
    return ans


def transformed_cost(profile, i, delays):
    ans = (F(0),)
    for e in profile[i]:
        probabilities = [(F(e in profile[j]), p[e]-F(e in profile[j]))
                         for j in range(n) if j != i]
        ans = add(ans, expected_delay(probabilities, delays[e]))
    return ans


delay_families = [
    [[0, 1, 1, 2], [0, 0, 3, 4], [0, 2, 2, 5], [0, 1, 4, 9]],
    [[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]],
    [[0, 0, 0, 0], [0, 2, 2, 2], [0, 1, 1, 8], [0, 0, 5, 5]],
]
checked = 0
equilibria = []
for delays in delay_families:
    count_equilibria = 0
    for profile in product(*bases):
        stable = True
        for i in range(n):
            initial_direct = direct_cost(profile, i, delays)
            initial_transformed = transformed_cost(profile, i, delays)
            for deviation in bases[i]:
                alternate = list(profile)
                alternate[i] = deviation
                direct_difference = sub(direct_cost(alternate, i, delays), initial_direct)
                transformed_difference = sub(transformed_cost(alternate, i, delays), initial_transformed)
                assert direct_difference == mul((F(1), F(-1)), transformed_difference)
                stable &= sign(transformed_difference) >= 0
                checked += 1
        count_equilibria += stable
    assert count_equilibria > 0
    equilibria.append(count_equilibria)


edges = tuple(combinations(range(4), 2))


def tree(selected):
    reached = {0}
    while True:
        enlarged = reached | {v for e in selected for u, v in (edges[e], edges[e][::-1]) if u in reached}
        if enlarged == reached:
            return len(reached) == 4
        reached = enlarged


trees = tuple(frozenset(t) for t in combinations(range(6), 3) if tree(t))
assert len(trees) == 16
tree_set = set(trees)
hall = None
for first, second in product(trees, repeat=2):
    left, right = first-second, second-first
    adjacency = {e: {f for f in right
                     if first-{e}|{f} in tree_set and second-{f}|{e} in tree_set}
                 for e in left}
    for size in range(1, len(left)+1):
        for subset in combinations(sorted(left), size):
            neighbors = set().union(*(adjacency[e] for e in subset))
            if len(neighbors) < size:
                hall = {"first_basis": sorted(first), "second_basis": sorted(second),
                        "left_subset": list(subset), "neighbor_subset": sorted(neighbors)}
                break
        if hall:
            break
    if hall:
        break
assert hall is not None

print(json.dumps({
    "status": "finite exact audit only; no theorem or novelty certification",
    "players": n, "resources": len(E), "bases_per_player": [len(b) for b in bases],
    "common_marginal": list(map(str, p)),
    "delay_families": delay_families,
    "checked_deviation_equalities": checked,
    "lexicographic_pure_equilibrium_counts": equilibria,
    "K4_edge_numbering": edges,
    "K4_tree_count": len(trees), "K4_Hall_obstruction": hall,
}, indent=2))
