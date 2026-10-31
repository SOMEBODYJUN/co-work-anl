#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).parent
p=ROOT/'COST_CHERNOFF_COROLLARY_CHECK.md'; b=p.read_bytes(); assert hashlib.sha256(b).hexdigest()=='2fed2a5ebf098fe9777af2c2f52fbeb533a0afc82f200718e56a7e86ace65432' and len(b)==3777
s=b.decode();
for marker in ['LIKELY_STANDARD_COROLLARY_PENDING_CHECK','Swamy–Traub','R={v:','SwapRounding','不宣称已解决原问题']:
    assert marker in s, marker
(ROOT/'validation.json').write_text(json.dumps({'status':'pass','checks':{'hash_and_size':True,'audit_markers':True},'interpretation':'Marker/integrity checks only; proof and oracle assumptions remain unaudited.'},ensure_ascii=False,indent=2)+'\n')
print('pass')
