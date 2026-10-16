from fractions import Fraction as F
from itertools import combinations
import json

triples = [(0,0,0), (0,1,1), (1,0,1), (1,1,0)]
perfect = [pair for pair in combinations(triples, 2) if all(len({a[k] for a in pair}) == 2 for k in range(3))]
assert perfect == []
machines = [('R', x) for x in range(2)] + [('S', a) for a in triples] + [('Y', y) for y in range(2)] + [('Z', z) for z in range(2)]
jobs = [('A', x, t) for x in range(2) for t in range(3)] + [('I', a, k) for a in triples for k in (1,2)]
mi = {v: k for k, v in enumerate(machines)}
domains = []
x = []
for job in jobs:
    if job[0] == 'A':
        _, xx, _ = job
        dom = [(mi[('R', xx)], F(1,2))] + [(mi[('S', a)], F(1)) for a in triples if a[0] == xx]
        frac = {dom[0][0]: F(2,3), **{i: F(1,6) for i, _ in dom[1:]}}
    else:
        _, a, k = job
        dom = [(mi[('S', a)], F(1,2)), (mi[(('Y' if k == 1 else 'Z'), a[k])], F(1))]
        frac = {i: F(1,2) for i, _ in dom}
    assert sum(frac.values()) == 1
    domains.append(dom)
    x.append(frac)

fractional_loads = [sum((dict(domains[j]).get(i, F(0)) * x[j].get(i, F(0)) for j in range(len(jobs))), F(0)) for i in range(len(machines))]
assert all(v == 1 for v in fractional_loads)
for i in range(len(machines)):
    positive_times = [p for dom in domains for machine, p in dom if machine == i]
    gamma = min(positive_times)
    assert max(positive_times) <= 2 * gamma
    assert sum((x[j].get(i, F(0)) for j in range(len(jobs))
                if dict(domains[j]).get(i, F(0)) > F(1, 2)), F(0)) <= 1
    assert sum((x[j].get(i, F(0)) for j in range(len(jobs))
                if dict(domains[j]).get(i, F(0)) > F(1, 3)), F(0)) <= 2
    if 1 < 4 * gamma:
        assert sum((row.get(i, F(0)) for row in x), F(0)) <= 1 // gamma

slots = []
for i in range(len(machines)):
    seq = sorted((j for j in range(len(jobs)) if i in x[j]), key=lambda j: (-dict(domains[j])[i], j))
    pos = F(0)
    buckets = {}
    for j in seq:
        left = x[j][i]
        while left:
            s = pos.numerator // pos.denominator
            take = min(left, s + 1 - pos)
            buckets.setdefault(s, []).append(j)
            pos += take
            left -= take
    slots.extend((i, js) for _, js in sorted(buckets.items()))

adj = [[s for s, (_, js) in enumerate(slots) if j in js] for j in range(len(jobs))]
matched = {}
def augment(j, seen):
    for s in adj[j]:
        if s in seen:
            continue
        seen.add(s)
        if s not in matched or augment(matched[s], seen):
            matched[s] = j
            return True
    return False
for j in range(len(jobs)):
    assert augment(j, set())
sigma = {j: slots[s][0] for s, j in matched.items()}
loads = [sum((dict(domains[j])[i] for j in sigma if sigma[j] == i), F(0)) for i in range(len(machines))]
assert max(loads) == F(3,2)

def has_schedule(cap):
    order = sorted(range(len(jobs)), key=lambda j: len(domains[j]))
    current = [F(0)] * len(machines)
    def go(k):
        if k == len(order):
            return True
        j = order[k]
        for i, p in domains[j]:
            if current[i] + p <= cap:
                current[i] += p
                if go(k + 1):
                    return True
                current[i] -= p
        return False
    return go(0)

assert not has_schedule(F(1))
assert has_schedule(F(3,2))
print(json.dumps({"status": "pass", "machines": len(machines), "jobs": len(jobs), "perfect_3dm_count": len(perfect), "fractional_loads": [str(v) for v in fractional_loads], "st_loads": [str(v) for v in loads], "OPT": "3/2", "input": {"machine_labels": machines, "job_labels": jobs, "eligible_times": [[(i, str(p)) for i, p in dom] for dom in domains]}, "fractional_certificate_by_job": [[(i, str(value)) for i, value in sorted(row.items())] for row in x], "assignment": [sigma[j] for j in range(len(jobs))], "scope": "one explicit parity 3DM NO instance, exact Fraction LP certificate, actual covering slot matching, independent bounded-capacity assignment backtracking"}, indent=2))
