"""Main's independent literal-pair audit of the complete finite ZZ extension.

Imports only the standard library; does not import the extension builder or
any discovering module. Auxiliaries represent upper envelopes, not joint mass.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import Counter, defaultdict
import gzip, hashlib, json, time

B = Path(__file__).resolve().parent
M = B / 'master_cuts'
stem = 'complete_zz_5799_v1'
started = time.time()

def read_matrix(p):
    with gzip.open(p, 'rt', encoding='utf-8') as f:
        return json.load(f)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def sparse(d):
    return [[j, str(v)] for j, v in sorted(d.items()) if v]

def pattern(a):
    distinct = []
    out = []
    for v in a:
        if v not in distinct:
            distinct.append(v)
        out.append(distinct.index(v))
    return tuple(out)

def group_key(a):
    return (a[0], a[1], tuple(a[2]), tuple(a[3]))

old_path = M / 'dynamic_5799_matrix.json.gz'
new_path = M / (stem + '_matrix.json.gz')
point_path = M / 'dynamic_5799_exact.json'
map_path = M / (stem + '_mapping.json')
old, new = read_matrix(old_path), read_matrix(new_path)
mapping = json.loads(map_path.read_text())
point = json.loads(point_path.read_text())
assert sha(old_path) == '0b4bd0a81097b022a638fdc44324c731768255579a5bf07618e12c35c9342bec'
assert sha(point_path) == '63edbafd53493a20ec64ced5f09a694ead3f894bfb6419cde425de0b3a1710c1'
assert sha(new_path) == '8b076497ef826b60c797edcb8dc719f2f7ad678a01a34ecf66d2e757af525a20'
assert (old['row_count'], old['column_count']) == (5799, 4849)
assert (new['row_count'], new['column_count']) == (11418, 7639)
assert new['rows'][:5799] == old['rows']
assert new['columns'][:4849] == old['columns']
assert new['objective'] == old['objective'] + ['0'] * 2790
assert new['normalization'] == old['normalization'] + ['0'] * 2790
assert new['nonnegative_columns'] == 'all'
assert [{k: v for k, v in c.items() if k != 'weight'} for c in point['columns']] == old['columns']
assert all(all(j < 4849 for j, v in row['nonzero']) for row in new['rows'][:5799])

blocks = {}
for col, record in enumerate(old['columns']):
    if record['kind'] == 'hist':
        h = col
        blocks[h] = {'hist': record, 'groups': {}}
    elif record['kind'] == 'joint-reply':
        key = group_key(record['group'])
        blocks[h]['groups'].setdefault(key, {})[tuple(record['state'])] = col
assert len(blocks) == 16
assert sum(len(v['groups']) for v in blocks.values()) == 194

edges = tuple((f, i, j) for f in (0, 1) for i in range(6) for j in range(6) if f or i != j)
classes = defaultdict(list)
self_classes = set()
for e in edges:
    for f in edges:
        k = (e[0], f[0], pattern(e[1:] + f[1:]))
        if e == f:
            self_classes.add(k)
        else:
            classes[k].append((e, f))
assert len(edges) == 66 and len(classes) == 39
assert sum(len(v) for v in classes.values()) == 66 * 65
assert len(self_classes) == 3 and not (self_classes & set(classes))
assert mapping['literal_edges'] == [list(e) for e in edges]
assert mapping['omitted_pure_self_classes'] == [[k[0], k[1], list(k[2])] for k in sorted(self_classes)]

aux = {}
for col in range(4849, 7639):
    record = new['columns'][col]
    assert record['kind'] == 'zz-frechet-upper-auxiliary'
    key = (record['hist_column'], group_key(record['source_group']), group_key(record['query_group']))
    assert key not in aux
    aux[key] = col
assert len(aux) == 2790
budget_rows = {k: defaultdict(F) for k in classes}
used_aux = set()
degrees = 0
literal_terms = 0
expected_maps = {}
for h, block in blocks.items():
    rec, groups = block['hist'], block['groups']
    words = tuple(w for w, count in zip(product((0, 1), repeat=3), rec['hist']) for _ in range(count))
    assert len(words) == 6
    P = sum(map(int, rec['actual_bits'][:4]))
    D = (P + 1) * (P + 2)
    def group(e):
        return (e[0], int(e[1] == e[2]), words[e[1]], words[e[2]])
    members = defaultdict(list)
    for e in edges:
        members[group(e)].append(e)
    assert set(members) == set(groups)
    gids = {g: j for j, g in enumerate(sorted(groups))}
    pair_counts = {}
    for key, pairs in sorted(classes.items()):
        grouped = defaultdict(list)
        for e, f in pairs:
            grouped[group(e), group(f)].append((e, f))
        for (g, k), subset in grouped.items():
            left, right = Counter(e for e, f in subset), Counter(f for e, f in subset)
            dl, dr = F(len(subset), len(members[g])), F(len(subset), len(members[k]))
            assert all(left[e] == dl for e in members[g])
            assert all(right[f] == dr for f in members[k])
            degrees += 2
        pair_counts[key] = [[gids[g], gids[k], len(pairs_)] for (g, k), pairs_ in sorted(grouped.items())]
        row = budget_rows[key]
        # Coefficients are reconstructed per literal pair, with its own N_C,
        # not copied from stored grouped multiplicities or endpoint choices.
        N = len(pairs)
        for e, f in pairs:
            g, k = group(e), group(f)
            source, query = groups[g], groups[k]
            assert set(source) == set(query) == {(0, 1), (1, 0), (1, 1)}
            z = aux[h, g, k]
            used_aux.add(z)
            for state in ((0, 1), (1, 1)):
                row[source[state]] += F(1, N * (P + 1))
                row[query[state]] -= F(1, N * (P + 1))
            row[source[1, 1]] -= F(1, N * D)
            row[z] += F(1, N * D)
            literal_terms += 1
    expected_maps[h] = (gids, words, members, pair_counts)
assert used_aux == set(range(4849, 7639))
assert literal_terms == 16 * 66 * 65

row_at = 5799
x = [F(c['weight']) for c in point['columns']] + [F(0)] * 2790
min_upper = None
for key, z in sorted(aux.items(), key=lambda p: p[1]):
    h, g, k = key
    sg, kg = blocks[h]['groups'][g], blocks[h]['groups'][k]
    qcols, vcols = (sg[1, 0], sg[1, 1]), (kg[0, 1], kg[1, 1])
    expected_q, expected_v = defaultdict(F), defaultdict(F)
    expected_q[z] = expected_v[z] = F(-1)
    for j in qcols:
        expected_q[j] += 1
    for j in vcols:
        expected_v[j] += 1
    assert new['rows'][row_at]['nonzero'] == sparse(expected_q)
    assert new['rows'][row_at + 1]['nonzero'] == sparse(expected_v)
    q, v = sum(x[j] for j in qcols), sum(x[j] for j in vcols)
    x[z] = min(q, v)
    assert x[z] >= 0
    slacks = [q - x[z], v - x[z]]
    min_upper = min(slacks) if min_upper is None else min(min_upper, *slacks)
    mapped = mapping['auxiliaries'][z - 4849]
    assert mapped['column_index'] == z and mapped['hist_column'] == h
    assert mapped['source_R_columns'] == list(qcols) and mapped['query_Z_columns'] == list(vcols)
    assert mapped['upper_q_row'] == row_at and mapped['upper_v_row'] == row_at + 1
    assert F(mapped['canonical_value_at_base']) == x[z]
    row_at += 2
assert row_at == 11379 and min_upper == 0
checks = []
for index, (key, row) in enumerate(sorted(budget_rows.items())):
    target = new['rows'][row_at + index]
    assert target['nonzero'] == sparse(row)
    assert all(v > 0 for j, v in row.items() if j >= 4849)
    slack = sum(F(v) * x[j] for j, v in target['nonzero'])
    rec = mapping['classes'][index]
    assert rec['class_index'] == index and rec['class'] == [key[0], key[1], list(key[2])]
    assert rec['row_index'] == row_at + index and rec['literal_pairs'] == len(classes[key])
    assert F(rec['normalization_scale']) == F(1, len(classes[key]))
    checks.append({'class': rec['class'], 'row_index': row_at + index,
                   'all_coefficients_match': True, 'canonical_base_slack': str(slack)})
for mapped in mapping['hist_blocks']:
    h = mapped['hist_column']
    gids, words, members, pair_counts = expected_maps[h]
    assert mapped['words'] == [list(w) for w in words]
    assert mapped['P'] == sum(map(int, blocks[h]['hist']['actual_bits'][:4]))
    assert len(mapped['groups']) == len(gids)
    for grouprec in mapped['groups']:
        g = group_key(grouprec['group'])
        assert grouprec['group_id'] == gids[g]
        assert grouprec['literal_edge_indices'] == [edges.index(e) for e in members[g]]
        assert grouprec['joint_columns'] == {''.join(map(str, s)): j for s, j in blocks[h]['groups'][g].items()}
    for clsrec, key in zip(mapped['class_pair_counts'], sorted(classes)):
        assert clsrec['pair_counts'] == pair_counts[key]

fill = json.loads((M / (stem + '_canonical_fill.json')).read_text())
assert fill['auxiliary_values'] == [[j, str(x[j])] for j in range(4849, 7639)]
assert [c['canonical_base_slack'] for c in checks] == [c['slack'] for c in fill['budget_values']]
assert sum(F(c['canonical_base_slack']) < 0 for c in checks) == 11
for row in new['rows']:
    sp = row['nonzero']
    assert sp == sorted(sp) and len({j for j, v in sp}) == len(sp)
    assert all(0 <= j < 7639 and F(v) != 0 for j, v in sp)
    if 'sparse_sha256' in row:
        digest = hashlib.sha256(json.dumps(sp, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()
        assert digest == row['sparse_sha256']

result = {'status': 'PASS', 'matrix_sha256': sha(new_path), 'mapping_sha256': sha(map_path),
          'old_matrix_sha256': sha(old_path), 'point_sha256': sha(point_path),
          'old_rows_and_columns_unchanged': True, 'rows': 11418, 'columns': 7639,
          'upper_rows_rebuilt': 5580, 'budget_rows_rebuilt': 39,
          'literal_pair_terms': literal_terms, 'biregular_degree_checks': degrees,
          'auxiliaries_used': len(used_aux), 'canonical_base_negative_budgets': 11,
          'budgets': checks, 'elimination': 'All q and v are nonnegative; each z <= min(q,v) and has only nonnegative coefficients in every class budget. Thus existence of z is equivalent to simultaneously setting all z=min(q,v). This is an upper-envelope equivalence, not a joint-realizability claim.',
          'scope': 'Only the complete 39 non-self ZZ Frechet upper-bound classes on the fixed 16 histograms, extending the frozen 5799 system.',
          'seconds': time.time() - started, 'verifier_sha256': sha(Path(__file__))}
Path(__file__).with_suffix('.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: v for k, v in result.items() if k != 'budgets'}, ensure_ascii=False, indent=2))
