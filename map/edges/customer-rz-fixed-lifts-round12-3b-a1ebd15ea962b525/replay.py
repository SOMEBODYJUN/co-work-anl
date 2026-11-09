"""Replay the fixed-coordinate comparisons with exact arithmetic, without an LP."""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TASK = ROOT / 'research/operations/map-v2/tasks' / (HERE.name + '.json')
WORDS = tuple(product(range(2), repeat=3))
STATES = ((0, 1), (1, 0), (1, 1))
EDGES = [(f, i, j) for f, i, j in product(range(2), range(6), range(6)) if f or i != j]
BASIC = ('source', 'pair', 'price', 'capacity', *(f'actual{k}' for k in range(6)), 'ownR', 'reverseR')
NEW = ('source', 'terminal_own_B', 'terminal_own_C', 'terminal_own_T', 'terminal_opt_average',
       *(f'terminal_actual_{k}' for k in range(1, 7)), 'terminal_B_average', 'terminal_C_average',
       'reverse_terminal', 'price', 'capacity')
CROSS = ('Z-R', 'R-Z', 'pair-RR')


def partition(indices):
    order = {}
    return tuple(order.setdefault(i, len(order)) for i in indices)


P3 = sorted({partition(p) for p in product(range(3), repeat=3)})
P4 = sorted({partition(p) for p in product(range(4), repeat=4)})
FIRST = (
    [f'old_{k}' for k in range(5)]
    + [f'new_{f}_{q}' for f, q in product('BC', NEW)]
    + list(product(('new-new',), range(2), range(2), P4))
    + list(product(('new-old',), range(2), range(3), P3))
    + list(product(('old-new',), range(2), P3))
)
SECOND = (
    list(product(('basic',), range(2), BASIC))
    + list(product(('Z-old',), range(2), range(3), P3))
    + list(product(('old-Z',), range(2), P3))
)
THIRD = list(product(CROSS, range(2), range(2), P4))


def freeze(item):
    return tuple(map(freeze, item)) if isinstance(item, list) else item


def share(n, d):
    return F(n, d) if n else F(0)


def without_weight(col):
    return {k: v for k, v in col.items() if k != 'weight'}


def load_inputs():
    task = json.loads(TASK.read_bytes())['definition']
    sources, bodies = {}, {}
    for segment in task['context_plan']['reading_passes']:
        path = ROOT / segment['source']['path']
        if path not in bodies:
            data = path.read_bytes()
            assert sha256(data).hexdigest() == segment['source']['sha256']
            bodies[path] = data.decode('utf-8')
        body = bodies[path]
        start, end = segment['start_char'], segment['end_char_exclusive']
        assert body.count('\n', 0, start) + 1 == segment['start_line']
        assert len(body[start:end].splitlines()) == segment['end_line'] - segment['start_line'] + 1
        if path.suffix == '.json' and path.name not in sources:
            sources[path.name] = json.loads(body)
    dependencies = sources['runtime-dependencies.json']
    entries = dependencies['prior_25_file_closure']
    assert len(entries) == dependencies['current_primary_overlap'] + dependencies['additional_related_files'] == 25
    for entry in entries:
        assert sha256((ROOT / entry['repo_path']).read_bytes()).hexdigest() == entry['sha256']
    print('15 reading spans and 25 pinned legacy runtime inputs matched')
    return sources


