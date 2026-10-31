#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).parent
E={'facility_journal_handoff.md':('bd423a4a1a24d2ce9aa78d3e4d0d6768772211634a9c7eaf54af439e921e04a2',9385,['SC-PHI-E/A','SPARSE-RHO-ALL','HC-2']), 'facility_publication_assessment_2026-10-01.md':('8d1ee7fe9f3a9e15cb8d1d6917757cc3d550594084e4ccfc9ce2714716ffa4ba',14967,['What the new theorem changes','SPARSE-RHO-ALL','No surviving fatal objection']), 'facility_publication_assessment_2026-10-06.md':('e2bbfb8692f9940fe4d171375504bbf09b0605c86263b7573ab6cde528f8f992',12375,['SC-PHI-E/A','SPARSE-RHO-ALL','不是外部同行评审','MF-PURE-CAP-POLY'])}
for n,(h,size,marks) in E.items():
 b=(ROOT/n).read_bytes(); assert (hashlib.sha256(b).hexdigest(),len(b))==(h,size),(n,hashlib.sha256(b).hexdigest(),len(b)); s=b.decode(); assert all(m in s for m in marks)
(ROOT/'validation.json').write_text(json.dumps({'status':'pass','checks':{'hashes_and_sizes':True,'assessment_markers':True},'interpretation':'Historical contribution/venue integrity only; no theorem, novelty or acceptance certification.'},ensure_ascii=False,indent=2)+'\n')
print('pass')
