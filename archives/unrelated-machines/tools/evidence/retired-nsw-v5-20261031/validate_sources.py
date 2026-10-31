#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent;m=json.loads((root/'manifest.json').read_text());out={}
for s in m['sources']:
 p=root/s['evidence_file'];h=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
 out[s['evidence_file']]={'exists':p.exists(),'size':p.stat().st_size if p.exists() else None,'sha256':h,'matches_source':h==s['source_sha256'],'matches_manifest':h==m['evidence_hashes'][s['evidence_file']]['sha256']}
ok=all(v['exists'] and v['matches_source'] and v['matches_manifest'] for v in out.values());print(json.dumps({'status':'pass' if ok else 'fail','checks':out,'scope':m['scope']},ensure_ascii=False,indent=2));raise SystemExit(0 if ok else 1)
