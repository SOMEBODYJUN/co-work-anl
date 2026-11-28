"""Capture only the already measured, pre-repair counterexamples from the frozen inline product."""
import argparse, gzip, json, re, sys
from pathlib import Path
sys.dont_write_bytecode = True
import independent_numeric as a
p = argparse.ArgumentParser()
p.add_argument('--html', type=Path)
args = p.parse_args()
old_hash = '7a588bb8046b62f33c557ea04a2d0eb3a8e2db9cd22994fec39bae1b4346daf1'
arch = a.HERE / 'previous_engine.js.gz'
temp = a.HERE / 'audit_previous_engine.cjs'
if args.html:
    src = next((t for attrs, t in re.findall('<script\\b([^>]*)>([\\s\\S]*?)</script>', args.html.read_text(),
        flags=re.I) if 'root.HouseholdEngine = factory()' in t)).encode()
    if a.sha(src) != old_hash:
        raise ValueError('Supplied HTML is not the frozen pre-repair version')
    arch.write_bytes(gzip.compress(src, mtime=0))
else:
    src = gzip.decompress(arch.read_bytes())
if a.sha(src) != old_hash:
    raise ValueError('Archived source hash differs')
names = [r['id'] for r in a.requests if r['id'].startswith(('margin_', 'unknown_', 'salary_funded'))]
items = [r for r in a.requests if r['id'] in names]
temp.write_bytes(src)
try:
    out = a.run_engine(items, temp)
finally:
    temp.unlink(missing_ok=True)
summary = {}
for k, v in out.items():
    if 'all' in v:
        summary[k] = {'candidateCount': len(v['all']),
            'feasibleActions': [r['actions'] for r in v['all'] if r['feasible']]}
    elif 'rows' in v:
        summary[k] = {'firstFailure': v['summary']['firstFailure'], 'terminalReal': v['summary']['terminalReal'],
            'firstMonth': {f: v['rows'][0][f] for f in ['cash', 'debt', 'financial', 'unpaid', 'prepaid']},
            'blocked': v['summary']['blocked']}
    else:
        summary[k] = v
rec = {'audit': 'Before repairs: observed counterexamples, not a release verdict', 'oldEngineSHA256': old_hash,
    'oldPackagedHTMLSHA256': '8b9b6da9297ed7c878642639428e04b56a1252abe71efd7615ea457070396e3a',
    'testInputSHA256': a.sha(a.canonical(items)), 'nodeResultsSHA256': a.sha(a.canonical(out)),
    'commands': 'Use the project numpy-financial Python to run preserve_old_failures.py. It uses the hash-checked archived source with the same independent data generator.', 'results': summary}
(a.HERE / 'pre_repair_findings.json').write_text(a.dump(rec))
print(a.dump({k: v for k, v in rec.items() if k != 'results'}))
