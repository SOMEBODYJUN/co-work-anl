"""Read existing artifacts only; no original MILP or structure-check rerun."""
from pathlib import Path
import json,hashlib,re,os
S=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-credible-weak-dag-attack-primary')
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
E=Path('archives/customer-attraction/tools/evidence/credible-weak-dag-attack-primary')
W=Path('cleanup/workspaces/Boss4/r3-credible-weak-dag-attack-primary')
IDS={'5253dce62f3159c5d985','82b0bd94aff958b218a8','6a9486c43f41e40329c1','ad1347974e6526bf0c33','3f3746b2117853f1086d'}
def read(p):return json.loads((S/p).read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    pm=read(E/'primary-manifest.json');rm=read(E/'runtime-manifest.json');sm=read(E/'source-manifest.json');claim=read(W/'claim-receipt.json');obs=read(W/'claim-observation.json');receipts=read(W/'semantic-receipts.json')
    assert claim['status']=='pushed'and claim['actor']=='Boss4'and IDS<=set(claim['ids'])
    assert claim['remote_tip']==obs['remote_tip']==sm['claim_push']=='15d5611461fa75b3b7fc657783e87cb40b28fb93'
    assert obs['capture_sha256']==sha((S/W/'claim-receipt.json').read_bytes())
    assert len(pm['sources'])==len(receipts)==5 and {r['id']for r in pm['sources']}==IDS=={r['id']for r in receipts}
    assert sum(r['size']for r in pm['sources'])==5441 and len(rm['sources'])==6 and sum(r['size']for r in rm['sources'])==55820
    assert len(sm['sources'])==11 and sm['runtime_input_files']==0
    byid={r['id']:r for r in sm['sources']}
    for row in sm['sources']:
        raw=(S/row['saved_path']).read_bytes();assert len(raw)==row['size']and sha(raw)==row['sha256']
        assert len(row['sources'])==2 and all(v['bytes_verified']for v in row['sources'])
    for row in receipts:
        assert row['disposition']=='integrated'and all(row[k]for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
        assert all((S/t).is_file()for t in row['targets'])
    frozen=[]
    for sid in ['82b0bd94aff958b218a8','6a9486c43f41e40329c1','ad1347974e6526bf0c33','3f3746b2117853f1086d']:
        d=read(Path(byid[sid]['saved_path']));assert d['exact_candidate']is None and d['universal_bound_proved']is False and d['milp']['floating_value']is None and d['milp']['floating_bound_not_a_certificate']is True;frozen.append(d)
    assert [r['milp']['status']for r in frozen]==[2,2,1,1]
    assert frozen[3]['portfolio']==[1,3,4,5]
    e=read(E/'replay/execution.json');assert e['status']=='finished'and e['exit_code']==0 and e['original_main_executions']==e['milp_calls']==1
    assert e['new_time_limit_seconds']==30 and e['unrerun_other_frozen_cases']==3 and e['source_bytes_unchanged']
    assert e['milp_status']==2 and e['exact_optimize_called']is False and e['exact_candidate_present']is False
    assert e['report_byte_identical_to_frozen']is False and e['report_equal_except_measured_milp_seconds']is True
    assert (S/E/'replay/stderr.txt').read_bytes()==b''
    newraw=(S/E/'replay/weak_dag_m3p5_q111_j234.json').read_bytes();assert sha(newraw)==e['report_sha256']
    old=dict(frozen[0]);new=json.loads(newraw);old['milp']=dict(old['milp']);old['milp'].pop('seconds');new['milp'].pop('seconds');assert old==new
    for row in sm['sources']:
        if row['path'].endswith('.py'):assert sha((S/E/'replay-tree'/row['path']).read_bytes())==row['sha256']
    struct=read(E/'frozen-model-structure-check.json');assert struct['status']=='pass'and struct['solver_calls']==struct['original_main_executions']==0
    assert len(struct['cases'])==4 and [(r['total_variables'],r['binary_variables'],r['total_constraints'])for r in struct['cases']]==[(822,770,1397),(822,770,1397),(1391,1300,2356),(5880,5733,10487)]
    pages=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(pages)==1;links=0
    for p in pages:
        text=p.read_text();assert all(k+':'in text for k in ['id','kind','type_tag','title','status','summary','source_refs'])
        for link in re.findall(r'\]\(([^)]+)\)',text):
            if '://'in link or link.startswith('#'):continue
            dest=Path(os.path.normpath(str(p.parent.relative_to(S)/link.split('#')[0])))
            assert(S/dest).is_file()or(R/dest).is_file(),(p,link);links+=1
    return dict(status='pass',primary_count=5,primary_bytes=5441,runtime_dependencies=6,runtime_bytes=55820,original_sources_hashed=11,primary_receipts=5,formal_bodies=1,formal_links_resolved=links,frozen_reports=4,frozen_statuses=[2,2,1,1],new_original_main_executions=1,new_milp_calls=1,new_milp_status=2,new_wall_seconds=e['wall_seconds'],new_report_sha256=e['report_sha256'],report_equality='Only measured milp.seconds differs; not byte-identical',exact_candidate_branch_executed=False,scope='Read-only delivery/structure checks; no solver, original main, exact recovery or structure-check rerun. No exact infeasibility, universal weak budget, or HALF result is certified.')
if __name__=='__main__':
    d=main();(S/W/'validation.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(json.dumps(d,ensure_ascii=False,indent=2))
