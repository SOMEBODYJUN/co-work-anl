"""Check frozen terminal-pool records and one saved corner over Fraction.

No original program, canonical package, equilibrium solver, LP, NumPy, or
SciPy is imported. This is finite input checking, not a universal pool proof.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ORIGINAL = HERE / 'original'
PRIMARY = ORIGINAL / 'research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round6_general/convex'


def full_policy(m, k, policy, signatures, weights):
    expected = {h for d in range(m) for h in product(range(k), repeat=d)}
    assert set(policy) == expected
    assert all(a in range(k) for a in policy.values())

    @lru_cache(None)
    def finish(h):
        return h if len(h) == m else finish(h + (policy[h],))

    def load(z):
        return tuple(sum(a in s for a in z) for s in signatures)

    def payoff(z, i):
        return sum((w / c for s, w, c in zip(signatures, weights, load(z))
                    if z[i] in s), F(0))

    comparisons = 0
    for h in expected:
        own = payoff(finish(h), len(h))
        for a in range(k):
            if a != policy[h]:
                assert own >= payoff(finish(h + (a,)), len(h))
                comparisons += 1
    return finish, load, payoff, len(expected), comparisons


def named_record(record):
    name = record['name']
    raw = json.loads((ORIGINAL / 'examples/customer_attraction' / f'{name}.json').read_text())
    cert = json.loads((ORIGINAL / 'evidence/certificates/customer_attraction' / f'{name}.json').read_text())
    strategy = cert.get('strategy', cert)
    action_rows = strategy['actions']
    policy = {tuple(r['history']): r['action'] for r in action_rows}
    assert len(policy) == len(action_rows)
    m, k = raw['players'], len(raw['topics'])
    signatures = tuple(frozenset(c['topics']) for c in raw['customers'])
    weights = tuple(F(c['multiplicity']) for c in raw['customers'])
    finish, load, payoff, histories, deviations = full_policy(m, k, policy, signatures, weights)
    z = finish(())
    if 'terminal_counts' in strategy:
        assert tuple(z.count(a) for a in range(k)) == tuple(strategy['terminal_counts'])
    us = tuple(payoff(z, i) for i in range(m))
    W = sum(us)
    beta, P = load(z[:-2]), z[-2]
    replies = tuple(finish(z[:-2] + (a,))[-1] for a in range(k))
    cols = tuple(tuple(load(finish(z[:i] + (a,))) for a in range(k)) for i in range(m))

    def U(t, b):
        return sum((weights[x] / (beta[x] + 1 + (b in s))
                    for x, s in enumerate(signatures) if t in s), F(0))

    J = tuple(sum((sum((weights[x] / (1 + cols[i][a][x])
                       for x, s in enumerate(signatures) if t in s), F(0))
                   for a in range(k) for t in range(k)), F(0)) / k**2 for i in range(m))
    Ipen = us[-2] - sum((U(a, replies[a]) for a in range(k)), F(0)) / k
    Ilast = us[-1] - sum((U(t, P) for t in range(k)), F(0)) / k
    G = sum((U(replies[a], a) - U(replies[t], a)
             for a in range(k) for t in range(k)), F(0)) / k**2

    def tax(reply):
        return sum((weights[x] / ((beta[x] + 1 + (reply(a) in s)) *
                                 (beta[x] + 2 + (reply(a) in s)))
                    for a in range(k) for t in range(k)
                    for x, s in enumerate(signatures) if a in s and t in s), F(0)) / k**2

    tp, tm = tax(lambda a: replies[a]), tax(lambda a: P)
    meanload = tuple(sum((cols[i][a][x] for i in range(m) for a in range(k)), F(0)) / (m*k)
                     for x in range(len(signatures)))
    rho = tuple(F(len(s), k) for s in signatures)
    value = sum((w*r/(1+l) for w, r, l in zip(weights, rho, meanload)), F(0))
    V = sum(J) - m*value
    early = sum(J[i] - us[i] for i in range(m-2))
    bank = Ipen + Ilast + G + tp + tm + V
    assert min(Ipen, Ilast, G, tp, tm, V) >= 0
    assert us[-2] - J[-2] == Ipen + G + tp
    assert us[-1] - J[-1] == Ilast + tm
    assert W - m*value == bank - early
    computed = dict(name=name, m=m, k=k, histories=histories,
                    terminal_payments_verified=True, all_balance_checks=True,
                    IC_pen=str(Ipen), IC_last=str(Ilast), cross_BR=str(G),
                    tax_pen=str(tp), tax_last=str(tm), Jensen_pool=str(V),
                    early_deficit=str(early), bank=str(bank), W_minus_mF=str(W-m*value))
    assert computed == record, (name, computed, record)
    return dict(name=name, unit_customers=int(sum(weights)), actual=list(z),
                W=str(W), histories=histories, nonself_deviations=deviations,
                complete_frozen_record_equal=True)


def saved_corner():
    raw = json.loads((PRIMARY / 'shared_cone_best.json').read_text())
    m, k = raw['record']['m'], raw['record']['k']
    policy = {tuple(row['history']): row['action'] for row in raw['policy']}
    assert len(policy) == len(raw['policy'])
    weights = tuple(F(str(x)).limit_denominator(1000000) for x in raw['details']['w'])
    assert weights == tuple(F(1, 3) if mask == 1 else F(1) if mask == 14 else F(0)
                            for mask in range(1, 1 << k))
    signatures = tuple(frozenset(a for a in range(k) if mask & (1 << a))
                       for mask in range(1, 1 << k))
    finish, load, payoff, histories, deviations = full_policy(m, k, policy, signatures, weights)
    z = finish(())
    assert z == tuple(raw['record']['actual']) == (2, 3, 1)
    # The two nonzero types have the same deleted load in all twelve columns.
    for i in range(m):
        for a in range(k):
            leaf = finish(z[:i] + (a,))
            deleted = leaf[:i] + leaf[i+1:]
            v = load(deleted)
            assert v[0] == 0 and v[13] == 2
    W = sum(payoff(z, i) for i in range(m))
    # All four pure queries have exactly 1/3 against every admissible shared q.
    pure_values = tuple(sum((weights[x] / (1 + (0 if mask == 1 else 2))
                             for x, mask in enumerate(range(1, 1 << k))
                             if a in signatures[x] and weights[x]), F(0)) for a in range(k))
    assert pure_values == (F(1, 3),)*k and W == 1
    return dict(scope='exact reconstruction of saved rational corner only',
                m=m, k=k, actual=list(z), histories=histories,
                nonself_deviations=deviations, W='1', deleted_pool_value='1/3',
                ratio='1', all_deleted_columns_constant_on_nonzero_types=True,
                all_pure_queries_equal=True, new_counterexample=False)


if __name__ == '__main__':
    frozen = json.loads((PRIMARY / 'audit_terminal_pool.json').read_text())
    result = dict(scope='finite exact standard-library input checking; no universal claim',
                  named=[named_record(r) for r in frozen['records']], shared_corner=saved_corner(),
                  original_main_calls=0, canonical_solver_calls=0,
                  canonical_verifier_calls=0, lp_calls=0, floating_optimizer_calls=0,
                  script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    print(json.dumps(result, indent=2))
