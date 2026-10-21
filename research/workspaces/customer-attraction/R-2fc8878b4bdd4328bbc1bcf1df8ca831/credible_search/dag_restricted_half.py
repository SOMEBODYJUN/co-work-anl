"""Restricted type-support half search using the existing exact DAG interface.

Support restriction is an experiment only. No failure of this search is a
theorem. Every proposed strategy is unfolded and exactly checked by the reused
interface. Added cuts are valid for any actual-root SPE: |T|<=m*u_a(q) for
each topic a occupied at q and every catalog topic T.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import importlib.util

ROOT = next(p for p in Path(__file__).resolve().parents
            if (p/'customer_attraction/__init__.py').is_file())
SOURCE = ROOT/'research/workspaces/customer-attraction/R-3d6f7a072d5e489eb5a0bdc4d32bb769/true_spe_search/outcome_dag_milp.py'
spec = importlib.util.spec_from_file_location('original_dag_restricted',SOURCE)
dag = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dag)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root',required=True)
    ap.add_argument('--portfolio',required=True)
    ap.add_argument('--seconds',type=float,default=25)
    ap.add_argument('--floor',type=float,default=1.8)
    ap.add_argument('--outside-order',type=int,default=1)
    ap.add_argument('--output',required=True,type=Path)
    args = ap.parse_args()
    q = tuple(map(int,args.root.split(',')))
    p,m = len(q),sum(q)
    occupied = tuple(a for a,c in enumerate(q) if c)
    outside_mask = sum(1<<a for a,c in enumerate(q) if not c)
    allowed = tuple(mask for mask in range(1,1<<p)
                    if (mask & outside_mask).bit_count()<=args.outside_order)
    J = tuple(map(int,args.portfolio.split(',')))
    objective = dag.coverage_row(p,J)
    original_milp = dag.milp

    def cut_milp(cost,*,integrality,bounds,constraints,options):
        from scipy.sparse import coo_matrix,vstack
        import numpy as np
        lo,hi = bounds.lb.copy(),bounds.ub.copy()
        for mask in range(1,1<<p):
            if mask not in allowed:
                hi[mask-1] = 0
        ii,jj,vv = [],[],[]
        row_id = 0
        for a in occupied:
            ua = dag.payoff_row(p,q,a)
            for t in range(p):
                for mask,u in enumerate(ua,1):
                    c = int(bool(mask & (1<<t)))-m*u
                    if c:
                        ii.append(row_id);jj.append(mask-1);vv.append(float(c))
                row_id += 1
        A = coo_matrix((vv,(ii,jj)),shape=(row_id,len(cost))).tocsc()
        combined = dag.LinearConstraint(vstack([constraints.A,A],format='csc'),
            np.r_[constraints.lb,np.full(row_id,-np.inf)],
            np.r_[constraints.ub,np.zeros(row_id)])
        return original_milp(cost,integrality=integrality,bounds=dag.Bounds(lo,hi),
                             constraints=combined,options=options)

    dag.milp = cut_milp
    cone,meta = dag.build(p,q,objective,args.seconds,objective_floor=args.floor)
    exact = dag.exact_optimize(cone,objective) if cone else None
    report = {'scope':'restricted-support unrestricted-history true-SPE half probe',
              'universal_claim_proved':False,'parameters':dict(vars(args)),
              'allowed_masks':allowed,'root_guarantee_cuts':len(occupied)*p,
              'milp':meta,'exact_candidate':exact}
    report['parameters']['output'] = str(args.output)
    args.output.write_text(json.dumps(dag.serializable(report),indent=2)+'\n')
    if exact:
        report['exact_candidate'] = {k:v for k,v in exact.items()
            if k not in ('integer_clones','strategy','dual_support')}
    print(json.dumps(dag.serializable(report)),flush=True)


if __name__=='__main__':
    main()
