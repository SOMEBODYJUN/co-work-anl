"""Complete-history MILP attack on the uniform portfolio interface.

Uses the existing complete-tree formulation, fixes a proposed actual action
pattern, and adds its true actual-prefix deviation queries to the objective.
This numerical discovery tool does not certify a general optimum.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import Bounds, milp

ROOT = Path(__file__).resolve().parents[5]
MODULE = ROOT / 'research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_boss/full_tree_milp.py'
spec = importlib.util.spec_from_file_location('complete_tree_source', MODULE)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--path', default='0,1,2')
    p.add_argument('--topics', type=int, default=5)
    p.add_argument('--portfolio', default='2,3,4')
    p.add_argument('--seconds', type=float, default=45)
    p.add_argument('--out', required=True)
    args = p.parse_args()
    path = tuple(map(int, args.path.split(',')))
    portfolio = tuple(map(int, args.portfolio.split(',')))
    m = len(path)
    if len(portfolio) != m:
        raise ValueError('exactly m comparison indices are required')
    model = base.build(m, args.topics, 0, 'individual')
    for i, a in enumerate(path):
        model['lower'][model['choices'][path[:i], a]] = 1
        model['upper'][model['choices'][path[:i], a]] = 1
    obj = np.zeros(model['n'])
    for i in range(m):
        obj[model['utilities'][(), i]] += m - 1
        for a in portfolio:
            obj[model['utilities'][path[:i] + (a,), i]] += 1
    for j, mask in enumerate(model['masks']):
        obj[j] -= m * int(any(mask & (1 << a) for a in portfolio))
    result = milp(obj, integrality=model['integrality'],
                  bounds=Bounds(model['lower'], model['upper']),
                  constraints=model['constraint'],
                  options={'time_limit': args.seconds, 'mip_rel_gap': 1e-9})
    out = {'parameters': vars(args), 'status': int(result.status),
           'message': str(result.message), 'fun': None if result.fun is None else float(result.fun),
           'mip_dual_bound': None if getattr(result, 'mip_dual_bound', None) is None else float(result.mip_dual_bound),
           'identity': 'numerical complete-history MILP proposal only'}
    if result.x is not None:
        out['types'] = result.x[:len(model['masks'])].tolist()
        out['actions'] = [{'history': h, 'action': a} for (h, a), j in model['choices'].items()
                          if result.x[j] > .5]
        out['root_utilities'] = [float(result.x[model['utilities'][(), i]]) for i in range(m)]
    Path(args.out).write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({k: v for k, v in out.items() if k not in ['types', 'actions']}), flush=True)


if __name__ == '__main__':
    main()
