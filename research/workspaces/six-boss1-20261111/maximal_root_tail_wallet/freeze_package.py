#!/usr/bin/env python3
"""Freeze only this new mathematical obligation, preserving old packages."""
from pathlib import Path
import json,hashlib

H=Path(__file__).resolve().parent;ROOT=H.parent.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    a=json.loads((H/'literal_input_check.json').read_text());b=json.loads((H/'literal_certificate_check.json').read_text())
    assert a['status']==b['status']=='PASS'
    assert a['input_sha256']==b['input_sha256']==sha(H/'exact_input.json')
    assert b['certificate_sha256']==sha(H/'exact_certificate.json')
    before=json.loads((H/'frozen_sources_before.json').read_text())
    changed=[p for p,h in before.items() if sha(ROOT/p)!=h];assert not changed,changed
    assert json.loads((H/'discovery_output.json').read_text())['optimizer_calls']==1
    assert json.loads((H/'DISCOVERY_CALL_CONSUMED.json').read_text())['calls_reserved']==1
    hashes={p.name:sha(p) for p in sorted(H.iterdir()) if p.is_file() and p.name not in {'SHA256SUMS','freeze_manifest.json'}}
    hashes['../maximal_root_tail_wallet.md']=sha(H.parent/'maximal_root_tail_wallet.md')
    out={'status':'PASS_AND_FROZEN','claim':'Universal root line and exact primal-dual match at the specified K0 for this necessary 128-type cone; not a full-SPE or globally optimal root-bound claim.',
         'input_sha256':b['input_sha256'],'certificate_sha256':b['certificate_sha256'],'optimizer_calls':1,
         'frozen_old_sources_checked':len(before),'changed_old_files':changed,
         'write_scope':['maximal_root_tail_wallet/','maximal_root_tail_wallet.md'],
         'file_sha256':hashes,'stopping_state':'One authorized LP consumed; no additional solve or old-input modification.'}
    (H/'freeze_manifest.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
    (H/'SHA256SUMS').write_text(''.join(f'{h}  {p}\n' for p,h in sorted(hashes.items())))
    print(json.dumps({'status':out['status'],'input_sha256':out['input_sha256'],'certificate_sha256':out['certificate_sha256'],
                      'freeze_manifest_sha256':sha(H/'freeze_manifest.json'),'files_hashed':len(hashes),'frozen_old_sources_unchanged':len(before)},indent=2))
if __name__=='__main__':main()
