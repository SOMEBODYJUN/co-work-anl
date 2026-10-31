#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent;m=json.loads((root/'manifest.json').read_text());s=m['sources'][0];p=root/s['evidence_file'];h=hashlib.sha256(p.read_bytes()).hexdigest();o={'status':'pass' if p.exists() and h==s['source_sha256'] else 'fail','sha256':h,'size':p.stat().st_size if p.exists() else None};print(json.dumps(o,ensure_ascii=False,indent=2));(root/'validation.json').write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n');raise SystemExit(0 if o['status']=='pass' else 1)
