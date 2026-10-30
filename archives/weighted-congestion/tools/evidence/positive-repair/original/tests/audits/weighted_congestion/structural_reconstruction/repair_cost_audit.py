#!/usr/bin/env python3
"""Literal-resource independent checks of the complete anchor repair interface.

No repository audit is imported. Fraction arithmetic is used throughout.
This is finite evidence, not a replacement for the general proof.
"""
from fractions import Fraction as Q
from itertools import product, combinations
import json
import hashlib
from pathlib import Path


class Game:
    def __init__(self, weights):
        self.weights = tuple(map(Q, weights))
        self.actions = [[set(), set()] for _ in weights]
        self.polynomials = []

    def resource(self, polynomial, entries):
        e = len(self.polynomials)
        self.polynomials.append(tuple(map(Q, polynomial)))
        for i, bit in entries:
            self.actions[i][bit].add(e)

    def monomial(self, degree, coefficient, entries):
        self.resource([Q(0)] * degree + [Q(coefficient)], entries)

    def costs(self, s):
        x = [Q(0)] * len(self.polynomials)
        for i, bit in enumerate(s):
            for e in self.actions[i][bit]:
                x[e] += self.weights[i]
        fee = []
        for e, polynomial in enumerate(self.polynomials):
            value = Q(0)
            for coefficient in reversed(polynomial):
                value = value * x[e] + coefficient
            fee.append(value)
        return tuple(sum((fee[e] for e in self.actions[i][bit]), Q(0))
                     for i, bit in enumerate(s))

    def states(self):
        return list(product((0, 1), repeat=len(self.weights)))

    def stable(self, s, alpha):
        old = self.costs(s)
        return all(old[i] <= alpha * self.costs(flip(s, i))[i]
                   for i in range(len(s)))

    def social(self, s, coefficients=None):
        return sum((q * cost for q, cost in zip(coefficients or self.weights,
                                               self.costs(s))), Q(0))


def flip(s, i):
    ans = list(s)
    ans[i] ^= 1
    return tuple(ans)


def front(bits):
    return sum(x != y for x, y in zip(bits, bits[1:])) <= 1


def in_front(s, classes):
    return all(front(tuple(s[i] for i in cc)) for cc in classes)


def add_clocks(g, classes, heights, degrees):
    for cc, height, degree in zip(classes, heights, degrees):
        w = g.weights[cc[0]]
        assert all(g.weights[i] == w for i in cc)
        for j, k in combinations(cc[1:], 2):
            for side in (0, 1):
                entries = [(i, side ^ phase)
                           for i, phase in zip((cc[0], j, k), (0, 1, 0))]
                g.monomial(degree, height / (3 * w) ** degree, entries)


def geometry_check():
    states = edges = 0
    for n in range(1, 10):
        for s in product((0, 1), repeat=n):
            states += 1
            triggered = [triple for triple in combinations(range(1, n), 2)
                         if (s[0], s[triple[0]], s[triple[1]]) in
                         ((0, 1, 0), (1, 0, 1))]
            assert bool(triggered) == (not front(s))
            if front(s):
                for i in range(n):
                    t = flip(s, i)
                    if not front(t):
                        continue
                    edges += 1
                    for j, k in combinations(range(1, n), 2):
                        triple = (0, j, k)
                        if i not in triple:
                            continue
                        old = tuple(s[u] ^ p for u, p in zip(triple, (0, 1, 0)))
                        new = tuple(t[u] ^ p for u, p in zip(triple, (0, 1, 0)))
                        idx = triple.index(i)
                        assert sum(x == old[idx] for x in old) == 2
                        assert sum(x == new[idx] for x in new) == 2
            else:
                i = next(j for j in range(1, n) if s[j] != s[0])
                t = flip(s, i)
                assert all((t[0], t[j], t[k]) not in ((0, 1, 0), (1, 0, 1))
                           for j, k in combinations(range(1, n), 2)
                           if i in (0, j, k))
    return dict(states=states, directed_front_edges=edges)


