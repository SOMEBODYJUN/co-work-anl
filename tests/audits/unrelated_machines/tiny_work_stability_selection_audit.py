"""Independent finite audit of the new selector/root/ell-leaf matrix.

Only the four-tuple parity source at ell=2,3 is audited.  All 1,024 and
16,384 legal complete assignments are enumerated, respectively.  This does
not optimize over all CONFIG points or prove general NP completeness.
"""

from fractions import Fraction as F
from itertools import combinations, product
import json
import hashlib
import platform
from pathlib import Path


PARITY = ((0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0))


def build(ell):
    machines = [f"S{a}" for a in range(4)]
    resources = [f"B{v}" for v in range(2)] + [f"C{v}" for v in range(2)]
    resources += [f"D{x}_{h}" for x in range(2) for h in range(ell - 2)]
    machines += resources + ["idle"]
    jobs, selectors, leaves = {}, {}, {}
    for x in range(2):
        j = f"selector{x}"
        selectors[x] = j
        jobs[j] = [(f"S{a}", F(1)) for a, t in enumerate(PARITY) if t[0] == x]
    for a, (x, y, z) in enumerate(PARITY):
        rr = [f"B{y}", f"C{z}"] + [f"D{x}_{h}" for h in range(ell - 2)]
        leaves[a] = []
        for h, r in enumerate(rr):
            j = f"leaf{a}_{h}"
            jobs[j] = [(f"S{a}", F(1, ell)), (r, F(1))]
            leaves[a].append(j)
    return machines, resources, jobs, selectors, leaves


def source_values():
    nu = 0
    for k in range(5):
        for aa in combinations(range(4), k):
            if all(len({PARITY[a][c] for a in aa}) == k for c in range(3)):
                nu = max(nu, k)
    neighbors = {
        x: sorted({(kind, t[c]) for t in PARITY if t[0] == x
                   for kind, c in (("B", 1), ("C", 2))})
        for x in range(2)
    }
    best = []

    def visit(x, used, current):
        nonlocal best
        if x == 2:
            if len(current) > len(best):
                best = list(current)
            return
        for r in neighbors[x]:
            if r not in used:
                visit(x + 1, used | {r}, current + [(x, r)])
        visit(x + 1, used, current)

    visit(0, set(), [])
    return nu, len(best), best


def configuration_point(ell, machines, resources, jobs, selectors, leaves):
    y = {i: [] for i in machines}
    for a, t in enumerate(PARITY):
        y[f"S{a}"] = [(F(1, 2), (selectors[t[0]],)),
                       (F(1, 2), tuple(leaves[a]))]
    for a in range(4):
        for j in leaves[a]:
            r = jobs[j][1][0]
            y[r].append((F(1, 2), (j,)))
    y["idle"] = [(F(1), ())]
    return y


def verify_config(ell, machines, jobs, y):
    costs = {j: dict(ee) for j, ee in jobs.items()}
    cover = {j: F(0) for j in jobs}
    diff = {}
    all_columns = 0
    for i in machines:
        eligible = [j for j in jobs if i in costs[j]]
        legal = set()
        for k in range(len(eligible) + 1):
            for cc in combinations(eligible, k):
                if sum((costs[j][i] for j in cc), F(0)) <= 1:
                    legal.add(frozenset(cc))
        all_columns += len(legal)
        assert sum((w for w, _ in y[i]), F(0)) == 1
        values = []
        mean = F(0)
        for w, cc in y[i]:
            assert w > 0 and len(cc) == len(set(cc))
            assert frozenset(cc) in legal
            assert sum(costs[j][i] == 1 for j in cc) <= 1
            tiny = sum((costs[j][i] for j in cc if costs[j][i] == F(1, ell)), F(0))
            values.append(tiny)
            mean += w * tiny
            for j in cc:
                cover[j] += w
        diff[i] = mean - min(values)
    assert all(v == 1 for v in cover.values())
    assert all(diff[i] == F(1, 2) for i in machines if i.startswith("S"))
    assert all(diff[i] == 0 for i in machines if not i.startswith("S"))
    assert max(diff.values()) == F(1, 2)
    assert not all(v <= F(1, 3) for v in diff.values())
    return {"all_legal_CONFIG_columns": all_columns,
            "positive_certificate_columns": sum(len(row) for row in y.values()),
            "certificate_stability_max": str(max(diff.values())),
            "certificate_accepts_omega_half": True,
            "same_certificate_rejects_omega_one_third": True}


