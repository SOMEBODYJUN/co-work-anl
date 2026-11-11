"""Assemble the frozen 23625 x 21021 common-X necessary system.

No optimizer import or call. Preserve every old coefficient and coordinate.
Promote all 420 former overlap uppers to real, freely recovered core values;
only the old 7954 max and 2790 min variables remain canonical auxiliaries.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import copy
import gzip
import io
import json
import time
import numpy as np

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = WORK.parents[2]
BASE = WORK / 'maxb_augmented_lp/full_lift'
OLDM, ROWS, COLS, NNZ = 22297, 23625, 21021, 3308634
PINS = {
    'maxb_augmented_lp/full_lift/exact_matrix.json.gz': 'c054aadf745ea4540233a3da693917498527d19d4ccecb0fdd34ad884e461e4b',
    'maxb_augmented_lp/full_lift/recovery/augmented_lp_exact.json': '5b1b649af5fc9d359e31dd03945d12708e599e0eeac75983ed188e60178b3bfe',
    'maxb_augmented_lp/full_lift/recovery/exact_dual_certificate.json': '4a6b6ca154ce645bcdabceb50bcb83982fead5875f257bf0a4c56f9576d7405f',
    'maxb_h3_bridge/rows_17.json': '3c9d360cbb0313ae84b4be7add4f4b3f6b67ba57f71cb8f366a2341e8f128d8d',
    'early_x_anchor_queries/rows_51.json': '0ad0b697193d7a8da2cc62275bbf9265912b0485d778d5edd93fc334bd8bb3eb',
    'common_x_own_lift/own_facets.json': '711e0d2b1499784f26fce26d8cc7a7a985c618df52a125f91af61a168bfc70ba',
    'maxb_augmented_lp/full_lift/epigraph_structure.json': '90a7673d817cbfcbca79c876b608e9d307c47b52897c795cfe8655c145ffa6f0',
    'maxb_augmented_lp/full_lift/zz_envelope_structure.json': 'b2136933db4b6c5f939d3218959b27c8bad012ff27cf9b14a1ecb01a7845f0bb',
}


def sha(p): return sha256(p.read_bytes()).hexdigest()


def read(p):
    with gzip.open(p, 'rt', encoding='utf-8') if p.suffix == '.gz' else p.open() as f:
        return json.load(f)


def save(name, obj):
    p = HERE / name
    assert not p.exists(), ('refuse_overwrite', name)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


@lru_cache(maxsize=None)
def rat(v): return F(v)


def main():
    started = time.monotonic()
    for name, pin in PINS.items():
        assert sha(WORK / name) == pin, name
    old = read(BASE / 'exact_matrix.json.gz')
    assert len(old['rows']) == OLDM and len(old['columns']) == COLS
    h3 = read(WORK / 'maxb_h3_bridge/rows_17.json')
    ap = read(WORK / 'early_x_anchor_queries/rows_51.json')
    own = read(WORK / 'common_x_own_lift/own_facets.json')
    additions, names, mapping = [], [], []
    for source, package, expected in [('H3', h3, (17, 1731)), ('early_AP', ap, (51, 5124)), ('own', own, (1260, 5718))]:
        records = package['rows']
        assert (len(records), sum(len(r['row']) for r in records)) == expected
        for local, rec in enumerate(records):
            assert F(rec.get('rhs', rec.get('constant', '0'))) == 0
            name = rec['name'] if isinstance(rec['name'], str) else json.dumps(rec['name'], separators=(',', ':'))
            mapping.append({'source': source, 'source_local_row': local, 'global_row': OLDM + len(additions),
                            'name': name, 'source_hypothetical_append_index': rec.get('append_index_if_used')})
            additions.append(rec['row']); names.append(name)
    assert len(additions) == 1328 and sum(map(len, additions)) == 12573
    columns = copy.deepcopy(old['columns'])
    upgrade = {
        'effective_kind': 'real-common-X-query-overlap', 'recovery_role': 'core',
        'canonical_min_permitted': False,
        'legacy_kind_field': 'Retained for coordinate identity; its former virtual-upper semantics are superseded.',
        'realization_scope': 'Same X mass and exact own Q/R eight-cell marginal, separately for each of 210 groups; no full joint law asserted.'}
    for j in range(20601, COLS):
        assert columns[j]['kind'] == 'X-query-overlap-upper'
        columns[j]['semantic_upgrade'] = copy.deepcopy(upgrade)
    old_metadata = {k: v for k, v in old.items() if k not in ('rows', 'row_names', 'columns', 'objective', 'normalization')}
    matrix = {
        'columns': columns, 'row_names': old['row_names'] + names, 'rows': old['rows'] + additions,
        'objective': old['objective'], 'normalization': old['normalization'],
        'baseline_rows': OLDM, 'baseline_columns': COLS, 'this_round_added_rows': 1328,
        'this_round_added_columns': 0, 'original_semantic_columns': 4849,
        'core_columns': 10277, 'canonical_auxiliary_columns': 10744,
        'canonical_max_auxiliaries': 7954, 'canonical_min_auxiliaries': 2790,
        'shared624_core_columns': 4992, 'common_X_mass_core_columns': 16,
        'common_X_real_overlap_core_columns': 420, 'all_columns_nonnegative': True,
        'inequality_convention': 'Every exact sparse row has value >= 0; homogeneous RHS zero.',
        'normalization_rhs': '1', 'old_metadata_for_provenance_only': old_metadata,
        'coordinate_semantics': 'The 420 semantic_upgrade records supersede their retained legacy kind labels. Only columns 4849..15592 may be canonically recomputed.',
        'scope': 'Full frozen fixed16-hist necessary LP plus H3, early AP and exact local own-X compatibility. Neither full-catalog joint law nor complete SPE sufficiency.'}
    assert len(matrix['rows']) == ROWS and len(set(matrix['row_names'])) == ROWS
    assert sum(map(len, matrix['rows'])) == NNZ
    assert matrix['columns'][:20601] == old['columns'][:20601]
    p = HERE / 'exact_matrix.json.gz'; assert not p.exists()
    with p.open('wb') as raw:
        with gzip.GzipFile(fileobj=raw, mode='wb', filename='', mtime=0) as z:
            with io.TextIOWrapper(z, encoding='utf-8') as f:
                json.dump(matrix, f, ensure_ascii=False, separators=(',', ':'))
    save('append_mapping.json', {'row_ranges_half_open': {'old': [0, OLDM], 'H3': [22297, 22314],
         'early_AP': [22314, 22365], 'own': [22365, ROWS]}, 'records': mapping})
    epi = read(BASE / 'epigraph_structure.json'); zz = read(BASE / 'zz_envelope_structure.json')
    core = list(range(4849)) + list(range(15593, COLS))
    assert len(core) == 10277
    structure = {
        'shape': [ROWS, COLS], 'core_columns': core, 'auxiliary_columns': list(range(4849, 15593)),
        'original_semantic_columns': list(range(4849)), 'shared624_columns': list(range(15593, 20585)),
        'X_mass_columns': list(range(20585, 20601)), 'real_overlap_columns': list(range(20601, COLS)),
        'max_thresholds': epi['thresholds'], 'min_auxiliaries': zz['auxiliaries'],
        'min_upper_rows': zz['upper_rows'], 'shared624_equality_positive_rows': list(range(19662, 20286, 2)),
        'B4_equality_positive_rows': list(range(5462, 5494, 2)),
        'forbidden_canonical_min_columns': list(range(20601, COLS)),
        'matrix_sha256': sha(p), 'semantic_upgrade': upgrade,
        'canonical_policy': 'Recompute only max_thresholds and min_auxiliaries. Preserve every recovered value in real_overlap_columns exactly.'}
    save('coordinate_structure.json', structure)
    blocks = []
    for block in own['blocks']:
        blocks.append({**block, 'joint_matrix_rows': list(range(22365 + 6 * block['block'], 22371 + 6 * block['block']))})
    save('own_blocks.json', {'blocks': blocks, 'source_sha256': PINS['common_x_own_lift/own_facets.json'],
         'matrix_sha256': sha(p), 'beta_choice': 'max(0, yQ-m10, yR-m01, yQ+yR-x)',
         'scope': '210 local eight-cell witnesses only; no cross-group joint law.'})
    old_dual = read(BASE / 'recovery/exact_dual_certificate.json')
    lower = F(old_dual['normalization_multiplier'])
    residuals = [rat(c) - lower * rat(a) for c, a in zip(matrix['objective'], matrix['normalization'])]
    for i, value in old_dual['row_multipliers']:
        assert 0 <= i < OLDM and F(value) > 0
        for j, a in matrix['rows'][i]: residuals[j] -= F(value) * rat(a)
    assert min(residuals) >= 0 and residuals == list(map(F, old_dual['residuals']))
    save('inherited_dual_lower_bound.json', {
        'normalization_multiplier': str(lower), 'row_multipliers': old_dual['row_multipliers'],
        'zero_extended_row_range_half_open': [OLDM, ROWS], 'zero_extended_row_count': 1328,
        'residuals': list(map(str, residuals)), 'minimum_coefficient_residual': str(min(residuals)),
        'matrix_sha256': sha(p), 'source_sha256': PINS['maxb_augmented_lp/full_lift/recovery/exact_dual_certificate.json'],
        'identity': 'objective = lower * normalization + sum_i lambda_i row_i + nonnegative residual',
        'verified': True, 'equality_to_new_primal': False,
        'scope': 'Inherited exact lower bound only. No new optimality or optimum-face exclusion claim.'})
    indptr = [0]; indices = []; data = []; scales = []
    for row in matrix['rows']:
        values = [float(rat(a)) for j, a in row]
        scale = max([abs(v) for v in values] + [1e-50]); scales.append(scale)
        indices.extend(j for j, a in row); data.extend(-v / scale for v in values); indptr.append(len(indices))
    np.savez_compressed(HERE / 'floating_problem.npz',
        indptr=np.asarray(indptr, dtype=np.int64), indices=np.asarray(indices, dtype=np.int64),
        data=np.asarray(data, dtype=np.float64), scales=np.asarray(scales, dtype=np.float64),
        shape=np.asarray([ROWS, COLS], dtype=np.int64), objective=np.asarray([float(rat(v)) for v in matrix['objective']]),
        normalization=np.asarray([float(rat(v)) for v in matrix['normalization']]),
        inequality_rhs=np.zeros(ROWS), normalization_rhs=np.ones(1))
    source_names = list(PINS) + ['main_common_X_pair_facets.md', 'root_x_joint_contract.md',
        'common_x_own_lift/report.md', 'common_x_own_lift/verification.json',
        'common_x_own_lift/evaluator_verification.json', 'maxb_h3_bridge.md', 'maxb_h3_bridge/atom_audit.json',
        'early_x_anchor_queries.md', 'early_x_anchor_queries/verification.json']
    generated = ['exact_matrix.json.gz', 'floating_problem.npz', 'coordinate_structure.json',
                 'own_blocks.json', 'append_mapping.json', 'inherited_dual_lower_bound.json']
    save('inputs_manifest.json', {'source_files': [{'path': str((WORK / name).relative_to(REPO)),
         'sha256': sha(WORK / name), 'bytes': (WORK / name).stat().st_size} for name in source_names],
         'generated_inputs': {name: sha(HERE / name) for name in generated},
         'assembler_sha256': sha(Path(__file__)), 'shape': [ROWS, COLS], 'nonzeros': NNZ,
         'optimizer_calls': 0, 'created_utc': datetime.now(timezone.utc).isoformat()})
    save('assembly_verification.json', {'status': 'ASSEMBLED_REQUIRES_INDEPENDENT_AUDIT',
         'rows': ROWS, 'columns': COLS, 'nonzeros': NNZ, 'added_rows': 1328, 'added_columns': 0,
         'unchanged_old_rows': OLDM, 'unchanged_descriptors': 20601, 'explicitly_upgraded_descriptors': 420,
         'core_columns': 10277, 'canonical_auxiliary_columns': 10744,
         'inherited_lower_bound': str(lower), 'optimizer_calls': 0, 'seconds': time.monotonic() - started})
    print(json.dumps(read(HERE / 'assembly_verification.json'), ensure_ascii=False, indent=2))


if __name__ == '__main__': main()
