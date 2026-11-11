#!/usr/bin/env python3
"""Instantiate the existing arbitrary-anchor AP theorem at actual players 1--3.

All point-free inputs are read-only.  The full 21021 descriptors, 158 literal
labels, S6 frequencies and raw old marginal definitions are used directly.
No optimizer, old point file, point weights, or frozen-matrix write is used.
Every output stays in this directory.  Run with -B; --freeze only seals output.
"""

from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations, product
from pathlib import Path
import gzip
import io
import json
import sys

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = WORK.parents[2]
RAW = REPO / ('archives/customer-attraction/tools/evidence/'
              'background-bns-and-ap-primary/original/research/workspaces/'
              'customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/'
              'credible_counterexample')
FILES = {
    'matrix': WORK / 'maxb_augmented_lp/full_lift/exact_matrix.json.gz',
    'lift': WORK / 'terminal_response_cycles/max_b_symbolic_lift.json',
    'labels': WORK / 'actual_pair_20910/labels_and_orbits.json',
    'h3_rows': WORK / 'maxb_h3_bridge/rows_17.json',
    'h3_audit': WORK / 'maxb_h3_audit/audit_result.json',
    'model': REPO / 'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md',
    'AP_object': REPO / 'archives/customer-attraction/state/引理/任意背景加权近饱和交换与统一锚主题上界--引理.md',
    'AP_version_resource': REPO / 'archives/customer-attraction/state/资源/背景BNS与AP的版本身份及固定支持有限声明--资源.md',
    'original_proof': RAW / 'background_near_saturation.md',
    'original_claims': RAW / 'CLAIMS.md',
    'original_readme': RAW / 'README.md',
}
PINS = {
    'matrix': 'c054aadf745ea4540233a3da693917498527d19d4ccecb0fdd34ad884e461e4b',
    'lift': '52129dc848cf47f569f61442962a01aec61c6317531be0d24837d41071c96a5c',
    'original_proof': 'f7f5d496681a3952159aa1a1c4299234aa2f59e14d6858ea12f2df2a5314665b',
    'original_claims': '6be7a7a0ad16cf3b243e29fad6e840a5b318d8ec0d452746d09060ed87252ccb',
    'original_readme': '98cff368ab51cf24dd09208070b10409fb28cf027d3eac6a23ce5f49cdc3fd87',
}
CONSTANTS = {1: F(43), 2: F(65, 2), 3: F(23)}


def digest(path):
    h = sha256()
    with path.open('rb') as file:
        for chunk in iter(lambda: file.read(1048576), b''):
            h.update(chunk)
    return h.hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=False).encode()


def frozen(value):
    return tuple(map(frozen, value)) if isinstance(value, list) else value


def add(row, index, amount):
    if amount:
        row[index] = row.get(index, F()) + amount
        if not row[index]:
            del row[index]


def sparse(row):
    return [[j, str(a)] for j, a in sorted(row.items()) if a]


def unpack(row):
    out = {j: F(a) for j, a in row}
    assert len(out) == len(row) and all(out.values())
    return out


def save(name, value):
    path = HERE / name
    assert not path.exists(), ('refuse_overwrite', str(path))
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


class Stream:
    def __init__(self, file):
        self.file, self.buffer, self.position = file, '', 0
        self.decoder = json.JSONDecoder()

    def fill(self):
        self.buffer = self.buffer[self.position:] + self.file.read(131072)
        self.position = 0

    def peek(self):
        while True:
            while self.position < len(self.buffer) and self.buffer[self.position].isspace():
                self.position += 1
            if self.position < len(self.buffer):
                return self.buffer[self.position]
            self.fill()
            assert self.buffer, 'unexpected JSON end'

    def take(self, symbol):
        assert self.peek() == symbol
        self.position += 1

    def value(self):
        self.peek()
        while True:
            try:
                value, end = self.decoder.raw_decode(self.buffer, self.position)
                self.position = end
                return value
            except json.JSONDecodeError:
                old = len(self.buffer) - self.position
                self.fill()
                assert len(self.buffer) > old, 'incomplete JSON value'


