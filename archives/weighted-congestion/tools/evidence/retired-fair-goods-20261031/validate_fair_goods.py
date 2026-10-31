#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).parent
expected={
 'candidate_report.md':('9496a71413fbf3b3511dea555117c317ffbf26b1623aaaa99e543be3d69cc1f5',18369,['FG01','FG02','Paper Fact','新颖性认证']),
 'candidates.json':('89442a34791086e3030aeb5b21e264bfe8bf267d23ee7646adc7d6030fe77c32',25477,['FG01','FG02']),
}
checks={}
for name,(h,size,markers) in expected.items():
 p=ROOT/name;b=p.read_bytes();t=b.decode();assert len(b)==size;assert hashlib.sha256(b).hexdigest()==h
 for m in markers:assert m in t,(name,m)
 checks[name]={'sha256':h,'size':size,'markers':markers}
d=json.loads((ROOT/'candidates.json').read_text());assert isinstance(d,dict) and isinstance(d.get('candidates'),list) and len(d['candidates'])>=8
v=json.loads((ROOT/'independent_scalar_verification.json').read_text());assert len(v)==5 and all(x['matches_frozen'] for x in v);assert [x['scalar_witness_count'] for x in v]==[6,256,26,106,9]
checks['independent_scalar_verification.json']={'sha256':hashlib.sha256((ROOT/'independent_scalar_verification.json').read_bytes()).hexdigest(),'size':(ROOT/'independent_scalar_verification.json').stat().st_size,'rows':len(v),'scalar_witness_counts':[x['scalar_witness_count'] for x in v],'matches_frozen':True}
m=json.loads((ROOT/'manifest.json').read_text());m['validation']=checks;(ROOT/'validation.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');print(json.dumps(checks,ensure_ascii=False,indent=2))
