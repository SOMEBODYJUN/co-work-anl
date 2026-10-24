"""Unit-customer Fraction regression, independent of solvers and author code."""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from pathlib import Path
import json
import platform


def audit(name, data, cert):
    m, k = data['players'], len(data['topics'])
    clients = [set(t['topics']) for t in data['customers']
               for _ in range(t.get('multiplicity', 1))]
    sets = [{x for x, t in enumerate(clients) if a in t} for a in range(k)]
    sigma = {tuple(t['history']): t['action'] for t in cert.get('strategy', cert)['actions']}
    hs = [h for i in range(m) for h in product(range(k), repeat=i)]
    assert set(hs) == set(sigma)

    def finish(h):
        h = tuple(h)
        while len(h) < m:
            h += (sigma[h],)
        return h

    def loads(z):
        return [sum(a in t for a in z) for t in clients]

    def pay(z, i, selected=None):
        c = loads(z)
        return sum((F(1, c[x]) for x in sets[z[i]] if selected is None or x in selected), F())

    z = finish(())
    covered = set().union(*(sets[a] for a in z))
    u = [pay(z, i) for i in range(m)]
    opt = max(combinations_with_replacement(range(k), m),
              key=lambda t: len(set().union(*(sets[a] for a in t))))
    owner = {}
    for i, a in enumerate(opt):
        for x in sets[a]:
            owner.setdefault(x, i)
    missing = set(owner)-covered
    rows, ic = {}, 0
    for h in hs:
        i, a = len(h), sigma[h]
        b, reset = finish(h), finish(z[:i]+(a,))
        cb, ca = loads(b), loads(reset)
        v, d = pay(b, i), pay(reset, i)
        for aa in range(k):
            assert v >= pay(finish(h+(aa,)), i)
            ic += 1
        e = u[i]-d
        assert e >= 0
        qf, qa = defaultdict(F), defaultdict(F)
        nf = jf = lf = na = ja = la = past = F()
        for x in sets[a]:
            aa = {j for j in range(m) if j != i and x in sets[reset[j]]}
            bb = {j for j in range(m) if j != i and x in sets[b[j]]}
            unit = F(1, ca[x]*cb[x])
            assert F(1, cb[x])-F(1, ca[x]) == (len(aa-bb)-len(bb-aa))*unit
            ja += unit
            la += len(aa & bb)*unit
            na += len(bb-aa)*unit
            for j in aa-bb:
                if j < i:
                    assert x in covered and x in sets[z[j]]
                    past += unit
                else:
                    qa[j] += unit
            if x not in covered:
                assert all(j > i for j in aa)
                jf += unit
                lf += len(aa & bb)*unit
                nf += len(bb-aa)*unit
                for j in aa-bb:
                    qf[j] += unit
        xp, yp = pay(b, i, covered), pay(reset, i, covered)
        pf, pa = sum(qf.values(), F()), sum(qa.values(), F())
        assert v-pf == xp+jf+lf
        assert v == u[i]+xp-yp+pf-nf-e
        assert v-pa-past == ja+la == d-na
        assert v-pa == u[i]+past-na-e
        if v:
            assert pf < v and pa+past < v
            future = list(range(i+1, m))
            for mask in range(1 << len(future)):
                js = [j for t, j in enumerate(future) if mask >> t & 1]
                assert sum((qf[j] for j in js), F())/v <= F(len(js), len(js)+1)
        else:
            assert not sets[a]
        rows[h] = dict(i=i, v=v, e=e, qf=qf, qa=qa, xp=xp, yp=yp,
                       nf=nf, jf=jf, lf=lf, na=na, ja=ja, la=la, past=past,
                       dest={j: reset[:j] for j in set(qf) | set(qa)})
    seed, absorbed = defaultdict(F), F()
    for i, a in enumerate(opt):
        y = finish(z[:i]+(a,))
        cy = loads(y)
        own = {x for x in missing if owner[x] == i}
        absorbed += sum((F(1, cy[x]) for x in own), F())
        for j in range(i+1, m):
            seed[y[:j]] += sum((F(1, cy[x]) for x in own & sets[y[j]]), F())
    total = sum(seed.values(), F())
    assert absorbed+total == len(missing)
    output = {}
    for mode in ['fresh', 'all']:
        mass, diag, ledger, pc, visits = defaultdict(F, seed), F(), F(), F(), F()
        for h in hs:
            if not mass[h]:
                continue
            r = rows[h]
            assert r['v'] > 0
            beta = mass[h]/r['v']
            visits += mass[h]
            if mode == 'fresh':
                q = r['qf']
                diag += beta*(r['xp']+r['jf']+r['lf'])
                ledger += beta*(u[r['i']]+r['xp']-r['yp']-r['nf']-r['e'])
            else:
                q = r['qa']
                diag += beta*(r['ja']+r['la'])
                pc += beta*r['past']
                ledger += beta*(u[r['i']]+r['past']-r['na']-r['e'])
            for j, value in q.items():
                dest = r['dest'][j]
                assert len(dest) > len(h)
                assert finish(dest) == finish(z[:len(h)]+(sigma[h],))
                mass[dest] += beta*value
        assert total == diag+pc == ledger
        if mode == 'fresh':
            assert visits <= sum((amount*F(m-len(h)+1, 2) for h, amount in seed.items()), F())
        output[mode] = {key: str(val) for key, val in dict(seed=total, diagonal=diag,
                            past_coupon=pc, signed_ledger=ledger, visits=visits).items()}
    return dict(name=name, players=m, topics=k, unit_customers=len(clients),
                complete_ic_checks=ic, actual=list(z), optimal=list(opt),
                fresh_positive_edges=sum(sum(v > 0 for v in row['qf'].values()) for row in rows.values()),
                all_positive_future_edges=sum(sum(v > 0 for v in row['qa'].values()) for row in rows.values()),
                welfare=len(covered), missing=len(missing), source_absorbed=str(absorbed), flows=output)


