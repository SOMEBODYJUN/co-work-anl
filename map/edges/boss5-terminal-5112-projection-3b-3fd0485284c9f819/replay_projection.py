"""Verify frozen row embeddings, strict projections and incomparable siblings.

Run from the repository root with NumPy and SciPy available to the archived
builders. No original main, optimizer, repository-control command, or network
is used. The frozen inputs are materialized under a temporary task directory.
"""
from base64 import b64decode, b64encode
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from importlib import import_module
from itertools import product
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from zlib import compress, decompress


REPO = Path.cwd()
EVIDENCE = REPO / 'archives/customer-attraction/tools/evidence'
HISTORICAL = Path('research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1')
CAPACITY = EVIDENCE / 'terminal-capacity-refinement-boss3'
MENU = EVIDENCE / 'b-family-menu-prices-boss3'
LATEST = EVIDENCE / 'coupled-latest-menu-check-boss3'
POINTS = {
    5112: CAPACITY / 'original/2ac41f3470c74caa54b1/terminal_capacity_refinement_exact.json',
    5277: LATEST / 'original/coupled_latest_exact.json',
    5664: MENU / 'original/research_2/maxroot_identity_exact.json',
    5692: MENU / 'original/research_2/all_menu_prices_exact.json',
}
POINT_SHAS = {
    5112: '0bf850f2489986a56cc2847cfdae0a1f8d86fe1b069a425cad5d40fa253e91ee',
    5277: '303291e7ec19437d226bb8d33d3e689beaf54f52103fde53a12e28f1058f806a',
    5664: 'd3c456a03806aef08378e96f89387b83d77161081a260b3764b8aa8f8097d43a',
    5692: '46e52c1cec4a5cac3e6d7fe3bbe8d227cd663e428ca7f4e955182343eedb418e',
}
OLD_COLUMNS = 1905
ZERO = F()


def read(path):
    return json.loads(path.read_bytes())


def materialize(runtime, package):
    subprocess.run(
        [sys.executable, '-B', str(package / 'materialize_runtime.py'), str(runtime)],
        cwd=REPO, check=True, stdout=subprocess.DEVNULL,
    )


def archived_capacity(runtime):
    """Recreate only the assembly in refine_terminal_portfolio --capacity --verify."""
    path = runtime / HISTORICAL / 'research_3'
    for manifest in ('related-inputs-manifest.json', 'source-manifest.json'):
        for record in read(CAPACITY / manifest)['sources']:
            name = Path(record['path']).name
            source = (REPO / record['retained_related_path'] if 'retained_related_path' in record
                      else CAPACITY / 'original' / record['id'] / name)
            raw = source.read_bytes()
            assert sha256(raw).hexdigest() == record['sha256']
            target = path / name
            if target.exists():
                assert raw == target.read_bytes(), name
            else:
                target.write_bytes(raw)
    sys.path.insert(0, str(path))
    refine = import_module('refine_terminal_portfolio')
    cols, names, rows, objective, norm = refine.base.build()
    assert len(rows) == 5043
    for filename, expected, row_builder in (
        ('continuous_refinement_cuts.json', 32, refine.cc.row),
        ('terminal_portfolio_refinement_cuts.json', 8, refine.pc.row),
        ('terminal_capacity_refinement_cuts.json', 29, refine.pc.row),
    ):
        cuts = read(path / filename)['cuts']
        assert len(cuts) == expected
        rows.extend(row_builder(cols, cut) for cut in cuts)
    return cols, rows, objective, norm


def descriptors(point):
    return [{k: v for k, v in col.items() if k != 'weight'} for col in point['columns']]


def dot(row, vector):
    return sum((row[index] * mass for index, mass in vector), ZERO)


def record_rows(report, key, rows):
    serialized = '\n'.join(''.join(f'{i}={value};' for i, value in enumerate(row[:OLD_COLUMNS]) if value)
                           for row in rows).encode('ascii')
    report[key] = b64encode(compress(serialized)).decode('ascii')
    report[key + '_hash'] = sha256(serialized).hexdigest()


