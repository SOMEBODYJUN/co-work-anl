#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).parent
E={'fair_fpo_independent.py':('182a7bbff5f36771281b9272606da8ad7163acae73089462a7cbb0abf9b6ca2e',4649,['support_fpo','domination_fpo','checked_instances','paper_counterexample']), 'probe_results.json':('5aca6a807c1134a43e2506d25df9f9067c80f2bac6d38e3fdbdeb5cc11fb9e74',1020,[]), 'personalized_efx_completion_independent.py':('b94cbc26e72d1acc9ff2dbaf33ac40d8e42a302e947fe3fd487333962cf2bfc0',4034,['def audit','completion_failure','Fraction','family_checks'])}
for n,(h,size,marks) in E.items():
 b=(ROOT/n).read_bytes(); assert (hashlib.sha256(b).hexdigest(),len(b))==(h,size),(n,hashlib.sha256(b).hexdigest(),len(b))
 s=b.decode(); assert all(m in s for m in marks)
p=json.loads((ROOT/'probe_results.json').read_text()); assert p['he_tao_reproduction']['allocation_types']==62720 and p['he_tao_reproduction']['efx_types']==0; assert p['fixed_13_grid']['points']==473 and p['fixed_13_grid']['nonexistence_points']==21; assert p['deletion_minimal_probe']['instances']==142 and p['deletion_minimal_probe']['nonexistence_instances']==[]; assert p['multipartite_lemma_check']['cases']==343536 and p['multipartite_lemma_check']['failures']==0
(ROOT/'validation.json').write_text(json.dumps({'status':'pass','checks':{'hashes_and_sizes':True,'probe_output_fields':True,'script_markers':True},'interpretation':'Finite exact integrity only; fPO/EFX+PO general claims remain open or refuted only where explicitly stated.'},ensure_ascii=False,indent=2)+'\n')
print('pass')
