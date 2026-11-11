#!/usr/bin/env python3
"""Freeze this obligation after exact all-type checks; never modify sources."""
from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent;ROOT=H.parent.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    i=json.loads((H/'literal_input_check.json').read_text());c=json.loads((H/'literal_certificate_check.json').read_text())
    assert i['status']==c['status']=='PASS'
    assert i['input_sha256']==c['input_sha256']==sha(H/'exact_input.json')
    assert c['certificate_sha256']==sha(H/'exact_certificate.json')
    old=json.loads((H/'frozen_sources_before.json').read_text());changed=[p for p,h in old.items() if sha(ROOT/p)!=h];assert not changed
    assert json.loads((H/'discovery_output.json').read_text())['optimizer_calls']==1
    assert json.loads((H/'DISCOVERY_CALL_CONSUMED.json').read_text())['calls_reserved']==1
    files={p.name:sha(p) for p in sorted(H.iterdir()) if p.is_file() and p.name not in ('freeze_manifest.json','SHA256SUMS')}
    files['../maximal_root_opt_requery.md']=sha(H.parent/'maximal_root_opt_requery.md')
    out={'status':'PASS_AND_FROZEN','claim':'Fixed-point exact noncompletion plus ALL128-type moment-envelope necessary cut; no partition, SPE, sharp-root-line or half claim.',
         'input_sha256':c['input_sha256'],'certificate_sha256':c['certificate_sha256'],'optimizer_calls':1,
         'frozen_old_sources_checked':len(old),'changed_old_files':changed,
         'write_scope':['maximal_root_opt_requery/','maximal_root_opt_requery.md'],'file_sha256':files,
         'stop_state':'One authorized phase-I consumed; further solver work awaits a separate Main release.'}
    (H/'freeze_manifest.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
    (H/'SHA256SUMS').write_text(''.join(f'{h}  {p}\n' for p,h in sorted(files.items())))
    print(json.dumps({'status':out['status'],'input_sha256':out['input_sha256'],'certificate_sha256':out['certificate_sha256'],
                      'freeze_manifest_sha256':sha(H/'freeze_manifest.json'),'files_hashed':len(files),'frozen_old_files_unchanged':len(old)},indent=2))
if __name__=='__main__':main()