def check_columns_and_rows(inputs):
    reports = [inputs[n] for n in ('full_new_reply_closure_exact.json', 'actual_fifth_nested_exact.json',
                                   'attractive_nested_exact.json')]
    tables = [inputs[f'{prefix}-all-row-slacks.json'] for prefix in ('closure1033', 'nested1097', 'attractive3889')]
    small, middle, large = [r['columns'] for r in reports]
    assert [len(c) for c in (small, middle, large)] == [211, 599, 1905]
    hist = {}
    old_r = {}
    small_descriptors = [{'kind': 'K'}]
    middle_descriptors = [{'kind': 'K'}]
    middle_hist = {}
    group_order = {}
    for hid, c in enumerate(small):
        if c['kind'] != 'hist':
            continue
        a = tuple(map(int, c['actual_bits']))
        words = [word for n, word in zip(c['hist'], WORDS) for _ in range(n)]
        assert len(a) == len(words) == 6 and sum(w[0] for w in words) == c['d'] == 1
        assert len(c['hist']) == 8 and min(c['hist']) >= 0
        assert hid == len(small_descriptors)
        hist[hid] = a, words, F(c['weight'])
        middle_hist[hid] = len(middle_descriptors)
        small_descriptors.append(without_weight(c))
        middle_descriptors.append(without_weight(c))
        groups = sorted({(f, int(i == j), words[i], words[j]) for f, i, j in EDGES})
        group_order[hid] = groups
        for g in groups:
            rid = len(small_descriptors)
            group = json.loads(json.dumps(g))
            small_descriptors.append({'kind': 'new-reply', 'hist_column': hid, 'group': group})
            old_r[hid, g] = rid
            for state in STATES:
                middle_descriptors.append({'kind': 'joint-reply', 'hist_column_old': hid,
                                           'group': group, 'state': list(state)})
    large_descriptors = middle_descriptors + [
        {'kind': 'overlap', 'hist_column': middle_hist[hid], 'groups': json.loads(json.dumps(pair))}
        for hid, groups in group_order.items() for pair in combinations(groups, 2)
    ]
    assert len(hist) == 16 and sum(h > 0 for _, _, h in hist.values()) == 10 and len(old_r) == 194
    for report, descriptors, table, counts in zip(
            reports, (small_descriptors, middle_descriptors, large_descriptors),
            tables, ((1033, 173, 61), (1097, 216, 96), (3889, 2241, 175))):
        rows, zeros, positives = counts
        cols = report['columns']
        assert [without_weight(c) for c in cols] == descriptors
        weights = [F(c['weight']) for c in cols]
        assert min(weights) >= 0 and sum(w > 0 for w in weights) == positives == report['positive_columns']
        assert len(table) == rows == report['verified_rows'] and all(k == i for i, (k, _, _) in enumerate(table))
        values = [F(s) for _, _, s in table]
        assert min(values) == 0 == F(report['minimum_slack']) and values.count(0) == zeros
        assert len({name for _, name, _ in table}) == rows
        assert [c for c in cols if c['kind'] in ('K', 'hist')] == [
            c for c in small if c['kind'] in ('K', 'hist')]
        welfare = sum(mass for a, _, mass in hist.values() if any(a))
        assert sum(mass for _, _, mass in hist.values()) == F(report['O']) == 1
        assert welfare == F(report['W']) < F(1, 2)
        assert 1 - 2*welfare == F(report['strict_half_gap'])
    assert tables[0][:702] == tables[1][:702] == tables[2][:702]
    assert sum(F(m['weight']) != F(l['weight']) for m, l in zip(middle, large)) == 78
    return hist, old_r, [r['columns'] for r in reports], [dict((n, F(s)) for _, n, s in table) for table in tables]


def first_rows(hist, r, K):
    rows = defaultdict(F)
    for f, multiplicity in zip('BC', (30, 36)):
        rows[f'new_{f}_capacity'] = multiplicity*K
    for hid, (a, words, h) in hist.items():
        p, pa, ell, s = sum(a[:3]), sum(a[:4]), sum(a[:5]), sum(a)
        D = (pa+1)*(pa+2)
        ha = share(a[4]+a[5], s) + F(a[4], D)
        d, nb, nc = map(sum, zip(*words))
        for i, (t, b, c) in enumerate(words):
            rows['old_0'] += h*(share(a[3], s)-share(t, p+t+b+c))
            rows['old_1'] += h*(ha-F(b+c, pa+1)+F(b*c, D))
            hi = share(b+c, p+t+b+c)+F(b, (p+t+1)*(p+t+2))
            for j, (_, bj, cj) in enumerate(words):
                if i != j:
                    rows['old_2'] += h*(share(c, p+t+b+c)-F(bj, p+t+b+1))
                    rows['old_4'] += h*(hi-F(bj+cj, p+t+1)+F(bj*cj, (p+t+1)*(p+t+2)))
                rows['old_3'] += h*(share(c, p+t+b+c)-F(cj, p+t+b+1))
        for f, i, j in EDGES:
            t, b, c = words[i]
            y = words[j][1+f]
            de = p+t+y+1
            re = r[hid, (f, int(i == j), words[i], words[j])]
            values = (h*share(b, p+t+b+c)-(h-re)*share(y, de-1)-re*share(y, de),)
            values += tuple((re-h*q)/de for q in (b, c, t, F(d, 6), *a, F(nb, 6), F(nc, 6)))
            values += (h*share(c, p+t+b+c)-re/(p+t+b+1), h*share(a[5], s)-re/(ell+1), -re)
            for name, value in zip(NEW, values):
                rows[f'new_{"BC"[f]}_{name}'] += value
            for g, k, l in EDGES:
                rf = r[hid, (g, int(k == l), words[k], words[l])]
                rows['new-new', f, g, partition((i, j, k, l))] += (re-rf)/de
            for k, (tk, bk, ck) in enumerate(words):
                for q in range(3):
                    rows['new-old', f, q, partition((i, j, k))] += (re-h*words[k][q])/de
                rows['old-new', f, partition((k, i, j))] += h*share(ck, p+tk+bk+ck)-re/(p+tk+bk+1)
    return rows


