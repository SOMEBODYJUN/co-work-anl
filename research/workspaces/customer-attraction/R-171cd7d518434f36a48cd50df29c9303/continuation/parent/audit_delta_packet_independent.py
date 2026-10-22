"""Independent exact replay; ignores packet desired and expected annotations."""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from math import lcm
import gzip
import hashlib
import json

ROOT = Path(__file__).resolve().parents[6]
SOURCE = ROOT / 'research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_k10_packet.json.gz'


def counts_of(size, total):
    if size == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for rest in counts_of(size - 1, total - first):
                yield (first,) + rest


def main():
    raw = SOURCE.read_bytes()
    data = json.loads(gzip.decompress(raw))
    nodes = data['nodes']
    n = data['instance']['players']
    names = data['instance']['topics']
    k = len(names)
    customers = [frozenset(c['topics']) for c in data['instance']['customers']
                 for _ in range(c['multiplicity'])]
    targets = [None] * len(nodes)
    last = [None] * len(nodes)
    for j in sorted(range(len(nodes)), key=lambda j: -sum(nodes[j]['counts'])):
        node = nodes[j]
        depth = sum(node['counts'])
        if depth == n:
            assert 'action' not in node
            targets[j] = tuple(node['counts'])
            continue
        assert len(node['children']) == k
        for action, child in enumerate(node['children']):
            expected = list(node['counts'])
            expected[action] += 1
            assert nodes[child]['counts'] == expected
        child = node['children'][node['action']]
        targets[j] = targets[child]
        last[j] = node['action'] if depth == n - 1 else last[child]
    reachable = {data['root']}
    pending = list(reachable)
    while pending:
        j = pending.pop()
        for child in nodes[j].get('children', []):
            if child not in reachable:
                reachable.add(child)
                pending.append(child)
    assert len(reachable) == len(nodes)

    @lru_cache(None)
    def payoff(a, counts):
        return sum((F(1, sum(counts[t] for t in client))
                    for client in customers if a in client), F(0))

    comparisons = 0
    for j, node in enumerate(nodes):
        if 'action' not in node:
            continue
        own = payoff(node['action'], targets[j])
        for a, child in enumerate(node['children']):
            assert own >= payoff(a, targets[child])
            comparisons += 1
    path, path_nodes = [], []
    j = data['root']
    while 'action' in nodes[j]:
        path_nodes.append(j)
        path.append(nodes[j]['action'])
        j = nodes[j]['children'][path[-1]]
    final = targets[data['root']]
    W = sum(any(final[a] for a in c) for c in customers)
    wlast = payoff(path[-1], final)
    matrices = []
    for i, j in enumerate(path_nodes[:-1]):
        reference = list(final)
        reference[path[i]] -= 1
        reference[path[-1]] -= 1
        actual = [payoff(a, targets[child])
                  for a, child in enumerate(nodes[j]['children'])]
        replies = [last[child] for child in nodes[j]['children']]
        matrix = []
        for a in range(k):
            row = []
            for b in range(k):
                reference_leaf = reference.copy()
                reference_leaf[a] += 1
                reference_leaf[replies[b]] += 1
                row.append(payoff(a, tuple(reference_leaf)) - actual[a])
            matrix.append(row)
        matrices.append(matrix)
    total = [[sum((matrix[a][b] for matrix in matrices), F(0))
              for b in range(k)] for a in range(k)]
    denominator = lcm(*(v.denominator for row in total for v in row))
    integer_matrix = [[int(v * denominator) for v in row] for row in total]

    def delta(counts):
        return F(sum(counts[a] * counts[b] * integer_matrix[a][b]
                     for a in range(k) for b in range(k)), sum(counts) ** 2 * denominator)

    opt, optimal = -1, []
    for counts in counts_of(k, n):
        covered = sum(any(counts[a] for a in c) for c in customers)
        if covered > opt:
            opt, optimal = covered, [counts]
        elif covered == opt:
            optimal.append(counts)
    values = [(delta(q), q) for q in optimal]
    low, high = min(values), max(values)
    query = names.index('T')
    pure = [matrix[query][query] for matrix in matrices]
    budget = F(W + wlast, 2 * n)
    assert pure == [F(1, 2)] * 10 + [F(0)] * 2
    assert len(optimal) == 2002 and opt == 36
    assert low[0] == -F(38375, 5577)
    assert high[0] == F(1373, 507)
    assert delta((1,) * k) == F(7, 132)
    report = {'source': str(SOURCE.relative_to(ROOT)),
              'sha256': hashlib.sha256(raw).hexdigest(), 'nodes': len(nodes),
              'comparisons': comparisons, 'customers': len(customers),
              'path': [names[a] for a in path], 'W': W, 'OPT': opt,
              'pure_T_delta_by_position': list(map(str, pure)),
              'pure_T_total': str(sum(pure)), 'budget': str(budget),
              'pure_T_excess': str(sum(pure) - budget),
              'optimal_count': len(optimal),
              'min_optimal_delta': str(low[0]), 'min_counts': low[1],
              'max_optimal_delta': str(high[0]), 'max_counts': high[1],
              'max_optimal_excess': str(high[0] - budget),
              'uniform_catalog_delta': str(delta((1,) * k)),
              'integer_matrix_denominator': denominator,
              'integer_total_delta_matrix': integer_matrix,
              'status': 'independent exact replay; auxiliary bridge only'}
    Path(__file__).with_name('delta_packet_independent_audit.json').write_text(
        json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
