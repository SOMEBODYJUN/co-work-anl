"""Frozen-byte/receipt/link checks only; no original mathematical execution."""
from pathlib import Path
import hashlib,json,os,re,subprocess
REPO=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
STAGE=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-harmonic-terminal-wallet')
EV=Path('archives/customer-attraction/tools/evidence/harmonic-terminal-wallet-primary')
WS=Path('cleanup/workspaces/Boss4/r3-harmonic-terminal-wallet')
PRIMARY=['f811c6617841fee2c723','70c3ea6d4f224667baf7','24605d29e47dc547a839','1deb05327659c64eae69','1a2500b24700429ddb8f']
DEPS=['3beb17d5735520b90e84','a7579960b289fff40c97','ff1a437e39e730d230eb','be317a14860bf5650dfe']
COMPARE=['81913c1ed717b432237f','2f4d8aa26332bab930ee','31bf9999273ddef0652e','01cb20ba6f27569c9083','40e1c6a28becf4e756ba','aa9b31201d1ae21709cf','5d0f5a3be2fc9f249d5a','23058322be690f0f6cc0']
CURRENT_FULL=[
 'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md',
 'archives/customer-attraction/state/引理/实际末对冻结查询的选择性钱包--引理.md',
 'archives/customer-attraction/state/计算/终局冻结钱包原程序及完整策略复跑--计算.md',
 'archives/customer-attraction/state/引理/循环污染查询的加权调和付款--引理.md',
 'archives/customer-attraction/state/反例/静态最优主题排列的冻结后缀失败--反例.md',
 'archives/customer-attraction/state/计算/弱匹配与分区查询的精确核验--计算.md',
]
CURRENT_SCOPE=['archives/customer-attraction/state/定理/五人半覆盖--定理.md','archives/customer-attraction/subarchives/six-providers/问题--问题.md']
def sha(raw): return hashlib.sha256(raw).hexdigest()
def dump(path,obj):
    (STAGE/path).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def main():
    dump(EV/'verification.json',dict(all_checks_passed=False,status='validation-in-progress'))
    inv={r['id']:r for r in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
    records=[]
    for sid in PRIMARY+DEPS+COMPARE:
        row=inv[sid]
        first=None
        locations=[]
        for loc in row['sources']:
            raw=subprocess.check_output(['git','show',loc['commit']+':'+loc['path']],cwd=REPO,timeout=30,env=dict(os.environ,GIT_NO_LAZY_FETCH='1'))
            assert len(raw)==row['size'] and sha(raw)==row['sha256']
            assert first is None or first==raw
            first=raw
            locations.append(dict(loc,bytes_verified=True))
        target=EV/'original'/row['path']
        (STAGE/target).parent.mkdir(parents=True,exist_ok=True)
        (STAGE/target).write_bytes(first)
        records.append(dict(id=sid,path=row['path'],blob=row['blob'],size=row['size'],sha256=row['sha256'],sources=locations,role='primary' if sid in PRIMARY else ('runtime-dependency-only-not-done' if sid in DEPS else 'comparison-only-not-done'),read_scope='full-text',saved_path=str(target)))
    current=[]
    for path in CURRENT_FULL+CURRENT_SCOPE:
        raw=(REPO/path).read_bytes()
        current.append(dict(path=path,size=len(raw),sha256=sha(raw),read_scope='full-text' if path in CURRENT_FULL else 'model-scope-and-status-passages-only'))
    dump(EV/'source-manifest.json',dict(primary_count=5,primary_bytes=sum(r['size'] for r in records if r['role']=='primary'),runtime_dependency_count=4,runtime_dependency_bytes=sum(r['size'] for r in records if r['role']=='runtime-dependency-only-not-done'),comparison_count=8,comparison_bytes=sum(r['size'] for r in records if r['role']=='comparison-only-not-done'),sources=records,current_objects=current,claim_push='c201c14b2a6773b8706f7464c6f22f4c0288e649',source_program_execution='one harmonic-terminal-wallet main; round8 audit function called twice, round8 main not called; no weak-Q or peer program run',local_blob_reads_no_lazy_fetch=True))
    execution=json.loads((STAGE/EV/'replay/execution.json').read_text())
    assert execution['executions_of_original_entrypoint']==1 and execution['exit_code']==0
    assert execution['generated_report_byte_identical_to_frozen'] and execution['input_and_code_bytes_unchanged']
    generated=(STAGE/EV/'replay/harmonic_terminal_wallet_exact_audit.json').read_bytes()
    assert generated==(STAGE/EV/'original'/inv['24605d29e47dc547a839']['path']).read_bytes()
    assert sha(generated)==execution['generated_report_sha256']
    report=json.loads(generated)
    assert sum(r['all_true_ic_including_self'] for r in report['cases'].values())==1812
    assert all(r['all_copy_client_and_refund_identities'] for r in report['cases'].values())
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
            assert resolved.exists() or (REPO/rel).exists(),(path,target)
            links.append(dict(file=str(path.relative_to(STAGE)),target=target,resolves=True))
        assert content.count('\\[')==content.count('\\]'),path
    receipts=json.loads((STAGE/WS/'semantic-receipts.json').read_text())
    assert {r['id'] for r in receipts}==set(PRIMARY)
    for r in receipts:
        assert all(r[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
        for target in r['targets']:
            assert (STAGE/target).exists() or (REPO/target).exists(),target
    result=dict(kind='frozen-byte-and-artifact-record-validation',all_checks_passed=True,primary_count=5,formal_object_count=len(formal),receipt_count=len(receipts),local_link_count=len(links),links=links,recorded_original_main_executions=1,recorded_previous_audit_function_calls=2,scope='This checker runs no mathematical source program. General proof in lemma and self-review; finite original replay checks two fixed full policies, not early debt or HALF.')
    dump(EV/'verification.json',result)
    print(json.dumps({k:result[k] for k in ['kind','all_checks_passed','formal_object_count','receipt_count','local_link_count']},ensure_ascii=False))
if __name__=='__main__': main()
