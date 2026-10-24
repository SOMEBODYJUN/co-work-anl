"""Independent parent regression of the new full-history construction and CL.

Two fixed fixtures, including an empty old topic.  No project solver imports.
The general statements rest on the analytic proofs, not these finite checks.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[5]


def audit(data, old_actions, J):
    n, p = data['players'], len(data['topics'])
    units = [frozenset(c['topics']) for c in data['customers']
             for _ in range(c.get('multiplicity', 1))]
    old_sets = [{x for x, s in enumerate(units) if a in s} for a in range(p)]
    assert len({frozenset(s) for s in old_sets}) == p
    assert J > 0
    B, m = p, n+1
    new_units = units + [frozenset({B}) for _ in range(J)]

    def utility(us, z, role):
        return sum((F(1, sum(a in s for a in z))
                    for s in us if z[role] in s), F())

    @lru_cache(None)
    def old_roll(h):
        return h if len(h) == n else old_roll(h + (old_actions[h],))

    eta = min(utility(units, old_roll(h), len(h)) for h in old_actions)
    L = max(F(len(T)) - min(F(len(T & S), 2) for S in old_sets)
            for T in old_sets)
    assert F(J, 2) <= eta and J >= L and n >= 2
    old_checks = 0
    for h in old_actions:
        for a in range(p):
            assert utility(units, old_roll(h), len(h)) >= utility(units, old_roll(h+(a,)), len(h))
            old_checks += 1

    actions = {}

    @lru_cache(None)
    def roll(h):
        if len(h) == m:
            return h
        children = [roll(h+(a,)) for a in range(p+1)]
        if h.count(B) == 0:
            a = B
        elif h.count(B) == 1:
            a = old_actions[tuple(a for a in h if a != B)]
        else:
            a = max(range(p+1), key=lambda a: (utility(new_units, children[a], len(h)), -a))
        actions[h] = a
        return children[a]

    z = old_roll(())
    zp = roll(())
    assert zp == (B,) + z
    checks, retained = 0, 0
    minimum_slack = None
    for h in actions:
        for a in range(p+1):
            gap = utility(new_units, roll(h), len(h))-utility(new_units, roll(h+(a,)), len(h))
            assert gap >= 0, (h, a, gap)
            checks += 1
            minimum_slack = gap if minimum_slack is None else min(gap, minimum_slack)
        if h.count(B) == 1:
            assert actions[h] == old_actions[tuple(a for a in h if a != B)]
            retained += 1

    def welfare(us, zz):
        return sum(any(a in s for a in zz) for s in us)

    def insertion(us, zz, a):
        return sum((F(1, 1+sum(t in s for t in zz)) for s in us if a in s), F())

    def menus(us, pp, zz, roller, dist):
        return [min(sum((dist[t] * insertion(us, roller(zz[:i]+(a,)), t)
                         for t in range(pp)), F())
                    for a in range(pp)) for i in range(len(zz))]

    W = welfare(units, z)
    M = max(insertion(units, z, a) for a in range(p))
    assert M <= J and F((n-1)*J, 2) <= W
    assert welfare(new_units, zp) == W+J
    Mp = max(insertion(new_units, zp, a) for a in range(p+1))
    assert Mp == max(M, F(J, 2))
    if M <= F(W, n):
        assert Mp <= F(W+J, n+1)

    distributions = [[F(int(t == a)) for t in range(p)] for a in range(p)]
    distributions.append([F(1, p)]*p)
    lambdas = [[F(1, n)]*n] + [[F(int(i == j)) for i in range(n)] for j in range(n)]
    cl_checks = 0
    for dist in distributions:
        old_psi = menus(units, p, z, old_roll, dist)
        Lz = sum((dist[a]*insertion(units, z, a) for a in range(p)), F())
        for alpha in (F(0), F(1, 3), F(1, 2), F(1)):
            distp = [(1-alpha)*v for v in dist]+[alpha]
            new_psi = menus(new_units, p+1, zp, roll, distp)
            for lam in lambdas:
                E = n*sum((lam[i]*old_psi[i] for i in range(n)), F())-W
                Ep = new_psi[0]+n*sum((lam[i]*new_psi[i+1] for i in range(n)), F())-W-J
                rhs = (1-alpha)*E-(1-alpha)*(J-Lz)-alpha*(W-F((n-1)*J, 2))
                assert Ep <= rhs
                cl_checks += 1
    return dict(old_players=n, old_topics=p, reserve=J, eta=str(eta), L=str(L),
                old_comparisons=old_checks, histories=len(actions), comparisons=checks,
                one_B_literal_histories=retained, minimum_slack=str(minimum_slack),
                W=W, M=str(M), W_lifted=W+J, M_lifted=str(Mp),
                quantitative_CL_checks=cl_checks, actual=list(zp))


def main():
    # Empty old topic is allowed, and the new topic is a distinct positive set.
    data = dict(players=2, topics=['A', 'empty'], customers=[dict(topics=[0], multiplicity=3)])
    actions = {(): 0, (0,): 0, (1,): 0}
    empty = audit(data, actions, 3)
    data = json.loads((ROOT/'examples/customer_attraction/individual_security_failure.json').read_text())
    cert = json.loads((ROOT/'evidence/certificates/customer_attraction/individual_security_failure.json').read_text())
    cert = cert.get('strategy', cert)
    actions = {tuple(r['history']): r['action'] for r in cert['actions']}
    nontrivial = audit(data, actions, 19)
    result = dict(status='PASS', scope='two fixed complete-history construction and CL regressions; not a proof of U, Mpath, or half',
                  empty_old_topic=empty, existing_individual_security_policy=nontrivial)
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
