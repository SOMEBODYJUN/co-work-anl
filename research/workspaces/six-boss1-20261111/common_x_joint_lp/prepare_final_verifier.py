"""Materialize the final independent checker without importing a generator.

The resulting verifier is self-contained standard-library code. This source
adaptation only adds the approved 51-row reconstruction and prefix checks.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE/'final'


def main():
    assert (OUT/'assembly_verification.json').is_file()
    source = (HERE/'verify_certificates.py').read_text()
    source = source.replace('23625', '23676').replace('3308634', '3313758')
    source = source.replace('WORK = HERE.parent\n', 'WORK = HERE.parents[1]\n')
    source = source.replace("'inherited_dual_rows_zero_extended': 1328", "'inherited_dual_rows_zero_extended': 1379")
    source = source.replace("'whole_W10_optimum_face_excluded': False", "'whole_W10_optimum_face_excluded_by_this_audit': False")
    marker = "PINS = {\n"
    insert = """PINS = {
    'common_x_joint_lp/exact_matrix.json.gz': '77781e837b86d7ec8e85634935377fd8183e4c3e945120dc4dd368a40bb1d09c',
    'main_prefix_maxx_interface/rows_51.json': '1a1876a01a505e74b1497fc1ac1ad62400b93bf648f53bf9966fc630f13b770c',
    'main_prefix_maxx_interface/freeze_manifest.json': 'f62812138600f7be7d1670f3455522989e01dbefd87eb692afce6cea4d868065',
"""
    assert source.count(marker) == 1; source = source.replace(marker, insert)
    marker = "    structure = read(HERE / 'coordinate_structure.json')\n"
    insert = marker + """    baseline = read(HERE.parent / 'exact_matrix.json.gz')
    assert len(baseline['rows']) == 23625
    assert matrix['rows'][:23625] == baseline['rows'] and matrix['row_names'][:23625] == baseline['row_names']
    for key in ('columns', 'objective', 'normalization'): assert matrix[key] == baseline[key]
"""
    assert source.count(marker) == 1; source = source.replace(marker, insert)
    marker = "    atoms = read(WORK / 'maxb_h3_bridge/atom_audit.json')\n"
    insert = """    stronger = read(WORK / 'main_prefix_maxx_interface/rows_51.json')
    assert stronger['row_count'] == 51 and stronger['nonzero_count'] == 5124 and stronger['new_columns'] == 0
    oldap = read(WORK / 'early_x_anchor_queries/rows_51.json')
    constants = {1: F(206, 5), 2: F(121, 4), 3: F(61, 3)}
    delta = {1: F(9, 5), 2: F(9, 4), 3: F(8, 3)}
    safe = {}
    for player in (1, 2, 3):
        row = defaultdict(F)
        for h, c in hist.items():
            bits = tuple(map(int, c['actual_bits'])); r = 7-player
            if bits[player-1]: row[h] += F(1, sum(bits))
            row[xc[h]] -= F(1, sum(bits[:player-1])+r)
        safe[player] = {j: v for j, v in row.items() if v}
        name = 'common-max-B:' + json.dumps(['actual-safe-X', player], separators=(',', ':'))
        assert enc(safe[player]) == old['rows'][old['row_names'].index(name)]
        assert enc(safe[player]) == stronger['safe_rows_from_raw_bits'][str(player)]
    yfrequency = Counter(); stronger_orbits = defaultdict(list)
    for k, rec in enumerate(stronger['rows']):
        player = rec['actual_player']; queries = [tuple(q) for q in rec['query_members']]
        assert player == oldap['rows'][k]['actual_player'] and F(rec['C']) == constants[player]
        assert F(rec['safe_subtraction']) == delta[player] and rec['old_AP_row_name'] == oldap['rows'][k]['name']
        assert rec['query_members'] == oldap['rows'][k]['query_members']
        literal = bridge_row(player, constants[player], queries, hist, xc, yc, margins)
        subtracted = enc(combine((1, sparse(oldap['rows'][k]['row'])), (-delta[player], safe[player])))
        assert literal == subtracted == rec['row'] == matrix['rows'][23625+k]
        assert matrix['row_names'][23625+k] == json.dumps(rec['name'], separators=(',', ':'))
        assert set(xc.values()).issubset(j for j, v in literal)
        prior_y = [(j, v) for j, v in oldap['rows'][k]['row'] if j >= 20601]
        new_y = [(j, v) for j, v in literal if j >= 20601]
        assert new_y == prior_y and all(rat(v) > 0 for j, v in new_y)
        yfrequency.update(j for j, v in new_y); stronger_orbits[player].append(frozenset(queries))
    assert set(yfrequency) == set(range(20601, COLS)) and set(yfrequency.values()) == {3}
    assert all(len(groups) == 17 and set(groups) == orbits for groups in stronger_orbits.values())
    independent17 = read(WORK / 'early3_maxx_cone/rows_17.json')
    assert [r['row'] for r in stronger['rows'][34:]] == [r['row'] for r in independent17['rows']]
    general_review = read(WORK / 'early3_maxx_cone/audit_main_family.json')
    assert general_review['status'] == 'PASS_INDEPENDENT_MAIN_FAMILY_AUDIT'
    assert general_review['raw_ordered_boolean_types'] == 1440 and general_review['actual_share_payment_checks'] == 2880
    assert general_review['optimizer_calls'] == 0 and general_review['main_script_imported'] is False
    for name, pin in general_review['source_sha256'].items(): assert sha(WORK/name) == pin
    checks.append({'source': 'stronger_prefix_SAFE_MAX', 'rows': 51, 'nonzeros': 5124,
                   'literal_formula_and_old_AP_minus_delta_SAFE_agree': True,
                   'constants': {str(k): str(v) for k, v in constants.items()}})
""" + marker
    assert source.count(marker) == 1; source = source.replace(marker, insert)
    marker = "        'old_rows_unchanged': OLDM, 'unchanged_column_descriptors': 20601,"
    insert = "        'old_rows_unchanged': OLDM, 'prepared_baseline_rows_unchanged': 23625, 'unchanged_column_descriptors': 20601,"
    assert source.count(marker) == 1; source = source.replace(marker, insert)
    dest = OUT/'verify_certificates.py'; assert not dest.exists()
    compile(source, str(dest), 'exec'); dest.write_text(source)
    print('Final self-contained independent verifier prepared; no verification or optimization executed by this adapter.')


if __name__ == '__main__': main()
