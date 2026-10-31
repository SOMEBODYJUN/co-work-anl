#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).parent
E={'three_by_three.md':('93f130d6cd664b6b14f8103690c89b47633119bfd287bea4bfbd78cebbe5bba4',1590,['time limit / no incumbent','2.001','不是不可行证书']), 'facility_eptas_direction_debate.md':('a3835b7b3d89f6f9fde2583d1bf70b87867ba48446f3f8728808ae3e7a743a13',10372,['EPTAS','近带','没有把这变成已完成正式一般 EPTAS 定理']), 'facility_journal_decision.md':('cdadfa6bd8cbf21e9308ebe5e527e95bd2cabef55ea65f4b67fb681d309b70b9',7415,['Write two papers','Algorithmica','external peer review'])}
for n,(h,size,marks) in E.items():
 b=(ROOT/n).read_bytes(); assert (hashlib.sha256(b).hexdigest(),len(b))==(h,size),(n,hashlib.sha256(b).hexdigest(),len(b)); s=b.decode(); assert all(m in s for m in marks)
(ROOT/'validation.json').write_text(json.dumps({'status':'pass','checks':{'hashes_and_sizes':True,'history_markers':True},'interpretation':'Historical/editorial integrity only; no theorem/publication certification.'},ensure_ascii=False,indent=2)+'\n')
print('pass')
