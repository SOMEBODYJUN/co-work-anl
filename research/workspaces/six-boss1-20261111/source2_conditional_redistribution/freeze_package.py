#!/usr/bin/env python3
"""Freeze this new package and its explicitly authorized sibling report.

Never overwrites a freeze.  Reads only this package and the four pinned
source proofs; performs no Git, optimization, network, or external writes.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
MANIFEST=HERE/'freeze_manifest.json'
SUMS=HERE/'SHA256SUMS'
assert not MANIFEST.exists() and not SUMS.exists(), 'Package is already frozen.'

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def load(name):
    return json.loads((HERE/name).read_text())

pins=load('source_pins.json')
for source in pins['sources']:
    assert digest(ROOT/source['path'])==source['sha256']
check=load('literal_checker_output.json')
assert check['status']=='PASS' and not check['mathematical_failures']
summary=load('derivation_summary.json')
assert summary['raw_endpoint_rows']==180 and summary['affine_segment_rows']==150
assert len(load('literal_row_checks.json')['all_rows_checked'])==333
assert not load('failure_log.json')['mathematical_failures']

payload=[]
for path in sorted(HERE.iterdir(),key=lambda p:p.name):
    assert path.is_file() and not path.is_symlink()
    if path.name not in ['freeze_manifest.json','SHA256SUMS']:
        payload.append({'path':path.name,'bytes':path.stat().st_size,'sha256':digest(path)})
report=HERE.parent/(HERE.name+'.md')
payload.append({'path':'../'+report.name,'bytes':report.stat().st_size,'sha256':digest(report)})
manifest={
    'status':'FROZEN_PASS',
    'agent_id':'/root/source2_conditional_redistribution',
    'run':'six-boss1-20261111',
    'frozen_at_utc':datetime.now(timezone.utc).isoformat(),
    'scope':'source 2; delta in [0,5977/6912]; tau3=0; tau4=5977/6912-delta; tau5=43/48+delta; s=0,61273/6912,9; pure q0=1/6 and ordered q0=1/5',
    'write_scope':[str(HERE.relative_to(ROOT))+'/',str(report.relative_to(ROOT))],
    'row_schema':'rows list; row.a is 513 exact rational strings; 512 lexicographic (a1,...,a6,x,o,c) columns, then independent K; raw >=0; positive numerical divisor 25',
    'complete_endpoint_rows':180,
    'additional_epsilon_rows':3,
    'complete_affine_rows':150,
    'raw_affine_hidden_states':1536,
    'all_weak_states_and_provenance_preserved':True,
    'epsilon_claims':'both PASS, all 1026 columns exactly zero residual',
    'independent_check_counts':check['counts'],
    'independent_point_row_metadata_checks':183,
    'source_pins_unchanged':pins['sources'],
    'optimizer_calls':0,
    'global_candidate_reads':0,
    'git_registry_map_RUN_auth_operations':0,
    'mathematical_failures':[],
    'execution_record':'one deliberate initial performance interruption; clean regenerated and independently verified package',
    'files':payload,
    'checksum_convention':'This manifest hashes all payload files. SHA256SUMS additionally hashes this manifest and the sibling report; SHA256SUMS is not self-hashed.',
    'freeze_commitment':'No writes after successful freeze verification.'
}
MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
allrecords=payload+[{'path':MANIFEST.name,'sha256':digest(MANIFEST)}]
SUMS.write_text(''.join(x['sha256']+'  '+x['path']+'\n' for x in allrecords))
for item in allrecords:
    assert digest(HERE/item['path'])==item['sha256']
print(json.dumps({'status':'FROZEN_PASS','agent_id':manifest['agent_id'],
                  'manifest_sha256':digest(MANIFEST),'SHA256SUMS_sha256':digest(SUMS),
                  'proof_sha256':digest(HERE/'proof.md'),
                  'payload_file_count':len(payload),
                  'payload_bytes':sum(x['bytes'] for x in payload)},ensure_ascii=False))
