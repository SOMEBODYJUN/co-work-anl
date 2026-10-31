#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).parent
E={
 'toy_search.py':('f25aa4dfe14f3f4a789c45b58fd73fd8b9a4907369de7f46fcaed29c025351e4',4995,['equal_partitions','mms_trials','mixed_efx','cycle_trials','optimal_alpha_demo']),
 'cross_field_toy_checks.py':('8fc46c77f144bfbac88d597086ed29356dedece7b68090cb380875b16bd14288',5161,['copies_sd_ef1','rank2_exact','key8_random','word_multisets_tested']),
 'verify_frozen.py':('ff19f582a7bbac8d5087f6b5a0e33cd9f54984415cf5bebf2e3b02cf0a3070b5',2111,['scalar_witness_count','matches_frozen','minimum_witness_count']),
}
for n,(h,size,marks) in E.items():
 b=(ROOT/n).read_bytes(); assert (hashlib.sha256(b).hexdigest(),len(b))==(h,size),(n,hashlib.sha256(b).hexdigest(),len(b))
 s=b.decode(); assert all(m in s for m in marks),(n,[m for m in marks if m not in s])
(ROOT/'validation.json').write_text(json.dumps({'status':'pass','checks':{'hashes_and_sizes':True,'implementation_markers':True},'interpretation':'Script integrity and marker checks only; finite checker semantics are not universal theorem proofs.'},ensure_ascii=False,indent=2)+'\n')
print('pass')
