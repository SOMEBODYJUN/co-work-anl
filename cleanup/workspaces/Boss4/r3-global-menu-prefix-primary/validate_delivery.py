"""Read existing evidence only; never runs either original main or exact check again."""
from pathlib import Path
import json,hashlib,re,os
S=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-global-menu-prefix-primary')
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
E=Path('archives/customer-attraction/tools/evidence/global-menu-prefix-primary')
W=Path('cleanup/workspaces/Boss4/r3-global-menu-prefix-primary')
IDS={'b512acfa743103100fdd','b1068437e0a3ccccf70e','63b07199c23072ad96d9','1f14d618a7256ce9fdd4','2306bc61d5e35b40eabd'}
def read(p):return json.loads((S/p).read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    pm=read(E/'primary-manifest.json');sm=read(E/'source-manifest.json');cm=read(E/'comparison-manifest.json');claim=read(W/'claim-receipt.json');obs=read(W/'claim-observation.json');receipts=read(W/'semantic-receipts.json')
    assert claim['status']=='pushed'and claim['actor']=='Boss4'and IDS<=set(claim['ids'])
    assert claim['remote_tip']==sm['claim_push']==obs['remote_tip']=='c59d0557ab194d2f8e0cf6563e29b97427609a1e'
    assert obs['capture_sha256']==sha((S/W/'claim-receipt.json').read_bytes())
    assert len(pm['sources'])==5 and {r['id']for r in pm['sources']}==IDS=={r['id']for r in receipts}
    assert len(receipts)==5 and sum(r['size']for r in pm['sources'])==22828
    assert len(cm['sources'])==1 and cm['sources'][0]['id']=='57e2038692b56ff33e54'and cm['sources'][0]['role']=='comparison-only-not-primary'
    assert sm['runtime_input_files']==sm['runtime_local_import_files']==0 and len(sm['sources'])==6
    for row in sm['sources']:
        raw=(S/row['saved_path']).read_bytes();assert len(raw)==row['size']and sha(raw)==row['sha256']
        assert len(row['sources'])==2 and all(loc['bytes_verified']for loc in row['sources'])
    for r in receipts:
        assert r['disposition']=='integrated'and all(r[k]for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
        assert all((S/t).is_file()for t in r['targets'])
    records={r['id']:r for r in sm['sources']};evs=[]
    for kind,cid,rid,expected_calls in [('v1','b1068437e0a3ccccf70e','63b07199c23072ad96d9',16),('v2','1f14d618a7256ce9fdd4','2306bc61d5e35b40eabd',11)]:
        e=read(E/f'replay-{kind}/execution.json');raw=(S/E/f'replay-{kind}'/Path(records[rid]['path']).name).read_bytes();report=json.loads(raw)
        assert e['status']=='finished'and e['exit_code']==0 and e['original_main_executions']==1 and e['code_bytes_unchanged']
        assert e['report_byte_identical_to_frozen']and raw==(S/records[rid]['saved_path']).read_bytes()and sha(raw)==e['report_sha256']
        assert sha((S/E/'replay-tree'/records[cid]['path']).read_bytes())==records[cid]['sha256']
        assert (S/E/f'replay-{kind}/stderr.txt').read_bytes()==b''and e['LP_calls_from_completed_control_flow']==expected_calls
        if kind=='v1':
            assert [r['m']for r in report]==list(range(3,11))and all(not r['success']for r in report)
            assert sum(len(r['active'])for r in report)==59
            for r in report:
                assert r['rows']==6*2**r['m'] and len(r['relaxed_coeff'])==2*(r['m']-2)
                for a in r['active']:assert len(a['type'][0])==r['m']and a['dual']<0
        else:
            assert [r['m']for r in report]==list(range(3,14))and [r['success']for r in report]==[True,True]+[False]*9
            assert [r['worst']for r in report if r['success']]==['0','0']
            assert all(set(r)=={'m','success'}for r in report if not r['success'])
            assert raw==(S/E/'replay-v2/stdout.txt').read_bytes()
        evs.append(dict(kind=kind,original_main_executions=1,LPs=expected_calls,bytes=len(raw),sha256=sha(raw),seconds=e['wall_seconds']))
    exact=read(E/'exact-template-check.json')
    assert exact['status']=='pass'and exact['original_main_executions']==exact['scipy_calls']==0
    assert exact['integer_grid_rows_checked']==528
    assert [r['m']for r in exact['positive_scaled_template_certificates']]==[3,4]
    assert sum(len(r['by_actual_membership'])for r in exact['positive_scaled_template_certificates'])==24
    assert exact['fixed_G_m3_exact_separator']['combined_R_L']==['0','0']and exact['fixed_G_m3_exact_separator']['combined_right_side']=='-1/3'
    links=0;pages=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(pages)==2
    for p in pages:
        text=p.read_text();assert all(k+':'in text for k in ['id','kind','type_tag','title','status','summary','source_refs'])
        for link in re.findall(r'\]\(([^)]+)\)',text):
            if '://'in link or link.startswith('#'):continue
            target=Path(os.path.normpath(str(p.parent.relative_to(S)/link.split('#')[0])))
            assert (S/target).is_file()or(R/target).is_file(),(p,link)
            links+=1
    return dict(status='pass',primary_sources=5,primary_bytes=22828,comparison_only_sources=1,all_originals_hashed=6,primary_receipts=5,formal_bodies=2,formal_links_resolved=links,original_main_executions=2,original_LPs=27,original_reports=evs,exact_check_saved_integer_rows=528,positive_certificate_membership_patterns=24,scope='Read-only transport/structure verification; no original main, LP, or exact_template_check.py rerun. Floating infeasible is not certified mathematically. Self-contained analytic proof and corrected source status remain essential.')
if __name__=='__main__':
    d=main();(S/W/'validation.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(json.dumps(d,ensure_ascii=False,indent=2))
