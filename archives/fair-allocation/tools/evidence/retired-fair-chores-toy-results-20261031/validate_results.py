#!/usr/bin/env python3
import hashlib, json
from pathlib import Path
ROOT=Path(__file__).parent
EXPECTED={
 'rank_toy_results.json':('c55c56b356811fea08ec04548a0ad3aff51ec40f8def5411fe873e31b7972a3e',1133),
 'toy_results.json':('3a097378f4b2e209ac1d9c34c6317bb626617b74c557b2e9931d49969b3a9251',2370),
}
def read(n):
 p=ROOT/n;b=p.read_bytes(); h=hashlib.sha256(b).hexdigest(); assert (h,len(b))==EXPECTED[n],(n,h,len(b)); return json.loads(b)
rank=read('rank_toy_results.json'); assert len(rank)==5
assert [(r['n'],r['m'],r['number_of_classes'],r['loops'],r['completed_trials'],r['allocations_per_profile'],r['counterexample']) for r in rank]==[
 (3,8,2,False,1000,6561,None),(3,9,2,True,500,19683,None),(3,8,3,False,1000,6561,None),(3,8,3,True,1000,6561,None),(4,7,2,True,500,16384,None)]
for r in rank: assert r['requested_trials']==r['completed_trials']
toy=read('toy_results.json'); assert set(toy)=={'mms','mixed_graphs','discarded_alpha_idea'}
assert len(toy['mms'])==3 and all(x['n']==3 and x['q']==3 and x['requested_trials']==x['completed_trials']==10000 and x['unlabelled_partitions']==280 and x['labelled_allocations']==1680 and x['first_failure'] is None for x in toy['mms'])
assert [x['values'] for x in toy['mms']]==[[0,1,2],[1,2,3],[1,2,5]]
mg=toy['mixed_graphs']; assert [(x['vertices'],x['profiles_checked'],x['exhaustive'],x['no_EFXplus0_witness']) for x in mg]==[(3,64,True,None),(4,256,True,None),(5,1024,True,None),(5,10000,False,None)]
a=toy['discarded_alpha_idea']; assert a['delta']==5 and a['minimum_social_cost']==5 and len(a['optimal_allocations'])==2
(ROOT/'validation.json').write_text(json.dumps({'status':'pass','checks':{'hashes_and_sizes':True,'rank_toy_shape':True,'mms_shape':True,'mixed_graph_shape':True,'alpha_boundary_shape':True},'interpretation':'Shape/integrity only; finite no-failure records and discarded finite checks are not universal fairness proofs.'},ensure_ascii=False,indent=2)+'\n')
print('pass')
