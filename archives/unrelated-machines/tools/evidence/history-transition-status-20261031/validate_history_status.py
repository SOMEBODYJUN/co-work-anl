#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).parent
expected={
 'FAILED_ROUTES.md':('af6f1aedf79a2ebd238037f6c1f68ba15e493aadc3b3a7a83255772dd7055aad',47885,19,['失败路线与准确否定范围','冻结宏任务后重开全部微任务仍不足','既定条件矩运输不能免费视为同层重置','同资源正权畸变有界的flat源不能靠增加菜单数放大']),
 'README.md':('464532a4f15c35677c6abf7f3538a36a295da69eb83b11372392dc78b4910894',42186,12,['共同研究：一般不相关并行机的统一常数2壁垒','研究目标与当前前沿','全局分配矩的可提取条件','UM-TARGET-v1']),
 'RESEARCH_STATE.md':('a7da843a169b705c4c6061f9c960122f190c7371c125aaa0e043f5f4f1781f7e',46236,21,['当前研究前沿：不相关并行机','当前承重义务','全局四阶分配矩的新增义务','本阶段的可复用桥梁与仍开放的主目标'])
}
checks={}
for name,(h,size,heads,markers) in expected.items():
 p=ROOT/name;b=p.read_bytes();t=b.decode(); assert len(b)==size; assert hashlib.sha256(b).hexdigest()==h; assert len(re.findall(r'^#+ ',t,flags=re.M))==heads
 for m in markers: assert m in t,(name,m)
 checks[name]={'sha256':h,'size':size,'headings':heads,'markers':markers,'classification':'historical route/status/failure context; no theorem inferred'}
m=json.loads((ROOT/'manifest.json').read_text());m['validation']=checks;(ROOT/'validation.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');print(json.dumps(checks,ensure_ascii=False,indent=2))
