"""Reuse the old count-Markov joint generator with valid W=1 bounds.

All catalog topic sizes are <=W=1 in any root SPE: each of the m actual
players can guarantee |T|/m by choosing T, and their payoffs sum to W.
Thus every propagated topic payoff and every customer type is <=1. Replacing
the old conditional big-M=m by 1 is valid. This restricts strategies to the
count-Markov subclass for discovery only, then expands and exactly verifies
the entire ordered-history strategy as before.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents
            if (p/'customer_attraction/__init__.py').is_file())
SOURCE = ROOT/'research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/credible_search/markov_joint.py'
raw = SOURCE.read_text()
replacements = {
    'hi=np.full(idx,m,dtype=float)':'hi=np.full(idx,1,dtype=float)',
    'row[zz]=m;add(row,ub=m)':'row[zz]=1;add(row,ub=1)',
    'row[zz]=-m;add(row,lb=-m)':'row[zz]=-1;add(row,lb=-1)',
}
for old,new in replacements.items():
    assert old in raw
    raw = raw.replace(old,new)
spec = importlib.util.spec_from_file_location('reused_tight_markov',SOURCE)
old = importlib.util.module_from_spec(spec)
exec(compile(raw,str(SOURCE),'exec'),old.__dict__)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--topics',type=int,default=7)
    ap.add_argument('--path',required=True)
    ap.add_argument('--portfolio',required=True)
    ap.add_argument('--seconds',type=float,default=25)
    ap.add_argument('--floor',type=float)
    ap.add_argument('--output',type=Path,required=True)
    args = ap.parse_args()
    path = tuple(map(int,args.path.split(',')))
    J = tuple(map(int,args.portfolio.split(',')))
    p,m = args.topics,len(path)
    q = tuple(path.count(a) for a in range(p))
    original_milp = old.milp

    def tightened_milp(cost,*,integrality,bounds,constraints,options):
        import numpy as np
        from scipy.sparse import coo_matrix,vstack
        rows = []
        # Explicit catalog-size caps justify the conditional constant 1.
        for t in range(p):
            rows.append(tuple(int(bool(mask&(1<<t))) for mask in range(1,1<<p)))
        ii,jj,vv = [],[],[]
        for i,row in enumerate(rows):
            for j,v in enumerate(row):
                if v:ii.append(i);jj.append(j);vv.append(v)
        lo,hi = [-np.inf]*p,[1]*p
        if args.floor is not None:
            for j,v in enumerate(old.coverage_row(p,J)):
                if v:ii.append(p);jj.append(j);vv.append(float(v))
            lo.append(args.floor);hi.append(np.inf)
        A = coo_matrix((vv,(ii,jj)),shape=(len(lo),len(cost))).tocsc()
        combined = old.LinearConstraint(vstack([constraints.A,A],format='csc'),
            np.r_[constraints.lb,lo],np.r_[constraints.ub,hi])
        return original_milp(cost,integrality=integrality,bounds=bounds,
                             constraints=combined,options=options)
    old.milp = tightened_milp
    cone,meta = old.candidate(p,path,J,args.seconds)
    point = None
    if cone:
        result = cone.optimize(J)
        if result['certified']:
            point = old.exact_export(cone,result)
    out = {'scope':'count-Markov discovery subclass; complete ordered-history SPE exact verification',
           'universal_claim_proved':False,'source':str(SOURCE.relative_to(ROOT)),
           'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
           'valid_conditional_big_M':1,'parameters':dict(vars(args)),
           'milp':meta,'exact_candidate':point}
    out['parameters']['output']=str(args.output)
    args.output.write_text(json.dumps(old.serializable(out),indent=2)+'\n')
    if point:
        out['exact_candidate']={k:v for k,v in point.items()
           if k not in ('instance','strategy','certificate','dual')}
    print(json.dumps(old.serializable(out)),flush=True)


if __name__=='__main__':
    main()
