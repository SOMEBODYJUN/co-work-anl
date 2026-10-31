from pathlib import Path
import hashlib, json
root = Path(__file__).resolve().parent
manifest = json.loads((root/'source-manifest.json').read_text())
repo = root.parents[4]
checks=[]
for s in manifest['sources']:
    src = repo / s['path']
    evidence_src = root / s['evidence_pdf']
    src_for_hash = src if src.exists() else evidence_src
    got = hashlib.sha256(src_for_hash.read_bytes()).hexdigest()
    txt = root / s['extracted_text']
    text = txt.read_text(errors='replace')
    checks.append({
        'id': s['id'],
        'source_exists': src.exists() or evidence_src.exists(),
        'evidence_pdf_exists': evidence_src.exists(),
        'sha256_matches': got == s['sha256'],
        'extracted_text_exists': txt.exists(),
        'extracted_text_lines': len(text.splitlines()),
        'extracted_text_nonempty': bool(text.strip()),
    })
if not all(x['source_exists'] and x['evidence_pdf_exists'] and x['sha256_matches'] and x['extracted_text_exists'] and x['extracted_text_nonempty'] for x in checks):
    raise SystemExit('source/evidence validation failed')
(root/'validation.json').write_text(json.dumps({'status':'PASS','checks':checks}, indent=2)+'\n')
print(json.dumps({'status':'PASS','checks':checks}, indent=2))
