"""Full ordered SPE semantic replay for the core root-envelope projections.

Finite implementation check, not a proof of HALF(5) or an independent review.
"""
from pathlib import Path
import json
from audit_root_copy_rows import check
from core_envelope_pricing import Universe
if __name__=='__main__':
    inputs=[[set()],[set(),{0},{0,1},{1,2}],[set(range(5)),{5},{6},{7},{8}],[{0,1},{1,2},{0,2,3},{3,4},{0,2,4}]]
    cases=[check(t,Universe,False) for t in inputs]
    result={'status':'passed','scope':__doc__,'cases':cases}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'passed','cases':len(cases),'full_IC':sum(c['full_IC'] for c in cases),'rows_per_nonempty_input':cases[-1]['rows']}))
