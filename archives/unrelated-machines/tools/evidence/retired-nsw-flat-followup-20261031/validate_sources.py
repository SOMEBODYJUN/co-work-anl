from pathlib import Path
import hashlib, json, gzip
root=Path(__file__).resolve().parent
m=json.loads((root/'source-manifest.json').read_text())
checks=[]
for s in m['sources']:
    if 'evidence_binary' in s:
        b=(root/s['evidence_binary']).read_bytes(); import subprocess; t=subprocess.run(['gzip','-dc',str(root/s['evidence_binary'])],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL).stdout;
        checks.append({'id':s['id'],'binary_exists':bool(b),'sha256_matches':hashlib.sha256(b).hexdigest()==s['sha256'],'size_matches':len(b)==s['size'],'decompressed_sha256_matches':hashlib.sha256(t).hexdigest()==s['decompressed_sha256'],'text_nonempty':bool(t.strip())})
    else:
        p=root/s['evidence']; b=p.read_bytes(); checks.append({'id':s['id'],'evidence_exists':p.exists(),'sha256_matches':hashlib.sha256(b).hexdigest()==s['sha256'],'size_matches':len(b)==s['size'],'text_nonempty':bool(p.read_text(errors='replace').strip())})
result={'status':'PASS' if all(all(v for k,v in c.items() if k not in ('id',)) for c in checks) else 'FAIL','checks':checks}
(root/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n'); print(json.dumps(result,ensure_ascii=False,indent=2))
if result['status']!='PASS': raise SystemExit(1)
