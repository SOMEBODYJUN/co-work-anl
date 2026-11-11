"""Main's separate sparse rational primal/dual check, without solver imports.

Run with an extended-system prefix and its predecessor; old columns are a prefix.
This proves optimality only for the explicitly saved finite matrix.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse, gzip, hashlib, json, time

parser = argparse.ArgumentParser()
parser.add_argument('prefix')
parser.add_argument('--base', required=True)
args = parser.parse_args()
B = Path(__file__).resolve().parent
D = B / 'master_cuts'
start = time.time()

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def matrix(prefix):
    p = D / (prefix + '_matrix.json.gz')
    return p, json.loads(gzip.decompress(p.read_bytes()))

mp, m = matrix(args.prefix)
bp, old = matrix(args.base)
pp = D / (args.prefix + '_exact.json')
dp = D / (args.prefix + '_dual.json')
p, d = json.loads(pp.read_text()), json.loads(dp.read_text())
assert d['matrix_sha256'] == sha(mp) and d['point_sha256'] == sha(pp)
assert m['columns'][:len(old['columns'])] == old['columns']
added_columns = len(m['columns']) - len(old['columns'])
assert added_columns >= 0
assert list(map(F, m['objective'])) == list(map(F, old['objective'])) + [F(0)] * added_columns
assert list(map(F, m['normalization'])) == list(map(F, old['normalization'])) + [F(0)] * added_columns
assert m['rows'][:len(old['rows'])] == old['rows']
assert len(m['rows']) == m['row_count'] and len(m['columns']) == m['column_count']
assert m['columns'] == [{k: v for k, v in c.items() if k != 'weight'} for c in p['columns']]
x = [F(c['weight']) for c in p['columns']]
c, n = list(map(F, m['objective'])), list(map(F, m['normalization']))
assert min(x) >= 0 and len(x) == len(c) == len(n) == m['column_count']
O = sum((nj * xj for nj, xj in zip(n, x)), F(0))
W = sum((cj * xj for cj, xj in zip(c, x)), F(0))
assert O == 1 and W == F(p['W']) == F(d['dual_value']) == F(d['normalization_multiplier'])
rows, slacks = [], []
for i, row in enumerate(m['rows']):
    assert row['index'] == i
    a = {j: F(v) for j, v in row['nonzero']}
    assert len(a) == len(row['nonzero']) and all(0 <= j < len(x) for j in a)
    s = sum((v * x[j] for j, v in a.items()), F(0))
    assert s >= 0, (i, row['name'], str(s))
    rows.append(a)
    slacks.append(s)
r = [cj - W * nj for cj, nj in zip(c, n)]
used = set()
positive_new = []
for z in d['row_multipliers']:
    i, lam = z['row_index'], F(z['weight'])
    assert i not in used and 0 <= i < len(rows) and lam >= 0
    assert z['row_name'] == m['rows'][i]['name']
    used.add(i)
    for j, v in rows[i].items():
        r[j] -= lam * v
    assert lam * slacks[i] == 0
    if i >= len(old['rows']) and lam > 0:
        positive_new.append(i)
assert min(r) >= 0 and r == list(map(F, d['residuals']))
assert sum((rj * xj for rj, xj in zip(r, x)), F(0)) == 0
out = {
    'status': 'PASS',
    'scope': 'Separate Fraction replay of every saved primal row and dual column; inherited rows unchanged; not an SPE or all-instance half proof',
    'base_sha256': sha(bp), 'matrix_sha256': sha(mp), 'point_sha256': sha(pp), 'dual_sha256': sha(dp),
    'rows': len(rows), 'columns': len(x), 'base_rows': len(old['rows']), 'base_columns': len(old['columns']), 'added_columns': added_columns,
    'positive_columns': sum(v > 0 for v in x), 'positive_dual_multipliers': sum(F(z['weight']) > 0 for z in d['row_multipliers']),
    'positive_new_row_indices': positive_new, 'minimum_primal_slack': str(min(slacks)),
    'minimum_dual_residual': str(min(r)), 'O': str(O), 'W': str(W),
    'strict_half_gap': str(1 - 2 * W), 'seconds': time.time() - start,
    'verifier_sha256': sha(Path(__file__)),
}
(B / ('main_verify_' + args.prefix + '.json')).write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(out, ensure_ascii=False, indent=2))
