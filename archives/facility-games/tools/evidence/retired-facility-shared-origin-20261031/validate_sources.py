#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).parent
E={'facility_publication_benchmark.md':('581a208ef5b9d1033fa0ea6b3ea12c68c8fa262ca03bb47eb2fbd519e47228ee',13611,['SPARSE-RHO-ALL','Algorithmica','Krogmann 博士论文']), 'near_band_origin.md':('aae5aba6059cd39da15c0a31f1b346f8c05c11b444506a5aec3db02ab74fec68',834,['近带补全','EPTAS','不是来自公开文献']), 'strong_chord_existence.md':('f4a9d7b612aa12e723dc75c85b48dbb6368a6b64504a230d0ef292041c5986fe',13029,['Arbitrary finite shared-client cross-chord lemma','maximum-square','bad positive gap'])}
for n,(h,size,marks) in E.items():
 b=(ROOT/n).read_bytes(); assert (hashlib.sha256(b).hexdigest(),len(b))==(h,size),(n,hashlib.sha256(b).hexdigest(),len(b)); s=b.decode(); assert all(m in s for m in marks)
(ROOT/'validation.json').write_text(json.dumps({'status':'pass','checks':{'hashes_and_sizes':True,'origin_markers':True},'interpretation':'History/proof-origin integrity only; no external priority or global theorem certification.'},ensure_ascii=False,indent=2)+'\n')
print('pass')
