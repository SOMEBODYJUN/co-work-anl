#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).parent
expected={
 'AGENTS.md':('75c4b78a9bdd984058cdb61cad58bd2c98bd88068a53ae19e5bb0eb76652b6ca',2316,['当前主攻是 UM-TARGET-v1','旧Cd/ln d命题现已被否定','新数学结果']),
 'PROTOCOL.md':('eeb8a5fb6b5629c384e5fa9d6c26615313d8fe2e46b92f63f7ee897a380697ca',3249,['共同研究与异步研讨','main','wcg/board','不产生排他研究权']),
 'README.md':('2571ddf90cd15c01f7fb1fe1bbcfee7f5007de5a4bb7165de079c45c4785f4a9',2875,['加权拥塞独立旧题与共享协作程序','WC-TARGET v1','线性全状态否定证明','外部同行评审'])
}
checks={}
for name,(h,size,markers) in expected.items():
 p=ROOT/name;b=p.read_bytes();t=b.decode();assert len(b)==size;assert hashlib.sha256(b).hexdigest()==h
 for m in markers:assert m in t,(name,m)
 checks[name]={'sha256':h,'size':size,'markers':markers,'classification':'historical model/tooling context; no new theorem inferred'}
m=json.loads((ROOT/'manifest.json').read_text());m['validation']=checks;(ROOT/'validation.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');print(json.dumps(checks,ensure_ascii=False,indent=2))
