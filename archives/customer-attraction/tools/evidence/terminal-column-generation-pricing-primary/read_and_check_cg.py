"""Read the complete frozen 737 CG snapshot; no solver or pricing execution.

Reversible field projection preserves every atom and every floating value.
The new20 rows alone are computed from literal final-player comparisons.
All binary64 masses are interpreted exactly, never rationally rounded.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import ast
import hashlib
import json
import math
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
OLD = ROOT / 'archives/customer-attraction/tools/evidence/round5-terminal-pricing-resumed-boss2/original/cg_terminal_cross.json'
TRANSPORT = ROOT / 'archives/customer-attraction/tools/evidence/round4-joint-transport-resumed-boss2/original/research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round4_coupling/joint_transport.py'
FIELDS = ('bits', 'AB_hist', 'AE_hist', 'second_hist', 'menus_lh')


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def literal_row(atom, source, target, pos, kind):
    """Enumerate source slots and all target member counts per shared t.

    A single binary menu is maximized by taking the smallest costs for D,
    largest for O. This uses exact per-slot denominators, not qcost arrays.
    """
    a, b, _, _, e, *_ = map(int, atom['bits'])
    source_slots = [v for v, n in zip(product((0, 1), repeat=3), atom[source + '_hist']) for _ in range(n)]
    k = 4 if target == 'Sbranch' else 3
    target_field = 'second_hist' if target == 'Sbranch' else target + '_hist'
    target_slots = [v for v, n in zip(product((0, 1), repeat=k), atom[target_field]) for _ in range(n)]
    inv = {t: [] for t in (0, 1)}
    own = F(0)
    for t, r, s in source_slots:
        den = 1 + a + (b if source == 'AB' else e) + t + r
        inv[t].append(F(1, den))
        own += F(s, den)
    counts = {t: sum(v[pos] for v in target_slots if v[0] == t) for t in (0, 1)}
    if kind == 'D':
        return own - sum((sum(sorted(inv[t])[:counts[t]], F(0)) for t in (0, 1)), F(0))
    return 4 * own - sum(counts.values()) * sum(inv[0] + inv[1], F(0)) + sum((sum(sorted(inv[t], reverse=True)[:counts[t]], F(0)) for t in (0, 1)), F(0))


def main():
    started = time.perf_counter()
    p = HERE / 'original/cg_dual_terminal.json'
    data = json.loads(p.read_text())
    old = json.loads(OLD.read_text())
    assert set(data) == {'scope', 'row_names', 'atoms', 'primal_float', 'dual_beta_float', 'dual_multipliers_float', 'history'}
    assert data['row_names'][:727] == old['row_names']
    assert data['atoms'][:871] == old['atoms']
    specs = []
    for source in ('AB', 'AE'):
        for target in ('AB', 'AE', 'Sbranch'):
            if source == target:
                continue
            for pos in range(1, 4 if target == 'Sbranch' else 3):
                for kind in ('D', 'O'):
                    specs.append((f'crossfinal:{source}:{target}:{pos}{kind}', source, target, pos, kind))
    assert data['row_names'][717:] == [s[0] for s in specs]
    assert len(set(data['row_names'])) == 737
    pools = {f: [] for f in FIELDS}
    encoded = []
    keys = set()
    for i, atom in enumerate(data['atoms']):
        assert set(atom) in (set(FIELDS), set(FIELDS) | {'exact_mass'})
        assert len(atom['bits']) == 10 and set(atom['bits']) <= {'0', '1'}
        ds = []
        for f, n in (('AB_hist', 8), ('AE_hist', 8), ('second_hist', 16)):
            h = atom[f]
            assert len(h) == n and all(type(v) is int and v >= 0 for v in h) and sum(h) == 5
            ds.append(sum(h[n // 2:]))
        assert len(set(ds)) == 1
        d = ds[0]
        assert len(atom['menus_lh']) == 3
        for ell, overlap in atom['menus_lh']:
            assert type(ell) is int and type(overlap) is int
            assert 0 <= overlap <= d and 0 <= ell - overlap <= 5 - d
        record = []
        for f in FIELDS:
            if atom[f] not in pools[f]:
                pools[f].append(atom[f])
            record.append(pools[f].index(atom[f]))
        key = tuple(record)
        assert key not in keys
        keys.add(key)
        extras = {k: v for k, v in atom.items() if k not in FIELDS}
        if extras:
            assert i < 67 and F(extras['exact_mass']) > 0
        encoded.append({'indices': record, 'extra_fields': extras})
    reconstructed = []
    for rec in encoded:
        atom = {f: pools[f][j] for f, j in zip(FIELDS, rec['indices'])}
        atom.update(rec['extra_fields'])
        reconstructed.append(atom)
    assert reconstructed == data['atoms']
    masses = data['primal_float']
    assert len(masses) == len(encoded) == 1141
    assert all(type(v) is float and math.isfinite(v) and v >= 0 for v in masses)
    sparse = [[i, x] for i, x in enumerate(masses) if x != 0]
    assert len(sparse) == 76
    restored_mass = [0.] * len(masses)
    for i, x in sparse:
        restored_mass[i] = x
    assert restored_mass == masses
    assert len(data['dual_multipliers_float']) == 57
    assert all(n in data['row_names'] and math.isfinite(v) and v > 1e-10 for n, v in data['dual_multipliers_float'].items())
    assert len(data['history']) == 10
    prior = 871
    for i, rec in enumerate(data['history']):
        assert set(rec) == {'iteration', 'columns', 'beta', 'pricing_minimum_scaled', 'new_columns', 'score_contexts', 'seconds'}
        assert rec['iteration'] == i and rec['columns'] == prior + rec['new_columns']
        assert all(math.isfinite(float(v)) for v in rec.values())
        assert rec['seconds'] > 0
        prior = rec['columns']
    assert prior == 1141 and data['history'][-1]['new_columns'] == 0
    assert data['history'][-1]['beta'] == data['dual_beta_float']
    projection = {
        'scope': 'Lossless semantic field projection; byte-exact original stored separately.',
        'source_sha256': digest(p),
        'atom_fields': FIELDS, 'value_pools': pools, 'all_atom_records': encoded,
        'primal_length': len(masses), 'nonzero_primal': sparse,
        'other_complete_fields': {k: v for k, v in data.items() if k not in ('atoms', 'primal_float')},
        'reconstruction_exact_json_value_equality': True,
    }
    (HERE / 'complete-field-projection.json').write_text(json.dumps(projection, ensure_ascii=False, indent=2) + '\n')
    # Extract only pure definition functions: no upstream main, IO, or imports.
    tree = ast.parse(TRANSPORT.read_text())
    keep = {'family', 'source_data', 'transport_max', 'joint_row'}
    module = ast.Module(body=[n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in keep], type_ignores=[])
    ns = {'F': F, 'product': product}
    exec(compile(module, str(TRANSPORT), 'exec'), ns)
    exact_masses = [F.from_float(v) for v in masses]
    totals = []
    matrix = []
    for atom in data['atoms']:
        row = []
        for name, source, target, pos, kind in specs:
            value = literal_row(atom, source, target, pos, kind)
            old_value = ns['joint_row'](atom, source, 'second' if target == 'Sbranch' else target, ((pos, kind, F(1)),))
            assert value == old_value
            row.append(value)
        matrix.append(row)
    for j, spec in enumerate(specs):
        total = sum((mass * row[j] for mass, row in zip(exact_masses, matrix)), F(0))
        totals.append({'row': spec[0], 'exact_binary64_mass_total': str(total), 'float_of_exact_total': float(total)})
    W = sum((m for m, a in zip(exact_masses, data['atoms']) if '1' in a['bits'][:5]), F(0))
    O = sum((m for m, a in zip(exact_masses, data['atoms']) if any(a['AB_hist'][4:])), F(0))
    report = {
        'scope': 'All frozen CG fields, plus20 final-player single rows at1141 saved columns; no full737 primal or dual certificate.',
        'input': {'path': str(p.relative_to(ROOT)), 'sha256': digest(p), 'bytes': p.stat().st_size},
        'old871': {'path': str(OLD.relative_to(ROOT)), 'sha256': digest(OLD), 'full_atom_prefix_equality': True},
        'original_pure_evaluator': {'path': str(TRANSPORT.relative_to(ROOT)), 'sha256': digest(TRANSPORT), 'definitions_only': sorted(keep)},
        'all1141_atoms_valid': True, 'duplicate_structural_atoms': 0,
        'value_pool_sizes': {k: len(v) for k, v in pools.items()},
        'old_exact_mass_fields_preserved': 67, 'new_atom_count_after871': 270,
        'float_mass_positive_count': 76, 'float_mass_zero_count': 1065,
        'float_positive_dual_count': 57,
        'W_binary64_exact': str(W), 'W_minus_one': str(W - 1),
        'O_binary64_exact': str(O), 'O_minus_saved_beta': str(O - F.from_float(data['dual_beta_float'])),
        'new20_coefficient_comparisons': len(matrix) * len(specs),
        'new20_all_coefficients_equal_original_definition': True,
        'new20_saved_float_mass_totals': totals,
        'negative_totals_count': sum(F(x['exact_binary64_mass_total']) < 0 for x in totals),
        'new20_exact_coefficients_by_atom': [[str(v) for v in row] for row in matrix],
        'execution': {'entrypoint_runs': 1, 'success': True, 'original_cli_runs': 0, 'LP_runs': 0, 'QR_runs': 0, 'full_universe_price_runs': 0, 'seconds': time.perf_counter() - started},
    }
    (HERE / 'complete-field-check.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'new20_exact_coefficients_by_atom'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
