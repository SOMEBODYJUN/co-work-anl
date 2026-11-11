#!/usr/bin/env python3
"""Freeze only the zero-optimizer v4 face package."""
from hashlib import sha256
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def digest(path):return sha256(path.read_bytes()).hexdigest()

def main():
    result=json.loads((HERE/'literal_check.json').read_text())
    assert result['status']=='PASS_ALL257_DUAL_RANK12_FULL225_FACE_AND_TWO_TRUE_TERMINAL_GAPS'
    assert result['optimizer_calls']==0
    for name,expected in result['file_sha256'].items():assert digest(HERE/name)==expected,name
    sources=json.loads((HERE/'source_hashes.json').read_text())['file_sha256']
    changed=[p for p,h in sources.items() if digest(ROOT/p)!=h]
    assert not changed,changed
    paths=sorted(p for p in HERE.iterdir() if p.is_file() and p.name not in {'freeze_manifest.json','SHA256SUMS'})
    hashes={p.name:digest(p) for p in paths}
    hashes['../v4_source2_identity.md']=digest(HERE.parent/'v4_source2_identity.md')
    out={
        'status':'PASS_AND_FROZEN_ZERO_OPTIMIZER',
        'claim':'Entire optimal face of the frozen225-row necessary cone is incompatible with a genuine complete-history pure SPE, by true source2 maximal-size rigidity and two strict terminal deviations.',
        'optimizer_calls':0,'raw_rows':225,'all_columns':257,
        'strict_positive_column_residuals':243,'zero_residual_columns':14,
        'equality_rank':12,'affine_dimension':2,
        'input_sha256':'b520abb0565c6df7ae4192971bf90d712ddf92a4304f3ce51710cd9b2617b8f5',
        'original_certificate_sha256':'290f90feba9bf7ec8232e16e59f02b7f4e05dc41413f14510592c3d16ef28819',
        'face_certificate_sha256':digest(HERE/'exact_face_certificate.json'),
        'read_only_sources_checked':len(sources),'changed_old_files':changed,
        'uses_320_family':False,'uses_243_phase_I':False,
        'write_scope':['v4_source2_identity/','v4_source2_identity.md'],
        'file_sha256':hashes,
        'stop_state':'Frozen old225 face exclusion only; no new global quantitative welfare bound or half claim. The separate243 symbolic package remains unbound.'}
    (HERE/'freeze_manifest.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    (HERE/'SHA256SUMS').write_text('\n'.join([f'{h}  {p}' for p,h in hashes.items()]+[f'{digest(HERE/"freeze_manifest.json")}  freeze_manifest.json'])+'\n')
    print(json.dumps({'status':out['status'],'optimizer_calls':0,
        'artifacts':len(hashes),'face_certificate_sha256':out['face_certificate_sha256'],
        'summary_sha256':digest(HERE.parent/'v4_source2_identity.md'),
        'manifest_sha256':digest(HERE/'freeze_manifest.json'),
        'read_only_sources_checked':len(sources),'changed_old_files':changed},indent=2))

if __name__=='__main__':main()
