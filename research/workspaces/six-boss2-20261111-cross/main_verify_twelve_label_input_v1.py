"""Independent Main reconstruction of one finite twelve-label unit game."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
from math import lcm,gcd,comb
from functools import reduce
import hashlib,json
B=Path(__file__).resolve().parent
P=B/'master_cuts'
candidate_path=P/'full_history_probe_12label_v1.json'
point_path=P/'complete_zz_5799_v1_original4849_exact.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
candidate,point=json.loads(candidate_path.read_text()),json.loads(point_path.read_text())
assert sha(candidate_path)=='59e86b2961662aba4c9a9c9128fa03f2ee68b0b7c5bd7577896bc897838508f7'
assert candidate['source']['point_sha256']==sha(point_path)
assert candidate['players']==6 and candidate['labels']==[f'A{i}' for i in range(1,7)]+[f'T{i}' for i in range(1,7)]
expected=defaultdict(F);source_actual=[F(0)]*6;hist_count=positive_hist=0
for col in point['columns']:
    if col['kind']!='hist':continue
    hist_count+=1
    mass=F(col['weight']);assert mass>=0
    assert col['d']==1 and sum(col['hist'])==6 and sum(col['hist'][4:])==1
    a=tuple(map(int,col['actual_bits']));mask=sum(bit<<i for i,bit in enumerate(a))
    for i,bit in enumerate(a):
        if bit:source_actual[i]+=mass*F(1,sum(a))
    if not mass:continue
    positive_hist+=1
    for t in range(6):expected[mask|(1<<(6+t))]+=mass/6
assert hist_count==16 and positive_hist==10 and len(expected)==48 and sum(expected.values())==1
den=lcm(*(v.denominator for v in expected.values()))
raw={mask:int(mass*den) for mask,mass in expected.items()}
common_gcd=reduce(gcd,raw.values())
counts={mask:value//common_gcd for mask,value in raw.items()}
N=sum(counts.values())
assert str(den)==candidate['rational_denominator_before_gcd'] and str(common_gcd)==candidate['integer_common_gcd_removed']
assert N==int(candidate['unit_customers']) and N.bit_length()==261
observed={}
for rec in candidate['nonzero_customer_types']:
    mask,m=rec['mask'],int(rec['integer_clones'])
    assert mask not in observed and m>0
    assert rec['members']==[candidate['labels'][j] for j in range(12) if mask&(1<<j)]
    assert F(m,N)==F(rec['normalized_mass'])==expected[mask]
    assert (mask>>6).bit_count()==1 and 0<mask<4096
    observed[mask]=m
assert observed==counts
topic_counts=[sum(m for mask,m in counts.items() if mask&(1<<j)) for j in range(12)]
assert topic_counts[6:]==[N//6]*6 and sum(topic_counts[6:])==N
W=sum(m for mask,m in counts.items() if mask&63)
actual=[sum((F(m,(mask&63).bit_count()) for mask,m in counts.items() if mask&(1<<j)),F(0)) for j in range(6)]
assert [u/N for u in actual]==source_actual and sum(actual)==W
assert F(W,N)==F(point['W'])<F(1,2)
saved=candidate['static_verification']
assert str(W)==saved['target_W'] and str(N)==saved['OPT6']
assert list(map(str,actual))==saved['target_actual_utilities']
assert list(map(str,topic_counts))==saved['topic_unit_customers']
assert candidate['target_terminal_counts']==[1]*6+[0]*6
assert candidate['specified_actual_order']==candidate['labels'][:6]
assert saved['terminal_count_states']==comb(17,6)==12376
assert saved['all_count_states']==comb(18,6)==18564
assert saved['all_count_terminal_containment_pairs_upper_bound']==comb(29,6)==475020
result={'status':'PASS','candidate_sha256':sha(candidate_path),'source_point_sha256':sha(point_path),
        'players':6,'common_labeled_catalog_size':12,'positive_integer_customer_types':48,
        'unit_customers':str(N),'OPT6':str(N),'OPT6_certificate':'Six T labels partition every unit customer exactly once.',
        'target_W_over_OPT6':str(F(W,N)),'source_actual_utilities_preserved':True,
        'scope':'A newly specified finite unit game realizing only the actual and six optimal marginals. No SPE outcome or B/C/R/Z realization asserted; failure does not exclude other or larger catalogs.',
        'verifier_sha256':sha(Path(__file__))}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
