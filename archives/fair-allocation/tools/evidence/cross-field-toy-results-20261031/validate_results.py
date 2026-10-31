#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).parent
p=ROOT/'toy_results.json'; b=p.read_bytes(); assert hashlib.sha256(b).hexdigest()=='decc0be5a91c19a267ce46dac06f3a26cb5b537d5fd8ef8ef5e7f23260efd75c' and len(b)==665
d=json.loads(b)
assert d['copies_sd_ef1']=={'n':3,'types':4,'strict_profiles_mod_type_relabeling':9216,'allocations_per_profile':81,'counterexamples':0}
assert d['rank2_chore_EF']=={'agents':3,'chores':[3,8],'word_multisets_tested':12825,'condition':'two loopless parallel classes per agent','EF_failures':0}
k=d['key8']; assert (k['agents'],k['goods'],k['categories'],k['complete_feasible_allocations'],k['seed'],k['valuation_range_inclusive'],k['random_profiles'],k['ordered_no_envy_and_EF1_failures'])==(4,8,[3,3,2],864,20261020,[0,20],1000,0)
(ROOT/'validation.json').write_text(json.dumps({'status':'pass','checks':{'hash_and_size':True,'copies_shape':True,'rank2_shape':True,'key8_shape':True},'interpretation':'Independent finite cross-field checks; model-specific evidence does not imply a cross-model theorem.'},ensure_ascii=False,indent=2)+'\n')
print('pass')