def second_rows(hist, joint, K):
    rows = defaultdict(F)
    for f, multiplicity in enumerate((30, 36)):
        rows['basic', f, 'capacity'] = multiplicity*K
    for hid, (a, words, h) in hist.items():
        p, pa, ell, s = sum(a[:3]), sum(a[:4]), sum(a[:5]), sum(a)
        D = (pa+1)*(pa+2)
        ha = share(a[4]+a[5], s)+F(a[4], D)
        for f, i, j in EDGES:
            g = f, int(i == j), words[i], words[j]
            de = p+words[i][0]+words[j][1+f]+1
            v01, v10, v11 = joint[hid, g]
            for (r, z), mass in zip(((0, 0), *STATES), (h-v01-v10-v11, v01, v10, v11)):
                assert mass >= 0
                vz = share(z, pa+r+z)
                values = (share(a[4], s)-share(r, pa+r+z), ha-F(r+z, pa+1)+F(r*z, D),
                          share(a[5], s)-F(z, ell+1), -F(z))
                values += tuple(vz-F(bit, pa+r+1) for bit in a)
                values += (vz-F(r, pa+r+1), F(r-z, de))
                for name, value in zip(BASIC, values):
                    rows['basic', f, name] += mass*value
                for k, (tk, bk, ck) in enumerate(words):
                    for q in range(3):
                        rows['Z-old', f, q, partition((i, j, k))] += mass*(vz-F(words[k][q], pa+r+1))
                    rows['old-Z', f, partition((k, i, j))] += mass*(share(ck, p+tk+bk+ck)-F(z, p+tk+bk+1))
    return rows


def margins(joint):
    return ({key: v10+v11 for key, (_, v10, v11) in joint.items()},
            {key: v01+v11 for key, (v01, _, v11) in joint.items()})


def third_rows(hist, joint, overlaps=None):
    rows = defaultdict(F)
    r, z = margins(joint)
    for hid, (a, words, h) in hist.items():
        p, pa, s = sum(a[:3]), sum(a[:4]), sum(a)
        D = (pa+1)*(pa+2)
        ha = share(a[4]+a[5], s)+F(a[4], D)
        groups = {(f, i, j): (f, int(i == j), words[i], words[j]) for f, i, j in EDGES}
        for (f, i, j), ge in groups.items():
            de = p+words[i][0]+words[j][1+f]+1
            re, ze, rze = r[hid, ge], z[hid, ge], joint[hid, ge][2]
            for (g, k, l), gf in groups.items():
                rf, zf = r[hid, gf], z[hid, gf]
                w = min(re, rf) if overlaps is None or ge == gf else overlaps[hid, *sorted((ge, gf))]
                assert 0 <= w <= min(re, rf)
                pat = partition((i, j, k, l))
                rows['Z-R', f, g, pat] += (ze-rf)/(pa+1)+(w-rze)/D
                rows['R-Z', f, g, pat] += (re-zf)/de
                rows['pair-RR', f, g, pat] += ha*h-(re+rf)/(pa+1)+w/D
    return rows


def table_matches(rows, names, table):
    assert rows.keys() <= set(names)
    assert all(rows[name] == table[str(name)] for name in names)


def counts(rows, names):
    values = [rows[key] for key in names]
    return sum(v < 0 for v in values), values.count(0), sum(v > 0 for v in values)


def load_joint(cols):
    states = defaultdict(list)
    for c in cols:
        if c['kind'] == 'joint-reply':
            states[c['hist_column_old'], freeze(c['group'])].append(F(c['weight']))
    return states


def fixed_211_joint(hists, old_r, r, sparse):
    rid_to_key = {rid: key for key, rid in old_r.items()}
    z = {}
    for rid, rbit, raw in sparse:
        assert rid in rid_to_key and rbit in (0, 1) and (rid, rbit) not in z
        z[rid, rbit] = F(raw)
        assert z[rid, rbit] > 0
    joint = {}
    for key, rid in old_r.items():
        h = hists[key[0]][2]
        v01, v11 = z.get((rid, 0), F(0)), z.get((rid, 1), F(0))
        assert 0 <= v01 <= h-r[key] and 0 <= v11 <= r[key]
        joint[key] = v01, r[key]-v11, v11
    assert margins(joint)[0] == r
    return joint


