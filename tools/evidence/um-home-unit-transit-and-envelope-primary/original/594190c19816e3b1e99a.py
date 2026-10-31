"""Independent finite oracle for home/unit cycle and root normalization.

No imports from the candidate implementation. Exhaustive job descriptors specify
only the assigned destination, because the transformations use no other edge.
All arithmetic is Fraction; finite evidence is not a universal proof.
"""
from fractions import Fraction as F
from itertools import product
import json


def loads(m, jobs, dest, roots):
    out = [F(0) for _ in range(m)]
    for i in roots:
        out[i] += 1
    for (h, a), d in zip(jobs, dest):
        out[d] += a if d == h else 1
    return out


def root_normalize(m, jobs, dest, roots):
    seen = set(roots)
    while True:
        extra = {d for (h, _), d in zip(jobs, dest) if d != h and h in seen}
        if extra <= seen:
            break
        seen |= extra
    return [d if h in seen else h for (h, _), d in zip(jobs, dest)], seen


def erase_cycles(m, jobs, dest):
    # Independently enumerate simple vertex cycles; do not use a graph library.
    dest = list(dest)
    steps = 0
    while True:
        edge = {(h, d): j for j, ((h, _), d) in enumerate(zip(jobs, dest)) if d != h}
        found = None
        for start in range(m):
            stack = [(start, [start])]
            while stack and found is None:
                v, path = stack.pop()
                for w in range(m):
                    if (v, w) not in edge:
                        continue
                    if w == start:
                        found = [edge[(path[t], path[t+1])] for t in range(len(path)-1)]
                        found.append(edge[(v, start)])
                        break
                    if w not in path:
                        stack.append((w, path + [w]))
            if found is not None:
                break
        if found is None:
            return dest, steps
        for j in found:
            dest[j] = jobs[j][0]
        steps += 1


def audit():
    counts = dict(assignments=0, sub_two=0, root_normalizations=0,
                  cycle_instances=0, cycles_removed=0, boundary_checks=0)
    sizes = [(1, 0), (1, 2), (2, 3), (3, 3)]
    for m, n in sizes:
        desc = [(h, a, d) for h in range(m) for a in (F(0), F(1,2), F(1)) for d in range(m)]
        for descriptors in product(desc, repeat=n):
            jobs = [(h, a) for h, a, _ in descriptors]
            dest = [d for _, _, d in descriptors]
            for roots in [()] + [(i,) for i in range(m)]:
                before = loads(m, jobs, dest, roots)
                after_dest, steps = erase_cycles(m, jobs, dest)
                after = loads(m, jobs, after_dest, roots)
                assert all(y <= x for x, y in zip(before, after))
                counts['assignments'] += 1
                counts['cycle_instances'] += bool(steps)
                counts['cycles_removed'] += steps
                C = max(before)
                if C >= 2:
                    continue
                counts['sub_two'] += 1
                indeg = [int(i in roots) for i in range(m)]
                for (h, _), d in zip(jobs, dest):
                    if d != h:
                        indeg[d] += 1
                assert max(indeg) <= 1
                baseline = [sum((a for h, a in jobs if h == i), F(0)) for i in range(m)]
                if max(baseline) <= C:
                    normalized, reached = root_normalize(m, jobs, dest, roots)
                    nl = loads(m, jobs, normalized, roots)
                    assert max(nl) <= C
                    assert all(nl[i] == before[i] for i in reached)
                    assert all(nl[i] == baseline[i] for i in range(m) if i not in reached)
                    assert erase_cycles(m, jobs, normalized)[1] == 0
                    counts['root_normalizations'] += 1
    # Root clearing can increase a machine's load while preserving makespan.
    jobs = [(0, F(1,2))]
    nd, seen = root_normalize(2, jobs, [1], ())
    assert loads(2, jobs, [1], ()) == [0, 1]
    assert loads(2, jobs, nd, ()) == [F(1,2), 0]
    counts['boundary_checks'] += 1
    # Home>1 invalidates row domination; never extrapolate beyond the hypothesis.
    jobs = [(0, F(3,2)), (1, F(3,2))]
    nd, steps = erase_cycles(2, jobs, [1,0])
    assert loads(2, jobs, nd, ()) == [F(3,2), F(3,2)]
    assert loads(2, jobs, [1,0], ()) == [1,1]
    assert steps == 1
    counts['boundary_checks'] += 1
    # A simultaneous normalization need not be executable below the same cap.
    jobs = [(0, F(1)), (1, F(1))]
    old = [1,0]
    assert loads(2, jobs, old, ()) == [1,1]
    for j in range(2):
        step = old[:]
        step[j] = jobs[j][0]
        assert max(loads(2, jobs, step, ())) == 2
    counts['boundary_checks'] += 1
    return counts


if __name__ == '__main__':
    print(json.dumps({'arithmetic': 'fractions.Fraction', 'result': audit(),
                      'scope': 'finite implementation audit only'}, sort_keys=True, indent=2))