def check_marginals(cols, weights):
    hist = {i for i, c in enumerate(cols) if c['kind'] == 'hist'}
    assert len(hist) == 16
    groups = defaultdict(dict)
    families = defaultdict(dict)
    old_hist_indices = {}
    current_hist = None
    old_index = 1
    for j, col in enumerate(cols):
        kind = col['kind']
        if kind == 'hist':
            assert len(col['actual_bits']) == 6 and set(col['actual_bits']) <= {'0', '1'}
            assert col['d'] == sum(col['hist'][4:]) == 1 and sum(col['hist']) == 6
            current_hist = j
            old_hist_indices[old_index] = j
            old_index += 1
        if kind == 'joint-reply':
            hj, group = old_hist_indices[col['hist_column_old']], json.dumps(col['group'])
            assert hj == current_hist
            state = tuple(col['state'])
            assert state not in groups[hj, group]
            old_index += state == (1, 1)
            groups[hj, group][state] = weights[j]
        if kind == 'actual-B-branch-state':
            families['B4', col['hist_column']][(col['Q'], col['R'], col['ell'])] = weights[j]
        if kind == 'actual-B-family-state':
            families[f"B{col['source']}", col['hist_column']][(*col['hidden'], col['ell'])] = weights[j]
        if kind == 'maximum-root-family-state':
            families['M', col['hist_column']][(col['M'], *col['hidden'], col['ell'])] = weights[j]
    assert len(groups) == 194 and old_index == 211
    implicit = {}
    for (hj, group), states in groups.items():
        assert set(states) == {(0, 1), (1, 0), (1, 1)}
        implicit[hj, group] = weights[hj] - sum(states.values())
        assert implicit[hj, group] >= 0
    for col, mass in zip(cols, weights):
        if col['kind'] == 'overlap':
            for group in col['groups']:
                states = groups[col['hist_column'], json.dumps(group)]
                assert mass <= states[1, 0] + states[1, 1]
    for (family, hj), states in families.items():
        bits = 6 if family == 'M' else 6 - int(family[1])
        assert set(states) == {(*hidden, ell) for hidden, ell in product(product(range(2), repeat=bits), (0, 6))}
        assert sum(states.values()) == weights[hj]
    assert len(families) in (0, 16, 64)
    return len(implicit), len(families)


def price_menu(cols, weights):
    hist = {j: (tuple(map(int, c['actual_bits'])), weights[j]) for j, c in enumerate(cols) if c['kind'] == 'hist'}
    actual = sum((mass * F(a[5], sum(a)) for a, mass in hist.values() if a[5]), ZERO)
    costs = defaultdict(F)
    for c, mass in zip(cols, weights):
        if c['kind'] == 'actual-B-branch-state':
            family = 'B4'
        elif c['kind'] == 'actual-B-family-state':
            family = f"B{c['source']}"
        elif c['kind'] == 'maximum-root-family-state':
            family = 'M'
        else:
            continue
        a, _ = hist[c['hist_column']]
        costs[family] += mass * F(c['ell'], 6 * (1 + sum(a[:5])))
    return {family: str(actual - cost) for family, cost in costs.items()}


