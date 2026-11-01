"""Static saved-artifact check; no historical CLI or mathematical scan."""
import ast
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
import re

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[4]
BODY=REPO/'archives/customer-attraction/state/程序/对角回复基本预算的拆分诊断程序--程序.md'
RECEIPT=REPO/'cleanup/workspaces/Boss7/receipts-round11/ae3a69e8e041bfd1b8f5.json'

def checked_file(path):
    data=path.read_bytes()
    return {'path':str(path.relative_to(REPO)),'bytes':len(data),'sha256':sha256(data).hexdigest()}

def main():
    assert __debug__
    manifest=json.loads((HERE/'source-manifest.json').read_bytes())
    sources=[manifest[k] for k in ('primary','direct_threshold_input','threshold_generation_source')]+manifest['shared_old_input_and_relevant_dependencies']
    for rec in sources:
        data=(REPO/rec['stored_path']).read_bytes()
        assert len(data)==rec['size'] and sha256(data).hexdigest()==rec['sha256']
    for rec in manifest['formal_objects_compared']:
        data=(REPO/rec['path']).read_bytes()
        assert len(data)==rec['bytes'] and sha256(data).hexdigest()==rec['sha256']
    for rec in manifest['other_evidence_compared']:assert (REPO/rec).is_file()
    for path in HERE.rglob('*.py'):ast.parse(path.read_bytes())
    json_count=0
    for path in HERE.rglob('*.json'):
        if path.name=='selfcheck.json':continue
        json.loads(path.read_bytes());json_count+=1
    receipt=json.loads(RECEIPT.read_bytes())
    assert receipt['id']==manifest['primary']['id']=='ae3a69e8e041bfd1b8f5'
    assert all(receipt[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
    for target in receipt['targets']:
        if target.endswith('/selfcheck.json'):continue
        assert (REPO/target).is_file(),target
    links=[]
    for path in (BODY,HERE/'README.md'):
        raw=path.read_text()
        for target in re.findall(r'\]\(([^)]+)\)',raw):
            if '://' in target or target.startswith('#'):continue
            dest=(path.parent/target.split('#')[0]).resolve()
            assert dest.is_file(),(path,target)
            links.append(str(dest.relative_to(REPO)))
    event=json.loads((HERE/'rerun/execution-event.json').read_bytes())
    out=json.loads((HERE/'rerun/stdout.json').read_bytes())
    assert event['exit_code']==0 and event['stderr_bytes']==0 and (HERE/'rerun/stderr.txt').stat().st_size==0
    assert event['stdout_bytes']==(HERE/'rerun/stdout.json').stat().st_size==938
    assert event['source_files_before']==event['source_files_after'] and len(event['source_files_before'])==50
    assert event['source_files_unchanged'] and event['generated_status_matches_stdout']
    local=json.loads((HERE/'input-and-local-check.json').read_bytes())
    slacks={(r['stage'],r['diagonal'],r['name']):F(r['value']) for r in local['split_slacks']}
    assert len(slacks)==56 and len(out['negative_rows'])==5
    assert [{'row':str(k),'slack':str(v)} for k,v in slacks.items() if v<0]==out['negative_rows']
    assert str(min(slacks.values()))==out['minimum_slack']==local['minimum_split_slack']
    for k,v in slacks.items():
        if v<0:assert slacks[k[0],1-k[1],k[2]]==-v
    assert len(local['merged_basic_slacks'])==28
    for r in local['merged_basic_slacks']:
        assert F(r['value'])==slacks[r['stage'],0,r['name']]+slacks[r['stage'],1,r['name']]>=0
    ledger=json.loads((HERE/'hybrid-moment-ledger.json').read_bytes())
    assert len(ledger)==194
    for r in ledger:
        h,rm,zm,v=(F(r[k]) for k in ('h','r','z','rz'))
        states={str((0,0)):h-rm-zm+v,str((0,1)):zm-v,str((1,0)):rm-v,str((1,1)):v}
        assert {k:F(v) for k,v in r['state_masses'].items()}==states and min(states.values())>=0
    assert sum(F(r['z'])!=F(r['old_z']) for r in ledger)==56
    assert sum(F(r['rz'])!=F(r['old_rz']) for r in ledger)==29
    assert local['variables']==321 and local['slabs']==25 and local['positive_histograms']==10
    inventory=[checked_file(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='selfcheck.json']
    result={'status':'PASS','scope':'static source/receipt/link/output/ledger consistency only; no new original run, graph build, optimization or repeated mathematical scan','primary_source_id':receipt['id'],'frozen_sources_checked':len(sources),'formal_comparison_fingerprints_checked':len(manifest['formal_objects_compared']),'json_files_parsed_excluding_selfcheck':json_count,'links_checked':len(links),'receipt':checked_file(RECEIPT),'body':checked_file(BODY),'evidence_file_inventory':inventory,'saved_original_events':1,'saved_current_point_math_checks':1,'new_original_or_math_runs_by_this_selfcheck':0,'confirmed_negative_rows':5,'confirmed_merged_rows':28,'confirmed_hybrid_groups':194}
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
