#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path
ROOT=Path(__file__).parent
expected={
 'research_README.md':('536edcfcec96437f8d3d3e05ce21c977ba0169b1435fa41da0e4fed131dd98eb',13823,['UM-TARGET-v1','OPEN','独立审查','代码、输入、证书']),
 'REPOSITORY_GUIDE.md':('f526b91a05c1dc54081f2ffa10b31ddd17a22b1d04257c6395d02b5f70d58c33',6909,['仓库生产、读取与保存规则','Truth、Value、Novelty','checkpoint','冲突']),
 'ROADMAP.md':('56a7b63cb80a21040560da3fa6f7e7961077b8dceca606b8cb210cdaf864e53b',4645,['当前研究路线','共同相关性与真实容量','联合舍入与可终止修复','新表示的可计算桥梁'])
}
checks={}
for name,(h,size,markers) in expected.items():
 p=ROOT/name; b=p.read_bytes(); t=b.decode(); assert hashlib.sha256(b).hexdigest()==h; assert len(b)==size
 for m in markers: assert m in t,(name,m)
 checks[name]={'sha256':h,'size':size,'markers':markers,'classification':'historical navigation/operating context; no theorem inferred'}
manifest=json.loads((ROOT/'manifest.json').read_text()); manifest['validation']=checks; (ROOT/'validation.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n'); print(json.dumps(checks,ensure_ascii=False,indent=2))
