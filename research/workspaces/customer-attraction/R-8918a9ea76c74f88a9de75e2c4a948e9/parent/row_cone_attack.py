"""Attack ROW-NET in frozen complete SPE cones; numerical proposals only.

The target is sum_j d_i(T_j) >= |union_j T_j|-W for all actual i and
exactly m comparison slots. A positive rational proposal is replayed exactly.
No finite negative result is a proof, and no cone point is called SPE before
all original ordered-history incentive rows are checked with Fraction.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json
import math
import sys

import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction.model import Instance, CustomerType
from customer_attraction.certificate import StrategyCertificate, verify_certificate


def attack(name):
    game = Instance.from_dict(json.loads((ROOT / f'examples/customer_attraction/{name}.json').read_text()))
    obj = json.loads((ROOT / f'evidence/certificates/customer_attraction/{name}.json').read_text())
    data = dict(obj.get('strategy', obj))
    if 'terminal_counts' not in data:
        lookup = {tuple(item['history']): item['action'] for item in data['actions']}
        history = ()
        while len(history) < game.players:
            history += (lookup[history],)
        data['terminal_counts'] = game.counts(history, terminal=True)
    cert = StrategyCertificate.from_dict(data)
    verify_certificate(game, cert).assert_valid()
    k, m = game.topic_count, game.players
    if k > 6:
        return {'fixture': name, 'status': 'not_run_resource_bound',
                'reason': 'dense IC by all customer patterns would exceed the chosen memory budget'}
    patterns = list(range(1, 1 << k))
    leaves = {}

    def walk(h):
        if len(h) == m:
            out = game.counts(h, terminal=True)
        else:
            for a in range(k):
                walk(h + (a,))
            out = leaves[h + (cert.actions[h],)]
        leaves[h] = out
        return out

    walk(())

    def utility(q, a):
        return [F(int(bool(B & (1 << a))), sum(q[t] for t in range(k) if B & (1 << t)))
                if B & (1 << a) else F(0) for B in patterns]

    rows = []
    for h, chosen in cert.actions.items():
        left = utility(leaves[h], chosen)
        for a in range(k):
            if a != chosen:
                right = utility(leaves[h + (a,)], a)
                rows.append([x-y for x, y in zip(left, right)])
    gamma = np.array(rows, dtype=float)
    actual = []
    h = ()
    while len(h) < m:
        a = cert.actions[h]
        actual.append(a)
        h += (a,)
    W = [F(int(any(B & (1 << a) for a in actual))) for B in patterns]
    record = {'fixture': name, 'actual': actual, 'tested': 0, 'maximum_proposal': -1.0}
    for i in range(m - 2):  # terminal two rows have an existing general proof
        prefix = tuple(actual[:i])
        query = [utility(leaves[prefix + (a,)], a) for a in range(k)]
        for size in range(1, min(m, k)+1):
            for support in combinations(range(k), size):
                mask = sum(1 << a for a in support)
                O = [F(int(bool(B & mask))) for B in patterns]
                for repeated in support[:1] if size == m else support:
                    T = tuple(support) + (repeated,) * (m-size)
                    defect = [O[t]-W[t]-sum(query[a][t] for a in T) for t in range(len(patterns))]
                    sol = linprog(-np.array(defect, dtype=float), A_ub=-gamma,
                                  b_ub=np.zeros(len(rows)), A_eq=np.array([W], dtype=float),
                                  b_eq=[1.0], bounds=(0, None), method='highs')
                    record['tested'] += 1
                    if not sol.success:
                        raise RuntimeError(sol.message)
                    record['maximum_proposal'] = max(record['maximum_proposal'], float(-sol.fun))
                    if -sol.fun > 1e-7:
                        x = [F(float(v)).limit_denominator(1000000) for v in sol.x]
                        if not all(sum(a*b for a, b in zip(row, x)) >= 0 for row in rows):
                            record.setdefault('unverified_proposals', []).append(float(-sol.fun))
                            continue
                        D = sum(a*b for a, b in zip(defect, x))
                        if D <= 0:
                            continue
                        den = math.lcm(*(v.denominator for v in x))
                        counts = [int(v*den) for v in x]
                        gcd = math.gcd(*counts)
                        counts = [v//gcd for v in counts]
                        witness = Instance(game.topics, tuple(CustomerType(frozenset(t for t in range(k) if B & (1 << t)), n)
                            for B, n in zip(patterns, counts) if n), m)
                        verification = verify_certificate(witness, cert)
                        verification.assert_valid()
                        result = {'fixture': name, 'position': i, 'comparison': T,
                                  'defect': str(D), 'game': witness.to_dict(),
                                  'strategy': cert.to_dict(),
                                  'checked_histories': verification.checked_histories,
                                  'checked_deviations': verification.checked_deviations}
                        (Path(__file__).parent/'row_counterexample.json').write_text(json.dumps(result, indent=2))
                        record['counterexample'] = result
                        return record
    return record


if __name__ == '__main__':
    reports = []
    for fixture in ['individual_security_failure', 'global_decorrelation_failure',
                    'root_tax_failure', 'five_individual_security', 'eight_cce_welfare_gap']:
        report = attack(fixture)
        reports.append(report)
        print(json.dumps({k:v for k,v in report.items() if k != 'counterexample'}), flush=True)
        (Path(__file__).parent/'row_cone_attack.json').write_text(json.dumps(reports, indent=2))
        if 'counterexample' in report:
            break
    (Path(__file__).parent/'row_cone_attack.json').write_text(json.dumps(reports, indent=2))
