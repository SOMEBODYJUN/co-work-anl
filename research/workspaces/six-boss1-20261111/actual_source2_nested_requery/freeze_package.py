#!/usr/bin/env python3
"""Freeze the unbound751 P25+C30 symbolic package, without a solver or point."""
from hashlib import sha256
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def digest(path):return sha256(path.read_bytes()).hexdigest()

def main():
    checked=json.loads((HERE/'literal_symbolic_check.json').read_text())
    assert checked['status']=='PASS_SYMBOLIC751_UNBOUND_TRUE_INTERNAL_P25_AND_C30'
    assert checked['optimizer_calls']==0 and checked['point_bound'] is False
    for name,h in checked['file_sha256'].items():assert digest(HERE/name)==h,name
    frozen=json.loads((HERE/'frozen_sources_before.json').read_text())['file_sha256']
    changed=[p for p,h in frozen.items() if digest(ROOT/p)!=h]
    assert not changed,changed
    paths=sorted(p for p in HERE.iterdir() if p.is_file() and p.name not in {'freeze_manifest.json','SHA256SUMS'})
    hashes={p.name:digest(p) for p in paths}
    hashes['../actual_source2_nested_requery.md']=digest(HERE.parent/'actual_source2_nested_requery.md')
    out={
        'status':'SYMBOLIC751_P25_C30_UNBOUND_AND_FROZEN',
        'claim':'Inherited243 plus507 genuine internal P25 rows and one true-history C30; exact single-state interface only, no fixed point or SPE/half claim.',
        'genuine_rows':751,'inherited_rows':243,'nested_P25_rows':507,'nested_C30_rows':1,
        'physical_columns':'32*s','mass_equations':'s','raw_inequalities':'751+2*s',
        'future_projection_states':8192,'optimizer_calls':0,
        'point_bound':False,'matrix_constructed':False,'certificate_sha256':None,
        'read_only_source_files_checked':len(frozen),'changed_old_files':changed,
        'write_scope':['actual_source2_nested_requery/','actual_source2_nested_requery.md'],
        'file_sha256':hashes,
        'stop_state':'Await a separate future exact point and explicit phase-I release; excluded v4/v5 points remain unbound.'}
    (HERE/'freeze_manifest.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    (HERE/'SHA256SUMS').write_text('\n'.join([f'{h}  {p}' for p,h in hashes.items()]+[f'{digest(HERE/"freeze_manifest.json")}  freeze_manifest.json'])+'\n')
    print(json.dumps({'status':out['status'],'artifacts':len(hashes),
        'catalogue_sha256':digest(HERE/'row_catalogue.json'),
        'kernel_sha256':digest(HERE/'symbolic_coefficients.py'),
        'summary_sha256':digest(HERE.parent/'actual_source2_nested_requery.md'),
        'manifest_sha256':digest(HERE/'freeze_manifest.json'),
        'optimizer_calls':0,'point_bound':False,'changed_old_files':changed},indent=2))

if __name__=='__main__':main()
