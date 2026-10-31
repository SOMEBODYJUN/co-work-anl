from pathlib import Path
import hashlib, json
root = Path(__file__).resolve().parent
manifest = json.loads((root / 'source-manifest.json').read_text())
repo = root.parents[4]
checks = []
for s in manifest['sources']:
    src = repo / s['path']
    ev = root / s['evidence_pdf']
    txt = root / s['extracted_text']
    use = src if src.exists() else ev
    text = txt.read_text(errors='replace')
    checks.append({
        'id': s['id'],
        'source_exists': src.exists() or ev.exists(),
        'evidence_pdf_exists': ev.exists(),
        'sha256_matches': hashlib.sha256(use.read_bytes()).hexdigest() == s['sha256'],
        'text_exists': txt.exists(),
        'text_lines': len(text.splitlines()),
        'text_nonempty': bool(text.strip()),
        'expected_text_lines': s['text_lines'],
        'text_line_count_matches': len(text.splitlines()) == s['text_lines'],
    })
required = all(c['source_exists'] and c['evidence_pdf_exists'] and c['sha256_matches'] and c['text_exists'] and c['text_nonempty'] and c['text_line_count_matches'] for c in checks)
result = {'status': 'PASS' if required else 'FAIL', 'checks': checks}
(root / 'validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
if not required:
    raise SystemExit(1)