def transfer_case(sizes, alpha):
    weights = []
    classes = []
    for a, n in enumerate(sizes):
        cc = tuple(range(len(weights), len(weights) + n))
        classes.append(cc)
        weights.extend([Q(a + 1, a + 2)] * n)
    g = Game(weights)
    for i in range(len(weights)):
        for b in (0, 1):
            g.resource([Q((i + 2 * b) % 4)], [(i, b)])
    # Shared resources include mandatory usage (same resource in both actions).
    for r in range(2):
        entries = []
        for i in range(len(weights)):
            code = (i * (r + 2) + r) % 4
            entries.extend([(i, code)] if code < 2 else
                           [(i, 0), (i, 1)] if code == 2 else [])
        g.resource([Q(1, 5), Q(1, 7), Q(1, 11)], entries)
    states = g.states()
    base = {s: g.costs(s) for s in states}
    B = max(max(x) for x in base.values())
    L = max((n - 1) * (n - 2) // 2 for n in sizes)
    height = 2 * alpha * max(B, Q(1))
    degree = 1
    while height <= alpha * (B + L * height * Q(2, 3) ** degree):
        degree += 1
    add_clocks(g, classes, [height] * len(classes), [degree] * len(classes))
    u, z = height * Q(2, 3) ** degree, height * Q(1, 3) ** degree
    actual = set()
    predicted = set()
    core = set()
    K = sum((g.weights[cc[0]] * ((len(cc) - 1) * (len(cc) - 2) // 2)
             * (2 * u + z) for cc in classes), Q(0))
    move_checks = 0
    social_repairs = 0
    for s in states:
        trigger_count_weight = Q(0)
        for cc in classes:
            trigger_count = sum((s[cc[0]], s[j], s[k]) in ((0, 1, 0), (1, 0, 1))
                                for j, k in combinations(cc[1:], 2))
            trigger_count_weight += g.weights[cc[0]] * trigger_count
        base_social = sum((w * b for w, b in zip(g.weights, base[s])), Q(0))
        assert g.social(s) == base_social + K + trigger_count_weight * (3 * height - 2 * u - z)
        if g.stable(s, alpha):
            actual.add(s)
        if not in_front(s, classes):
            cc = next(cc for cc in classes if not front(tuple(s[i] for i in cc)))
            i = next(i for i in cc[1:] if s[i] != s[cc[0]])
            assert g.costs(s)[i] > alpha * g.costs(flip(s, i))[i]
            # All test bases have degree at most 2, and alpha>=1, so the
            # new social-compression theorem applies without further budget.
            assert g.social(s) > g.social(flip(s, i))
            social_repairs += 1
            continue
        assert g.social(s) == sum((w * b for w, b in zip(g.weights, base[s])), Q(0)) + K
        survives = core_survives = True
        for cc in classes:
            n = len(cc)
            for position, i in enumerate(cc):
                t = flip(s, i)
                margin = g.costs(s)[i] - alpha * g.costs(t)[i]
                move_checks += 1
                if in_front(t, classes):
                    r = (n - 1) * (n - 2) // 2 if position == 0 else max(n - 2, 0)
                    bm = base[s][i] - alpha * base[t][i]
                    assert margin == bm - (alpha - 1) * r * u
                    survives &= bm <= (alpha - 1) * r * u
                    core_survives &= bm <= 0
                else:
                    assert margin < 0
        if survives:
            predicted.add(s)
        if core_survives:
            core.add(s)
    assert actual == predicted
    assert core <= actual
    fronts = [s for s in states if in_front(s, classes)]
    front_base_opt = min(sum((w * b for w, b in zip(g.weights, base[s])), Q(0))
                         for s in fronts)
    full_opt = min(map(g.social, states))
    assert full_opt == front_base_opt + K
    for s in actual:
        b_social = sum((w * b for w, b in zip(g.weights, base[s])), Q(0))
        if front_base_opt > 0:
            lam = b_social / front_base_opt
            assert lam >= 1 and g.social(s) <= lam * full_opt
        else:
            assert full_opt == K
    if alpha == 1:
        assert actual == core
    return dict(sizes=sizes, alpha=str(alpha), states=len(states), move_checks=move_checks,
                degree=degree, base_core_stable=len(core), expanded_stable=len(actual),
                K=str(K), social_repair_checks=social_repairs,
                full_social_optimum=str(full_opt), front_base_optimum=str(front_base_opt))


def new_approximate_point():
    g = Game([1, 1, 1])
    for i, costs in enumerate(((3, 1), (1, 1), (1, 1))):
        for bit, cost in enumerate(costs):
            g.resource([cost], [(i, bit)])
    s = (0, 0, 0)
    assert g.costs(s)[0] > 2 * g.costs(flip(s, 0))[0]
    add_clocks(g, [(0, 1, 2)], [Q(20)], [3])
    assert Q(20) > 2 * (Q(3) + Q(160, 27))
    assert g.stable(s, Q(2))
    return dict(state=s, alpha=2, current=list(map(str, g.costs(s))),
                deviating=[str(g.costs(flip(s, i))[i]) for i in range(3)])


def individual_and_fairness_nonconstancy():
    g = Game([1, 1, 1])
    add_clocks(g, [(0, 1, 2)], [Q(27)], [3])
    s, t = (0, 0, 0), (1, 0, 0)
    assert front(s) and front(t)
    a, b = g.costs(s), g.costs(t)
    assert a == (Q(8), Q(1), Q(8)) and b == (Q(8), Q(8), Q(1))
    assert sum(a) == sum(b) == Q(17)
    assert sum(q * x for q, x in zip((1, 2, 1), a)) == 18
    assert sum(q * x for q, x in zip((1, 2, 1), b)) == 25
    return dict(states=[s, t], individual_costs=[list(map(str, a)), list(map(str, b))],
                class_uniform_social=17, nonuniform_social=[18, 25])


def social_optimum_need_not_be_front():
    # Three original players, then three mandatory users of weight 3.
    g = Game([1, 1, 1, 3, 3, 3])
    cheap = (0, 1, 0)
    for i in range(3):
        g.monomial(10, Q(1, 4 ** 10),
                   [(i, 1 - cheap[i]), (i + 3, 0), (i + 3, 1)])
        # Distinct legal actions for the mandatory users, with identical costs.
        for bit in (0, 1):
            g.resource([0], [(i + 3, bit)])
    base = {s: g.social(s) for s in g.states()}
    add_clocks(g, [(0, 1, 2)], [Q(6, 5)], [6])
    u, z = Q(6, 5) * Q(2, 3) ** 6, Q(6, 5) * Q(1, 3) ** 6
    assert Q(6, 5) > 1 + u
    states = g.states()
    s = (0, 1, 0, 0, 0, 0)
    t = flip(s, 1)
    assert g.costs(s)[1] > g.costs(t)[1]
    assert g.social(t) > g.social(s)
    optimum = min(map(g.social, states))
    front_optimum = min(g.social(x) for x in states if front(x[:3]))
    assert optimum == g.social(s) < front_optimum
    assert all(not front(x[:3]) for x in states if g.social(x) == optimum)
    # Every front state has the same exact clock social cost, despite this failure.
    K = 2 * u + z
    assert all(g.social(x) - base[x] == K for x in states if front(x[:3]))
    return dict(RD_margin=str(Q(6, 5) - 1 - u), gate_degree=6, base_degree=10,
                nonfront_state=s, repair_state=t,
                mover_before=str(g.costs(s)[1]), mover_after=str(g.costs(t)[1]),
                full_social_optimum=str(optimum), best_front_social=str(front_optimum),
                repair_social=str(g.social(t)), front_gate_constant=str(K),
                optimum_approximately=float(optimum), front_approximately=float(front_optimum))


def baseline_changes_approximation():
    alpha = Q(2)
    old, new, b = Q(3), Q(1), Q(1)
    assert old > alpha * new
    assert old + b <= alpha * (new + b)
    return dict(alpha=2, before=[str(old), str(new)],
                after=[str(old + b), str(new + b)],
                margin_shift=str(-(alpha - 1) * b))


def total_cost_insertion_bound():
    checks = 0
    for degree in range(11):
        for old in (Q(0), Q(1, 3), Q(1), Q(3), Q(10)):
            for weight in (Q(1, 5), Q(1), Q(7, 2)):
                new = old + weight
                difference = new ** (degree + 1) - old ** (degree + 1)
                assert weight * new ** degree <= difference
                assert difference <= (degree + 1) * weight * new ** degree
                checks += 1
    return dict(exact_checks=checks, degrees=list(range(11)))


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    report = dict(
        status="all exact assertions passed",
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        geometry=geometry_check(),
        transfer=[transfer_case(sizes, a) for sizes in
                  ((1,), (2,), (3,), (4,), (5,), (3, 2), (3, 3))
                  for a in (Q(1), Q(3, 2), Q(2))],
        added_approximate_state=new_approximate_point(),
        individual_nonconstancy=individual_and_fairness_nonconstancy(),
        global_optimum_boundary=social_optimum_need_not_be_front(),
        base_background=baseline_changes_approximation(),
        social_insertion_bound=total_cost_insertion_bound(),
    )
    path = args.output
    with path.open("x") as out:
        json.dump(report, out, indent=2, ensure_ascii=False)
        out.write("\n")
    print(json.dumps({"output": str(path), "status": report["status"],
                      "geometry": report["geometry"],
                      "transfer_cases": len(report["transfer"]),
                      "global_optimum_boundary": report["global_optimum_boundary"]},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
