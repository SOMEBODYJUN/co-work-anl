"""One fixed definition-level exact check of the saved distinct-topic policy.

No discovery code, canonical package, LP, RNG, or all-SPE solver is imported.
The nine-client alias point has a separate analytic all-history proof and is
not replayed here. All original action rows and integer customer types are used.
"""
from pathlib import Path
from itertools import product,combinations
from functools import lru_cache
from fractions import Fraction
from collections import Counter
from hashlib import sha256
import json

here=Path(__file__).resolve().parent
source=here/'original/research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/ordered_policy_mutation_distinct_best.json'
data=source.read_bytes()
assert sha256(data).hexdigest()=='3eb9352d28e19a6877082c73cee3772deb97f10a81180bd2831c91c0989c51b4'
d=json.loads(data);inst=d['instance'];k=7;m=5;L=60
assert inst['players']==m and inst['topics']==list(map(str,range(k)))
types=[]
for row in inst['customers']:
    topics=row['topics'];n=row['multiplicity']
    assert len(topics)==len(set(topics)) and all(type(a)is int and 0<=a<k for a in topics)
    assert type(n)is int and n>0
    types.append((sum(1<<a for a in topics),n))
assert len(types)==9 and len(set(mask for mask,n in types))==9
actions=d['strategy']['actions'];histories=[h for depth in range(m) for h in product(range(k),repeat=depth)]
assert [tuple(row['history']) for row in actions]==histories
assert all(set(row)=={'history','action'} and type(row['action'])is int and 0<=row['action']<k for row in actions)
sigma={tuple(row['history']):row['action'] for row in actions}
assert len(sigma)==len(histories)==2801
@lru_cache(None)
def finish(h):
    return h if len(h)==m else finish(h+(sigma[h],))
@lru_cache(None)
def payoff(leaf,a):
    value=0
    for mask,n in types:
        if mask>>a&1:
            den=sum(mask>>t&1 for t in leaf)
            assert 1<=den<=m and L%den==0
            value+=n*(L//den)
    return value
def welfare(labels):
    selected=sum(1<<a for a in set(labels))
    return sum(n for mask,n in types if mask&selected)
actual=finish(());q=[actual.count(a) for a in range(k)]
assert q==d['strategy']['terminal_counts']
counts=Counter();proper=Counter();bydepth={depth:Counter() for depth in range(m)};min_proper=None;minimizers=[];ties=[]
profiles=[]
for h in histories:
    chosen=sigma[h];leaf=finish(h);u=payoff(leaf,chosen)
    deviations=[payoff(finish(h+(a,)),a) for a in range(k)]
    slacks=[u-v for v in deviations]
    for a,s in enumerate(slacks):
        sign='positive' if s>0 else 'zero' if s==0 else 'negative'
        counts[sign]+=1;bydepth[len(h)][sign]+=1
        if a!=chosen:
            proper[sign]+=1
            if min_proper is None or s<min_proper:min_proper=s;minimizers=[{'history':list(h),'chosen':chosen,'deviation':a}]
            elif s==min_proper:minimizers.append({'history':list(h),'chosen':chosen,'deviation':a})
            if s==0:ties.append({'history':list(h),'chosen':chosen,'deviation':a})
    profiles.append({'history':list(h),'chosen':chosen,'actual_leaf':list(leaf),'payoff_scaled':u,'forced_payoffs_scaled':deviations,'slacks_scaled':slacks})
assert counts['negative']==proper['negative']==0
assert sum(counts.values())==19607 and sum(proper.values())==16806
W=welfare(actual);supports=[{'topics':list(J),'cover':welfare(J)} for J in combinations(range(k),m)]
OPT=max(x['cover'] for x in supports);ratio=Fraction(OPT,W)
assert ratio==Fraction(d['ratio'])
differences=[]
for a,b in combinations(range(k),2):
    distance=sum(n for mask,n in types if (mask>>a&1)!=(mask>>b&1))
    slack=1000*distance-W;assert distance>0 and slack>=0
    differences.append({'topics':[a,b],'symmetric_difference_clients':distance,'1000_distance_minus_W':slack})
static=[]
for i,a in enumerate(actual):
    old=payoff(actual,a)
    for alt in range(k):
        changed=actual[:i]+(alt,)+actual[i+1:]
        static.append({'position':i,'deviation':alt,'gain_scaled':payoff(changed,alt)-old})
profile_bytes=''.join(json.dumps(row,separators=(',',':'))+'\n' for row in profiles).encode()
(here/'fixed-distinct-all-history-profiles.jsonl').write_bytes(profile_bytes)
result={
 'status':'PASS','scope':'One fixed saved distinct-topic complete policy, exact integer scaled utilities; no original discovery replay or all-strategy enumeration',
 'input_sha256':sha256(data).hexdigest(),'players':m,'labelled_topics':k,'unit_clients':sum(n for mask,n in types),'positive_customer_types':len(types),
 'topic_cardinalities':[welfare([a]) for a in range(k)],'complete_histories':len(histories),'actual_ordered_path':list(actual),'terminal_counts':q,
 'actual_payoffs':[str(Fraction(payoff(actual,a),L)) for a in actual],'actual_welfare':W,'optimal_welfare':OPT,'ratio':str(ratio),'half_slack':2*W-OPT,
 'proper_comparisons':dict(proper),'inclusive_comparisons':dict(counts),'by_depth_inclusive':{str(k):dict(v) for k,v in bydepth.items()},
 'minimum_proper_slack':str(Fraction(min_proper,L)),'minimum_proper_slack_witnesses':minimizers,'proper_ties':ties,
 'all_21_comparison_supports':supports,'optimal_supports':[x['topics'] for x in supports if x['cover']==OPT],
 'all_21_pairwise_distinctions':differences,'minimum_pairwise_difference':min(x['symmetric_difference_clients'] for x in differences),
 'all_35_static_deviations':static,'maximum_static_gain':str(Fraction(max(x['gain_scaled'] for x in static),L)),
 'all_history_profiles_sha256':sha256(profile_bytes).hexdigest(),'all_history_profiles_bytes':len(profile_bytes),'utility_scale':L,
 'execution_counts':{'new_fixed_complete_check':1,'original_mutation_entrypoint':0,'Engine':0,'LP':0,'RNG':0,'canonical_package':0,'all_SPE_solver':0,'nine_client_replay':0}
}
print(json.dumps(result,ensure_ascii=False,indent=2))
