#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).parent
E={
 'toy_checks.py':('0dd9b02ab90c72c308186f73ff94f315d2b6953ea3e1340b20a86fbab7b4cb22',4225,['ordered_ef1_witness','copies_allocations','sd_witnesses','key_search']),
 'copies_exhaustive.py':('f9bfecf8ad21c76b61db78709e5343b909bc304a07507ba456a32cdfac9c173d',1562,['profiles_checked','minimum_witness_count','all_instances_have_sd_ef1']),
 'rank_toys.py':('878e8f5fccf285c7fd86421250229e6045a5c9813555da55dde0b200f4fa5c6e',1764,['rank_tables','allocations','residual','counterexample']),
}
for n,(h,size,markers) in E.items():
 b=(ROOT/n).read_bytes(); assert (hashlib.sha256(b).hexdigest(),len(b))==(h,size),(n,hashlib.sha256(b).hexdigest(),len(b))
 s=b.decode(); assert all(m in s for m in markers),(n,[m for m in markers if m not in s])
(ROOT/'validation.json').write_text(json.dumps({'status':'pass','checks':{'hashes_and_sizes':True,'implementation_markers':True},'interpretation':'Source/script integrity only; finite checker behavior does not establish universal fairness claims.'},ensure_ascii=False,indent=2)+'\n')
print('pass')
