#!/usr/bin/env python3
"""Freeze root72 result with unscaled-row identities and old-source hashes."""
from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent;ROOT=H.parent.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    a=json.loads((H/'literal_input_check.json').read_text());b=json.loads((H/'literal_certificate_check.json').read_text())
    assert a['status']==b['status']=='PASS'
    assert a['input_sha256']==b['input_sha256']==sha(H/'exact_input.json') and b['certificate_sha256']==sha(H/'exact_certificate.json')
    old=json.loads((H/'frozen_sources_before.json').read_text());changed=[p for p,h in old.items() if sha(ROOT/p)!=h];assert not changed
    assert json.loads((H/'discovery_output.json').read_text())['optimizer_calls']==1 and json.loads((H/'DISCOVERY_CALL_CONSUMED.json').read_text())['calls_reserved']==1
    files={p.name:sha(p) for p in sorted(H.iterdir()) if p.is_file() and p.name not in ('freeze_manifest.json','SHA256SUMS')}
    files['../maximal_root_tail_wallet_v2.md']=sha(H.parent/'maximal_root_tail_wallet_v2.md')
    out={'status':'PASS_AND_FROZEN','claim':'Universal root line and matching exact primal/unscaled-dual at the specified K in the root72 necessary cone; not sharp global root bound, full SPE or half.',
         'input_sha256':b['input_sha256'],'certificate_sha256':b['certificate_sha256'],'raw_rows':72,'columns':129,'optimizer_calls':1,
         'frozen_old_sources_checked':len(old),'changed_old_files':changed,'appended_cut_numerical_divisor':'126000',
         'integer_budget_scale_over_primitive_line':'2','write_scope':['maximal_root_tail_wallet_v2/','maximal_root_tail_wallet_v2.md'],
         'file_sha256':files,'stop_state':'No appended offdiagonal strengthening and no extra solve; further inputs require separate release.'}
    (H/'freeze_manifest.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
    (H/'SHA256SUMS').write_text(''.join(f'{h}  {p}\n' for p,h in sorted(files.items())))
    print(json.dumps({'status':out['status'],'input_sha256':out['input_sha256'],'certificate_sha256':out['certificate_sha256'],
                      'freeze_manifest_sha256':sha(H/'freeze_manifest.json'),'files_hashed':len(files),'old_sources_unchanged':len(old)},indent=2))
if __name__=='__main__':main()
