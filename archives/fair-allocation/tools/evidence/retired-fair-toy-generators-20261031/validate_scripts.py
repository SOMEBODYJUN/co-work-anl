#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).parent
E={
 'construct_rank2.py':('3e109ea30d7bb8c42e301807a29f48243145628b8b674a610516fbf0fa2a95fa',3982,['missing_word','matching','construct','assert efx and (m<n or ef)']),
 'mixed_extension_toys.py':('d7e70c77f3c3fd5c6d2714a468d5e674b45ad7025e65bc2425561bb6da07719f',1081,['mixed_efx','cycle_trials','orient','counterexample_to_universal_EFXplus0']),
 'rank2_cap_toys.py':('7d429375b6998aeb0bbff5906eae77a86c0d1310ca2cc579afc74e77f2d61735',844,['rank_tables','np.minimum','rank_cap','allocations']),
}
for n,(h,size,marks) in E.items():
 b=(ROOT/n).read_bytes(); assert (hashlib.sha256(b).hexdigest(),len(b))==(h,size),(n,hashlib.sha256(b).hexdigest(),len(b))
 s=b.decode(); assert all(m in s for m in marks),(n,[m for m in marks if m not in s])
(ROOT/'validation.json').write_text(json.dumps({'status':'pass','checks':{'hashes_and_sizes':True,'implementation_markers':True},'interpretation':'Source/script integrity only; dependencies and finite checks do not establish universal fairness theorems.'},ensure_ascii=False,indent=2)+'\n')
print('pass')
