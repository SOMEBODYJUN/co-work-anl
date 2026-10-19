"""Finite exact audit of the weighted profile-exchange coupling, not the algorithm.

Enumerates original resource ownerships and leaf matchability directly.  Does not
use matroid exchange, the potential formula, or the proof's coupling construction.
No end-to-end 19/10 or asymptotic claim is inferred from these small instances.
"""

from fractions import Fraction as F
from itertools import product
import json
import random


def leaves_fit(leaf_edges, free_mask):
    reachable = {0}
    for edges in leaf_edges:
        reachable = {
            used | (1 << u)
            for used in reachable
            for u in edges
            if (free_mask & (1 << u)) and not (used & (1 << u))
        }
        if not reachable:
            return False
    return True


def optimal_vectors(profile, menus, owner, home_weight, lambdas, leaf_edges, n):
    states = [menus[j][s] if s >= 0 else (F(0),) * n
              for j, s in enumerate(profile)]
    choices = [(-1,) + tuple(j for j in range(len(owner)) if states[j][u])
               for u in range(n)]
    fit = {mask: leaves_fit(leaf_edges, ((1 << n) - 1) ^ mask)
           for mask in range(1 << n)}
    best = None
    vectors = set()
    enumerated = 0
    for assignment in product(*choices):
        used = sum(1 << u for u, j in enumerate(assignment) if j >= 0)
        if not fit[used]:
            continue
        enumerated += 1
        values = [F(0)] * len(lambdas)
        for u, j in enumerate(assignment):
            if j >= 0:
                values[owner[j]] += home_weight[j] * states[j][u]
        vector = tuple(lambdas[i] * values[i] for i in range(len(lambdas)))
        value = sum(vector)
        if best is None or value > best:
            best = value
            vectors = {vector}
        elif value == best:
            vectors.add(vector)
    assert best is not None
    return best, vectors, enumerated


def audit():
    rng = random.Random(31082026)
    tested = 0
    ownerships = 0
    old_optima = 0
    extreme_weight_cases = 0
    same_outer_helper_changes = 0
    for case in range(240):
        n = 4 + case % 2
        nleaves = 1 + (case // 2) % 2
        while True:
            leaf_edges = [tuple(u for u in range(n) if rng.randrange(3))
                          for _ in range(nleaves)]
            if leaves_fit(leaf_edges, (1 << n) - 1):
                break
        menus = []
        for _ in range(3):
            states = []
            for _ in range(2):
                raw = [rng.randrange(4) for _ in range(n)]
                if not sum(raw):
                    raw[rng.randrange(n)] = 1
                states.append(tuple(F(x, sum(raw)) for x in raw))
            menus.append(states)
        owner = (0, 0, 1)
        home_weight = (F(2, 5), F(3, 5), F(1))
        if case % 3 == 0:
            lambdas = (F(1, 17), F(91, 17))
            extreme_weight_cases += 1
        elif case % 3 == 1:
            lambdas = (F(27, 5), F(2, 9))
            extreme_weight_cases += 1
        else:
            lambdas = (F(1), F(1))
        profile = tuple(rng.choice((-1, 0, 1)) for _ in range(3))
        j = case % 3
        s_new = rng.choice(tuple(s for s in (-1, 0, 1) if s != profile[j]))
        changed = list(profile)
        changed[j] = s_new
        old_best, old, nold = optimal_vectors(
            profile, menus, owner, home_weight, lambdas, leaf_edges, n)
        new_best, new, nnew = optimal_vectors(
            changed, menus, owner, home_weight, lambdas, leaf_edges, n)
        bound = lambdas[owner[j]] * home_weight[j]
        for x in old:
            successful = []
            for y in new:
                diff = tuple(y[i] - x[i] for i in range(len(lambdas)))
                if max(map(abs, diff)) <= bound and sum(map(abs, diff)) <= 2 * bound:
                    assert sum(diff) == new_best - old_best
                    successful.append(y)
            assert successful, (case, profile, changed, x, old_best, new_best, new)
        tested += 1
        old_optima += len(old)
        ownerships += nold + nnew
        same_outer_helper_changes += int(j in (0, 1))
    return {
        "scope": "Exact finite integral-network coupling only; no asymptotic or full-algorithm audit",
        "cases": tested,
        "feasible_original_resource_ownerships": ownerships,
        "all_old_optimal_outer_vectors_checked": old_optima,
        "heterogeneous_lambda_cases": extreme_weight_cases,
        "changed_helper_has_other_same_outer_helper_cases": same_outer_helper_changes,
        "passed": True,
    }


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True, indent=2))
