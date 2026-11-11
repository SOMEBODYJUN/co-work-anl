"""One full-domain cutting-plane optimization, with exact upper/dual recovery.

No grid and no per-type choice of multipliers. Numeric LPs discover a common
58-vector; universal upper claims require a complete integer-arithmetic
separation. Finite exact duals are explicitly cone lower bounds only.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
import os
from pathlib import Path
import time

import numpy as np
from scipy.optimize import linprog

from cone import (HERE, NAMES, SCALES, Oracle, check_inputs, exclusive,
                  literal_vector, old_point, seeds, target, verify_lower,
                  verify_upper, witness_key)


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, indent=2) + '\n')
    tmp.replace(path)


def log(value):
    print(json.dumps(value), flush=True)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def exact_affine(equations, n, approximate):
    """Fraction RREF; free coordinates remain rational and near numeric x.

    Inconsistent equations are not silently discarded. Upper recovery selects
    independent equalities numerically first, then checks every inequality.
    """
    matrix = [[F(v) for v in row] + [F(rhs)] for row, rhs in equations]
    pivots = []
    r = 0
    for c in range(n):
        p = next((i for i in range(r, len(matrix)) if matrix[i][c]), None)
        if p is None:
            continue
        matrix[r], matrix[p] = matrix[p], matrix[r]
        a = matrix[r][c]
        matrix[r] = [x/a for x in matrix[r]]
        for i in range(len(matrix)):
            if i != r and matrix[i][c]:
                a = matrix[i][c]
                matrix[i] = [x-a*y for x, y in zip(matrix[i], matrix[r])]
        pivots.append(c)
        r += 1
        if r == len(matrix):
            break
    for row in matrix[r:]:
        if not any(row[:n]) and row[n]:
            raise ValueError('inconsistent exact active equations')
    sol = [F(float(v)).limit_denominator(10**12) for v in approximate]
    for i, c in reversed(list(enumerate(pivots))):
        sol[c] = matrix[i][n] - sum(matrix[i][j]*sol[j] for j in range(c+1, n))
    assert all(dot(row, sol) == rhs for row, rhs in equations)
    return sol, len(pivots)


def exact_independent_equations(candidates, n):
    """Choose independent coefficient rows exactly, preserving input order."""
    basis = {}
    selected = []
    for coeff, rhs in candidates:
        row = [F(x) for x in coeff]
        for p, old in sorted(basis.items()):
            if row[p]:
                v = row[p]
                row = [x-v*y for x, y in zip(row, old)]
        p = next((i for i, x in enumerate(row) if x), None)
        if p is None:
            continue
        v = row[p]
        basis[p] = [x/v for x in row]
        selected.append((coeff, rhs))
        if len(selected) == n:
            break
    return selected


def matrix_for(witnesses):
    rows, rhs = [], []
    k = None
    for w in witnesses:
        a, kk = literal_vector(w)
        if k is None:
            k = kk
        assert kk == k
        rows.append(tuple(a) + (-F(exclusive(w)),))
        rhs.append(target(w))
    rows.append(tuple(k) + (F(0),))
    rhs.append(F(0))
    return rows, rhs


def solve_lp(witnesses, time_limit):
    rows, rhs = matrix_for(witnesses)
    A = np.asarray(rows, dtype=float)
    b = np.asarray(rhs, dtype=float)
    c = np.zeros(len(NAMES)+1)
    c[-1] = 1
    fit = linprog(c, A_ub=A, b_ub=b, bounds=(0, None), method='highs-ds',
                  options={'time_limit': time_limit, 'dual_feasibility_tolerance': 1e-9,
                           'primal_feasibility_tolerance': 1e-9})
    return fit, rows, rhs


def recover_upper(fit, rows, rhs):
    # Positive numeric entries identify the face. Exact full-domain checking
    # below decides validity; this recovery alone never certifies anything.
    support = [j for j, v in enumerate(fit.x) if v > 1e-12]
    if not support:
        raise ValueError('empty upper support')
    mandatory = [i for i, y in enumerate(fit.ineqlin.marginals) if y < -1e-10]
    optional = sorted((i for i, v in enumerate(fit.ineqlin.residual) if v < 2e-7 and i not in mandatory),
                      key=lambda i: abs(float(fit.ineqlin.residual[i])))
    equations = exact_independent_equations(
        [(tuple(rows[i][j] for j in support), rhs[i]) for i in mandatory + optional], len(support))
    v, rank = exact_affine(equations, len(support), [fit.x[j] for j in support])
    x = [F(0)]*len(fit.x)
    for j, a in zip(support, v):
        x[j] = a
    if any(a < 0 for a in x):
        raise ValueError('negative recovered upper multiplier')
    violations = [i for i, (row, b) in enumerate(zip(rows, rhs)) if dot(row, x) > b]
    if violations:
        raise ValueError(f'exact upper violates {len(violations)} saved constraints')
    return {'schema': 1, 'cone': 'shifted-53-plus-five-actual-Z-safe-queries',
            'epsilon': str(x[-1]), 'normalized_multipliers': {n: str(v) for n, v in zip(NAMES, x[:-1])},
            'outer_multipliers': {n: str(v/s) for n, s, v in zip(NAMES, SCALES, x[:-1])},
            'recovery_rank': rank, 'positive_variables': len(support),
            'full_domain_verified': False}


def recover_lower(fit, rows, rhs, witnesses):
    support = [i for i, v in enumerate(fit.ineqlin.marginals) if v < -1e-10]
    if not support:
        return None
    # Complementarity: every positive primal coordinate has zero dual slack.
    active = [j for j, v in enumerate(fit.x) if v > 1e-10]
    equations = []
    for j in active:
        # -A^T alpha <= c; equality at positive primal variables.
        equations.append(([-rows[i][j] for i in support], F(int(j == len(NAMES)))))
    alpha, rank = exact_affine(equations, len(support), [-fit.ineqlin.marginals[i] for i in support])
    if any(v < 0 for v in alpha):
        raise ValueError('negative recovered dual atom')
    value = -sum(rhs[i]*v for i, v in zip(support, alpha))
    cert = {'schema': 1, 'cone': 'shifted-53-plus-five-actual-Z-safe-queries',
            'lower_bound': str(value), 'capacity_mass': '0', 'atoms': [],
            'recovery_rank': rank, 'not_an_SPE_counterexample': True}
    for i, v in zip(support, alpha):
        if i == len(witnesses):
            cert['capacity_mass'] = str(v)
        elif v:
            cert['atoms'].append({'mass': str(v), 'witness': witnesses[i]})
    verify_lower(cert)
    return cert


def exact_point_from_certificate(c):
    return [F(c['normalized_multipliers'][n]) for n in NAMES], F(c['epsilon'])


def add_rows(witnesses, found, seen, limit=None, numeric_tolerance=0):
    found = sorted(found, key=lambda r: float(F(r['residual'])))
    added = 0
    for row in found:
        if float(F(row['residual'])) >= -numeric_tolerance:
            continue
        w = row['witness']
        key = witness_key(w)
        if key in seen:
            continue
        witnesses.append(w)
        seen.add(key)
        added += 1
        if limit and added >= limit:
            break
    return added


def save_state(path, witnesses, history, next_iteration):
    state = {'schema': 1, 'row_names': NAMES, 'witnesses': witnesses,
             'history': history, 'next_iteration': next_iteration}
    dump(path, state)
    checkpoint_dir = os.environ.get('RESEARCH_CHECKPOINT_DIR')
    if checkpoint_dir:
        dump(Path(checkpoint_dir)/'background_reweight_checkpoint.json', state)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output-dir', type=Path, default=HERE/'actions_full')
    ap.add_argument('--max-iterations', type=int, default=80)
    ap.add_argument('--seconds', type=int, default=6500)
    ap.add_argument('--max-cuts', type=int, default=2048)
    ap.add_argument('--resume-from', type=Path)
    ap.add_argument('--seed-only', action='store_true', help='Small finite LP only; never a universal upper claim.')
    ap.add_argument('--smoke', action='store_true', help='Eight masks, explicitly not the whole domain.')
    args = ap.parse_args()
    started = time.monotonic()
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    inputs = check_inputs()
    dump(out/'bound_inputs.json', inputs)
    resume = args.resume_from or (Path(os.environ['RESEARCH_RESUME_FROM']) if os.environ.get('RESEARCH_RESUME_FROM') else None)
    if resume:
        state = json.loads(resume.read_text())
        assert state['row_names'] == NAMES
        witnesses, history, first = state['witnesses'], state['history'], state['next_iteration']
    else:
        witnesses, history, first = seeds(), [], 0
    seen = {witness_key(w) for w in witnesses}
    # Source proof gives this feasible point, before reoptimization. The local
    # seed audit is exact but does not replace the archived full-domain proof.
    base = old_point()
    old_eps = F(inputs['baseline_epsilon'])
    rows0, rhs0 = matrix_for(witnesses)
    assert all(dot(a, base+[old_eps]) <= b for a, b in zip(rows0, rhs0))
    log({'phase': 'seed rows audited', 'rows': len(witnesses), 'baseline_epsilon': str(old_eps)})
    oracle = None
    best_lower = None
    best_upper = None
    stop_reason = 'iteration limit'
    for iteration in range(first, args.max_iterations):
        remaining = args.seconds - (time.monotonic()-started)
        if remaining < 120:
            stop_reason = 'checkpoint before time limit'
            break
        fit, rows, rhs = solve_lp(witnesses, max(5, min(300, remaining-90)))
        rec = {'iteration': iteration, 'constraints': len(witnesses)+1,
               'lp_status': int(fit.status), 'lp_message': fit.message,
               'seconds': time.monotonic()-started}
        if not fit.success:
            history.append(rec)
            stop_reason = 'LP did not return an optimum'
            break
        rec['numeric_epsilon'] = float(fit.fun)
        rec['positive_outer_weights'] = int(np.count_nonzero(fit.x[:-1] > 1e-12))
        dump(out/f'iteration_{iteration:03d}_numeric.json', rec | {
            'normalized_multipliers': {n: float(v) for n, v in zip(NAMES, fit.x[:-1])}})
        try:
            lower = recover_lower(fit, rows, rhs, witnesses)
            if lower is not None:
                audit = verify_lower(lower)
                rec['exact_lower_bound'] = lower['lower_bound']
                if best_lower is None or F(lower['lower_bound']) > F(best_lower['lower_bound']):
                    best_lower = lower
                    dump(out/'exact_lower_certificate.json', lower)
                    dump(out/'exact_lower_audit.json', audit)
        except (ValueError, AssertionError) as e:
            rec['lower_recovery_error'] = str(e)
        log(rec)
        if args.seed_only:
            history.append(rec)
            stop_reason = 'finite seed LP only; no universal upper claim'
            break
        if oracle is None:
            masks = [0, 1, 31, 32, 511, 512, 992, 1023] if args.smoke else None
            oracle = Oracle(mask_ids=masks, progress=log)
        sep = oracle.separate(fit.x[:-1], fit.x[-1], progress=log)
        rec['numeric_separation_minimum'] = sep['minimum']
        rec['numeric_negative_cases'] = sep['negative_conditional_cases']
        rec['complete_domain_scanned_numerically'] = sep['complete_domain']
        added = add_rows(witnesses, sep['rows'], seen, limit=args.max_cuts, numeric_tolerance=2e-9)
        rec['new_numeric_cuts'] = added
        if not added:
            try:
                upper = recover_upper(fit, rows, rhs)
                dump(out/'candidate_exact_upper.json', upper)
                audit = verify_upper(upper, oracle, progress=log)
                dump(out/'candidate_exact_upper_audit.json', audit)
                rec['exact_separation_minimum'] = audit['minimum']
                rec['exact_separation_status'] = audit['status']
                if audit['status'] == 'UNIVERSAL-CONE-CERTIFICATE':
                    upper['full_domain_verified'] = True
                    best_upper = upper
                    dump(out/'exact_upper_certificate.json', upper)
                    dump(out/'exact_upper_audit.json', audit)
                    stop_reason = 'complete exact upper certificate'
                    if best_lower is not None and F(best_lower['lower_bound']) == F(upper['epsilon']):
                        stop_reason = 'exact optimum of the full coefficient-domain cone'
                    history.append(rec)
                    save_state(out/'checkpoint.json', witnesses, history, iteration+1)
                    break
                new_exact = add_rows(witnesses, audit['rows'], seen, limit=args.max_cuts)
                rec['new_exact_cuts'] = new_exact
                if not new_exact:
                    stop_reason = 'exact recovery needs a better basis; no universal upper claim'
                    history.append(rec)
                    break
            except (ValueError, AssertionError) as e:
                rec['upper_recovery_error'] = str(e)
                stop_reason = 'exact recovery failed; saved lower bound and checkpoint'
                history.append(rec)
                break
        history.append(rec)
        save_state(out/'checkpoint.json', witnesses, history, iteration+1)
        dump(out/'iteration_history.json', history)
    next_iteration = history[-1]['iteration']+1 if history else first
    save_state(out/'checkpoint.json', witnesses, history, next_iteration)
    summary = {'status': stop_reason, 'rows': len(witnesses), 'iterations': len(history),
               'seconds': time.monotonic()-started, 'cone_rows': len(NAMES),
               'common_vector_for_b0_and_b1': True,
               'exact_lower_bound': best_lower['lower_bound'] if best_lower else None,
               'exact_upper_bound': best_upper['epsilon'] if best_upper else None,
               'universal_upper_verified': best_upper is not None,
               'six_player_half_status': 'OPEN', 'not_an_SPE_counterexample': True}
    dump(out/'summary.json', summary)
    dump(out/'iteration_history.json', history)
    log(summary)


if __name__ == '__main__':
    main()
