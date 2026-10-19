"""Finite, full-job exact audits for the informed three-value scope review.

Times are stored in units of 1/ell, so all optimization uses integers.
The general proof remains in the accompanying Markdown review.
"""
from fractions import Fraction
from itertools import combinations, product
import json
import hashlib
import platform
from pathlib import Path


def maximum_3dm(q, triples):
    for size in range(min(q, len(triples)), -1, -1):
        for chosen in combinations(triples, size):
            if all(len({a[d] for a in chosen}) == size for d in range(3)):
                return size
    raise AssertionError("empty matching must exist")


def maximum_h_matching(q, triples):
    adjacent = [set() for _ in range(q)]
    for x, y, z in triples:
        adjacent[x].add(("B", y))
        adjacent[x].add(("C", z))
    owner = {}

    def augment(x, seen):
        for u in sorted(adjacent[x]):
            if u in seen:
                continue
            seen.add(u)
            if u not in owner or augment(owner[u], seen):
                owner[u] = x
                return True
        return False

    return sum(augment(x, set()) for x in range(q))


def full_matrix(q, triples, ell):
    machine_names = [("S", a) for a in range(len(triples))]
    machine_names += [("B", y) for y in range(q)]
    machine_names += [("C", z) for z in range(q)]
    machine_names += [("D", x, t) for x in range(q) for t in range(ell-2)]
    machine_names += [("idle",)]
    index = {name: pos for pos, name in enumerate(machine_names)}
    jobs = []
    for x in range(q):
        eligible = [(index[("S", a)], ell)
                    for a, triple in enumerate(triples) if triple[0] == x]
        assert eligible
        jobs.append((f"selector:{x}", eligible))
    for a, (x, y, z) in enumerate(triples):
        resources = [("B", y), ("C", z)]
        resources += [("D", x, t) for t in range(ell-2)]
        assert len(resources) == ell
        for t, resource in enumerate(resources):
            jobs.append((f"leaf:{a}:{t}",
                         [(index[("S", a)], 1), (index[resource], ell)]))
    return machine_names, jobs


def optimum_by_all_assignments(q, triples, ell):
    machine_names, jobs = full_matrix(q, triples, ell)
    best = None
    best_assignment = None
    assignments = 0
    for selected in product(*(eligible for _, eligible in jobs)):
        loads = [0]*len(machine_names)
        for machine, duration in selected:
            loads[machine] += duration
        value = max(loads, default=0)
        assignments += 1
        if best is None or value < best:
            best = value
            best_assignment = [machine_names[machine] for machine, _ in selected]
    assert best is not None and len(best_assignment) == len(jobs)
    return Fraction(best, ell), assignments, len(jobs), len(machine_names)


def main():
    sources = [
        ("perfect", 2, [(0, 0, 0), (1, 1, 1)]),
        ("parity_middle", 2,
         [(x, y, x ^ y) for x in range(2) for y in range(2)]),
        ("nonisolated_h_deficiency", 4,
         [(0, 0, 0), (1, 0, 0), (2, 0, 0),
          (3, 1, 1), (3, 2, 2), (3, 3, 3)]),
    ]
    records = []
    for name, q, triples in sources:
        assert all({a[d] for a in triples} == set(range(q)) for d in range(3))
        nu = maximum_3dm(q, triples)
        mu = maximum_h_matching(q, triples)
        for ell in (2, 3):
            expected = (Fraction(1) if nu == q else
                        Fraction(ell+1, ell) if mu == q else
                        Fraction(ell+2, ell))
            actual, count, jobs, machines = optimum_by_all_assignments(q, triples, ell)
            assert actual == expected
            records.append({"source": name, "q": q, "ell": ell,
                            "nu": nu, "mu": mu, "jobs": jobs,
                            "machines": machines,
                            "complete_assignments_enumerated": count,
                            "actual_optimum": str(actual),
                            "classification_value": str(expected)})
    print(json.dumps({"source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      "python_version": platform.python_version(),
                      "arithmetic": "integers in units 1/ell, fractions.Fraction only for reporting",
                      "command": "python3 tests/audits/unrelated_machines/selector_tiny_root_three_values_audit.py",
                      "scope": "Six finite complete ordinary-UM matrices; all original jobs retained",
                      "status": "PASS", "records": records}, indent=2))


if __name__ == "__main__":
    main()
