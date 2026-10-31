#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).parent
E={'normal_form_exact_v1.md':('33094582e9804d6a0a7aaa78122b5eac90e2fb65e5d9089aa939b7b618092a29',5108,['三态','资源度三','Exact Statements','Partial Decoder']), 'normal_form_proof_v1.md':('079dfbfd274eb503db6e1e7410a251fa146f15be0c12941f235e6224591d9b28',7203,['正值分配','任意中间target actual','OPT2','精确规模']), 'normal_form_independent_review_v1.md':('642049e4d872554efad0d8ebb5398713a922ca0524a80f1a33070407e8e9fa3d',10419,['Exact-first','无fatal','全部incidence jobs','独立重证'])}
for n,(h,size,marks) in E.items():
 b=(ROOT/n).read_bytes(); assert (hashlib.sha256(b).hexdigest(),len(b))==(h,size),(n,hashlib.sha256(b).hexdigest(),len(b)); s=b.decode(); assert all(m in s for m in marks)
(ROOT/'validation.json').write_text(json.dumps({'status':'pass','checks':{'hashes_and_sizes':True,'normal_form_markers':True},'interpretation':'Exact/proof/review integrity only; restricted normalized-flat source, no general UM theorem or novelty certification.'},ensure_ascii=False,indent=2)+'\n')
print('pass')
