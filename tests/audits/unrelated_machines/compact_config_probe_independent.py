#!/usr/bin/env python3
"""紧凑共享逃逸族的全单机配置延伸独立审计。

This module imports no other project audit/certificate implementation.  It
builds the actual sparse processing matrix, generates full configuration-LP
extensions, and checks them from that matrix using Fraction.  Every locally
legal machine configuration is enumerated for k=2.  Larger instances use
explicit, reproducible representative configurations, not complete enumeration.
The scalar recipe audit is separate from the expanded-certificate audit.
"""

from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations
import json
import platform
import random


class Compact:
    def __init__(self, k):
        assert k >= 2
        self.k, self.N = k, 2 * k * k
        self.G = self.N - 2 * k
        self.z = ("z",)
        self.V = [("V", a) for a in range(self.N)]
        self.global_machines = [("G", g) for g in range(self.G)]
        self.R = [[("R", a, ell) for ell in range(k + 1)] for a in range(self.N)]
        self.machines = self.V + self.global_machines + [v for row in self.R for v in row] + [self.z]
        self.p = {}
        for a in range(self.N):
            self.p[("X", a)] = {v: F(1) for v in [self.V[a]] + self.global_machines}
            for s in range(k):
                self.p[("Y", a, s)] = {v: F(1) for v in self.R[a]}
                self.p[("Y", a, s)][self.z] = F(1, k)
                self.p[("Z", a, s)] = {v: F(1) for v in self.R[a]}
                self.p[("Z", a, s)][self.V[a]] = F(1, k)
        self.by_machine = {v: [] for v in self.machines}
        for j, times in self.p.items():
            for v in times:
                self.by_machine[v].append(j)

    def legal(self, v, C):
        return len(set(C)) == len(C) and all(v in self.p[j] for j in C) and sum(self.p[j][v] for j in C) <= 1

    def configurations(self, v):
        # This is used exhaustively only for the k=2 fixture.
        jobs = self.by_machine[v]
        max_size = self.k if v[0] in ("V", "z") else 1
        for size in range(max_size + 1):
            for C in combinations(jobs, size):
                if self.legal(v, C):
                    yield C

    def extension(self, query, C):
        """The independent recipe uses uniform singleton routing on equal R/G.

        The common sink is a single deterministic configuration.  Each block's
        remaining unit-job marginals are spread uniformly over its unpinned R
        machines; their total, not a counting relaxation, is checked <= capacity.
        """
        assert self.legal(query, C)
        C = tuple(sorted(C))
        k, N, G = self.k, self.N, self.G
        alpha = [F(1, k)] * N
        pinned_V = {}
        escaped = set()

        def other(a):
            return 1 if a == 0 else 0

        def escape(a, count):
            assert 0 <= count <= k
            escaped.update(("Y", a, s) for s in range(count))

        if query[0] == "V":
            a = query[1]
            pinned_V[a] = C
            if C == (("X", a),):
                alpha[a] = F(1)
                for b in range(N):
                    if b != a:
                        alpha[b] = F(2 * k - 1, N - 1)
                escape(a, k - 1)
            else:
                assert all(j[0] == "Z" for j in C)
                alpha[a] = F(0)
                b = other(a)
                alpha[b] = F(2, k)
                escape(a, max(k - len(C) - 1, 0))
                escape(b, 1)
        elif query[0] == "G":
            if not C:
                for a in range(k):
                    alpha[a] = F(2, k)
                    escape(a, 1)
            else:
                a = C[0][1]
                alpha[a] = F(0)
                b = other(a)
                alpha[b] = F(2, k)
                escape(b, 1)
        elif query[0] == "R":
            a = query[1]
            alpha[a] = F(0)
            b = other(a)
            alpha[b] = F(2, k)
            escape(b, 1)
            if C and C[0][0] == "Z":
                pinned_V[a] = tuple(("Z", a, s) for s in range(k) if ("Z", a, s) != C[0])
        else:
            assert query == self.z
            escaped.update(C)
        assert len(escaped) <= k
        assert all(0 <= a <= 1 for a in alpha)

        y = {}

        def put(v, configurations):
            merged = defaultdict(F)
            for jobs, weight in configurations:
                if weight:
                    merged[tuple(sorted(jobs))] += weight
            y[v] = dict(merged)

        for a, v in enumerate(self.V):
            if a in pinned_V:
                put(v, [(pinned_V[a], F(1))])
            else:
                put(v, [((("X", a),), alpha[a]), (tuple(("Z", a, s) for s in range(k)), 1 - alpha[a])])

        def marginal(v, j):
            return sum((weight for jobs, weight in y[v].items() if j in jobs), F(0))

        global_demands = {("X", a): 1 - marginal(self.V[a], ("X", a)) for a in range(N)}
        available_global = self.global_machines[:]
        if query[0] == "G":
            available_global.remove(query)
            put(query, [(C, F(1))])
            if C:
                assert global_demands[C[0]] == 1
                global_demands[C[0]] = F(0)
        global_total = sum(global_demands.values())
        assert global_total <= len(available_global)
        assert available_global
        for v in available_global:
            q = len(available_global)
            put(v, [((j,), demand / q) for j, demand in global_demands.items()] + [((), 1 - global_total / q)])

        for a in range(N):
            demands = {("Y", a, s): F(("Y", a, s) not in escaped) for s in range(k)}
            demands.update({("Z", a, s): 1 - marginal(self.V[a], ("Z", a, s)) for s in range(k)})
            available = self.R[a][:]
            if query[0] == "R" and query[1] == a:
                available.remove(query)
                put(query, [(C, F(1))])
                if C:
                    assert demands[C[0]] == 1
                    demands[C[0]] = F(0)
            total = sum(demands.values())
            assert total <= len(available)
            assert all(0 <= x <= 1 for x in demands.values())
            q = len(available)
            for v in available:
                put(v, [((j,), demand / q) for j, demand in demands.items()] + [((), 1 - total / q)])
        put(self.z, [(escaped, F(1))])
        return y

    def verify(self, y, query, C):
        assert set(y) == set(self.machines)
        cover = {j: F(0) for j in self.p}
        maximum_weight_bits = 0
        for v, cfg in y.items():
            assert sum(cfg.values()) == 1
            for jobs, weight in cfg.items():
                assert weight >= 0 and self.legal(v, jobs)
                maximum_weight_bits = max(maximum_weight_bits, weight.numerator.bit_length(), weight.denominator.bit_length())
                for j in jobs:
                    cover[j] += weight
        assert all(x == 1 for x in cover.values())
        assert y[query].get(tuple(sorted(C)), F(0)) == 1
        return maximum_weight_bits


