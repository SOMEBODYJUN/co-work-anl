"""Screen a sufficient half-coverage bridge in saved full policy cones.

Floating LP only. A negative value requires a separate exact certificate.
No equilibrium or customer-positivity constraint is relaxed in the model.
"""
import gzip
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'history/source/notes/customer_attraction/transport_round'))
spec = importlib.util.spec_from_file_location(
    'cone_source', ROOT / 'history/source/notes/customer_attraction/transport_round/common_q_generator.py')
source = importlib.util.module_from_spec(spec)
spec.loader.exec_module(source)


def main():
    cases = json.load(gzip.open(
        ROOT / 'evidence/certificates/customer_attraction/new_policy_security_cones.json.gz', 'rt'))['cases']
    spaces = {}
    records = []
    for case in cases:
        m, p = case['players'], case['topics']
        if (m, p) not in spaces:
            spaces[m, p] = source.Space(m, p)
        s = spaces[m, p]
        actions = {tuple(z['history']): z['action'] for z in case['policy']}
        cone = s.full_policy(actions)
        terminal = cone['realized'][0]
        load = s.den[terminal]
        c = cone['c']
        best = None
        for topic in range(p):
            width = s.inc[:, topic] * np.where(load > 0, (m + 1) / (load + 1), m)
            gap = (1 + 1 / m) * c - width
            result = linprog(gap, A_ub=-cone['gamma'] / s.L,
                             b_ub=np.zeros(len(cone['gamma'])),
                             A_eq=[c], b_eq=[1], bounds=(0, None), method='highs')
            if not result.success:
                raise RuntimeError(result.message)
            if best is None or result.fun < best['gap']:
                best = {'gap': result.fun, 'topic': topic,
                        'weights': result.x.tolist()}
        records.append({'name': case['name'], 'players': m, 'topics': p,
                        'root_counts': s.tc[terminal], 'best': best})
        print(json.dumps({'name': case['name'], 'gap': best['gap']}), flush=True)
    output = Path(__file__).with_name('saved_cones.json')
    with output.open('x') as stream:
        json.dump({'status': 'floating LP screening, no general conclusion',
                   'candidate': 'D_T <= (1+1/m) W', 'records': records}, stream, indent=2)


if __name__ == '__main__':
    main()
