"""Exact SAME-X root append, entirely symbolic and standard-library only.

The immutable old 21021 coordinates keep their identities.  The 1216 mu
coordinates are the weight-free root_sorting_20910 coordinates; eta has one
matching coordinate per mu, shared by every row.  No point is loaded, no
optimizer is imported, and no file outside HERE is written.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement, product
from pathlib import Path
import gzip
import json
import time

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
ROOT = BASE / 'root_sorting_20910/symbolic_matrix_exact.json.gz'
OWN = BASE / 'root_x_joint_contract/own_blocks.json'
XLIFT = BASE / 'terminal_response_cycles/max_b_symbolic_lift.json'
KINDS = ('old', 'mu', 'eta', 'z', 'cost')


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()


def write(name, value):
    data = canonical(value) + b'\n'
    path = HERE / name
    if path.suffix == '.gz':
        with path.open('wb') as f:
            with gzip.GzipFile(fileobj=f, mode='wb', mtime=0) as out:
                out.write(data)
    else:
        path.write_bytes(data)


def frozen(value):
    return tuple(map(frozen, value)) if isinstance(value, (list, tuple)) else value


def bits(value, n=5):
    return tuple((value >> k) & 1 for k in range(n - 1, -1, -1))


def share(numerator, denominator):
    return F(numerator, denominator) if numerator else F()


def sparse():
    return defaultdict(F)


def plus(target, source, factor=F(1)):
    for key, value in source.items():
        target[key] = target.get(key, F()) + factor * value
    return target


def expr(kind, index, value=F(1)):
    return {(kind, index): F(value)} if value else {}


def cleaned(value):
    return {key: val for key, val in value.items() if val}


def expr_key(value):
    return tuple(sorted(cleaned(value).items()))


def encoded_expr(value):
    return [[kind, index, str(v)] for (kind, index), v in sorted(cleaned(value).items())]


def make_row(name, value, category='principal', **meta):
    return dict(name=name, category=category,
                **{kind: [[i, str(v)] for (k, i), v in sorted(cleaned(value).items()) if k == kind]
                   for kind in KINDS}, **meta)


def row_expr(row):
    return {(kind, j): F(value) for kind in KINDS for j, value in row.get(kind, [])}


def orbit_key(queries):
    names, answer = {}, []
    for family, role, ids in queries:
        answer.append((family, role, tuple(names.setdefault(i, len(names)) for i in ids)))
    return tuple(answer)


def unordered_key(q, r):
    return min(orbit_key((q, r)), orbit_key((r, q)))


def catalog():
    old = [('A', k, ()) for k in range(6)]
    old += [(family, 0, (i,)) for family in ('T', 'B', 'C') for i in range(6)]
    old += [(family, f, (i, j)) for family in ('R', 'Z')
            for f, i, j in product(range(2), range(6), range(6)) if f or i != j]
    old += [('H', k, ()) for k in range(2)]
    tails = [('Y', k, (i,)) for k in range(5) for i in range(6)]
    return old, [('X', 0, ())], tails


class Builder:
    def __init__(self):
        with gzip.open(ROOT, 'rt') as f:
            root = json.load(f)
        self.root = root
        self.old = root['original_columns']
        assert len(self.old) == 4849 and all('weight' not in c for c in self.old)
        own, xlift = json.loads(OWN.read_text()), json.loads(XLIFT.read_text())
        self.hist = {int(h): c for h, c in own['hist_records']}
        self.mu = root['mu_columns']
        self.index = {(c['hist'], c['old_word'], c['state']): j for j, c in enumerate(self.mu)}
        self.groups = [(h, w) for h, c in self.hist.items() for w, n in enumerate(c['hist']) if n]
        assert self.groups == [tuple(v) for v in own['root_groups']]
        assert len(self.hist) == 16 and len(self.groups) == 38 and len(self.mu) == 1216
        assert self.mu == [dict(hist=h, old_word=w, state=s) for h, w in self.groups for s in range(32)]
        self.x = {c['hist_column']: 20585 + i for i, c in enumerate(xlift['new_columns'])
                  if c['kind'] == 'common-X-mass'}
        assert set(self.x) == set(self.hist) and sorted(self.x.values()) == list(range(20585, 20601))
        self.query = {}
        for i, c in enumerate(xlift['new_columns'], 20585):
            if c['kind'] != 'common-X-mass':
                self.query[c['hist_column'], frozen(c['query_token'])] = (
                    {('old', j): F(v) for j, v in c['query_marginal']}, expr('old', i))
        assert len(self.query) == 420
        self.a, self.C = sparse(), sparse()
        for h, c in self.hist.items():
            actual = tuple(map(int, c['actual_bits']))
            assert self.old[h] == c
            self.a['old', h] = share(actual[4], sum(actual))
            self.C['old', self.x[h]] = F(1, sum(actual[:4]) + 1)
        self.a, self.C = cleaned(self.a), cleaned(self.C)
        # Compare symbolic incomes; XLIFT's 436 new columns use compressed 4849 offset.
        assert self.a == {('old', j): F(v) for j, v in xlift['incomes'][4]}
        assert self.C == {('old', j - 4849 + 20585): F(v) for j, v in xlift['B_X']}
        self.z, self.zmap, self.cost, self.costmap = [], {}, [], {}
        self.rc_blocks, self.rp_blocks = [], []

    def marginal(self, h, q):
        """Resolve a block token to total / X=0 / X=1 masses."""
        family = q[0]
        if family == 'constant':
            total, one = expr('old', h, q[1]), expr('old', self.x[h], q[1])
        elif family == 'X':
            total = one = expr('old', self.x[h])
        elif family == 'Y':
            _, k, w = q
            total = {('mu', self.index[h, w, s]): F(bits(s)[k]) for s in range(32) if bits(s)[k]}
            one = {('eta', self.index[h, w, s]): F(bits(s)[k]) for s in range(32) if bits(s)[k]}
        else:
            token = (family, q[1]) if family in ('R', 'Z') else ('H', q[1])
            total, one = self.query[h, token]
        zero = plus(plus(sparse(), total), one, F(-1))
        return total, cleaned(zero), one

    def resolve(self, h, words, q):
        family, role, ids = q
        if family == 'A':
            return ('constant', int(self.hist[h]['actual_bits'][role]))
        if family in ('T', 'B', 'C'):
            return ('constant', bits(words[ids[0]], 3)[('T', 'B', 'C').index(family)])
        if family in ('X', 'H'):
            return (family, role)
        if family == 'Y':
            return ('Y', role, words[ids[0]])
        i, j = ids
        return (family, (role, int(i == j), bits(words[i], 3), bits(words[j], 3)))

    def root_wallet(self, h, w):
        answer = sparse()
        for s in range(32):
            e, t = bits(s), w >> 2
            p, N = t + sum(e[:3]), t + sum(e)
            answer['mu', self.index[h, w, s]] = share(e[3] + e[4], N) + F(e[3], (p + 1) * (p + 2))
        return cleaned(answer)

    def direct(self):
        rows = []
        specs = ([('RX', k) for k in range(1, 6)] + [('RPQ', q) for q in range(6)] + [('RXX',)]
                 + [('XM', k) for k in range(1, 6)] + [('XC', k) for k in range(1, 6)]
                 + [('RC-SAME', l, m) for l, m in combinations_with_replacement(range(6), 2) if (l, m) != (0, 0)])
        for spec in specs:
            row = sparse()
            family = spec[0]
            if family in ('XM', 'RC-SAME'):
                plus(row, self.C)
            if family in ('XC', 'RC-SAME'):
                plus(row, self.a)
            for j, desc in enumerate(self.mu):
                h, w, s = desc['hist'], desc['old_word'], desc['state']
                e, t = bits(s), w >> 2
                N, p = t + sum(e), t + sum(e[:3])
                P = sum(map(int, self.hist[h]['actual_bits'][:4]))
                Dp, DP = (p + 1) * (p + 2), (P + 1) * (P + 2)
                fac = F(self.hist[h]['hist'][w], 6)
                W = share(e[3] + e[4], N) + F(e[3], Dp)
                um, ue = F(), F()
                if family == 'RX':
                    k = spec[1] - 1
                    um, ue = share(e[k], N), -F(1, t + sum(e[:k]) + 5 - k)
                elif family == 'RPQ':
                    q = (t,) + e
                    um, ue = W - F(q[spec[1]], p + 1), -F(1, p + 1) + F(q[spec[1]], Dp)
                elif family == 'RXX':
                    um, ue = W, -F(1, p + 1) - F(1, p + 2)
                elif family in ('XM', 'XC'):
                    um = -F(e[spec[1] - 1], P + 1)
                    if family == 'XC':
                        ue = F(e[spec[1] - 1], DP)
                else:
                    v, l, m = (t,) + e, spec[1], spec[2]
                    um = -F(v[l] + v[m], P + 1) + F(v[l] * v[m], DP)
                row['mu', j] += fac * um
                row['eta', j] += fac * ue
            rows.append(make_row(list(spec), row, source_family=('root_true_source' if family in ('RX', 'RPQ', 'RXX') else 'actual_first_four')))
        assert len(rows) == 42
        upper = [make_row(['eta-upper', j], {('mu', j): F(1), ('eta', j): F(-1)}, 'eta-upper') for j in range(1216)]
        equalities = []
        for h, w in self.groups:
            row = {('eta', self.index[h, w, s]): F(1) for s in range(32)}
            row['old', self.x[h]] = F(-1)
            equalities.append(make_row(['eta-mass', h, w], row, 'equality'))
        hist_x_bounds = []
        for h, x in self.x.items():
            hist_x_bounds += [make_row(['X-nonnegative', h], {('old', x): F(1)}, 'inherited-bound'),
                              make_row(['X-upper', h], {('old', h): F(1), ('old', x): F(-1)}, 'inherited-bound')]
        return dict(status='SYMBOLIC_DIRECT42_NO_GAME_POINT_EVALUATED', old_column_count=21021,
                    mu_columns=self.mu, eta_columns=self.mu, hist_records=list(self.hist.items()),
                    hist_to_x=list(self.x.items()), rows=rows, eta_upper_rows=upper,
                    eta_equalities=equalities, hist_x_bounds=hist_x_bounds,
                    nonnegative_variables=['all eta', 'all mu inherited'],
                    inherited_root_mu_mass='Each group sum(mu)=H; the exact 438-principal root lift remains separate.',
                    sources=[dict(path=str(p.relative_to(BASE)), sha256=digest(p)) for p in (ROOT, OWN, XLIFT)])

    def minimum(self, h, epsilon, left, right):
        caps = tuple(sorted((expr_key(left), expr_key(right))))
        key = h, epsilon, caps
        if key not in self.zmap:
            self.zmap[key] = len(self.z)
            self.z.append(dict(hist=h, X_bit=epsilon, caps=[encoded_expr(dict(cap)) for cap in caps]))
        return self.zmap[key]

    def sorting_cost(self, h, w, epsilon, query):
        prices = tuple(F(1, (w >> 2) + sum(bits(s)[:3]) + 1 + epsilon) for s in range(32))
        key = h, w, epsilon, prices, expr_key(query)
        if key not in self.costmap:
            self.costmap[key] = len(self.cost)
            self.cost.append(dict(hist=h, old_word=w, X_bit=epsilon, prices=list(map(str, prices)),
                                  source_indices=[self.index[h, w, s] for s in range(32)],
                                  query=encoded_expr(query), lambdas=list(map(str, sorted(set(prices))))))
        return self.costmap[key]

    def root_pairs(self, orbits):
        rows = []
        for oi, (key, literals) in enumerate(sorted(orbits.items())):
            row = sparse()
            for h, c in self.hist.items():
                words = [w for w, count in enumerate(c['hist']) for _ in range(count)]
                counts = Counter((words[i], self.resolve(h, words, q),
                                  q[0] == 'Y' and q[2][0] == i) for i, q in literals)
                assert sum(counts.values()) == len(literals)
                for (w, q, same), count in sorted(counts.items()):
                    fac = F(count, len(literals))
                    plus(row, self.root_wallet(h, w), fac)
                    record = dict(orbit=oi, hist=h, source_word=w, query=q,
                                  same_root=same, count=count, orbit_size=len(literals), factor=str(fac))
                    if q[0] == 'constant' or (q[0] == 'Y' and same):
                        for s in range(32):
                            p = (w >> 2) + sum(bits(s)[:3])
                            v = q[1] if q[0] == 'constant' else bits(s)[q[1]]
                            j = self.index[h, w, s]
                            row['mu', j] -= fac * F(v, p + 1)
                            row['eta', j] += fac * (-F(1, p + 1) + F(v, (p + 1) * (p + 2)))
                        record['method'] = 'exact-root-state'
                    elif q[0] == 'X':
                        for s in range(32):
                            p = (w >> 2) + sum(bits(s)[:3])
                            row['eta', self.index[h, w, s]] -= fac * (F(1, p + 1) + F(1, p + 2))
                        record['method'] = 'exact-repeat-X'
                    else:
                        for s in range(32):
                            p = (w >> 2) + sum(bits(s)[:3])
                            row['eta', self.index[h, w, s]] -= fac * F(1, p + 1)
                        _, zero, one = self.marginal(h, q)
                        costs = [self.sorting_cost(h, w, epsilon, qq) for epsilon, qq in enumerate((zero, one))]
                        for j in costs:
                            row['cost', j] -= fac
                        record.update(method='conditional-sorting-envelope', cost=costs)
                    self.rp_blocks.append(record)
            rows.append(make_row(['RP-ORBIT', oi], row, orbit=key, orbit_size=len(literals),
                                 source=['T_i', 'Y_i1', 'Y_i2', 'Y_i3'], wallet='root W'))
        return rows

    def actual_pairs(self, orbits):
        rows = []
        for oi, (key, literals) in enumerate(sorted(orbits.items())):
            row = plus(plus(sparse(), self.a), self.C)
            for h, c in self.hist.items():
                words = [w for w, count in enumerate(c['hist']) for _ in range(count)]
                P = sum(map(int, c['actual_bits'][:4]))
                DP = (P + 1) * (P + 2)
                counts = Counter()
                for q, r in literals:
                    a, b = self.resolve(h, words, q), self.resolve(h, words, r)
                    same = q[0] == r[0] == 'Y' and q[2] == r[2]
                    a, b = sorted((a, b))
                    counts[a, b, same] += 1
                assert sum(counts.values()) == len(literals)
                for (q, r, same), count in sorted(counts.items()):
                    fac = F(count, len(literals))
                    qt, q0, q1 = self.marginal(h, q)
                    rt, r0, r1 = self.marginal(h, r)
                    # Keep known constant query bits on the same root measure.
                    # Replacing sum(mu)=H here is valid but would obscure exact
                    # coefficient equality with the direct RC-SAME interface.
                    if q[0] == 'constant':
                        assert r[0] == 'Y'
                        qt = {('mu', self.index[h, r[2], s]): F(q[1]) for s in range(32)}
                    elif r[0] == 'constant':
                        assert q[0] == 'Y'
                        rt = {('mu', self.index[h, q[2], s]): F(r[1]) for s in range(32)}
                    plus(row, qt, -fac / (P + 1))
                    plus(row, rt, -fac / (P + 1))
                    record = dict(orbit=oi, hist=h, queries=[q, r], same_root=same,
                                  count=count, orbit_size=len(literals), factor=str(fac))
                    if q[0] == 'constant' or r[0] == 'constant':
                        inter = {j: v * (q[1] if q[0] == 'constant' else r[1])
                                 for j, v in (rt if q[0] == 'constant' else qt).items()}
                        record['method'] = 'exact-constant-bit'
                    elif q[0] == 'X' or r[0] == 'X':
                        inter = r1 if q[0] == 'X' else q1
                        record['method'] = 'exact-shared-X'
                    elif same:
                        assert q[0] == r[0] == 'Y' and q[2] == r[2]
                        inter = {('mu', self.index[h, q[2], s]): F(bits(s)[q[1]] * bits(s)[r[1]])
                                 for s in range(32) if bits(s)[q[1]] * bits(s)[r[1]]}
                        record['method'] = 'exact-same-root'
                    else:
                        z = [self.minimum(h, epsilon, a, b) for epsilon, (a, b) in enumerate(((q0, r0), (q1, r1)))]
                        inter = {('z', j): F(1) for j in z}
                        record.update(method='conditional-intersection-envelope', z=z)
                    plus(row, inter, fac / DP)
                    self.rc_blocks.append(record)
            rows.append(make_row(['RC-ORBIT', oi], row, orbit=key, orbit_size=len(literals),
                                 source=['A1', 'A2', 'A3', 'A4'], wallet='actual a+C'))
        return rows

    def auxiliary_rows(self):
        upper, pieces = [], []
        for j, desc in enumerate(self.z):
            for k, cap in enumerate(desc['caps']):
                row = {(kind, index): F(v) for kind, index, v in cap}
                row['z', j] = F(-1)
                upper.append(make_row(['conditional-min-cap', j, k], row, 'conditional-min-cap'))
        for j, desc in enumerate(self.cost):
            for lam in map(F, desc['lambdas']):
                row = {('cost', j): F(1)}
                plus(row, {(kind, index): F(v) for kind, index, v in desc['query']}, -lam)
                for index, price in zip(desc['source_indices'], map(F, desc['prices'])):
                    value = max(lam - price, F())
                    if desc['X_bit']:
                        plus(row, expr('eta', index, value))
                    else:
                        plus(row, expr('mu', index, value))
                        plus(row, expr('eta', index, -value))
                pieces.append(make_row(['conditional-sorting-piece', j, str(lam)], row, 'conditional-sorting-piece'))
        return upper, pieces


def main():
    started = time.perf_counter()
    builder = Builder()
    direct = builder.direct()
    write('direct_interface_exact.json.gz', direct)
    old, xs, ys = catalog()
    queries = old + xs + ys
    assert len(old) == 158 and len(queries) == 189
    ordered, unordered, root_pairs = defaultdict(list), defaultdict(list), defaultdict(list)
    for q, r in product(queries, repeat=2):
        if q[0] == 'Y' or r[0] == 'Y':
            ordered[orbit_key((q, r))].append((q, r))
    for q, r in combinations_with_replacement(queries, 2):
        if q[0] == 'Y' or r[0] == 'Y':
            unordered[unordered_key(q, r)].append((q, r))
    for i in range(6):
        for q in queries:
            root_pairs[orbit_key((('source', 0, (i,)), q))].append((i, q))
    assert len(ordered) == 360 and len(unordered) == 185 and len(root_pairs) == 41
    assert len({orbit_key((q, r)) for q, r in product(old, repeat=2)}) == 490
    rp = builder.root_pairs(root_pairs)
    rc = builder.actual_pairs(unordered)
    zrows, costrows = builder.auxiliary_rows()
    principals = [r for r in direct['rows'] if r['name'][0] in ('RX', 'XM')] + rp + rc
    assert len(principals) == 236
    # Exact duplicates are recognized only after full coefficient equality.
    maps = defaultdict(list)
    for i, row in enumerate(principals):
        maps[expr_key(row_expr(row))].append(i)
    alias = []
    for i, row in enumerate(direct['rows']):
        match = maps[expr_key(row_expr(row))]
        assert match
        alias.append(dict(direct=i, direct_name=row['name'], extended=match[0], extended_name=principals[match[0]]['name']))
    unordered_ids = {key: i for i, key in enumerate(sorted(unordered))}
    ordered_map = [dict(ordered=i, key=key, literal_count=len(ordered[key]),
                        unordered=unordered_ids[unordered_key(*key)])
                   for i, key in enumerate(sorted(ordered))]
    orbit_data = dict(old_catalog=old, X_catalog=xs, root_catalog=ys,
                      old_ordered_orbits=490,
                      actual_RC_unordered=[dict(orbit=i, key=key, literal_count=len(v), literals=v)
                                           for i, (key, v) in enumerate(sorted(unordered.items()))],
                      actual_RC_ordered=ordered_map,
                      root_PAIR=[dict(orbit=i, key=key, literal_count=len(v), literals=v)
                                 for i, (key, v) in enumerate(sorted(root_pairs.items()))],
                      direct_to_extended=alias)
    write('query_orbits_exact.json.gz', orbit_data)
    extended = dict(status='SYMBOLIC_SHARED_ETA_CONDITIONAL_ENVELOPE_NO_GAME_POINT_EVALUATED',
                    old_column_count=21021, mu_columns=builder.mu, eta_columns=builder.mu,
                    hist_records=list(builder.hist.items()), hist_to_x=list(builder.x.items()),
                    principal_rows=principals, eta_upper_rows=direct['eta_upper_rows'],
                    eta_equalities=direct['eta_equalities'], z_columns=builder.z, cost_columns=builder.cost,
                    z_upper_rows=zrows, sorting_piece_rows=costrows,
                    root_PAIR_blocks=builder.rp_blocks, actual_RC_blocks=builder.rc_blocks,
                    direct_to_extended=alias,
                    nonnegative_variables=['all eta', 'all z', 'all cost; mu inherited'],
                    required_old_semantics='420 y are real X overlaps satisfying the 1260 own facets; all old rows remain.',
                    inherited_root=dict(path=str(ROOT.relative_to(BASE)), sha256=digest(ROOT),
                                        principal_rows=438, inequalities=len(builder.root['rows']), equalities=38,
                                        mu=1216, aux=2700, lower=9572),
                    omitted=['joint optimal transports across different query blocks',
                             'a complete old hidden law with one X over that full law',
                             'global named-root correlations and ordered-history/alias constraints'])
    write('extended_interface_exact.json.gz', extended)
    # Namespaces enable append to an existing variable-mu system, without fixing mu.
    sizes = [('old', 21021), ('mu', 1216), ('inherited_root_aux', 2700),
             ('inherited_root_lower', 9572), ('eta', 1216), ('z', len(builder.z)), ('cost', len(builder.cost))]
    offset, blocks = 0, []
    for name, size in sizes:
        blocks.append(dict(namespace=name, offset=offset, count=size))
        offset += size
    write('append_index_map.json', dict(blocks=blocks, column_count=offset,
                                        old_21021_identity_preserved=True, actual_parent_rows=23676,
                                        root_438_inequalities=len(builder.root['rows']), root_equalities=38,
                                        new_inequalities=len(principals)+len(direct['eta_upper_rows'])+len(zrows)+len(costrows),
                                        new_equalities=38, nonnegativity_is_variable_bound=True,
                                        no_combined_parent_matrix_written=True))
    counts = dict(direct_rows=42, extension_principals=236, root_PAIR_rows=41,
                  actual_RC_unordered_rows=185, actual_RC_ordered_orbits=360,
                  actual_RC_ordered_literal_pairs=sum(map(len, ordered.values())),
                  actual_RC_unordered_literal_pairs=sum(map(len, unordered.values())),
                  eta_columns=1216, eta_upper_rows=1216, eta_mass_equalities=38,
                  conditional_min_columns=len(builder.z), conditional_min_cap_rows=len(zrows),
                  conditional_sorting_columns=len(builder.cost), conditional_sorting_piece_rows=len(costrows),
                  root_PAIR_block_occurrences=len(builder.rp_blocks), actual_RC_block_occurrences=len(builder.rc_blocks),
                  root_PAIR_orbit_size_distribution=dict(Counter(map(len, root_pairs.values()))),
                  actual_RC_ordered_orbit_size_distribution=dict(Counter(map(len, ordered.values()))),
                  actual_RC_unordered_orbit_size_distribution=dict(Counter(map(len, unordered.values()))))
    counts['new_inequalities'] = len(principals)+1216+len(zrows)+len(costrows)
    counts['new_inequality_nonzeros'] = sum(sum(len(r[k]) for k in KINDS) for r in principals+direct['eta_upper_rows']+zrows+costrows)
    counts['direct_principal_nonzeros'] = sum(sum(len(r[k]) for k in KINDS) for r in direct['rows'])
    write('build_summary.json', dict(status='BUILT_SYMBOLIC_INTERFACES', counts=counts,
                                     optimizer_calls=0, game_point_values_read=0,
                                     frozen23676_matrix_modified=False,
                                     elapsed_seconds=time.perf_counter()-started))
    print(json.dumps(counts, sort_keys=True))


if __name__ == '__main__':
    main()
