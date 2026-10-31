#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).parent
expected={
 'rank2_two_classes_lemma.md':('12b9460d10d35f9129395803331ce7c617ac04fd05bbf54f8ee56115840c3558',4551,['FC-LEMMA-R2-2C-v1','EF','EFX','全局未匹配 item']),
 'candidate_report.md':('344c42c2575cd0ec70b0d858c5ef3e63fcd5dd2e0272d57ad4fb2ffe05fcb752',21813,['FC-01','FC-02','未认证新颖性','FC-LEMMA-R2-2C-v1']),
}
checks={}
for name,(h,size,markers) in expected.items():
 p=ROOT/name;b=p.read_bytes();t=b.decode();assert len(b)==size;assert hashlib.sha256(b).hexdigest()==h
 for m in markers:assert m in t,(name,m)
 checks[name]={'sha256':h,'size':size,'markers':markers}
d=json.loads((ROOT/'candidates.json').read_text());assert d['recommendation']==['FC-01','FC-02'];assert d['local_progress'][0]['id']=='FC-LEMMA-R2-2C-v1'; assert len(d['candidates'])>=8
checks['candidates.json']={'sha256':hashlib.sha256((ROOT/'candidates.json').read_bytes()).hexdigest(),'size':(ROOT/'candidates.json').stat().st_size,'recommendation':d['recommendation'],'candidate_count':len(d['candidates'])}
m=json.loads((ROOT/'manifest.json').read_text());m['validation']=checks;(ROOT/'validation.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');print(json.dumps(checks,ensure_ascii=False,indent=2))
