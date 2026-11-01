"""Exact-copy transport whitelist after completed semantic checks."""
from pathlib import Path
import hashlib,json
S=Path(__file__).resolve().parents[4];W=Path(__file__).resolve().parent
assert json.loads((W/'validation.json').read_text())['status']=='pass'
rows=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and p!=S/'copy-files.json':
  b=p.read_bytes();rows.append({'path':str(p.relative_to(S)),'size':len(b),'sha256':hashlib.sha256(b).hexdigest()})
assert not any('__pycache__' in r['path'] for r in rows)
out={'stage_root':str(S),'manifest_is_transport_only':True,'file_count':len(rows),'bytes':sum(r['size'] for r in rows),'files':rows}
p=S/'copy-files.json';p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'file_count':len(rows),'bytes':out['bytes'],'manifest_bytes':p.stat().st_size,'manifest_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}))
