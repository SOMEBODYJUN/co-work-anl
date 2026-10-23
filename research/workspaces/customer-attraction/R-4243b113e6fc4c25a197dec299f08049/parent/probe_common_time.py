"""One finite compatibility diagnostic for the product-menu time obligation.

Uses existing complete SPE certificates only; no random seed search. HiGHS is
a discovery oracle. A feasible finite result is not a universal theorem.
"""
from __future__ import annotations

import json
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction.model import Instance
from customer_attraction.certificate import StrategyCertificate, verify_certificate


def menu(instance, cert):
    m, k = instance.players, instance.topic_count

    @lru_cache(None)
    def terminal(h):
        return h if len(h) == m else terminal(h + (cert.actions[h],))

    actual = terminal(())
    w = instance.welfare(instance.counts(actual))
    matrix = []
    for i in range(m):
        layer = []
        for a in range(k):
            z = terminal(actual[:i] + (a,))
            layer.append([
                sum((F(t.multiplicity,
                       1 + sum(b in t.topics for b in z))
                     for t in instance.customers if q in t.topics), F(0))
                for q in range(k)
            ])
        matrix.append(layer)
    return matrix, w, actual


def oracle(matrix, w, lam):
    m, k = len(matrix), len(matrix[0])
    # Variables p[0:k], z[0:m]; z_i <= each endpoint price in layer i.
    rows = []
    for i in range(m):
        for a in range(k):
            row = [-float(x) for x in matrix[i][a]] + [0.] * m
            row[k + i] = 1.
            rows.append(row)
    out = linprog([0.] * k + [-float(x) for x in lam],
                  A_ub=rows, b_ub=np.zeros(m*k),
                  A_eq=[[1.] * k + [0.] * m], b_eq=[1.],
                  bounds=[(0, None)]*(k+m), method='highs')
    if not out.success:
        raise RuntimeError(out.message)
    # Rational query is evaluated independently with Fraction, even though
    # its discovery and the master feasibility check remain numerical.
    p = [F(float(x)).limit_denominator(10**7) for x in out.x[:k]]
    total = sum(p, F(0))
    p = [x/total for x in p]
    psi = [min(sum((p[q]*matrix[i][a][q] for q in range(k)), F(0))
               for a in range(k)) for i in range(m)]
    gap = sum(float(lam[i])*float(psi[i]) for i in range(m))-w/m
    return gap, p, psi


def load_corpus():
    accepted, skipped = [], []
    for path in sorted((ROOT/'evidence/certificates/customer_attraction').glob('*.json')):
        inp = ROOT/'examples/customer_attraction'/path.name
        if not inp.exists():
            continue
        try:
            inst = Instance.from_dict(json.loads(inp.read_text()))
            if not (1 <= inst.players <= 6 and inst.topic_count <= 8):
                continue
            raw = json.loads(path.read_text())
            raw = raw.get('strategy', raw.get('certificate', raw))
            cert = StrategyCertificate.from_dict(raw)
            check = verify_certificate(inst, cert)
            if not check.valid:
                skipped.append([path.name, 'invalid under canonical checker'])
                continue
            k, w, a = menu(inst, cert)
            accepted.append(dict(name=path.name, players=inst.players,
                                 topics=inst.topic_count, matrix=k, W=w,
                                 actual=list(a)))
        except (KeyError, ValueError, TypeError) as exc:
            skipped.append([path.name, str(exc)])
    return accepted, skipped


def main():
    corpus, skipped = load_corpus()
    results = []
    for m in sorted({g['players'] for g in corpus}):
        games = [g for g in corpus if g['players'] == m]
        cuts = []
        lam = np.ones(m)/m
        status = 'ITERATION_LIMIT'
        for iteration in range(30):
            fresh = []
            worst = -float('inf')
            for g in games:
                gap, p, psi = oracle(g['matrix'], g['W'], lam)
                worst = max(worst, gap)
                if gap > 1e-8:
                    fresh.append(dict(game=g['name'], p=list(map(str, p)),
                                      d=list(map(str, [v-F(g['W'],m) for v in psi]))))
            if not fresh:
                status = 'FINITE_CORPUS_COMPATIBLE_ONLY'
                break
            cuts.extend(fresh)
            out = linprog([0.]*m,
                          A_ub=[[float(F(v)) for v in cut['d']] for cut in cuts],
                          b_ub=np.zeros(len(cuts)), A_eq=[[1.]*m], b_eq=[1.],
                          bounds=[(0,None)]*m, method='highs')
            if not out.success:
                status = 'NUMERICAL_SEPARATION_CANDIDATE_REQUIRES_EXACT_RECONSTRUCTION'
                break
            lam = out.x
        result = dict(m=m, games=[g['name'] for g in games], status=status,
                      iterations=iteration+1, common_time=list(map(float,lam)),
                      last_worst_gap=worst, rational_query_cuts=cuts)
        results.append(result)
        print(m, len(games), status, list(lam), worst, flush=True)
    report = dict(scope='Specified finite canonical certificate corpus only; '
                  'not proof of universal time, menu bridge, or half.',
                  algorithm='finite cutting planes with numerical HiGHS LP; '
                  'each queried psi recomputed with exact rational arithmetic',
                  games=len(corpus), skipped=skipped, results=results)
    Path(__file__).with_name('common_time_diagnostic.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    main()
