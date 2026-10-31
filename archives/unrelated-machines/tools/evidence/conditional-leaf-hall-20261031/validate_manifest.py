#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent;m=json.loads((root/'manifest.json').read_text());out={}
for s in m['sources']:
 p=root/s['export'];h=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
 out[s['id']]={'exists':p.exists(),'size':p.stat().st_size if p.exists() else None,'sha256':h,'matches_source':h==s['sha256']}
ok=all(v['exists'] and v['matches_source'] for v in out.values());r={'status':'pass' if ok else 'fail','checks':out};print(json.dumps(r,ensure_ascii=False,indent=2));(root/'validation.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');raise SystemExit(0 if ok else 1)
