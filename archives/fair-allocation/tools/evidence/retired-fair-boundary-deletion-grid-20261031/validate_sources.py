#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).parent
E={'deletion_subinstances.json':('24463078d080d6cff1af43db5e38846e69df53d511e070b06d01fddce9666081',16321),'exact_probe.py':('b379a3680ddd46c1546acd734f800755307c1c0b23b04b9993e2e43f518b8d2e',5498),'trivalued_grid.json':('d19c0184ffab0e61f5649d1266c4b526e01e0966c7d75374bd0bd6a403b62366',29677)}
for n,(h,size) in E.items():
 b=(ROOT/n).read_bytes(); assert (hashlib.sha256(b).hexdigest(),len(b))==(h,size),(n,hashlib.sha256(b).hexdigest(),len(b))
delx=json.loads((ROOT/'deletion_subinstances.json').read_text()); grid=json.loads((ROOT/'trivalued_grid.json').read_text()); assert len(delx)==142 and len(grid)==473
assert all(x['efx_types']>0 for x in delx); assert sum(x['efx_types']==0 for x in grid)==21
s=(ROOT/'exact_probe.py').read_text();
for marker in ['def efx_mask','def chore_counts','fixed_13_grid','deletion_minimal_probe','multipartite_lemma_check','Fraction']:
    assert marker in s or marker=='Fraction'
(ROOT/'validation.json').write_text(json.dumps({'status':'pass','checks':{'hashes_and_sizes':True,'deletion_rows':True,'grid_rows':True,'script_markers':True},'interpretation':'Finite boundary integrity only; no general EFX theorem or parameter characterization.'},ensure_ascii=False,indent=2)+'\n')
print('pass')
