"""Exact regression of the stated general routing identities on old certificates.

No instance search, no new equilibrium selection, no claim of a capacity bound.
The mathematical statements are proved in all_fresh_submarkov_elimination.md.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations_with_replacement, product
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]


def run(name):
    ins = json.loads((ROOT / 'examples/customer_attraction' / f'{name}.json').read_text())
    cert = json.loads((ROOT / 'evidence/certificates/customer_attraction' / f'{name}.json').read_text())
    policy = {tuple(r['history']): r['action'] for r in cert.get('strategy', cert)['actions']}
    types = [(frozenset(t['topics']), t['multiplicity']) for t in ins['customers']]
    m, q = ins['players'], len(ins['topics'])

    def finish(h):
        h = tuple(h)
        while len(h) < m:
            h += (policy[h],)
        return h

    def counts(z):
        return [sum(a in likes for a in z) for likes, _ in types]

    def pay(z, i, keep=lambda x: True):
        c = counts(z)
        return sum((F(w, c[x]) for x, (likes, w) in enumerate(types)
                    if keep(x) and z[i] in likes), F())

    def coverage(z):
        return sum(w for likes, w in types if any(a in likes for a in z))

    Z = finish(())
    cz = counts(Z)
    C = {x for x, c in enumerate(cz) if c}
    actual_pay = [pay(Z, i) for i in range(m)]
    histories = [h for d in range(m) for h in product(range(q), repeat=d)]
    records = {}
    ic_checks = subset_checks = full_future_edges = past_coupons = 0

    for g in histories:
        i = len(g)
        B = finish(g)
        a = policy[g]
        A = finish(Z[:i] + (a,))
        W = finish(g + (Z[i],))
        ca, cb = counts(A), counts(B)
        v, d = pay(B, i), pay(A, i)
        e, ell = actual_pay[i] - d, v - pay(W, i)
        assert e >= 0 and ell >= 0
        for action in range(q):
            assert v >= pay(finish(g + (action,)), i)
            ic_checks += 1
        rec = {'i': i, 'B': B, 'A': A, 'v': v, 'd': d, 'e': e,
               'ell': ell, 'X': pay(B, i, lambda x: x in C),
               'Y': pay(A, i, lambda x: x in C)}
        for mode in ('fresh', 'all'):
            edges, coupons = defaultdict(F), defaultdict(F)
            neg = diag = common = F()
            for x, (likes, w) in enumerate(types):
                if a not in likes or (mode == 'fresh' and x in C):
                    continue
                JA = {j for j in range(m) if j != i and A[j] in likes}
                JB = {j for j in range(m) if j != i and B[j] in likes}
                raw = F(w, ca[x] * cb[x])
                assert F(w, cb[x]) - F(w, ca[x]) == raw * (len(JA - JB) - len(JB - JA))
                diag += raw
                common += raw * len(JA & JB)
                neg += raw * len(JB - JA)
                for j in JA - JB:
                    if j > i:
                        r = A[:j]
                        assert finish(r) == A and policy[r] == A[j]
                        assert pay(A, j) > 0
                        edges[r] += raw
                        if mode == 'all':
                            full_future_edges += 1
                    else:
                        assert mode == 'all' and x in C and Z[j] in likes and g[j] not in likes
                        coupons[(j, x)] += raw
                        past_coupons += 1
            p_future, p_past = sum(edges.values(), F()), sum(coupons.values(), F())
            restricted_v = v if mode == 'all' else v - rec['X']
            restricted_d = d if mode == 'all' else d - rec['Y']
            assert restricted_v - restricted_d == p_future + p_past - neg
            assert restricted_v - p_future - p_past == diag + common
            if mode == 'all':
                assert v - p_future - p_past == d - neg
                assert (v == 0 and p_future == p_past == diag == common == 0) or v > p_future + p_past
            else:
                assert v - p_future == rec['X'] + diag + common
            if v:
                candidates = range(m) if mode == 'all' else range(i + 1, m)
                candidates = tuple(j for j in candidates if j != i)
                role_q = defaultdict(F)
                for r, amount in edges.items():
                    role_q[len(r)] += amount
                for (j, _), amount in coupons.items():
                    role_q[j] += amount
                for bits in product((0, 1), repeat=len(candidates)):
                    J = {j for j, flag in zip(candidates, bits) if flag}
                    lhs = sum((role_q[j] for j in J), F()) / v
                    assert lhs <= F(len(J), len(J) + 1)
                    subset_checks += 1
            rec[mode] = {'edges': dict(edges), 'coupons': dict(coupons),
                         'Pfuture': p_future, 'Ppast': p_past, 'N': neg,
                         'J': diag, 'L': common}
        records[g] = rec

    optimum = max(combinations_with_replacement(range(q), m), key=coverage)
    O = {x for x, (likes, _) in enumerate(types) if any(a in likes for a in optimum)}
    R = O - C
    b = defaultdict(F)
    source_absorb = F()
    for x in R:
        likes, w = types[x]
        owner = next(i for i, a in enumerate(optimum) if a in likes)
        Y = finish(Z[:owner] + (optimum[owner],))
        cy = counts(Y)[x]
        source_absorb += F(w, cy)
        for j in range(owner + 1, m):
            if Y[j] in likes:
                r = Y[:j]
                assert policy[r] == Y[j] and records[r]['v'] > 0
                b[r] += F(w, cy)
    source_mass = sum(w for x, (_, w) in enumerate(types) if x in R)
    assert source_mass == source_absorb + sum(b.values(), F())

    flows = {}
    for mode in ('fresh', 'all'):
        incoming = defaultdict(F, b)
        mass_loss = ledger = actual_repeat = past_exit = F()
        active = transfers = 0
        for g in histories:
            rec = records[g]
            if not incoming[g]:
                continue
            active += 1
            assert rec['v'] > 0
            beta = incoming[g] / rec['v']
            r = rec[mode]
            for child, amount in r['edges'].items():
                assert len(child) > len(g)
                incoming[child] += beta * amount
                transfers += 1
            mass_loss += beta * (rec['v'] - r['Pfuture'])
            actual_repeat += beta * actual_pay[len(g)]
            if mode == 'fresh':
                ledger += beta * (actual_pay[len(g)] + rec['X'] - rec['Y'] - r['N'] - rec['e'])
                assert rec['v'] - r['Pfuture'] == rec['X'] + r['J'] + r['L']
            else:
                ledger += beta * (actual_pay[len(g)] + r['Ppast'] - r['N'] - rec['e'])
                past_exit += beta * r['Ppast']
                assert rec['v'] - r['Pfuture'] == r['J'] + r['L'] + r['Ppast']
        assert mass_loss == ledger == sum(b.values(), F())
        flows[mode] = {'active_natural_contexts': active,
                       'input_captured_mass': str(sum(b.values(), F())),
                       'exact_ledger': str(ledger),
                       'raw_repeated_actual_profit_term': str(actual_repeat),
                       'past_coupon_exit_mass': str(past_exit),
                       'source_initialized_positive_transfers': transfers}
    probes = {}
    for mode in ('fresh', 'all'):
        seeds = [g for g in histories if records[g]['v'] and records[g][mode]['edges']]
        if not seeds:
            probes[mode] = {'status': 'no positive edge in these fixed certificates'}
            continue
        seed = seeds[0]
        incoming = defaultdict(F, {seed: F(1)})
        ledger = F()
        transfers = active = 0
        for g in histories:
            if not incoming[g]:
                continue
            active += 1
            rec, r = records[g], records[g][mode]
            beta = incoming[g] / rec['v']
            for child, amount in r['edges'].items():
                assert len(child) > len(g)
                incoming[child] += beta * amount
                transfers += 1
            if mode == 'fresh':
                ledger += beta * (actual_pay[len(g)] + rec['X'] - rec['Y'] - r['N'] - rec['e'])
            else:
                ledger += beta * (actual_pay[len(g)] + r['Ppast'] - r['N'] - rec['e'])
        assert ledger == 1 and transfers > 0
        probes[mode] = {'scope': 'arbitrary unit profit injection permitted by the routing lemma; not an OPT-owner initialization',
                        'history': list(seed), 'active_contexts': active,
                        'positive_transfers': transfers, 'exact_ledger': str(ledger)}
    return {'case': name, 'IC_checks': ic_checks, 'subset_checks': subset_checks,
            'all_future_customer_edges': full_future_edges,
            'past_coupon_labels_checked': past_coupons,
            'source_R_mass': source_mass, 'source_current_absorb': str(source_absorb),
            'flows': flows, 'nonzero_edge_probes': probes}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    output = HERE / args.output
    assert output.resolve().parent == HERE.resolve()
    result = {'status': 'PASS', 'scope': 'existing-certificate formula and domain regression only; no coupon capacity claim',
              'cases': [run(n) for n in ('portfolio_matching_failure', 'root_tax_failure')]}
    with output.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps(result, indent=2))
