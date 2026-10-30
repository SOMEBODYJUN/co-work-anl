"""Run the unmodified diagonal probe and raw-DAG verifier once each.

Then check the returned finite objects by raw unit-customer shares and check
the RESET/covariance identities, retaining the original misleading scope text.
Use a fresh --run-dir; no Git, network or scientific Python dependency.
"""
from __future__ import annotations

import argparse
from collections import Counter
from contextlib import redirect_stdout, redirect_stderr
from fractions import Fraction as F
import hashlib
from itertools import product
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import time

BASE = Path(__file__).resolve().parent
DIAG = 'research/workspaces/customer-attraction/R-24e40cab6b8d43ecbbf1c15c4d0edcd5/dynamic_flow/diagonal_push_obstruction.py'
DAGDIR = 'research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/counterexample'


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def textify(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): textify(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return list(map(textify, value))
    return value


def write(path, obj):
    path.write_text(json.dumps(textify(obj), ensure_ascii=False, indent=2) + '\n')


def raw_utility(likes, path, action, extra=0):
    return sum((F(1, extra + sum(t in interest for t in path))
                for interest in likes if action in interest), F(0))


def node_quantities(likes, prefix, tails, p, u):
    """All tails include their forced action; no model/solver helper is used."""
    size = len(p)
    b = [sum(t in interest for t in prefix) for interest in likes]
    a = [[int(A in interest) for interest in likes] for A in range(size)]
    n = [[sum(t in interest for t in tails[A][1:]) for interest in likes]
         for A in range(size)]
    c = [v + 1 for v in b]
    d = [sum((F(a[A][x], c[x] + n[A][x]) for x in range(len(likes))), F(0))
         for A in range(size)]
    K = [[sum((F(int(T in interest), c[x] + a[A][x] + n[A][x])
               for x, interest in enumerate(likes)), F(0))
          for A in range(size)] for T in range(size)]
    R, J = [], []
    for A in range(size):
        rrow, jrow = [], []
        for T in range(size):
            r = sum((F((a[A][x] - a[T][x]) * (n[A][x] - n[T][x]),
                       (c[x] + n[A][x]) * (c[x] + n[T][x]))
                     for x in range(len(likes))), F(0))
            j = sum((F(1, (c[x] + n[A][x]) * (c[x] + n[A][x] + 1))
                     + F(1, (c[x] + n[T][x]) * (c[x] + n[T][x] + 1))
                     for x in range(len(likes)) if a[A][x] and a[T][x]), F(0))
            assert K[T][A] + K[A][T] - d[A] - d[T] == r - j
            rrow.append(r); jrow.append(j)
        R.append(rrow); J.append(jrow)
    px = [sum(p[A] * a[A][x] for A in range(size)) for x in range(len(likes))]
    tax = sum((2 * px[x] * sum((p[A] * F(a[A][x], (c[x] + n[A][x]) *
                                                       (c[x] + n[A][x] + 1))
                              for A in range(size)), F(0))
               for x in range(len(likes))), F(0))
    wrong_tax = sum((2 * px[x] ** 2 * sum((p[A] * F(a[A][x], (c[x] + n[A][x]) *
                                                                (c[x] + n[A][x] + 1))
                                       for A in range(size)), F(0))
                     for x in range(len(likes))), F(0))
    covariance = F(0)
    for x in range(len(likes)):
        tail = [F(n[A][x], c[x] + n[A][x]) for A in range(size)]
        covariance += (sum(p[A] * a[A][x] * tail[A] for A in range(size))
                       - px[x] * sum(p[A] * tail[A] for A in range(size))) / c[x]
    er = sum(p[A] * p[T] * R[A][T] for A in range(size) for T in range(size))
    ej = sum(p[A] * p[T] * J[A][T] for A in range(size) for T in range(size))
    mean_d = sum(p[A] * d[A] for A in range(size))
    mean_k = sum(p[T] * p[A] * K[T][A] for T in range(size) for A in range(size))
    slack = u - mean_d
    assert er == 2 * covariance and ej == tax
    assert u - mean_k == slack + (ej - er) / 2
    return dict(K=K, D=d, R=R, J=J, p=p, actual_u=u,
                pKp=mean_k, pD=mean_d, mean_IC_slack=slack,
                pKp_minus_pD=mean_k - mean_d, pKp_minus_actual_u=mean_k - u,
                direct_mean_R=er, covariance_half_R=covariance,
                direct_mean_J=ej, corrected_mean_J=tax,
                old_squared_p_unconditional_formula=wrong_tax,
                old_formula_error=wrong_tax - ej, pair_identities_checked=size ** 2)


def independent_diagonal(export):
    inst, cert = export['instance'], export['certificate']
    likes = [set(c['topics']) for c in inst['customers'] for _ in range(c['multiplicity'])]
    m, size = inst['players'], len(inst['topics'])
    actions = {tuple(row['history']): row['action'] for row in cert['actions']}
    expected = {h for depth in range(m) for h in product(range(size), repeat=depth)}
    assert set(actions) == expected and m == 3 and size == 5 and len(likes) == 8
    comparisons = []

    def finish(h):
        while len(h) < m:
            h += (actions[h],)
        return h

    for h in sorted(expected, key=lambda q: (len(q), q)):
        prescribed = actions[h]
        terminal = finish(h)
        current = raw_utility(likes, terminal, prescribed)
        alternatives = [raw_utility(likes, finish(h + (t,)), t) for t in range(size)]
        assert current == alternatives[prescribed] and all(current >= v for v in alternatives)
        comparisons.append(dict(history=h, action=prescribed, payoff=current,
                                all_alternative_payoffs=alternatives))
    root_path = finish(())
    counts = tuple(root_path.count(t) for t in range(size))
    assert list(counts) == cert['terminal_counts']
    branches = [finish((t,)) for t in range(size)]
    p = tuple(F(v) for v in export['p'])
    node = node_quantities(likes, (), branches, p, raw_utility(likes, root_path, root_path[0]))
    assert node['pKp'] == F(1501, 1722) and node['pD'] == F(248, 287)
    assert node['pKp_minus_pD'] == F(13, 1722)
    assert node['pKp_minus_actual_u'] == -F(2517, 1722)
    assert node['old_formula_error'] != 0
    remaining = []
    for h in product(range(size), repeat=1):
        tails = [finish(h + (t,))[len(h):] for t in range(size)]
        u = raw_utility(likes, finish(h), actions[h])
        remaining.append(dict(prefix=h, **node_quantities(likes, h, tails, p, u)))
    return dict(status='all_passed', instance=inst, certificate=cert,
                root_path=root_path, root_branches=branches, root_node=node,
                second_layer_nodes=remaining, all_history_payoffs=comparisons,
                checked_histories=len(comparisons), nonself_deviations=len(comparisons) * (size-1),
                pair_identities_checked=25 * 6,
                scope='pKp > pD, while pKp < actual u. This finite example does not refute the universal actual-u root cap.')


def independent_base(source):
    raw = json.loads((source / DAGDIR / 'pure_menu_two_block_dag.json').read_text())
    inst, nodes = raw['instance'], raw['nodes']
    likes = [set(c['topics']) for c in inst['customers'] for _ in range(c['multiplicity'])]
    root = nodes[raw['root']]
    def path(start):
        answer = []
        while nodes[start]['action'] is not None:
            a = nodes[start]['action']; answer.append(a); start = nodes[start]['children'][a]
        return tuple(answer)
    branches = [tuple([t]) + path(root['children'][t]) for t in range(8)]
    root_path = path(raw['root']); u = raw_utility(likes, root_path, root_path[0])
    p = tuple(F(1,2) if t in (3,7) else F(0) for t in range(8))
    result = node_quantities(likes, (), branches, p, u)
    assert result['R'][3][7] == F(9,10) and result['J'][3][7] == 0
    assert result['D'][3] == result['D'][7] == u == F(13,4)
    assert result['pKp'] == F(359,120) < u
    assert result['direct_mean_R'] == F(9,20) and result['direct_mean_J'] == F(29,30)
    # Counts of ordered paths through the complete DAG, including repeated topics.
    ways = Counter({raw['root']: 1})
    for depth in range(8):
        for identity in [j for j,n in enumerate(nodes) if sum(n['counts']) == depth]:
            for child in nodes[identity]['children']:
                ways[child] += ways[identity]
    decisions = sum(ways[j] for j,n in enumerate(nodes) if n['action'] is not None)
    leaves = sum(ways[j] for j,n in enumerate(nodes) if n['action'] is None)
    assert decisions == sum(8 ** d for d in range(8)) == 2396745
    assert leaves == 8 ** 8 == 16777216
    return dict(status='all_passed', root_path=root_path, root_branches=branches,
                raw_DAG_nodes=len(nodes), expanded_decision_histories=decisions,
                expanded_terminal_histories=leaves, root_node=result,
                selected_pair=dict(A=3,T=7,R='9/10',e_A='0',e_T='0',J='0'),
                interpretation='Pairwise local e+J budget fails. The same two-action iid diagonal cap succeeds. Cartesian all-k conclusions use the written algebraic proof, not finite product enumeration.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-dir', type=Path, required=True)
    args = parser.parse_args(); output = args.run_dir.resolve()
    if output.exists():
        parser.error('Use a new directory; never overwrite prior evidence')
    manifest = json.loads((BASE / 'source-manifest.json').read_text())
    for row in manifest['files']:
        p=BASE/'original'/row['path']
        assert p.stat().st_size == row['size'] and digest(p) == row['sha256']
    output.mkdir(parents=True)
    source = output / 'source'; shutil.copytree(BASE / 'original', source)
    sys.path.insert(0, str(source))
    captured = {}
    target = str(source / DIAG)
    def capture(frame, event, arg):
        if event == 'return' and frame.f_code.co_filename == target and frame.f_code.co_name == 'main':
            captured.update(frame.f_locals)
    start = time.monotonic()
    with (output/'diagonal.stdout.txt').open('w') as stdout, (output/'diagonal.stderr.txt').open('w') as stderr:
        with redirect_stdout(stdout), redirect_stderr(stderr):
            sys.setprofile(capture)
            try:
                namespace = runpy.run_path(target, run_name='__main__')
            finally:
                sys.setprofile(None)
    diag_duration = time.monotonic() - start
    inst = namespace['INSTANCE']
    export = dict(instance=inst.to_dict(), certificate=captured['cert'].to_dict(),
                  p=list(map(str, namespace['P'])), root_K=captured['K'], root_D=captured['d'],
                  verification=dict(valid=captured['checked'].valid,
                                    checked_histories=captured['checked'].checked_histories,
                                    checked_deviations=captured['checked'].checked_deviations))
    write(output/'diagonal-export.json', export)
    write(output/'diagonal-independent.json', independent_diagonal(textify(export)))
    command = [sys.executable, str(source/DAGDIR/'verify_pure_menu_dag.py'),
               '--output', str(output/'base-original-report.json')]
    env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
    start=time.monotonic()
    completed=subprocess.run(command,cwd=source,env=env,capture_output=True)
    base_duration=time.monotonic()-start
    (output/'base.stdout.txt').write_bytes(completed.stdout)
    (output/'base.stderr.txt').write_bytes(completed.stderr)
    if completed.returncode:
        raise SystemExit(completed.returncode)
    write(output/'base-reset-independent.json', independent_base(source))
    scalar_cases=0
    for c in range(1,6):
        for nA,nT,aA,aT in product(range(8),range(8),range(2),range(2)):
            lhs=F(aT,c+aA+nA)+F(aA,c+aT+nT)-F(aA,c+nA)-F(aT,c+nT)
            r=F((aA-aT)*(nA-nT),(c+nA)*(c+nT))
            j=(F(1,(c+nA)*(c+nA+1))+F(1,(c+nT)*(c+nT+1))) if aA*aT else F(0)
            assert lhs==r-j; scalar_cases+=1
    record=dict(schema_version=1,status='all_passed',python_version=sys.version.split()[0],
                original_diagonal_main_executions=1,original_base_verifier_executions=1,
                diagonal_command=[sys.executable,*sys.argv], diagonal_cwd=str(Path.cwd()),
                diagonal_invocation='runpy.run_path(original_script, run_name=__main__); Python profiler captures main return locals without calling solver again',
                base_command=command,base_cwd=str(source),source_tree=str(source),environment={'PYTHONDONTWRITEBYTECODE':'1'},
                elapsed_seconds={'diagonal_original':diag_duration,'base_original':base_duration},
                scalar_RESET_checks=scalar_cases,returncode=completed.returncode,
                original_source_sha256={r['path']:r['sha256'] for r in manifest['files']},
                log_sha256={p.name:digest(p) for p in output.glob('*.txt')},
                scope_correction='Original diagonal docstring and stdout scope falsely name pKp<=actual u. Actual asserted gap is against mean forced payoff pD; original bytes/logs are retained unchanged.')
    for row in manifest['files']:
        assert digest(source/row['path']) == row['sha256']
    write(output/'execution.json',record)
    print(json.dumps(dict(status='all_passed',output=str(output),scalar_RESET_checks=scalar_cases,
                          diagonal_original_runs=1,base_original_runs=1),indent=2))


if __name__ == '__main__':
    main()
