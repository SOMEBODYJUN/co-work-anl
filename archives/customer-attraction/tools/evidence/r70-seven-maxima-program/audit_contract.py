"""Independent Fraction reconstruction of the captured literal source contract, no LP/import."""
from collections import Counter
from fractions import Fraction as F
import gzip
import hashlib
from itertools import combinations, combinations_with_replacement
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
C = ROOT / 'original-event' / 'capture.json.gz'
assert hashlib.sha256(C.read_bytes()).hexdigest() == '8596a6fada0d4f9f8c5d1f768c1fb416593ff17b0ab2ae438a401bc92b2bd8c5'
data = json.loads(gzip.decompress(C.read_bytes()))
assert data['excluded'] == 6 and data['route'] is None
alpha = [F(1,12)]*6
beta = list(map(F, ['1/21','2/37','1/16','2/27','1/11','7/72']))
pairs = list(combinations_with_replacement(range(7),2))
names = ([f'M{t}' for t in range(6)] + [f'P{t}{j}' for t in range(5) for j in range(7)]
         + [f'L{j}' for j in range(7)] + [f'T{j}{k}' for j,k in pairs])
assert names == data['names'] and len(names) == 76

def row_values(I, J, literal):
    q = len(J)
    s = [F((2**t if literal else 1),q) if t in J else F(0) for t in range(6)]
    floor = [F(1,6) if len(I)==7 else alpha[t] if len(I)==1 else beta[t] for t in range(6)]
    r = [s[t]-floor[t] for t in range(6)]
    for t in range(5):
        old = sum(v<t for v in J)
        r += [s[t] - (F(1,old+6-t) if j in I else 0) for j in range(7)]
    old5 = sum(v<5 for v in J)
    r += [s[5] - (F(1,old5+1) if j in I else 0) for j in range(7)]
    old4 = sum(v<4 for v in J)
    tax = F(1,(old4+1)*(old4+2)) if 4 in J else F(0)
    for j,k in pairs:
        v = int(j in I) + int(k in I)
        r.append(s[4]+s[5]+tax-(F(v,old4+v) if v else 0))
    return r

records = []
differences = Counter()
checked = 0
for index,(imask,jmask) in enumerate(data['types']):
    I = {i for i in range(7) if imask & 2**i}
    J = {j for j in range(6) if jmask & 2**j}
    assert I and ((0 in I)==(5 in J))
    assert index == (imask-1)*32 + (jmask & 31)
    literal, actual = row_values(I,J,True), row_values(I,J,False)
    assert [float(x) for x in literal] == data['A'][index]
    b = F(bool(J))-F(bool(I-{6}),2)
    assert float(b) == data['b'][index]
    for name,u,v in zip(names,literal,actual):
        assert u >= v
        differences[name[0]] += int(u != v)
        checked += 1
assert len(data['types']) == 4064 and checked == 308864

# Simple exact separator for the literal source rows. This is deliberately new,
# not a rationalization of the 36-support floating optimizer output.
support = [(frozenset((0,j)),frozenset(range(6)),F(1,18)) for j in range(1,7)]
support += [(frozenset((j,k)),frozenset(),F(2,45)) for j,k in combinations(range(1,7),2)]
assert len(support) == 21 and sum(w for I,J,w in support) == 1
means = [F(0)]*76
true_means = [F(0)]*76
target = F(0)
customers = []
for I,J,w in support:
    assert len(I)==2 and all(0 in I for t in J) and ((5 in J)==(0 in I))
    old, true = row_values(I,J,True),row_values(I,J,False)
    means = [a+w*b for a,b in zip(means,old)]
    true_means = [a+w*b for a,b in zip(true_means,true)]
    target += w*(F(bool(J))-F(bool(I-{6}),2))
    mass = 90*w
    assert mass.denominator == 1
    customers.extend([I]*mass.numerator)
    records.append({'I':sorted(I),'J':sorted(J),'weight':str(w),'unit_multiplicity_at_scale90':mass.numerator})
assert target == -F(1,6) and all(x>=0 for x in means)
assert all(true_means[names.index(f'L{j}')] == -F(19,108) for j in range(1,7))
assert true_means[names.index('L0')] == 0
# Explicit profile, not a complete strategy: all six choose B0.
covers = [{x for x,I in enumerate(customers) if j in I} for j in range(7)]
assert len(customers)==90 and list(map(len,covers))==[30,25,25,25,25,25,25]
assert all(not a<=b for i,a in enumerate(covers) for j,b in enumerate(covers) if i!=j)
last_income = F(len(covers[0]),6)
deviation = sum((F(1,6) if x in covers[0] else F(1)) for x in covers[1])
assert last_income == 5 and deviation == F(125,6)
assert last_income-deviation == -F(95,6)
assert len(set().union(*covers[:6]))==90

route_counts = {}
for route in [(0,0,0,0,0),(0,0,0,0,1),(0,1,2,3,4)]:
    count = sum(2**sum(bool(I & 2**a) for a in route) for I in range(1,128))
    route_counts[''.join(map(str,route))] = count
assert route_counts == {'00000':2111,'00001':1631,'01234':971}
result = {
 'status':'PASS', 'identity':'one independent standard-library contract audit; not an original source main or LP',
 'capture_sha256':hashlib.sha256(C.read_bytes()).hexdigest(),
 'source_sha256':data['source_sha256'], 'captured_columns_checked':4064,
 'captured_coefficients_compared':checked,'captured_targets_compared':4064,
 'source_matrix_equals_literal_bit_value_formula':True,
 'literal_minus_equal_share_is_pointwise_nonnegative':True,
 'strictly_changed_coefficients_by_family':dict(differences),
 'private_suffix':list(map(str,alpha)),'shared_suffix':list(map(str,beta)),
 'route_column_counts_by_formula':route_counts,
 'all_original_helpers_calls':0,'original_main_calls':0,'LP_calls':0,'SPE_solver_calls':0,
 'simple_exact_separator':{
   'distinct_from_float_optimizer':True,'route':'000000','all_excluded_indices_0_through_6_same_target':True,
   'support':records,'total_weight':'1','target':str(target),
   'literal_minimum_row_average':str(min(means)),
   'literal_row_averages':{n:str(x) for n,x in zip(names,means)},
   'equal_share_row_averages':{n:str(x) for n,x in zip(names,true_means)},
   'profile_unit_customer_count':90,'profile_topic_sizes':list(map(len,covers)),
   'profile_action_sequence':[0]*6,'profile_actual_coverage':30,'profile_six_topic_optimum':90,
   'profile_last_income':str(last_income),'profile_last_deviates_to_B1_income':str(deviation),
   'profile_is_SPE':False,'complete_strategy_constructed':False
 },
 'float_event_retained_separately':{'res_status':data['res']['status'],'sep_status':data['sep']['status'],
                                  'sep_fun':data['sep']['fun'],'positive_support_over_1e_8':sum(x>1e-8 for x in data['sep']['x'])}
}
(ROOT/'contract-audit.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='simple_exact_separator'},ensure_ascii=False))
