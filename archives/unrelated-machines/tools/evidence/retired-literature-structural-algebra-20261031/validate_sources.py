from pathlib import Path
import hashlib, json
root=Path(__file__).resolve().parent
m=json.loads((root/'source-manifest.json').read_text())
repo=root.parents[4]
checks=[]
for s in m['sources']:
    src=repo/s['path']; ev=root/s['evidence_pdf']; txt=root/s['extracted_text']
    use=src if src.exists() else ev
    t=txt.read_text(errors='replace')
    checks.append({'id':s['id'],'source_exists':src.exists() or ev.exists(),'evidence_pdf_exists':ev.exists(),'sha256_matches':hashlib.sha256(use.read_bytes()).hexdigest()==s['sha256'],'text_exists':txt.exists(),'text_lines':len(t.splitlines()),'text_nonempty':bool(t.strip())})
if not all(c['source_exists'] and c['evidence_pdf_exists'] and c['sha256_matches'] and c['text_exists'] and c['text_nonempty'] for c in checks): raise SystemExit('validation failed')
(root/'validation.json').write_text(json.dumps({'status':'PASS','checks':checks},indent=2)+'\n')
print(json.dumps({'status':'PASS','checks':checks},indent=2))
