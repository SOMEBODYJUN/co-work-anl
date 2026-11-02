"""Exact attacks on the signed harmonic terminal-budget candidate.

This checks existing witnesses, rather than a new random finite SPE scan.
"""
from fractions import Fraction as F
from itertools import combinations, product
from functools import lru_cache
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction.model import Instance
from customer_attraction.certificate import StrategyCertificate, verify_certificate


def all_minimal_optima(instance):
    """All optimal supports, enough to minimize either concave budget.

    At a fixed support, H_(c+d)-H_c is concave in the topic counts.
    A minimum over q>=1, sum(q)=m is attained by putting all spare
    copies on a single support topic. D is linear, with the same fact.
    """
    p, m = instance.topic_count, instance.players
    best, supports = -1, []
    for k in range(1, min(m, p)+1):
        for S in combinations(range(p), k):
            q = tuple(int(a in S) for a in range(p))
            w = instance.welfare(q)
            if w > best:
                best, supports = w, [S]
            elif w == best:
                supports.append(S)
    for S in supports:
        spare = m-len(S)
        for a in (S if spare else S[:1]):
            q = tuple(int(t in S)+spare*int(t == a) for t in range(p))
            yield best, q


def budgets(instance, actual, q):
    W = instance.welfare(actual)
    B = D = F(0)
    outside = missing = 0
    for r in instance.customers:
        c = sum(actual[t] for t in r.topics)
        d = sum(q[t] for t in r.topics)
        B += r.multiplicity*sum((F(1, c+j) for j in range(1, d+1)), F(0))
        D += r.multiplicity*F(d, c+1)
        outside += r.multiplicity*int(c > 0 and d == 0)
        missing += r.multiplicity*int(c == 0 and d > 0)
    return dict(B=B, D=D, W=W, outside=outside, missing=missing,
                B_gap=B-W-outside, D_gap=D-W-outside)


def audit(name):
    instance = Instance.from_dict(json.loads((ROOT/'examples/customer_attraction'/f'{name}.json').read_text()))
    source = json.loads((ROOT/'evidence/certificates/customer_attraction'/f'{name}.json').read_text())
    for k in ('strategy', 'certificate'):
        if k in source and 'actions' in source[k]:
            source = source[k]
            break
    if 'actions' not in source:
        return dict(name=name, skipped_schema=list(source))
    if 'terminal_counts' not in source:
        actions = {tuple(row['history']): row['action'] for row in source['actions']}
        h = ()
        while len(h) < instance.players:
            h += (actions[h],)
        source['terminal_counts'] = instance.counts(h, terminal=True)
    cert = StrategyCertificate.from_dict(source)
    valid = verify_certificate(instance, cert)
    valid.assert_valid()
    candidates = [(q, budgets(instance, cert.terminal_counts, q)) for opt, q in all_minimal_optima(instance)]
    minB = min(candidates, key=lambda item: item[1]['B_gap'])
    minD = min(candidates, key=lambda item: item[1]['D_gap'])
    maxB = max(candidates, key=lambda item: item[1]['B_gap'])
    return dict(name=name, m=instance.players, p=instance.topic_count,
                checked_histories=valid.checked_histories,
                checked_deviations=valid.checked_deviations,
                actual=valid.terminal_history, actual_counts=cert.terminal_counts,
                optimal=instance.optimal_welfare(), extrema_candidates=len(candidates),
                minB=dict(q=minB[0], **minB[1]),
                minD=dict(q=minD[0], **minD[1]),
                largest_extreme_B=dict(q=maxB[0], **maxB[1]))


def main():
    names = ['optimal_last_query_failure', 'portfolio_matching_failure',
             'prefix_balance_failure', 'fractional_actual_load_failure',
             'worst_cce_welfare_failure', 'worst_pne_welfare_failure',
             'aggregate_theta_failure', 'individual_security_failure',
             'coverage_opportunity_failure', 'root_tax_failure']
    report = [audit(name) for name in names]
    encoded = json.dumps(report, indent=2, default=str)
    Path(__file__).with_name('known_witness_audit.json').write_text(encoded+'\n')
    print(encoded)


if __name__ == '__main__':
    main()
