from pathlib import Path
import hashlib, json
root=Path(__file__).resolve().parent
m=json.loads((root/'source-manifest.json').read_text())
checks=[]
for s in m['sources']:
    p=root/s['evidence']; b=p.read_bytes(); t=p.read_text(errors='replace')
    checks.append({'id':s['id'],'evidence_exists':p.exists(),'sha256_matches':hashlib.sha256(b).hexdigest()==s['sha256'],'size_matches':len(b)==s['size'],'lines':len(t.splitlines()),'expected_lines':s['lines'],'line_count_matches':len(t.splitlines())==s['lines'],'nonempty':bool(t.strip())})
result={'status':'PASS' if all(c['evidence_exists'] and c['sha256_matches'] and c['size_matches'] and c['line_count_matches'] and c['nonempty'] for c in checks) else 'FAIL','checks':checks}
(root/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n'); print(json.dumps(result,ensure_ascii=False,indent=2))
if result['status']!='PASS': raise SystemExit(1)
