"""Exact arithmetic for one primary PI certificate; reuse prior full-SPE/OPT run, no strategy search/rerun."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations_with_replacement
from collections import Counter
import json,hashlib
E=Path(__file__).resolve().parent;rows=json.loads((E/'source-manifest.json').read_text());src=next(x for x in rows if x['id']=='73bc0f6d20fe90dbd39c');path=E/'original'/src['path'];assert hashlib.sha256(path.read_bytes()).hexdigest()==src['sha256'];d=json.loads(path.read_text());inst=d['instance'];customers=[(frozenset(x['topics']),x['multiplicity'])for x in inst['customers']];assert sum(w for _,w in customers)==430
expected={frozenset(q):w for leaf in [1,2,4,5]for q,w in [([leaf],55),([0,leaf],15),([3,leaf],15),([0,3,leaf],21)]};expected[frozenset([1,2,4,5])]=6;assert dict(customers)==expected
reuse=json.loads((E/'reused-validation-manifest.json').read_text());ex=json.loads((E/'reused-pi-sanity-validation/execution.json').read_text());trace=json.loads((E/'reused-pi-sanity-validation/execution-state.json').read_text());prior=trace['completed_original_report'];assert reuse['input_sha256']==src['sha256']==ex['true_external_inputs'][0]['sha256']and ex['returncode']==0;assert prior['ordered_histories']==43 and prior['IC_comparisons']==258 and prior['actual_u']==['91','91','83']and prior['OPT']==324
H=[sum((F(1,j)for j in range(1,c+1)),F())for c in range(5)]
def phi(profile):return sum((w*H[sum(a in likes for a in profile)]for likes,w in customers),F())
result={};buckets=[]
for r in [3,4]:
 profiles=list(combinations_with_replacement(range(6),r));values=[phi(z)for z in profiles];best=max(values);maximizers=[list(z)for z,v in zip(profiles,values)if v==best];groups={}
 for z,v in zip(profiles,values):
  count=Counter(z);key=(tuple(sorted([count[0],count[3]],reverse=True)),tuple(sorted([count[i]for i in [1,2,4,5]],reverse=True)))
  if key in groups:assert groups[key]['value']==v;groups[key]['multiplicity']+=1
  else:groups[key]={'value':v,'multiplicity':1}
 for (center,leaf),g in sorted(groups.items(),reverse=True):buckets.append({'slots':r,'sorted_centers':list(center),'sorted_leaves':list(leaf),'potential':str(g['value']),'orbit_profiles':g['multiplicity']})
 result[str(r)]={'multiset_profiles':len(profiles),'symmetry_buckets':len(groups),'maximum_potential':str(best),'maximizers_as_sorted_topics':maximizers,'stored_maximizer_counts':d['potential_maximizers'][str(r)]}
 target=tuple(i for i,c in enumerate(d['potential_maximizers'][str(r)])for _ in range(c));assert len(target)==r and phi(target)==best
assert result['3']['maximum_potential']==d['P_r']=='329'and result['4']['maximum_potential']==d['P_r1']=='873/2';gap=F(d['P_r1'])-F(d['P_r'])-F(d['exact_root_payoff']);assert gap==F(d['delta_minus_root'])==F(33,2)
rootmenus=sorted((q for q in trace['query_menus']if q['role']==0),key=lambda q:q['action']);assert len(rootmenus)==6 and all(q['D']=='91'for q in rootmenus)
K=[[sum((F(w,1+sum(a in likes for a in menu['leaf']))for likes,w in customers if query in likes),F())for menu in rootmenus]for query in range(6)];assert max(map(max,K))==90
background=(0,0,3);pure_values=[sum((F(w,1+sum(a in likes for a in background))for likes,w in customers if query in likes),F())for query in range(6)];assert max(pure_values)==F(315,4)<91
out={'scope':'one exact already stored PI input, new closed arithmetic only: harmonic maxima at182 multiset profiles and42 explicit query sums; fullSPE/OPT validation reused, no original program/LP/SPE solver rerun','input_sha256':src['sha256'],'new_original_program_calls':0,'new_full_SPE_checks':0,'reused_SPE_IC_count':258,'reused_OPT_multiset_profiles':56,'prior_full_validation_execution':ex['start_utc'],'unit_customers':430,'types':17,'actual':prior['actual'],'actual_u':prior['actual_u'],'W':prior['W'],'OPT3':prior['OPT'],'minimum_full_IC_slack':'0 (prior nonnegative IC plus prescribed self rows)','harmonic':result,'symmetry_buckets':buckets,'next_increment':str(F(d['P_r1'])-F(d['P_r'])),'PI_gap':str(gap),'full_root_K':[[str(x)for x in row]for row in K],'max_full_root_K':'90','root_u':'91','WP_at_this_input':'every full root K entry<=90<91, so all-pWP holds strictly here; distinct from the bank counterfamily','pure_background':list(background),'pure_background_query_values':list(map(str,pure_values)),'pure_background_max':'315/4','pure_background_scope':'one 3-slot legal pure background upper witness, not a new scan of the free safety optimum'}
(E/'pi-certificate-arithmetic.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'P3':result['3'],'P4':result['4'],'buckets':len(buckets),'PI_gap':str(gap),'maxK':90,'pureBackgroundMax':str(max(pure_values))},ensure_ascii=False))
