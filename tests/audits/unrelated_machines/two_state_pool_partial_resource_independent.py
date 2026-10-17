from fractions import Fraction as F
from itertools import product, combinations
from collections import deque
import json


def formula(s, K):
    assert type(s) is int and s >= 1 and K >= s
    return max((min(F(k, 2 * s), F(min(s, s * s // k), K)), k)
               for k in range(1, 2 * s + 1))


def construct(s, k):
    assert 1 <= k <= 2 * s
    t = min(s, s * s // k)
    if k <= s:
        answer = {r: [r * s + c for c in range(s)] for r in range(k)}
    else:
        h = k - s
        answer = {s + c: [((c * t + d) % s) * s + c for d in range(t)]
                  for c in range(h)}
        used = {cell for cells in answer.values() for cell in cells}
        for r in range(s):
            answer[r] = [r * s + c for c in range(s) if r * s + c not in used][:t]
    assert len(answer) == k
    all_cells = [cell for cells in answer.values() for cell in cells]
    assert len(all_cells) == len(set(all_cells))
    for label, cells in answer.items():
        assert len(cells) >= t
        if label < s:
            assert all(cell // s == label for cell in cells)
        else:
            assert all(cell % s == label - s for cell in cells)
    return answer, t


def exhaustive_grid(s):
    """Independent resource->row/column/unused exhaustive assignment."""
    best = [0] * (2 * s)
    count = 0
    for assignment in product(range(3), repeat=s * s):
        loads = [0] * (2 * s)
        for cell, use in enumerate(assignment):
            if use == 1:
                loads[cell // s] += 1
            elif use == 2:
                loads[s + cell % s] += 1
        loads.sort(reverse=True)
        best = [max(a, b) for a, b in zip(best, loads)]
        count += 1
    return best, count


def feasible_flow(s, selected, t):
    """Independent integer matching feasibility, not the cyclic witness."""
    n = 2 + s * s + len(selected)
    source, sink = n - 2, n - 1
    graph = [[] for _ in range(n)]

    def edge(u, v, capacity):
        graph[u].append([v, capacity, len(graph[v])])
        graph[v].append([u, 0, len(graph[u]) - 1])

    index = {label: s * s + j for j, label in enumerate(selected)}
    for cell in range(s * s):
        edge(source, cell, 1)
        for label in (cell // s, s + cell % s):
            if label in index:
                edge(cell, index[label], 1)
    for label in selected:
        edge(index[label], sink, t)
    total = 0
    while True:
        previous = [None] * n
        previous[source] = (source, 0)
        queue = deque([source])
        while queue and previous[sink] is None:
            u = queue.popleft()
            for j, (v, capacity, _) in enumerate(graph[u]):
                if capacity and previous[v] is None:
                    previous[v] = (u, j)
                    queue.append(v)
        if previous[sink] is None:
            break
        v = sink
        while v != source:
            u, j = previous[v]
            target, _, back = graph[u][j]
            graph[u][j][1] -= 1
            graph[v][back][1] += 1
            v = u
        total += 1
    return total == t * len(selected)


def all_subsets_grid(s):
    best = [0] * (2 * s)
    checks = 0
    for k in range(1, 2 * s + 1):
        for selected in combinations(range(2 * s), k):
            for t in range(s + 1):
                ok = feasible_flow(s, selected, t)
                if ok:
                    best[k - 1] = max(best[k - 1], t)
                checks += 1
    return best, checks


def main():
    brute_count = 0
    for s in range(1, 4):
        best, count = exhaustive_grid(s)
        assert best == [min(s, s * s // k) for k in range(1, 2 * s + 1)]
        brute_count += count
    flow_checks = 0
    for s in range(1, 5):
        best, checks = all_subsets_grid(s)
        assert best == [min(s, s * s // k) for k in range(1, 2 * s + 1)]
        flow_checks += checks
    cyclic_checks = opt_checks = 0
    for s in range(1, 101):
        for k in range(1, 2 * s + 1):
            _, t = construct(s, k)
            assert t == min(s, s * s // k)
            cyclic_checks += 1
        for K in sorted({s, 2 * s - 1, 2 * s, 3 * s, 10 ** 100 + s}):
            value, k = formula(s, K)
            answer, _ = construct(s, k)
            actual = min(F(len(answer), 2 * s), min(F(len(cells), K) for cells in answer.values()))
            assert value == actual
            if K >= 2 * s:
                assert value == F(s, K)
            opt_checks += 1
    value, k = formula(4, 4)
    assert value == F(5, 8) and k == 5
    witness, quota = construct(4, 5)
    return {'status': 'passed', 'resource_assignments_bruteforced_s_1_2_3': brute_count,
            'all_selected_subsets_quota_flow_checks_s_1_through_4': flow_checks,
            'cyclic_all_k_constructions_s_1_through_100': cyclic_checks,
            'optimized_actual_tree_checks': opt_checks,
            's_K_4': {'value': str(value), 'selected_variables': k, 'quota': quota,
                       'actual_allocations': witness},
            'precision': 'exact integers/Fraction',
            'scope': 'statement-first independent proof/probe, not canonical status'}


if __name__ == '__main__':
    print(json.dumps(main(), indent=2))
