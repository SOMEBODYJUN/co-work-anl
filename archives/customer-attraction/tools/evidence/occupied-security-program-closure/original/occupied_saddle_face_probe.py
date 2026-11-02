"""Discovery: reweight a complete static saddle face to attack occupied payoff.

Candidate: for static optimal p and every pure minimizing m-slot q, every
occupied d has U_d(q)>=v.  This uses no sequential truncation or SPE assumption.
All LP output is discovery only until an exact rational saddle certificate.
"""
from itertools import combinations_with_replacement
from pathlib import Path
import json
import random
import numpy as np
from scipy.optimize import linprog


def saddle(K):
    # K[background,query].
    n, k = K.shape
    out = linprog(np.r_[np.zeros(k), -1.],
                  A_ub=np.column_stack((-K, np.ones(n))), b_ub=np.zeros(n),
                  A_eq=[np.r_[np.ones(k), 0.]], b_eq=[1.],
                  bounds=[(0, None)] * k + [(None, None)], method='highs')
    assert out.success
    return out.x[:-1], -out.ineqlin.marginals, out.x[-1]


def attack(m, k, weights, rng):
    M = np.array([[(mask >> a) & 1 for mask in range(1, 1 << k)]
                  for a in range(k)], dtype=float)
    counts = np.array([tuple(q.count(a) for a in range(k))
                       for q in combinations_with_replacement(range(k), m)])
    load = counts @ M
    insertion = 1 / (1 + load)
    K = (insertion * weights) @ M.T
    p, Q, value = saddle(K)
    if value < 1e-9:
        return None
    static_coeff = insertion * (p @ M)
    query_coeff = M * (Q @ insertion)
    active = np.where(np.abs(K @ p - value) < 1e-7 * max(value, 1))[0]
    pairs = [(qi, d) for qi in active for d in np.where(counts[qi] > 0)[0]]
    rng.shuffle(pairs)
    best = None
    # Scan every active occupied pair of this complete finite saddle face.
    for qi, d in pairs:
        payoff = M[d] / np.maximum(load[qi], 1)
        out = linprog(payoff,
                      A_ub=np.vstack((-static_coeff, query_coeff)),
                      b_ub=np.r_[-np.ones(len(counts)), np.ones(k)],
                      A_eq=[static_coeff[qi]], b_eq=[1.],
                      bounds=[(0, None)] * len(weights), method='highs')
        if not out.success:
            continue
        if best is None or out.fun < best['occupied_value']:
            best = {'m': m, 'k': k, 'p': p.tolist(), 'Q': Q.tolist(),
                    'counts': counts[qi].tolist(), 'd': int(d),
                    'weights': out.x.tolist(), 'occupied_value': float(out.fun),
                    'full_backgrounds': len(counts), 'active_backgrounds': len(active)}
    return best


if __name__ == '__main__':
    rng = random.Random(731261023)
    report = {'status': 'numerical saddle-face discovery only', 'cases': 0,
              'best': None, 'candidate': None}
    for case in range(80):
        m, k = [(1, 4), (2, 5), (3, 5), (4, 5), (6, 5), (8, 5), (6, 6), (8, 6)][case % 8]
        density = rng.choice([.1, .25, .5, 1.])
        weights = np.array([rng.randint(1, 50) if rng.random() < density else 0
                            for _ in range((1 << k) - 1)], dtype=float)
        z = attack(m, k, weights, rng)
        if z is not None and (report['best'] is None or z['occupied_value'] < report['best']['occupied_value']):
            report['best'] = z
            print(case, m, k, z['occupied_value'], flush=True)
        report['cases'] = case + 1
        if z is not None and z['occupied_value'] < 1 - 1e-7:
            report['candidate'] = z
            break
    target = Path(__file__).with_name('occupied_saddle_face_probe.json')
    target.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'cases': report['cases'], 'best_value': report['best']['occupied_value'],
                      'candidate': report['candidate'] is not None}), flush=True)
