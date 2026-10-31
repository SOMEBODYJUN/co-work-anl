"""Read saved evidence only; no original or independent mathematics rerun."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,re,os
S=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-true-spe-outcome-witness-primary')
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
E=Path('archives/customer-attraction/tools/evidence/true-spe-outcome-witness-primary')
W=Path('cleanup/workspaces/Boss4/r3-true-spe-outcome-witness-primary')
IDS={'3280297283b964029c8d','8c7a0f8291365ec3226d','ba24829ca8aa642f892c','962b57c6915dcb2636ca','7e9c940cf8071349841b'}
def read(p):return json.loads((S/p).read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    pm=read(E/'primary-manifest.json');sm=read(E/'source-manifest.json');claim=read(W/'claim-receipt.json');obs=read(W/'claim-observation.json');receipts=read(W/'semantic-receipts.json')
    assert claim['status']=='pushed'and claim['actor']=='Boss4'and IDS<=set(claim['ids'])and obs['local_sync_status']=='synced'
    assert claim['remote_tip']==obs['remote_tip']==sm['claim_push']=='372a7d401e044cd87f4457e55b6ae7e79704565a'
    assert obs['capture_sha256']==sha((S/W/'claim-receipt.json').read_bytes())
    assert len(pm['sources'])==len(receipts)==5 and {r['id']for r in pm['sources']}==IDS=={r['id']for r in receipts}
    assert sum(r['size']for r in pm['sources'])==27378 and len(sm['sources'])==17 and len({r['id']for r in sm['sources']})==17
    assert sum(r['size']for r in sm['sources'])==305742
    for row in sm['sources']:
        raw=(S/row['saved_path']).read_bytes();assert len(raw)==row['size']and sha(raw)==row['sha256']
        assert len(row['sources'])==2 and all(s['bytes_verified']for s in row['sources'])
    for r in receipts:
        assert r['disposition']=='integrated'and all(r[k]for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
        assert all((S/t).is_file()for t in r['targets'])
    byid={r['id']:r for r in sm['sources']};runs=[]
    for kind,cid,rid in [('audit','962b57c6915dcb2636ca','7e9c940cf8071349841b'),('markov','6543d29d729f96c9276b','1c15c43ca580c43498d7')]:
        e=read(E/f'replay-{kind}/execution.json');assert e['status']=='finished'and e['exit_code']==0 and e['original_main_executions']==1 and e['code_and_input_bytes_unchanged']
        raw=(S/E/f'replay-{kind}'/Path(byid[rid]['path']).name).read_bytes();assert raw==(S/byid[rid]['saved_path']).read_bytes()and sha(raw)==e['report_sha256']and e['report_byte_identical_to_frozen']
        assert (S/E/f'replay-{kind}/stderr.txt').read_bytes()==b'' and e['large_baseline_branch_executed']is False
        runs.append(dict(kind=kind,original_main_executions=1,seconds=e['wall_seconds'],report_bytes=len(raw),report_sha256=sha(raw)))
    audit=read(E/'replay-audit/outcome_dag_audit.json')
    assert audit['fixed_input_positive_welfare_target_checks']==57 and audit['successful_full_history_exact_checks']==31
    assert audit['exact_fixed_m4_cone_new_budget_optimal_duals']==4 and len(audit['combinatorial_size_formula_checks'])==30
    assert audit['known_nonmarkov_root_023_accepted_and_exactly_verified']and audit['same_count_different_action_observed']
    assert [x['exact_ratio']for x in audit['known_sharp_two_topic_regressions']]==['3/2','4/3']
    markov=read(E/'replay-markov/markov_obstruction_report.json')
    assert markov['Markov_last_maps_exhausted']==len(markov['Markov_last_map_results'])==648 and markov['Markov_second_maps_exhausted']==130776
    assert markov['complete_SPE_comparisons']==155 and len(markov['full_policy'])==31
    assert sum(markov['legal_types'])==markov['total_unit_customers']==24831 and min(markov['legal_types'])>0
    assert markov['full_min_welfare']==22428 and markov['Markov_min_welfare']==22429 and markov['OPT']==22431
    assert '023'in markov['all_full_SPE_root_sets']and '023'not in markov['all_count_Markov_SPE_root_sets']
    independent=read(E/'independent-input-review.json');assert independent['status']=='pass'and independent['solver_calls']==0
    assert independent['fixed_m4_nonzero_distinct_IC_rows']==82 and [p['value']for p in independent['fixed_m4_exact_proofs']]==['7/4','7/4','655/364','2711/1547']
    assert all(F(x['min_dual_coordinate_residual'])>=0 for x in independent['fixed_m4_exact_proofs'])and F(independent['old13_exact_budget_excess'])>0
    correction=read(W/'corrections/correction-metadata.json');proposed=(S/W/'corrections/count-policy-purification-replacement.md').read_bytes();assert sha(proposed)==correction['proposed_sha256']and correction['shared_file_modified']is False
    current=sha((R/correction['target']).read_bytes());correction_state='base-still-matches'if current==correction['base_sha256']else'already-matches-proposal'if current==correction['proposed_sha256']else'changed-in-parallel-root-review-needed'
    pages=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(pages)==3;links=0
    for p in pages:
        t=p.read_text();assert all(k+':'in t for k in ['id','kind','type_tag','title','status','summary','source_refs'])
        for link in re.findall(r'\]\(([^)]+)\)',t):
            if '://'in link or link.startswith('#'):continue
            dest=Path(os.path.normpath(str(p.parent.relative_to(S)/link.split('#')[0])))
            assert (S/dest).is_file()or(R/dest).is_file(),(p,link);links+=1
    return dict(status='pass',primary_sources=5,primary_bytes=27378,original_sources_hashed=17,original_bytes=305742,primary_receipts=5,formal_objects=3,formal_links_resolved=links,primary_original_audit_runs=1,comparison_original_std_audit_runs=1,new_original_MILP_calls=60,new_fixed_cone_LPs=2,new_fixed_budget_duals_replayed=4,original_executions=runs,Markov_exhaustive_last_maps=648,Markov_exhaustive_second_maps=130776,correction_target=correction['target'],correction_current_state=correction_state,shared_correction_applied_by_this_agent=False,scope='Read-only hashes/structure/delivery verification; no original/independent audit rerun. Exact counterexample rejects count-policy purification, not HALF; universal tax bridge false, fixed-cone bounds and DAG equivalence retain their scopes.')
if __name__=='__main__':
    d=main();(S/W/'validation.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(json.dumps(d,ensure_ascii=False,indent=2))
