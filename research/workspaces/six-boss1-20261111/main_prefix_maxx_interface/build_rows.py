"""Main's exact 51-row interface; no LP point or optimizer is read."""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import copy
import gzip
import hashlib
import json

HERE = Path(__file__).resolve().parent
W = HERE.parent
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
oldpath = W / 'early_x_anchor_queries/rows_51.json'
colpath = W / 'early_x_anchor_queries/columns_21021.json.gz'
thirdpath = W / 'early3_maxx_cone/rows_17.json'
assert sha(oldpath) == '0ad0b697193d7a8da2cc62275bbf9265912b0485d778d5edd93fc334bd8bb3eb'
assert sha(thirdpath) == 'ea55c096ced52605b8e03d951f0f4ea1c84130f3d05b351258b42a3be32bf5a0'
old = json.loads(oldpath.read_text())
third = json.loads(thirdpath.read_text())
with gzip.open(colpath, 'rt') as f:
    column_data = json.load(f)
cols = column_data['columns'] if isinstance(column_data, dict) else column_data
assert len(cols) == 21021 and all('weight' not in c for c in cols)
constants = {1: F(206, 5), 2: F(121, 4), 3: F(61, 3)}
previous = {1: F(43), 2: F(65, 2), 3: F(23)}
safe = {}
for i in range(1, 4):
    row = {}
    for h, col in enumerate(cols):
        if col['kind'] == 'hist':
            bits = tuple(map(int, col['actual_bits']))
            if bits[i - 1]:
                row[h] = F(1, sum(bits))
    for j in range(20585, 20601):
        h = cols[j]['hist_column']
        bits = tuple(map(int, cols[h]['actual_bits']))
        row[j] = -F(1, sum(bits[:i - 1]) + 7 - i)
    safe[i] = row
rows = []
overlap_uses = Counter()
for entry in old['rows']:
    i = entry['actual_player']
    delta = previous[i] - constants[i]
    coeff = {j: F(c) for j, c in entry['row']}
    for j, c in safe[i].items():
        coeff[j] = coeff.get(j, F(0)) - delta * c
        if not coeff[j]:
            del coeff[j]
    encoded = [[j, str(c)] for j, c in sorted(coeff.items())]
    assert {j: F(c) for j, c in encoded if j >= 20601} == {j: F(c) for j, c in entry['row'] if j >= 20601}
    assert all(F(c) > 0 for j, c in encoded if j >= 20601)
    for j, c in encoded:
        if j >= 20601:
            overlap_uses[j] += 1
    if i == 3:
        assert encoded == third['rows'][entry['orbit_id']]['row']
    new = {k: copy.deepcopy(v) for k, v in entry.items()
           if k not in ('name', 'C', 'row', 'M_upper')}
    new.update(name=['common-X-prefix-SAFE-MAX', i] + entry['name'][2:],
               C=str(constants[i]), row=encoded,
               old_AP_row_name=entry['name'], old_AP_C=str(previous[i]),
               safe_subtraction=str(delta),
               source_claim='Main analytic common f_P-max X and true-prefix SAFE payment; not arbitrary-anchor AP',
               coefficient_identity='new_row = old_AP_row - delta * SAFE_i(X)')
    rows.append(new)
assert len(rows) == 51
assert set(overlap_uses) == set(range(20601, 21021))
assert set(overlap_uses.values()) == {3}
source_files = [oldpath, colpath, thirdpath,
                W / 'main_prefix_safety_maxx_family.md',
                W / 'main_prefix_safety_maxx_family.py',
                W / 'main_prefix_safety_maxx_family.json']
sources = {str(p.relative_to(W)): sha(p) for p in source_files}
data = {'status': 'EXACT_51_ROW_PREFIX_SAFE_MAX_INTERFACE',
        'full_dimension': 21021, 'new_columns': 0, 'row_count': 51,
        'nonzero_count': sum(len(r['row']) for r in rows),
        'constants_by_actual_player': {str(i): str(c) for i, c in constants.items()},
        'all16_histograms_retained': True,
        'all420_overlap_coefficients_unchanged_and_positive': True,
        'each_overlap_used_in_three_rows': True,
        'third17_exactly_match_independently_built_early3_interface': True,
        'safe_rows_from_raw_bits': {str(i): [[j, str(c)] for j, c in sorted(r.items())] for i, r in safe.items()},
        'source_sha256': sources, 'point_weights_read_by_builder': False,
        'optimizer_calls': 0, 'rows': rows,
        'scope': 'Universal inequalities require the same complete-catalogue f_P-max X. The subtraction is an interface identity, not a deduction from arbitrary-anchor AP alone.'}
out = HERE / 'rows_51.json'
assert not out.exists()
out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
manifest = {'status': 'COEFFICIENT_PACKET_FROZEN_BEFORE_THIS_PACKET_POINT_EVALUATION',
            'source_sha256': sources,
            'files': [{'name': p.name, 'sha256': sha(p), 'bytes': p.stat().st_size}
                      for p in (Path(__file__), out)],
            'mathematical_proof': '../main_prefix_safety_maxx_family.md',
            'independent_general_family_review': 'Pending separate reviewer; no Actions authorization from this file.'}
dest = HERE / 'freeze_manifest.json'
assert not dest.exists()
dest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'rows': 51, 'columns': 21021, 'nonzeros': data['nonzero_count'],
                  'rows_sha256': sha(out), 'freeze_sha256': sha(dest)}, indent=2))