def read_matrix(lift):
    metadata, columns, names = {}, None, None
    row_count = nnz = 0
    negative = Counter()
    positive = Counter()
    safe = {}
    with gzip.open(FILES['matrix'], 'rt') as file:
        stream = Stream(file)
        stream.take('{')
        while stream.peek() != '}':
            key = stream.value()
            stream.take(':')
            if key == 'columns':
                columns = stream.value()
                assert len(columns) == 21021
                assert columns[20585:] == lift['new_columns']
                assert all('weight' not in c for c in columns)
                overlap = {j for j, c in enumerate(columns)
                           if c['kind'] == 'X-query-overlap-upper'}
                assert len(overlap) == 420
            elif key == 'row_names':
                names = stream.value()
            elif key == 'rows':
                assert columns is not None
                stream.take('[')
                while stream.peek() != ']':
                    raw = stream.value()
                    nnz += len(raw)
                    assert all(0 <= j < 21021 for j, _ in raw)
                    if row_count < 20910:
                        assert all(j < 20585 for j, _ in raw)
                    else:
                        row = unpack(raw)
                        source = lift['rows'][row_count - 20910]
                        mapped = {j if j < 4849 else j + 15736: a
                                  for j, a in unpack(source['row']).items()}
                        assert row == mapped
                        if source['name'][0] == 'actual-safe-X':
                            safe[source['name'][1]] = (row_count, row)
                        for j in overlap.intersection(row):
                            if row[j] < 0:
                                assert row[j] == -1
                                assert source['name'][0] in ('overlap-at-most-X',
                                                            'overlap-at-most-query')
                                negative[j] += 1
                            else:
                                positive[j] += 1
                    row_count += 1
                    if stream.peek() == ',':
                        stream.take(',')
                stream.take(']')
            else:
                metadata[key] = stream.value()
            if stream.peek() == ',':
                stream.take(',')
        stream.take('}')
    assert row_count == len(names) == 22297 and nnz == 3296061
    assert set(safe) == set(range(1, 7))
    assert all(negative[j] == 2 for j in overlap)
    assert metadata['all_columns_nonnegative'] is True
    assert metadata['baseline_rows'] == 20910
    assert metadata['maxb_lift_sha256'] == PINS['lift']
    return columns, safe, {'rows': row_count, 'columns': len(columns),
                           'nonzeros': nnz, 'negative_upper_occurrences': sum(negative.values()),
                           'positive_upper_occurrences': sum(positive.values())}


def proof_atoms():
    atoms = []
    kernel_pairs = 0
    for i, constant in CONSTANTS.items():
        r = 7 - i
        A, alpha, beta = F(5 * (r - 1)), F(r) - F(6, 5), F(r, 2) - F(6, 5)
        assert constant == A + F(r*r, 2)
        assert min(A, alpha, beta) >= 0
        assert A + r + F(r * (r - 2), 2) == constant
        for b, z in product(range(i), range(r - 1)):
            kernel = F(1, b+z+1) - F(1, b+1) + F(r*z, 2*(b+r))
            assert kernel >= 0 and b+r <= 6
            kernel_pairs += 1
            for x, ell, q in product(range(2), repeat=3):
                n = x + z + ell
                w = F(1, b+r)
                v = F(x, b+n) if x else F()
                t = F(ell, b+n) if ell else F()
                query = F(q, b+x+z+1)
                L = q*x*w + F(q*(1-x), b+1)
                d, dL = x*(r-n)*w, x*(1-ell)*w
                Rd = 5*(v-x*w)-d
                Rt = r*ell*(1-x)*w - F(6, 5)*dL - (t-v)
                Rq = query-L+F(r, 2)*z*(1-x)*w
                assert min(Rd, Rt, Rq, d-dL) >= 0
                # u terms are separately checked above.  The per-customer
                # constants of all global budgets must match exactly.
                paid_without_u = (-A*v - r*ell*w - F(r, 2)*z*w + (t-query)
                                  + Rt + Rq + alpha*Rd + beta*(d-dL))
                target_without_u = -(constant-1)*x*w-L
                assert paid_without_u == target_without_u
                expanded_L = F(q, b+1) - F((r-1)*x*q, (b+1)*(b+r))
                assert expanded_L == L
                atoms.append({'actual_player': i, 'remaining_players': r,
                              'b': b, 'middle_count': z, 'X': x, 'last': ell,
                              'query': q, 'C': str(constant), 'R_d': str(Rd),
                              'R_t': str(Rt), 'R_Q': str(Rq),
                              'd_minus_d_L': str(d-dL),
                              'identity_residual': '0'})
    assert len(atoms) == 176 and kernel_pairs == 22
    return {'scope': 'All 176 local coefficient types in the explicit M=6 payment identity; not SPE enumeration.',
            'case_count': len(atoms), 'integer_kernel_b_z_pairs': kernel_pairs,
            'all_remainders_nonnegative': True, 'all_payment_identities_exact': True,
            'global_safety_budgets_not_assumed_pointwise_nonnegative': True,
            'records': atoms}


