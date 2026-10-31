from collections import Counter
from functools import lru_cache
from itertools import combinations, product
from fractions import Fraction
import json


def build(q, triples):
    # Integer times scaled by two; machine 0 is the isolated dummy.
    source = {x: 1 + x for x in range(q)}
    sets = {a: 1 + q + a for a in range(len(triples))}
    y = {e: 1 + q + len(triples) + e for e in range(q)}
    z = {e: 1 + 2*q + len(triples) + e for e in range(q)}
    jobs = []
    for x in range(q):
        opts = ((source[x], 1),) + tuple((sets[a], 2) for a,t in enumerate(triples) if t[0] == x)
        jobs.extend([opts] * 3)
    for a, (_x, yy, zz) in enumerate(triples):
        jobs.append(((sets[a], 1), (y[yy], 2)))
        jobs.append(((sets[a], 1), (z[zz], 2)))
    return 1 + 3*q + len(triples), jobs


def generic_feasible(machine_count, jobs, capacity):
    # Plain integer scheduling search. It has no knowledge of 3DM,
    # sources, activations, sets, or the reduction's counting argument.
    groups = tuple(Counter(jobs).items())
    options = tuple(k for k,v in groups)
    initial_counts = tuple(v for k,v in groups)
    visits = 0

    @lru_cache(maxsize=None)
    def visit(counts, loads):
        nonlocal visits
        visits += 1
        if not any(counts):
            return True
        best = None
        for group, count in enumerate(counts):
            if not count:
                continue
            admissible = tuple((machine, time) for machine,time in options[group]
                               if loads[machine] + time <= capacity)
            if not admissible:
                return False
            rank = (len(admissible), -count, group)
            if best is None or rank < best[0]:
                best = rank, group, admissible
        _, group, admissible = best
        counts2 = list(counts)
        counts2[group] -= 1
        for machine,time in sorted(admissible, key=lambda p: (-loads[p[0]], p[1], p[0])):
            loads2 = list(loads)
            loads2[machine] += time
            if visit(tuple(counts2), tuple(loads2)):
                return True
        return False

    answer = visit(initial_counts, (0,) * machine_count)
    return answer, visits


def perfect_3dm(q, triples):
    return any(all(len({triples[a][coordinate] for a in chosen}) == q for coordinate in range(3))
               for chosen in combinations(range(len(triples)), q))


def check_case(q, triples, checks):
    machines, jobs = build(q, triples)
    assert len(jobs) == 3*q + 2*len(triples)
    assert all(sum(time == 1 for _,time in opts) == 1 for opts in jobs)
    expected = perfect_3dm(q, triples)
    found, visits = generic_feasible(machines, jobs, 2)
    assert found == expected, (q, triples, expected, found)
    checks['cases'] += 1
    checks['nodes'] += visits
    checks['yes'] += expected


def main():
    checks = {'cases': 0, 'nodes': 0, 'yes': 0}
    ranges = []
    for q in range(3):
        universe = tuple(product(range(q), repeat=3))
        for mask in range(1 << len(universe)):
            triples = tuple(t for a,t in enumerate(universe) if mask >> a & 1)
            check_case(q, triples, checks)
        ranges.append({'q':q, 'families':1 << len(universe)})
    # Repeated triples and q=3 hand cases, including isolated coordinates.
    extras = [
        (1, ((0,0,0), (0,0,0))),
        (2, ((0,0,0), (0,0,0), (1,1,1))),
        (2, ((0,0,0), (1,0,1))),
        (3, ((0,0,0), (1,1,1), (2,2,2))),
        (3, ((0,0,0), (1,0,1), (2,2,2))),
        (3, ((0,0,0), (0,1,1), (1,2,2))),
    ]
    for q, triples in extras:
        check_case(q, triples, checks)
    # Half-grid equivalence is exact at the rational level.
    deltas = [Fraction(0), Fraction(1,3), Fraction(49,100), Fraction(499999,1000000)]
    assert all((2*(1+d)).numerator // (2*(1+d)).denominator == 2 for d in deltas)
    # Endpoint obstruction: x exists but no triples. At delta=1/2,
    # the three activation jobs fit on R_x, giving a false 3DM positive.
    machines, jobs = build(1, ())
    assert perfect_3dm(1, ()) is False
    assert generic_feasible(machines, jobs, 3)[0] is True
    print(json.dumps({'reduction':'per-x-source / two-incidence 3DM',
                      'complete_ranges':ranges, 'extra_cases':len(extras),
                      'checks':checks, 'rational_deltas':[str(d) for d in deltas],
                      'endpoint_half_false_positive':True}, indent=2))


if __name__ == '__main__':
    main()
