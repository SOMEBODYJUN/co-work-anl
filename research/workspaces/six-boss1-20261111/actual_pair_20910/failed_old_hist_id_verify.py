"""Independent literal/Boolean audit of the complete actual-source PAIR family.

No constructor, solver, previous evaluator or feature module is imported.
The verifier rebuilds action identities, all S6 images, actual source profits,
own-state moments, B4 joint moments, and the fixed linear upper rows directly.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
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
PSHA = 'cb45ee6f8df153764c91bd77d0543527cc44719ff7cc43646ffce06a7921a932'
MSHA = '96388092e21621f157b4428ce99f98b93afa99ed3a0c12c72b1d6475c26fba30'


def sha(p):
    return sha256(p.read_bytes()).hexdigest()


def read(p):
    if p.name.endswith('.gz'):
        with gzip.open(p, 'rt') as f:
            return json.load(f)
    return json.loads(p.read_text())


def freeze(v):
    return tuple(map(freeze, v)) if isinstance(v, list) else v


@lru_cache(maxsize=None)
def f(v):
    return Q(v)


def decode(items):
    result = {}
    for j, v in items:
        assert type(j) is int and 0 <= j < 4849 and j not in result
        a = f(v)
        assert a
        result[j] = a
    return result


def accumulate(row, other, scale):
    for j, v in other.items():
        row[j] = row.get(j, Q()) + scale*v
        if not row[j]:
            del row[j]


def evaluate(row, values):
    return sum((v*values[j] for j,v in row.items()), Q())


def serial(v):
    if isinstance(v, Q):
        return str(v)
    if isinstance(v, dict):
        return {str(k):serial(x) for k,x in v.items()}
    if isinstance(v, (tuple,list)):
        return [serial(x) for x in v]
    return v


def write(name, data):
    (HERE/name).write_text(json.dumps(serial(data), ensure_ascii=False, indent=2)+'\n')


def main():
    start = time.perf_counter()
    assert sha(POINT) == PSHA and sha(MATRIX) == MSHA
    point = read(POINT)
    columns = point['columns']
    values = [f(c['weight']) for c in columns]
    assert len(columns) == 20585 and min(values) >= 0
    labels_saved = read(HERE/'labels_and_orbits.json')
    rows_saved = read(HERE/'symbolic_rows.json.gz')
    freq_saved = read(HERE/'orbit_hist_frequencies.json.gz')
    summary = read(HERE/'build_summary.json')
    savedwallet = read(HERE/'hist_wallets.json')
    for data in (labels_saved, rows_saved, freq_saved, summary, savedwallet):
        assert data['point_sha256'] == PSHA

    # Action names and exact ordered histories, independently constructed.
    actions = [('A',i) for i in range(6)]
    actions += [(kind,i) for kind in ('T','B','C') for i in range(6)]
    nodes = [(fam,i,j) for fam in range(2) for i in range(6) for j in range(6)
             if fam == 1 or i != j]
    actions += [(kind,)+e for kind in ('R','Z') for e in nodes]
    actions += [('H',0),('H',1)]
    lookup = {a:i for i,a in enumerate(actions)}
    assert len(actions) == len(lookup) == 158
    assert [list(e) for e in nodes] == labels_saved['literal_node_order']
    names = []
    kinds = []
    for j,a in enumerate(actions):
        if a[0] in ('R','Z'):
            name = f'{a[0]}{a[1]}_{a[2]+1}_{a[3]+1}'
            kind = f'{a[0]}{a[1]}'
            indices = list(a[2:])
        else:
            name = f'{a[0]}{a[1]+1}'
            kind = name if a[0] in ('A','H') else a[0]
            indices = [] if a[0] in ('A','H') else [a[1]]
        l = labels_saved['labels'][j]
        assert (l['id'],l['name'],l['kind'],l['indices']) == (j,name,kind,indices)
        names.append(name)
        kinds.append(kind)
    assert labels_saved['no_D_labels'] and labels_saved['B4_third_bit_is_menu_mean_not_action']

    perms = tuple(permutations(range(6)))
    def moved(q, pi):
        a = actions[q]
        if a[0] in ('A','H'):
            return q
        if a[0] in ('T','B','C'):
            return lookup[a[0],pi[a[1]]]
        return lookup[a[0],a[1],pi[a[2]],pi[a[3]]]
    orbits = labels_saved['ordered_pair_orbits']
    assert len(orbits) == 490
    covered = set()
    s6checks = 0
    for oid,o in enumerate(orbits):
        assert o['id'] == oid
        q,r = o['representative']
        images = Counter((moved(q,pi),moved(r,pi)) for pi in perms)
        members = set(map(tuple,o['members']))
        assert members == set(images) and len(members) == o['size']
        assert set(images.values()) == {720//o['size']}
        assert not (members & covered)
        covered.update(members)
        for u,v in members:
            assert labels_saved['ordered_pair_orbit_index'][u][v] == oid
            s6checks += images[u,v]
        assert [names[q],names[r]] == o['representative_names']
    assert covered == set(product(range(158),repeat=2)) and s6checks == 490*720
    assert sum(q == r for q,r in covered) == 158

    # Parse exact moment columns directly, including all zero histograms.
    hist = {}
    own = defaultdict(dict)
    jointB4 = defaultdict(dict)
    current = None
    for j,c in enumerate(columns[:4849]):
        if c['kind'] == 'hist':
            current = j
            hist[j] = c
        elif c['kind'] == 'joint-reply':
            assert c['hist_column_old'] == current
            g = freeze(c['group'])
            own[current].setdefault(g,{})[tuple(c['state'])] = j
        elif c['kind'] == 'actual-B-family-state' and c['source'] == 4:
            assert c['ell'] in (0,6)
            state = tuple(c['hidden'])+(c['ell']//6,)
            assert state not in jointB4[c['hist_column']]
            jointB4[c['hist_column']][state] = j
    assert len(hist) == 16 and sum(len(d) for d in own.values()) == 194
    for h in hist:
        assert set(jointB4[h]) == set(product(range(2),repeat=3))
        assert sum(values[j] for j in jointB4[h].values()) == values[h]
        for g,d in own[h].items():
            assert set(d) == {(0,1),(1,0),(1,1)}
            assert sum(values[j] for j in d.values()) <= values[h]
    hist_ids = list(hist)
    assert len(freq_saved['records']) == 16*490
    savedfreq = {(r['hist_column'],r['orbit_id']):r for r in freq_saved['records']}
    assert len(savedfreq) == 16*490

    # Three genuine ICs plus the exact fifth-player self tax.
    proof_cases = 0
    for p in range(5):
        D = (p+1)*(p+2)
        def U(t,r):
            return Q(t,p+t+r) if t else Q()
        for a,b,t,s,v in product(range(2),repeat=5):
            wallet_bit = U(a,b)+U(b,a)+Q(a,D)
            target = Q(t+s,p+1)-Q(t*s,D)
            delta1 = U(a,b)-U(t,v)
            delta2 = U(v,t)-U(s,t)
            delta3 = U(b,a)-U(v,a)
            assert wallet_bit-target == delta1+delta2+delta3+Q(a*(1-v),D)
            proof_cases += 1
    assert proof_cases == 160
    wallet = {}
    u5 = u6 = tax = Q()
    for h,c in hist.items():
        a = tuple(map(int,c['actual_bits']))
        P = sum(a[:4]); D = (P+1)*(P+2)
        cross = Q(a[4]*a[5],D)
        fifth = Q(a[4],P+1)-cross
        sixth = Q(a[5],P+1)-cross
        t = Q(a[4],D)
        cwallet = fifth+sixth+t
        total = sum(a)
        assert fifth == (Q(a[4],total) if a[4] else Q())
        assert sixth == (Q(a[5],total) if a[5] else Q())
        if cwallet:
            wallet[h] = cwallet
        u5 += fifth*values[h]; u6 += sixth*values[h]; tax += t*values[h]
    assert wallet == decode(savedwallet['wallet_sparse_original4849'])
    assert [u5,u6,tax] == [f(savedwallet[k]) for k in ('u5','u6','self_tax')]
    fullwallet = u5+u6+tax
    assert fullwallet == f(savedwallet['wallet'])

    rebuilt = [dict(wallet) for _ in orbits]
    queryprices = [[Q(),Q()] for _ in orbits]
    overlaps = [Q() for _ in orbits]
    degreechecks = 0
    cellchecks = 0
    expanded_boolean_checks = 0
    truth_tables = {}

    for h,c in hist.items():
        a = tuple(map(int,c['actual_bits']))
        P = sum(a[:4]); D = (P+1)*(P+2)
        words = []
        for w,n in zip(product(range(2),repeat=3),c['hist']):
            words.extend([w]*n)
        assert len(words) == 6
        tokens = []
        marg = {}
        eligible = defaultdict(list)
        for q,action in enumerate(actions):
            k = action[0]
            if k == 'A':
                token = ('bit',a[action[1]])
            elif k in ('T','B','C'):
                token = ('bit',words[action[1]][('T','B','C').index(k)])
            elif k in ('R','Z'):
                fam,i,j = action[1:]
                token = ('own',int(k=='Z'),(fam,int(i==j),words[i],words[j]))
            else:
                token = ('B4',action[1])
            tokens.append(token)
            eligible[token].append(q)
            if token[0] == 'bit':
                marg[token] = {h:Q(1)} if token[1] else {}
            elif token[0] == 'own':
                marg[token] = {j:Q(1) for s,j in own[h][token[2]].items() if s[token[1]]}
            else:
                marg[token] = {j:Q(1) for s,j in jointB4[h].items() if s[token[1]]}
        masses = {t:evaluate(row,values) for t,row in marg.items()}

        def classify(q,r):
            tq,tr = tokens[q],tokens[r]
            if q == r:
                return 'identical-label'
            if tq[0] == tr[0] == 'bit':
                return 'two-static-bits'
            if tq[0] == 'bit' or tr[0] == 'bit':
                return 'static-times-marginal'
            if actions[q][0] in ('R','Z') and actions[r][0] in ('R','Z') and actions[q][1:] == actions[r][1:]:
                return 'same-node-own-RZ'
            if actions[q][0] == actions[r][0] == 'H':
                return 'same-B4-joint'
            return 'unknown-Frechet'

        for oid,o in enumerate(orbits):
            grouped = defaultdict(list)
            for q,r in o['members']:
                grouped[tokens[q],tokens[r],classify(q,r)].append((q,r))
            records = savedfreq[h,oid]['groups']
            recorded = {(freeze(g['q_token']),freeze(g['r_token']),g['rule']):g for g in records}
            assert set(recorded) == set(grouped) and len(recorded) == len(records)
            assert sum(g['S6_frequency'] for g in records) == 720
            for key,members in grouped.items():
                tq,tr,rule = key
                rec = recorded[key]
                assert set(map(tuple,rec['pair_members'])) == set(members)
                number = len(members)
                count720 = number*(720//len(o['members']))
                assert rec['literal_pair_count'] == number and rec['S6_frequency'] == count720
                weight = Q(count720,720)
                assert weight == f(rec['orbit_average'])
                assert decode(rec['q_marginal']) == marg[tq]
                assert decode(rec['r_marginal']) == marg[tr]
                assert f(rec['q_value']) == masses[tq] and f(rec['r_value']) == masses[tr]
                for side,token in enumerate((tq,tr)):
                    if token[0] == 'bit':
                        continue
                    counts = Counter(p[side] for p in members)
                    group_labels = [q for q in eligible[token] if kinds[q] == kinds[members[0][side]]]
                    assert set(counts) == set(group_labels)
                    assert set(counts.values()) == {Q(number,len(group_labels))}
                    # This is a symbolic coefficient check on arbitrary literal
                    # membership variables, not a same-word-equals-label claim.
                    for q in group_labels:
                        assert Q(counts[q],len(o['members'])) == weight/Q(len(group_labels))
                        degreechecks += 1
                choice = rec['chosen_side']
                if rule == 'identical-label':
                    overlap = marg[tq]
                elif rule == 'two-static-bits':
                    overlap = {h:Q(1)} if tq[1]*tr[1] else {}
                elif rule == 'static-times-marginal':
                    bit,other = (tq,tr) if tq[0] == 'bit' else (tr,tq)
                    overlap = marg[other] if bit[1] else {}
                elif rule == 'same-node-own-RZ':
                    overlap = {own[h][tq[2]][1,1]:Q(1)}
                elif rule == 'same-B4-joint':
                    overlap = {j:Q(1) for s,j in jointB4[h].items() if s[0]*s[1]}
                else:
                    assert choice in ('q','r')
                    overlap = marg[tq] if choice == 'q' else marg[tr]
                    assert evaluate(overlap,values) == min(masses[tq],masses[tr])
                assert decode(rec['chosen_overlap']) == overlap
                assert evaluate(overlap,values) == f(rec['overlap_value'])
                if rule != 'unknown-Frechet':
                    assert choice is None

                # Enumerate ALL Boolean states of the exact parent sources.
                # Two different R/Z parents get 4x4 states; R/Z and B4 get
                # 4x8; shared parents are evaluated on their one joint state.
                q0,r0 = members[0]
                parents = []
                def parent(q):
                    ac = actions[q]
                    if ac[0] in ('R','Z'):
                        return ('own',)+ac[1:]
                    if ac[0] == 'H':
                        return ('B4',)
                    return None
                pq,pr = parent(q0),parent(r0)
                for p in (pq,pr):
                    if p is not None and p not in parents:
                        parents.append(p)
                parent_sizes = tuple(2 if p[0]=='own' else 3 for p in parents)
                qrole = None if pq is None else parents.index(pq)
                rrole = None if pr is None else parents.index(pr)
                semantic = (P,rule,tq[:2],tr[:2],qrole,rrole,parent_sizes,choice)
                if semantic not in truth_tables:
                    table = []
                    domains = [tuple(product(range(2),repeat=n)) for n in parent_sizes]
                    for state in product(*domains):
                        qb = tq[1] if pq is None else state[qrole][tq[1]]
                        rb = tr[1] if pr is None else state[rrole][tr[1]]
                        ob = qb*rb if rule != 'unknown-Frechet' else (qb if choice=='q' else rb)
                        gap = Q(ob-qb*rb,D)
                        assert gap >= 0
                        if rule != 'unknown-Frechet':
                            assert gap == 0
                        table.append(dict(parent_states=state,q=qb,r=rb,
                                          exact_intersection=qb*rb,linear_upper_bit=ob,gap=gap))
                    truth_tables[semantic] = table
                expanded_boolean_checks += len(truth_tables[semantic])

                accumulate(rebuilt[oid],marg[tq],-weight/Q(P+1))
                accumulate(rebuilt[oid],marg[tr],-weight/Q(P+1))
                accumulate(rebuilt[oid],overlap,weight/Q(D))
                queryprices[oid][0] += weight*masses[tq]/Q(P+1)
                queryprices[oid][1] += weight*masses[tr]/Q(P+1)
                overlaps[oid] += weight*evaluate(overlap,values)/Q(D)
                cellchecks += 1
        print(json.dumps(dict(stage='independent_literal_hist',hist_column=h,
                              elapsed_seconds=time.perf_counter()-start)),flush=True)
    assert degreechecks == freq_saved['random_degree_checks']
    assert rows_saved['original_columns'] == 4849 and rows_saved['full_matrix_columns'] == 20585
    assert rows_saved['auxiliary_zero_range'] == [4849,20585]
    assert len(rows_saved['rows']) == 490
    exact = []
    for oid,saved in enumerate(rows_saved['rows']):
        assert saved['orbit_id'] == oid and saved['auxiliary_coefficients_all_zero']
        assert rebuilt[oid] == decode(saved['sparse_original4849_row'])
        lhs = fullwallet-queryprices[oid][0]-queryprices[oid][1]+overlaps[oid]
        assert lhs == evaluate(rebuilt[oid],values) == f(saved['exact_slack'])
        exact.append(lhs)
    assert min(exact) == f(summary['minimum_slack'])
    minimum_ids = [i for i,v in enumerate(exact) if v == min(exact)]
    assert minimum_ids == summary['minimum_orbits']
    negatives = [i for i,v in enumerate(exact) if v<0]
    assert negatives == summary['negative_orbits']
    for oid,v in enumerate(exact):
        assert v == exact[orbits[oid]['reversed_orbit']]
    write('boolean_upper_audit.json',dict(status='PASS',three_IC_plus_self_tax_cases=proof_cases,
          unique_local_truth_tables=len(truth_tables),unique_boolean_cases=sum(map(len,truth_tables.values())),
          expanded_hist_orbit_boolean_cases=expanded_boolean_checks,
          tables=[dict(pattern=k,truth_table=v) for k,v in truth_tables.items()],
          independent_parent_states_are_enumerated_only_for_a_pointwise_upper_bound=True,
          no_common_Frechet_realization_asserted=True))

    # Verify every claimed proportional duplicate, and independently scan all
    # existing rows to certify absence of other proportional copies.
    del freq_saved,savedfreq
    matrix = read(MATRIX)
    assert len(matrix['rows']) == 20910 and len(matrix['columns']) == 20585
    assert matrix['columns'] == [{k:v for k,v in c.items() if k!='weight'} for c in columns]
    def ray(row):
        if not row:
            return ()
        lead = min(row)
        scale = abs(row[lead])
        return tuple((j,v/scale) for j,v in sorted(row.items()))
    targets = defaultdict(list)
    for i,r in enumerate(rebuilt):
        targets[ray(r)].append(i)
    found = defaultdict(list)
    original_only = 0
    for i,r in enumerate(matrix['rows']):
        if any(j>=4849 for j,v in r):
            continue
        original_only += 1
        row = {j:f(v) for j,v in r}
        key = ray(row)
        if key in targets:
            for oid in targets[key]:
                scale = rebuilt[oid][min(row)]/row[min(row)] if row else None
                if row:
                    assert scale > 0 and rebuilt[oid] == {j:v*scale for j,v in row.items()}
                found[oid].append(dict(matrix_row=i,matrix_row_name=matrix['row_names'][i],
                                      multiplier_of_matrix_row=None if scale is None else str(scale),
                                      both_identically_zero=not row))
    compared = read(HERE/'matrix_positive_proportional_comparison.json')
    assert compared['matrix_sha256'] == MSHA and compared['no_linear_independence_claim']
    assert compared['all_original_coordinate_rows'] == original_only
    for rec in compared['matches']:
        assert rec['existing_rows'] == found.get(rec['orbit_id'],[])
    assert compared['orbits_with_existing_positive_proportional_copy'] == sorted(found)
    assert compared['distinct_nonzero_positive_rays'] == sum(bool(k) for k in targets)
    family = read(HERE/'family_summary.json')
    for rec in family['rows']:
        ids = [i for i,o in enumerate(orbits) if [kinds[q] for q in o['representative']] == rec['kinds']]
        assert len(ids) == rec['orbit_count']
        assert sum(orbits[i]['size'] for i in ids) == rec['literal_ordered_pairs']
        m = min(exact[i] for i in ids)
        assert m == f(rec['minimum_slack']) and rec['minimizers'] == [i for i in ids if exact[i]==m]
    output = dict(status='PASS',point_sha256=PSHA,matrix_sha256=MSHA,
          label_count=158,ordered_pair_orbits=490,literal_ordered_pairs=158**2,
          full_S6_images_checked=s6checks,histograms=16,zero_mass_histograms=sum(values[h]==0 for h in hist),
          literal_hist_pair_occurrences=16*158**2,hist_orbit_groups_checked=cellchecks,
          group_marginal_symbolic_degree_checks=degreechecks,
          three_IC_plus_tax_Boolean_cases=proof_cases,unknown_and_known_Boolean_cases=expanded_boolean_checks,
          source_u5=u5,source_u6=u6,source_self_tax=tax,source_wallet=fullwallet,
          all4849_symbolic_coefficients_checked=True,all15736_auxiliary_coefficients_zero=True,
          all490_exact_slacks_checked=True,negative_orbits=negatives,
          minimum_slack=min(exact),minimum_slack_float=float(min(exact)),minimum_orbits=minimum_ids,
          minimum_names=[orbits[i]['representative_names'] for i in minimum_ids],
          distinct_nonzero_positive_rays=sum(bool(k) for k in targets),
          existing_positive_proportional_copy_orbits=sorted(found),
          exact_orbit_values=[dict(orbit_id=i,q_price=queryprices[i][0],r_price=queryprices[i][1],
                                  overlap_upper_credit=overlaps[i],slack=v) for i,v in enumerate(exact)],
          elapsed_seconds=time.perf_counter()-start,optimizer_calls=0,
          interpretation='Closed only this complete named-query strong PAIR family at the one actual source; all unknown overlaps are necessary upper bounds, not a joint realization; six-player half remains OPEN.')
    write('independent_verification.json',output)
    print(json.dumps(serial({k:v for k,v in output.items() if k!='exact_orbit_values'}),ensure_ascii=False,indent=2),flush=True)


if __name__ == '__main__':
    main()
