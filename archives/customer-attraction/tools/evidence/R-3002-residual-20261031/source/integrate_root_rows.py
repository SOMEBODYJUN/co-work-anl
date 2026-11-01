"""Reoptimize the frozen 16-histogram 3889-row lift with certified root cuts.

This is a necessary-condition experiment. A feasible sub-half point is an
obstruction for precisely the listed rows, never an instance or an SPE.
The histogram support is restricted; failure cannot establish HALF6.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse, hashlib, json, sys, time
import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'work.py').exists())
OLD = ROOT / 'research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra'
SOURCE = OLD / 'attractive_nested_exact.json'
CUTDIR = HERE.parent / 'research_4'
sys.path.insert(0, str(OLD))
import attractive_nested as at
import full_new_reply_closure as cl

FILES = (
    'root_requery_baseline_o4.2_exact.json',
    'root_requery_o4.2_exact.json',
    'root_requery_third_L_o4.2_exact.json',
    'root_requery_branch_D_o4.2_exact.json',
    'root_requery_L_D_o4.34514_exact.json',
)


def cuts(include_joint):
    result = []
    for filename in FILES[:5 if include_joint else 4]:
        path = CUTDIR / filename
        data = json.loads(path.read_text())
        mul = data['multipliers_numerators']
        den = data['denominator']
        a = F(sum(v for k, v in mul.items() if k.startswith(('LASTO:', 'PAIRO:'))), den)
        beta = F(data['equality_numerator'] - sum(v for k, v in mul.items() if k.startswith('CAP:')), den)
        result.append({'file': str(path.relative_to(ROOT)),
                       'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                       'a': str(a), 'beta': str(beta)})
    return result


def build(include_joint=True):
    original = json.loads(SOURCE.read_text())
    hc = [c for c in original['columns'] if c['kind'] == 'hist']
    cols, names, m, obj, normal = at.build(hc)
    extra = cuts(include_joint)
    for cut in extra:
        a, beta = F(cut['a']), F(cut['beta'])
        row = [F()] * len(cols)
        for j, col in enumerate(cols):
            if col['kind'] == 'K':
                row[j] = -beta
            elif col['kind'] == 'hist':
                actual = tuple(map(int, col['actual_bits']))
                row[j] = (F(actual[0], sum(actual)) if actual[0] else F()) - a * int(col['d'] > 0)
        names.append('root-requery:' + cut['file'])
        m.append(row)
    return cols, names, m, obj, normal, extra


def verify(data):
    cols, names, m, obj, normal, extra = build(data['include_joint'])
    assert data['cuts'] == extra
    assert len(cols) == len(data['certificate']['columns'])
    for c, d in zip(cols, data['certificate']['columns']):
        assert c == {k: v for k, v in d.items() if k != 'weight'}
    v = [F(c['weight']) for c in data['certificate']['columns']]
    assert min(v) >= 0
    assert sum(x * y for x, y in zip(normal, v)) == 1
    slacks = [sum(x * y for x, y in zip(row, v)) for row in m]
    assert min(slacks) >= 0
    welfare = sum(x * y for x, y in zip(obj, v))
    assert welfare == F(data['certificate']['W']) < F(1, 2)
    return {'verified_rows': len(m), 'verified_columns': len(cols),
            'minimum_slack': str(min(slacks)), 'W': str(welfare),
            'strict_half_gap': str(1 - 2 * welfare),
            'new_root_slacks': [str(x) for x in slacks[-len(extra):]]}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--without-joint', action='store_true')
    ap.add_argument('--verify', type=Path)
    ap.add_argument('--output', type=Path, default=HERE / 'root_rows_joint_point.json')
    args = ap.parse_args()
    if args.verify:
        print(json.dumps(verify(json.loads(args.verify.read_text())), indent=2)); return
    started = time.time()
    cols, names, m, obj, normal, extra = build(not args.without_joint)
    print('BUILT', len(m), len(cols), 'seconds', time.time() - started, flush=True)
    matrix = np.array(m, dtype=float)
    scale = np.max(np.abs(matrix), axis=1); scale[scale == 0] = 1
    sol = linprog(np.array(obj, dtype=float), A_ub=-matrix / scale[:, None],
                  b_ub=np.zeros(len(m)), A_eq=[np.array(normal, dtype=float)], b_eq=[1],
                  bounds=(0, None), method='highs',
                  options={'dual_feasibility_tolerance': 1e-9, 'primal_feasibility_tolerance': 1e-9})
    print('LP', sol.message, 'W', sol.fun, flush=True)
    report = {'scope': 'frozen sixteen-histogram support; necessary conditions only; not an SPE or game, no universal bound',
              'include_joint': not args.without_joint,
              'source': str(SOURCE.relative_to(ROOT)),
              'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              'cuts': extra, 'rows': len(m), 'columns': len(cols),
              'lp_success': bool(sol.success), 'lp_message': sol.message,
              'floating_W': float(sol.fun) if sol.fun is not None else None}
    if sol.success and sol.fun < .5:
        report['certificate'] = cl.exact_point(cols, names, m, obj, normal, sol.x)
        report['exact_verification'] = verify(report)
    report['seconds'] = time.time() - started
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'certificate'}, indent=2), flush=True)


if __name__ == '__main__':
    main()
