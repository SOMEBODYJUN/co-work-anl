"""Local exact check of the 36 added rows; never build or solve the full graph.

The semantic coefficients enumerate all ordered index edges, independently of
the source's histogram multiplicity formula. Only added_rows and its constants
are extracted by AST; importing the full dependency graph is unnecessary.
"""
import argparse
import ast
from collections import Counter
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path

def digest(path):
    b = path.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def load_added(source):
    tree = ast.parse(source.read_text())
    selected = []
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in {'GROUPS', 'KEYS', 'PAT'} for t in node.targets):
            selected.append(node)
        if isinstance(node, ast.FunctionDef) and node.name == 'added_rows':
            selected.append(node)
    assert len(selected) == 4
    namespace = {'F': F, 'product': product}
    exec(compile(ast.Module(body=selected, type_ignores=[]), str(source), 'exec'), namespace)
    expected = tuple((i, member, f, diag) for i in range(6) for member in range(2) for f, diag in [(0, 0), (1, 0), (1, 1)])
    assert namespace['KEYS'] == expected
    return namespace['added_rows'], expected

def semantic_rows(columns, keys):
    patterns = tuple(product(range(2), repeat=3))
    rows = [[F(0) for c in columns] for key in keys]
    edges = Counter()
    actual = None
    group_checks = []
    for j, column in enumerate(columns):
        kind = column['kind']
        if kind == 'hist':
            actual = tuple(int(v) for v in column['actual_bits'])
            assert len(actual) == 6 and set(actual) <= {0, 1}
            assert len(column['hist']) == 8 and sum(column['hist']) == 6
            words = [w for w, n in zip(patterns, column['hist']) for _ in range(n)]
            assert column['d'] == sum(w[0] for w in words)
            edges = Counter((family, int(left == right), words[left], words[right])
                            for family in range(2) for left in range(6) for right in range(6)
                            if family == 1 or left != right)
            counts = {str(g): sum(n for (family, diagonal, wi, wj), n in edges.items() if (family, diagonal) == g)
                      for g in [(0, 0), (1, 0), (1, 1)]}
            assert list(counts.values()) == [30, 30, 6]
            group_checks.append({'hist_column': j, 'edge_count': sum(edges.values()), 'group_edge_counts': counts})
            for row, (position, member, family, diagonal) in zip(rows, keys):
                own = F(actual[position], sum(actual)) if actual[position] else F(0)
                # One copy of the same actual-source payoff for every legal edge.
                row[j] = sum(own * count for (f, d, wi, wj), count in edges.items() if (f, d) == (family, diagonal))
        elif kind == 'joint-reply':
            assert actual is not None
            family, diagonal, wi, wj = column['group']
            group = (family, diagonal, tuple(wi), tuple(wj))
            assert group in edges
            assert tuple(column['state']) in [(0, 1), (1, 0), (1, 1)]
            for row, (position, member, f, d) in zip(rows, keys):
                if (f, d) == (family, diagonal) and column['state'][member]:
                    # Sum the customer's worst-case legal deviation share over
                    # every edge represented by this single joint-state column.
                    row[j] = sum((-F(1, sum(actual[:position]) + 6 - position)
                                  for _ in range(edges[group])), F(0))
        else:
            assert kind in {'K', 'overlap'}
    return rows, group_checks

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--point', type=Path, action='append', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    added_rows, keys = load_added(args.source)
    output = {'scope': '36 new floor rows only; explicit ordered-index coefficient enumeration; no whole graph, no original CLI, no LP, no SPE verification',
              'source': digest(args.source), 'source_execution': 'AST-selected GROUPS/KEYS/PAT/added_rows only', 'points': []}
    canonical = None
    for path in args.point:
        data = json.loads(path.read_text())
        cols = data['columns']
        descriptors = [{k: v for k, v in c.items() if k != 'weight'} for c in cols]
        if canonical is None:
            canonical = descriptors
        assert descriptors == canonical, 'Different column layouts cannot share a positional weight vector'
        observed = added_rows(cols)
        expected, groups = semantic_rows(cols, keys)
        assert observed == expected
        weights = [F(c['weight']) for c in cols]
        assert all(v >= 0 for v in weights)
        welfare = sum((w for c, w in zip(cols, weights) if c['kind'] == 'hist' and '1' in c['actual_bits']), F(0))
        norm = sum((w for c, w in zip(cols, weights) if c['kind'] == 'hist' and c['d'] > 0), F(0))
        assert norm == 1 and welfare == F(data['W'])
        slacks = [sum((a * b for a, b in zip(row, weights)), F(0)) for row in expected]
        output['points'].append({'input_name': path.name, **digest(path), 'column_count': len(cols),
                                'column_kinds': dict(Counter(c['kind'] for c in cols)), 'all_column_descriptors_equal_first_point': True,
                                'coefficient_equalities': len(cols)*len(keys), 'group_checks': groups,
                                'O': str(norm), 'W': str(welfare), 'positive_columns': sum(v>0 for v in weights),
                                'floor_rows': len(keys), 'minimum_floor_slack': str(min(slacks)),
                                'negative_floor_rows': sum(v<0 for v in slacks), 'zero_floor_rows': sum(v==0 for v in slacks),
                                'slacks': [{'key': list(k), 'value': str(v)} for k, v in zip(keys, slacks)]})
    output['pass'] = True
    args.out.write_text(json.dumps(output, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({p['input_name']: {k:p[k] for k in ['coefficient_equalities','negative_floor_rows','zero_floor_rows','minimum_floor_slack']} for p in output['points']}, indent=2))

if __name__ == '__main__':
    main()
