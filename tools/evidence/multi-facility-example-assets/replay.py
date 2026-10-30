"""Read preserved inputs and run the original quick entry once in a fresh tree.

This is a small independent fixture check, not a universal proof or another
execution of the already preserved 90-random-case global audit.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
from itertools import product
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

BASE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize(raw):
    # Named-site fixture files are data, not the production integer-index schema.
    labels = raw.get('sites', list(range(raw.get('m', 0))))
    lookup = {v: i for i, v in enumerate(labels)}
    clients = [(F(c['weight']), tuple(lookup[t] for t in c['sites']))
               for c in raw['clients']]
    return labels, raw['k'], clients


def greedy(labels, k, clients):
    q = [0] * len(labels)
    home = [-1] * len(clients)
    order, scores, maxima = [], [], []
    for _ in range(k):
        candidates = []
        for t in range(len(labels)):
            if q[t]:
                score = sum((w for i, (w, _) in enumerate(clients)
                             if home[i] == t), F(0)) / (q[t] + 1)
            else:
                score = sum((w for i, (w, menu) in enumerate(clients)
                             if home[i] < 0 and t in menu), F(0))
            candidates.append(score)
        score = max(candidates)
        tied = [t for t, x in enumerate(candidates) if x == score]
        t = tied[0]
        order.append(labels[t]); scores.append(str(score)); maxima.append(len(tied))
        if not q[t]:
            for i, (_, menu) in enumerate(clients):
                if home[i] < 0 and t in menu:
                    home[i] = t
        q[t] += 1
    pools = [sum((w for i, (w, _) in enumerate(clients) if home[i] == t), F(0))
             for t in range(len(labels))]
    return dict(order=order, scores=scores, number_of_maximizing_sites=maxima,
                q=q, home=home, gamma=scores[-1], original_pool_weights=list(map(str, pools)))


def independent_fixtures(source):
    table = {}
    for p in sorted((source / 'examples/multi_facility').glob('*.json')):
        if p.name == 'rational.json':
            continue  # only the quick audit reads this dependency
        raw = json.loads(p.read_text())
        labels, k, clients = normalize(raw)
        table[p.name] = greedy(labels, k, clients)
    p = source / 'examples/multi_facility/equal_light_flow_local_ne.json'
    raw = json.loads(p.read_text()); expected = raw['expected']
    labels, k, clients = normalize(raw)
    actual = table[p.name]
    for key, expected_key in [('order', 'strict_greedy_order'), ('scores', 'greedy_scores'),
                              ('q', 'q'), ('gamma', 'gamma')]:
        assert actual[key] == expected[expected_key], (key, actual[key])
    assert actual['number_of_maximizing_sites'] == [1] * k
    q, home, gamma = actual['q'], actual['home'], F(actual['gamma'])
    occupied = {t for t in range(len(q)) if q[t]}
    movable = [i for i, (w, menu) in enumerate(clients)
               if w < gamma and len(set(menu) & occupied) > 1]
    assert movable == expected['movable_indices']
    c = [F(w) / gamma - n for w, n in zip(actual['original_pool_weights'], q)]
    weights = [clients[i][0] / gamma for i in movable]
    assert list(map(str, c)) == expected['normalized_c']
    assert list(map(str, weights)) == expected['normalized_w']
    menus = [tuple(t for t in clients[i][1] if t in occupied) for i in movable]
    rows = []
    for a in product(*menus):
        assignment = home.copy()
        for i, t in zip(movable, a):
            assignment[i] = t
        totals = [sum((w for i, (w, _) in enumerate(clients) if assignment[i] == t), F(0))
                  for t in range(len(q))]
        X = [totals[t] / gamma - q[t] for t in range(len(q))]
        b = c.copy()
        for i, delta in zip(movable, weights):
            b[home[i]] -= delta
        counts = Counter(a); delta = weights[0]
        psi = sum(((b[t] * counts[t] + delta * counts[t] * (counts[t] - 1) / 2) / q[t]
                   for t in occupied), F(0))
        # Every original occupied option and every labeled customer's actual
        # conditional cost is checked, including moves which leave the box.
        comparisons = []
        for i, (w, menu) in enumerate(clients):
            s = assignment[i]
            own = w + (totals[s] - w) / q[s]
            for t in sorted(set(menu) & occupied - {s}):
                alternative = w + totals[t] / q[t]
                comparisons.append(dict(customer=i, source=labels[s], target=labels[t],
                                        current=str(own), alternative=str(alternative),
                                        stable=own <= alternative))
        h_ok = all((X[t] - delta) / q[t] <= (1 - delta) / q[home[i]]
                   for i, t, delta in zip(movable, a, weights))
        rows.append(dict(movable_assignment=[labels[t] for t in a],
                         site_totals=list(map(str, totals)), X=list(map(str, X)),
                         Psi=str(psi), full_box=all(0 <= x <= 1 for x in X),
                         exact_site_NE=all(r['stable'] for r in comparisons),
                         H=h_ok, comparisons=comparisons))
    local = next(r for r in rows if r['movable_assignment'] == expected['local_ne_movable_assignment'])
    assert local['X'] == expected['local_ne_X'] and local['Psi'] == expected['local_ne_Psi']
    assert local['exact_site_NE'] and not local['full_box']
    minimum = min(F(r['Psi']) for r in rows)
    minimizers = [r for r in rows if F(r['Psi']) == minimum]
    assert len(minimizers) == 1
    assert minimizers[0]['movable_assignment'] == expected['unique_global_movable_assignment']
    assert str(minimum) == expected['global_Psi'] and minimizers[0]['full_box']
    return dict(status='all_passed', greedy_fixtures=table,
                local_NE_all_four_legal_assignments=rows,
                scope='Five fixture greedy replays; only local-NE fixture has new all-assignment NE/Psi checks. Other counterexample audits are not rerun.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-dir', type=Path, required=True)
    args = parser.parse_args()
    destination = args.run_dir.resolve()
    if destination.exists():
        parser.error('Use a new run directory; preserved evidence is never overwritten')
    manifest = json.loads((BASE / 'source-manifest.json').read_text())
    for row in manifest['files']:
        p = BASE / 'original' / row['path']
        assert p.stat().st_size == row['size'] and sha(p) == row['sha256']
    destination.mkdir(parents=True)
    source = destination / 'source'
    shutil.copytree(BASE / 'original', source)
    (destination / 'fixture-check.json').write_text(json.dumps(independent_fixtures(source), indent=2) + '\n')
    # Execute the unmodified quick entry's actual __main__ once, retaining its
    # otherwise-unprinted report from runpy's completed module namespace.
    driver = ("import json,runpy,sys; from pathlib import Path; "
              "d=runpy.run_module('tests.test_greedy_box_global',run_name='__main__'); "
              "Path(sys.argv[1]).write_text(json.dumps(d['report'],indent=2)+'\\n')")
    command = [sys.executable, '-c', driver, str(destination / 'quick-report.json')]
    env = os.environ.copy()
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['PYTHONPATH'] = str(source)
    env['TMPDIR'] = str(destination)
    start = time.monotonic()
    result = subprocess.run(command, cwd=source, env=env, capture_output=True)
    duration = time.monotonic() - start
    (destination / 'quick.stdout.txt').write_bytes(result.stdout)
    (destination / 'quick.stderr.txt').write_bytes(result.stderr)
    record = dict(schema_version=1, command=command, cwd=str(source),
                  environment={k: env[k] for k in ['PYTHONDONTWRITEBYTECODE','PYTHONPATH','TMPDIR']},
                  python_version=sys.version.split()[0], returncode=result.returncode,
                  elapsed_seconds=duration, original_quick_entry_executions=1,
                  dependency_source_sha256={row['path']: row['sha256'] for row in manifest['files']},
                  log_sha256={p.name: sha(p) for p in destination.glob('quick.*.txt')},
                  scope='Original quick __main__ with random_cases=12. The 90-case audit, potential, repair-order, cap and equal-flow full audits are not run.')
    (destination / 'execution.json').write_text(json.dumps(record, indent=2) + '\n')
    for row in manifest['files']:
        assert sha(source / row['path']) == row['sha256']
    if result.returncode:
        raise SystemExit(result.returncode)
    print(json.dumps(dict(status='all_passed', run_dir=str(destination),
                          primary_sources=6, original_files=manifest['total_files'],
                          quick_report=json.loads((destination / 'quick-report.json').read_text())['counts']),indent=2))


if __name__ == '__main__':
    main()