def upper_envelope(cols, rows_by_name, prefix, branch, family):
    """Build a Farkas obstruction using the actual third-source matrix rows."""
    multipliers = {
        'actualB-3-explicit:IC': 670, 'actualB-3-explicit:M': 9,
        'actualB-3-explicit:Z': 1, 'actualB-3-explicit:CAP:hidden:3': 4,
        **{f'actualB-3-cross:{i}': w for i, w in zip((8, 12, 13, 14), (76, 32, 100, 105))},
    }
    selected = [(rows_by_name[name], weight) for name, weight in multipliers.items()]
    coefficients = [sum((row[j] * w for row, w in selected), ZERO) for j in range(len(cols))]
    assert coefficients[0] == 4 and not any(coefficients[1:OLD_COLUMNS])
    hist = defaultdict(dict)
    for j, c in enumerate(cols[OLD_COLUMNS:], OLD_COLUMNS):
        if c['kind'] == 'actual-B-family-state' and c['source'] == 3:
            hist[c['hist_column']][tuple(c['hidden']), c['ell']] = coefficients[j]
        else:
            assert coefficients[j] == 0
    maxima = {}
    for hj, values in hist.items():
        c = cols[hj]
        a = tuple(map(int, c['actual_bits']))
        hidden_states = tuple(product(range(2), repeat=3))
        assert set(values) == set(product(hidden_states, (0, 6)))
        for hidden in hidden_states:
            for ell in range(7):
                names, primitive = branch.branch_rows(a + (0,), (2, 5), hidden, c['d'], ell)
                assert names[:3] == ['IC', 'M', 'Z']
                cross = family.cross(a, c['hist'], hidden, 3)
                v = (670 * primitive[0] + 9 * primitive[1] + primitive[2]
                     + 4 * primitive[names.index('CAP:hidden:3')]
                     + sum(w * cross[i] for i, w in zip((8, 12, 13, 14), (76, 32, 100, 105))))
                assert v == ((6 - ell) * values[hidden, 0] + ell * values[hidden, 6]) / 6
        maxima[hj] = max(values.values())
    assert len(maxima) == 16
    bounds = {
        n: str(4 * weights[0] + sum(weights[j] * value for j, value in maxima.items()))
        for n, weights in prefix.items()
    }
    assert F(bounds[5277]) == -F(1505595416077174278327675259267902161027078757,
                                 735576345002473658294053882445594433882234368)
    assert F(bounds[5692]) > 0
    return {'weights': multipliers, 'histogram_maxima': {j: str(v) for j, v in maxima.items()},
            'evaluated_bounds': bounds}


