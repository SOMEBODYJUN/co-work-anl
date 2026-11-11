"""All named-query strong PAIR rows at the single actual four-prefix source.

This file only writes its own directory.  No optimizer or strategy search is
used.  Hist, own R/Z states and the one B4 joint state are parsed directly
from the pinned 20910-row exact point.  Unknown intersections are bounded
after complete S6-orbit aggregation, with a fixed linear marginal choice.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import permutations, product
from pathlib import Path
import gzip
import json
import time

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
POINT = WORK / 'full624_augmented_lp/recovery/augmented_lp_exact.json'
MATRIX = WORK / 'full624_augmented_lp/recovery/exact_matrix.json.gz'
POINT_SHA = 'cb45ee6f8df153764c91bd77d0543527cc44719ff7cc43646ffce06a7921a932'
MATRIX_SHA = '96388092e21621f157b4428ce99f98b93afa99ed3a0c12c72b1d6475c26fba30'
Q = 4849
N = 20585
STATES = tuple(product(range(2), repeat=2))
WORDS = tuple(product(range(2), repeat=3))


def sha(p):
    return sha256(p.read_bytes()).hexdigest()


def serial(v):
    if isinstance(v, F):
        return str(v)
    if isinstance(v, dict):
        return {str(k): serial(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [serial(x) for x in v]
    return v


def save(name, data):
    text = json.dumps(serial(data), ensure_ascii=False, indent=2) + '\n'
    if name.endswith('.gz'):
        with (HERE / name).open('wb') as raw:
            with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0) as f:
                f.write(text.encode())
    else:
        (HERE / name).write_text(text)


def add(row, j, value):
    if value:
        row[j] = row.get(j, F()) + value
        if not row[j]:
            del row[j]


def addrow(row, other, scale=F(1)):
    for j, a in other.items():
        add(row, j, a * scale)


def sparse(row):
    return [[j, str(v)] for j, v in sorted(row.items()) if v]


def dot(row, x):
    return sum((v * x[j] for j, v in row.items() if x[j]), F())


def labels_and_orbits():
    labels = []

    def addlabel(name, kind, indices=(), **data):
        labels.append(dict(id=len(labels), name=name, kind=kind,
                           indices=list(indices), **data))

    for i in range(6):
        addlabel(f'A{i+1}', f'A{i+1}', actual_position=i,
                 definition=f'actual action at player {i+1}')
    for kind, k in [('T', 0), ('B', 1), ('C', 2)]:
        for i in range(6):
            addlabel(f'{kind}{i+1}', kind, (i,), word_slot=k,
                     definition={'T': 'legal optimal-menu label T_i',
                                 'B': 'sigma5(A1,A2,A3,T_i)',
                                 'C': 'sigma6(A1,A2,A3,T_i,B_i)'}[kind])
    nodes = [e for e in product(range(2), range(6), range(6)) if e[0] or e[1] != e[2]]
    for kind in ('R', 'Z'):
        for e, (family, i, j) in enumerate(nodes):
            addlabel(f'{kind}{family}_{i+1}_{j+1}', f'{kind}{family}', (i, j),
                     family=family, node_index=e, node=[family, i, j],
                     own_coordinate=0 if kind == 'R' else 1,
                     definition=('sigma6(A1,A2,A3,T_i,' + ('B_j' if family == 0 else 'C_j') + ')'
                                 if kind == 'R' else 'sigma6(A1,A2,A3,A4,R_(family,i,j))'))
    for i in range(2):
        addlabel(f'H{i+1}', f'H{i+1}', B4_coordinate=i,
                 definition=('sigma5(A1,A2,A3,A6)' if i == 0 else 'sigma6(A1,A2,A3,A6,H1)'))
    assert len(labels) == 158 and len({l['name'] for l in labels}) == 158

    def signature(ids):
        mapping = {}
        return tuple((labels[q]['kind'], tuple(mapping.setdefault(i, len(mapping))
                                                for i in labels[q]['indices'])) for q in ids)

    orbits, bysig, pairmap = [], {}, []
    for q in range(158):
        row = []
        for r in range(158):
            key = signature((q, r))
            if key not in bysig:
                bysig[key] = len(orbits)
                orbits.append(dict(id=len(orbits), signature=key, representative=[q, r], members=[]))
            o = bysig[key]
            orbits[o]['members'].append([q, r])
            row.append(o)
        pairmap.append(row)
    assert len(orbits) == 490 and sum(len(o['members']) for o in orbits) == 158**2
    for o in orbits:
        o['size'] = len(o['members'])
        o['S6_repetitions_per_member'] = 720 // o['size']
        assert 720 % o['size'] == 0
        o['representative_names'] = [labels[i]['name'] for i in o['representative']]
        o['reversed_orbit'] = pairmap[o['representative'][1]][o['representative'][0]]
    return labels, nodes, orbits, pairmap


def main():
    started = time.perf_counter()
    assert sha(POINT) == POINT_SHA and sha(MATRIX) == MATRIX_SHA
    point = json.loads(POINT.read_text())
    columns = point['columns']
    assert len(columns) == N and point['original_columns'] == Q
    x = [F(c['weight']) for c in columns]
    assert min(x) >= 0
    hist, own, b4 = {}, defaultdict(dict), defaultdict(list)
    current = None
    for j, c in enumerate(columns[:Q]):
        if c['kind'] == 'hist':
            current = j
            hist[j] = c
        elif c['kind'] == 'joint-reply':
            f, same, wi, wj = c['group']
            g = (f, same, tuple(wi), tuple(wj))
            own[current].setdefault(g, {})[tuple(c['state'])] = j
        elif c['kind'] == 'actual-B-family-state' and c['source'] == 4:
            b4[c['hist_column']].append(j)
    assert len(hist) == 16 and sum(map(len, own.values())) == 194
    for h in hist:
        assert len(b4[h]) == 8 and sum((x[j] for j in b4[h]), F()) == x[h]
        for d in own[h].values():
            assert set(d) == set(STATES[1:])
            assert sum((x[j] for j in d.values()), F()) <= x[h]

    labels, nodes, orbits, pairmap = labels_and_orbits()
    wallet = {}
    u5 = u6 = tax = F()
    hist_metadata = []
    for h, c in hist.items():
        a = tuple(map(int, c['actual_bits']))
        P, load = sum(a[:4]), sum(a)
        uc = F(a[4] + a[5], load) if load else F()
        tc = F(a[4], (P+1)*(P+2))
        wallet[h] = uc + tc
        u5 += x[h] * (F(a[4], load) if load else F())
        u6 += x[h] * (F(a[5], load) if load else F())
        tax += x[h] * tc
        hist_metadata.append(dict(hist_column=h, actual_bits=c['actual_bits'], hist=c['hist'],
                                  prefix_load=P, actual_total_load=load, mass=x[h],
                                  wallet_coefficient=uc+tc, u5_u6_coefficient=uc, self_tax_coefficient=tc))
    wallet_value = dot(wallet, x)
    assert wallet_value == u5+u6+tax
    rows = [dict(wallet) for _ in orbits]
    expected_values = [wallet_value for _ in orbits]
    frequencies = []
    rule_counts = Counter()
    choice_counts = Counter()
    degree_checks = 0

    for h, c in hist.items():
        a = tuple(map(int, c['actual_bits']))
        P = sum(a[:4])
        words = tuple(w for w, n in zip(WORDS, c['hist']) for _ in range(n))
        assert len(words) == 6
        tokens = []
        marginal, kind, local_labels = {}, {}, defaultdict(list)
        for label in labels:
            q = label['id']
            if 'actual_position' in label:
                tok = ('bit', a[label['actual_position']])
            elif 'word_slot' in label:
                tok = ('bit', words[label['indices'][0]][label['word_slot']])
            elif 'node' in label:
                f, i, j = label['node']
                g = (f, int(i == j), words[i], words[j])
                tok = ('own', label['own_coordinate'], g)
            else:
                tok = ('B4', label['B4_coordinate'])
            tokens.append(tok)
            local_labels[tok].append(q)
            if tok not in marginal:
                if tok[0] == 'bit':
                    marginal[tok] = {h: F(tok[1])} if tok[1] else {}
                elif tok[0] == 'own':
                    marginal[tok] = {j: F(1) for s, j in own[h][tok[2]].items() if s[tok[1]]}
                else:
                    marginal[tok] = {j: F(1) for j in b4[h] if columns[j]['hidden'][tok[1]]}
        values = {t: dot(m, x) for t, m in marginal.items()}

        def pair_rule(q, r):
            tq, tr = tokens[q], tokens[r]
            if q == r:
                return 'identical-label'
            if tq[0] == 'bit' and tr[0] == 'bit':
                return 'two-static-bits'
            if tq[0] == 'bit' or tr[0] == 'bit':
                return 'static-times-marginal'
            if 'node' in labels[q] and 'node' in labels[r] and labels[q]['node'] == labels[r]['node']:
                assert tq[0] == tr[0] == 'own' and tq[1] != tr[1]
                return 'same-node-own-RZ'
            if tq[0] == tr[0] == 'B4':
                assert tq[1] != tr[1]
                return 'same-B4-joint'
            return 'unknown-Frechet'

        for o in orbits:
            oid, total = o['id'], o['size']
            groups = defaultdict(list)
            for q, r in o['members']:
                groups[(tokens[q], tokens[r], pair_rule(q, r))].append((q, r))
            records = []
            for (tq, tr, rule), members in sorted(groups.items(), key=lambda kv: repr(kv[0])):
                number = len(members)
                alpha = F(number, total)
                s6count = number * o['S6_repetitions_per_member']
                assert F(s6count, 720) == alpha
                # Every random literal label of a descriptor group occurs with
                # the same degree.  Thus the group average really is the exact
                # orbit marginal, even with extra queried index/word conditions.
                degrees = []
                for side, token in enumerate((tq, tr)):
                    if token[0] != 'bit':
                        dc = Counter(pair[side] for pair in members)
                        eligible = [i for i in local_labels[token] if labels[i]['kind'] == labels[members[0][side]]['kind']]
                        counts = [dc.get(i, 0) for i in eligible]
                        assert counts and min(counts) == max(counts) > 0, (h, oid, token, counts)
                        degree_checks += len(counts)
                        degrees.append(dict(side=side, eligible_label_ids=eligible,
                                            degree=counts[0], total_occurrences=sum(counts)))
                mq, mr = marginal[tq], marginal[tr]
                choice = None
                if rule == 'identical-label':
                    overlap = mq
                elif rule == 'two-static-bits':
                    overlap = {h: F(tq[1]*tr[1])} if tq[1]*tr[1] else {}
                elif rule == 'static-times-marginal':
                    tb, tm = (tq, tr) if tq[0] == 'bit' else (tr, tq)
                    overlap = marginal[tm] if tb[1] else {}
                elif rule == 'same-node-own-RZ':
                    assert tq[2] == tr[2]
                    overlap = {own[h][tq[2]][1, 1]: F(1)}
                elif rule == 'same-B4-joint':
                    overlap = {j: F(1) for j in b4[h] if columns[j]['hidden'] == [1, 1]}
                else:
                    vq, vr = values[tq], values[tr]
                    if vq < vr:
                        choice = 'q'
                    elif vr < vq:
                        choice = 'r'
                    else:
                        # Use a reversal-invariant symbolic tie break.  Equal
                        # current values never mean equal labels/events.
                        choice = 'q' if sparse(mq) <= sparse(mr) else 'r'
                    overlap = mq if choice == 'q' else mr
                    assert dot(overlap, x) == min(vq, vr)
                    choice_counts[(choice, 'tie' if vq == vr else 'strict')] += 1
                ov = dot(overlap, x)
                addrow(rows[oid], mq, -alpha/F(P+1))
                addrow(rows[oid], mr, -alpha/F(P+1))
                addrow(rows[oid], overlap, alpha/F((P+1)*(P+2)))
                expected_values[oid] += alpha * (-(values[tq]+values[tr])/F(P+1) + ov/F((P+1)*(P+2)))
                rule_counts[rule] += number
                records.append(dict(q_token=tq, r_token=tr, rule=rule, literal_pair_count=number,
                                    S6_frequency=s6count, orbit_average=alpha, pair_members=members,
                                    q_marginal=sparse(mq), r_marginal=sparse(mr),
                                    chosen_overlap=sparse(overlap), chosen_side=choice,
                                    q_value=values[tq], r_value=values[tr], overlap_value=ov,
                                    random_marginal_degree_certificates=degrees))
            assert sum(r['literal_pair_count'] for r in records) == total
            assert sum(r['S6_frequency'] for r in records) == 720
            frequencies.append(dict(hist_column=h, orbit_id=oid, groups=records))
        print(json.dumps(dict(stage='hist_exact_pair_orbits', hist_column=h,
                              elapsed_seconds=time.perf_counter()-started)), flush=True)

    evaluated = [dot(row, x) for row in rows]
    assert evaluated == expected_values
    assert all(evaluated[o['id']] == evaluated[o['reversed_orbit']] for o in orbits)
    negative = [i for i, value in enumerate(evaluated) if value < 0]
    minimum = min(evaluated)
    minimizers = [i for i, value in enumerate(evaluated) if value == minimum]
    row_records = []
    for o, row, value in zip(orbits, rows, evaluated):
        row_records.append(dict(orbit_id=o['id'], representative=o['representative'],
                                representative_names=o['representative_names'], orbit_size=o['size'],
                                sparse_original4849_row=sparse(row), exact_slack=value,
                                slack_float=float(value), auxiliary_coefficients_all_zero=True))
    save('labels_and_orbits.json', dict(point_sha256=POINT_SHA, label_count=158, labels=labels,
         counts_by_kind=dict(Counter(d['kind'] for d in labels)), literal_node_order=nodes,
         permutation_convention='old slot i moves to pi(i); move T/B/C and both R/Z indices simultaneously; A and H fixed',
         no_D_labels=True, B4_third_bit_is_menu_mean_not_action=True,
         omitted_alias='R_(0,i,i) is C_i by its exact ordered history; the 30 off-diagonal R0 nodes are retained',
         same_word_does_not_mean_same_label=True, repeated_queries_included=True,
         ordered_pair_orbits=orbits, ordered_pair_orbit_index=pairmap))
    save('hist_wallets.json', dict(point_sha256=POINT_SHA, source=['A1','A2','A3','A4'],
         actual_tail=['A5','A6'], u5=u5, u6=u6, self_tax=tax, wallet=wallet_value,
         wallet_sparse_original4849=sparse(wallet), hist_records=hist_metadata))
    save('orbit_hist_frequencies.json.gz', dict(point_sha256=POINT_SHA, permutation_count=720,
         ordered_orbit_count=len(orbits), random_degree_checks=degree_checks, records=frequencies))
    save('symbolic_rows.json.gz', dict(point_sha256=POINT_SHA, original_columns=Q,
         full_matrix_columns=N, auxiliary_zero_range=[Q,N], rows=row_records))
    for i in negative:
        record = dict(row_records[i])
        record['dense_original4849_row'] = [str(rows[i].get(j, F())) for j in range(Q)]
        record['point_sha256'] = POINT_SHA
        record['source_wallet'] = 'actual u5 + actual u6 + sum a5/((P+1)(P+2))'
        record['fixed_overlap_choices'] = [r for r in frequencies if r['orbit_id'] == i]
        save(f'negative_orbit_{i}.json', record)
    save('summary_before_matrix_comparison.json', dict(point_sha256=POINT_SHA,
         ordered_pair_orbits=len(orbits), literal_ordered_pairs=158**2,
         zero_orbits=sum(v == 0 for v in evaluated), negative_orbits=negative,
         minimum_slack=minimum, minimum_slack_float=float(minimum), minimum_orbits=minimizers,
         minimum_pairs=[orbits[i]['representative_names'] for i in minimizers],
         wallet=wallet_value, u5=u5, u6=u6, self_tax=tax,
         all_family_rows_nonnegative=not negative, rule_literal_counts=dict(rule_counts),
         unknown_choices={str(k):v for k,v in choice_counts.items()}, optimizer_calls=0))
    print(json.dumps(serial(dict(stage='COMPLETE_EXACT_FAMILY', negatives=negative,
         minimum=minimum, minimum_float=float(minimum), minimizers=minimizers,
         minimum_pairs=[orbits[i]['representative_names'] for i in minimizers])), ensure_ascii=False), flush=True)

    @lru_cache(maxsize=None)
    def rat(s):
        return F(s)

    def ray(row):
        if not row:
            return ()
        sortedrow = sorted(row.items())
        scale = abs(sortedrow[0][1])
        return tuple((j, v/scale) for j, v in sortedrow)

    target_rays = defaultdict(list)
    for i, row in enumerate(rows):
        target_rays[ray(row)].append(i)
    matches = defaultdict(list)
    with gzip.open(MATRIX, 'rt') as f:
        matrix = json.load(f)
    assert len(matrix['rows']) == 20910 and len(matrix['columns']) == N
    assert [{k:v for k,v in c.items() if k != 'weight'} for c in columns] == matrix['columns']
    eligible = 0
    for i, r in enumerate(matrix['rows']):
        if any(j >= Q for j, _ in r):
            continue
        eligible += 1
        row = {j:rat(v) for j,v in r}
        k = ray(row)
        if k in target_rays:
            for oid in target_rays[k]:
                scale = next(iter(rows[oid].values())) if False else None
                if row:
                    j = min(row)
                    scale = rows[oid][j]/row[j]
                    assert scale > 0 and rows[oid] == {jj:vv*scale for jj,vv in row.items()}
                matches[oid].append(dict(matrix_row=i, matrix_row_name=matrix['row_names'][i],
                                         multiplier_of_matrix_row=scale, both_identically_zero=not row))
    duplicates = [v for v in target_rays.values() if len(v)>1]
    save('matrix_positive_proportional_comparison.json', dict(matrix_sha256=MATRIX_SHA,
         matrix_rows_checked=20910, all_original_coordinate_rows=eligible,
         distinct_nonzero_positive_rays=sum(bool(k) for k in target_rays),
         internal_positive_proportional_classes=duplicates,
         matches=[dict(orbit_id=i, existing_rows=matches.get(i, [])) for i in range(len(orbits))],
         orbits_with_existing_positive_proportional_copy=sorted(matches),
         no_linear_independence_claim=True))
    family = defaultdict(list)
    for o in orbits:
        q, r = o['representative']
        family[(labels[q]['kind'],labels[r]['kind'])].append(o['id'])
    family_records = []
    for key, ids in sorted(family.items()):
        v = min(evaluated[i] for i in ids)
        family_records.append(dict(kinds=key, orbit_count=len(ids),
             literal_ordered_pairs=sum(orbits[i]['size'] for i in ids), minimum_slack=v,
             minimum_slack_float=float(v), minimizers=[i for i in ids if evaluated[i] == v],
             negative_orbits=[i for i in ids if evaluated[i] < 0]))
    save('family_summary.json', dict(point_sha256=POINT_SHA, rows=family_records))
    save('build_summary.json', dict(status='NEGATIVE_NECESSARY_ROW_FOUND' if negative else 'ALL_SINGLE_SOURCE_PAIR_ROWS_NONNEGATIVE',
         point_sha256=POINT_SHA, matrix_sha256=MATRIX_SHA, labels=158, histograms=16,
         ordered_pair_orbits=490, literal_ordered_pairs=158**2, zero_orbits=sum(v==0 for v in evaluated),
         negative_orbits=negative, minimum_slack=minimum, minimum_slack_float=float(minimum),
         minimum_orbits=minimizers, minimum_pairs=[orbits[i]['representative_names'] for i in minimizers],
         distinct_nonzero_positive_rays=sum(bool(k) for k in target_rays),
         existing_copy_orbits=sorted(matches), wallet=wallet_value, source_u5=u5, source_u6=u6, self_tax=tax,
         exact_Fraction_arithmetic=True, optimizer_calls=0, elapsed_seconds=time.perf_counter()-started,
         scope='Only the complete 158-label strong PAIR family at the one actual four-prefix source; no SPE completion or six-player half theorem.'))
    print(json.dumps(serial(dict(stage='FINISHED', elapsed_seconds=time.perf_counter()-started,
         negative_orbits=negative, minimum_slack=minimum, distinct_nonzero_positive_rays=sum(bool(k) for k in target_rays),
         existing_copy_orbit_count=len(matches))), ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
