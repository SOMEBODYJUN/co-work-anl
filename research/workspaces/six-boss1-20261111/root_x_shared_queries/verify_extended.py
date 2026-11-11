"""Independent literal/orbit audit of the entire shared-eta append.

No builder, numerical point, optimizer or third-party package is imported.
Orbit membership is reconstructed from all 720 permutations of each named
representative.  Old masses are reconstructed from the own four-state maps.
All arithmetic is rational; all writes stay in this directory.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations, product
from pathlib import Path
import gzip
import json
import time

AUDIT_DIR = Path(__file__).resolve().parent
BASE = AUDIT_DIR.parent
NS = ('old', 'mu', 'eta', 'z', 'cost')


def read_gz(name):
    with gzip.open(AUDIT_DIR / name, 'rt') as f:
        return json.load(f)


def freeze(x):
    return tuple(map(freeze, x)) if isinstance(x, (tuple, list)) else x


def tidy(a):
    return {k: v for k, v in a.items() if v}


def add(a, b, scale=Q(1)):
    for k, v in b.items():
        a[k] = a.get(k, Q()) + scale * v
    return a


def decode(a):
    return {(ns, j): Q(v) for ns in NS for j, v in a.get(ns, [])}


def triple(a):
    return {(ns, j): Q(v) for ns, j, v in a}


def signature(a):
    return tuple(sorted(tidy(a).items()))


def canon(qq):
    seen, answer = {}, []
    for family, role, indices in qq:
        answer.append((family, role, tuple(seen.setdefault(i, len(seen)) for i in indices)))
    return tuple(answer)


def move(q, p):
    return q[0], q[1], tuple(p[i] for i in q[2])


def binary(s, n):
    return tuple(map(int, format(s, f'0{n}b')))


def payoff(e, n):
    return Q(e, n) if e else Q()


def run():
    start = time.perf_counter()
    data = read_gz('extended_interface_exact.json.gz')
    direct = read_gz('direct_interface_exact.json.gz')
    inv = read_gz('query_orbits_exact.json.gz')
    own = json.loads((BASE / 'root_x_joint_contract/own_blocks.json').read_text())
    hist = {h: d for h, d in own['hist_records']}
    xmap = {b['H_column']: b['X_column'] for b in own['blocks']}
    mu = data['mu_columns']
    index = {(d['hist'], d['old_word'], d['state']): i for i, d in enumerate(mu)}
    assert mu == direct['mu_columns'] == data['eta_columns']
    counts = Counter()
    masses = {}
    for b in own['blocks']:
        h = b['H_column']
        group = freeze(b['key'][2]) if b['key'][0] == 'own-RZ' else None
        for member, letter, ycol in ((0, 'R', b['yQ_column']), (1, 'Z', b['yR_column'])):
            total = {}
            for ab, values in b['mass_by_QR'].items():
                if int(ab[member]):
                    add(total, {('old', i): Q(v) for i, v in values})
            token = (letter, group) if group is not None else ('H', member)
            one = {('old', ycol): Q(1)}
            masses[h, token] = tidy(total), one
    assert len(masses) == 420
    tails = {s: binary(s, 5) for s in range(32)}
    words_by_h = {h: [w for w, n in enumerate(d['hist']) for _ in range(n)] for h, d in hist.items()}
    aq, cq = {}, {}
    for h, d in hist.items():
        a = tuple(map(int, d['actual_bits']))
        aq['old', h] = payoff(a[4], sum(a))
        cq['old', xmap[h]] = Q(1, sum(a[:4])+1)
    aq = tidy(aq)

    def resolve(h, q):
        family, role, ids = q
        words = words_by_h[h]
        if family == 'A':
            return ('constant', int(hist[h]['actual_bits'][role]))
        if family in ('T', 'B', 'C'):
            w = binary(words[ids[0]], 3)
            return ('constant', w[{'T': 0, 'B': 1, 'C': 2}[family]])
        if family in ('H', 'X'):
            return family, role
        if family == 'Y':
            return family, role, words[ids[0]]
        i, j = ids
        return family, (role, int(i == j), binary(words[i], 3), binary(words[j], 3))

    marginal_cache = {}

    def marginal(h, token):
        key = h, token
        if key in marginal_cache:
            return marginal_cache[key]
        family = token[0]
        if family == 'Y':
            total = {('mu', index[h, token[2], s]): Q(tails[s][token[1]]) for s in range(32)}
            one = {('eta', index[h, token[2], s]): Q(tails[s][token[1]]) for s in range(32)}
        elif family == 'constant':
            total = {('old', h): Q(token[1])}
            one = {('old', xmap[h]): Q(token[1])}
        elif family == 'X':
            total = one = {('old', xmap[h]): Q(1)}
        else:
            total, one = masses[h, token]
        zero = add(dict(total), one, Q(-1))
        answer = tidy(total), tidy(zero), tidy(one)
        marginal_cache[key] = answer
        return answer

    zlookup = {}
    for i, d in enumerate(data['z_columns']):
        assert len(d['caps']) == 2
        caps = tuple(sorted(signature(triple(c)) for c in d['caps']))
        key = d['hist'], d['X_bit'], caps
        assert key not in zlookup
        zlookup[key] = i
        assert d['hist'] in hist and d['X_bit'] in (0, 1)
        counts['conditional_min_descriptors'] += 1
    costlookup = {}
    for i, d in enumerate(data['cost_columns']):
        h, w, epsilon = d['hist'], d['old_word'], d['X_bit']
        expected_indices = [index[h, w, s] for s in range(32)]
        price = [Q(1, (w//4)+sum(tails[s][:3])+1+epsilon) for s in range(32)]
        assert d['source_indices'] == expected_indices
        assert list(map(Q, d['prices'])) == price
        assert list(map(Q, d['lambdas'])) == sorted(set(price))
        key = h, w, epsilon, signature(triple(d['query']))
        assert key not in costlookup
        costlookup[key] = i
        counts['conditional_sorting_descriptors'] += 1
        counts['conditional_sorting_price_coefficients'] += 32

    # Independently enumerate each full S6 orbit from the named representative.
    ps = tuple(permutations(range(6)))
    all_catalog = set(freeze(q) for name in ('old_catalog', 'X_catalog', 'root_catalog') for q in inv[name])
    assert len(all_catalog) == 189
    seen_rc, seen_rp = set(), set()
    rc_orbits, rp_orbits = [], []
    for item in inv['actual_RC_unordered']:
        key = freeze(item['key'])
        generated = {tuple(sorted(move(q, p) for q in key)) for p in ps}
        literals = {tuple(sorted(freeze(pair))) for pair in item['literals']}
        assert generated == literals and len(literals) == item['literal_count']
        assert not (seen_rc & generated)
        assert all(a in all_catalog and b in all_catalog and ('Y' in (a[0], b[0])) for a, b in generated)
        seen_rc |= generated
        rc_orbits.append(sorted(generated))
        counts['RC_permutation_images'] += 720
    for item in inv['root_PAIR']:
        key = freeze(item['key'])
        assert key[0] == ('source', 0, (0,))
        generated = {(p[0], move(key[1], p)) for p in ps}
        literals = {(i, freeze(q)) for i, q in item['literals']}
        assert generated == literals and len(literals) == item['literal_count']
        assert not (seen_rp & generated)
        assert all(q in all_catalog for i, q in generated)
        seen_rp |= generated
        rp_orbits.append(sorted(generated))
        counts['RP_permutation_images'] += 720
    assert len(seen_rc) == 5235 and len(seen_rp) == 1134
    assert seen_rp == {(i, q) for i in range(6) for q in all_catalog}
    expected_rc = {tuple(sorted((q, r))) for q, r in product(all_catalog, repeat=2) if 'Y' in (q[0], r[0])}
    assert seen_rc == expected_rc
    expected_ordered = {canon((q, r)) for q, r in product(all_catalog, repeat=2) if 'Y' in (q[0], r[0])}
    assert {freeze(d['key']) for d in inv['actual_RC_ordered']} == expected_ordered
    for d in inv['actual_RC_ordered']:
        q, r = freeze(d['key'])
        generated = {(move(q, p), move(r, p)) for p in ps}
        assert len(generated) == d['literal_count']
        assert {tuple(sorted(p)) for p in generated} == set(rc_orbits[d['unordered']])
        counts['ordered_to_unordered_maps'] += 1

    row_by_name = {freeze(r['name']): r for r in data['principal_rows']}
    assert len(row_by_name) == 236
    rp_record = defaultdict(dict)
    rc_record = defaultdict(dict)
    for b in data['root_PAIR_blocks']:
        key = b['hist'], b['source_word'], freeze(b['query']), b['same_root']
        assert key not in rp_record[b['orbit']]
        assert Q(b['factor']) == Q(b['count'], b['orbit_size'])
        rp_record[b['orbit']][key] = b
    for b in data['actual_RC_blocks']:
        key = b['hist'], tuple(sorted(map(freeze, b['queries']))), b['same_root']
        assert key not in rc_record[b['orbit']]
        assert Q(b['factor']) == Q(b['count'], b['orbit_size'])
        rc_record[b['orbit']][key] = b

    def root_piece(h, w, query, same):
        out = {}
        for state in range(32):
            e = tails[state]
            p = w//4+sum(e[:3])
            N = w//4+sum(e)
            wallet = payoff(e[3], N)+payoff(e[4], N)+Q(e[3], (p+1)*(p+2))
            j = index[h, w, state]
            if query[0] == 'X':
                # Literal Phi(X,X) at bits 0 and 1.
                mu_c = wallet
                eta_c = -Q(1, p+1)-Q(1, p+2)
            elif query[0] == 'constant' or same:
                bit = query[1] if query[0] == 'constant' else e[query[1]]
                f0 = wallet-Q(bit, p+1)
                f1 = wallet-Q(1, p+1)-Q(bit, p+2)
                mu_c, eta_c = f0, f1-f0
            else:
                mu_c, eta_c = wallet, -Q(1, p+1)
            out['mu', j], out['eta', j] = mu_c, eta_c
        ids = []
        if query[0] not in ('constant', 'X') and not same:
            _, zero, one = marginal(h, query)
            for epsilon, q in enumerate((zero, one)):
                j = costlookup[h, w, epsilon, signature(q)]
                out['cost', j] = Q(-1)
                ids.append(j)
        return tidy(out), ids

    for oi, literal in enumerate(rp_orbits):
        expected, expected_blocks = {}, {}
        for h in hist:
            word = words_by_h[h]
            frequencies = Counter((word[i], resolve(h, q), q[0] == 'Y' and q[2] == (i,)) for i, q in literal)
            for (w, query, same), multiplicity in frequencies.items():
                factor = Q(multiplicity, len(literal))
                block, ids = root_piece(h, w, query, same)
                add(expected, block, factor)
                b = rp_record[oi][h, w, query, same]
                assert Q(b['factor']) == factor
                if ids:
                    assert b['method'] == 'conditional-sorting-envelope' and b['cost'] == ids
                else:
                    assert b['method'].startswith('exact-')
                expected_blocks[h, w, query, same] = factor
                counts['RP_literal_blocks'] += 1
        assert set(rp_record[oi]) == set(expected_blocks)
        row = row_by_name['RP-ORBIT', oi]
        assert tidy(expected) == decode(row), ('root principal mismatch', oi)
        counts['RP_nonzero_coefficients'] += len(tidy(expected))
        counts['RP_principal_rows'] += 1

    def actual_piece(h, q, r, same):
        P = sum(map(int, hist[h]['actual_bits'][:4]))
        qt, q0, q1 = marginal(h, q)
        rt, r0, r1 = marginal(h, r)
        if q[0] == 'constant':
            qt = {('mu', index[h, r[2], s]): Q(q[1]) for s in range(32)}
        elif r[0] == 'constant':
            rt = {('mu', index[h, q[2], s]): Q(r[1]) for s in range(32)}
        out = add(add({}, qt, -Q(1, P+1)), rt, -Q(1, P+1))
        ids = []
        if q[0] == 'constant' or r[0] == 'constant':
            bit, marginal_q = (q[1], rt) if q[0] == 'constant' else (r[1], qt)
            inter = {i: v*bit for i, v in marginal_q.items()}
        elif q[0] == 'X' or r[0] == 'X':
            inter = r1 if q[0] == 'X' else q1
        elif same:
            assert q[0] == r[0] == 'Y' and q[2] == r[2]
            inter = {('mu', index[h, q[2], s]): Q(tails[s][q[1]] & tails[s][r[1]]) for s in range(32)}
        else:
            inter = {}
            for epsilon, (a, b) in enumerate(((q0, r0), (q1, r1))):
                j = zlookup[h, epsilon, tuple(sorted((signature(a), signature(b))))]
                inter['z', j] = Q(1)
                ids.append(j)
        return tidy(add(out, inter, Q(1, (P+1)*(P+2)))), ids

    for oi, literals in enumerate(rc_orbits):
        expected = add(dict(aq), cq)
        expected_blocks = {}
        for h in hist:
            frequencies = Counter()
            for a, b in literals:
                q, r = sorted((resolve(h, a), resolve(h, b)))
                same = a[0] == b[0] == 'Y' and a[2] == b[2]
                frequencies[q, r, same] += 1
            for (q, r, same), multiplicity in frequencies.items():
                factor = Q(multiplicity, len(literals))
                block, ids = actual_piece(h, q, r, same)
                add(expected, block, factor)
                b = rc_record[oi][h, (q, r), same]
                assert Q(b['factor']) == factor
                if ids:
                    assert b['method'] == 'conditional-intersection-envelope' and b['z'] == ids
                else:
                    assert b['method'].startswith('exact-')
                expected_blocks[h, (q, r), same] = factor
                counts['RC_literal_blocks'] += 1
        assert set(rc_record[oi]) == set(expected_blocks)
        row = row_by_name['RC-ORBIT', oi]
        assert tidy(expected) == decode(row), ('actual principal mismatch', oi)
        counts['RC_nonzero_coefficients'] += len(tidy(expected))
        counts['RC_principal_rows'] += 1

    # Bounds and finite dual pieces reconstructed independently, including signs.
    seen = set()
    for row in data['z_upper_rows']:
        name, j, cap = row['name']
        assert name == 'conditional-min-cap' and (j, cap) not in seen
        seen.add((j, cap))
        expected = triple(data['z_columns'][j]['caps'][cap])
        add(expected, {('z', j): Q(-1)})
        assert tidy(expected) == decode(row)
        counts['conditional_min_cap_rows'] += 1
        counts['conditional_min_cap_nonzeros'] += len(tidy(expected))
    assert seen == set(product(range(len(data['z_columns'])), (0, 1)))
    seen = set()
    for row in data['sorting_piece_rows']:
        _, j, value = row['name']
        lam = Q(value)
        assert (j, lam) not in seen
        seen.add((j, lam))
        d = data['cost_columns'][j]
        expected = {('cost', j): Q(1)}
        add(expected, triple(d['query']), -lam)
        for index0, price in zip(d['source_indices'], map(Q, d['prices'])):
            delta = max(Q(), lam-price)
            if d['X_bit'] == 0:
                add(expected, {('mu', index0): delta, ('eta', index0): -delta})
            else:
                add(expected, {('eta', index0): delta})
        assert tidy(expected) == decode(row)
        counts['conditional_sorting_piece_rows'] += 1
        counts['conditional_sorting_piece_nonzeros'] += len(tidy(expected))
    assert seen == {(j, Q(lam)) for j, d in enumerate(data['cost_columns']) for lam in d['lambdas']}
    for row in data['principal_rows']:
        assert all(Q(value) >= 0 for _, value in row['z'])
        assert all(Q(value) <= 0 for _, value in row['cost'])
        assert all(0 <= j < 1216 for j, _ in row['eta'])
        counts['shared_eta_and_auxiliary_sign_rows'] += 1
    assert data['nonnegative_variables'] == ['all eta', 'all z', 'all cost; mu inherited']

    # The full append retains the exact 42-row layer with coefficient identities.
    for alias in data['direct_to_extended']:
        a, b = direct['rows'][alias['direct']], data['principal_rows'][alias['extended']]
        assert a['name'] == alias['direct_name'] and b['name'] == alias['extended_name']
        assert decode(a) == decode(b)
        counts['direct_to_extended_exact_row_matches'] += 1
    assert counts['direct_to_extended_exact_row_matches'] == 42
    assert data['eta_upper_rows'] == direct['eta_upper_rows']
    assert data['eta_equalities'] == direct['eta_equalities']

    # Verify finite sorting identity without optimization, with signs and zero/endpoints.
    # Positive prices and a fixed source mass permit a greedy exact minimizer.
    for epsilon in (0, 1):
        for perm in permutations((0, 1, 4)):
            prices = [Q(1, p+1+epsilon) for p in perm]
            measure = [Q(1, 4), Q(1, 2), Q(1, 4)]
            for q in (Q(), Q(1, 8), Q(1, 4), Q(1, 2), Q(7, 8), Q(1)):
                remain, greedy = q, Q()
                for i in sorted(range(3), key=lambda i: prices[i]):
                    selected = min(remain, measure[i])
                    greedy += selected*prices[i]
                    remain -= selected
                dual = max(lam*q-sum(m*max(lam-c, Q()) for m, c in zip(measure, prices)) for lam in prices)
                assert remain == 0 and greedy == dual
                counts['conditional_sorting_exact_truth_cases'] += 1
    for p in range(5):
        for z, q in product((0, 1), repeat=2):
            assert Q(z+q, p+1)-Q(z*q, (p+1)*(p+2)) == Q(z, p+1)+Q(q, p+1+z)
            counts['conditional_PAIR_pointwise_identities'] += 1
    # X-split intersection envelope dominates the true intersection and is no
    # larger than the unsplit envelope, on all small integer two-layer tables.
    for table in product(range(3), repeat=8):
        qt, rt, actual, split = 0, 0, 0, 0
        for epsilon in (0, 1):
            m00, m01, m10, m11 = table[4*epsilon:4*epsilon+4]
            q, r = m10+m11, m01+m11
            qt += q
            rt += r
            actual += m11
            split += min(q, r)
        assert actual <= split <= min(qt, rt)
        counts['conditional_intersection_truth_cases'] += 1

    inherited = BASE / data['inherited_root']['path']
    assert sha256(inherited.read_bytes()).hexdigest() == data['inherited_root']['sha256']
    assert data['inherited_root']['principal_rows'] == 438
    assert data['inherited_root']['inequalities'] == 36776
    assert data['inherited_root']['equalities'] == 38
    status = dict(status='INDEPENDENT_EXACT_EXTENDED_SHARED_X_INTERFACE_PASS', counts=dict(counts),
                  principal_rows=236, shared_eta_columns=1216, hist_groups=16, word_groups=38,
                  numerical_point_reads=0, optimizer_calls=0, full_global_law_claim=False,
                  sources={name: sha256((AUDIT_DIR/name).read_bytes()).hexdigest()
                           for name in ('extended_interface_exact.json.gz', 'direct_interface_exact.json.gz',
                                        'query_orbits_exact.json.gz', 'verify_extended.py')},
                  elapsed_seconds=time.perf_counter()-start)
    (AUDIT_DIR / 'extended_verification.json').write_text(json.dumps(status, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(status, ensure_ascii=False, sort_keys=True))


if __name__ == '__main__':
    run()
