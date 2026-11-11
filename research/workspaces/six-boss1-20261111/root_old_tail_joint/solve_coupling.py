"""Small common coupling on every incidence orbit of the given 17 root states.

Mode fixed preserves their masses, mode rebudget preserves the original old
hist masses and all 163 old budgets plus root source budget, allowing new root
state masses. This is finite-support feasibility, never complete-domain pricing.
"""
import argparse
from collections import defaultdict
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import time

import numpy as np
from scipy.optimize import linprog

from common import (HERE, BASE, read_sources, aligned_assignments,
                    literal_interface, names, write_json, q)


def root_contract():
    path = BASE / 'cross_root_pricing/contract.py'
    spec = importlib.util.spec_from_file_location('old_root_contract', path)
    mod = importlib.util.module_from_spec(spec)
    # Read-only sibling consumption: do not create a bytecode cache there.
    exec(compile(path.read_text(), str(path), 'exec'), mod.__dict__)
    return mod


def model(mode):
    frozen, root, product, hist = read_sources()
    rc = root_contract()
    rownames = rc.row_names(True)
    data = rc.load_inputs()
    caps = rc.budgets(data, rownames)
    cnames = names()
    positive_hist = {i: h for i, h in hist.items() if F(h['weight'])}
    cols = []
    for i, h in positive_hist.items():
        for j, r in enumerate(root['support']):
            if r['actual'] != h['actual_bits'] or r['d'] != h['d']:
                continue
            old, assignments = aligned_assignments(h, r)
            rpay, costs = rc.compressed_column(r['actual'], r['d'],
                   rc.column_roots(r['one_word'], r['zero_words']), rownames, data['remainder'])
            for new in assignments:
                inter = literal_interface(r['actual'], old, new)
                cols.append({'original_column_index': i, 'joint_atom_index': j,
                             'actual': r['actual'], 'old_words': old, 'new_words': list(new),
                             'root': rpay, 'costs': costs,
                             'interface': [inter[name] for name in cnames]})
    eq_names = [('old-hist', i) for i in positive_hist]
    if mode == 'fixed':
        eq_names += [('root-atom', j) for j in range(len(root['support']))]
    eq = [[F(c['original_column_index'] == n[1]) if n[0] == 'old-hist'
           else F(c['joint_atom_index'] == n[1]) for c in cols] for n in eq_names]
    beq = [F(positive_hist[n[1]]['weight']) if n[0] == 'old-hist'
           else F(root['support'][n[1]]['mass']) for n in eq_names]
    ub_names = []
    ub = []
    bub = []
    if mode == 'rebudget':
        ub_names = rownames + [('root-source',)]
        ub = [[c['costs'][k] for c in cols] for k in range(len(rownames))]
        ub += [[c['root'] for c in cols]]
        bub = caps + [data['u'][0]]
    ub_names += cnames
    ub += [[-c['interface'][k] for c in cols] for k in range(len(cnames))]
    bub += [F(0)] * len(cnames)
    return cols, eq_names, eq, beq, ub_names, ub, bub


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', choices=['fixed', 'rebudget'], required=True)
    args = ap.parse_args()
    start = time.monotonic()
    cols, en, eq, be, un, ub, bu = model(args.mode)
    ae = np.array(eq, dtype=float); b = np.array(be, dtype=float)
    au = np.array(ub, dtype=float); d = np.array(bu, dtype=float)
    obj = np.array([c['root'] for c in cols], dtype=float)
    sol = linprog(obj, A_ub=au, b_ub=d, A_eq=ae, b_eq=b, bounds=(0, None),
                  method='highs', options={'dual_feasibility_tolerance': 1e-9,
                                           'primal_feasibility_tolerance': 1e-9})
    report = {'mode': args.mode, 'scope': 'Full incidence coupling on fixed 17 root states only; not full root domain or SPE.',
              'status': int(sol.status), 'message': sol.message, 'variables': len(cols),
              'equalities': len(eq), 'inequalities': len(ub), 'elapsed_seconds': time.monotonic()-start}
    if sol.success:
        report.update({'objective_float': float(sol.fun),
                       'positive_support': [{'column': j, 'mass_float': float(x)} for j, x in enumerate(sol.x) if x > 1e-10],
                       'active_rows': [{'index': j, 'name': list(un[j]), 'slack_float': float(x)}
                                       for j, x in enumerate(sol.ineqlin.residual) if x < 1e-9]})
    else:
        # Which single C rows already rule out this FIXED marginal support?
        # Only diagnostic float discovery here; exact bound is a separate step.
        maxima = []
        for k, name in enumerate(names()):
            f = np.array([-c['interface'][k] for c in cols], dtype=float)
            r = linprog(f, A_eq=ae, b_eq=b, bounds=(0, None), method='highs')
            if r.success:
                maxima.append({'row': list(name), 'maximum_float': -float(r.fun),
                               'positive_support': [{'column': j, 'mass_float': float(x)} for j, x in enumerate(r.x) if x > 1e-10],
                               'equality_dual': list(map(float, r.eqlin.marginals))})
        report['single_interface_maxima_over_margins_only'] = maxima
    serialcols = []
    for c in cols:
        serialcols.append({k: (str(v) if isinstance(v, F) else [str(x) for x in v]
                              if k in ('costs', 'interface') else v) for k, v in c.items()})
    report['columns'] = serialcols
    write_json(HERE / f'{args.mode}_coupling_discovery.json', report)
    print(json.dumps({k:v for k,v in report.items() if k not in ('columns','single_interface_maxima_over_margins_only')}, indent=2))
    for r in report.get('single_interface_maxima_over_margins_only', []):
        print(r['row'], r['maximum_float'])


if __name__ == '__main__':
    main()
