"""Exactly one Actions phase I; no local optimizer is authorized for this task.

Variable order is (1216 mu, 2700 min auxiliaries, 9572 lower bounds, delta).
Saved slack S=A_old*x+B*mu+C*z+D*L is constrained S+delta>=0 for
the 438 main rows and S>=0 for all 5400 cap and 30938 sorting-piece rows.
The scipy convention is -(B,C,D)y-delta <= A_old*x.  Mass equalities
are E*y=-F_old*x.  All lifted variables, including delta, are nonnegative.
One highs-ds call minimizes delta; its output is discovery, never proof.
"""
from pathlib import Path
from datetime import datetime, timezone
from fractions import Fraction as F
import argparse
import gzip
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
import traceback

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
PIN = 'cb45ee6f8df153764c91bd77d0543527cc44719ff7cc43646ffce06a7921a932'
MPIN = 'cf57bb8ceea25d2504db60326ae5a8abd9f461f36339bc5b57dd820ce1efd8b4'
APIN = '15521969def62799dc10a6d83e8d90e26cb86e6221d4ac704ce0a17966bd6637'
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('PYTHONDONTWRITEBYTECODE', '1')


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def write(p, obj):
    data = (json.dumps(obj, ensure_ascii=False, indent=2)+'\n').encode()
    if str(p).endswith('.gz'):
        with open(p, 'wb') as f:
            with gzip.GzipFile(fileobj=f, mode='wb', mtime=0) as g:
                g.write(data)
    else:
        Path(p).write_bytes(data)


def stamp(out, stage, **kw):
    obj = dict(utc=datetime.now(timezone.utc).isoformat(), stage=stage, **kw)
    with open(out/'progress.jsonl', 'a') as f:
        f.write(json.dumps(obj)+'\n')
    print(json.dumps(obj), flush=True)


