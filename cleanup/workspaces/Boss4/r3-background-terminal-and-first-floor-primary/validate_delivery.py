"""Read saved evidence only; do not repeat any original or supplementary audit."""
from pathlib import Path
import json,hashlib,re,os
S=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-background-terminal-and-first-floor-primary')
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
E=Path('archives/customer-attraction/tools/evidence/background-terminal-first-floor-primary')
W=Path('cleanup/workspaces/Boss4/r3-background-terminal-and-first-floor-primary')
IDS={'791c11050bd539113e7b','62965fc71b6de6e370d6','9c939c75abe0238b894f','f44e0b68b125e6689ed2','54a842cb6b974fca2c33'}
def read(p):return json.loads((S/p).read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    pm=read(E/'primary-manifest.json');sm=read(E/'source-manifest.json');claim=read(W/'claim-receipt.json');obs=read(W/'claim-observation.json');receipts=read(W/'semantic-receipts.json')
    assert claim['status']=='pushed'and claim['actor']=='Boss4'and IDS<=set(claim['ids'])
    assert claim['remote_tip']==obs['remote_tip']==sm['claim_push']=='406e4f57100ac0a6d8fb9733f4781451337e5f9f'
    assert obs['capture_sha256']==sha((S/W/'claim-receipt.json').read_bytes())
    assert len(pm['sources'])==len(receipts)==5 and {r['id']for r in pm['sources']}==IDS=={r['id']for r in receipts}
    assert sum(r['size']for r in pm['sources'])==47644 and len(sm['sources'])==6
    assert sm['runtime_input_files']==sm['runtime_local_import_files']==0
    for row in sm['sources']:
        raw=(S/row['saved_path']).read_bytes();assert len(raw)==row['size']and sha(raw)==row['sha256']
        assert len(row['sources'])==2 and all(l['bytes_verified']for l in row['sources'])
    for row in receipts:
        assert row['disposition']=='integrated'and all(row[k]for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
        assert all((S/t).is_file()for t in row['targets'])
    byid={r['id']:r for r in sm['sources']};runs=[]
    for kind,cid,rid in [('terminal','791c11050bd539113e7b','62965fc71b6de6e370d6'),('probe','9c939c75abe0238b894f',None),('walk','f44e0b68b125e6689ed2','54a842cb6b974fca2c33')]:
        x=read(E/f'replay-{kind}/execution.json');assert x['status']=='finished'and x['exit_code']==0 and x['original_main_executions']==1 and x['code_bytes_unchanged']
        assert sha((S/E/'replay-tree'/byid[cid]['path']).read_bytes())==byid[cid]['sha256']
        assert (S/E/f'replay-{kind}/stderr.txt').read_bytes()==b''
        if rid:
            raw=(S/E/f'replay-{kind}'/Path(byid[rid]['path']).name).read_bytes();assert raw==(S/byid[rid]['saved_path']).read_bytes()and sha(raw)==x['report_sha256']and x['report_byte_identical_to_frozen']
        if kind=='walk':assert x['LP_calls_if_default_loop_completed']==100 and b'DONE 5 7 8.0'in(S/E/'replay-walk/stdout.txt').read_bytes()
        if kind=='probe':assert b'4.205623901581722'in(S/E/'replay-probe/stdout.txt').read_bytes()
        runs.append(dict(kind=kind,original_main_executions=1,seconds=x['wall_seconds'],exit_code=0,report_sha256=x.get('report_sha256')))
    terminal=read(E/'replay-terminal/global_terminal_layers_audit.json')['reports'];assert[(r['k'],r['m'])for r in terminal]==[(1,6),(2,9)]
    assert [(r['W'],r['OPT_m'],r['OPT_minus_2W'])for r in terminal]==[(7,15,1),(13,31,5)]
    assert [r['tail_ordered_action_comparisons_represented']for r in terminal]==[117649,1100000000]
    exact=read(E/'frozen-first-floor-exact-audit.json')
    assert exact['source_sha256']==byid['54a842cb6b974fca2c33']['sha256']
    assert exact['stored_count_state_action_entries']==330 and exact['ordered_decision_histories']==2801
    assert exact['ordered_action_comparisons_including_self']==19607 and exact['ordered_nonself_comparisons']==16806 and exact['count_action_comparisons_including_self']==2310
    assert exact['labels_merged']is False and exact['equal_coverage_label_classes']==[[0,1,3,4],[2],[5],[6]]
    assert exact['actual_path']==[3,3,3,1,1]and exact['actual_payoffs']==['1']*5 and exact['W']=='5'and exact['OPT_m']=='8'and exact['root_opt_ratio']=='8'
    assert exact['optimal_multisets_checked']==462 and exact['minimum_exact_IC_slack']=='0'and exact['original_discovery_main_executions']==exact['scipy_calls']==0
    assert [x['count_states']for x in exact['layers']]==[1,7,28,84,210]and [x['ordered_decision_histories']for x in exact['layers']]==[1,7,49,343,2401]
    pages=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(pages)==2;links=0
    for p in pages:
        t=p.read_text();assert all(k+':'in t for k in ['id','kind','type_tag','title','status','summary','source_refs'])
        for link in re.findall(r'\]\(([^)]+)\)',t):
            if '://'in link or link.startswith('#'):continue
            dest=Path(os.path.normpath(str(p.parent.relative_to(S)/link.split('#')[0])))
            assert (S/dest).is_file()or(R/dest).is_file(),(p,link)
            links+=1
    return dict(status='pass',primary_sources=5,primary_bytes=47644,comparison_only_sources=1,originals_hashed=6,primary_receipts=5,formal_bodies=2,formal_links_resolved=links,original_main_executions=3,original_runs=runs,floating_discovery_LP_calls=156,frozen_policy_count_state_entries=330,frozen_policy_ordered_decision_histories=2801,frozen_policy_ordered_comparisons=19607,frozen_policy_nonself_comparisons=16806,scope='Read-only transmission/structure validation. No original or supplementary main rerun; exact saved-input certification and global analytic arguments remain separate from discovery scans. No label merging, universal first-player guarantee, or HALF counterexample is certified.')
if __name__=='__main__':
    d=main();(S/W/'validation.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(json.dumps(d,ensure_ascii=False,indent=2))
