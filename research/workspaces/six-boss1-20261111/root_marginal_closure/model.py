"""Complete single-root marginal lift; no finite root-incidence restriction.

For each of all 16 fixed hist records and every occupied OLD word, every
five-tail binary state is present, including 00000.  Equal old words share
one marginal, never one named root label.  Symbolic coefficients retain the
first 4849 original columns, even though discovery fixes their exact value.

Rows are positive slack.  Min auxiliaries are upper-envelope devices and
are not asserted to be simultaneous realizable intersections.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import combinations_with_replacement, product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
POINT = BASE/'union_augmented_lp/augmented_lp_exact.json'
PIN = 'b0ca65cfe61e5e3ef09537cba2a986c171aeaa7106f673077f803c80ee2b68e3'
KAPPA = F(226487, 10**21)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def bits(w, n):
    return tuple((w >> (n-1-k)) & 1 for k in range(n))


def q(n, d):
    return F(n, d) if n else F()


def canon(seq):
    names = {}
    return tuple(names.setdefault(i, len(names)) for i in seq)


def clean(x):
    return {k: v for k, v in x.items() if v}


def write_json(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')


class Row:
    def __init__(self, name, category='principal'):
        self.name = tuple(name)
        self.category = category
        self.old = defaultdict(F)
        self.mu = defaultdict(F)
        self.aux = defaultdict(F)

    def output(self):
        return dict(name=self.name, category=self.category,
                    old=[[k, str(v)] for k, v in sorted(clean(self.old).items())],
                    mu=[[k, str(v)] for k, v in sorted(clean(self.mu).items())],
                    aux=[[k, str(v)] for k, v in sorted(clean(self.aux).items())])


def inputs():
    assert sha(POINT) == PIN
    point = json.loads(POINT.read_text())
    old = point['columns'][:4849]
    hist = {j: c for j, c in enumerate(old) if c['kind'] == 'hist'}
    assert len(hist) == 16
    assert all(sum(c['hist']) == 6 and sum(c['hist'][4:]) == c['d'] == 1 for c in hist.values())
    own, b4 = {}, defaultdict(list)
    for j, c in enumerate(old):
        if c['kind'] == 'hist':
            h = j
        elif c['kind'] == 'joint-reply':
            f, d, wi, wj = c['group']
            key = (h, f, d, tuple(wi), tuple(wj))
            own.setdefault(key, {})[tuple(c['state'])] = j
        elif c['kind'] == 'actual-B-family-state' and c['source'] == 4:
            b4[c['hist_column']].append((j, tuple(c['hidden'])+(c['ell']//6,)))
    assert len(own) == 194 and all(set(v) == {(0, 1), (1, 0), (1, 1)} for v in own.values())
    assert len(b4) == 16 and all(len(v) == 8 for v in b4.values())
    table = {}
    for t in (0, 1):
        source = BASE/f'background_five_bridge/fixed53_b{t}_profit.json'
        for r in json.loads(source.read_text())['min_by_actual_and_d']:
            table[t, int(r['actual'], 2), r['d']] = F(r['min_rho'])
    assert len(table) == 384
    return point, old, hist, own, b4, table


def build():
    point, old, hist, own, b4, table = inputs()
    groups = [(h, w) for h, c in hist.items() for w, n in enumerate(c['hist']) if n]
    mu = [dict(hist=h, old_word=w, state=s) for h, w in groups for s in range(32)]
    assert len(groups) == 38 and len(mu) == 1216
    index = {(r['hist'], r['old_word'], r['state']): j for j, r in enumerate(mu)}
    rows, rowmap, aux, auxmap = [], {}, [], {}

    def row(name):
        name = tuple(name)
        if name not in rowmap:
            rowmap[name] = Row(name)
            rows.append(rowmap[name])
        return rowmap[name]

    def minimum(key, h, w, k, cap):
        key = tuple(key)
        if key not in auxmap:
            j = len(aux)
            auxmap[key] = j
            aux.append(dict(key=key, hist=h, old_word=w, tail=k,
                            old_cap=[[c, str(v)] for c, v in sorted(cap.items()) if v]))
        return auxmap[key]

    # All 117 old root budgets whose literal coefficient uses one root state.
    for j, m in enumerate(mu):
        h, w, state = m['hist'], m['old_word'], m['state']
        c = hist[h]
        a, e, (t, b, z) = tuple(map(int, c['actual_bits'])), bits(state, 5), bits(w, 3)
        n = F(c['hist'][w], 6)
        total, d = t+sum(e), c['d']
        row(('gamma',)).mu[j] += n*(2*q(sum(e), total)-table[t, state, d-t])
        row(('root-source',)).mu[j] -= n*q(t, total)
        for k in range(5):
            income, den = q(e[k], total), t+sum(e[:k])+5-k
            row(('price', k)).mu[j] -= n*F(e[k], sum(a[:5])+1)
            row(('capacity', k)).mu[j] -= n*e[k]
            for i in range(6):
                row(('floor-actual', k, i)).mu[j] += n*(income-F(a[i], den))
            row(('floor-other-opt', k)).mu[j] += n*(5*income-F(d-t, den))
            row(('floor-root', k)).mu[j] += n*(income-F(t, den))
            for l in range(5):
                if l != k:
                    row(('floor-own-tail', k, l)).mu[j] += n*(income-F(e[l], den))
            for i in range(5):
                row(('actual-floor', i, k)).mu[j] -= n*F(e[k], sum(a[:i])+6-i)
        ownbits, pref = (t,)+e, sum(a[:4])
        for x, y in combinations_with_replacement(range(6), 2):
            row(('actual-pair', x, y)).mu[j] -= n*(F(ownbits[x]+ownbits[y], pref+1)
                -F(ownbits[x]*ownbits[y], (pref+1)*(pref+2)))
    assert len(rows) == 118
    row(('gamma',)).old[0] -= KAPPA
    for h, c in hist.items():
        a = tuple(map(int, c['actual_bits']))
        pay = [q(v, sum(a)) for v in a]
        row(('gamma',)).old[h] -= F(5, 6)  # Only this fixed d=1 support.
        row(('root-source',)).old[h] += pay[0]
        for k in range(5):
            row(('price', k)).old[h] += pay[5]
            for i in range(5):
                row(('actual-floor', i, k)).old[h] += pay[i]
        ap = sum(a[:4])
        wallet = F(a[4], ap+1+a[5])+F(a[5], ap+1+a[4])+F(a[4], (ap+1)*(ap+2))
        for x, y in combinations_with_replacement(range(6), 2):
            row(('actual-pair', x, y)).old[h] += wallet
    for k in range(5):
        row(('capacity', k)).old[0] += 1

    # The 40 old-B/C single queries and 36 true same-donor PAIR queries.
    for j, m in enumerate(mu):
        h, w, state = m['hist'], m['old_word'], m['state']
        c = hist[h]
        a, e, t = tuple(map(int, c['actual_bits'])), bits(state, 5), w >> 2
        total, pref = t+sum(e), t+sum(e[:3])
        newwallet = F(e[3], pref+1+e[4])+F(e[4], pref+1+e[3])+F(e[3], (pref+1)*(pref+2))
        for v, count in enumerate(c['hist']):
            if not count:
                continue
            ot, ob, oc = bits(v, 3)
            p = sum(a[:3])+ot
            oldwallet = F(ob, p+1+oc)+F(oc, p+1+ob)+F(ob, (p+1)*(p+2))
            for rel in ('same', 'off'):
                mult = F(c['hist'][w], 6)*(int(v == w) if rel == 'same' else F(count-int(v == w), 5))
                if not mult:
                    continue
                for k in range(5):
                    row(('C-to-Y', k, rel)).mu[j] += mult*F(oc-e[k], p+ob+1)
                    row(('B-to-Y', k, rel)).mu[j] += mult*(F(ob, p+1+oc)-F(e[k], p+2))
                row(('Y5-to-C', rel)).mu[j] += mult*(q(e[4], total)-F(oc, t+sum(e[:4])+1))
                row(('Y5-to-B', rel)).mu[j] += mult*(q(e[4], total)-F(ob, t+sum(e[:4])+1))
                for k in range(4):
                    den = t+sum(e[:k])+5-k
                    for name, member in (('B', ob), ('C', oc)):
                        row(('Y-to-old', k, name, rel)).mu[j] += mult*(q(e[k], total)-F(member, den))
                for l, k in combinations_with_replacement(range(5), 2):
                    row(('old-pair-to-Y', l, k, rel)).mu[j] += mult*(oldwallet
                        -F(e[l]+e[k], p+1)+F(e[l]*e[k], (p+1)*(p+2)))
                for vname, wname, vb, wb in (('B', 'B', ob, ob), ('B', 'C', ob, oc), ('C', 'C', oc, oc)):
                    row(('new-pair-to-old', vname, wname, rel)).mu[j] += mult*(newwallet
                        -F(vb+wb, pref+1)+F(vb*wb, (pref+1)*(pref+2)))
    assert len(rows) == 194

    # Full simultaneous-S6 triple orbits; all 396 named root/node queries.
    nodes = [(f, j, k) for f, j, k in product(range(2), range(6), range(6)) if f or j != k]
    orbits = defaultdict(list)
    for i in range(6):
        for f, j, k in nodes:
            orbits[f, canon((i, j, k))].append((i, j, k))
    assert len(orbits) == 8 and sum(map(len, orbits.values())) == 396
    for h, c in hist.items():
        words = [w for w, n in enumerate(c['hist']) for _ in range(n)]
        wb = list(map(lambda w: bits(w, 3), words))
        a = tuple(map(int, c['actual_bits']))
        p3, P = sum(a[:3]), sum(a[:4])
        for (f, pattern), triples in orbits.items():
            counts = Counter((words[i], int(j == k), wb[j], wb[k]) for i, j, k in triples)
            for (w, diag, v, z), count in counts.items():
                fac = F(count, len(triples))
                ss = own[h, f, diag, v, z]
                cap = {ss[1, 0]: F(1), ss[1, 1]: F(1)}
                den = p3+v[0]+z[1+f]+1
                for l in range(5):
                    rn = row(('R-to-Y', f, pattern, l))
                    zn = row(('Z-to-Y-upper', f, pattern, l))
                    for k0 in cap:
                        rn.old[k0] += fac/F(den)
                    zn.old[ss[0, 1]] += fac/F(P+1)
                    zn.old[ss[1, 1]] += fac/F(P+2)
                    ai = minimum(('Z', h, w, l, f, diag, v, z), h, w, l, cap)
                    zn.aux[ai] += fac/F((P+1)*(P+2))
                    for state in range(32):
                        member = bits(state, 5)[l]
                        j0 = index[h, w, state]
                        rn.mu[j0] -= fac*F(member, den)
                        zn.mu[j0] -= fac*F(member, P+1)
        base = p3+a[5]
        cap = {j: F(s[0]) for j, s in b4[h] if s[0]}
        for l in range(5):
            fn = row(('F-to-Y-upper', l))
            hn = row(('H1-safe-to-Y', l))
            for j, s in b4[h]:
                fn.old[j] += F(s[1], base+s[0]+1)
                hn.old[j] += F(s[0], base+s[1]+1)
            for w, count in enumerate(c['hist']):
                if not count:
                    continue
                fac = F(count, 6)
                ai = minimum(('F', h, w, l), h, w, l, cap)
                fn.aux[ai] += fac/F((base+1)*(base+2))
                for state in range(32):
                    member = bits(state, 5)[l]
                    j0 = index[h, w, state]
                    fn.mu[j0] -= fac*F(member, base+1)
                    hn.mu[j0] -= fac*F(member, base+2)
        # Exactly representable B4 true final PAIR -> same-root two tails.
        for l, k in combinations_with_replacement(range(5), 2):
            pn = row(('B4-pair-to-Y', l, k))
            for j, s in b4[h]:
                pn.old[j] += F(s[0], base+1+s[1])+F(s[1], base+1+s[0])+F(s[0], (base+1)*(base+2))
            for w, count in enumerate(c['hist']):
                if not count:
                    continue
                for state in range(32):
                    e, fac = bits(state, 5), F(count, 6)
                    pn.mu[index[h, w, state]] -= fac*(F(e[l]+e[k], base+1)
                        -F(e[l]*e[k], (base+1)*(base+2)))
    assert len(rows) == 299
    main_count = len(rows)
    for j, m in enumerate(aux):
        cap = Row(('min-cap-old', j), 'auxiliary-cap')
        cap.old.update({k: F(v) for k, v in m['old_cap']})
        cap.aux[j] = F(-1)
        y = Row(('min-cap-root', j), 'auxiliary-cap')
        for state in range(32):
            y.mu[index[m['hist'], m['old_word'], state]] = F(bits(state, 5)[m['tail']])
        y.aux[j] = F(-1)
        rows.extend((cap, y))
    equality = []
    for h, w in groups:
        r = Row(('mass', h, w), 'equality')
        r.old[h] = F(-1)
        for state in range(32):
            r.mu[index[h, w, state]] = F(1)
        equality.append(r)
    return dict(point=point, old=old, hist=hist, own=own, b4=b4, table=table,
                groups=groups, mu=mu, aux=aux, rows=rows, eq=equality, principal=main_count,
                orbits=orbits)


def export(model):
    out = dict(scope='Homogeneous symbolic complete 32-state single-root lift on all 16 fixed original hist identities; not the complete old 239-family cone.',
               point_sha256=PIN, old_column_count=4849, mu_column_count=len(model['mu']),
               aux_column_count=len(model['aux']), principal_row_count=model['principal'],
               equality_count=len(model['eq']), nonnegative_variables=['all mu', 'all min auxiliaries'],
               root_groups=[dict(hist=h, old_word=w) for h, w in model['groups']],
               mu_columns=model['mu'], aux_columns=model['aux'],
               rows=[r.output() for r in model['rows']], equalities=[r.output() for r in model['eq']],
               original_columns=model['old'],
               gamma_support='All 16 retained hist have d=1; the 5/6 coefficient is this support identity, not a general O6 theorem.',
               omitted=['25 cross-root-floor', '21 cross-root-pair', 'Y-to-R/Z sorting envelopes',
                        'Y-to-H1/H2 sorting envelopes', 'Y-pair-to-B4 joint-state envelopes',
                        'common realizability of min overlaps', 'same ordered-history strategy consistency'],
               sources=[dict(path=str(p.relative_to(BASE)), sha256=sha(p)) for p in [POINT,
                   BASE/'root_pair_joint_19662/verify_completion.py', BASE/'background_five_bridge.md',
                   BASE/'background_five_bridge/fixed53_b0_profit.json',
                   BASE/'background_five_bridge/fixed53_b1_profit.json',
                   BASE/'main_glued_terminal_interfaces.md', BASE/'main_glued_single_query_upper.py',
                   BASE/'main_glued_single_query_upper.json']], script_sha256=sha(__file__))
    write_json(HERE/'symbolic_coefficients_exact.json', out)
    return out


if __name__ == '__main__':
    model = build()
    export(model)
    print(json.dumps(dict(mu=len(model['mu']), groups=len(model['groups']), aux=len(model['aux']),
                          principal=model['principal'], all_rows=len(model['rows']), equality=len(model['eq']))))
