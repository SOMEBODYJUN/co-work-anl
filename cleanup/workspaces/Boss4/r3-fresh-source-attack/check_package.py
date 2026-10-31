"""Verify frozen scope, bytes, links, receipts and already recorded runs only."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

REPO=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
STAGE=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-fresh-source-attack')
EV=Path('archives/customer-attraction/tools/evidence/optimal-fresh-source-attack-primary')
WS=Path('cleanup/workspaces/Boss4/r3-fresh-source-attack')
PRIMARY=['e34ee6479d87bca78052','c320561014ad69bbebf0','2abfdaad5623537eeb3a','7cfd730044a42f607965','4ff936ca40b885e9237f']
COMPARISON=['9da7c5510bd045b3d059','94f62b8bf6ed8c17630c','f628126751d47bbb0ff3','6b81f6445e9914b0b550','8b9cf44d16a024398ef3']
CURRENT_FULL=[
 'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md',
 'archives/customer-attraction/state/想法/最优覆盖查询的自留份额预算--想法.md',
 'archives/customer-attraction/state/引理/笛卡尔目录的最优查询缺陷与三倍根修复--引理.md',
 'archives/customer-attraction/state/引理/最优元组跨角色零净损失替换门--引理.md',
 'archives/customer-attraction/state/引理/最优组合影价松弛与正损失替换停界--引理.md',
]
CURRENT_SCOPE=[
 'archives/customer-attraction/state/定理/五人半覆盖--定理.md',
 'archives/customer-attraction/subarchives/six-providers/问题--问题.md',
]
PREFIXES=['evidence/certificates/customer_attraction/','examples/customer_attraction/']
POLICIES=['worst_cce_welfare_failure','aggregate_theta_failure','individual_security_failure','prefix_balance_failure']

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def dump(path,obj):
    (STAGE/path).parent.mkdir(parents=True,exist_ok=True)
    (STAGE/path).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

def main():
    dump(EV/'verification.json',dict(all_checks_passed=False,status='validation-in-progress'))
    inventory={r['id']:r for r in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
    runtime=json.loads((STAGE/EV/'runtime-input-manifest.json').read_text())
    supplement=json.loads((STAGE/EV/'supplement/input-scan-and-multiset-check.json').read_text())
    scan={r['name']:r for r in supplement['scan']}
    records=[]
    for old in runtime['frozen_sources']:
        row=inventory[old['id']]
        raw=(STAGE/old['saved_path']).read_bytes()
        assert len(raw)==row['size'] and sha(raw)==row['sha256']
        role='primary' if row['id'] in PRIMARY else 'frozen-directory-dependency-not-done'
        use=[]
        if role!='primary':
            name=Path(row['path']).name
            if name in scan and scan[name]['source_reads_json']:
                use.append('exact-main-JSON-read')
            else:
                use.append('preserved-directory-entry-not-opened-by-exact-main')
            if Path(name).stem in POLICIES:
                use.append('float-main-policy-actions-or-m-and-p-read')
            use.append('supplement-full-JSON-parse')
        records.append(dict(old,role=role,read_scope='full-text' if role=='primary' else 'fully-JSON-parsed; source field-use separately recorded',use=use))
    for sid in COMPARISON:
        row=inventory[sid]
        first=None
        locations=[]
        for loc in row['sources']:
            raw=subprocess.check_output(['git','show',loc['commit']+':'+loc['path']],cwd=REPO,timeout=30)
            assert len(raw)==row['size'] and sha(raw)==row['sha256']
            assert first is None or first==raw
            first=raw
            locations.append(dict(loc,bytes_verified=True))
        target=EV/'original'/row['path']
        (STAGE/target).parent.mkdir(parents=True,exist_ok=True)
        (STAGE/target).write_bytes(first)
        records.append(dict(id=sid,path=row['path'],blob=row['blob'],size=row['size'],sha256=row['sha256'],sources=locations,role='comparison-only-not-done',read_scope='full-text',saved_path=str(target)))
    commits=sorted({loc['commit'] for row in runtime['frozen_sources'] for loc in row['sources']})
    listings=[]
    expected={r['path'] for r in runtime['frozen_sources'] if r['id'] not in PRIMARY}
    for commit in commits:
        paths=subprocess.check_output(['git','ls-tree','-r','--name-only',commit,'--']+PREFIXES,cwd=REPO,timeout=30).decode().splitlines()
        direct=sorted(p for p in paths if any(p.startswith(pre) and p.endswith('.json') and '/' not in p[len(pre):] for pre in PREFIXES))
        assert set(direct)==expected
        listings.append(dict(commit=commit,nonrecursive_json_paths=direct,equals_preserved_directory_set=True))
    dump(EV/'frozen-directory-listing.json',dict(prefixes=PREFIXES,listings=listings,top_level_certificate_count=29,top_level_example_count=22,nested_JSON_files_excluded_by_original_glob=True))
    current=[]
    for path in CURRENT_FULL+CURRENT_SCOPE:
        raw=(REPO/path).read_bytes()
        current.append(dict(path=path,size=len(raw),sha256=sha(raw),read_scope='full-text' if path in CURRENT_FULL else 'model-scope-and-current-status-passages-only'))
    dump(EV/'source-manifest.json',dict(primary_count=5,primary_bytes=sum(r['size'] for r in records if r['role']=='primary'),directory_dependency_count=51,directory_dependency_bytes=sum(r['size'] for r in records if r['role']=='frozen-directory-dependency-not-done'),comparison_count=5,comparison_bytes=sum(r['size'] for r in records if r['role']=='comparison-only-not-done'),sources=records,current_objects=current,claim_push='6015570f6c0db3c8c3e52fbbabb8ee88976fb1ab',source_program_executions='two distinct original mains, once each; one separately labelled new static multiset supplement'))
    execution=json.loads((STAGE/EV/'replay/execution.json').read_text())
    assert len(execution['runs'])==2
    for run in execution['runs']:
        assert run['executions_of_original_entrypoint']==1 and run['exit_code']==0
        assert run['generated_report_byte_identical_to_frozen'] and run['input_and_code_bytes_unchanged']
    reports=['audit_optimal_fresh_self_reserve.json','attack_optimal_fresh_policy_cones.json']
    for name in reports:
        raw=(STAGE/EV/'replay'/name).read_bytes()
        originals=[r for r in records if r['role']=='primary' and Path(r['path']).name==name]
        assert len(originals)==1 and raw==(STAGE/originals[0]['saved_path']).read_bytes()
    exact=json.loads((STAGE/EV/'replay'/reports[0]).read_text())
    floating=json.loads((STAGE/EV/'replay'/reports[1]).read_text())
    assert len(exact['rows'])==16 and exact['counterexamples_found']==0
    assert len(floating['rows'])==4 and sum(r['targets'] for r in floating['rows'])==65
    assert sum(r['feasible_targets'] for r in floating['rows'])==57
    assert supplement['executions']==1 and supplement['total_multisets']==2767 and supplement['all_checks_passed']
    formal=sorted((STAGE/'archives/customer-attraction/state').rglob('*.md'))
    links=[]
    for path in formal+[STAGE/EV/'README.md']:
        content=path.read_text()
        if path in formal:
            assert content.startswith('---\n')
            front=content.split('---',2)[1]
            for key in ['id','kind','type_tag','title','status','summary','source_refs']:
                assert re.search('^'+key+':',front,re.M),(path,key)
        for target in re.findall(r'\]\(([^)]+)\)',content):
            if '://' in target or target.startswith('#'): continue
            target=target.split('#')[0]
            resolved=(path.parent/target).resolve()
            rel=resolved.relative_to(STAGE)
            exists=resolved.exists() or (REPO/rel).exists()
            assert exists,(path,target)
            links.append(dict(file=str(path.relative_to(STAGE)),target=target,resolves=True))
        assert content.count('\\[')==content.count('\\]'),path
    receipts=json.loads((STAGE/WS/'semantic-receipts.json').read_text())
    assert {r['id'] for r in receipts}==set(PRIMARY)
    for receipt in receipts:
        assert all(receipt[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
        for target in receipt['targets']:
            assert (STAGE/target).exists() or (REPO/target).exists(),target
    result=dict(kind='artifact-byte-scope-and-recorded-run-validation',all_checks_passed=True,primary_count=5,formal_object_count=len(formal),receipt_count=len(receipts),local_link_count=len(links),links=links,frozen_scan_directory_set_exact=True,recorded_original_mains=2,executions_per_original_main=1,supplement_executions=1,scope='No source main or supplement is executed by this mechanical checker. The two original reports are exact byte replays; floating success is not an exact dual or universal theorem, and the supplement checks no SPE ICs.')
    dump(EV/'verification.json',result)
    print(json.dumps({k:result[k] for k in ['kind','all_checks_passed','formal_object_count','receipt_count','local_link_count','frozen_scan_directory_set_exact','recorded_original_mains']},ensure_ascii=False))

if __name__=='__main__':
    main()
