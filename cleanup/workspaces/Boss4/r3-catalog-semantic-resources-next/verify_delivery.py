from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parents[4]
manifest=B/'copy-files.json'
if not manifest.exists():raise SystemExit('External transport copy-files.json required; this verifier does not retrieve Git objects')
rows=json.loads(manifest.read_text())
for r in rows:
 p=B/r['path'];assert p.stat().st_size==r['bytes'];assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
print(len(rows),'exact transport files verified')
