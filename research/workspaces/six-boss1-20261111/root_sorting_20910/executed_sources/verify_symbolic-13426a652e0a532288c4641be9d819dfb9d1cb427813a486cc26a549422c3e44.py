"""Independent literal/sorting audit; standard library only.

No constructor or solver is imported.  The original 5699 rows are matched
byte-for-coefficient to the separately rerun independent inherited auditor.
New main rows are rebuilt using named indices, not multiplicity formulas.
Each RS2 piece is rebuilt and RS1/RS3 are checked by separate greedy values.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import combinations_with_replacement, permutations, product
from pathlib import Path
import gzip
import hashlib
import json
import time

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
KINDS = ('old', 'mu', 'aux', 'lower')
PIN = 'cb45ee6f8df153764c91bd77d0543527cc44719ff7cc43646ffce06a7921a932'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def freeze(x):
    return tuple(map(freeze, x)) if isinstance(x, (list, tuple)) else x


def bits(s, n=5):
    return tuple(map(int, format(s, f'0{n}b')))


def rational_income(n, d):
    return F(n, d) if n else F()


def pat(a):
    seen = {}
    return tuple(seen.setdefault(x, len(seen)) for x in a)


def nonzero(d):
    return tuple((k, v) for k, v in sorted(d.items()) if v)


def greedy(masses, prices, quantity):
    assert all(x >= 0 for x in masses) and 0 <= quantity <= sum(masses)
    left, cost = quantity, F()
    chosen = [F() for _ in masses]
    for s in sorted(range(len(masses)), key=lambda i: (prices[i], i)):
        take = min(left, masses[s])
        cost += take*prices[s]
        chosen[s] = take
        left -= take
    assert left == 0
    return cost, chosen


def dual_value(masses, prices, quantity):
    return max(lam*quantity-sum((m*max(lam-c, F()) for m, c in zip(masses, prices)), F())
               for lam in set(prices))


def main():
    start = time.perf_counter()
    modelpath = HERE/'symbolic_matrix_exact.json.gz'
    with gzip.open(modelpath, 'rt') as f:
        model = json.load(f)
    newpath = BASE/model['point_path']
    assert sha(newpath) == model['point_sha256'] == PIN
    point = json.loads(newpath.read_text())
    for source in model['sources']:
        assert sha(BASE/source['path']) == source['sha256']
    inherited = json.loads((BASE/'root_marginal_closure/symbolic_coefficients_exact.json').read_text())
    iaudit = json.loads((HERE/'inherited_independent_audit.json').read_text())
    assert iaudit['status'] == 'INDEPENDENT FULL-STATE MARGINAL AND CANONICAL-MIN AUDIT PASSED'
    assert iaudit['symbolic_sha256'] == sha(BASE/'root_marginal_closure/symbolic_coefficients_exact.json')
    old = [{k: v for k, v in c.items() if k != 'weight'} for c in point['columns'][:4849]]
    assert old == model['original_columns']
    previous = json.loads((BASE/'union_augmented_lp/augmented_lp_exact.json').read_text())
    desc = lambda c: {k: v for k, v in c.items() if k != 'weight'}
    assert list(map(desc, point['columns'][:15593])) == list(map(desc, previous['columns']))
    hist = {i: c for i, c in enumerate(old) if c['kind'] == 'hist'}
    groups = [(h, w) for h, c in hist.items() for w, n in enumerate(c['hist']) if n]
    mu = [dict(hist=h, old_word=w, state=s) for h, w in groups for s in range(32)]
    assert mu == model['mu_columns'] and len(groups) == 38 and len(mu) == 1216
    assert len(hist) == 16 and sum(F(point['columns'][h]['weight']) == 0 for h in hist) == 6
    lookup = {(c['hist'], c['old_word'], c['state']): j for j, c in enumerate(mu)}
    assert model['aux_columns'] == inherited['aux_columns']
    rows = model['rows']
    saved = {freeze(r['name']): r for r in rows}
    assert len(saved) == len(rows) == 36776
    for r in inherited['rows']:
        assert saved[freeze(r['name'])] == dict(r, lower=[])
    assert model['equalities'] == [dict(r, lower=[]) for r in inherited['equalities']]
    own, b4 = {}, defaultdict(list)
    for j, c in enumerate(old):
        if c['kind'] == 'hist':
            h = j
        if c['kind'] == 'joint-reply':
            family, diag, v, w = c['group']
            own.setdefault((h, family, diag, tuple(v), tuple(w)), {})[tuple(c['state'])] = j
        if c['kind'] == 'actual-B-family-state' and c['source'] == 4:
            b4[c['hist_column']].append((j, tuple(c['hidden'])+(c['ell']//6,)))
    assert len(own) == 194 and len(b4) == 16
    lower_lookup = {}
    for j, d in enumerate(model['lower_columns']):
        assert d['source_mu'] == [lookup[d['hist'], d['old_word'], s] for s in range(32)]
        prices = tuple(map(F, d['prices']))
        assert list(map(F, d['lambdas'])) == sorted(set(prices))
        key = (d['hist'], d['old_word'], prices,
               tuple((k, F(v)) for k, v in d['query_old']),
               tuple((k, F(v)) for k, v in d['query_mu']))
        assert key not in lower_lookup
        lower_lookup[key] = j
    expected = defaultdict(lambda: {k: defaultdict(F) for k in KINDS})

    def add(name, kind, col, val):
        expected[freeze(name)][kind][col] += val

    def lower(h, w, prices, qo=None, qm=None):
        return lower_lookup[h, w, tuple(prices), nonzero(qo or {}), nonzero(qm or {})]

    def safe(w, k):
        return [F(1, (w >> 2)+sum(bits(s)[:k])+5-k) for s in range(32)]

    def pprice(w, delta):
        return [F(1, (w >> 2)+sum(bits(s)[:3])+delta) for s in range(32)]

    def income(name, h, word, den, tail=None):
        t = word >> 2
        for state in range(32):
            e = bits(state)
            if tail is None:
                b = t+sum(e[:3])
                z = F(e[3], b+1+e[4])+F(e[4], b+1+e[3])+F(e[3], (b+1)*(b+2))
            else:
                z = rational_income(e[tail], t+sum(e))
            add(name, 'mu', lookup[h, word, state], z/den)

    # Every distinct named ordered pair, including repeated old words.
    pair_literal_count = 0
    floor_freq, pair_freq = Counter(), Counter()
    for h, c in hist.items():
        words = [w for w in range(8) for _ in range(c['hist'][w])]
        for i in range(6):
            for j in range(6):
                if i == j:
                    continue
                v, w = words[i], words[j]
                floor_freq[h, v, w] += F(1, 6)
                pair_freq[h, v, w] += F(1, 30)
                for k, l in product(range(5), repeat=2):
                    name = ('cross-floor-upper', k, l)
                    income(name, h, v, 6, k)
                    qm = {lookup[h, w, s]: F(bits(s)[l]) for s in range(32)}
                    add(name, 'lower', lower(h, v, safe(v, k), qm=qm), -F(1, 6))
                    pair_literal_count += 1
                for x in range(6):
                    for y in range(x, 6):
                        name = ('cross-pair-upper', x, y)
                        income(name, h, v, 30)
                        u, vq = {}, {}
                        for s in range(32):
                            roles = (w >> 2,)+bits(s)
                            a, b = roles[x], roles[y]
                            u[lookup[h, w, s]] = F(a+b-a*b)
                            vq[lookup[h, w, s]] = F(a*b)
                        add(name, 'lower', lower(h, v, pprice(v, 1), qm=u), -F(1, 30))
                        add(name, 'lower', lower(h, v, pprice(v, 2), qm=vq), -F(1, 30))
                        pair_literal_count += 1
    for (h, v, w), freq in floor_freq.items():
        n = hist[h]['hist']
        assert freq == F(n[v]*(n[w]-int(v == w)), 6)
        assert pair_freq[h, v, w] == freq/5
    orbits = defaultdict(list)
    for f, i, j, k in product(range(2), range(6), range(6), range(6)):
        if f or j != k:
            orbits[f, pat((i, j, k))].append((i, j, k))
    for (f, pattern), triples in orbits.items():
        i, j, k = triples[0]
        freq = Counter((p[i], p[j], p[k]) for p in permutations(range(6)))
        assert set(freq) == set(triples) and set(freq.values()) == {720//len(triples)}
    triple_literal_count = 0
    for h, c in hist.items():
        words = [w for w in range(8) for _ in range(c['hist'][w])]
        for (f, pattern), triples in orbits.items():
            den = len(triples)
            for i, j, k in triples:
                source = words[i]
                states = own[h, f, int(j == k), bits(words[j], 3), bits(words[k], 3)]
                for bit, namepart in enumerate(('R', 'Z')):
                    qo = {col: F(state[bit]) for state, col in states.items()}
                    for tail in range(5):
                        name = ('Y-to-'+namepart+'-upper', f, pattern, tail)
                        income(name, h, source, den, tail)
                        add(name, 'lower', lower(h, source, safe(source, tail), qo=qo), -F(1, den))
                        triple_literal_count += 1
        for i in range(6):
            word = words[i]
            for bit in (0, 1):
                qo = {col: F(state[bit]) for col, state in b4[h]}
                for tail in range(5):
                    name = ('Y-to-H'+str(bit+1)+'-upper', tail)
                    income(name, h, word, 6, tail)
                    add(name, 'lower', lower(h, word, safe(word, tail), qo=qo), -F(1, 6))
            for x, y in combinations_with_replacement(range(2), 2):
                name = ('new-pair-to-B4-upper', x, y)
                income(name, h, word, 6)
                u = {col: F(s[x]+s[y]-s[x]*s[y]) for col, s in b4[h]}
                v = {col: F(s[x]*s[y]) for col, s in b4[h]}
                add(name, 'lower', lower(h, word, pprice(word, 1), qo=u), -F(1, 6))
                add(name, 'lower', lower(h, word, pprice(word, 2), qo=v), -F(1, 6))
    assert len(expected) == 139
    newcoefs = 0
    for name, parts in expected.items():
        for kind in KINDS:
            direct = nonzero(parts[kind])
            assert direct == tuple((j, F(v)) for j, v in saved[name][kind]), (name, kind)
            newcoefs += len(direct)
    piececoefs = piececount = 0
    for j, d in enumerate(model['lower_columns']):
        for lam in map(F, d['lambdas']):
            wanted = {k: defaultdict(F) for k in KINDS}
            wanted['lower'][j] = F(1)
            for k, v in d['query_old']:
                wanted['old'][k] -= lam*F(v)
            for k, v in d['query_mu']:
                wanted['mu'][k] -= lam*F(v)
            for k, price in zip(d['source_mu'], map(F, d['prices'])):
                if price < lam:
                    wanted['mu'][k] += lam-price
            r = saved['sorting-piece', j, str(lam)]
            assert r['category'] == 'sorting-lower-piece'
            for kind in KINDS:
                direct = nonzero(wanted[kind])
                assert direct == tuple((k, F(v)) for k, v in r[kind])
                piececoefs += len(direct)
            piececount += 1
    assert piececount == 30938 and len(expected)+len(inherited['rows'])+piececount == len(rows)
    # Exact endpoint and interior RS1/RS2 truth tables; H=0 is included.
    templates = {tuple(map(F, d['prices'])) for d in model['lower_columns']}
    sorting_cases = nested_cases = bit_cases = 0
    for prices in templates:
        for salt in (0, 3):
            masses = [F((7*s+salt)%11, 13) for s in range(32)]
            order = sorted(range(32), key=lambda s: (prices[s], s))
            ends = [F()]
            for s in order:
                ends.append(ends[-1]+masses[s])
            quantities = set(ends+[sum(ends[k:k+2], F())/2 for k in range(32)])
            for quantity in quantities:
                val, theta = greedy(masses, prices, quantity)
                assert val == dual_value(masses, prices, quantity)
                assert all(0 <= a <= b for a, b in zip(theta, masses)) and sum(theta) == quantity
                sorting_cases += 1
        assert greedy([F()]*32, prices, F())[0] == dual_value([F()]*32, prices, F()) == 0
        sorting_cases += 1
    for t in (0, 1):
        a = [F(1, t+sum(bits(s)[:3])+1) for s in range(32)]
        d = [F(1, t+sum(bits(s)[:3])+2) for s in range(32)]
        masses = [F((s*5+2)%9, 17) for s in range(32)]
        H = sum(masses)
        for iu in range(7):
            for iv in range(iu+1):
                u, v = H*iu/6, H*iv/6
                ca, tu = greedy(masses, a, u)
                cd, tv = greedy(masses, d, v)
                assert all(ivv <= iuu for ivv, iuu in zip(tv, tu))
                # Nested allocation realizes intersection, union-only, neither.
                actual = sum((tv[s]*(a[s]+d[s])+(tu[s]-tv[s])*a[s] for s in range(32)), F())
                assert actual == ca+cd
                nested_cases += 1
        for s in range(32):
            b = t+sum(bits(s)[:3])
            for q, r in product((0, 1), repeat=2):
                literal = F(q+r, b+1)-F(q*r, (b+1)*(b+2))
                assert literal == a[s]*(q+r-q*r)+d[s]*q*r
                bit_cases += 1
    regression = regression_checks(model, hist, own, lookup, saved)
    dominance_cells = obstruction_checks(model, hist, own, lookup)
    report = dict(status='INDEPENDENT_SYMBOLIC_LITERAL_SORTING_AUDIT_PASS',
                  point_sha256=PIN, matrix_sha256=sha(modelpath), verifier_sha256=sha(__file__),
                  all_hist=16, zero_hist=6, root_groups=38, mu_columns=1216,
                  old_prefix_descriptors=15593, semantic_old_columns=4849, old_aux_columns=10744,
                  inherited_rows_verified=5699, inherited_nonzero_coefficients=iaudit['independent_nonzero_coefficients'],
                  new_main_rows=139, all_main_rows=438, new_main_nonzero_coefficients=newcoefs,
                  sorting_piece_rows=piececount, sorting_piece_nonzero_coefficients=piececoefs,
                  named_cross_root_evaluations=pair_literal_count, named_reverse_evaluations=triple_literal_count,
                  S6_checks=8*720, price_templates=len(templates), exact_sorting_truth_cases=sorting_cases,
                  nested_union_intersection_cases=nested_cases, pair_bit_identities=bit_cases,
                  old_seven_bounds=regression, full32_obstruction_dominance_cells=dominance_cells,
                  no_fixed_old_mu_used_for_new_point=True, elapsed_seconds=time.perf_counter()-start)
    (HERE/'symbolic_independent_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False))


def regression_checks(model, hist, own, lookup, saved):
    oldpoint = json.loads((BASE/'union_augmented_lp/augmented_lp_exact.json').read_text())
    old = [F(c['weight']) for c in oldpoint['columns'][:4849]]
    cert = json.loads((BASE/'root_marginal_closure/marginal_completion_exact.json').read_text())
    mu = list(map(F, cert['mu']))
    bounds = json.loads((BASE/'root_network_joint/fixed_mu_upper_bounds_exact.json').read_text())
    assert sha(BASE/'root_marginal_closure/marginal_completion_exact.json') == bounds['mu_sha256']
    cached = {}

    def L(j):
        if j not in cached:
            d = model['lower_columns'][j]
            masses = [mu[s] for s in d['source_mu']]
            prices = list(map(F, d['prices']))
            q = sum((old[k]*F(v) for k, v in d['query_old']), F())
            q += sum((mu[k]*F(v) for k, v in d['query_mu']), F())
            value, _ = greedy(masses, prices, q)
            assert value == dual_value(masses, prices, q)
            cached[j] = value
        return cached[j]

    output, checked = [], 0
    for r in bounds['rows']:
        name = r['name']
        if name[0].startswith('cross-'):
            newname = (name[0]+'-upper', *name[1:])
        else:
            newname = (name[0]+'-upper', name[1][0], tuple(name[1][1]), name[2])
        row = saved[newname]
        value = sum((old[k]*F(v) for k, v in row['old']), F())
        value += sum((mu[k]*F(v) for k, v in row['mu']), F())
        value += sum((L(k)*F(v) for k, v in row['lower']), F())
        assert value == F(r['upper']), (name, value, r['upper'])
        for p in r['pieces']:
            h = p['hist']
            source = p.get('source_old_word', p.get('root_old_word'))
            masses = [mu[lookup[h, source, s]] for s in range(32)]
            t = source >> 2
            if name[0] == 'cross-pair':
                x, y = name[1:]
                donor = p['donor_old_word']
                umass = vmass = F()
                for s in range(32):
                    roles = (donor >> 2,)+bits(s)
                    a, b = roles[x], roles[y]
                    mass = mu[lookup[h, donor, s]]
                    umass += mass*(a+b-a*b)
                    vmass += mass*a*b
                a = [F(1, t+sum(bits(s)[:3])+1) for s in range(32)]
                d = [F(1, t+sum(bits(s)[:3])+2) for s in range(32)]
                wallet = []
                for s in range(32):
                    e = bits(s); b = t+sum(e[:3])
                    wallet.append(F(e[3], b+1+e[4])+F(e[4], b+1+e[3])+F(e[3], (b+1)*(b+2)))
                upper = sum((mass*w for mass, w in zip(masses, wallet)), F())-greedy(masses, a, umass)[0]-greedy(masses, d, vmass)[0]
            else:
                k = name[1] if name[0] == 'cross-floor' else name[2]
                if name[0] == 'cross-floor':
                    donor, l = p['donor_old_word'], name[2]
                    q = sum((mu[lookup[h, donor, s]]*bits(s)[l] for s in range(32)), F())
                else:
                    wb = bits(source, 3)
                    states = own[h, 1, 1, wb, wb]
                    q = old[states[1, 0]]+old[states[1, 1]]
                prices = [F(1, t+sum(bits(s)[:k])+5-k) for s in range(32)]
                income = sum((masses[s]*rational_income(bits(s)[k], t+sum(bits(s))) for s in range(32)), F())
                upper = income-greedy(masses, prices, q)[0]
            assert upper == F(p['upper']), (name, h, source)
            checked += 1
        output.append(dict(name=name, upper=str(value), upper_float=float(value), transport_blocks=len(r['pieces'])))
    assert checked == 293 and len(output) == 7 and sum(F(r['upper']) < 0 for r in output) == 2
    return output


def obstruction_checks(model, hist, own, lookup):
    # Independently reread every stored full32 potential and every dominance cell.
    raw = json.loads((BASE/'root_network_joint/full32_obstruction_rows_exact.json').read_text())
    assert raw['mu_columns'] == model['mu_columns']
    cells = 0
    for row in raw['rows']:
        oldcoef, mucoef = defaultdict(F), defaultdict(F)
        for p in row['pieces']:
            h, factor = p['hist'], F(p['factor'])
            if row['source_query'][0] == 'cross-pair':
                v, w = p['source_old_word'], p['donor_old_word']
                aa, bb = list(map(F, p['alpha'])), list(map(F, p['beta']))
                assert len(aa) == len(bb) == 32
                for s in range(32):
                    e = bits(s); b = (v >> 2)+sum(e[:3])
                    H = F(e[3], b+1+e[4])+F(e[4], b+1+e[3])+F(e[3], (b+1)*(b+2))
                    mucoef[lookup[h, v, s]] += factor*aa[s]
                    mucoef[lookup[h, w, s]] += factor*bb[s]
                    for z in range(32):
                        f = bits(z)
                        cell = H-F(f[3]+f[4], b+1)+F(f[3]*f[4], (b+1)*(b+2))
                        assert aa[s]+bb[z] >= cell
                        cells += 1
            else:
                w = p['root_old_word']
                aa, bb = list(map(F, p['alpha'])), list(map(F, p['beta']))
                oldcoef[h] += factor*bb[0]
                wb = bits(w, 3); ss = own[h, 1, 1, wb, wb]
                assert p['R_old_columns'] == [ss[1, 0], ss[1, 1]]
                for col in p['R_old_columns']:
                    oldcoef[col] += factor*(bb[1]-bb[0])
                for s in range(32):
                    e = bits(s); t = w >> 2
                    mucoef[lookup[h, w, s]] += factor*aa[s]
                    for q in (0, 1):
                        cell = rational_income(e[4], t+sum(e))-F(q, t+sum(e[:4])+1)
                        assert aa[s]+bb[q] >= cell
                        cells += 1
        assert nonzero(oldcoef) == tuple((k, F(v)) for k, v in row['old'])
        assert nonzero(mucoef) == tuple((k, F(v)) for k, v in row['mu'])
    assert cells == raw['total_full_domain_dominance_cells'] == 82304
    return cells


if __name__ == '__main__':
    main()
