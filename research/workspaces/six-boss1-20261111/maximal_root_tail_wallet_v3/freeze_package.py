#!/usr/bin/env python3
"""Freeze this new package only after complete exact/literal proof checks."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
import json
H=Path(__file__).resolve().parent;ROOT=H.parent.parents[2]
def digest(p):return sha256(p.read_bytes()).hexdigest()
def main():
    if (H/'freeze_manifest.json').exists():raise SystemExit('Package is already frozen.')
    a=json.loads((H/'literal_input_check.json').read_text());b=json.loads((H/'literal_certificate_check.json').read_text())
    p=json.loads((H/'proof_transcription_check.json').read_text());c=json.loads((H/'exact_certificate.json').read_text())
    assert a['status']==b['status']=='PASS' and p['status']=='PASS_EXACT_PROOF_TABLES_AND_PARAMETER_BUDGET'
    assert all(t['input_sha256']==digest(H/'exact_input.json') for t in [a,b,p,c])
    assert b['certificate_sha256']==p['certificate_sha256']==digest(H/'exact_certificate.json')
    assert p['proof_sha256']==digest(H/'proof.md')
    marker=json.loads((H/'DISCOVERY_CALL_CONSUMED.json').read_text());discovery=json.loads((H/'discovery_output.json').read_text())
    assert marker['calls_reserved']==discovery['optimizer_calls']==c['optimizer_calls']==1
    assert marker['input_sha256']==digest(H/'exact_input.json')
    assert marker['preflight_sha256']==digest(H/'literal_input_check.json')
    frozen=json.loads((H/'frozen_sources_before.json').read_text());assert all(digest(ROOT/r)==d for r,d in frozen.items())
    adjacent=H.with_suffix('.md');files=sorted(p for p in H.rglob('*') if p.is_file() and p.name not in ['freeze_manifest.json','SHA256SUMS'])+[adjacent]
    entries=[{'path':str(p.relative_to(H.parent)),'sha256':digest(p),'bytes':p.stat().st_size} for p in files]
    manifest={'status':'FROZEN_EXACT_ROOT270_WITH_LITERAL_CHECK','input_sha256':digest(H/'exact_input.json'),
              'certificate_sha256':digest(H/'exact_certificate.json'),'raw_rows':270,'columns':129,'equalities':2,
              'homogeneous_columns':131,'optimizer_calls':1,'exact_arithmetic_only_after_discovery':True,
              'old_sources_unchanged':len(frozen),'universal_root_line':c['universal_root_line'],
              'exact_fixed_K_optimum':c['objective'],'root_gap_over_v6_u':c['comparison_at_released_K']['root_gap_over_v6_u'],
              'files':entries,'not_claimed':['complete SPE realization','global root sharpness','half coverage','new full256 optimum'],
              'further_optimizer_calls_authorized':False}
    (H/'freeze_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
    sums=[e['sha256']+'  '+e['path'] for e in entries]+[digest(H/'freeze_manifest.json')+'  '+str((H/'freeze_manifest.json').relative_to(H.parent))]
    (H/'SHA256SUMS').write_text('\n'.join(sums)+'\n')
    print(json.dumps({'status':manifest['status'],'files':len(entries),'freeze_manifest_sha256':digest(H/'freeze_manifest.json'),
                      'input_sha256':manifest['input_sha256'],'certificate_sha256':manifest['certificate_sha256']},indent=2))
if __name__=='__main__':main()
