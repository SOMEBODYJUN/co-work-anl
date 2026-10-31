#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).parent
E={'tiny_home_k2_exact_v3.md':('cc9d1037da7e86c74226968b890eaad6e646c4179bf16fe789a776818d2b6c39',2124,['UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-19-10-APPROX-v3','Cmax≤19/10','k≥2']), 'tiny_home_k2_exact_v4.md':('8948b47cc8b2f303f7f1446ecb0137da163d0b65e906ec4169c5f85294ef877d',2486,['v4','k=1','Cmax≤19/10','OPEN']), 'tiny_home_k2_refinement_proof_v3.md':('ba7556c84d8ce5759c66fd840448085e94c435a94723573d76d73f9f5530b877',3235,['曲率','ν≤1/(16384k²)','Fraction','新颖性未认证'])}
for n,(h,size,marks) in E.items():
 b=(ROOT/n).read_bytes(); assert (hashlib.sha256(b).hexdigest(),len(b))==(h,size),(n,hashlib.sha256(b).hexdigest(),len(b)); s=b.decode(); assert all(m in s for m in marks)
(ROOT/'validation.json').write_text(json.dumps({'status':'pass','checks':{'hashes_and_sizes':True,'candidate_scope_markers':True},'interpretation':'Candidate/domain/proof-integrity only; no general UM theorem, software verification, novelty or external certification.'},ensure_ascii=False,indent=2)+'\n')
print('pass')
