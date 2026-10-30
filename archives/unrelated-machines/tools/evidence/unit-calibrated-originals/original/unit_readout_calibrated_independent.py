#!/usr/bin/env python3
"""Independent exact audit of the no-pins unitforest cardinality LP.

Only finite explicit instances are tested. The accompanying proof establishes
the quantified claims; this executable does not call an LP solver.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import random

VERSION = "unitforest-independent-cardinality-slots-v2"
SEED = 430691


def ceil(x):
    return -(-x.numerator // x.denominator)


def enc(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): enc(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [enc(v) for v in x]
    return x


class Forest:
    def __init__(self, k, h, variables, leaf_clause, capacities):
        assert k >= 1 and h >= 1 and variables >= 0
        self.k, self.h, self.variables = k, h, variables
        self.leaf_clause = dict(leaf_clause)
        self.capacities = tuple(capacities)
        assert all(isinstance(a, int) and a >= 0 for a in capacities)
        self.internals = []
        self.children = {}
        self.parent = {}
        self.child = {}
        self.outgoing = {}
        self.incoming = {}
        self.jobs = []
        self.selectors = []
        for v in range(variables):
            sj = ("S", v)
            self.selectors.append(sj)
            self.jobs.append(sj)
            for sign in (0, 1):
                for depth in range(h):
                    for path in product(range(k), repeat=depth):
                        m = (v, sign, path)
                        self.internals.append(m)
                        self.incoming[m] = sj if depth == 0 else ("P", v, sign, path)
                        self.outgoing[m] = []
                        for a in range(k):
                            cp = path + (a,)
                            job = ("P", v, sign, cp)
                            self.jobs.append(job)
                            self.parent[job] = m
                            if depth + 1 < h:
                                self.child[job] = (v, sign, cp)
                            else:
                                c = self.leaf_clause[(v, sign, cp)]
                                assert 0 <= c < len(capacities)
                                self.child[job] = ("C", c)
                            self.outgoing[m].append(job)
        assert len(set(self.jobs)) == len(self.jobs)
        self.leaves = [j for j in self.jobs if j[0] == "P" and len(j[3]) == h]
        self.degree = Counter(self.child[j][1] for j in self.leaves)

    def validate_lp(self, r, roots, down):
        assert 1 <= r <= self.k
        for v in range(self.variables):
            assert roots[v, 0] + roots[v, 1] == 1
        assert all(0 <= x <= 1 for x in roots.values())
        assert all(0 <= x <= 1 for x in down.values())
        assert set(down) == set(self.parent)
        for m in self.internals:
            inc = roots[m[0], m[1]] if not m[2] else down[self.incoming[m]]
            assert sum((down[j] for j in self.outgoing[m]), F(0)) >= r - 1 + inc
        usage = Counter()
        for j in self.leaves:
            usage[self.child[j][1]] += down[j]
        assert all(usage[c] <= a for c, a in enumerate(self.capacities))

    def actual(self, assignment):
        assert set(assignment) == set(self.jobs)
        loads = defaultdict(F)
        for j, m in assignment.items():
            if j[0] == "S":
                assert m in ((j[1], 0, ()), (j[1], 1, ()))
                p = F(1)
            elif m == self.parent[j]:
                p = F(1, self.k)
            elif len(j[3]) < self.h:
                assert m == self.child[j]
                p = F(1)
            else:
                c = self.child[j][1]
                assert m[0:2] == ("C", c)
                assert 0 <= m[2] < self.capacities[c]
                p = F(1)
            loads[m] += p
        maximum = max(loads.values(), default=F(0))
        unit_max = max((x for m, x in loads.items() if m[0] == "C"), default=F(0))
        return maximum, unit_max, loads


def matching(adjacency):
    """Deterministic augmenting-path matching, indexed by the supplied lists."""
    js, ss = {}, {}
    for start in adjacency:
        seen = {start}
        predecessor = {}
        queue = deque([start])
        free = None
        while queue and free is None:
            j = queue.popleft()
            for slot in adjacency[j]:
                if slot in predecessor:
                    continue
                predecessor[slot] = j
                if slot not in ss:
                    free = slot
                    break
                nxt = ss[slot]
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
        if free is None:
            return None
        slot = free
        while True:
            j = predecessor[slot]
            old = js.get(j)
            js[j], ss[slot] = slot, j
            if old is None:
                break
            slot = old
    assert len(js) == len(adjacency)
    return js


def slots_for_row(row, pieces, adjacency):
    """Split arbitrary exact rational masses at integer slot boundaries."""
    position = F(0)
    for job, mass in pieces:
        assert 0 <= mass <= 1
        while mass:
            index = position.numerator // position.denominator
            amount = min(mass, index + 1 - position)
            slot = (row, index)
            if slot not in adjacency[job]:
                adjacency[job].append(slot)
            mass -= amount
            position += amount
    return ceil(position)


def round_lp(forest, r, roots, down):
    forest.validate_lp(r, roots, down)
    adjacency = {j: [] for j in forest.jobs}
    bound = forest.k - r + 1
    rowsizes = {}
    for m in forest.internals:
        incoming = forest.incoming[m]
        mass = roots[m[0], m[1]] if not m[2] else down[incoming]
        pieces = [(incoming, mass)]
        pieces.extend((j, 1 - down[j]) for j in forest.outgoing[m])
        count = slots_for_row(m, pieces, adjacency)
        assert count <= bound
        rowsizes[m] = count
    for c, capacity in enumerate(forest.capacities):
        pieces = [(j, down[j]) for j in forest.leaves if forest.child[j][1] == c]
        count = slots_for_row(("C", c), pieces, adjacency)
        assert count <= capacity
        rowsizes["C", c] = count
    matched = matching(adjacency)
    assert matched is not None
    assignment = {}
    for j, (row, index) in matched.items():
        assignment[j] = ("C", row[1], index) if row[0] == "C" else row
    maximum, unit_max, loads = forest.actual(assignment)
    assert maximum <= F(2 * forest.k - r, forest.k)
    assert unit_max <= 1
    return assignment, maximum, rowsizes, loads


def generated_lp(k, h, variables, clause_count, r, rng, irregular=True, denominator=11):
    leaves = {}
    for v in range(variables):
        for sign in (0, 1):
            for p in product(range(k), repeat=h):
                leaves[v, sign, p] = rng.randrange(clause_count)
    roots, down = {}, {}
    for v in range(variables):
        q = F(rng.randrange(denominator + 1), denominator) if irregular else F(1, 2)
        roots[v, 0], roots[v, 1] = q, 1 - q
        for sign in (0, 1):
            for depth in range(h):
                for p in product(range(k), repeat=depth):
                    incoming = roots[v, sign] if depth == 0 else down["P", v, sign, p]
                    base = F(r - 1 + incoming, k)
                    for a in range(k):
                        alpha = F(rng.randrange(6), 5) if irregular else F(0)
                        down["P", v, sign, p + (a,)] = base + (1 - base) * alpha
    usage = Counter()
    for (v, sign, p), c in leaves.items():
        usage[c] += down["P", v, sign, p]
    capacities = [ceil(usage[c]) for c in range(clause_count)]
    return Forest(k, h, variables, leaves, capacities), roots, down


def root_profile(forest, r, bits):
    roots = {(v, s): F(bits[v] == s) for v in range(forest.variables) for s in (0, 1)}
    down = {}
    for m in forest.internals:
        q = roots[m[0], m[1]] if not m[2] else down[forest.incoming[m]]
        for j in forest.outgoing[m]:
            down[j] = F(r - 1 + q, forest.k)
    return roots, down


def all_parent(forest):
    assignment = {j: forest.parent[j] for j in forest.parent}
    assignment.update({j: (j[1], 0, ()) for j in forest.selectors})
    assert forest.actual(assignment)[0] == (2 if forest.variables else 0)
    return assignment


def one_path_matching(forest):
    """Return actual paths, or None when the necessary capacity matching fails."""
    representatives = {}
    for (v, sign, p), c in forest.leaf_clause.items():
        representatives.setdefault((v, c), (sign, p))
    adjacency = {}
    for v in range(forest.variables):
        adjacency[v] = [(c, i) for c, a in enumerate(forest.capacities)
                        if (v, c) in representatives for i in range(min(a, forest.variables))]
    mat = matching(adjacency)
    if mat is None:
        return None
    assignment = {j: forest.parent[j] for j in forest.parent}
    for v, (c, unit) in mat.items():
        sign, path = representatives[v, c]
        assignment["S", v] = (v, sign, ())
        for depth in range(1, forest.h + 1):
            job = ("P", v, sign, path[:depth])
            assignment[job] = forest.child[job] if depth < forest.h else ("C", c, unit)
    maximum, unit_max, _ = forest.actual(assignment)
    assert maximum <= 2 - F(1, forest.k) and unit_max <= 1
    return assignment


def audit():
    rng = random.Random(SEED)
    counts = Counter()
    observed = set()
    for k in range(1, 6):
        for h in range(1, 4):
            for r in range(1, k + 1):
                for irregular in (False, True):
                    f, roots, down = generated_lp(k, h, 2, 5, r, rng, irregular)
                    _, maximum, _, _ = round_lp(f, r, roots, down)
                    observed.add(str(maximum))
                    counts["feasible_lp_rounded"] += 1
    # Empty variables/zero-capacity clauses and a genuinely giant denominator.
    empty = Forest(1, 1, 0, {}, [0, 0])
    round_lp(empty, 1, {}, {})
    counts["empty_lp_rounded"] += 1
    huge = 2**521 + 39
    f, roots, down = generated_lp(3, 2, 2, 4, 2, rng, True, huge)
    round_lp(f, 2, roots, down)
    counts["giant_denominator_lp_rounded"] += 1
    # Independently check actual C=1 witnesses and the density-conditional profile.
    for k in range(2, 5):
        for h in (1, 2):
            for r in range(1, k + 1):
                a = F(r - 1, k - 1)
                for rep in range(5):
                    f0, _, _ = generated_lp(k, h, 2, 4, r, rng, False)
                    caps = [max(ceil(a * f0.degree[c]), rng.randrange(5)) for c in range(4)]
                    f = Forest(k, h, 2, f0.leaf_clause, caps)
                    for bits in product((0, 1), repeat=2):
                        q = Counter(c for (v, s, _), c in f.leaf_clause.items() if bits[v] == s)
                        if any(q[c] > caps[c] for c in range(4)):
                            continue
                        roots, down = root_profile(f, r, bits)
                        f.validate_lp(r, roots, down)
                        # The forced subtree schedule is an actual C=1 witness.
                        ass = {j: f.parent[j] for j in f.parent}
                        ass.update({("S", v): (v, bits[v], ()) for v in range(2)})
                        leafunit = Counter()
                        for j in f.parent:
                            if j[2] != bits[j[1]]:
                                continue
                            if len(j[3]) < h:
                                ass[j] = f.child[j]
                            else:
                                c = f.child[j][1]
                                ass[j] = ("C", c, leafunit[c])
                                leafunit[c] += 1
                        assert f.actual(ass)[0] == 1
                        counts["actual_one_density_profiles"] += 1
    bounded_records = []
    for D in (F(2), F(5, 2), F(3), F(7, 2), F(5), F(10)):
        for k in range(1, 9):
            for h in (1, 2):
                for rep in range(3):
                    variables, clauses = 3, 4
                    leaves = {(v, s, p): rng.randrange(clauses)
                              for v in range(variables) for s in (0, 1)
                              for p in product(range(k), repeat=h)}
                    degrees = Counter(leaves.values())
                    caps = [ceil(F(degrees[c], 1) / D) for c in range(clauses)]
                    f = Forest(k, h, variables, leaves, caps)
                    assert all(f.degree[c] <= D * caps[c] for c in range(clauses))
                    if k >= D:
                        r = 1 + ((F(k - 1) / (2 * D)).numerator // (F(k - 1) / (2 * D)).denominator)
                        assert F(r, k) >= 1 / (4 * D)
                        roots = {(v, s): F(1, 2) for v in range(variables) for s in (0, 1)}
                        down = {}
                        for m in f.internals:
                            inc = roots[m[0], m[1]] if not m[2] else down[f.incoming[m]]
                            for j in f.outgoing[m]:
                                down[j] = F(r - 1 + inc, k)
                        _, maximum, _, _ = round_lp(f, r, roots, down)
                        assert maximum <= 2 - 1 / (4 * D)
                        result = "uniform_lp"
                    else:
                        ass = one_path_matching(f)
                        if ass is None:
                            ass = all_parent(f)
                            maximum = f.actual(ass)[0]
                            result = "matching_failure_exact_two"
                        else:
                            maximum = f.actual(ass)[0]
                            assert maximum < 2 - 1 / D
                            result = "one_path_matching"
                    counts[result] += 1
                    if len(bounded_records) < 8 or result == "matching_failure_exact_two":
                        bounded_records.append({"D": D, "k": k, "h": h,
                                                "result": result, "actual_C": maximum})
    # Deliberate exact-two obstruction: every variable sees only one unit.
    f = Forest(1, 1, 3, {(v, s, (0,)): 0 for v in range(3) for s in (0, 1)}, [1])
    assert f.degree[0] <= 10 * f.capacities[0]
    assert one_path_matching(f) is None
    assert f.actual(all_parent(f))[0] == 2
    counts["deliberate_matching_obstruction"] += 1
    # Exact counterexample to unconditional necessity of the strengthened LP.
    negative = Forest(2, 1, 1,
                      {(0, s, (a,)): 0 for s in (0, 1) for a in (0, 1)}, [2])
    ass = {j: negative.parent[j] for j in negative.parent}
    ass["S", 0] = (0, 0, ())
    ass["P", 0, 0, (0,)] = ("C", 0, 0)
    ass["P", 0, 0, (1,)] = ("C", 0, 1)
    assert negative.actual(ass)[0] == 1
    # For r=2, the two root rows imply total leaf-down >= 2(r-1)+1=3.
    assert 2 * (2 - 1) + 1 > negative.capacities[0]
    counts["unconditional_necessity_negative_control"] += 1
    return {"version": VERSION, "seed": SEED, "counts": dict(counts),
            "observed_rounded_makespans": sorted(observed, key=F),
            "giant_denominator_bit_length": huge.bit_length(),
            "bounded_D_sample": bounded_records,
            "limits": ["finite audits do not prove the general claims",
                       "no LP infeasibility oracle or physical-schedule enumeration was run",
                       "matching-failure OPT=2 uses the separate mandatory-path proof"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit()
    result["code_sha256"] = sha256(Path(__file__).read_bytes()).hexdigest()
    payload = json.dumps(enc(result), ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        if args.output.exists():
            raise FileExistsError("Refusing to overwrite frozen audit output")
        args.output.write_text(payload)
    print(payload, end="")


if __name__ == "__main__":
    main()
