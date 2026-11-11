"""Small seeded LPs, first 203 then 239 nonroot budgets at the NEW point."""
from pathlib import Path
import json
import sys
import time
import numpy as np
import scipy
from scipy.optimize import linprog
from model import HERE, PIN, input_snapshot, load_inputs, root_contract, seed_columns, sha, system, write_json


def solve(data, cols, pairs):
    start = time.monotonic()
    en, eq, be, un, ub, bu = system(data, cols, pairs)
    ae, au = np.array(eq, dtype=float), np.array(ub, dtype=float)
    sol = linprog(np.array([c['root'] for c in cols], dtype=float),
        A_eq=ae, b_eq=np.array(be, dtype=float), A_ub=au, b_ub=np.array(bu, dtype=float),
        bounds=(0, None), method='highs', options={'dual_feasibility_tolerance': 1e-9,
                                                  'primal_feasibility_tolerance': 1e-9})
    report = {'scope': 'Finite 32-column seed only; infeasibility cannot separate the full domain.',
              'point_sha256': PIN, 'pairs_included': pairs,
              'status': int(sol.status), 'message': sol.message,
              'columns': len(cols), 'equality_rows': len(eq), 'nonroot_rows': len(ub)-1,
              'root_source_coefficient': 1, 'elapsed_seconds': time.monotonic()-start}
    if sol.success:
        report.update({'root_cost_float': float(sol.fun),
                       'support': [{'column': j, 'mass_float': float(x)}
                                   for j, x in enumerate(sol.x) if x > 1e-10],
                       'active_rows': [{'index': j, 'row': list(un[j]), 'slack_float': float(x)}
                                       for j, x in enumerate(sol.ineqlin.residual) if abs(x) < 1e-9],
                       'equality_duals': list(map(float, sol.eqlin.marginals)),
                       'inequality_duals': list(map(float, sol.ineqlin.marginals))})
    else:
        # Phase I retains exact fixed old hist margins, with one common t>=0
        # relaxing each budget by t.  Its dual can later prove only seed failure.
        phase = linprog(np.r_[np.zeros(len(cols)), 1.],
            A_eq=np.c_[ae, np.zeros(len(eq))], b_eq=np.array(be, dtype=float),
            A_ub=np.c_[au, -np.ones(len(ub))], b_ub=np.array(bu, dtype=float),
            bounds=(0, None), method='highs')
        assert phase.success
        report['phase_I'] = {'violation_float': float(phase.fun),
            'equality_duals': list(map(float, phase.eqlin.marginals)),
            'inequality_duals': list(map(float, phase.ineqlin.marginals)),
            'support': [{'column': j, 'mass_float': float(x)}
                        for j, x in enumerate(phase.x[:-1]) if x > 1e-10]}
    name = 'seed_239_discovery.json' if pairs else 'seed_203_discovery.json'
    write_json(HERE/name, report)
    print(json.dumps({k: v for k, v in report.items() if k not in ('inequality_duals', 'equality_duals')}, indent=2))
    return sol.success


def main():
    data = load_inputs()
    write_json(HERE/'inputs_exact.json', input_snapshot(data))
    cols = seed_columns(data, root_contract())
    manifest = {'point_sha256': PIN, 'root_states_only_from_prior_certificate': True,
        'candidate_states': data['seeds'],
        'columns': [{k: v for k, v in c.items() if k in ('hist', 'seed_root_state', 'actual', 'old_words', 'new_words')}
                    for c in cols]}
    write_json(HERE/'seed_columns.json', manifest)
    print('FRESH K', str(data['K']), float(data['K']))
    print('FRESH u', list(map(str, data['u'])))
    print('FRESH W', str(data['W']))
    for pairs in (False, True):
        solve(data, cols, pairs)
    write_json(HERE/'discovery_environment.json', {'actual_argv': [sys.executable, *sys.argv],
        'python': sys.version, 'numpy': np.__version__, 'scipy': scipy.__version__,
        'point_sha256': PIN, 'input_snapshot_sha256': sha(HERE/'inputs_exact.json'),
        'script_sha256': sha(__file__)})


if __name__ == '__main__':
    main()
