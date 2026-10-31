"""Validate stored results and scalar identities; execute no original or LP."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,re
REPO=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
STAGE=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-root-stationary-weak-history')
EV=Path('archives/customer-attraction/tools/evidence/root-stationary-weak-primary')
WS=Path('cleanup/workspaces/Boss4/r3-root-stationary-weak-history')
IDS=['d9373374b8958e716d53','a5b0c3a6776a1e022678','6808f2beec1bb6b2941b','8b152f1b38c788bfe6c2','e1d7eeedac139253663e']
CURRENT_FULL=[
 'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md',
 'archives/customer-attraction/state/反例/根回复成员平稳核封顶--反例.md',
 'archives/customer-attraction/state/反例/实际终局经验独立核封顶--反例.md',
 'archives/customer-attraction/state/引理/平稳根重置的成员矩与收益协方差--引理.md',
 'archives/customer-attraction/state/反例/成员平稳但根收益不可交换的三人见证--反例.md',
 'archives/customer-attraction/state/定理/末两人回复循环静态运输恒等式--定理.md',
 'archives/customer-attraction/state/计算/末两人运输与指定核的双实现核验--计算.md',
 'archives/customer-attraction/state/障碍/自适应后继与真实菜单安全值--障碍.md',
 'archives/customer-attraction/state/定理/静态混合安全值的锐目录计数界--定理.md',
 'archives/customer-attraction/state/定义/跨分支去相关与激励补偿总预算--定义.md',
 'archives/customer-attraction/state/定理/完整策略锥的静态安全值对偶--定理.md',
]
CURRENT_SCOPE=['archives/customer-attraction/state/定理/五人半覆盖--定理.md','archives/customer-attraction/subarchives/six-providers/问题--问题.md']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def dump(rel,obj):
    p=STAGE/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def main():
    dump(EV/'verification.json',dict(all_checks_passed=False,status='checking-existing-records'))
    inv={r['id']:r for r in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
    sm=json.loads((STAGE/EV/'source-manifest.json').read_text());rows={r['id']:r for r in sm['sources']}
    assert {r['id']for r in rows.values()if r['role']=='primary'}==set(IDS)
    assert sm['primary_bytes']==22313 and sm['runtime_dependency_bytes']==377167
    for sid,r in rows.items():
        raw=(STAGE/r['saved_path']).read_bytes()
        assert len(raw)==inv[sid]['size']and sha(raw)==inv[sid]['sha256']
        assert len(r['sources'])==2 and all(loc['bytes_verified']for loc in r['sources'])
    executions=[]
    for kind,rid,cid,dep in [('audit',IDS[2],IDS[1],'8d74fd183eba467a811f'),('probe',IDS[4],IDS[3],'74e42e785c0da1cb0ee5')]:
        folder=EV/('replay-'+kind);event=json.loads((STAGE/folder/'execution.json').read_text())
        assert event['status']=='finished'and event['original_entrypoint_executions']==1 and event['exit_code']==0
        assert event['generated_report_byte_identical_to_frozen']and event['code_and_inputs_unchanged']
        raw=(STAGE/folder/Path(rows[rid]['path']).name).read_bytes()
        assert raw==(STAGE/rows[rid]['saved_path']).read_bytes()and sha(raw)==event['generated_report_sha256']
        assert (STAGE/folder/'stderr.txt').read_bytes()==b''
        for sid in [cid,dep]:assert sha((STAGE/EV/'replay-tree'/rows[sid]['path']).read_bytes())==rows[sid]['sha256']
        executions.append(event)
    a=json.loads((STAGE/rows[IDS[2]]['saved_path']).read_text())
    assert (a['players'],a['unit_customers'],a['automaton_nodes'],a['edges'],a['complete_SPE_comparisons'],a['nonself_SPE_comparisons'])==(13,36,27243,112050,112050,93375)
    assert a['minimum_SPE_difference']=='0'and a['zero_columns']==[]and a['stationary_equation_rank_including_normalization']==6
    pi=list(map(F,a['stationary_pi']));tails=a['root_response_tails'];matrix=[list(map(F,row))for row in a['query_by_root_tail_matrix']]
    assert min(pi)>=0 and sum(pi)==1 and all(len(B)==6 and sum(B)==12 and min(B)>=0 for B in tails)
    assert all(sum(pi[i]*F(tails[i][j],12)for i in range(6))==pi[j]for j in range(6))
    values=[sum(x*y for x,y in zip(row,pi))for row in matrix]
    assert values==list(map(F,a['stationary_query_values']))
    assert max(values)==F(a['cap'])==F(427,156)and values.index(max(values))==2
    assert F(a['weak_threshold'])==F(2*a['W'],25)==F(66,25)
    assert F(a['cap'])-F(a['weak_threshold'])==F(a['weak_gap'])==F(379,3900)
    q=list(map(F,a['alternate_root_menu_probabilities']));p=list(map(F,a['root_menu_optimal_query']))
    assert min(q)>=0 and min(p)>=0 and sum(q)==sum(p)==1
    alt=[sum(x*y for x,y in zip(row,q))for row in matrix]
    assert alt==list(map(F,a['alternate_root_menu_query_values']))
    assert max(alt)==F(29,12)<F(a['strong_threshold'])==F(33,13)
    lower=[sum(p[i]*matrix[i][j]for i in range(6))for j in range(6)]
    assert lower==[F(29,12)]*6==list(map(F,a['root_menu_query_values_by_background']))
    assert max(map(F,a['unrestricted_static_query_values']))==F(a['true_security_upper_bound'])==F(5,2)
    probe=json.loads((STAGE/rows[IDS[4]]['saved_path']).read_text())
    assert probe['query']==5 and probe['scale']==13237 and len(probe['customers'])==21
    assert len({r['mask']for r in probe['customers']})==21 and all(0<r['mask']<64 and r['multiplicity']>0 for r in probe['customers'])
    assert sum(r['multiplicity']for r in probe['customers'])==probe['scale']
    vals=list(map(F,probe['query_values']))
    assert max(vals)==vals[5]==3024 and F(probe['W'])==8180
    assert (F(5,2)*max(vals)-F(probe['W']))/probe['scale']==F(probe['normalized_weak_gap'])==F(-20,427)
    certificate=json.loads((STAGE/rows['74e42e785c0da1cb0ee5']['saved_path']).read_text())
    assert probe['actions']==certificate['strategy']['actions']and len(probe['actions'])==43
    review=json.loads((STAGE/rows['cc31f0e547a5bce7512e']['saved_path']).read_text())
    assert review['root_tail_counts']==tails and review['stationary_probability']==a['stationary_pi']
    assert review['checked_true_deviations']==93375 and review['augmented_rank']==6
    assert review['cap']==a['cap']and review['exact_weak_violation']==a['weak_gap']
    assert review['source_sha256']==rows['8d74fd183eba467a811f']['sha256']
    current=[]
    for path in CURRENT_FULL+CURRENT_SCOPE:
        raw=(REPO/path).read_bytes()
        current.append(dict(path=path,size=len(raw),sha256=sha(raw),read_scope='full-text'if path in CURRENT_FULL else'model-and-status-passages'))
    dump(EV/'current-comparison-manifest.json',dict(scope='Current related object content snapshots; GB before/after correction evidence is separately frozen in the workspace.',objects=current))
    gb=json.loads((STAGE/WS/'gb-sign-correction/verification.json').read_text())
    assert gb['all_checks_passed']and gb['certificates']==13 and gb['exact_coordinate_residuals']==4914
    assert len(gb['saved_five_budget_policies'])==5 and all(F(r['achieved_C_minus_W'])<0 for r in gb['saved_five_budget_policies'])
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
    for r in receipts:
        assert all(r[k]for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note'])
        assert r['disposition']=='integrated'
        for target in r['targets']:assert(STAGE/target).exists()or(REPO/target).exists()
    result=dict(kind='record-and-frozen-byte-check-no-original-run',all_checks_passed=True,formal_objects=len(formal),primary_receipts=len(receipts),local_links=len(links),links=links,original_audit_main_executions=1,original_probe_main_executions=1,original_probe_internal_LP_calls=6,root_review_main_executions_this_batch=0,comparison_sources_not_done=4,extra_GB_correction_is_separate=True,scope='Only unique prescribed root stationary weak cap is refuted; arbitrary root-menu value is 29/12, negative three-player recovered point has no exact cone upper certificate. No half/general-security refutation.')
    dump(EV/'verification.json',result);print(json.dumps({k:result[k]for k in ['all_checks_passed','formal_objects','primary_receipts','local_links','original_audit_main_executions','original_probe_main_executions']},ensure_ascii=False))
if __name__=='__main__':main()
