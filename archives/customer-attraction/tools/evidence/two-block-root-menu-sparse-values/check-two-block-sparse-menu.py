from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import cache
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import sys

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
DAG = ROOT / 'archives/customer-attraction/tools/evidence/Boss7-resume-d22-menu/original/pure_menu_two_block_dag.json'
PAYLOAD = '6190bc98dedda4fb22a1af6339702c03a6cb3b04cd8dfe6b18a577782e5d2f95'
LOCAL = (([0], 2), ([1, 3], 4), ([0, 2], 6), ([2, 3], 3), ([0, 1, 2, 3], 1))
UNITS = tuple(tuple(a + 4 * j for a in labels) for j in range(2)
              for labels, n in LOCAL for _ in range(n))

@cache
def pay(a, q, extra=0):
    return sum((F(1, sum(q[i] for i in t) + extra) for t in UNITS if a in t), F(0))


def read_dag():
    payload = DAG.read_bytes()
    assert sha256(payload).hexdigest() == PAYLOAD
    cert = json.loads(payload)
    assert cert['schema'] == 'CA_COMPLETE_SPE_DAG_v1'
    nodes, root = cert['nodes'], cert['root']
    assert nodes[root]['counts'] == [0] * 8 and nodes[root]['action'] == 3
    terminal = {}
    multiplicity = {root: 1}
    decisions = Counter()
    reached_by_depth = Counter()
    order = sorted(range(len(nodes)), key=lambda i: sum(nodes[i]['counts']))
    for i in reversed(order):
        n = nodes[i]
        assert set(n) == {'counts', 'target', 'action', 'children'}
        c, q = tuple(n['counts']), tuple(n['target'])
        a, children = n['action'], n['children']
        assert len(c) == len(q) == 8 and all(type(x) is int and x >= 0 for x in c + q)
        assert sum(c) <= sum(q) == 8 and all(x <= y for x, y in zip(c, q))
        if sum(c) == 8:
            assert a is None and children == [] and c == q
            terminal[i] = c
            continue
        assert type(a) is int and 0 <= a < 8 and len(children) == 8
        assert all(type(j) is int and 0 <= j < len(nodes) for j in children)
        terminal[i] = terminal[children[a]]
        assert terminal[i] == q
        for b, j in enumerate(children):
            expected = list(c)
            expected[b] += 1
            assert nodes[j]['counts'] == expected
            gap = pay(a, terminal[i]) - pay(b, terminal[j])
            assert gap >= 0
            decisions[gap > 0] += 1
    for i in order:
        count = multiplicity[i]
        reached_by_depth[sum(nodes[i]['counts'])] += count
        for child in nodes[i]['children']:
            multiplicity[child] = multiplicity.get(child, 0) + count
    assert reached_by_depth == {d: 8 ** d for d in range(9)}
    assert len(nodes) == 13872 and decisions == {False: 8764, True: 50732}
    cols = [terminal[i] for i in nodes[root]['children']]
    assert list(map(list, cols)) == cert['root_columns']
    h = (2, 1, 1, 0)
    local = [(2, 0, 1, 1), (1, 1, 1, 1), (1, 0, 2, 1), (1, 0, 1, 2)]
    assert cols == [q + h for q in local] + [h + q for q in local]
    own = [pay(i, q) for i, q in enumerate(cols)]
    assert own == [F(13, 4), F(9, 4), F(13, 4), F(13, 4)] * 2
    path = []
    cursor = root
    while nodes[cursor]['action'] is not None:
        a = nodes[cursor]['action']
        path.append(a)
        cursor = nodes[cursor]['children'][a]
    assert path == [3, 0, 2, 3, 4, 4, 5, 6]
    assert sum(pay(a, terminal[root]) for a in path) == len(UNITS) == 32
    return [[pay(a, q, 1) for q in cols] for a in range(8)]


def cap(K, q):
    return max(sum(a * b for a, b in zip(row, q)) for row in K)


def column_mixes(K, support):
    size = len(support) + 1
    normal = [F(1)] * len(support) + [F(0), F(1)]
    equations = [[F(int(i == j)) for j in range(size)] + [F(0)] for i in range(size - 1)]
    equations += [[*(row[i] for i in support), -F(1), F(0)] for row in K]
    for active in combinations(equations, size - 1):
        rows = [normal[:], *(line[:] for line in active)]
        for j in range(size):
            k = next((i for i in range(j, size) if rows[i][j]), None)
            if k is None:
                break
            rows[j], rows[k] = rows[k], rows[j]
            rows[j] = [v / rows[j][j] for v in rows[j]]
            for i in range(size):
                if i != j and rows[i][j]:
                    rows[i] = [x - rows[i][j] * y for x, y in zip(rows[i], rows[j])]
        else:
            prob = [F(0)] * 8
            for i, j in enumerate(support):
                prob[j] = rows[i][-1]
            if min(prob) >= 0 and cap(K, prob) <= rows[-1][-1]:
                yield rows[-1][-1], tuple(prob)


def main():
    K = read_dag()
    expected = {1: F(37, 10), 2: F(123, 40), 3: F(1717, 560), 4: F(851, 280)}
    optimizers = defaultdict(set)
    for size, v in expected.items():
        opt = None
        for subset in combinations(range(8), size):
            for value, q in column_mixes(K, subset):
                if opt is None or value < opt:
                    opt = value
                    optimizers[size].clear()
                if opt == value:
                    optimizers[size].add(q)
        assert opt == v
    assert len(optimizers[1]) == 8
    assert optimizers[2] == {(0, 0, 0, F(1, 2)) * 2}
    q3 = (0, 0, 0, F(15, 28), 0, 0, F(1, 28), F(3, 7))
    assert optimizers[3] == {q3, q3[4:] + q3[:4]}
    q4 = (0, 0, F(1, 14), F(3, 7)) * 2
    assert optimizers[4] == {q4}
    p = (0, 0, F(2, 7), F(3, 14)) * 2
    assert min(sum(p[i] * row[j] for i, row in enumerate(K)) for j in range(8)) == expected[4]
    for size, v in expected.items():
        print(f'support at most {size}: {v}; minimizers {len(optimizers[size])}')
    print('all 162 supports, all 13872 DAG nodes and all 59496 local comparisons checked')


if __name__ == '__main__':
    main()
