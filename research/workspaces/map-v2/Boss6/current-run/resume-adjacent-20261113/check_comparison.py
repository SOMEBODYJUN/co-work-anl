"""Read-only exact report checks and a new finite mixed-cost comparison.

No original entry point is imported or executed. Existing evidence is never written.
The finite mixed-cost fixtures do not certify SPE realization or welfare.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations_with_replacement, permutations, product
from math import comb, factorial
from pathlib import Path
import hashlib
import json

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'research/registry.json').is_file())
HERE = Path(__file__).resolve().parent
TASK = 'customer-attraction-3a-3a-33fad33b32a8d904'
task = json.loads((ROOT / f'research/operations/map-v2/tasks/{TASK}.json').read_text())['definition']
registry = json.loads((ROOT / 'research/registry.json').read_text())
objects = registry['objects']
if isinstance(objects, dict):
    objects = list(objects.values())
selected = {x['object_id']: x for x in objects if x['object_id'] in task['input_pins']}
refs = {}
for obj in selected.values():
    for ref in [obj['body'], *obj.get('evidence', [])]:
        path = ref['path']
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == ref['sha256']
        refs[path] = ref['sha256']

path = 'archives/customer-attraction/tools/evidence/shared-matching-loss-and-adjacent-load-primary/new-loss-layers-adjacent-and-727.json'
data = json.loads((ROOT / path).read_text())
generic = data['generic_layers']
assert generic['q_values'] == [1,2,3] and generic['menus'] == 3 and generic['source_load_configurations_per_q'] == 2
assert generic['weight_vectors'] == [[1,2,3],[0,1,2]]
assert generic['D_complement_masks'] == [[0,0,0],[1,0,1],[1,1,1]]
assert generic['combined_cases'] == 12*sum(8**q for q in range(1,4)) == 7008
assert generic['label_group_layer_identities'] == 2*generic['combined_cases'] == 14016
def sum_permutation_multiplicities(n):
    total = 0
    for word in combinations_with_replacement(range(8),n):
        ways = factorial(n)
        for value in Counter(word).values():
            ways //= factorial(value)
        total += ways**2
    return total
literal_count_formula = 0
for q in range(1,4):
    a,b = (q+1)//2,q//2
    literal_count_formula += 6*(sum_permutation_multiplicities(q)+8**q+8**b*sum_permutation_multiplicities(a)+8**a*sum_permutation_multiplicities(b))
assert generic['literal_label_group_matching_assignments'] == literal_count_formula == 29136
assert generic['two_menu_n_range'] == [0,6]
integer_count = sum((n+1) for n in range(7) for k in range(n+1) for l in range(n+1) for h in range(max(0,k+l-n),min(k,l)+1))
assert generic['two_menu_integer_brackets'] == integer_count == 1218
assert generic['twolevel_rational_identities'] == 2*integer_count == 2436
adj = data['adjacent']
counts = Counter()
compatible = Counter()
for row in adj['all_margin_records']:
    q, L, M = row['q'], row['L'], row['M']
    assert len(L) == len(M) == 4 and L[-1] == 0
    assert sum(L) == sum(M) == q
    assert all(type(z) is int and z >= 0 for z in L + M)
    fl = fm = 0
    X, Y = [], []
    good = True
    for l, m in zip(L, M):
        old = fl
        fl += l
        fm += m
        X.append(fl - fm)
        Y.append(fm - old)
        good &= old <= fm <= fl
    assert row['X'] == X and row['Y'] == Y
    assert row['compatible'] == good == all(z >= 0 for z in X + Y)
    assert X[-1] == 0
    counts[q] += 1
    witness = row['witness']
    if good:
        compatible[q] += 1
        assert len(witness) == q
        assert all(0 <= p <= 2 and a in (0, 1) for p, a in witness)
        assert [sum(p == c for p, a in witness) for c in range(4)] == L
        assert [sum(p + a == c for p, a in witness) for c in range(4)] == M
        assert [sum(p == c and a == 1 for p, a in witness) for c in range(4)] == X
        assert [sum(p == c and a == 0 for p, a in witness) for c in range(4)] == Y
    else:
        assert witness is None
assert len(adj['all_margin_records']) == adj['all_margin_pairs'] == sum(comb(q+2, 2)*comb(q+3, 3) for q in range(5))
assert sum(compatible.values()) == adj['compatible_pairs'] == sum(comb(q+5, 5) for q in range(5))
assert adj['indexed_lists'] == sum(6**q for q in range(5))
for q in range(5):
    assert counts[q] == comb(q+2, 2)*comb(q+3, 3)
    assert compatible[q] == comb(q+5, 5)
wide = adj['increments012_counterexample']
assert Counter(p for p,q in wide['joint1']) == Counter(p for p,q in wide['joint2'])
assert Counter(q for p,q in wide['joint1']) == Counter(q for p,q in wide['joint2'])
assert [str(sum((F(1,(p+1)*(q+1)) for p,q in wide[key]), F(0))) for key in ('joint1','joint2')] == wide['reciprocal_joint_costs']
assert wide['reciprocal_joint_costs'] == ['2/3', '7/12']

# Check every saved atom, layer term, literal assignment and weighted aggregate.
# This is report arithmetic, not regeneration of the original 727-row system.
triples = list(product((0,1), repeat=3))
quads = list(product((0,1), repeat=4))
def expand(hist, types):
    assert len(hist) == len(types) and all(type(n) is int and n >= 0 for n in hist)
    return [t for t,n in zip(types,hist) for _ in range(n)]
point = data['point727']
sums = dict.fromkeys(('M','N','joint','loss'), F(0))
literal_count = strict = layer_count = 0
for ai, row in enumerate(point['atom_records']):
    assert row['atom'] == ai
    source, target = expand(row['AB_hist'],triples), expand(row['second_hist'],quads)
    assert len(source) == len(target) == 5
    mass = F(row['mass'])
    assert mass > 0
    dd = [None] * 5
    group_loss = F(0)
    expected_assignments = [()]
    for label, group in enumerate(row['groups']):
        assert group['label'] == label
        pos = [i for i,t in enumerate(source) if t[0] == label]
        tuples = [(t[2],t[3]) for t in target if t[0] == label]
        ds = list(map(F, group['inverse_denominators']))
        assert pos == group['source_positions'] and tuples == list(map(tuple,group['target_tuples']))
        assert len(pos) == len(tuples) == len(ds)
        for i,d in zip(pos,ds):
            dd[i] = d
        k, l = sum(t[0] for t in tuples), sum(t[1] for t in tuples)
        h = sum(t[0]*t[1] for t in tuples)
        assert [group[x] for x in ('k','l','h','u')] == [k,l,h,k+l-h]
        assert group['high_slots'] == sum(source[i][1] == 0 for i in pos)
        sd, ss = sorted(ds,reverse=True), sorted((sum(t) for t in tuples),reverse=True)
        delta = F(0)
        assert len(group['layer_terms']) == max(0,len(ds)-1)
        for r, term in enumerate(group['layer_terms'],1):
            jump = sd[r-1]-sd[r]
            bracket = min(k,r)+min(l,r)-sum(ss[:r])
            assert term['r'] == r and F(term['jump']) == jump and F(term['bracket']) == bracket and F(term['term']) == jump*bracket
            assert jump >= 0 and bracket >= 0
            delta += jump*bracket
            layer_count += 1
        assert F(group['loss']) == delta
        group_loss += delta
        expected_assignments = [old+tuple(zip(pos,perm)) for old in expected_assignments for perm in set(permutations(tuples))]
    bases = {1/d-1-source[i][0]-source[i][1] for i,d in enumerate(dd)}
    assert len(bases) == 1 and next(iter(bases)) in (0,1,2)
    stored_assignments = set()
    vals = []
    for match in row['literal_matchings']:
        assignment = tuple(map(tuple,match['target_assignment']))
        stored_assignments.add(assignment)
        lm = sum((dd[i]*(source[i][2]-assignment[j][0]) for i in range(5) for j in range(5) if i != j),F(0))
        ln = sum((dd[i]*(source[i][2]-assignment[j][1]) for i in range(5) for j in range(5) if i != j),F(0))
        assert F(match['M_offdiag']) == lm and F(match['N_offdiag']) == ln and F(match['joint']) == lm+ln
        vals.append((lm,ln,lm+ln))
        literal_count += 1
    expected = set()
    for indexed in expected_assignments:
        assignment = [None]*5
        for i,t in indexed:
            assignment[i] = t
        expected.add(tuple(assignment))
    assert stored_assignments == expected and len(stored_assignments) == len(vals)
    m,n,j = (max(v[i] for v in vals) for i in range(3))
    loss = m+n-j
    assert F(row['M_upper']) == m and F(row['N_upper']) == n and F(row['joint_upper']) == j
    assert F(row['loss']) == loss == group_loss >= 0
    strict += loss > 0
    for key,value in zip(sums,(m,n,j,loss)):
        sums[key] += mass*value
assert len(point['atom_records']) == point['atoms'] == 69
assert literal_count == point['distinct_literal_matchings'] == 217
assert strict == point['strict_tax_atoms'] == 20
for key,field in [('M','M_separate_upper'),('N','N_separate_upper'),('joint','joint_upper'),('loss','weighted_loss')]:
    assert sums[key] == F(point[field])
assert sums['M']+sums['N']-sums['joint'] == sums['loss'] and sums['joint'] < 0

old = json.loads((ROOT/'archives/customer-attraction/tools/evidence/round5-load-audits-resumed-boss2/original/round5_pricing/audit_adjacent_loads.json').read_text())
assert len(old['records']) == 30
for row in old['records']:
    m,q = row['m'],row['q']
    assert row['unique_joint_laws'] == comb(q+2*(m-1)-1,2*(m-1)-1)
    assert row['all_marginal_pair_checks'] == (comb(q+m-2,m-2)*comb(q+m-1,m-1) if q <= 3 else 0)
assert sum(r['unique_joint_laws'] for r in old['records']) == old['client_histogram_checks'] == 4899
assert sum(r['all_marginal_pair_checks'] for r in old['records']) == old['all_marginal_pair_checks'] == 3525
old2 = json.loads((ROOT/'archives/customer-attraction/tools/evidence/round5-shared-matching-resumed-boss2/original/adjacent_load_checks.json').read_text())
assert old2['individual_list_reconstructions'] == 1555
assert old2['unique_margin_pairs_checked'] == 210
assert old2['margin_compatibility_pairs'] == sum(comb(q+3,3)**2 for q in range(5)) == 1742

def pattern_coeff(q,kind,z,w,B,C,K):
    return [(1,z+w,z*w),(q-1,B-z+C-w,K-z*w),(q-1,(q-1)*z+C-w,z*(C-w)),(q-1,B-z+(q-1)*w,(B-z)*w),((q-1)*(q-2),(q-2)*(B-z+C-w),(B-z)*(C-w)-(K-z*w))][kind]

# New comparison fixtures: one label, all source and target multisets q=1..3.
# Exact bijections on actual pairs vs canonically recovered pairs; all five
# pair modes, both omega values and three nonnegative terminal D/O choices.
fixture_count = cost_count = 0
first_gap = None
states = list(product(range(3),(0,1)))
targets = list(product((0,1),repeat=2))
for q in range(1,4):
    for raw in combinations_with_replacement(states,q):
        source = [(p,p+a) for p,a in reversed(raw)]
        L = [sum(p==c for p,Q in source) for c in range(4)]
        M = [sum(Q==c for p,Q in source) for c in range(4)]
        fl=fm=0
        recovered=[]
        for c in range(4):
            oldfl=fl
            fl+=L[c];fm+=M[c]
            recovered += [(c,c)]*(fm-oldfl)+[(c,c+1)]*(fl-fm)
        assert Counter(source) == Counter(recovered)
        for target in combinations_with_replacement(targets,q):
            fixture_count += 1
            B,C,K = sum(t[0] for t in target),sum(t[1] for t in target),sum(t[0]*t[1] for t in target)
            perms=list(set(permutations(target)))
            for mode,omega,(alpha,beta) in product(range(5),(1,2),((1,0),(0,1),(1,1))):
                def values(src):
                    out=[]
                    for perm in perms:
                        term=pair=F(0)
                        for (p,Q),(z,w) in zip(src,perm):
                            n,ell,dot=pattern_coeff(q,mode,z,w,B,C,K)
                            term += F(-beta*B+(beta-alpha)*z,Q+1)
                            pair += -F(ell,p+1)+F(omega*dot,(p+1)*(p+2))
                        out.append((term,pair,term+pair))
                    return out
                actual, restored = values(source),values(recovered)
                assert max(v[2] for v in actual) == max(v[2] for v in restored)
                separate=max(v[0] for v in actual)+max(v[1] for v in actual)
                joint=max(v[2] for v in actual)
                assert separate >= joint
                if separate > joint and first_gap is None:
                    first_gap={'q':q,'source':source,'target':target,'mode':mode,'omega':omega,'alpha':alpha,'beta':beta,'joint_query_max':str(joint),'sum_separate_query_max':str(separate),'gap':str(separate-joint)}
                cost_count += 1
assert first_gap is not None

result={'status':'passed','reference_file_hashes':refs,'complete_adjacent_report_records':len(adj['all_margin_records']),'adjacent_records_by_q':dict(counts),'compatible_by_q':dict(compatible),'old_30_records_checked':30,'saved69_atom_rows_checked':69,'saved69_literal_assignments_checked':literal_count,'saved69_layer_terms_checked':layer_count,'new_mixed_fixture_pairs':fixture_count,'new_mixed_cost_comparisons':cost_count,'strict_separate_vs_joint_fixture':first_gap,'original_CLI_entries':0,'old_evidence_outputs_modified':False,'scope':'Exact report arithmetic and finite generic mixed-query fixtures only. Arbitrary finite loads/record counts use the analytic recurrence and transport proof; no fixture is asserted to be a full SPE or root welfare certificate.'}
(HERE/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='reference_file_hashes'},ensure_ascii=False,indent=2))
