"""RS1--3 lift on every retained hist and every 32-state root marginal.

All coefficients are homogeneous and exact.  Old coordinates stay symbolic.
The phase-I point is deliberately NOT consulted while building coefficients.
Only identical (source group, price vector, symbolic query) blocks are shared.
This is a necessary, separately optimized block envelope, not a joint law.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import combinations_with_replacement, product
from pathlib import Path
import gzip
import hashlib
import json
import time

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
POINT = BASE/'full624_augmented_lp/recovery/augmented_lp_exact.json'
PIN = 'cb45ee6f8df153764c91bd77d0543527cc44719ff7cc43646ffce06a7921a932'
OLDPOINT = BASE/'union_augmented_lp/augmented_lp_exact.json'
OLDPIN = 'b0ca65cfe61e5e3ef09537cba2a986c171aeaa7106f673077f803c80ee2b68e3'
UPSTREAM = BASE/'root_marginal_closure/symbolic_coefficients_exact.json'
UPIN = '2565aeea4db47b6b12bd608290b226f7b165af2d061f0f4e62db5ce033fd1a60'
KINDS = ('old', 'mu', 'aux', 'lower')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, obj):
    data = (json.dumps(obj, ensure_ascii=False, separators=(',', ':'))+'\n').encode()
    if str(path).endswith('.gz'):
        with open(path, 'wb') as f:
            with gzip.GzipFile(fileobj=f, mode='wb', mtime=0) as g:
                g.write(data)
    else:
        Path(path).write_bytes(data)


def bits(s, n=5):
    return tuple((s >> (n-k-1)) & 1 for k in range(n))


def freeze(x):
    return tuple(map(freeze, x)) if isinstance(x, (list, tuple)) else x


def pattern(indices):
    names = {}
    return tuple(names.setdefault(i, len(names)) for i in indices)


def share(n, d):
    return F(n, d) if n else F()


def clean(d):
    return tuple((k, v) for k, v in sorted(d.items()) if v)


def descriptor(c):
    return {k: v for k, v in c.items() if k != 'weight'}


class Row:
    def __init__(self, name, category='principal'):
        self.name, self.category = tuple(name), category
        self.parts = {k: defaultdict(F) for k in KINDS}

    def output(self):
        return dict(name=self.name, category=self.category,
                    **{k: [[j, str(v)] for j, v in clean(a)] for k, a in self.parts.items()})


def build():
    start = time.perf_counter()
    assert sha(POINT) == PIN and sha(OLDPOINT) == OLDPIN and sha(UPSTREAM) == UPIN
    point, previous, oldmodel = [json.loads(p.read_text()) for p in (POINT, OLDPOINT, UPSTREAM)]
    allcols = point['columns']
    assert len(allcols) == 20585 and len(previous['columns']) == 15593
    assert [descriptor(c) for c in allcols[:15593]] == [descriptor(c) for c in previous['columns']]
    old = [descriptor(c) for c in allcols[:4849]]
    assert old == [descriptor(c) for c in oldmodel['original_columns']]
    hist = {h: c for h, c in enumerate(old) if c['kind'] == 'hist'}
    groups = [(h, w) for h, c in hist.items() for w, n in enumerate(c['hist']) if n]
    assert len(hist) == 16 and len(groups) == 38
    assert all(c['d'] == sum(c['hist'][4:]) == 1 and sum(c['hist']) == 6 for c in hist.values())
    mu = [dict(hist=h, old_word=w, state=s) for h, w in groups for s in range(32)]
    assert mu == oldmodel['mu_columns'] and len(mu) == 1216
    lookup = {(r['hist'], r['old_word'], r['state']): j for j, r in enumerate(mu)}
    own, b4 = {}, defaultdict(list)
    for j, c in enumerate(old):
        if c['kind'] == 'hist':
            h = j
        elif c['kind'] == 'joint-reply':
            f, diag, v, w = c['group']
            own.setdefault((h, f, diag, tuple(v), tuple(w)), {})[tuple(c['state'])] = j
        elif c['kind'] == 'actual-B-family-state' and c['source'] == 4:
            b4[c['hist_column']].append((j, tuple(c['hidden'])+(c['ell']//6,)))
    assert len(own) == 194 and all(len(x) == 3 for x in own.values())
    assert len(b4) == 16 and all(len(x) == 8 for x in b4.values())
    principal, rowmap, lower, lowermap = [], {}, [], {}
    blocks = []

    def row(name):
        key = freeze(name)
        if key not in rowmap:
            rowmap[key] = Row(name)
            principal.append(rowmap[key])
        return rowmap[key]

    def lower_bound(h, w, prices, query_old=None, query_mu=None):
        qo, qm = clean(query_old or {}), clean(query_mu or {})
        key = (h, w, tuple(prices), qo, qm)
        if key not in lowermap:
            j = len(lower)
            lowermap[key] = j
            lower.append(dict(hist=h, old_word=w, prices=list(map(str, prices)),
                              source_mu=[lookup[h, w, s] for s in range(32)],
                              query_old=[[k, str(v)] for k, v in qo],
                              query_mu=[[k, str(v)] for k, v in qm],
                              lambdas=list(map(str, sorted(set(prices))))))
        return lowermap[key]

    def source_income(r, h, w, factor, tail=None):
        t = w >> 2
        for s in range(32):
            e = bits(s)
            if tail is None:
                b = t+sum(e[:3])
                val = F(e[3], b+1+e[4])+F(e[4], b+1+e[3])+F(e[3], (b+1)*(b+2))
            else:
                val = share(e[tail], t+sum(e))
            r.parts['mu'][lookup[h, w, s]] += factor*val

    def safe_prices(w, k):
        return [F(1, (w >> 2)+sum(bits(s)[:k])+5-k) for s in range(32)]

    def pair_prices(w, delta):
        return [F(1, (w >> 2)+sum(bits(s)[:3])+delta) for s in range(32)]

    for h, c in hist.items():
        for v, nv in enumerate(c['hist']):
            if not nv:
                continue
            for w, nw in enumerate(c['hist']):
                count = nv*(nw-int(v == w))
                if not count:
                    continue
                for k, l in product(range(5), repeat=2):
                    r = row(('cross-floor-upper', k, l))
                    fac = F(count, 6)
                    source_income(r, h, v, fac, k)
                    query = {lookup[h, w, s]: F(bits(s)[l]) for s in range(32)}
                    li = lower_bound(h, v, safe_prices(v, k), query_mu=query)
                    r.parts['lower'][li] -= fac
                    blocks.append(dict(row=r.name, hist=h, source=v, donor=w, factor=str(fac),
                                       lower=[li], roles=[l], kind='root-single'))
                for x, y in combinations_with_replacement(range(6), 2):
                    r = row(('cross-pair-upper', x, y))
                    fac = F(count, 30)
                    source_income(r, h, v, fac)
                    unions, intersections = {}, {}
                    for s in range(32):
                        donor = (w >> 2,)+bits(s)
                        a, b = donor[x], donor[y]
                        unions[lookup[h, w, s]] = F(a | b)
                        intersections[lookup[h, w, s]] = F(a & b)
                    ls = [lower_bound(h, v, pair_prices(v, 1), query_mu=unions),
                          lower_bound(h, v, pair_prices(v, 2), query_mu=intersections)]
                    for li in ls:
                        r.parts['lower'][li] -= fac
                    blocks.append(dict(row=r.name, hist=h, source=v, donor=w, factor=str(fac),
                                       lower=ls, roles=[x, y], kind='root-pair'))
    assert len(principal) == 46
    orbits = defaultdict(list)
    for f, i, j, k in product(range(2), range(6), range(6), range(6)):
        if f or j != k:
            orbits[f, pattern((i, j, k))].append((i, j, k))
    assert len(orbits) == 8 and sum(map(len, orbits.values())) == 396
    for h, c in hist.items():
        words = [w for w, n in enumerate(c['hist']) for _ in range(n)]
        wb = [bits(w, 3) for w in words]
        for (f, pat), triples in orbits.items():
            counts = Counter((words[i], int(j == k), wb[j], wb[k]) for i, j, k in triples)
            for (w, diag, v, z), count in counts.items():
                states = own[h, f, diag, v, z]
                fac = F(count, len(triples))
                for member in (0, 1):
                    tag = ('R', 'Z')[member]
                    query = {j: F(s[member]) for s, j in states.items()}
                    for k in range(5):
                        r = row(('Y-to-'+tag+'-upper', f, pat, k))
                        source_income(r, h, w, fac, k)
                        li = lower_bound(h, w, safe_prices(w, k), query_old=query)
                        r.parts['lower'][li] -= fac
                        blocks.append(dict(row=r.name, hist=h, source=w, factor=str(fac),
                                           lower=[li], own=[f, diag, v, z], member=member,
                                           kind='old-single'))
        for w, count in enumerate(c['hist']):
            if not count:
                continue
            fac = F(count, 6)
            for member in (0, 1):
                query = {j: F(s[member]) for j, s in b4[h]}
                for k in range(5):
                    r = row(('Y-to-H'+str(member+1)+'-upper', k))
                    source_income(r, h, w, fac, k)
                    li = lower_bound(h, w, safe_prices(w, k), query_old=query)
                    r.parts['lower'][li] -= fac
                    blocks.append(dict(row=r.name, hist=h, source=w, factor=str(fac),
                                       lower=[li], member=member, kind='B4-single'))
            for x, y in combinations_with_replacement(range(2), 2):
                r = row(('new-pair-to-B4-upper', x, y))
                source_income(r, h, w, fac)
                union = {j: F(s[x] | s[y]) for j, s in b4[h]}
                intersection = {j: F(s[x] & s[y]) for j, s in b4[h]}
                ls = [lower_bound(h, w, pair_prices(w, 1), query_old=union),
                      lower_bound(h, w, pair_prices(w, 2), query_old=intersection)]
                for li in ls:
                    r.parts['lower'][li] -= fac
                blocks.append(dict(row=r.name, hist=h, source=w, factor=str(fac),
                                   lower=ls, roles=[x, y], kind='B4-pair'))
    assert len(principal) == 139
    newrows = [r.output() for r in principal]
    base_rows = [dict(r, lower=[]) for r in oldmodel['rows']]
    rows = base_rows[:299]+newrows+base_rows[299:]
    assert len(base_rows) == 5699
    piece_rows = []
    for j, d in enumerate(lower):
        prices = list(map(F, d['prices']))
        for lam in map(F, d['lambdas']):
            r = Row(('sorting-piece', j, str(lam)), 'sorting-lower-piece')
            r.parts['lower'][j] = F(1)
            for k, v in d['query_old']:
                r.parts['old'][k] -= lam*F(v)
            for k, v in d['query_mu']:
                r.parts['mu'][k] -= lam*F(v)
            for k, price in zip(d['source_mu'], prices):
                r.parts['mu'][k] += max(lam-price, F())
            piece_rows.append(r.output())
    rows += piece_rows
    eqs = [dict(r, lower=[]) for r in oldmodel['equalities']]
    old_aux = [descriptor(c) for c in allcols[4849:15593]]
    identity = dict(point_sha256=PIN, previous_point_sha256=OLDPIN,
                    previous_prefix_descriptors_equal=15593, old_semantic_columns=4849,
                    old_auxiliary_columns=10744, old_auxiliary_kinds=dict(Counter(c['kind'] for c in old_aux)),
                    extra_full624_columns=4992, full_point_columns=20585,
                    old_auxiliary_descriptors_sha256=hashlib.sha256(json.dumps(old_aux, sort_keys=True).encode()).hexdigest(),
                    hist_ids=list(hist), zero_hist_ids=[h for h in hist if not F(allcols[h]['weight'])],
                    semantic_weights_used_in_symbolic_coefficients=False)
    sources = [POINT, OLDPOINT, UPSTREAM, BASE/'main_root_sorting_contract.md',
               BASE/'root_marginal_closure.md', BASE/'root_marginal_closure/model.py',
               BASE/'root_marginal_closure/verify_completion.py', BASE/'root_network_joint.md',
               BASE/'root_marginal_closure/marginal_completion_exact.json',
               BASE/'root_network_joint/fixed_mu_upper_bounds_exact.json',
               BASE/'root_network_joint/full32_obstruction_rows_exact.json',
               BASE/'../../../archives/customer-attraction/state/引理/跨族末两人菜单的共同锚点与运输界--引理.md']
    out = dict(scope='Complete RS1--3 block sorting envelope, fixed hist identities; no common coupling or SPE assertion.',
               point_path=str(POINT.relative_to(BASE)), point_sha256=PIN,
               original_columns=old, old_column_count=4849, old_column_identity=identity,
               root_groups=[dict(hist=h, old_word=w) for h, w in groups],
               mu_columns=mu, mu_column_count=1216,
               aux_columns=oldmodel['aux_columns'], aux_column_count=2700,
               lower_columns=lower, lower_column_count=len(lower),
               principal_row_count=438, inherited_principal_count=299, added_principal_count=139,
               cap_row_count=5400, sorting_piece_row_count=len(piece_rows),
               rows=rows, equalities=eqs, equality_count=38, transport_blocks=blocks,
               nonnegative_variables=['all mu', 'all min aux', 'all sorting lower'],
               omitted=['simultaneous common law across blocks', 'same ordered-history strategy consistency'],
               sources=[dict(path=str(p.relative_to(BASE)), sha256=sha(p)) for p in sources],
               script_sha256=sha(__file__))
    write(HERE/'symbolic_matrix_exact.json.gz', out)
    write(HERE/'input_identity.json', identity)
    summary = dict(principal=438, inherited_principal=299, new_principal=139, cap_rows=5400,
                   sorting_lower_variables=len(lower), sorting_piece_rows=len(piece_rows),
                   total_inequalities=len(rows), equalities=38, mu=1216, min_aux=2700,
                   phase1_variables=1216+2700+len(lower)+1,
                   independent_transport_block_occurrences=len(blocks),
                   symbolic_nonzeros=sum(len(r[k]) for r in rows for k in KINDS),
                   matrix_sha256=sha(HERE/'symbolic_matrix_exact.json.gz'),
                   elapsed_seconds=time.perf_counter()-start)
    write(HERE/'model_summary.json', summary)
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == '__main__':
    build()
