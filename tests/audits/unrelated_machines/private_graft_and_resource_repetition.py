"""需求树私有替换与资源复制的精确有限审计。

Run at repository root; stdout is a fresh JSON record. General identities are
proved in the manuscript, not inferred from these finite enumerations.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import platform

ROOT = Path(__file__).resolve().parents[3]
INPUT = ROOT / 'examples/unrelated_machines/parity_3dm_repetition.json'


def score_tree(k, edges, root=0):
    incoming = [0] * len(k)
    children = [[] for _ in k]
    for u, v in edges:
        incoming[v] += 1
        children[u].append(v)
    seen, stack = {root}, [root]
    while stack:
        for v in children[stack.pop()]:
            assert v not in seen
            seen.add(v)
            stack.append(v)
    assert incoming[root] == 0
    assert all(incoming[v] == 1 for v in seen if v != root)
    return min([Q(1)] + [Q(len(children[v]), k[v]) for v in seen if k[v]])


def optimum(k, edges):
    """Enumerate all parent choices; discard disconnected parent components."""
    incoming = [[] for _ in k]
    for u, v in edges:
        incoming[v].append(u)
    best = Q(0)
    for parents in product(*[[None] + incoming[v] for v in range(1, len(k))]):
        children = [[] for _ in k]
        for v, p in enumerate(parents, 1):
            if p is not None:
                children[p].append(v)
        seen, stack, active = {0}, [0], []
        while stack:
            u = stack.pop()
            for v in children[u]:
                assert v not in seen
                active.append((u, v))
                seen.add(v)
                stack.append(v)
        best = max(best, score_tree(k, active))
    return best


def graft(outer, inner):
    k, edges = list(outer[0]), list(outer[1])
    for v in [v for v, demand in enumerate(k) if demand == 0]:
        ids = {0: v}
        k[v] = inner[0][0]
        for w in range(1, len(inner[0])):
            ids[w] = len(k)
            k.append(inner[0][w])
        edges.extend((ids[u], ids[w]) for u, w in inner[1])
    return k, edges


def all_small():
    for n in range(1, 4):
        possible = [(u, v) for u in range(n) for v in range(u + 1, n)]
        for mask in range(1 << len(possible)):
            edges = [e for i, e in enumerate(possible) if mask >> i & 1]
            for k in product(range(3), repeat=n):
                if all(k[u] > 0 for u, _ in edges):
                    yield k, edges


def matching_size(triples):
    return max([0] + [r for r in range(1, len(triples) + 1)
                      if any(all(len({t[c] for t in subset}) == r for c in range(3))
                             for subset in combinations(triples, r))])


def rooted_3dm(triples, q):
    k = [q] + [1] * q + [2] * len(triples) + [0] * (2 * q)
    ai, yi = 1 + q, 1 + q + len(triples)
    zi = yi + q
    edges = [(0, 1 + x) for x in range(q)]
    for i, (x, y, z) in enumerate(triples):
        edges.extend([(1 + x, ai + i), (ai + i, yi + y), (ai + i, zi + z)])
    return k, edges


def token_jobs(k, edges):
    jobs = [{0: Q(1)}]
    for v, demand in enumerate(k):
        if not demand:
            continue
        children = [w for u, w in edges if u == v]
        count = min(demand, len(children))
        jobs.extend([{v: Q(1, demand), **{w: Q(1) for w in children}}
                     for _ in range(count)])
        if count < demand:
            jobs.append({v: 1 - Q(count, demand)})
    return jobs


def schedule_feasible(jobs, m, bound):
    """Exhaustive original-job assignment oracle, no tree or matching solver."""
    order = sorted(range(len(jobs)), key=lambda j: (len(jobs[j]), -max(jobs[j].values())))
    loads, assignment = [Q(0)] * m, [-1] * len(jobs)
    calls = 0

    def search(pos):
        nonlocal calls
        calls += 1
        if pos == len(order):
            return True
        j = order[pos]
        for i, p in jobs[j].items():
            if loads[i] + p <= bound:
                loads[i] += p
                assignment[j] = i
                if search(pos + 1):
                    return True
                loads[i] -= p
        return False

    ok = search(0)
    return ok, assignment if ok else None, calls


def tensor_map(bits):
    out = []
    pos = 0
    if len(bits) % 2:
        a, b, c = bits[:3]
        out += [b, c, a ^ b]
        pos = 3
    for pos in range(pos, len(bits), 2):
        a, b = bits[pos:pos + 2]
        out += [b, a ^ b]
    return tuple(out)


def main():
    fixture = json.loads(INPUT.read_text())
    parity = [tuple(t) for t in fixture['triples']]
    samples = list(all_small())
    checked = 0
    values = [optimum(*g) for g in samples]
    for i, outer in enumerate(samples):
        for j, inner in enumerate(samples):
            composite = graft(outer, inner)
            if len(composite[0]) <= 6:
                assert optimum(*composite) == min(values[i], values[j])
                checked += 1
    assert matching_size(parity) == 1
    k, edges = rooted_3dm(parity, 2)
    b = optimum(k, edges)
    assert b == Q(1, 2)
    jobs = token_jobs(k, edges)
    at_one, _, calls_one = schedule_feasible(jobs, len(k), Q(1))
    at_half, assignment, calls_half = schedule_feasible(jobs, len(k), Q(3, 2))
    assert not at_one and at_half
    actual_loads = [sum((job.get(i, 0) for job, dest in zip(jobs, assignment) if dest == i), Q(0))
                    for i in range(len(k))]
    assert max(actual_loads) == Q(3, 2)
    pooled = fixture['pool_double_matching']
    assert all(tuple(e[0] for e in row) in parity for row in pooled)
    assert all(len({tuple(row[c]) for row in pooled}) == 4 for c in range(3))
    tensor_checks = []
    for t in range(2, 11):
        rows = []
        for x in product(range(2), repeat=t):
            y = tensor_map(x)
            z = tuple(a ^ b for a, b in zip(x, y))
            assert all(tuple(e) in parity for e in zip(x, y, z))
            rows.append((x, y, z))
        assert all(len({row[c] for row in rows}) == 2 ** t for c in range(3))
        tensor_checks.append({'power': t, 'matching_size': len(rows)})
    result = {
        'claims': ['UM-PRIVATE-GRAFT-NO-AMPLIFICATION-v1', 'UM-RESOURCE-REPETITION-SOUNDNESS-NO-v1'],
        'python': platform.python_version(), 'arithmetic': 'integers and fractions.Fraction; exact',
        'command': 'python3 tests/audits/unrelated_machines/private_graft_and_resource_repetition.py',
        'seed': None, 'small_graphs': len(samples), 'private_graft_cases': checked,
        'graft_scope': 'all topologically labeled n=1,2,3 DAGs, demands 0,1,2, zero only at sinks; all ordered pairs expanded to at most 6 vertices',
        'parity': {'maximum_3dm': 1, 'perfect_target': 2, 'rooted_b_star': str(b),
                   'token_machine_count': len(k), 'token_job_count': len(jobs),
                   'actual_optimum': '3/2', 'assignment_search_calls': [calls_one, calls_half],
                   'schedule_at_three_halves': assignment, 'loads': list(map(str, actual_loads)),
                   'pool_double_perfect_size': 4},
        'tensor_checks': tensor_checks,
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'input_sha256': hashlib.sha256(INPUT.read_bytes()).hexdigest(),
        'limitations': 'finite evidence only; does not establish general identities, general hardness, or preserve NO for other repetition gadgets',
        'all_passed': True,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