def verify(runtime, mode):
    points = {}
    for n, path in POINTS.items():
        raw = path.read_bytes()
        assert sha256(raw).hexdigest() == POINT_SHAS[n]
        points[n] = json.loads(raw)
    prefix = descriptors(points[5112])
    assert len(prefix) == OLD_COLUMNS and all(descriptors(p)[:OLD_COLUMNS] == prefix for p in points.values())
    weights = {n: [F(c['weight']) for c in p['columns']] for n, p in points.items()}
    assert all(min(v) >= 0 for v in weights.values())
    nonzero = {n: [(i, w) for i, w in enumerate(v) if w] for n, v in weights.items()}
    sys.argv = [__file__]
    if mode == 5112:
        cols, rows, objective, norm = archived_capacity(runtime)
        names = None
    else:
        local = runtime / HISTORICAL / ('research_5' if mode == 5277 else 'research_2')
        sys.path.insert(0, str(local))
        if mode == 5277:
            entry = import_module('coupled_latest_master')
            assert {'--latest', '--local-v2'} <= set(sys.argv)
            cols, names, rows, objective, norm = entry.build()
        else:
            entry = import_module('B_menu_prices_master')
            assert '--latest' in sys.argv and not ({'--local-v2', '--new-local'} & set(sys.argv))
            cols, names, rows, objective, norm = entry.build(all_families=True)
    assert json.loads(json.dumps(cols)) == descriptors(points[mode])
    assert len(cols) == len(norm) == len(objective) and len(rows) == mode
    assert all(len(row) == len(cols) for row in rows)
    assert norm == [F(c['d']) if c['kind'] == 'hist' else ZERO for c in cols]
    assert objective == [F(int('1' in c['actual_bits'])) if c['kind'] == 'hist' else ZERO for c in cols]
    assert cols[0]['kind'] == 'K' and sum(c['kind'] == 'K' for c in cols) == 1
    assert dot(norm, nonzero[mode]) == F(points[mode]['O']) == 1
    assert dot(objective, nonzero[mode]) == F(points[mode]['W']) < F(1, 2)
    slacks = [dot(row, nonzero[mode]) for row in rows]
    assert min(slacks) == F(points[mode]['minimum_slack']) == 0
    assert len(nonzero[mode]) == points[mode]['positive_columns']
    report = {'rows': mode, 'columns': dict(Counter(c['kind'] for c in cols)),
              'point_sha256': POINT_SHAS[mode], 'positive_coordinates': len(nonzero[mode]),
              'zero_slacks': slacks.count(0), 'O': '1', 'W': points[mode]['W'], 'K': str(weights[mode][0]),
              'marginals_checked': check_marginals(cols, weights[mode]),
              'ordinary_Y_average_last_price': price_menu(cols, weights[mode])}
    if mode == 5112:
        record_rows(report, 'rows_5112', rows)
        return report
    old_stop = 5198 if mode == 5277 else 5180
    assert all(not any(row[OLD_COLUMNS:]) for row in rows[:old_stop])
    assert [name.split(':')[0] for name in names[5177:5180]] == ['early-actual-B-projection'] * 3
    assert [int(name.rsplit(':', 1)[1]) for name in names[5177:5180]] == [2, 3, 4]
    assert not any(names[i].startswith('actualB') for i in range(old_stop))
    record_rows(report, 'rows_5112', (*rows[:5043], *rows[5108:5177]))
    record_rows(report, 'rows_5180', rows[:5180])
    old_vectors = {n: [(i, w) for i, w in nonzero[n] if i < OLD_COLUMNS] for n in (5112, 5277, 5692)}
    added = [*rows[5043:5108], *rows[5177:5180]]
    report['common_added_slacks_on_5112'] = [str(dot(row, old_vectors[5112])) for row in added]
    assert len(added) == 68
    assert all(F(v) > 0 for v in report['common_added_slacks_on_5112'][:65])
    assert [F(v) < 0 for v in report['common_added_slacks_on_5112'][65:]] == [True, True, False]
    if mode == 5277:
        report['local_v2_slacks'] = {
            n: {name: str(dot(row, old_vectors[n])) for name, row in zip(names[5180:5198], rows[5180:5198])}
            for n in (5112, 5277, 5692)
        }
        assert sum(F(v) < 0 for v in report['local_v2_slacks'][5692].values()) == 7
    else:
        lookup = dict(zip(names, rows))
        assert len(lookup) == len(names)
        family = import_module('coupled_B_families_master')
        report['third_source_upper_envelope'] = upper_envelope(cols, lookup, weights, family, family)
        assert descriptors(points[5664]) == descriptors(points[5692])
        assert weights[5664][0] == weights[5692][0]
        assert all(weights[5664][i] == weights[5692][i] for i,c in enumerate(cols) if c['kind'] == 'hist')
        assert sum(a != b for a, b in zip(weights[5664], weights[5692])) == 214
        assert min(dot(row, nonzero[5664]) for row in rows[:5664]) == 0
        report['ordinary_Y_average_last_price_5664'] = price_menu(cols, weights[5664])
        report['four_menu_slack_signs'] = {
            n: {name: str(dot(row, nonzero[n])) for name, row in zip(names[-28:], rows[-28:])}
            for n in (5664, 5692)
        }
        assert [name for name, v in report['four_menu_slack_signs'][5664].items() if F(v) < 0] == ['actual-B-2:actual-menu-price:6']
        assert sum(F(v) == 0 for v in report['four_menu_slack_signs'][5692].values()) == 4
    return report


def main():
    if len(sys.argv) == 3:
        print(json.dumps(verify(Path(sys.argv[1]), int(sys.argv[2])), ensure_ascii=False))
        return
    reports = {}
    with TemporaryDirectory(prefix='.projection-', dir=Path(__file__).resolve().parent) as tmp:
        for mode in (5112, 5277, 5692):
            runtime = Path(tmp) / str(mode)
            materialize(runtime, LATEST if mode in (5112, 5277) else MENU)
            result = subprocess.run([sys.executable, '-B', __file__, str(runtime), str(mode)],
                                    check=True, stdout=subprocess.PIPE, text=True)
            reports[mode] = json.loads(result.stdout)
    for key, models in (('rows_5112', (5112, 5277, 5692)), ('rows_5180', (5277, 5692))):
        row_data = [decompress(b64decode(reports[n].pop(key))) for n in models]
        assert all(raw == row_data[0] for raw in row_data)
    reports['exact_serialized_row_comparison'] = {'rows_5112': True, 'rows_5180': True}
    assert reports[5277]['common_added_slacks_on_5112'] == reports[5692]['common_added_slacks_on_5112']
    print(json.dumps(reports, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
