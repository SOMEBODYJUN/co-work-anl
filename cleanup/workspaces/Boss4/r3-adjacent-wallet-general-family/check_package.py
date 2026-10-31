"""Frozen bytes, recorded execution, receipt and artifact links; no source run."""
from pathlib import Path
import hashlib,json,os,re,subprocess
REPO=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
STAGE=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-adjacent-wallet-general-family')
EV=Path('archives/customer-attraction/tools/evidence/adjacent-wallet-general-family-primary')
WS=Path('cleanup/workspaces/Boss4/r3-adjacent-wallet-general-family')
PRIMARY=['81bc4b8504d7a37b9805','3a4479719e981f9bc43d','2e83f00a05168c0aa558','d6ada5ea6dd4defa20fe','662bb9acaf7487aaf7e7']
COMPARE=['5aa36b9a875a25bc107b','23058322be690f0f6cc0','6b81f6445e9914b0b550']
CURRENT_FULL=[
 'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md',
 'archives/customer-attraction/state/算法/完整历史纯SPE终局全集--算法.md',
 'archives/customer-attraction/state/问题/完整历史计数策略净化--问题.md',
 'archives/customer-attraction/state/反例/同负载历史的不同续局--反例.md',
 'archives/customer-attraction/state/反例/十客户重复实际行的相邻钱包失败--反例.md',
 'archives/customer-attraction/state/引理/静态覆盖松弛吸收末对钱包的直接缺额式--引理.md',
 'archives/customer-attraction/state/候选/真实最优组合的净差匹配与共同付款--候选.md',
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
        target=EV/'original'/row['path'];(STAGE/target).parent.mkdir(parents=True,exist_ok=True);(STAGE/target).write_bytes(first)
        records.append(dict(id=sid,path=row['path'],blob=row['blob'],size=row['size'],sha256=row['sha256'],sources=locations,role='primary' if sid in PRIMARY else 'comparison-only-not-done',read_scope='full-text',saved_path=str(target)))
    current=[]
    for path in CURRENT_FULL+CURRENT_SCOPE:
        raw=(REPO/path).read_bytes();current.append(dict(path=path,size=len(raw),sha256=sha(raw),read_scope='full-text' if path in CURRENT_FULL else 'model-scope-and-status-passages-only'))
    dump(EV/'source-manifest.json',dict(primary_count=5,primary_bytes=sum(r['size'] for r in records if r['role']=='primary'),comparison_count=3,comparison_bytes=sum(r['size'] for r in records if r['role']=='comparison-only-not-done'),external_runtime_dependency_count=0,sources=records,current_objects=current,claim_push='e8bb5a61692cd2aa542bbb4e710bc00c3bdf6ada',source_program_execution='one exact count-prefix audit main; no other mathematical program execution',local_blob_reads_no_lazy_fetch=True))
    execution=json.loads((STAGE/EV/'replay/execution.json').read_text())
    assert execution['executions_of_original_entrypoint']==1 and execution['exit_code']==0
    assert execution['generated_report_byte_identical_to_frozen'] and execution['original_code_bytes_unchanged']
    raw=(STAGE/EV/'replay/optimal_adjacent_family_exact_audit.json').read_bytes()
    assert raw==(STAGE/EV/'original'/inv['2e83f00a05168c0aa558']['path']).read_bytes()
    assert sha(raw)==execution['generated_report_sha256']
    cases=json.loads(raw)['cases'];assert [r['m'] for r in cases]==[2,3,5,7]
    assert sum(r['count_prefix_states'] for r in cases)==5361
    assert sum(r['IC_checked_with_self'] for r in cases)==47480
    assert sum(r['all_ordered_histories_represented'] for r in cases)==600708
    assert [r['minimum_optimal_gap'] for r in cases]==['-2','-3/2','-1/2','1/2']
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
    receipts=json.loads((STAGE/WS/'semantic-receipts.json').read_text());assert {r['id'] for r in receipts}==set(PRIMARY)
    for r in receipts:
        assert all(r[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
        for target in r['targets']:assert (STAGE/target).exists() or (REPO/target).exists(),target
    result=dict(kind='frozen-byte-and-artifact-record-validation',all_checks_passed=True,formal_object_count=len(formal),receipt_count=len(receipts),local_link_count=len(links),links=links,recorded_original_main_executions=1,count_states_actually_iterated=5361,IC_comparisons_actually_checked=47480,ordered_histories_represented_not_iterated=600708,scope='No mathematical original is executed by this checker; analytic all-m proof separate from the four-case exact QA. No count-policy purification, general funding or HALF conclusion.')
    dump(EV/'verification.json',result);print(json.dumps({k:result[k] for k in ['kind','all_checks_passed','formal_object_count','receipt_count','local_link_count']},ensure_ascii=False))
if __name__=='__main__':main()
