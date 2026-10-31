"""Check saved bytes/records and exact scalar identities. No source main/import/LP."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,os,re,subprocess
REPO=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
STAGE=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-alpha-oq-fixed-saddle-audits')
EV=Path('archives/customer-attraction/tools/evidence/alpha-oq-fixed-saddle-primary')
WS=Path('cleanup/workspaces/Boss4/r3-alpha-oq-fixed-saddle-audits')
PRIMARY=['9edffc6508386d059f3a','a33dd82cb4d23fab6163','8b9cf44d16a024398ef3','17bad95333c2be5f6402','34930f098ddd0db955e8']
CURRENT_FULL=[
 'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md',
 'archives/customer-attraction/state/定义/跨分支去相关与激励补偿总预算--定义.md',
 'archives/customer-attraction/state/定理/完整策略锥的静态安全值对偶--定理.md',
 'archives/customer-attraction/state/等价/固定完整SPE策略锥的有限价格合同--等价.md',
 'archives/customer-attraction/state/定理/静态混合安全值的锐目录计数界--定理.md',
 'archives/customer-attraction/state/反例/三人全分布补偿预算--反例.md',
 'archives/customer-attraction/state/反例/三人逐人混合安全值--反例.md',
 'archives/customer-attraction/state/审查/指定完整策略锥安全证书与预算边界--审查.md',
 'archives/customer-attraction/state/引理/完整槽均值cap的原源范数账与付款接口--引理.md',
 'archives/customer-attraction/state/审查/可信均值菜单与完整槽的内部复核合同--审查.md',
 'archives/customer-attraction/state/反例/实际均匀缩放负载的弱付款桥--反例.md',
 'archives/customer-attraction/state/计算/分数负载四主题族的全历史核验--计算.md',
]
CURRENT_SCOPE=[
 'archives/customer-attraction/state/定理/五人半覆盖--定理.md',
 'archives/customer-attraction/subarchives/six-providers/问题--问题.md',
]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def dump(rel,obj):
    path=STAGE/rel;path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def snapshot(path):
    raw=(REPO/path).read_bytes()
    return dict(path=str(path),size=len(raw),sha256=sha(raw))
def main():
    dump(EV/'verification.json',dict(all_checks_passed=False,status='checking-existing-records'))
    inv={r['id']:r for r in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
    runtime=json.loads((STAGE/EV/'runtime-input-manifest.json').read_text())
    rows=runtime['sources'];byid={r['id']:r for r in rows}
    assert {r['id']for r in rows if r['role']=='primary'}==set(PRIMARY)
    assert runtime['runtime_dependency_count']==2 and runtime['primary_bytes']==15274
    for row in rows:
        record=inv[row['id']];raw=(STAGE/row['saved_path']).read_bytes()
        assert len(raw)==record['size']and sha(raw)==record['sha256']
        assert len(row['sources'])==len(record['sources'])and all(loc['bytes_verified']for loc in row['sources'])
    # Full-text alpha-one MD comparison; not an additional primary disposition.
    sid='6b81f6445e9914b0b550';record=inv[sid];first=None;locations=[]
    for loc in record['sources']:
        raw=subprocess.check_output(['git','show',loc['commit']+':'+loc['path']],cwd=REPO,timeout=30,env=dict(os.environ,GIT_NO_LAZY_FETCH='1'))
        assert len(raw)==record['size']and sha(raw)==record['sha256']
        assert first is None or first==raw
        first=raw;locations.append(dict(loc,bytes_verified=True))
    rel=EV/'original'/record['path'];(STAGE/rel).parent.mkdir(parents=True,exist_ok=True);(STAGE/rel).write_bytes(first)
    rows.append(dict(id=sid,path=record['path'],size=record['size'],sha256=record['sha256'],sources=locations,role='comparison-only-not-done',read_scope='full-text',saved_path=str(rel)))
    dump(EV/'source-manifest.json',dict(claim_push='6976742b9e0d64b0fd6ea8cbd7dd34e3acac5bd2',root_local_sync_at_claim='needs-attention; no synced assertion from this stage',primary_count=5,primary_bytes=15274,runtime_dependency_count=2,runtime_dependency_bytes=377206,comparison_count=1,sources=rows,current_objects=[dict(snapshot(p),read_scope='full-text')for p in CURRENT_FULL]+[dict(snapshot(p),read_scope='model-and-status-passages-only')for p in CURRENT_SCOPE],local_blob_reads_no_lazy_fetch=True))
    execution=json.loads((STAGE/EV/'replay/execution.json').read_text())
    assert execution['status']=='finished'and execution['executions_of_original_entrypoint']==1 and execution['exit_code']==0
    assert execution['generated_report_byte_identical_to_frozen']and execution['code_and_inputs_unchanged']
    frozen=STAGE/byid['34930f098ddd0db955e8']['saved_path']
    generated=STAGE/EV/'replay/optimal_query_fixed_cone_attack.json'
    assert frozen.read_bytes()==generated.read_bytes()
    assert sha(generated.read_bytes())==execution['generated_report_sha256']
    for sid in ['17bad95333c2be5f6402','847a210188334e25b4bd','8d74fd183eba467a811f']:
        assert sha((STAGE/EV/'replay-tree'/byid[sid]['path']).read_bytes())==byid[sid]['sha256']
    assert (STAGE/EV/'replay/stderr.txt').read_bytes()==b''
    report=json.loads(generated.read_text())
    assert (report['n'],report['k'],report['types'],report['gamma_distinct'],report['static_backgrounds'])==(13,6,63,31454,6188)
    p=list(map(F,report['p']));Q=report['Q']
    assert all(x>=0 for x in p)and sum(p)==1
    assert sum(F(r['probability'])for r in Q)==1 and all(F(r['probability'])>0 for r in Q)
    assert len(Q)==6 and all(len(r['background'])==6 and sum(r['background'])==12 and min(r['background'])>=0 for r in Q)
    assert F(report['original_exact_safety_value'])==F(30955,13476)
    assert F(report['original_exact_sum_C'])-F(report['original_W'])==F(-451885873,181602576)
    assert report['max_C_minus_W_normalized']==0
    assert report['rational_min_slack']==report['rational_C_minus_W']=='0'
    assert report['rational_v']=='1/13'and report['weights']=={'63':'1'}
    assert report['packet_sha256']==byid['8d74fd183eba467a811f']['sha256']
    # Exact scalar equality to existing sufficiently executed old13 evidence.
    old=Path('archives/customer-attraction/tools/evidence/fractional-load-boundaries')
    paths=[
      Path('archives/customer-attraction/state/反例/实际均匀缩放负载的弱付款桥--反例.md'),
      Path('archives/customer-attraction/state/计算/分数负载四主题族的全历史核验--计算.md'),
      old/'source-manifest.json',old/'replay-summary.json',old/'replay-refined-tax.json',old/'replay-alpha-one.json',old/'replay.py',
      old/'original/research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/security/audit_refined_tax_packet.py',
      old/'original/research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_k10_packet.json.gz',
    ]
    for sid in ['9edffc6508386d059f3a','a33dd82cb4d23fab6163','6b81f6445e9914b0b550']:
        path=old/'original'/inv[sid]['path'];paths.append(path)
        assert sha((REPO/path).read_bytes())==inv[sid]['sha256']
    alpha=json.loads((STAGE/byid['a33dd82cb4d23fab6163']['saved_path']).read_text())
    oldalpha=json.loads((REPO/old/'replay-alpha-one.json').read_text())
    assert alpha==oldalpha
    assert alpha['source_sha256']==report['packet_sha256']==sha((REPO/paths[8]).read_bytes())
    assert alpha['m_max_g_minus_W_minus_J']==alpha['max_F_minus_W_minus_J']=='37/66'
    oldSPE=json.loads((REPO/old/'replay-refined-tax.json').read_text())
    assert (oldSPE['automaton_nodes'],oldSPE['decision_nodes'],oldSPE['decision_comparisons'],oldSPE['minimum_spe_gap'])==(27243,18675,112050,'0')
    dump(EV/'reused-old13-evidence.json',dict(scope='Existing complete-SPE audit plus same-SHA alpha-one scalar execution reused; neither original main executed this batch.',alpha_one_primary_ids=PRIMARY[:2],alpha_one_executions_this_batch=0,full_SPE_original_executions_this_batch=0,alpha_output_semantically_equal_to_original=True,alpha_original_output_byte_equal_to_existing_replay=(STAGE/byid['a33dd82cb4d23fab6163']['saved_path']).read_bytes()==(REPO/old/'replay-alpha-one.json').read_bytes(),source_packet_sha256=report['packet_sha256'],existing_records=[snapshot(p)for p in paths]))
    formal=sorted((STAGE/'archives/customer-attraction/state').rglob('*.md'));links=[]
    for path in formal+[STAGE/EV/'README.md']:
        content=path.read_text()
        if path in formal:
            assert content.startswith('---\n');front=content.split('---',2)[1]
            for key in ['id','kind','type_tag','title','status','summary','source_refs']:
                assert re.search('^'+key+':',front,re.M),(path,key)
        assert content.count(r'\[')==content.count(r'\]'),path
        assert content.count(r'\(')==content.count(r'\)'),path
        for target in re.findall(r'\]\(([^)]+)\)',content):
            if '://'in target or target.startswith('#'):continue
            dest=(path.parent/target.split('#')[0]).resolve();rel=dest.relative_to(STAGE)
            assert dest.exists()or(REPO/rel).exists(),(path,target)
            links.append(dict(file=str(path.relative_to(STAGE)),target=target,resolves=True))
    receipts=json.loads((STAGE/WS/'semantic-receipts.json').read_text())
    assert len(receipts)==5 and {r['id']for r in receipts}==set(PRIMARY)
    assert {r['id']for r in receipts if r['disposition']=='duplicate'}==set(PRIMARY[:2])
    for row in receipts:
        assert all(row[k]for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note'])
        assert all((STAGE/t).exists()or(REPO/t).exists()for t in row['targets'])
    result=dict(kind='frozen-bytes-and-recorded-results-check-no-source-execution',all_checks_passed=True,formal_objects=len(formal),primary_receipts=len(receipts),local_links=len(links),links=links,recorded_OQ_main_executions=1,recorded_internal_LP_calls=3,alpha_one_executions_this_batch=0,old_full_SPE_audit_executions_this_batch=0,helper_search_main_executions_this_batch=0,exact_normalized_recovered_point={'63':'1'},scope='Exact original saddle and exact feasible zero point are distinct from floating fixed-cone optimum; no exact cone upper certificate or general funding/HALF conclusion.')
    dump(EV/'verification.json',result)
    print(json.dumps({k:result[k]for k in ['all_checks_passed','formal_objects','primary_receipts','local_links','recorded_OQ_main_executions','recorded_internal_LP_calls']},ensure_ascii=False))
if __name__=='__main__':main()
