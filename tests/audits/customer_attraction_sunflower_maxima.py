"""Independent finite audit of arbitrary sunflower maximal catalogs.

Literal unit-customer masks, exact Fraction payoff comparisons, and complete
ordered-history strategies are used for the small suite. A separately coded
continuation menu checks larger n, retaining all subgame-perfect ties rather
than one count-based policy. Neither imports the canonical CAG package.
Finite success is not a proof of the structural theorem.
"""

from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
import json


def structure(catalog):
    distinct = set(catalog)
    maxima = tuple(sorted(a for a in distinct if not any(
        a != b and a & b == a for b in distinct)))
    if len(maxima) == 1:
        return maxima[0], maxima
    core = maxima[0]
    for a in maxima[1:]:
        core &= a
    petals = tuple(a & ~core for a in maxima)
    if any(a & b for a, b in combinations(petals, 2)):
        return None
    return core, maxima


def private_gap(catalog):
    core, maxima = structure(catalog)
    return len(maxima) == 1 or all(any(
        a & b == a and ((b & ~core) & ~a) for b in maxima)
        for a in set(catalog) - set(maxima))


def seats(catalog, n):
    core, maxima = structure(catalog)
    weights = tuple((b & ~core).bit_count() for b in maxima)
    table = sorted((F(w, k) for w in weights for k in range(1, n + 1)), reverse=True)
    mu = table[n - 1]
    strictly_above = tuple(sum(F(w, k) > mu for k in range(1, n + 1)) for w in weights)
    if mu:
        assert sum(strictly_above) <= n - 1
        assert all(w <= (e + 1) * mu for w, e in zip(weights, strictly_above))
        for count in range(min(n, len(weights)) + 1):
            for indices in combinations(range(len(weights)), count):
                assert sum(weights[j] for j in indices) <= (2 * n - 1) * mu
    assignment = tuple(next(j for j, b in enumerate(maxima) if a & b == a)
                       for a in catalog)
    positive = tuple(sorted(set(v for v in table if v)))
    return core, maxima, weights, mu, assignment, positive


def payoff(catalog, action, terminal):
    return sum((F(1, sum(bool(catalog[b] & (1 << x))
                        for b in terminal))
                for x in range(max(catalog).bit_length())
                if catalog[action] & (1 << x)), F(0))


def welfare(catalog, terminal):
    covered = 0
    for a in terminal:
        covered |= catalog[a]
    return covered.bit_count()


def all_full_spe(catalog, n):
    """Enumerate the Cartesian product of complete child SPE strategies."""
    topics = len(catalog)

    @lru_cache(None)
    def solve(history):
        if len(history) == n:
            return ((history, ()),)
        result = []
        children = [solve(history + (a,)) for a in range(topics)]
        for replies in product(*children):
            values = [payoff(catalog, a, terminal)
                      for a, (terminal, _) in enumerate(replies)]
            descendants = tuple(item for _, policy in replies for item in policy)
            for a, value in enumerate(values):
                if value == max(values):
                    result.append((replies[a][0], ((history, a),) + descendants))
        return tuple(result)

    return solve(())


def verify(catalog, n, terminal, items, audit_threshold=False):
    actions = dict(items)
    expected = {h for i in range(n)
                for h in product(range(len(catalog)), repeat=i)}
    assert len(items) == len(actions) and set(actions) == expected

    def follow(h):
        while len(h) < n:
            h += (actions[h],)
        return h

    assert follow(()) == terminal
    if audit_threshold:
        core, maxima, weights, mu, assignment, positive = seats(catalog, n)
    threshold_checks = 0
    for h in expected:
        actual = follow(h)
        for a in range(len(catalog)):
            branch = follow(h + (a,))
            assert payoff(catalog, actions[h], actual) >= payoff(catalog, a, branch)
        if audit_threshold:
            p = tuple(sum(assignment[a] == j for a in h) for j in range(len(maxima)))
            for j, maximum in enumerate(maxima):
                petal = maximum & ~core
                for x in range(petal.bit_length()):
                    if petal & (1 << x):
                        assert sum(bool(catalog[a] & (1 << x)) for a in h) <= p[j]
            for level in positive:
                capacities = tuple(sum(F(w, k) >= level for k in range(1, n + 1))
                                   for w in weights)
                remaining = sum(max(d - q, 0) for d, q in zip(capacities, p))
                if remaining >= n - len(h):
                    for a in actual[len(h):]:
                        assert payoff(catalog, a, actual) >= level + F(core.bit_count(), n)
                        threshold_checks += 1
    return actions, threshold_checks


