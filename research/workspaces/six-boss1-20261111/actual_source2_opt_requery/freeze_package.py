#!/usr/bin/env python3
"""Freeze this symbolic package only; no point binding or solver."""
from hashlib import sha256
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def digest(path):return sha256(path.read_bytes()).hexdigest()

def main():
    checked=json.loads((HERE/'literal_symbolic_check.json').read_text())
    assert checked['status']=='PASS_SYMBOLIC_UNBOUND'
    for name,expected in checked['file_sha256'].items():
        assert digest(HERE/name)==expected,(name,'run literal check after final source edits')
    before=json.loads((HERE/'frozen_sources_before.json').read_text())['file_sha256']
    changed=[p for p,h in before.items() if digest(ROOT/p)!=h]
    assert not changed,changed
    skip={'freeze_manifest.json','SHA256SUMS'}
    paths=sorted(p for p in HERE.iterdir() if p.is_file() and p.name not in skip)
    hashes={p.name:digest(p) for p in paths}
    hashes['../actual_source2_opt_requery.md']=digest(HERE.parent/'actual_source2_opt_requery.md')
    out={
        'status':'SYMBOLIC_UNBOUND_AND_FROZEN',
        'claim':'243 sourced necessary rows and exact single-state interface; no fixed point, LP result, universal numeric cut, complete SPE or half claim.',
        'genuine_rows':243,'physical_columns':'32*s','mass_equations':'s',
        'raw_inequalities':'243+2*s','future_full_projection_states':8192,
        'optimizer_calls':0,'point_bound':False,'matrix_constructed':False,
        'fixed_input_sha256':None,'certificate_sha256':None,
        'read_only_source_files_checked':len(before),'changed_old_files':changed,
        'write_scope':['actual_source2_opt_requery/','actual_source2_opt_requery.md'],
        'file_sha256':hashes,
        'stop_state':'Await a separate explicit Main exact-point and optimizer release; this symbolic package is not a phase-I authorization.'}
    (HERE/'freeze_manifest.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    lines=[f'{h}  {n}' for n,h in hashes.items()]
    lines.append(f'{digest(HERE/"freeze_manifest.json")}  freeze_manifest.json')
    (HERE/'SHA256SUMS').write_text('\n'.join(lines)+'\n')
    print(json.dumps({'status':out['status'],'artifacts':len(hashes),
        'row_catalogue_sha256':digest(HERE/'row_catalogue.json'),
        'kernel_sha256':digest(HERE/'symbolic_coefficients.py'),
        'summary_sha256':digest(HERE.parent/'actual_source2_opt_requery.md'),
        'manifest_sha256':digest(HERE/'freeze_manifest.json'),
        'optimizer_calls':0,'changed_old_files':changed},indent=2))

if __name__=='__main__':main()
