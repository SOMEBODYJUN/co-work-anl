"""Validate frozen bytes and already recorded runs; execute no mathematical source."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,os,re,subprocess

REPO=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
STAGE=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-security-named-attack-history')
EV=Path('archives/customer-attraction/tools/evidence/security-named-attack-history-primary')
WS=Path('cleanup/workspaces/Boss4/r3-security-named-attack-history')
PRIMARY=['2c2fdb99195aa0a9e3ad','1d305bb3f9999d836b5b','c19b4a93560ff473adf5','6aca9b93763f751a2cb7','6b81f6445e9914b0b550']
COMPARE=['0726b9dff91beaee504d','8b9cf44d16a024398ef3','17bad95333c2be5f6402','34930f098ddd0db955e8']
CURRENT_FULL=[
 'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md',
 'archives/customer-attraction/state/算法/完整历史纯SPE终局全集--算法.md',
 'archives/customer-attraction/state/反例/三人碰撞自由族福利障碍--反例.md',
 'archives/customer-attraction/state/障碍/最大主题加性预算与分数价格曲线--障碍.md',
 'archives/customer-attraction/state/引理/静态覆盖松弛吸收末对钱包的直接缺额式--引理.md',
 'archives/customer-attraction/state/反例/十客户重复实际行的相邻钱包失败--反例.md',
 'archives/customer-attraction/state/反例/唯一最优支持下相邻钱包的固定倍数反族--反例.md',
 'archives/customer-attraction/state/反例/实际均匀缩放负载的弱付款桥--反例.md',
 'archives/customer-attraction/state/计算/分数负载四主题族的全历史核验--计算.md',
]
CURRENT_SCOPE=[
 'archives/customer-attraction/state/定理/五人半覆盖--定理.md',
 'archives/customer-attraction/subarchives/six-providers/问题--问题.md',
]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def dump(rel,obj):
    (STAGE/rel).parent.mkdir(parents=True,exist_ok=True)
    (STAGE/rel).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def snapshot(path):
    raw=(REPO/path).read_bytes()
    return dict(path=str(path),size=len(raw),sha256=sha(raw))
def main():
    dump(EV/'verification.json',dict(all_checks_passed=False,status='checking-existing-evidence'))
    inv={r['id']:r for r in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
    runtime=json.loads((STAGE/EV/'runtime-input-manifest.json').read_text())
    records=runtime['frozen_sources']
    assert {r['id'] for r in records if r['role']=='primary'}==set(PRIMARY)
    assert runtime['runtime_dependency_count']==3
    for record in records:
        row=inv[record['id']]
        raw=(STAGE/record['saved_path']).read_bytes()
        assert len(raw)==row['size'] and sha(raw)==row['sha256']
        assert all(loc['bytes_verified'] for loc in record['sources'])
        assert len(record['sources'])==len(row['sources'])
    for sid in COMPARE:
        row=inv[sid];first=None;locations=[]
        for loc in row['sources']:
            raw=subprocess.check_output(['git','show',loc['commit']+':'+loc['path']],cwd=REPO,timeout=30,env=dict(os.environ,GIT_NO_LAZY_FETCH='1'))
            assert len(raw)==row['size'] and sha(raw)==row['sha256']
            assert first is None or first==raw
            first=raw;locations.append(dict(loc,bytes_verified=True))
        target=EV/'original'/row['path']
        (STAGE/target).parent.mkdir(parents=True,exist_ok=True)
        (STAGE/target).write_bytes(first)
        records.append(dict(id=sid,path=row['path'],size=row['size'],sha256=row['sha256'],blob=row['blob'],sources=locations,role='comparison-only-not-done',read_scope='full-file',saved_path=str(target)))
    current=[dict(snapshot(p),read_scope='full-text')for p in CURRENT_FULL]
    current += [dict(snapshot(p),read_scope='model-and-status-passages-only')for p in CURRENT_SCOPE]
    dump(EV/'source-manifest.json',dict(claim_push='a00c34fe9498ab5bc9439b7a1c12d60bccf8805b',primary_count=5,primary_bytes=sum(inv[s]['size']for s in PRIMARY),runtime_dependency_count=3,runtime_dependency_bytes=sum(r['size']for r in records if r['role']=='runtime-dependency-only-not-done'),comparison_count=len(COMPARE),comparison_bytes=sum(inv[s]['size']for s in COMPARE),sources=records,current_objects=current,original_entrypoints_executed_this_batch=1,local_blob_reads_no_lazy_fetch=True))
    execution=json.loads((STAGE/EV/'replay/execution.json').read_text())
    assert execution['executions_of_original_entrypoint']==1 and execution['exit_code']==0
    assert execution['generated_report_byte_identical_to_frozen'] and execution['code_and_input_bytes_unchanged']
    raw=(STAGE/EV/'replay/adjacent_wallet_named_packets.json').read_bytes()
    assert raw==(STAGE/EV/'original'/inv['c19b4a93560ff473adf5']['path']).read_bytes()
    assert sha(raw)==execution['generated_report_sha256']
    for row in runtime['replay_code_and_inputs']:
        assert sha((STAGE/EV/'replay-tree'/row['path']).read_bytes())==row['sha256']
    packets=json.loads(raw)['packets'];assert len(packets)==2
    assert sum(p['ordered_decision_histories']for p in packets)==302
    assert sum(p['comparisons_including_self']for p in packets)==1812
    assert sum(p['nonself_comparisons']for p in packets)==1510
    assert sum(p['topics']**p['m']for p in packets)==1512
    expected=[
      dict(name='old52',W=47,OPT=52,row_maximizing_tuple=[0,0,0,0],minimum_optimal_Q='48',minimum_optimal_assignment=[0,5,1,4],optimal_ordered_comparison_tuples=24,strong_gap_left_minus_wallets='-11/6',weak_gap_min_Q_minus_W_minus_wallets='-17/6',minimum_static_cashout_margin_over_all_comparisons='167/6'),
      dict(name='old1953',W=1735,OPT=1740,row_maximizing_tuple=[1,1,1],minimum_optimal_Q='1736',minimum_optimal_assignment=[1,2,5],optimal_ordered_comparison_tuples=6,strong_gap_left_minus_wallets='-983/3',weak_gap_min_Q_minus_W_minus_wallets='-986/3',minimum_static_cashout_margin_over_all_comparisons='2732/3'),
    ]
    for p,want in zip(packets,expected):
        for key,value in want.items():assert p[key]==value,(p['name'],key)
        assert p['minimum_SPE_gap']=='0'
        assert sum(map(F,p['actual_payoffs']))==p['W']
        assert sum(map(F,p['adjacent_wallets']))==F(p['wallet_sum'])
        assert [str(max(map(F,row)))for row in p['frozen_matrix']]==p['row_maxima']
        assert sum(map(F,p['row_maxima']))-p['W']==F(p['strong_left_sum_max_minus_W'])==2
        assert F(p['minimum_optimal_Q'])-p['W']-F(p['wallet_sum'])==F(p['weak_gap_min_Q_minus_W_minus_wallets'])
    # This is reuse of an existing execution, never a new invocation.
    old=Path('archives/customer-attraction/tools/evidence/fractional-load-boundaries')
    reusepaths=[
      Path('archives/customer-attraction/state/反例/实际均匀缩放负载的弱付款桥--反例.md'),
      Path('archives/customer-attraction/state/计算/分数负载四主题族的全历史核验--计算.md'),
      old/'source-manifest.json',old/'replay-summary.json',old/'replay-refined-tax.json',old/'replay-alpha-one.json',old/'replay.py',
      old/'original/research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/security/audit_refined_tax_packet.py',
      old/'original/research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_k10_packet.json.gz',
    ]
    for sid in ['6b81f6445e9914b0b550','9edffc6508386d059f3a','a33dd82cb4d23fab6163']:
        path=old/'original'/inv[sid]['path'];reusepaths.append(path)
        assert sha((REPO/path).read_bytes())==inv[sid]['sha256']
    alpha=json.loads((REPO/old/'replay-alpha-one.json').read_text())
    automaton=json.loads((REPO/old/'replay-refined-tax.json').read_text())
    assert alpha['source_sha256']=='bad2b15d1abe89d9fa8671df84de8638a4b1ca46279712baa5482abb2bdf18ce'
    assert sha((REPO/reusepaths[8]).read_bytes())==alpha['source_sha256']
    assert alpha['m_max_g_minus_W_minus_J']==alpha['max_F_minus_W_minus_J']=='37/66'
    assert automaton['automaton_nodes']==27243 and automaton['decision_nodes']==18675 and automaton['decision_comparisons']==112050
    assert inv['6b81f6445e9914b0b550']['path'] in (REPO/reusepaths[0]).read_text()
    dump(EV/'reused-old13-evidence.json',dict(scope='Existing same-SHA full automaton and alpha-one scalar executions reused; no new old13 run or duplicate counterexample object.',this_batch_old13_executions=0,primary_md_id='6b81f6445e9914b0b550',primary_md_sha256=inv['6b81f6445e9914b0b550']['sha256'],source_packet_sha256=alpha['source_sha256'],existing_records=[snapshot(p)for p in reusepaths],existing_automaton_counts=dict(nodes=27243,decision_nodes=18675,incl_self_IC=112050),existing_scalar_violation='37/66'))
    formal=sorted((STAGE/'archives/customer-attraction/state').rglob('*.md'));links=[]
    for path in formal+[STAGE/EV/'README.md']:
        content=path.read_text()
        if path in formal:
            assert content.startswith('---\n')
            front=content.split('---',2)[1]
            for key in ['id','kind','type_tag','title','status','summary','source_refs']:
                assert re.search('^'+key+':',front,re.M),(path,key)
        assert content.count(r'\[')==content.count(r'\]'),path
        assert content.count(r'\(')==content.count(r'\)'),path
        for target in re.findall(r'\]\(([^)]+)\)',content):
            if '://' in target or target.startswith('#'):continue
            resolved=(path.parent/target.split('#')[0]).resolve();rel=resolved.relative_to(STAGE)
            assert resolved.exists() or (REPO/rel).exists(),(path,target)
            links.append(dict(file=str(path.relative_to(STAGE)),target=target,resolves=True))
    receipts=json.loads((STAGE/WS/'semantic-receipts.json').read_text())
    assert {r['id']for r in receipts}==set(PRIMARY)
    assert len(receipts)==5
    for row in receipts:
        assert all(row[k]for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
        assert all(row[k]for k in ['read_note','comparison_note','decision_note'])
        for target in row['targets']:assert (STAGE/target).exists()or(REPO/target).exists(),target
    result=dict(kind='record-and-frozen-byte-validation-no-mathematical-run',all_checks_passed=True,formal_objects=len(formal),primary_receipts=len(receipts),local_links=len(links),links=links,recorded_original_main_executions=1,old13_executions_this_batch=0,optimal_query_LP_executions_this_batch=0,ordered_decision_histories=302,incl_self_IC=1812,nonself_IC=1510,ordered_comparison_tuples=1512,scope='Finite named diagnostics, existing old13 evidence reuse, analytic static identities and corrected candidate status; no universal funding or HALF upgrade.')
    dump(EV/'verification.json',result)
    print(json.dumps({k:result[k]for k in ['all_checks_passed','formal_objects','primary_receipts','local_links','recorded_original_main_executions']},ensure_ascii=False))
if __name__=='__main__':main()