def audit_full(catalog, n):
    core, maxima, weights, mu, assignment, positive = seats(catalog, n)
    optimum = max(welfare(catalog, p)
                  for p in product(range(len(catalog)), repeat=n))
    results = all_full_spe(catalog, n)
    assert results
    checks = 0
    for terminal, policy in results:
        actions, verified = verify(catalog, n, terminal, policy, audit_threshold=True)
        checks += verified
        if private_gap(catalog):
            assert all(catalog[a] in maxima for a in actions.values())
        w = welfare(catalog, terminal)
        assert w >= n * mu + core.bit_count()
        assert optimum <= core.bit_count() + (F(2) - F(1, n)) * (w - core.bit_count())
        if private_gap(catalog):
            for i, a in enumerate(terminal):
                for b in range(len(catalog)):
                    deviation = terminal[:i] + (b,) + terminal[i + 1:]
                    assert payoff(catalog, a, terminal) >= payoff(catalog, b, deviation)
    return len(results), sum(len(p) for _, p in results), checks


def audit_menus(catalog, n):
    """Set-valued exact menu, checking every count state and retained action.

    Different action-child menus are chosen independently. Caching outcome sets
    does not force same-load histories to share one continuation strategy.
    """
    core, maxima, weights, mu, assignment, positive = seats(catalog, n)
    m = len(catalog)
    nodes = 0

    def path(q):
        return tuple(a for a, k in enumerate(q) for _ in range(k))

    def add(q, a):
        return q[:a] + (q[a] + 1,) + q[a + 1:]

    @lru_cache(None)
    def solve(q):
        nonlocal nodes
        nodes += 1
        if sum(q) == n:
            return frozenset((q,))
        replies = [solve(add(q, a)) for a in range(m)]
        values = [[(t, payoff(catalog, a, path(t))) for t in menu]
                  for a, menu in enumerate(replies)]
        floor = max(min(u for _, u in table) for table in values)
        retained = set()
        for a, table in enumerate(values):
            for terminal, u in table:
                if u >= floor:
                    if private_gap(catalog):
                        assert catalog[a] in maxima
                    retained.add(terminal)
        assert retained
        p = tuple(sum(q[a] for a in range(m) if assignment[a] == j)
                  for j in range(len(maxima)))
        for level in positive:
            capacities = tuple(sum(F(w, k) >= level for k in range(1, n + 1))
                               for w in weights)
            if sum(max(d - k, 0) for d, k in zip(capacities, p)) >= n - sum(q):
                for terminal in retained:
                    for a in range(m):
                        if terminal[a] > q[a]:
                            assert payoff(catalog, a, path(terminal)) >= level + F(core.bit_count(), n)
        return frozenset(retained)

    root = solve((0,) * m)
    optimum = max(welfare(catalog, p)
                  for k in range(min(m, n) + 1)
                  for p in combinations(range(m), k))
    for q in root:
        w = welfare(catalog, path(q))
        assert w >= n * mu + core.bit_count()
        assert optimum <= core.bit_count() + (F(2) - F(1, n)) * (w - core.bit_count())
    return nodes, len(root)


