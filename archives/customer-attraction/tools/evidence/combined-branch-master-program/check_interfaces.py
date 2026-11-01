"""Current cleanup checks; does not import/build/solve any historical graph.

Checks frozen input interfaces and static branch counts.  The separately kept
unmodified CLI event is the sole current check of all 5108 matrix rows.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import ast
import json

HERE = Path(__file__).resolve().parent
EVIDENCE = HERE.parent
MANIFEST = json.loads((HERE / 'rerun/available-frozen-files-manifest.json').read_text())
BY_ID = {x['id']: x for x in MANIFEST}
PRIMARY = '9aa0e3af9d15dc62a830'
POINT = '5e6ada29cce2eeda7f9e'
SKIPPED = {'358135a42d98d3ff5129', 'dcb82d5dd75f34db2ecf'}


def path(key):
    if key == PRIMARY:
        return HERE / 'original/combined_branch_master.py'
    if key == POINT:
        return EVIDENCE / 'full156-tail-parent-report/original/research_5/combined_branch_master_exact.json'
    return HERE / 'dependencies' / BY_ID[key]['path']


def read(key):
    return json.loads(path(key).read_text())


def nonnegative(values):
    values = list(map(F, values))
    assert min(values, default=F()) >= 0
    return len(values)


def main():
    checked = []
    for key, rec in BY_ID.items():
        if key in SKIPPED:
            continue
        data = path(key).read_bytes()
        assert len(data) == rec['size'] and sha256(data).hexdigest() == rec['sha256']
        checked.append(key)
    p = read(POINT)
    old = read('dfc2594ca7e3f26b6d7f')
    cols = p['columns']
    assert len(cols) == len(old['columns']) == 1905
    desc = lambda c: {k: v for k, v in c.items() if k != 'weight'}
    assert [desc(c) for c in cols] == [desc(c) for c in old['columns']]
    ys = [F(c['weight']) for c in cols]
    assert min(ys) >= 0
    hist = [c for c in cols if c['kind'] == 'hist']
    O = sum(F(c['weight']) for c in hist if c['d'] > 0)
    W = sum(F(c['weight']) for c in hist if '1' in c['actual_bits'])
    assert O == 1 and W == F(p['W']) < F(1, 2)

    oldcuts = read('5cf473265575f67bc3d6')['cuts']
    assert len(oldcuts) == 6
    multipliers = nonnegative(c[k] for c in oldcuts for k in ('alpha', 'beta', 'gamma'))
    maxroot_ids = ['550849c3ad669b881e7b', '5735c449f9e073951236', '3a2d5aabf2297a18e3d0']
    maxroots = [c for key in maxroot_ids for c in read(key)]
    assert len(maxroots) == 8
    # C is a signed coefficient, not a nonnegative multiplier.
    assert all(F(c['B']) > 0 for c in maxroots)
    pair = read('a44b6d08df200e20a7f4')['cuts']
    joint = read('b43e77694bd2abc24dfe')
    for c in pair + joint['pair_cuts']:
        multipliers += nonnegative(c['alpha'])
    menu = read('079852db78fd902db91d')['cuts'] + joint['menu_cuts']
    for c in menu:
        multipliers += nonnegative(z['weight'] for z in c['weights'])
        assert sum(F(z['weight']) for z in c['weights'] if z['spec'][0] == 'leader') > 0
    compact = read('8cfbb4dae13c68090beb')['cuts']
    targeted = read('a7bfdf52f41a28327a0b')['cuts']
    for c in compact + targeted:
        multipliers += nonnegative(c['weights'].values())
    counts = {'base_priced': 331, 'bridge': 50, 'frozen_free_reply': len(oldcuts),
              'nested_horizon': 200, 'maxroot': len(maxroots), 'strong_pair': len(pair),
              'initial_menu': len(menu) - len(joint['menu_cuts']), 'compact_joint': len(compact),
              'existing_root': 1, 'target_joint_present': len(targeted), 'AB_tables': 2,
              'joint_menu': len(joint['menu_cuts']), 'joint_pair': len(joint['pair_cuts']),
              'fourth_indexed_table': 1}
    assert sum(counts.values()) == 702
    # Check lookup domains and used rational coefficients, not their historical
    # hidden-customer maximization certificates or discovery metadata.
    domain = {(''.join(map(str, a)), d) for a in product((0, 1), repeat=6) for d in range(7)}
    table_checks = []
    for key in ['8515d814e4850ea5e1f9', 'ea95460897aa4838a7f3', 'b62dfdc807c4b60b5083']:
        j = read(key)
        cc = j['coefficients']
        assert len(cc) == 448 and {(z['actual_bits'], z['d']) for z in cc} == domain
        [F(z['coefficient']) for z in cc]
        scale = j['row_scale'] * j['integer_row_weights']['source'] if 'row_scale' in j else j['scale'] * j['integer_weights'][0]
        assert F(scale) > 0
        table_checks.append({'id': key, 'entries': 448, 'positive_normalizer': str(scale)})
    oldquery = read('c8a04fcb6deb981585d0')['selected']
    continuous = read('0e0463f4cf45c16d0c84')['selected']
    assert len(oldquery) == 8 and len(continuous) == 64
    for c in oldquery:
        assert len(c['cut']) == 8
        multipliers += nonnegative(c['cut'][6:])
    for c in continuous:
        assert len(c['cut']) == 8
        multipliers += nonnegative(c['cut'][5:])
    increments = {
        'continuous_refinement': len(read('9ddb1502995eb9e435eb')['cuts']),
        'terminal_portfolio': len(read('a2933368a00aed4a0c18')['cuts']),
        'terminal_capacity': len(read('504b5c22ca1331dc9ef5')['cuts']),
        'early_B': len(read('519adddb8a5e5058acc5')['rows'])}
    assert increments == {'continuous_refinement': 32, 'terminal_portfolio': 8, 'terminal_capacity': 29, 'early_B': 3}
    local = read('a737621e71157881030f')
    v2 = read('80444e2ea783541f539e')
    local_counts = {k: len(local.get(k, [])) for k in ['nested', 'requery', 'portfolio']}
    v2_counts = {k: len(v2.get(k, [])) for k in ['nested', 'requery', 'portfolio']}
    assert local_counts == {'nested': 5, 'requery': 4, 'portfolio': 0}
    assert v2_counts == {'nested': 5, 'requery': 5, 'portfolio': 8}
    tree = ast.parse(path(PRIMARY).read_text())
    build = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'build')
    imports = [(n.name, n.asname) for node in ast.walk(build) if isinstance(node, ast.Import) for n in node.names]
    assert [n for n in imports if n[1] == 'portfolio'] == [('terminal_portfolio_cuts', 'portfolio')]
    report = {
        'scope': 'current static/data-interface audit; no historical build, optimizer, or entrypoint invocation',
        'status': 'PASS', 'frozen_files_checked': len(checked), 'checked_ids': checked,
        'column_count': len(cols), 'column_kind_counts': dict(Counter(c['kind'] for c in cols)),
        'all_1905_non_weight_descriptors_equal_old_attractive_layout': True,
        'descriptor_limit': 'compares saved layouts; original default build plus frozen ordering defines the runtime interface; not a second independent graph generator',
        'O': str(O), 'W': str(W), 'K': str(ys[0]), 'nonnegative_point_coordinates': True,
        'inherited_702_row_counts': counts, 'historical_multipliers_nonnegative_checked': multipliers,
        'lookup_interfaces': table_checks, 'historical_projection_certificates_regenerated': False,
        'latest_additions': increments, 'local_additions': local_counts, 'local_v2_additions': v2_counts,
        'static_default_rows': 5108, 'static_latest_rows': 5180, 'static_new_local_rows': 5117,
        'static_latest_new_local_rows': 5189, 'static_latest_local_v2_rows': 5198,
        'standalone_local_v2': 'not executed: static unbound portfolio local at the first nonempty portfolio cut, because only --latest imports it',
        'extended_modes_executed': False}
    out = HERE / 'interface-audit.json'
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
