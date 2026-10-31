"""Read-only mathematical evidence/structure check; no original program run."""
from pathlib import Path
import hashlib,json,os,re,subprocess
REPO=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
STAGE=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-direct-surplus-compact-wallet')
EV=Path('archives/customer-attraction/tools/evidence/direct-surplus-compact-wallet-primary')
WS=Path('cleanup/workspaces/Boss4/r3-direct-surplus-compact-wallet')
PRIMARY=['23058322be690f0f6cc0','5aa36b9a875a25bc107b','4f9bddd16812ef8b7605','c056b152c687bc4468ec','8ed477b1d30e8bca1bb1']
COMPARE=['81bc4b8504d7a37b9805','ea4e17bb94b68e371a43','0e4d87b534a528e316c0','8a67f41e320176ef87d5','f0257bb0ec1b1cc5f477','6e553ecf00149eaae721','6b81f6445e9914b0b550','dc1f11657e05cad7e9b6','f811c6617841fee2c723','30449824f9a39ec251e2','d6615b67f13236c12415','d47f19fc500e70147de8']
CURRENT_FULL=[
 'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md',
 'archives/customer-attraction/state/引理/实际末对冻结查询的选择性钱包--引理.md',
 'archives/customer-attraction/state/引理/同一实际福利对末对钱包的调和复制付款--引理.md',
 'archives/customer-attraction/state/计算/调和末对钱包的原审计与审查身份--计算.md',
 'archives/customer-attraction/state/反例/静态最优主题排列的冻结后缀失败--反例.md',
 'archives/customer-attraction/state/想法/最优覆盖查询的自留份额预算--想法.md',
]
CURRENT_SCOPE=['archives/customer-attraction/state/定理/五人半覆盖--定理.md','archives/customer-attraction/subarchives/six-providers/问题--问题.md']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def dump(path,obj):(STAGE/path).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def main():
    dump(EV/'verification.json',dict(all_checks_passed=False,status='validation-in-progress'))
    inv={r['id']:r for r in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
    records=[]
    for sid in PRIMARY+COMPARE:
        row=inv[sid];first=None;locations=[]
        for loc in row['sources']:
            raw=subprocess.check_output(['git','show',loc['commit']+':'+loc['path']],cwd=REPO,timeout=30,env=dict(os.environ,GIT_NO_LAZY_FETCH='1'))
            assert len(raw)==row['size'] and sha(raw)==row['sha256']
            assert first is None or first==raw
            first=raw;locations.append(dict(loc,bytes_verified=True))
        target=EV/'original'/row['path']
        (STAGE/target).parent.mkdir(parents=True,exist_ok=True);(STAGE/target).write_bytes(first)
        records.append(dict(id=sid,path=row['path'],blob=row['blob'],size=row['size'],sha256=row['sha256'],sources=locations,role='primary' if sid in PRIMARY else 'comparison-only-not-done',read_scope='full-text',saved_path=str(target)))
    current=[]
    for path in CURRENT_FULL+CURRENT_SCOPE:
        raw=(REPO/path).read_bytes()
        current.append(dict(path=path,size=len(raw),sha256=sha(raw),read_scope='full-text' if path in CURRENT_FULL else 'model-scope-and-status-passages-only'))
    dump(EV/'source-manifest.json',dict(primary_count=5,primary_bytes=sum(r['size'] for r in records if r['role']=='primary'),comparison_count=12,comparison_bytes=sum(r['size'] for r in records if r['role']=='comparison-only-not-done'),external_runtime_dependency_count=0,sources=records,current_objects=current,claim_push='776eb54ad832ed0a91f8b12fd1bfe1b09680ea38',source_program_execution='one author compact audit main; tree/root literal and general-family programs read only, not run',local_blob_reads_no_lazy_fetch=True))
    execution=json.loads((STAGE/EV/'replay/execution.json').read_text())
    assert execution['executions_of_original_entrypoint']==1 and execution['exit_code']==0
    assert execution['generated_report_byte_identical_to_frozen'] and execution['original_code_bytes_unchanged']
    raw=(STAGE/EV/'replay/compact_adjacent_counterexample_exact.json').read_bytes()
    assert raw==(STAGE/EV/'original'/inv['c056b152c687bc4468ec']['path']).read_bytes()
    assert sha(raw)==execution['generated_report_sha256']
    report=json.loads(raw)
    assert report['full_ordered_decision_histories']==21 and report['all_true_IC_including_self']==84
    assert report['W']==9 and report['OPT']==10 and report['strict_candidate_violation']=='1'
    assert [r['minimum_Q'] for r in report['optimal_assignments']]==['15/2','17/2','8','6']
    counter=STAGE/'archives/customer-attraction/state/反例/十客户重复实际行的相邻钱包失败--反例.md'
    ctext=counter.read_text()
    for row in report['complete_strategy_true_payoffs']:
        h='∅' if not row['history'] else ','.join(row['history'])
        assert '|'+h+'|'+row['action']+'|('+','.join(row['true_deviation_profits'])+')|' in ctext
    formal=sorted((STAGE/'archives/customer-attraction/state').rglob('*.md'));links=[]
    for path in formal+[STAGE/EV/'README.md']:
        content=path.read_text()
        if path in formal:
            assert content.startswith('---\n');front=content.split('---',2)[1]
            for key in ['id','kind','type_tag','title','status','summary','source_refs']:
                assert re.search('^'+key+':',front,re.M),(path,key)
        for target in re.findall(r'\]\(([^)]+)\)',content):
            if '://' in target or target.startswith('#'):continue
            target=target.split('#')[0];resolved=(path.parent/target).resolve();rel=resolved.relative_to(STAGE)
            assert resolved.exists() or (REPO/rel).exists(),(path,target)
            links.append(dict(file=str(path.relative_to(STAGE)),target=target,resolves=True))
        assert content.count('\\[')==content.count('\\]'),path
    receipts=json.loads((STAGE/WS/'semantic-receipts.json').read_text())
    assert {r['id'] for r in receipts}==set(PRIMARY)
    for r in receipts:
        assert all(r[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
        for target in r['targets']:assert (STAGE/target).exists() or (REPO/target).exists(),target
    result=dict(kind='frozen-byte-report-table-and-artifact-validation',all_checks_passed=True,formal_object_count=len(formal),receipt_count=len(receipts),local_link_count=len(links),links=links,all_21_IC_rows_preserved=True,recorded_original_main_executions=1,scope='Checker executes no mathematical original; analytic proof and failure-level checks in self-review, finite original run in replay/execution.json. No HALF counterexample or general early payment claimed.')
    dump(EV/'verification.json',result)
    print(json.dumps({k:result[k] for k in ['kind','all_checks_passed','formal_object_count','receipt_count','local_link_count','all_21_IC_rows_preserved']},ensure_ascii=False))
if __name__=='__main__':main()
