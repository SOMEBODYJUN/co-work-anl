#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).parent
E={'two_ray_search.py':('040f906afa36709a80c8848ed0b0a692830a653bcc3719b23f54036a481d26f4',1517,['linprog','counterexamples','two nonnegative resource rays']), 'two_ray_search.json':('216c1a17aa1e11d5d5c7ca834d608453192efb9fe80d34a3ad14f41b88a833ed',126,[]), 'two_class_attack.py':('affd74711e28905c7d322a35e75159f6411e5c6d2c78ea620d7f8e38ca1fc03f',3989,['def solve','uniform_subsupport','def poisson','finite weight LP'])}
for n,(h,size,marks) in E.items():
 b=(ROOT/n).read_bytes(); assert (hashlib.sha256(b).hexdigest(),len(b))==(h,size),(n,hashlib.sha256(b).hexdigest(),len(b)); s=b.decode(); assert all(m in s for m in marks)
d=json.loads((ROOT/'two_ray_search.json').read_text()); assert d['seed']==20261020 and d['trials']==300 and d['counterexamples']==[] and 'not exhausted' in d['scope']
(ROOT/'validation.json').write_text(json.dumps({'status':'pass','checks':{'hashes_and_sizes':True,'ray_result_fields':True,'script_markers':True},'interpretation':'Finite numerical integrity only; no weighted-congestion theorem or universal gap proof.'},ensure_ascii=False,indent=2)+'\n')
print('pass')