def scalar_audit():
    count = 0
    for k in range(2, 129):
        N, G = 2 * k * k, 2 * k * k - 2 * k
        assert G - 1 >= 1
        normal = F(1, k)
        alpha_x_other = F(2 * k - 1, N - 1)
        assert 0 <= alpha_x_other < normal
        assert 1 + (N - 1) * alpha_x_other == 2 * k
        assert F(2, k) + (N - 2) * normal == 2 * k
        assert k * F(2, k) + (N - k) * normal == 2 * k + 1
        for retained_Z in range(k + 1):
            d = k - retained_Z
            escapes = max(d - 1, 0)
            assert k + d - escapes <= k + 1
            assert escapes + 1 <= k
        theta = 2 - F(1, k)
        assert F(2 * k, k) == 2 > theta
        assert theta + F(1, k) == 2
        count += 1
    return {"k_range": [2, 128], "cases": count, "arithmetic": "Fraction", "full_instance_enumeration": False}


def exhaustive_k2():
    instance = Compact(2)
    counts = defaultdict(int)
    max_bits = 0
    for v in instance.machines:
        for C in instance.configurations(v):
            max_bits = max(max_bits, instance.verify(instance.extension(v, C), v, C))
            counts[v[0]] += 1
    return {
        "k": 2,
        "machines": len(instance.machines),
        "jobs": len(instance.p),
        "configurations_by_machine_type": dict(counts),
        "total_configurations": sum(counts.values()),
        "all_machine_configurations_enumerated": True,
        "all_complete_extensions_verified": True,
        "maximum_checked_weight_bits": max_bits,
    }


def representative_audit():
    rng = random.Random(20261016)
    results = []
    for k in range(3, 9):
        instance = Compact(k)
        queries = []
        # Every subset at one V, including the empty and full configurations.
        for size in range(k + 1):
            queries += [(instance.V[0], C) for C in combinations([("Z", 0, s) for s in range(k)], size)]
        queries.append((instance.V[0], (("X", 0),)))
        queries += [(instance.global_machines[0], ()), (instance.global_machines[0], (("X", 0),))]
        queries += [(instance.R[0][0], ()), (instance.R[0][0], (("Y", 0, 0),)), (instance.R[0][0], (("Z", 0, 0),))]
        Ys = [j for j in instance.p if j[0] == "Y"]
        for size in range(k + 1):
            queries.append((instance.z, tuple(rng.sample(Ys, size))))
        max_bits = 0
        for v, C in queries:
            max_bits = max(max_bits, instance.verify(instance.extension(v, C), v, C))
        results.append({"k": k, "queries": len(queries), "maximum_checked_weight_bits": max_bits})
    return {"seed": 20261016, "runs": results, "all_expanded_machine_configurations_enumerated": False}


def main():
    print(json.dumps({
        "title": "紧凑共享逃逸族的完整单机配置延伸独立审计",
        "python": platform.python_version(),
        "arithmetic": "fractions.Fraction; exact; no numerical tolerance",
        "imports_project_certificate_generators": False,
        "scalar": scalar_audit(),
        "exhaustive": exhaustive_k2(),
        "representative": representative_audit(),
        "limitation": "Finite checks do not replace the general extension proof. No approximation algorithm or consistent joint/SA distribution is certified.",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
