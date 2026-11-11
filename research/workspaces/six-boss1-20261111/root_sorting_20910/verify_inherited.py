# Exact copy of the independent upstream auditor, with only input/output
# paths redirected so this execution never writes a frozen upstream file.
"""Independent standard-library literal audit of the complete marginal lift.

No constructor, discovery, recovery, SciPy, NumPy or SymPy is imported.
Every coefficient is rebuilt on all 1216 root columns.  B/C interfaces use
explicit named source/donor sums; R/Z uses every literal triple rather than
the constructor's compressed old-word multiplicities.  Fraction checks
cover all 5699 rows and all 38 equalities, including zero-mass hist records.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import permutations, product
from pathlib import Path
import hashlib
import json
import time

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
PIN = 'b0ca65cfe61e5e3ef09537cba2a986c171aeaa7106f673077f803c80ee2b68e3'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def freeze(v):
    return tuple(map(freeze, v)) if isinstance(v, (list, tuple)) else v


def bits(w, width):
    return tuple(int(c) for c in format(w, f'0{width}b'))


def share(n, denominator):
    return F(n, denominator) if n else F()


def pattern(indices):
    first = {}
    return tuple(first.setdefault(i, len(first)) for i in indices)


def main():
    start = time.perf_counter()
    point_path = BASE/'union_augmented_lp/augmented_lp_exact.json'
    model_path, cert_path = BASE/'root_marginal_closure/symbolic_coefficients_exact.json', BASE/'root_marginal_closure/marginal_completion_exact.json'
    assert sha(point_path) == PIN
    point = json.loads(point_path.read_text())
    model, cert = json.loads(model_path.read_text()), json.loads(cert_path.read_text())
    assert model['point_sha256'] == cert['point_sha256'] == PIN
    assert cert['symbolic_sha256'] == sha(model_path)
    for s in model['sources']:
        assert sha(BASE/s['path']) == s['sha256']
    old = point['columns'][:4849]
    assert old == model['original_columns'] and len(old) == 4849
    weights = list(map(lambda r: F(r['weight']), old))
    hist = {i: c for i, c in enumerate(old) if c['kind'] == 'hist'}
    assert len(hist) == 16 and sum(weights[h] > 0 for h in hist) == 10
    assert all(c['d'] == sum(c['hist'][4:]) == 1 and sum(c['hist']) == 6 for c in hist.values())
    groups = [(h, w) for h, c in hist.items() for w in range(8) if c['hist'][w]]
    expected_mu = [dict(hist=h, old_word=w, state=s) for h, w in groups for s in range(32)]
    assert expected_mu == model['mu_columns'] and len(expected_mu) == 1216 and len(groups) == 38
    lookup = {(r['hist'], r['old_word'], r['state']): j for j, r in enumerate(expected_mu)}
    mu = list(map(F, cert['mu']))
    assert len(mu) == 1216 and min(mu) >= 0 and sum(v > 0 for v in mu) == cert['positive_mu'] == 35
    for h, w in groups:
        assert sum((mu[lookup[h, w, s]] for s in range(32)), F()) == weights[h]
    tables = {}
    for t in (0, 1):
        for r in json.loads((BASE/f'background_five_bridge/fixed53_b{t}_profit.json').read_text())['min_by_actual_and_d']:
            tables[t, int(r['actual'], 2), r['d']] = F(r['min_rho'])
    assert len(tables) == 384
    own, b4 = {}, defaultdict(list)
    current = None
    for j, c in enumerate(old):
        if c['kind'] == 'hist':
            current = j
        if c['kind'] == 'joint-reply':
            f, diag, v, w = c['group']
            own.setdefault((current, f, diag, tuple(v), tuple(w)), {})[tuple(c['state'])] = j
        if c['kind'] == 'actual-B-family-state' and c['source'] == 4:
            b4[c['hist_column']].append((j, tuple(c['hidden'])+(c['ell']//6,)))
    assert len(own) == 194 and len(b4) == 16

    expected = defaultdict(lambda: {key: defaultdict(F) for key in ('old', 'mu', 'aux')})

    def add(name, kind, column, coefficient):
        expected[freeze(name)][kind][column] += coefficient

    # One marked root at each named position whose old word is w.
    # Literal B/C sources are all six named indices; same/off use 6/30.
    literal_interfaces = 0
    for column, m in enumerate(expected_mu):
        h, word, s = m['hist'], m['old_word'], m['state']
        c = hist[h]
        a, e = tuple(map(int, c['actual_bits'])), bits(s, 5)
        words = [w for w in range(8) for _ in range(c['hist'][w])]
        oldbits = list(map(lambda w: bits(w, 3), words))
        t = word >> 2
        total, pref = t+sum(e), t+sum(e[:3])
        n = F(c['hist'][word], 6)
        add(('gamma',), 'mu', column, n*(2*share(sum(e), total)-tables[t, s, 1-t]))
        add(('root-source',), 'mu', column, -n*share(t, total))
        for k in range(5):
            real_income, safe = share(e[k], total), t+sum(e[:k])+5-k
            add(('price', k), 'mu', column, -n*F(e[k], sum(a[:5])+1))
            add(('capacity', k), 'mu', column, -n*e[k])
            for i in range(6):
                add(('floor-actual', k, i), 'mu', column, n*(real_income-F(a[i], safe)))
            add(('floor-other-opt', k), 'mu', column, n*(5*real_income-F(1-t, safe)))
            add(('floor-root', k), 'mu', column, n*(real_income-F(t, safe)))
            for l in range(5):
                if l != k:
                    add(('floor-own-tail', k, l), 'mu', column, n*(real_income-F(e[l], safe)))
            for i in range(5):
                add(('actual-floor', i, k), 'mu', column, -n*F(e[k], sum(a[:i])+6-i))
        rootbits, apref = (t,)+e, sum(a[:4])
        for x in range(6):
            for y in range(x, 6):
                query = F(rootbits[x]+rootbits[y], apref+1)-F(rootbits[x]*rootbits[y], (apref+1)*(apref+2))
                add(('actual-pair', x, y), 'mu', column, -n*query)
        for root_index in range(6):
            if words[root_index] != word:
                continue
            for old_index in range(6):
                ot, ob, oc = oldbits[old_index]
                p = sum(a[:3])+ot
                same = old_index == root_index
                rel, normalizer = ('same', 6) if same else ('off', 30)
                for k in range(5):
                    add(('C-to-Y', k, rel), 'mu', column, F(oc-e[k], normalizer*(p+ob+1)))
                    add(('B-to-Y', k, rel), 'mu', column,
                        (F(ob, p+1+oc)-F(e[k], p+2))/normalizer)
                for tag, member in (('C', oc), ('B', ob)):
                    add(('Y5-to-'+tag, rel), 'mu', column,
                        (share(e[4], total)-F(member, t+sum(e[:4])+1))/normalizer)
                for k in range(4):
                    for tag, member in (('B', ob), ('C', oc)):
                        add(('Y-to-old', k, tag, rel), 'mu', column,
                            (share(e[k], total)-F(member, t+sum(e[:k])+5-k))/normalizer)
                oldpay = F(ob, p+1+oc)+F(oc, p+1+ob)
                oldtax = F(ob, (p+1)*(p+2))
                newpay = F(e[3], pref+1+e[4])+F(e[4], pref+1+e[3])
                newtax = F(e[3], (pref+1)*(pref+2))
                for l in range(5):
                    for k in range(l, 5):
                        query = F(e[l]+e[k], p+1)-F(e[l]*e[k], (p+1)*(p+2))
                        add(('old-pair-to-Y', l, k, rel), 'mu', column, (oldpay+oldtax-query)/normalizer)
                for vn, wn, v, w in (('B', 'B', ob, ob), ('B', 'C', ob, oc), ('C', 'C', oc, oc)):
                    query = F(v+w, pref+1)-F(v*w, (pref+1)*(pref+2))
                    add(('new-pair-to-old', vn, wn, rel), 'mu', column, (newpay+newtax-query)/normalizer)
                literal_interfaces += 38
    add(('gamma',), 'old', 0, -F(226487, 10**21))
    for h, c in hist.items():
        a = tuple(map(int, c['actual_bits']))
        add(('gamma',), 'old', h, -F(5, 6))
        add(('root-source',), 'old', h, share(a[0], sum(a)))
        for k in range(5):
            add(('price', k), 'old', h, share(a[5], sum(a)))
            for i in range(5):
                add(('actual-floor', i, k), 'old', h, share(a[i], sum(a)))
        p = sum(a[:4])
        wallet = F(a[4], p+1+a[5])+F(a[5], p+1+a[4])+F(a[4], (p+1)*(p+2))
        for x in range(6):
            for y in range(x, 6):
                add(('actual-pair', x, y), 'old', h, wallet)
    for k in range(5):
        add(('capacity', k), 'old', 0, F(1))
    assert len(expected) == 194

    # Independent explicit simultaneous-S6 orbit and denominator audit.
    orbits = defaultdict(list)
    for f, i, j, k in product(range(2), range(6), range(6), range(6)):
        if f == 0 and j == k:
            continue
        orbits[f, pattern((i, j, k))].append((i, j, k))
    assert len(orbits) == 8 and sum(map(len, orbits.values())) == 396
    perms = tuple(permutations(range(6)))
    for (f, pat), triples in orbits.items():
        i, j, k = triples[0]
        counts = Counter((p[i], p[j], p[k]) for p in perms)
        assert set(counts) == set(triples) and set(counts.values()) == {720//len(triples)}
    auxiliaries = {freeze(r['key']): j for j, r in enumerate(model['aux_columns'])}
    assert len(auxiliaries) == model['aux_column_count'] == 2700
    aux_caps = {}
    literal_new = 0
    for h, c in hist.items():
        a = tuple(map(int, c['actual_bits']))
        words = [w for w in range(8) for _ in range(c['hist'][w])]
        oldbits = list(map(lambda w: bits(w, 3), words))
        P = sum(a[:4])
        for (f, pat), triples in orbits.items():
            normalizer = len(triples)
            for i, j, k in triples:
                v, w = oldbits[j], oldbits[k]
                states = own[h, f, int(j == k), v, w]
                rcols = (states[1, 0], states[1, 1])
                den = sum(a[:3])+v[0]+w[1+f]+1
                for l in range(5):
                    rn, zn = ('R-to-Y', f, pat, l), ('Z-to-Y-upper', f, pat, l)
                    for rc in rcols:
                        add(rn, 'old', rc, F(1, normalizer*den))
                    add(zn, 'old', states[0, 1], F(1, normalizer*(P+1)))
                    add(zn, 'old', states[1, 1], F(1, normalizer*(P+2)))
                    ai = auxiliaries['Z', h, words[i], l, f, int(j == k), v, w]
                    add(zn, 'aux', ai, F(1, normalizer*(P+1)*(P+2)))
                    aux_caps[ai] = {rc: F(1) for rc in rcols}
                    for s in range(32):
                        member = bits(s, 5)[l]
                        col = lookup[h, words[i], s]
                        add(rn, 'mu', col, -F(member, normalizer*den))
                        add(zn, 'mu', col, -F(member, normalizer*(P+1)))
                    literal_new += 2
        base = sum(a[:3])+a[5]
        for l in range(5):
            fn, hn = ('F-to-Y-upper', l), ('H1-safe-to-Y', l)
            for j, hidden in b4[h]:
                h1, h2 = hidden[:2]
                add(fn, 'old', j, F(h2, base+h1+1))
                add(hn, 'old', j, F(h1, base+h2+1))
            for i in range(6):
                ai = auxiliaries['F', h, words[i], l]
                aux_caps[ai] = {j: F(s[0]) for j, s in b4[h] if s[0]}
                add(fn, 'aux', ai, F(1, 6*(base+1)*(base+2)))
                for s in range(32):
                    col, member = lookup[h, words[i], s], bits(s, 5)[l]
                    add(fn, 'mu', col, -F(member, 6*(base+1)))
                    add(hn, 'mu', col, -F(member, 6*(base+2)))
        for l in range(5):
            for k in range(l, 5):
                pn = ('B4-pair-to-Y', l, k)
                for j, hidden in b4[h]:
                    h1, h2 = hidden[:2]
                    add(pn, 'old', j, F(h1, base+1+h2)+F(h2, base+1+h1)+F(h1, (base+1)*(base+2)))
                for i in range(6):
                    for s in range(32):
                        e = bits(s, 5)
                        query = F(e[l]+e[k], base+1)-F(e[l]*e[k], (base+1)*(base+2))
                        add(pn, 'mu', lookup[h, words[i], s], -query/6)
    assert len(expected) == 299 and len(aux_caps) == 2700
    canonical = []
    for j, r in enumerate(model['aux_columns']):
        actual_cap = {k: F(v) for k, v in r['old_cap']}
        assert actual_cap == aux_caps[j]
        capvalue = sum((weights[k]*v for k, v in actual_cap.items()), F())
        rootcols = [lookup[r['hist'], r['old_word'], s] for s in range(32) if bits(s, 5)[r['tail']]]
        y = sum((mu[k] for k in rootcols), F())
        canonical.append(min(capvalue, y))
        for col, coef in aux_caps[j].items():
            add(('min-cap-old', j), 'old', col, coef)
        add(('min-cap-old', j), 'aux', j, F(-1))
        for col in rootcols:
            add(('min-cap-root', j), 'mu', col, F(1))
        add(('min-cap-root', j), 'aux', j, F(-1))
    assert canonical == list(map(F, cert['canonical_min'])) and min(canonical) >= 0
    assert len(expected) == 5699
    saved = {freeze(r['name']): r for r in model['rows']}
    assert len(saved) == len(model['rows']) == len(expected) and set(saved) == set(expected)
    coeff_count = 0
    values = {}
    for name, parts in expected.items():
        value = F()
        for kind, vector in (('old', weights), ('mu', mu), ('aux', canonical)):
            direct = {k: v for k, v in parts[kind].items() if v}
            stored = {k: F(v) for k, v in saved[name][kind]}
            assert stored == direct, (name, kind)
            coeff_count += len(direct)
            value += sum((vector[k]*v for k, v in direct.items()), F())
        assert value >= 0, (name, value)
        values[name] = value
    certvals = {freeze(r['row']): F(r['slack']) for r in cert['all_slacks']}
    assert values == certvals and len(certvals) == 5699
    assert values['root-source',] == F(cert['root_source_slack'])
    for r in model['equalities']:
        kind, h, word = r['name']
        assert kind == 'mass'
        assert r['old'] == [[h, '-1']] and r['aux'] == []
        assert r['mu'] == [[lookup[h, word, s], '1'] for s in range(32)]

    # Regression: the old 17-atom marginal has exactly Main's 45 bounds.
    old_cert = json.loads((BASE/'root_pair_joint_19662/joint_completion_exact.json').read_text())
    old_mu = [F() for _ in mu]
    for atom in old_cert['atoms']:
        h = atom['hist']
        mass = F(atom['mass'])
        for w, s in zip(atom['old_words'], atom['new_words']):
            old_mu[lookup[h, w, s]] += mass/hist[h]['hist'][w]
    old_min = []
    for j, r in enumerate(model['aux_columns']):
        cap = sum((weights[k]*v for k, v in aux_caps[j].items()), F())
        y = sum((old_mu[lookup[r['hist'], r['old_word'], s]] for s in range(32) if bits(s, 5)[r['tail']]), F())
        old_min.append(min(cap, y))
    main_bounds = {freeze(r['query']): F(r['upper']) for r in json.loads((BASE/'main_glued_single_query_upper.json').read_text())['rows']}
    old_upper = {}
    for name in expected:
        if name[0] not in ('Z-to-Y-upper', 'F-to-Y-upper'):
            continue
        original_name = (name[0].replace('-upper', ''),)+name[1:]
        value = F()
        for kind, vector in (('old', weights), ('mu', old_mu), ('aux', old_min)):
            value += sum((vector[k]*v for k, v in expected[name][kind].items()), F())
        assert value == main_bounds[original_name]
        old_upper[original_name] = value
    assert len(old_upper) == 45 and sum(v < 0 for v in old_upper.values()) == 8
    summary = defaultdict(list)
    for name, value in values.items():
        if name[0].startswith('min-cap-'):
            continue
        summary[name[0]].append(value)
    report = dict(scope='Independent complete symbolic coefficient and rational witness audit; single-root marginal/envelope relaxation only.',
                  point_sha256=PIN, symbolic_sha256=sha(model_path), certificate_sha256=sha(cert_path),
                  verifier_sha256=sha(__file__), all_16_hist_retained=True, hist_zero=6,
                  complete_groups=38, complete_mu_columns=1216, positive_mu=35,
                  full_state_zero_included=True, principal_rows=299, cap_rows=5400, total_rows=5699,
                  mass_equalities=38, independent_nonzero_coefficients=coeff_count,
                  old_interface_literal_evaluations=literal_interfaces,
                  rz_literal_evaluations=literal_new, simultaneous_S6_permutation_checks=8*720,
                  canonical_min_auxiliaries=2700, old_marginal_bounds_reproduced=45,
                  old_marginal_bounds_negative=8, new_bounds_negative=0,
                  root_source_slack=str(values['root-source',]),
                  principal_zero=sum(v == 0 for vv in summary.values() for v in vv),
                  family_summary=[dict(family=k, count=len(v), minimum=str(min(v)), minimum_float=float(min(v)),
                                       zero=sum(x == 0 for x in v)) for k, v in summary.items()],
                  elapsed_seconds=time.perf_counter()-start,
                  status='INDEPENDENT FULL-STATE MARGINAL AND CANONICAL-MIN AUDIT PASSED')
    (HERE/'inherited_independent_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