def main():
    cases = policies = histories = genuinely_overlapping = threshold_checks = 0
    for size in range(1, 5):
        for catalog in combinations(range(8), size):
            structural = structure(catalog)
            if structural is None:
                continue
            for n in (1, 2):
                count, nodes, checked = audit_full(catalog, n)
                cases += 1
                policies += count
                histories += nodes
                threshold_checks += checked
                core, maxima = structural
                global_core = catalog[0]
                for mask in catalog[1:]:
                    global_core &= mask
                genuinely_overlapping += int(len(maxima) > 1 and core != global_core)

    selected = [
        ((7, 25, 2), 3),          # common core 1, private petals 2 each, missing core
        ((7, 25, 0), 3),          # empty strict subtheme
        ((7, 25, 2, 7), 3),       # duplicate maximal label, independent ordered ties
        ((15, 113, 2, 32), 2),    # core 1, three-customer petals, internal omissions
        ((2, 3, 5), 3),           # private-full core-deficient action, non-PNE SPE
        ((30, 31, 97), 2),        # strict nonmaximal root certificate below
    ]
    for catalog, n in selected:
        count, nodes, checked = audit_full(catalog, n)
        cases += 1
        policies += count
        histories += nodes
        threshold_checks += checked

    menu_cases = menu_nodes = menu_outcomes = 0
    for catalog in ((7, 25, 2), (15, 113, 2, 32), (7, 25, 97, 2, 32),
                    (7, 25, 2, 7), (7, 25, 6), (15, 113, 14, 112),
                    (2, 3, 5)):
        for n in (3, 4, 5, 7):
            count, outcomes = audit_menus(catalog, n)
            menu_cases += 1
            menu_nodes += count
            menu_outcomes += outcomes

    # Full boundary certificate: sunflower alone does not imply maximal actions.
    catalog = (30, 31, 97)  # D=4 petals, A=core+4 petals, B=core+2 petals
    policy = (((), 0), ((0,), 2), ((1,), 1), ((2,), 1))
    assert structure(catalog) is not None and not private_gap(catalog)
    verify(catalog, 2, (0, 2), policy)
    assert welfare(catalog, (0, 2)) == 7
    assert payoff(catalog, 0, (0, 2)) == 4

    # One exact arithmetic improvement example and zero boundary for the
    # general-maxima interface; neither is a universal welfare audit.
    triangle = (7 | 512 | 1024, 56 | 512 | 2048, 448 | 1024 | 2048)
    general_table = []
    for j, maximum in enumerate(triangle):
        others = 0
        for k, other in enumerate(triangle):
            if j != k:
                others |= other
        private = (maximum & ~others).bit_count()
        shared = maximum.bit_count() - private
        assert (private, shared) == (3, 2)
        general_table.extend(F(private, k) + F(shared, 3) for k in range(1, 4))
    general_mu = sorted(general_table, reverse=True)[2]
    assert general_mu == F(11, 3) and 3 * general_mu == 11
    assert sorted([F(0, k) + F(0, 3) for k in range(1, 4)], reverse=True)[2] == 0
    print(json.dumps({
        "full_strategy_catalog_cases": cases,
        "full_spe_policies": policies,
        "ordered_history_nodes": histories,
        "full_history_threshold_player_checks": threshold_checks,
        "cases_outside_old_global_core_structure": genuinely_overlapping,
        "larger_set_menu_cases": menu_cases,
        "larger_set_menu_count_states": menu_nodes,
        "larger_set_menu_root_outcomes": menu_outcomes,
        "nonmaximal_and_non_PNE_sunflower_certificate": "verified DB, W=OPT=7",
        "general_private_shared_seat_arithmetic_example": "n=3, w=3, v=2, nu=11/3, W>=11",
        "general_zero_seat_boundary": "nu=0",
        "universal_proof_source": "sunflower_maxima_bound.md sections 2-3",
        "verification_scope": "finite regression, not a universal proof",
    }, indent=2))


if __name__ == "__main__":
    main()
