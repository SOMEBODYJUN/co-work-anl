"""Fraction regression for the explicitly stated general OFF-IC/FRESH bridge.

No instance search: replays two already stored full SPE certificates, then all
actual-prefix query -> later prescribed-action parent contexts. Universal claims
are proved in the companion markdown, not inferred from these checks.
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
    inst = json.loads((ROOT / 'examples/customer_attraction' / (name + '.json')).read_text())
    cert = json.loads((ROOT / 'evidence/certificates/customer_attraction' / (name + '.json')).read_text())
    policy = {tuple(r['history']): r['action']
              for r in cert.get('strategy', cert)['actions']}
    likes = [frozenset(t['topics']) for t in inst['customers']
             for _ in range(t['multiplicity'])]
    m, q = inst['players'], len(inst['topics'])

    def finish(h):
        h = tuple(h)
        while len(h) < m:
            h += (policy[h],)
        return h

    def counts(z):
        return [sum(a in t for a in z) for t in likes]

    def pay(z, i):
        c = counts(z)
        return sum((F(1, c[x]) for x, t in enumerate(likes) if z[i] in t), F())

    source_ic = 0
    for depth in range(m):
        for h in product(range(q), repeat=depth):
            z = finish(h)
            for a in range(q):
                assert pay(z, depth) >= pay(finish(h + (a,)), depth)
                source_ic += 1

    Z = finish(())
    C = {x for x, t in enumerate(likes) if any(a in t for a in Z)}
    optimum = max(combinations_with_replacement(range(q), m),
                  key=lambda z: sum(any(a in t for a in z) for t in likes))
    O = {x for x, t in enumerate(likes) if any(a in t for a in optimum)}
    R = O - C
    seen = set()
    contexts = fresh_checks = tracked_terms = new_outside_terms = recipients = 0
    max_half_ratio = F()
    for j in range(m - 1):
        for parent_action in range(q):
            B = finish(Z[:j] + (parent_action,))
            for i in range(j + 1, m):
                g, a = B[:i], B[i]
                key = j, parent_action, i, g
                if key in seen:
                    continue
                seen.add(key)
                assert policy[g] == a and finish(g) == B
                A = finish(Z[:i] + (a,))
                W = finish(g + (Z[i],))
                cz, ca, cb, cw = map(counts, (Z, A, B, W))
                ell = pay(B, i) - pay(W, i)
                e = pay(Z, i) - pay(A, i)
                assert ell >= 0 and e >= 0
                tc = sum((F(1, cz[x]) - F(1, cw[x])
                          for x, t in enumerate(likes) if Z[i] in t), F())
                tc += sum((F(1, cb[x]) - F(1, ca[x])
                           for x in C if a in likes[x]), F())
                fresh = [x for x, t in enumerate(likes) if a in t and x not in C]
                tf = sum((F(1, cb[x]) - F(1, ca[x]) for x in fresh), F())
                assert e == tc + tf - ell
                h_to = defaultdict(F)
                for x in fresh:
                    U = {k for k in range(i + 1, m) if A[k] in likes[x]}
                    V = {k for k in range(i + 1, m) if B[k] in likes[x]}
                    b = sum(v in likes[x] for v in g)
                    assert ca[x] == 1 + len(U) and cb[x] == b + 1 + len(V)
                    assert F(1, cb[x]) - F(1, ca[x]) == F(len(U - V) - len(V - U) - b, ca[x] * cb[x])
                    fresh_checks += 1
                    if x not in O:
                        new_outside_terms += 1
                    if x in R and parent_action in likes[x]:
                        assert b >= 1
                        for k in U - V:
                            term = F(1, ca[x] * cb[x])
                            assert term <= F(1, 2 * ca[x])
                            h_to[k] += term
                            tracked_terms += 1
                for k, value in h_to.items():
                    full = pay(A, k)
                    assert full > 0 and value <= full / 2
                    max_half_ratio = max(max_half_ratio, value / full)
                    recipients += 1
                contexts += 1
    return {'case': name, 'unit_customers': len(likes), 'players': m,
            'source_full_history_IC_checks': source_ic,
            'parent_contexts': contexts, 'fresh_signed_identity_checks': fresh_checks,
            'new_outside_terms_kept': new_outside_terms,
            'tracked_positive_recipient_terms': tracked_terms,
            'whole_recipient_half_checks': recipients,
            'max_tracked_whole_coefficient': str(max_half_ratio)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', help='new output filename in this directory')
    args = parser.parse_args()
    out = {'status': 'PASS', 'scope': 'definition-level regression; no global cost claim',
           'cases': [run(n) for n in ('portfolio_matching_failure', 'root_tax_failure')]}
    # Pure local count arithmetic, not a purported SPE: old prefix=1,
    # off-future=0, actual-query future=2. Two new recipient charges each 1/6
    # and old-prefix credit -1/6 sum to the fresh reset 1/2-1/3=1/6.
    ca, cb, old_prefix = 3, 2, 1
    term = F(1, ca * cb)
    assert 2 * term - old_prefix * term == F(1, cb) - F(1, ca)
    assert term / F(1, ca) == F(1, 2)
    out['nonzero_local_count_regression'] = {
        'scope': 'algebra only, not a game or SPE certificate',
        'new_recipient_charges': [str(term), str(term)],
        'old_prefix_credit': str(-term),
        'net_fresh_reset': str(term),
        'whole_recipient_fraction_if_only_this_customer': '1/2'}
    if args.output:
        p = (HERE / args.output).resolve()
        assert p.parent == HERE.resolve()
        with p.open('x') as f:
            json.dump(out, f, indent=2)
            f.write('\n')
    print(json.dumps(out, indent=2))
