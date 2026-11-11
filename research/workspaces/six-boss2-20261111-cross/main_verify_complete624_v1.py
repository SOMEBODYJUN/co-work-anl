"""Independent Main audit of the entire raw 624 common hidden extension.

Reconstructs the structural domain, every link, every raw budget coefficient,
and the nonnegative-min identity. Imports no discovering or construction code.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
import gzip, hashlib, json, time
from main_cross_query_features_v1 import query_samples, literal_product, pay
from main_reverse_terminal_features_v1 import all_616, reverse_value, projection_624, moment_product, CROSS_NAMES

B = Path(__file__).resolve().parent
J = B / 'joint_requery'
M = B / 'master_cuts'
stem = 'complete624_actual4_R00_v1'
started = time.time()
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def matrix(path):
    with gzip.open(path, 'rt', encoding='utf-8') as f:
        return json.load(f)

def sparse(d):
    return [[j, str(v)] for j, v in sorted(d.items()) if v]

oldp, newp = M/'complete_zz_5799_v1_matrix.json.gz', J/(stem+'_matrix.json.gz')
mapping_path = J/(stem+'_mapping.json')
old, new = matrix(oldp), matrix(newp)
mapping = json.loads(mapping_path.read_text())
assert sha(oldp) == '8b076497ef826b60c797edcb8dc719f2f7ad678a01a34ecf66d2e757af525a20'
assert sha(newp) == '556c3cac51e87a699d1f3a9c427f556836932b6fc2399fa330f375c6efd8231a'
assert (new['row_count'], new['column_count']) == (12666, 12631)
assert new['rows'][:11418] == old['rows'] and new['columns'][:7639] == old['columns']
assert new['objective'] == old['objective'] + ['0']*4992
assert new['normalization'] == old['normalization'] + ['0']*4992
assert new['nonnegative_columns'] == 'all'
assert all(all(j < 7639 for j, v in row['nonzero']) for row in new['rows'][:11418])

blocks = {}
for j, rec in enumerate(old['columns'][:4849]):
    if rec['kind'] == 'hist':
        h = j
        blocks[h] = {'descriptor': rec, 'groups': {}}
    elif rec['kind'] == 'joint-reply' and rec['group'][:2] == [0, 0]:
        key = tuple(rec['group'][2]), tuple(rec['group'][3])
        blocks[h]['groups'].setdefault(key, {})[tuple(rec['state'])] = j
assert len(blocks) == 16 and sum(len(b['groups']) for b in blocks.values()) == 78

# Transpose only the new raw budget block. Keep original coefficient strings
# and parse each once when comparing an independently derived exact value.
saved_columns = defaultdict(dict)
old_budget_parts = {}
name_to_row = {}
for row in new['rows'][12042:]:
    name = row['feature_name']
    assert name not in name_to_row and row['name'] == 'macro624:budget:'+name
    name_to_row[name] = row['index']
    old_budget_parts[name] = {}
    for col, value in row['nonzero']:
        if col < 4849:
            old_budget_parts[name][col] = F(value)
        else:
            assert col >= 7639
            saved_columns[col][name] = value
assert len(name_to_row) == 624

states = tuple(product((0, 1), repeat=2))
hidden_states = tuple(product((0, 1), repeat=4))
assert mapping['RZ_state_order'] == [list(v) for v in states]
assert mapping['hidden_state_order'] == [list(v) for v in hidden_states]
rec_pack = json.loads((J/'reverse_terminal_5799_one_v1.json').read_text())['cuts'][0]
theta = {n:F(w) for n,w in rec_pack['weights'].items()}
phi = projection_624(theta)
budget_terms = None
group_index = 0
literal_checks, feature_checks, min_residuals = 0, 0, 0
projected = defaultdict(F)
point = json.loads((M/'complete_zz_5799_v1_exact.json').read_text())
original_x = [F(c['weight']) for c in point['columns']]
zero_marginals = 0
for hist, block in blocks.items():
    desc = block['descriptor']
    actual = tuple(map(int, desc['actual_bits']))
    words = tuple(w for w, n in zip(product((0, 1), repeat=3), desc['hist']) for _ in range(n))
    assert len(words) == 6
    pairs = defaultdict(list)
    for i in range(6):
        for j in range(6):
            if i != j:
                pairs[words[i], words[j]].append((i, j))
    assert set(pairs) == set(block['groups']) and sum(len(v) for v in pairs.values()) == 30
    for key in sorted(block['groups']):
        state_cols = block['groups'][key]
        assert set(state_cols) == {(0, 1), (1, 0), (1, 1)}
        rec = mapping['groups'][group_index]
        assert rec['group_index'] == group_index and rec['hist_column'] == hist
        assert rec['actual_bits'] == desc['actual_bits'] and rec['hist'] == desc['hist']
        assert rec['six_words'] == [list(w) for w in words]
        assert rec['group'] == [0, 0, list(key[0]), list(key[1])]
        assert rec['literal_index_pairs'] == [list(p) for p in pairs[key]]
        weight = F(len(pairs[key]), 30)
        assert rec['multiplicity'] == len(pairs[key]) and F(rec['orbit_weight']) == weight
        left, right = pairs[key][0]
        for si, rz in enumerate(states):
            state_rec = rec['states'][si]
            samples, qs, moments = query_samples(actual, words, left, right, rz)
            for i, j in pairs[key]:
                assert query_samples(actual, words, i, j, rz)[1:] == (qs, moments)
                literal_checks += 1
            for name in CROSS_NAMES:
                assert moment_product(name, qs, moments) == literal_product(samples, name)
            p, ell, t = sum(actual[:3]), sum(actual[:5]), rz[0]
            assert state_rec['state'] == list(rz)
            assert state_rec['visible'] == {'p':p,'ell':ell,'t':t,'queries':list(map(str,qs)),'moments':list(map(str,moments))}
            cols = list(range(7639+64*group_index+16*si, 7639+64*group_index+16*si+16))
            assert state_rec['hidden_columns'] == cols
            marginal = {hist:F(1), **{col:F(-1) for col in state_cols.values()}} if rz == (0,0) else {state_cols[rz]:F(1)}
            assert state_rec['old_marginal_affine'] == sparse(marginal)
            value = sum(v*original_x[col] for col,v in marginal.items())
            assert value >= 0
            zero_marginals += value == 0
            plus = {col:F(1) for col in cols}
            plus.update({col:-v for col,v in marginal.items()})
            ri = 11418+8*group_index+2*si
            assert state_rec['equality_plus_row'] == ri and state_rec['equality_minus_row'] == ri+1
            assert new['rows'][ri]['nonzero'] == sparse(plus)
            assert new['rows'][ri+1]['nonzero'] == sparse({col:-v for col,v in plus.items()})
            minimum = phi(p,ell,t,qs,moments)
            for col, hidden in zip(cols, hidden_states):
                descriptor = new['columns'][col]
                assert descriptor['kind'] == 'actual4-R-shared624-conditional-mass'
                assert descriptor['hist_column'] == hist and descriptor['group'] == rec['group']
                assert descriptor['state'] == list(rz) and descriptor['macro_hidden'] == list(hidden)
                features, budgets = all_616(p,ell,t,qs,moments,hidden+(0,0))
                for node in ('priorR','priorZ'):
                    for label in ('b','c','j','v'):
                        name = node+':'+label
                        features[name] = reverse_value(name,qs,hidden)
                        budgets[name] = (F(0),F(0),F(0))
                assert set(features) == set(name_to_row) and len(features) == 624
                if budget_terms is None:
                    budget_terms = budgets
                else:
                    assert budgets == budget_terms
                saved = saved_columns[col]
                assert set(saved) <= set(features)
                for name,value in features.items():
                    assert -weight*value == F(saved.get(name,'0')), (col,name)
                    feature_checks += 1
                cost = sum(w*features[n] for n,w in theta.items())
                assert cost >= minimum
                min_residuals += cost > minimum
                # Weighted raw budgets + nonnegative (cost-minimum) column
                # residual + signed equality rows cancel every new column.
                assert -weight*cost+weight*(cost-minimum)+weight*minimum == 0
            for col,v in marginal.items():
                projected[col] -= weight*minimum*v
        group_index += 1
assert group_index == 78 and literal_checks == 1920 and feature_checks == 4992*624
assert zero_marginals == 247
for name,(r,u,k) in budget_terms.items():
    expected = {0:F(k)} if k else {}
    for h,b in blocks.items():
        a = tuple(map(int,b['descriptor']['actual_bits']))
        value = r*pay(a[3],sum(a))+u*pay(a[5],sum(a))
        if value:
            expected[h] = value
    assert old_budget_parts[name] == expected
    mapped = mapping['budgets'][name_to_row[name]-12042]
    assert mapped['feature_name'] == name and mapped['row_index'] == name_to_row[name]
    assert mapped['external_coefficients'] == {'u4':str(F(r)),'u6':str(F(u)),'K':str(F(k))}
    assert mapped['identically_zero_row'] == (not new['rows'][name_to_row[name]]['nonzero'])
    if name in theta:
        for col,value in expected.items():
            projected[col] += theta[name]*value
expected_projected = {col:F(v) for col,v in rec_pack['sparse_row']}
assert {col:v for col,v in projected.items() if v} == expected_projected
assert min_residuals == 4582
new_point_slack = sum(v*original_x[col] for col,v in projected.items())
assert new_point_slack < 0
for row in new['rows'][11418:]:
    sp = row['nonzero']
    assert sp == sorted(sp) and len(sp) == len({j for j,v in sp})
    assert all(not 4849 <= j < 7639 for j,v in sp)
    digest = hashlib.sha256(json.dumps(sp,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
    assert digest == row['sparse_sha256']

report = {'status':'PASS','matrix_sha256':sha(newp),'mapping_sha256':sha(mapping_path),
          'base_matrix_sha256':sha(oldp),'rows':12666,'columns':12631,
          'old_rows_and_columns_unchanged':True,'new_columns':4992,'old_word_pair_groups':78,
          'marginal_equalities_rebuilt':312,'raw_budgets_rebuilt':624,
          'all_new_feature_coefficients_checked':feature_checks,'literal_query_checks':literal_checks,
          'all_zero_mass_domains_retained':True,'zero_RZ_marginals_retained':zero_marginals,
          'old_624_separator_exact_min_identity':True,'positive_min_residual_columns':min_residuals,
          'old_624_separator_slack_on_new_ZZ_point':str(new_point_slack),
          'scope':'Complete shared-hidden raw624 lift for only actual4/R/family0 off-diagonal on all fixed16 histograms. Every new coefficient independently reconstructed; no full-SPE sufficiency or all-structure closure.',
          'seconds':time.time()-started,'verifier_sha256':sha(Path(__file__))}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