def loads(machines, jobs, assignment):
    out = {i: F(0) for i in machines}
    for j, i in assignment.items():
        ee = dict(jobs[j])
        assert i in ee
        out[i] += ee[i]
    assert set(assignment) == set(jobs)
    return out


def decode_matching(assignment, selectors, leaves):
    result = []
    for x in range(2):
        a = int(assignment[selectors[x]][1:])
        exported = [assignment[j] for j in leaves[a]
                    if assignment[j].startswith(("B", "C"))]
        assert exported
        result.append((x, exported[0]))
    assert len({r for _, r in result}) == 2
    return result


def actual_upper(ell, machines, jobs, selectors, leaves, matching):
    assignment = {}
    chosen = {}
    for x, (kind, v) in matching:
        c = 1 if kind == "B" else 2
        a = next(a for a, t in enumerate(PARITY) if t[0] == x and t[c] == v)
        chosen[a] = f"{kind}{v}"
        assignment[selectors[x]] = f"S{a}"
    for a in range(4):
        for j in leaves[a]:
            r = jobs[j][1][0]
            export = a in chosen and (r.startswith("D") or r == chosen[a])
            assignment[j] = r if export else f"S{a}"
    actual = max(loads(machines, jobs, assignment).values())
    assert actual == 1 + F(1, ell)
    decode_matching(assignment, selectors, leaves)
    return assignment


def audit(ell):
    machines, resources, jobs, selectors, leaves = build(ell)
    assert len(machines) == 4 + 2 * ell + 1
    assert len(jobs) == 2 + 4 * ell
    assert sum(len(ee) for ee in jobs.values()) == 4 * (2 * ell + 1)
    nu, mu, matching = source_values()
    assert (nu, mu) == (1, 2)
    y = configuration_point(ell, machines, resources, jobs, selectors, leaves)
    config_result = verify_config(ell, machines, jobs, y)
    actual_upper(ell, machines, jobs, selectors, leaves, matching)
    names = list(jobs)
    count, best, best_count = 0, None, 0
    histogram = {}
    decodable_count = 0
    for choices in product(*(jobs[j] for j in names)):
        assignment = {j: edge[0] for j, edge in zip(names, choices)}
        c = max(loads(machines, jobs, assignment).values())
        histogram[str(c)] = histogram.get(str(c), 0) + 1
        count += 1
        if best is None or c < best:
            best, best_count = c, 1
        elif c == best:
            best_count += 1
        assert not (c < 1 + F(1, ell))
        if c < 1 + F(2, ell):
            decode_matching(assignment, selectors, leaves)
            decodable_count += 1
    assert count == 2 ** (4 * ell + 2)
    assert best == 1 + F(1, ell)
    return {"ell": ell, "source_q": 2, "source_tuples": len(PARITY),
            "source_nu": nu, "source_mu": mu,
            "machines_including_one_idle": len(machines), "jobs": len(jobs),
            "finite_edges": sum(len(ee) for ee in jobs.values()),
            "complete_assignments_checked": count, "actual_OPT": str(best),
            "optimal_assignment_count": best_count,
            "assignments_checked_by_absolute_second_decoder": decodable_count,
            "makespan_histogram": histogram, **config_result}


if __name__ == "__main__":
    print(json.dumps({"source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      "arithmetic": "fractions.Fraction; all complete assignments in the two declared seeds",
                      "python_version": platform.python_version(),
                      "command": "python3 tests/audits/unrelated_machines/tiny_work_stability_selection_audit.py",
                      "ok": True,
                      "scope": "four-tuple parity only; all complete assignments; exact Fraction arithmetic",
                      "general_CONFIG_parameterization_optimized": False,
                      "general_NP_completeness_tested": False,
                      "cases": [audit(2), audit(3)]}, indent=2, sort_keys=True))