def replay():
    inputs = load_inputs()
    hist, old_r, (small, middle, large), (t1, t2, t3) = check_columns_and_rows(inputs)
    r1 = {key: F(small[rid]['weight']) for key, rid in old_r.items()}
    assert all(0 <= r <= hist[key[0]][2] and hist[key[0]][2]-r == t1[f'reply-upper:{old_r[key]}']
               for key, r in r1.items())
    K = F(small[0]['weight'])
    table_matches(first_rows(hist, r1, K), FIRST, t1)
    joint2, joint3 = map(load_joint, (middle, large))
    r2, r3 = margins(joint2)[0], margins(joint3)[0]
    assert sum(r1[key] != r2[key] for key in r1) == 16
    assert sum(r1[key] != r3[key] for key in r1) == 12
    assert sum(r2[key] != r3[key] for key in r1) == 16
    for joint, r, table in ((joint2, r2, t2), (joint3, r3, t3)):
        assert joint.keys() == old_r.keys()
        table_matches(first_rows(hist, r, K), FIRST, table)
        table_matches(second_rows(hist, joint, K), SECOND, table)
        for key, rid in old_r.items():
            assert hist[key[0]][2]-sum(joint[key]) == table[f'joint-state-upper:{rid}']
    large_hid = {i: hid for i, hid in zip((i for i, c in enumerate(large) if c['kind'] == 'hist'), hist)}
    overlap3 = {}
    for i, c in enumerate(large):
        if c['kind'] == 'overlap':
            hid = large_hid[c['hist_column']]
            ge, gf = freeze(c['groups'])
            w = F(c['weight'])
            overlap3[hid, ge, gf] = w
            assert all(r3[hid, g]-w == t3[f'overlap-upper:{i}:{g}'] for g in (ge, gf))
    assert len(overlap3) == 1306
    table_matches(third_rows(hist, joint3, overlap3), THIRD, t3)
    max_cross = third_rows(hist, joint2)
    assert counts(max_cross, THIRD) == (0, 54, 126)
    print('Frozen 599 point: exact min-overlap lift, 126 positive and 54 empty new rows')
    print('Original points: 78 joint-weight differences (599 vs 1905), R-marginal differences 16/12/16')

    certificates = json.loads((HERE / 'witnesses.json').read_bytes())
    for case, count in (('lift_599', 51), ('lift_1905', 53), ('strict_cut', 63)):
        assert len(certificates[case]) == count
        joint = fixed_211_joint(hist, old_r, r1, certificates[case])
        added = second_rows(hist, joint, K)
        assert len(added) == 56 and counts(added, SECOND) == (0, 8, 56)
        if case != 'lift_599':
            cross = third_rows(hist, joint)
            assert len(cross) == 126
            if case == 'lift_1905':
                assert counts(cross, THIRD) == (0, 54, 126)
            else:
                key = 'R-Z', 0, 0, (0, 1, 1, 0)
                # (i,j,k,l)=(i,j,j,i). This row is independent of overlap.
                z = margins(joint)[1]
                reversal = sum((r1[hid, (0, 0, words[i], words[j])]-z[hid, (0, 0, words[j], words[i])])
                               / (sum(a[:3])+words[i][0]+words[j][1]+1)
                               for hid, (a, words, _) in hist.items() for i, j in product(range(6), repeat=2)
                               if i != j)
                assert cross[key] == reversal == F(certificates['strict_slack']) < 0
        print(case, 'exact', certificates['strict_slack'] if case == 'strict_cut' else 'feasible')

    psi_path = ROOT / 'archives/customer-attraction/tools/evidence/tail3-B-projection-program/related/tail3_B_projection_certificate.json'
    psi_bytes = psi_path.read_bytes()
    psi = json.loads(psi_bytes)
    reported = inputs['thirteen-term-result.json']
    assert sha256(psi_bytes).hexdigest() == reported['projection_table_sha256']
    assert psi['old_point_sha256'] == '24a2f9fa7e7a47e26e065b41ada98e1788a5b448251fb8c1e881557c1f7c9f11'
    table = {(c['actual_bits'], c['d']): F(c['psi']) for c in psi['table']}
    assert len(table) == len(psi['table']) == 448
    terms = reported['terms']
    for term in terms:
        coefficient = table[term['actual_bits'], term['d']]
        assert F(term['psi']) == coefficient
        assert F(term['contribution']) == F(term['mass'])*coefficient
    assert len(terms) == 13 and sum(F(t['contribution']) for t in terms) == F(reported['exact_total']) > 0
    value = sum(h*table[''.join(map(str, a)), 1] for a, _, h in hist.values())
    assert value == F(psi['old_point_value']) == F(reported['mature_old_211_negative_value']) < 0
    print('Shared actual/d boundary excluded by independent psi:', value)


if __name__ == '__main__':
    replay()
