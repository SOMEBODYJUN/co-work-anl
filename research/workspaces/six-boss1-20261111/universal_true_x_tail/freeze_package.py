#!/usr/bin/env python3
"""Hash the completed new package after the independent exact checks."""
from pathlib import Path
import json,hashlib

H=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    checks=json.loads((H/'literal_certificate_check.json').read_text())
    inp=json.loads((H/'literal_input_check.json').read_text())
    assert checks['status']==inp['status']=='PASS'
    assert checks['certificate_sha256']==sha(H/'exact_certificate.json')
    assert checks['input_sha256']==inp['input_sha256']==sha(H/'exact_input.json.gz')
    before=json.loads((H/'frozen_sources_before.json').read_text())
    changed=[p for p,h in before.items() if sha(H.parent/p)!=h]
    assert not changed,changed
    assert json.loads((H/'discovery_output.json').read_text())['optimizer_calls']==1
    assert json.loads((H/'DISCOVERY_CALL_CONSUMED.json').read_text())['calls_reserved']==1
    files={p.name:sha(p) for p in sorted(H.iterdir()) if p.is_file() and p.name not in {'freeze_manifest.json','SHA256SUMS'}}
    files['../universal_true_x_tail.md']=sha(H.parent/'universal_true_x_tail.md')
    out={'status':'PASS_AND_FROZEN','claim':'Exact fixed-point true-X-tail infeasibility and ALL-256-type universal projection cut; no half or complete-SPE claim.',
         'input_sha256':checks['input_sha256'],'certificate_sha256':checks['certificate_sha256'],
         'optimizer_calls':1,'frozen_old_files_checked':len(before),'changed_old_files':changed,
         'write_scope':['universal_true_x_tail/','universal_true_x_tail.md'],
         'stopping_state':'No further discovery authorized or performed; one-call guard remains active.','file_sha256':files}
    (H/'freeze_manifest.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
    (H/'SHA256SUMS').write_text(''.join(f'{h}  {p}\n' for p,h in sorted(files.items())))
    print(json.dumps({'status':out['status'],'new_package_files_hashed':len(files),'frozen_old_files_unchanged':len(before),
                      'freeze_manifest_sha256':sha(H/'freeze_manifest.json'),'input_sha256':checks['input_sha256'],
                      'certificate_sha256':checks['certificate_sha256']},indent=2))
if __name__=='__main__':main()
