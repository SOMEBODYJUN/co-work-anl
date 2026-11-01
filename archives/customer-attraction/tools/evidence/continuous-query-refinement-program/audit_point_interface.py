"""New exact input audit, independent of the old builders and LP solvers."""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import ast
import json


def main():
    p = ArgumentParser()
    for name in ['point', 'reference', 'source', 'cuts', 'output']:
        p.add_argument('--' + name, type=Path, required=True)
    a = p.parse_args()
    loaded = {}
    fingerprints = {}
    for name in ['point', 'reference', 'source', 'cuts']:
        data = getattr(a, name).read_bytes()
        fingerprints[name] = {'size': len(data), 'sha256': sha256(data).hexdigest()}
        loaded[name] = data.decode()
    point, ref, cuts = (json.loads(loaded[k]) for k in ['point', 'reference', 'cuts'])
    assert fingerprints['source']['sha256'] == '9af39d9eecc13ff203713ed60e2058b9d8faa2a6cd8836a76b952201b4da5e19'
    assert fingerprints['point']['sha256'] == 'abac45f78980d02f2bd056758a96653aa0bc0d8b87571820a5742397dc490246'
    assert fingerprints['cuts']['sha256'] == 'aa696d0ebbb1e5b1ccc3b593c5f5a4bcac4cf411966dfd9499192d8170fb5c36'
    tree = ast.parse(loaded['source'])
    assert any(isinstance(n, ast.FunctionDef) and n.name == 'main' for n in tree.body)
    cols, old = point['columns'], ref['columns']
    assert len(cols) == len(old) == 1905
    descriptor = lambda c: {k: v for k, v in c.items() if k != 'weight'}
    assert all(descriptor(c) == descriptor(d) for c, d in zip(cols, old))
    weights, oldweights = [[F(c['weight']) for c in cs] for cs in [cols, old]]
    assert min(weights) >= 0 and cols[0]['kind'] == 'K'
    changes = [{'column': i, 'kind': c['kind'], 'refinement_weight': str(weights[i]),
                'combined_5108_weight': str(oldweights[i])}
               for i, c in enumerate(cols) if weights[i] != oldweights[i]]
    hist, groups = {}, {}
    nearest_hist = None
    for j, c in enumerate(cols):
        if c['kind'] == 'hist':
            nearest_hist = j
            assert len(c['actual_bits']) == 6 and set(c['actual_bits']) <= {'0', '1'}
            assert len(c['hist']) == 8 and all(isinstance(x, int) and x >= 0 for x in c['hist'])
            assert sum(c['hist']) == 6
            assert sum(n * bits[0] for n, bits in zip(c['hist'], product((0, 1), repeat=3))) == c['d']
            hist[j] = c
        elif c['kind'] == 'joint-reply':
            assert nearest_hist is not None
            key = (nearest_hist, json.dumps(c['group'], separators=(',', ':')))
            group = groups.setdefault(key, {})
            state = tuple(c['state'])
            assert state not in group
            group[state] = j
    assert len(hist) == 16 and len(groups) == 194
    marginal_changes = Counter()
    joint_results = []
    for (hi, gs), block in groups.items():
        assert set(block) == {(0, 1), (1, 0), (1, 1)}
        y00 = weights[hi] - sum(weights[j] for j in block.values())
        assert y00 >= 0
        r = sum(weights[j] for st, j in block.items() if st[0])
        z = sum(weights[j] for st, j in block.items() if st[1])
        oldr = sum(oldweights[j] for st, j in block.items() if st[0])
        oldz = sum(oldweights[j] for st, j in block.items() if st[1])
        marginal_changes['R'] += int(r != oldr)
        marginal_changes['Z'] += int(z != oldz)
        joint_results.append({'hist_column': hi, 'group': json.loads(gs), '00': str(y00),
                              'R': str(r), 'Z': str(z)})
    O = sum(weights[j] for j, c in hist.items() if c['d'] > 0)
    W = sum(weights[j] for j, c in hist.items() if '1' in c['actual_bits'])
    assert O == F(point['O']) == 1
    assert W == F(point['W']) == F(ref['W']) < F(1, 2)
    assert O - 2 * W == F(point['strict_half_gap'])
    assert sum(w > 0 for w in weights) == point['positive_columns'] == 179
    assert point['base_rows'] == 5043 and point['continuous_cut_rows'] == len(cuts['cuts']) == 32
    assert point['verified_rows'] == 5075
    assert weights[0] == oldweights[0] and all(weights[j] == oldweights[j] for j in hist)
    result = {'status': 'PASS', 'scope': 'new input-interface and point-identity audit; no matrix build or LP',
              'fingerprints': fingerprints, 'all_original_scalar_fields': {k: v for k, v in point.items() if k != 'columns'},
              'column_kind_counts': dict(Counter(c['kind'] for c in cols)),
              'positive_by_kind': dict(Counter(c['kind'] for c, w in zip(cols, weights) if w > 0)),
              'non_weight_descriptors_equal_5108_point': True, 'all_point_coordinates_nonnegative': True,
              'histograms_checked': len(hist), 'joint_blocks_checked': len(groups),
              'all_194_implicit_00_nonnegative': True, 'O': str(O), 'W': str(W),
              'same_K_and_all_hist_weights_as_5108': True,
              'different_coordinates_by_kind': dict(Counter(c['kind'] for c in changes)),
              'different_R_or_Z_marginals': dict(marginal_changes),
              'different_coordinates': changes, 'joint_block_values': joint_results,
              'limits': 'No overlap bounds or the remaining graph rows are independently regenerated here; the separate original --verify event checks all 5075 frozen-system rows. Same W/hist/K does not identify the full point.'}
    a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ['different_coordinates', 'joint_block_values']}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
