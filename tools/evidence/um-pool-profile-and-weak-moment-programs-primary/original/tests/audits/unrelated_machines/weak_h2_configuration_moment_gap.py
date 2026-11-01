#!/usr/bin/env python3
"""Small exact checks for moment_bridge.md; no scheduling enumeration.

Checks generic multislice full M2 for (n,m)=(4,3),(5,3), and a
k=2,b=2 global H2 fixture through M1, every load localizer, one-hot tests
through degree two, shared CONFIG marginals, and the strong-contract pair
objection. The mixed global M2 is proved by tensor/mixing, not numerically
checked here. All arithmetic is rational/integer.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
from math import lcm
import json


def falling(x, q):
    out = F(1)
    for h in range(q):
        out *= x - h
    return out


def canonical(ends):
    d = {}
    for j, a in ends:
        if j in d and d[j] != a:
            return None
        d[j] = a
    return tuple(sorted(d.items()))


def monomials(domains, degree):
    result = [()]
    jobs = sorted(domains)
    for q in range(1, degree + 1):
        for js in combinations(jobs, q):
            for choices in product(*(domains[j] for j in js)):
                result.append(tuple(zip(js, choices)))
    return result


def psd_rank(matrix):
    """Exact symmetric Bareiss congruence, with zero-pivot safety."""
    size = len(matrix)
    denominator = 1
    for row in matrix:
        for x in row:
            denominator = lcm(denominator, x.denominator)
    a = [[int(x * denominator) for x in row] for row in matrix]
    previous = 1
    rank = 0
    for k in range(size):
        assert all(a[i][i] >= 0 for i in range(k, size)), "negative pivot"
        candidates = [i for i in range(k, size) if a[i][i] > 0]
        if not candidates:
            assert all(a[i][j] == 0 for i in range(k, size)
                       for j in range(k, size)), "nonzero zero-diagonal block"
            break
        pindex = candidates[0]
        if pindex != k:
            a[k], a[pindex] = a[pindex], a[k]
            for row in a:
                row[k], row[pindex] = row[pindex], row[k]
        pivot = a[k][k]
        for i in range(k + 1, size):
            for j in range(i, size):
                numerator = pivot * a[i][j] - a[i][k] * a[k][j]
                value, remainder = divmod(numerator, previous)
                assert remainder == 0, "Bareiss division not exact"
                a[i][j] = a[j][i] = value
        for i in range(k + 1, size):
            a[i][k] = a[k][i] = 0
        previous = pivot
        rank += 1
    return rank


def multislice(n, m):
    t = F(n, m)

    @lru_cache(None)
    def mu(ends):
        s = canonical(ends)
        if s is None:
            return F(0)
        counts = [0] * m
        for _, a in s:
            counts[a] += 1
        answer = F(1)
        for count in counts:
            answer *= falling(t, count)
        return answer / falling(n, len(s))

    return mu


def generic_check(n, m):
    domains = {j: list(range(m)) for j in range(n)}
    mu = multislice(n, m)
    mons2 = monomials(domains, 2)
    matrix = [[mu(s + u) for u in mons2] for s in mons2]
    rank = psd_rank(matrix)
    one_hot_tests = row_tests = 0
    t = F(n, m)
    for s in monomials(domains, 3):
        for j in range(n):
            assert sum((mu(s + ((j, a),)) for a in range(m)), F(0)) == mu(s)
            one_hot_tests += 1
        for a in range(m):
            assert sum((mu(s + ((j, a),)) for j in range(n)), F(0)) == t * mu(s)
            row_tests += 1
    return {"n": n, "m": m, "M2_dimension": len(matrix), "M2_rank": rank,
            "one_hot_tests_degree_le_3": one_hot_tests,
            "row_identity_tests_degree_le_3": row_tests}


def mixed_fixture(k=2, b=2):
    r = b + 1
    n = b + k
    t = F(n, r)
    machines = []
    for a in range(k):
        machines.append(("V", a))
    for g in range(k - 1):
        machines.append(("G", g))
    for a in range(k):
        for ell in range(r):
            machines.append(("R", a, ell))
    jobs = []
    types = {}
    for a in range(k):
        for typ, count in (("X", 1), ("Y", b), ("Z", k)):
            for h in range(count):
                j = len(jobs)
                jobs.append(j)
                types[j] = (typ, a, h)
    domains, p = {}, {}
    for j, (typ, a, _) in types.items():
        if typ == "X":
            domains[j] = [("V", a)] + [("G", g) for g in range(k - 1)]
        elif typ == "Y":
            domains[j] = [("R", a, ell) for ell in range(r)]
        else:
            domains[j] = [("V", a)] + [("R", a, ell) for ell in range(r)]
        for machine in domains[j]:
            p[(j, machine)] = F(1, k) if typ == "Z" and machine[0] == "V" else F(1)

    @lru_cache(None)
    def conditional(active, ends):
        s = canonical(ends)
        if s is None:
            return F(0)
        g_values = []
        true_r = {a: [] for a in range(k) if a != active}
        active_counts = [0] * r
        active_q = 0
        for j, machine in s:
            typ, a, _ = types[j]
            if typ == "X":
                if a == active:
                    if machine != ("V", a):
                        return F(0)
                else:
                    if machine[0] != "G":
                        return F(0)
                    g_values.append(machine[1])
            elif typ == "Z" and a != active:
                if machine != ("V", a):
                    return F(0)
            elif a == active:
                if machine[:2] != ("R", a):
                    return F(0)
                active_counts[machine[2]] += 1
                active_q += 1
            else:
                assert typ == "Y" and machine[:2] == ("R", a)
                true_r[a].append(machine[2])
        if len(set(g_values)) != len(g_values) or len(g_values) > k - 1:
            return F(0)
        answer = F(1) / falling(k - 1, len(g_values))
        for values in true_r.values():
            if len(set(values)) != len(values):
                return F(0)
            answer /= falling(r, len(values))
        for count in active_counts:
            answer *= falling(t, count)
        answer /= falling(n, active_q)
        return answer

    @lru_cache(None)
    def moment(ends):
        return sum((conditional(a, ends) for a in range(k)), F(0)) / k

    edges = [(j, machine) for j in jobs for machine in domains[j]]
    mons1 = [()] + [(e,) for e in edges]
    m1 = [[moment(s + u) for u in mons1] for s in mons1]
    m1rank = psd_rank(m1)
    onehot = 0
    for s in monomials(domains, 2):
        for j in jobs:
            assert sum((moment(s + ((j, a),)) for a in domains[j]), F(0)) == moment(s)
            onehot += 1
    localizers = []
    for machine in machines:
        row_edges = [e for e in edges if e[1] == machine]
        matrix = [[t * moment(s + u) - sum(
            (p[e] * moment(s + u + (e,)) for e in row_edges), F(0))
                   for u in mons1] for s in mons1]
        localizers.append({"machine": str(machine), "rank": psd_rank(matrix)})

    configs = {machine: [] for machine in machines}
    for machine in machines:
        if machine[0] == "V":
            a = machine[1]
            xjob = next(j for j in jobs if types[j][:2] == ("X", a))
            zjobs = tuple(j for j in jobs if types[j][:2] == ("Z", a))
            configs[machine] = [((xjob,), F(1, k)), (zjobs, F(k - 1, k))]
        elif machine[0] == "G":
            configs[machine] = [((j,), F(1, k)) for j in jobs if types[j][0] == "X"]
        else:
            a = machine[1]
            configs[machine] = [((j,), F(1, r)) for j in jobs
                                if types[j][:2] == ("Y", a)]
            configs[machine] += [((j,), F(1, k * r)) for j in jobs
                                 if types[j][:2] == ("Z", a)]
        assert sum((w for _, w in configs[machine]), F(0)) == 1
        for js, weight in configs[machine]:
            assert weight >= 0
            assert sum((p[(j, machine)] for j in js), F(0)) <= 1 <= t
    for e in edges:
        j, machine = e
        marginal = sum((w for js, w in configs[machine] if j in js), F(0))
        assert marginal == moment((e,))
    yjobs = [j for j in jobs if types[j][:2] == ("Y", 0)]
    zjob = next(j for j in jobs if types[j][:2] == ("Z", 0))
    resource = ("R", 0, 0)
    pair = moment(((yjobs[0], resource), (yjobs[1], resource)))
    triple = moment(((yjobs[0], resource), (yjobs[1], resource), (zjob, resource)))
    assert pair > 0 and triple < 0
    assert pair == falling(t, 2) / falling(n, 2) / k
    assert triple == falling(t, 3) / falling(n, 3) / k
    return {"k": k, "b": b, "T": str(t), "jobs": len(jobs),
            "machines": len(machines), "edges": len(edges), "M1_rank": m1rank,
            "one_hot_tests_degree_le_2": onehot,
            "all_global_load_localizers_dimension": len(mons1),
            "localizer_PSD_ranks": localizers,
            "all_shared_CONFIG_edge_marginals_checked": len(edges),
            "positive_same_resource_pair": str(pair),
            "negative_same_resource_triple": str(triple),
            "mixed_global_M2_numerically_checked": False,
            "mixed_global_M2_proof": "tensor products of PSD components, then nonnegative average"}


if __name__ == "__main__":
    print(json.dumps({"generic_multislice": [generic_check(4, 3), generic_check(5, 3)],
                      "mixed_H2": mixed_fixture()}, ensure_ascii=False, indent=2))