def worker(args):
    import numpy as np
    import scipy
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix
    out = args.output
    stamp(out, 'verify-inputs')
    assert sha(args.matrix) == MPIN and sha(args.point) == PIN and sha(args.audit) == APIN
    with gzip.open(args.matrix, 'rt') as f:
        raw = json.load(f)
    audit = json.loads(args.audit.read_text())
    assert audit['status'] == 'INDEPENDENT_SYMBOLIC_LITERAL_SORTING_AUDIT_PASS'
    assert audit['matrix_sha256'] == MPIN and audit['point_sha256'] == PIN
    point = json.loads(args.point.read_text())
    old = [F(c['weight']) for c in point['columns'][:4849]]
    descriptors = [{k: v for k, v in c.items() if k != 'weight'} for c in point['columns'][:4849]]
    assert descriptors == raw['original_columns']
    assert len(point['columns']) == 20585 and raw['principal_row_count'] == 438
    nm, na, nl = raw['mu_column_count'], raw['aux_column_count'], raw['lower_column_count']
    nv = nm+na+nl+1
    assert (nm, na, nl, nv) == (1216, 2700, 9572, 13489)
    offsets = {'mu': 0, 'aux': nm, 'lower': nm+na}
    constants = []

    def matrix(records, equality=False):
        rr, cc, vv, rhs = [], [], [], []
        for i, r in enumerate(records):
            sign = 1 if equality else -1
            for kind, offset in offsets.items():
                for col, coef in r[kind]:
                    rr.append(i); cc.append(offset+col); vv.append(sign*float(F(coef)))
            constant = sum((old[col]*F(coef) for col, coef in r['old']), F())
            rhs.append(float(-constant if equality else constant))
            if not equality:
                constants.append(str(constant))
                if i < 438:
                    rr.append(i); cc.append(nv-1); vv.append(-1.)
        return coo_matrix((vv, (rr, cc)), shape=(len(records), nv)).tocsr(), np.array(rhs)

    A, b = matrix(raw['rows'])
    E, f = matrix(raw['equalities'], True)
    c = np.zeros(nv); c[-1] = 1.
    assert A.shape == (36776, nv) and E.shape == (38, nv)
    np.savez_compressed(out/'phase1_input_arrays.npz', A_data=A.data, A_indices=A.indices,
                        A_indptr=A.indptr, A_shape=np.array(A.shape), b=b,
                        E_data=E.data, E_indices=E.indices, E_indptr=E.indptr,
                        E_shape=np.array(E.shape), f=f, objective=c,
                        lower_bounds=np.zeros(nv), upper_bounds=np.full(nv, np.inf))
    write(out/'input_order.json.gz', dict(old_columns=raw['original_columns'],
          old_weights=list(map(str, old)), mu_columns=raw['mu_columns'],
          min_columns=raw['aux_columns'], sorting_columns=raw['lower_columns'],
          row_names=[r['name'] for r in raw['rows']],
          equality_names=[r['name'] for r in raw['equalities']], exact_old_constants=constants,
          variable_offsets=offsets, phase_column=nv-1, matrix_sha256=MPIN, point_sha256=PIN))
    options = dict(primal_feasibility_tolerance=1e-9, dual_feasibility_tolerance=1e-9,
                   time_limit=float(args.time_limit), disp=True)
    convention = dict(slack='S = A_old*x + B*mu + C*min + D*L',
          main_inequality='S + delta >= 0', other_inequality='S >= 0',
          scipy_inequality='-(B,C,D)*y - main_indicator*delta <= A_old*x',
          equality='E*y = -F_old*x', nonnegative_variables='all mu, min, L, delta',
          objective='min delta', method='highs-ds', options=options,
          dual_conversion='For scipy marginals pi<=0 and eta free, set lambda=-pi>=0 and mass multiplier rho=eta; sum(lambda*slack)+sum(rho*mass) has nonpositive lifted coefficients at positive-phase optimum. Its old value equals minus the dual objective. Exact recovery is mandatory.',
          no_other_optimization=True)
    write(out/'lp_convention.json', convention)
    start = time.perf_counter()
    stamp(out, 'solve-start', variables=nv, inequalities=A.shape[0], equalities=E.shape[0],
          nnz=A.nnz+E.nnz, method='highs-ds', time_limit=args.time_limit)
    # This is the only optimization call in this script.
    result = linprog(c, A_ub=A, b_ub=b, A_eq=E, b_eq=f, bounds=(0, None),
                     method='highs-ds', options=options)
    elapsed = time.perf_counter()-start
    arrays = {}
    if result.x is not None:
        arrays.update(x=np.asarray(result.x), mu=np.asarray(result.x[:nm]),
                      aux=np.asarray(result.x[nm:nm+na]), lower=np.asarray(result.x[nm+na:-1]),
                      phase=np.asarray([result.x[-1]]))
    for section, prefix in (('ineqlin', 'inequality'), ('eqlin', 'equality'),
                            ('lower', 'lower_bound'), ('upper', 'upper_bound')):
        block = getattr(result, section, None)
        if block is not None:
            for field in ('residual', 'marginals'):
                val = getattr(block, field, None)
                if val is not None:
                    arrays[prefix+'_'+field] = np.asarray(val)
    np.savez_compressed(out/'floating_solver_arrays.npz', **arrays)
    summary = dict(status=int(result.status), success=bool(result.success), message=result.message,
          mathematical_status='NUMERICAL_DISCOVERY_ONLY', iterations=int(result.nit),
          elapsed_seconds=elapsed, method='highs-ds', options=options,
          point_sha256=PIN, matrix_sha256=MPIN, script_sha256=sha(__file__),
          audit_sha256=sha(args.audit), input_arrays_sha256=sha(out/'phase1_input_arrays.npz'),
          solver_arrays_sha256=sha(out/'floating_solver_arrays.npz'),
          python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__,
          variables=nv, inequalities=A.shape[0], equalities=E.shape[0],
          phase=None if result.x is None else float(result.x[-1]),
          positive_mu=None if result.x is None else int(np.count_nonzero(result.x[:nm] > 1e-9)),
          objective=None if result.fun is None else float(result.fun), exactly_one_solver_call=True)
    write(out/'phase1_discovery.json', summary)
    stamp(out, 'solve-finished', **summary)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--matrix', type=Path, default=HERE/'symbolic_matrix_exact.json.gz')
    p.add_argument('--point', type=Path, default=BASE/'full624_augmented_lp/recovery/augmented_lp_exact.json')
    p.add_argument('--audit', type=Path, default=HERE/'symbolic_independent_audit.json')
    p.add_argument('--output', type=Path, default=HERE/'actions_discovery')
    p.add_argument('--time-limit', type=int, default=1800)
    p.add_argument('--worker', action='store_true')
    args = p.parse_args()
    assert 1 <= args.time_limit <= 1800
    for k in ('matrix', 'point', 'audit', 'output'):
        setattr(args, k, getattr(args, k).resolve())
    args.output.mkdir(parents=True, exist_ok=True)
    if args.worker:
        try:
            worker(args)
        except BaseException as exc:
            write(args.output/'worker_failure.json', dict(type=type(exc).__name__, error=str(exc),
                  traceback=traceback.format_exc(), utc=datetime.now(timezone.utc).isoformat()))
            raise
        return
    marker = args.output/'phase1_started.json'
    with open(marker, 'x') as f:
        json.dump(dict(utc=datetime.now(timezone.utc).isoformat(), script_sha256=sha(__file__),
                       exactly_one_solver_call_authorized=True), f)
    (args.output/'executed_actions_phase1.py').write_bytes(Path(__file__).read_bytes())
    argv = [sys.executable, '-B', str(Path(__file__).resolve()), '--worker',
            '--matrix', str(args.matrix), '--point', str(args.point), '--audit', str(args.audit),
            '--output', str(args.output), '--time-limit', str(args.time_limit)]
    start = time.perf_counter()
    with open(args.output/'solver.stdout.txt', 'w') as out, open(args.output/'solver.stderr.txt', 'w') as err:
        result = subprocess.run(argv, stdout=out, stderr=err)
    record = dict(argv=argv, cwd=os.getcwd(), returncode=result.returncode,
                  elapsed_seconds=time.perf_counter()-start, script_sha256=sha(__file__),
                  matrix_sha256=sha(args.matrix), point_sha256=sha(args.point),
                  audit_sha256=sha(args.audit), stdout_sha256=sha(args.output/'solver.stdout.txt'),
                  stderr_sha256=sha(args.output/'solver.stderr.txt'))
    write(args.output/'execution.json', record)
    print(json.dumps(record), flush=True)
    if (args.output/'phase1_discovery.json').exists():
        print((args.output/'phase1_discovery.json').read_text(), flush=True)
    raise SystemExit(result.returncode)


if __name__ == '__main__':
    main()