def build():
    hashes = {key: digest(path) for key, path in FILES.items()}
    for key, pin in PINS.items():
        assert hashes[key] == pin, key
    lift = json.loads(FILES['lift'].read_text())
    catalogue = json.loads(FILES['labels'].read_text())
    h3 = json.loads(FILES['h3_rows'].read_text())
    h3_audit = json.loads(FILES['h3_audit'].read_text())
    assert h3_audit['status'] == 'PASS'
    columns, old_safe, matrix_info = read_matrix(lift)
    atoms = proof_atoms()

    hist, joint, b4, old_to_current = {}, defaultdict(dict), defaultdict(list), {}
    current = None
    for j, c in enumerate(columns[:4849]):
        if c['kind'] == 'hist':
            current = j
            hist[j] = c
        elif c['kind'] == 'joint-reply':
            old = c['hist_column_old']
            assert old_to_current.setdefault(old, current) == current
            joint[current, frozen(c['group'])][tuple(c['state'])] = j
        elif c['kind'] == 'actual-B-family-state' and c['source'] == 4:
            b4[c['hist_column']].append((j, tuple(c['hidden']), c['ell']))
    assert len(hist) == len(old_to_current) == len(set(old_to_current.values())) == 16
    assert len(joint) == 194 and all(set(v) == {(0,1), (1,0), (1,1)} for v in joint.values())
    assert set(b4) == set(hist) and all(len(v) == 8 for v in b4.values())
    xcols = {c['hist_column']: j for j, c in enumerate(columns) if c['kind'] == 'common-X-mass'}
    upper = {(c['hist_column'], frozen(c['query_token'])): j
             for j, c in enumerate(columns) if c['kind'] == 'X-query-overlap-upper'}
    assert set(xcols) == set(hist) and sorted(xcols.values()) == list(range(20585, 20601))
    assert len(upper) == 420 and sorted(upper.values()) == list(range(20601, 21021))

    def marginal(h, token):
        if token[0] == 'bit':
            return {h: F(1)} if token[1] else {}
        if token[0] in ('R', 'Z'):
            axis = int(token[0] == 'Z')
            return {j: F(1) for state, j in joint[h, token[1]].items() if state[axis]}
        assert token[0] == 'H'
        return {j: F(1) for j, state, ell in b4[h] if state[token[1]]}

    for (h, token), j in upper.items():
        assert marginal(h, token) == unpack(columns[j]['query_marginal'])

    def label(d):
        if 'actual_position' in d:
            return ('A', d['actual_position'])
        if d['kind'] in ('T', 'B', 'C'):
            assert d['word_slot'] == ('T','B','C').index(d['kind'])
            return (d['kind'], *d['indices'])
        if 'own_coordinate' in d:
            assert d['node'] == [d['family'], *d['indices']]
            return ('R' if d['own_coordinate'] == 0 else 'Z', d['family'], *d['indices'])
        return ('H', d['B4_coordinate'])

    labels = [label(d) for d in catalogue['labels']]
    expected = [('A', j) for j in range(6)]
    expected += [(kind, j) for kind in ('T','B','C') for j in range(6)]
    nodes = [(f, j, k) for f, j, k in product(range(2), range(6), range(6)) if f or j != k]
    expected += [(kind, *node) for kind in ('R','Z') for node in nodes]
    expected += [('H', j) for j in range(2)]
    assert labels == expected and len(set(labels)) == 158
    perms = tuple(permutations(range(6)))

    def moved(q, pi):
        if q[0] in ('A','H'):
            return q
        if q[0] in ('T','B','C'):
            return (q[0], pi[q[1]])
        return (q[0], q[1], pi[q[2]], pi[q[3]])

    def orbit_key(q):
        if q[0] in ('A','H'):
            return q
        if q[0] in ('T','B','C'):
            return (q[0],)
        return (q[0], q[1], int(q[2] == q[3]))

    remaining, orbits = set(labels), []
    for q in labels:
        if q not in remaining:
            continue
        images = Counter(moved(q, pi) for pi in perms)
        assert set(images) <= remaining
        assert set(images.values()) == {720 // len(images)}
        members = [t for t in labels if t in images]
        orbits.append({'key': orbit_key(q), 'representative': q,
                       'members': members, 'images': images})
        remaining -= set(images)
    assert not remaining and len(orbits) == 17
    words = {h: [tuple(map(int, f'{k:03b}')) for k, n in enumerate(c['hist']) for _ in range(n)]
             for h, c in hist.items()}
    assert all(len(v) == 6 for v in words.values())

    def token_of(h, q):
        if q[0] == 'A':
            return ('bit', int(hist[h]['actual_bits'][q[1]]))
        if q[0] in ('T','B','C'):
            return ('bit', words[h][q[1]][('T','B','C').index(q[0])])
        if q[0] == 'H':
            return q
        kind, family, j, k = q
        return (kind, (family, int(j == k), words[h][j], words[h][k]))

    frequencies, frequency_records = {}, []
    for orb in orbits:
        records = []
        for h in hist:
            counts = Counter(token_of(h, q) for q in orb['members'])
            projected = Counter()
            for q, n in orb['images'].items():
                projected[token_of(h, q)] += n
            assert projected == {t: n*720//len(orb['members']) for t, n in counts.items()}
            frequencies[h, orb['key']] = counts
            records.append({'hist_column': h, 'frequencies': [[t,n] for t,n in sorted(counts.items(), key=repr)]})
        frequency_records.append({'orbit': orb['key'], 'representative': orb['representative'],
                                  'size': len(orb['members']), 'members': orb['members'],
                                  'S6_member_multiplicity': 720//len(orb['members']),
                                  'histogram_frequencies': records})

    incomes = {}
    safe_rows = {}
    for i in range(1, 7):
        incomes[i] = {h: F(1, sum(map(int,c['actual_bits'])))
                      for h,c in hist.items() if c['actual_bits'][i-1] == '1'}
        row = dict(incomes[i])
        for h,c in hist.items():
            b = sum(map(int, c['actual_bits'][:i-1]))
            add(row, xcols[h], -F(1, b+7-i))
        assert row == old_safe[i][1]
        safe_rows[i] = row
        assert incomes[i] == unpack(lift['incomes'][i-1])

    def generate(i, constant, orb, mode):
        r = 7-i
        row = {j: constant*a for j,a in incomes[i].items()}
        for h,c in hist.items():
            b = sum(map(int,c['actual_bits'][:i-1]))
            add(row, xcols[h], -(constant-1)/F(b+r))
            if mode == 'frequency':
                queries = frequencies[h, orb['key']].items()
            else:
                queries = [(token_of(h,q),1) for q in orb['members']]
            for token, n in queries:
                weight = F(n,len(orb['members']))
                for j,a in marginal(h,token).items():
                    add(row,j,-weight*a/F(b+1))
                if token[0] == 'bit':
                    if token[1]:
                        add(row,xcols[h],weight*F(r-1,(b+1)*(b+r)))
                else:
                    add(row,upper[h,token],weight*F(r-1,(b+1)*(b+r)))
        return row

    rows, used, per_player = [], Counter(), {}
    zero_hist = set(lift['zero_histograms'])
    assert zero_hist == {1,59,366,449,524,574} <= set(hist)
    for i,C in CONSTANTS.items():
        player_rows = []
        for oid,orb in enumerate(orbits):
            row = generate(i,C,orb,'frequency')
            assert row == generate(i,C,orb,'literal')
            assert all(0 <= j < 21021 for j in row)
            assert all(row[xcols[h]] < 0 for h in hist)
            for j in set(upper.values()).intersection(row):
                assert row[j] > 0
                used[j] += 1
            record = {'name':['common-X-early-arbitrary-anchor-AP',i,*orb['key']],
                      'actual_player':i,'remaining_players':7-i,'M_upper':'6','C':str(C),
                      'source_history':['A'+str(k) for k in range(1,i)],
                      'orbit_id':oid,'orbit_size':len(orb['members']),
                      'query_members':orb['members'], 'row':sparse(row),'rhs':'0',
                      'histogram_frequencies':frequency_records[oid]['histogram_frequencies']}
            rows.append(record)
            player_rows.append(record)
        per_player[str(i)] = {'C':str(C),'rows':len(player_rows),
                             'nonzero_count':sum(len(row['row']) for row in player_rows),
                             'all_16_hist_X_columns_in_each_row':True,
                             'all_six_old_zero_histograms_retained':True}
    assert len(rows) == 51 and set(used) == set(upper.values())
    assert set(used.values()) == {3}

    # A limited exact comparison at player 4 only, with the same X,Q and b.
    h3_by_members = {frozenset(map(tuple,row['query_members'])):unpack(row['row']) for row in h3['rows']}
    assert len(h3_by_members) == 17
    for orb in orbits:
        ap4 = generate(4,F(29,2),orb,'frequency')
        paid = dict(h3_by_members[frozenset(orb['members'])])
        for j,a in safe_rows[4].items():
            add(paid,j,F(9,2)*a)
        assert ap4 == paid

    assert hashes == {key:digest(path) for key,path in FILES.items()}, 'input changed during build'
    columns_digest = sha256(canonical(columns)).hexdigest()
    packet = {'status':'POINT_FREE_EXACT_51_ROW_PACKAGE',
              'source_object':'customer-attraction/background-weighted-near-saturation-exchange-and-common-anchor-cap',
              'source_claim':'B10-AP-v1; total-player bound M=6',
              'inequality_convention':'Every sparse row has value >= 0; homogeneous RHS 0.',
              'formula':'C_i*u_i-(C_i-1)*sum_h x_h/(b_h+r_i)-avg_Q sum_h q_h/(b_h+1)+avg_Q sum_h (r_i-1)*XQ_h/((b_h+1)*(b_h+r_i)) >= 0',
              'full_dimension':21021,'new_columns':0,'row_count':51,
              'nonzero_count':sum(len(row['row']) for row in rows),
              'columns_file':'columns_21021.json.gz','columns_canonical_sha256':columns_digest,
              'base_matrix_sha256':hashes['matrix'],'base_matrix_rows':22297,
              'common_X_columns':sorted(xcols.values()),'overlap_upper_columns':sorted(upper.values()),
              'all_overlap_coefficients_strictly_positive':True,
              'canonical_min_normalization_preserved':True,
              'all_zero_histograms_retained':sorted(zero_hist),
              'per_player':per_player,'input_sha256':hashes,
              'point_weights_read':False,'fixed_point_evaluated':False,'optimizer_called':False,
              'matrix_mutated':False,'rows':rows}
    orbit_report = {'literal_label_count':158,'orbit_count':17,'S6_permutations':720,
                    'histograms':16,'hist_representative_image_checks':16*17*720,
                    'literal_hist_query_count_per_player':16*158,
                    'literal_hist_query_count_all_three_players':3*16*158,
                    'all_orbits_derived_from_literal_labels':True,
                    'all_420_marginals_rebuilt_from_raw_old_descriptors':True,
                    'orbit_records':frequency_records}
    reading = {'complete_reading_done':True,'source_version':'AP-v1, with v2/empty-anchor boundaries separately read',
               'independent_read_only_source_review':'/root/early_x_anchor_queries/ap_source_audit; completed; agrees with constants and payment identity',
               'not_claimed':['external peer review','novel AP theorem','global six-player half proof','SPE realizability of LP points'],
               'locator':{
                   'original_proof':'lines 8--26: quantifiers/M; 33--112: real branches and integer kernel; 132--155: arbitrary-anchor AP and total-m bound',
                   'original_claims':'lines 8,10,14--17: AP-v1/AP-v2, common M_C and empty anchor',
                   'AP_object':'sections 量词、背景与两个版本; 任意锚主题AP的完整新增误差; 从真实实例到线性固定支持的准确合同'},
               'files':[{'key':key,'path':str(path.relative_to(REPO)),
                         'sha256':hashes[key],'bytes':path.stat().st_size}
                        for key,path in FILES.items()]}
    verification = {'status':'EXACT_EARLY_X_AP_51_ROWS_PASS',
                    'matrix':matrix_info,'input_sha256':hashes,
                    'full_columns_canonical_sha256':columns_digest,
                    'all_1387_common_X_rows_matched_frozen_matrix':True,
                    'all_6_SAFE_rows_rebuilt_from_actual_bits':True,
                    'proof_atom_cases':176,'integer_kernel_b_z_pairs':22,
                    'all_payment_coefficients_and_remainders_nonnegative':True,
                    'literal_labels':158,'single_query_orbits':17,
                    'S6_hist_representative_image_checks':195840,
                    'literal_hist_query_checks_all_three_players':7584,
                    'rows':51,'columns':21021,'new_columns':0,
                    'nonzero_count':packet['nonzero_count'],'per_player':per_player,
                    'common_X_mass_columns':16,'existing_overlap_upper_columns':420,
                    'positive_new_overlap_occurrences':1260,
                    'existing_upper_variables_have_only_the_two_negative_upper_bound_rows':True,
                    'all_420_marginals_rebuilt_from_raw_old_descriptors':True,
                    'literal_vs_frequency_rows_exactly_equal':True,
                    'all_zero_histograms_retained':sorted(zero_hist),
                    'player4_AP_equals_H3_plus_9_over_2_SAFE_exact_rows':17,
                    'no_cross_player_dominance_claim':True,
                    'point_weights_read':False,'old_point_file_opened':False,
                    'fixed_point_evaluated':False,'optimizer_called':False,
                    'frozen_inputs_unchanged':True,'matrix_mutated':False,
                    'constructor_imported':False,'created_utc':datetime.now(timezone.utc).isoformat()}
    target = HERE/'columns_21021.json.gz'
    assert not target.exists()
    with target.open('wb') as raw:
        with gzip.GzipFile(filename='',fileobj=raw,mode='wb',mtime=0) as packed:
            packed.write(json.dumps(columns,ensure_ascii=False,separators=(',',':')).encode())
    save('proof_atoms_176.json',atoms)
    save('orbit_frequency_audit.json',orbit_report)
    save('rows_51.json',packet)
    save('source_reading.json',reading)
    save('verification.json',verification)
    print(json.dumps({k:verification[k] for k in ('status','rows','columns','new_columns',
                    'nonzero_count','per_player','proof_atom_cases','frozen_inputs_unchanged',
                    'point_weights_read','fixed_point_evaluated','optimizer_called')},ensure_ascii=False,indent=2))


def freeze():
    report = json.loads((HERE/'verification.json').read_text())
    assert report['status'] == 'EXACT_EARLY_X_AP_51_ROWS_PASS'
    assert report['input_sha256'] == {key:digest(path) for key,path in FILES.items()}
    names = ['build_and_check.py','columns_21021.json.gz','proof_atoms_176.json',
             'orbit_frequency_audit.json','rows_51.json','source_reading.json','verification.json']
    assets = [HERE/name for name in names] + [WORK/'early_x_anchor_queries.md']
    for name in ('build.stdout.json','build.stderr.txt'):
        if (HERE/name).exists():
            assets.append(HERE/name)
    manifest = {'status':'FROZEN_RELEASED','task':'early_x_anchor_queries',
                'scope':'Existing AP theorem instantiated at actual players 1--3; 51 rows, zero new columns; no augmented matrix created.',
                'rows':51,'columns':21021,'new_columns':0,
                'nonzero_count':report['nonzero_count'],
                'input_sha256':report['input_sha256'],
                'assets':[{'path':str(path.relative_to(REPO)),'sha256':digest(path),
                           'bytes':path.stat().st_size} for path in assets],
                'point_evaluated':False,'optimizer_called':False,'matrix_mutated':False,
                'git_RUN_registry_mutated':False,
                'created_utc':datetime.now(timezone.utc).isoformat()}
    save('freeze_manifest.json',manifest)
    paths = assets + [HERE/'freeze_manifest.json']
    target = HERE/'SHA256SUMS'
    assert not target.exists()
    target.write_text(''.join(f'{digest(path)}  {path.relative_to(WORK)}\n' for path in paths))
    print(json.dumps({'status':'FROZEN_RELEASED','manifest_sha256':digest(HERE/'freeze_manifest.json'),
                      'rows':51,'nonzero_count':report['nonzero_count']},ensure_ascii=False))


if __name__ == '__main__':
    if sys.argv[1:] == ['--freeze']:
        freeze()
    else:
        assert not sys.argv[1:]
        build()
