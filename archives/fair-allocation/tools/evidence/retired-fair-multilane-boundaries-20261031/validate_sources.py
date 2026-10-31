#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).parent
E={
 'chores_trivalued_exact_boundary.md':('f065820a5b36deb16e1c87187faa77dc056434769a00a00f2aa53d29f810bb2e',4769,['SEL-CHORES-TRIVALUED-AUDIT-v1','62720','23/22','142','473']),
 'chores_trivalued_type_audit.py':('1145b46f785fa3c8eaffc8abd2257fcf55fbbcbc591cb5c88fc6dd3801c3f731',7039,['solve_types','solve_labelled','Fraction','invalid_inputs_rejected','published-instance reproduction']),
 'fair_fpo_compatibility_boundary.md':('5a64414593b129da01a864942a27017c053878fd77e2ec648ce13eccc36b7046',3701,['SEL-FAIR-FPO-PROBE-v1','A=B=2','10/11','256','1600']),
}
for n,(h,size,marks) in E.items():
 b=(ROOT/n).read_bytes(); assert (hashlib.sha256(b).hexdigest(),len(b))==(h,size),(n,hashlib.sha256(b).hexdigest(),len(b))
 s=b.decode(); assert all(m in s for m in marks),(n,[m for m in marks if m not in s])
(ROOT/'validation.json').write_text(json.dumps({'status':'pass','checks':{'hashes_and_sizes':True,'semantic_markers':True},'interpretation':'Source and implementation integrity checks only; finite observations and known counterexamples are not universal theorem proofs.'},ensure_ascii=False,indent=2)+'\n')
print('pass')