def main():
    scalar_checks = scalar_positive = 0
    for n in range(1, 7):
        for i in range(n):
            for ma in range(1 << n):
                if not (ma >> i & 1):
                    continue
                aa = {j for j in range(n) if ma >> j & 1}
                for mb in range(1 << n):
                    if not (mb >> i & 1):
                        continue
                    bb = {j for j in range(n) if mb >> j & 1}
                    ca, cb = len(aa), len(bb)
                    unit = F(1, ca*cb)
                    pos, neg = len(aa-bb)*unit, len(bb-aa)*unit
                    assert F(1, cb)-F(1, ca) == pos-neg
                    assert F(1, cb)-pos == (1+len((aa & bb)-{i}))*unit
                    scalar_checks += 1
                    scalar_positive += bool(pos)
                    if all(j >= i for j in aa):
                        assert pos/F(1, cb) <= F(n-i-1, n-i)
    result = []
    for name in ['portfolio_matching_failure', 'root_tax_failure', 'individual_security_failure',
                 'eight_cce_welfare_gap', 'coverage_opportunity_failure', 'prefix_balance_failure']:
        data = json.loads(Path(f'examples/customer_attraction/{name}.json').read_text())
        cert = json.loads(Path(f'evidence/certificates/customer_attraction/{name}.json').read_text())
        result.append(audit(name, data, cert))
    for m in [1, 3]:
        empty = dict(players=m, topics=['Empty'], customers=[])
        actions = [dict(history=list(h), action=0) for i in range(m) for h in product([0], repeat=i)]
        result.append(audit(f'empty_m{m}', empty, dict(actions=actions)))
    data = dict(players=1, topics=['A', 'Empty'], customers=[dict(topics=[0])])
    result.append(audit('one_player', data, dict(actions=[dict(history=[], action=0)])))
    print(json.dumps(dict(python=platform.python_version(), arithmetic='fractions.Fraction',
                         status='finite_exact_regression_not_a_general_proof',
                         scalar_algebra_not_spe=dict(checks=scalar_checks, positive_cases=scalar_positive),
                         cases=result), indent=2))


if __name__ == '__main__':
    main()
