"""Reuse the existing unrestricted outcome-witness DAG to attack a weak floor.

Only positive, exact full-history SPE points can refute the proposed floor.
Floating MIP bounds and finite failures carry no mathematical conclusion.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import importlib.util
import json
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents
            if (p / 'customer_attraction/__init__.py').is_file())
SOURCE = ROOT / 'research/workspaces/customer-attraction/R-3d6f7a072d5e489eb5a0bdc4d32bb769/true_spe_search/outcome_dag_milp.py'
spec = importlib.util.spec_from_file_location('original_outcome_dag', SOURCE)
dag = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dag)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--target', type=int, required=True)
    ap.add_argument('--portfolio', required=True)
    ap.add_argument('--seconds', type=float, default=15)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    q = tuple(map(int, args.root.split(',')))
    p, m = len(q), sum(q)
    J = tuple(map(int, args.portfolio.split(',')))
    assert q[args.target] > 0 and len(J) <= m
    u = dag.payoff_row(p, q, args.target)
    v = dag.coverage_row(p, J)
    objective = tuple(vv-(2*m-1)*uu for vv,uu in zip(v,u))
    cone, meta = dag.build(p, q, objective, args.seconds)
    exact = dag.exact_optimize(cone, objective) if cone else None
    if exact and exact['certified']:
        clones = exact['integer_clones']
        ua = dag.dot(u, clones)
        comparison = dag.dot(v, clones)
        exact['individual_payoff'] = ua
        exact['comparison_coverage'] = comparison
        exact['weak_individual_gap'] = (2*m-1)*ua-exact['optimal_welfare']
        exact['comparison_ratio'] = comparison/ua
        exact['actual_OPT_ratio'] = Fraction(exact['optimal_welfare'], ua)
    report = {
        'scope': 'weak individual floor OPT_m <= (2m-1)u_i; unrestricted full-history DAG candidate generation',
        'universal_claim_proved': False,
        'parameters': dict(vars(args)), 'milp': meta, 'exact_candidate': exact,
    }
    report['parameters']['output'] = str(args.output)
    args.output.write_text(json.dumps(dag.serializable(report), indent=2)+'\n')
    summary = dict(report)
    if exact:
        summary['exact_candidate'] = {k:v for k,v in exact.items()
            if k not in ('integer_clones', 'strategy', 'dual_support')}
    print(json.dumps(dag.serializable(summary)), flush=True)


if __name__ == '__main__':
    main()
