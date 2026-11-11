"""Verify the original-column interface and all maximal ZZ budget values."""
from pathlib import Path
from fractions import Fraction as F
import gzip, hashlib, json
B = Path(__file__).resolve().parent
D = B / 'master_cuts'
stem = 'complete_zz_5799_v1'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
fullp, oldp = D/(stem+'_exact.json'), D/(stem+'_original4849_exact.json')
full, old = json.loads(fullp.read_text()), json.loads(oldp.read_text())
matrix = json.loads(gzip.decompress((D/(stem+'_matrix.json.gz')).read_bytes()))
mapping = json.loads((D/(stem+'_mapping.json')).read_text())
submitted = json.loads((D/(stem+'_verification.json')).read_text())
assert len(full['columns']) == 7639 and len(old['columns']) == 4849
assert old['columns'] == full['columns'][:4849]
assert F(old['W']) == F(full['W']) and F(old['O']) == F(full['O']) == 1
x = [F(c['weight']) for c in full['columns']]
for rec in mapping['auxiliaries']:
    q = sum(x[j] for j in rec['source_R_columns'])
    v = sum(x[j] for j in rec['query_Z_columns'])
    assert 0 <= x[rec['column_index']] <= min(q, v)
    x[rec['column_index']] = min(q, v)
values = []
for rec, target in zip(mapping['classes'], submitted['ZZ_min_values']):
    row = matrix['rows'][rec['row_index']]
    value = sum(F(v)*x[j] for j, v in row['nonzero'])
    assert value == F(target['slack']) >= 0 and rec['class'] == target['class']
    values.append({'class': rec['class'], 'slack': str(value)})
assert len(values) == 39 and min(F(v['slack']) for v in values) == 0
report = {'status': 'PASS', 'full_point_sha256': sha(fullp), 'projection_sha256': sha(oldp),
          'prefix_weights_and_descriptors_identical': True,
          'scope': 'Exact 4849-column projection of the certified full ZZ point; all 39 maximal min budgets nonnegative; no true cross-intersection realization.',
          'ZZ_min_values': values, 'verifier_sha256': sha(Path(__file__))}
Path(__file__).with_suffix('.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k != 'ZZ_min_values'}, ensure_ascii=False, indent=2))
