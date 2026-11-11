"""Main's exact certificate replay with explicit immutable file arguments.

All primal rows and dual columns are checked without importing a producer or
optimizer. A matrix's semantic coefficients are audited in a separate report.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse
import gzip
import hashlib
import json
import time

ap = argparse.ArgumentParser()
ap.add_argument('--matrix', required=True)
ap.add_argument('--point', required=True)
ap.add_argument('--dual', required=True)
ap.add_argument('--base-matrix', required=True)
ap.add_argument('--report', required=True)
args = ap.parse_args()
start = time.time()


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(p):
    data = p.read_bytes()
    if p.suffix == '.gz':
        data = gzip.decompress(data)
    return json.loads(data)


mp, pp, dp, bp = map(Path, (args.matrix, args.point, args.dual, args.base_matrix))
m, p, d, base = map(load, (mp, pp, dp, bp))
report_path = Path(args.report)
assert not report_path.exists(), 'Refuse to overwrite a frozen audit'
assert d['matrix_sha256'] == sha(mp) and d['point_sha256'] == sha(pp)
assert m['columns'][:len(base['columns'])] == base['columns']
assert m['rows'][:len(base['rows'])] == base['rows']
extra = len(m['columns']) - len(base['columns'])
assert extra >= 0
c = list(map(F, m['objective']))
n = list(map(F, m['normalization']))
assert c == list(map(F, base['objective'])) + [F(0)] * extra
assert n == list(map(F, base['normalization'])) + [F(0)] * extra
assert len(m['rows']) == m['row_count']
assert len(m['columns']) == m['column_count']
assert m['columns'] == [{k:v for k,v in col.items() if k != 'weight'} for col in p['columns']]
x = [F(col['weight']) for col in p['columns']]
assert len(x) == len(c) == len(n) == m['column_count']
assert min(x) >= 0
O = sum((v*y for v,y in zip(n,x)), F(0))
W = sum((v*y for v,y in zip(c,x)), F(0))
assert O == 1
assert W == F(p['W']) == F(d['dual_value']) == F(d['normalization_multiplier'])
rows = []
slacks = []
for i, row in enumerate(m['rows']):
    assert row['index'] == i
    a = {j:F(v) for j,v in row['nonzero']}
    assert len(a) == len(row['nonzero']) and all(0 <= j < len(x) for j in a)
    s = sum((v*x[j] for j,v in a.items()), F(0))
    assert s >= 0, (i,row['name'],str(s))
    rows.append(a)
    slacks.append(s)
residual = [cj-W*nj for cj,nj in zip(c,n)]
used = set()
positive_added = []
positive_count = 0
for term in d['row_multipliers']:
    i, lam = term['row_index'], F(term['weight'])
    assert i not in used and 0 <= i < len(rows) and lam >= 0
    assert term['row_name'] == m['rows'][i]['name']
    used.add(i)
    positive_count += (lam > 0)
    for j,v in rows[i].items():
        residual[j] -= lam*v
    assert lam*slacks[i] == 0
    if i >= len(base['rows']) and lam > 0:
        positive_added.append({'row_index':i,'row_name':term['row_name'],'weight':str(lam)})
assert min(residual) >= 0
assert residual == list(map(F,d['residuals']))
assert sum((rj*xj for rj,xj in zip(residual,x)), F(0)) == 0
out = {
    'status':'PASS',
    'scope':'Exact optimality of this explicitly saved finite rational matrix only; every primal row and dual column independently checked. No general welfare bound or full-SPE realization is implied.',
    'base_matrix_path':str(bp),'matrix_path':str(mp),'point_path':str(pp),'dual_path':str(dp),
    'base_sha256':sha(bp),'matrix_sha256':sha(mp),'point_sha256':sha(pp),'dual_sha256':sha(dp),
    'verifier_sha256':sha(Path(__file__)),
    'rows':len(rows),'columns':len(x),'base_rows':len(base['rows']),'base_columns':len(base['columns']),
    'positive_columns':sum(y>0 for y in x),'positive_dual_multipliers':positive_count,
    'positive_added_rows':positive_added,
    'minimum_primal_slack':str(min(slacks)),'minimum_dual_residual':str(min(residual)),
    'O':str(O),'W':str(W),'strict_half_gap':str(1-2*W),
    'seconds':time.time()-start,
}
report_path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k != 'positive_added_rows'},ensure_ascii=False,indent=2))
print('positive_added_rows_count',len(positive_added))
