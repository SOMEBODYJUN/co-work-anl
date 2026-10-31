#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).parent
E={'combinatorial_submodular_k2k.py':('936eda8b34beca49b6f0b76a0914592e2ca993b4f09f2378569054c7b5f3888b',1845,['def nullity','def ratio','def enum_rank','SLSQP']), 'combinatorial_submodular_k2k_results.json':('b81d695f184a4d4930b3ccc045fe38f86c946156222e703d5505a55d92c5e62a',7476,[])}
for n,(h,size,marks) in E.items():
 b=(ROOT/n).read_bytes(); assert (hashlib.sha256(b).hexdigest(),len(b))==(h,size),(n,hashlib.sha256(b).hexdigest(),len(b)); s=b.decode(); assert all(m in s for m in marks)
d=json.loads((ROOT/'combinatorial_submodular_k2k_results.json').read_text()); assert d['status']=='finite numerical evidence, not proof'; assert [x['k'] for x in d['base_optimizations']]==list(range(2,17)); assert len(d['rank_checks'])==16; assert max(x['error'] for x in d['rank_checks'])<=1e-10
(ROOT/'validation.json').write_text(json.dumps({'status':'pass','checks':{'hashes_and_sizes':True,'optimization_rows':True,'rank_checks':True},'interpretation':'Finite numerical integrity only; no global optimization or asymptotic theorem.'},ensure_ascii=False,indent=2)+'\n')
print('pass')
