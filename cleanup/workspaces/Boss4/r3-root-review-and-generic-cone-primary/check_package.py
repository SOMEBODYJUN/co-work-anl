"""Recorded-byte/results validation only; do not run a source main or LP."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,re
REPO=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
STAGE=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-root-review-and-generic-cone-primary')
EV=Path('archives/customer-attraction/tools/evidence/root-review-and-generic-cone-primary')
WS=Path('cleanup/workspaces/Boss4/r3-root-review-and-generic-cone-primary')
IDS=['8fb492268f7ad2fd3e37','cc31f0e547a5bce7512e','deb74d312cf9a35b4985','847a210188334e25b4bd','d0790545c28af71b92b1']
CURRENT_FULL=[
 'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md',
 'archives/customer-attraction/state/定理/完整策略锥的静态安全值对偶--定理.md',
 'archives/customer-attraction/state/定义/跨分支去相关与激励补偿总预算--定义.md',
 'archives/customer-attraction/state/定理/静态混合安全值的锐目录计数界--定理.md',
 'archives/customer-attraction/state/反例/唯一根成员平稳核的弱封顶失败--反例.md',
 'archives/customer-attraction/state/计算/根平稳弱核的原审计与三人锥探针--计算.md',
 'archives/customer-attraction/state/计算/固定原安全鞍点下的完整策略查询锥审计--计算.md',
]
CURRENT_SCOPE=['archives/customer-attraction/state/定理/五人半覆盖--定理.md','archives/customer-attraction/subarchives/six-providers/问题--问题.md']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def dump(rel,obj):
    p=STAGE/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def main():
    dump(EV/'verification.json',dict(all_checks_passed=False,status='checking-saved-artifacts'))
    inv={r['id']:r for r in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
    sm=json.loads((STAGE/EV/'source-manifest.json').read_text());rows={r['id']:r for r in sm['sources']}
    assert {r['id']for r in rows.values()if r['role']=='primary'}==set(IDS)
    assert (sm['primary_bytes'],sm['runtime_dependency_bytes'],sm['comparison_bytes'])==(25179,372216,21873)
    for sid,row in rows.items():
        raw=(STAGE/row['saved_path']).read_bytes()
        assert len(raw)==inv[sid]['size']and sha(raw)==inv[sid]['sha256']
        assert len(row['sources'])==2 and all(loc['bytes_verified']for loc in row['sources'])
    for kind,cid,rid in [('review',IDS[0],IDS[1]),('cone',IDS[3],IDS[4])]:
        folder=EV/('replay-'+kind);event=json.loads((STAGE/folder/'execution.json').read_text())
        assert event['status']=='finished'and event['original_main_executions']==1 and event['exit_code']==0
        assert event['code_and_input_bytes_unchanged']and event['generated_report_byte_identical_to_frozen']and event['generated_report_semantically_equal_to_frozen']
        output=Path(event['actual_generated_relative_path']).name
        raw=(STAGE/folder/output).read_bytes()
        assert raw==(STAGE/rows[rid]['saved_path']).read_bytes()and sha(raw)==event['generated_report_sha256']
        assert (STAGE/folder/'stderr.txt').read_bytes()==b''
        for sid in [cid,'8d74fd183eba467a811f']:
            assert sha((STAGE/EV/'replay-tree'/rows[sid]['path']).read_bytes())==rows[sid]['sha256']
    r=json.loads((STAGE/rows[IDS[1]]['saved_path']).read_text())
    assert (r['players'],r['unit_customers'],r['reachable_automaton_nodes'],r['checked_true_deviations'],r['augmented_rank'])==(13,36,27243,93375,6)
    assert r['source_sha256']==rows['8d74fd183eba467a811f']['sha256']
    pi=list(map(F,r['stationary_probability']));tails=r['root_tail_counts'];assert sum(pi)==1 and min(pi)>=0
    assert all(len(B)==6 and sum(B)==12 for B in tails)
    assert all(sum(pi[a]*F(tails[a][b],12)for a in range(6))==pi[b]for b in range(6))
    assert max(map(F,r['queries'].values()))==F(r['cap'])==F(427,156)
    assert F(r['cap'])-F(r['weak_bound_W_over_m_minus_half'])==F(r['exact_weak_violation'])==F(379,3900)
    assert max(map(F,r['unrestricted_query_values']))==F(5,2)<F(r['W'],13)
    cone=json.loads((STAGE/rows[IDS[4]]['saved_path']).read_text());trace=cone['trace']
    assert len(trace)==32 and {item['start']for item in trace}==set(range(16))
    for start in range(16):assert [item['iteration']for item in trace if item['start']==start]==[0,1]
    for item in trace:
        assert item['p']==[1.0,0.0,0.0,0.0,0.0,0.0]and item['weights']==[[63,1.0]]
        assert item['W']==1.0 and item['v']==0.07692307692307693 and item['true_gap']==0.0
        assert item['true_gap']==13*item['v']-item['W']
    assert cone['best']==trace[0]and cone['best']['start']==cone['best']['iteration']==0
    assert max(item['cone_margin']for item in trace)==4.218847493575595e-15
    assert min(item['cone_margin']for item in trace)==-3.3306690738754696e-16
    ce=json.loads((STAGE/EV/'replay-cone/execution.json').read_text())
    assert (ce['executed_mode'],ce['executed_factor'],ce['start_count'],ce['generated_trace_rows'],ce['internal_LP_calls_from_completed_control_flow'])==('all',13,16,32,65)
    assert Path(ce['actual_generated_relative_path']).name=='cone_security_probe_all_13.json'
    assert Path(ce['frozen_report_relative_path']).name=='cone_security_probe.json'
    current=[]
    for path in CURRENT_FULL+CURRENT_SCOPE:
        raw=(REPO/path).read_bytes();current.append(dict(path=path,size=len(raw),sha256=sha(raw),read_scope='full-text'if path in CURRENT_FULL else'model-and-status-passages'))
    dump(EV/'current-comparison-manifest.json',dict(objects=current,comparison_source_dispositions_this_batch=0))
    # The review MD's mathematical result and prior identity already have a source_ref.
    assert rows[IDS[2]]['path']in (REPO/CURRENT_FULL[4]).read_text()
    formal=sorted((STAGE/'archives/customer-attraction/state').rglob('*.md'));links=[]
    for path in formal+[STAGE/EV/'README.md']:
        content=path.read_text()
        if path in formal:
            assert content.startswith('---\n');front=content.split('---',2)[1]
            for key in ['id','kind','type_tag','title','status','summary','source_refs']:assert re.search('^'+key+':',front,re.M),(path,key)
        assert content.count(r'\[')==content.count(r'\]')and content.count(r'\(')==content.count(r'\)'),path
        for target in re.findall(r'\]\(([^)]+)\)',content):
            if '://'in target or target.startswith('#'):continue
            dest=(path.parent/target.split('#')[0]).resolve();rel=dest.relative_to(STAGE)
            assert dest.exists()or(REPO/rel).exists(),(path,target)
            links.append(dict(file=str(path.relative_to(STAGE)),target=target,resolves=True))
    receipts=json.loads((STAGE/WS/'semantic-receipts.json').read_text())
    assert len(receipts)==5 and {r['id']for r in receipts}==set(IDS)
    assert {r['id']for r in receipts if r['disposition']=='duplicate'}=={IDS[2]}
    for row in receipts:
        assert all(row[k]for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note'])
        assert all((STAGE/t).exists()or(REPO/t).exists()for t in row['targets'])
    result=dict(kind='recorded-source-bytes-results-and-trace-check-no-original-run',all_checks_passed=True,formal_objects=len(formal),primary_receipts=len(receipts),local_links=len(links),links=links,root_review_original_main_executions=1,generic_original_main_executions=1,generic_default_mode='all',generic_factor=13,generic_starts=16,generic_trace_rows=32,generic_internal_LP_calls=65,other_modes_executed=0,scope='Independent fixed old13 certification plus finite alternating numerical diagnostic. Exact all-interest zero point has no global cone upper certificate; no HALF/general-security conclusion.')
    dump(EV/'verification.json',result);print(json.dumps({k:result[k]for k in ['all_checks_passed','formal_objects','primary_receipts','local_links','root_review_original_main_executions','generic_original_main_executions']},ensure_ascii=False))
if __name__=='__main__':main()
