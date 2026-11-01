#!/usr/bin/env python3
"""Local record/byte checks only; no Git/network/source loading or math rerun."""
from pathlib import Path
import json,hashlib,re,sys
S=Path(__file__).resolve().parents[3];R=S.parents[1]/'boss4-research'
E=Path('tools/evidence/r174-workspace-and-bridge-primary');W=Path('cleanup/workspaces/Boss4/r3-174-workspace-and-bridge-primary');M=W/'copy-files.json';V=E/'validation.json'
def read(p):return json.loads((S/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def validate(manifest=True):
    primary=read(E/'source-manifest.json');support=read(E/'support-manifest.json');ids={x['id'] for x in primary};foreign={x['id'] for x in support}
    assert ids=={'55534811e2b0fc724132','03fe28a4a550c647aa0a','0abe71e0f3a6d2e380b7'}
    assert foreign=={'a03e39c3ec6ec4a9319b','b243bc081ceffd6be46b','b81e4d0d48f6fad07a88'} and ids.isdisjoint(foreign)
    c=read(E/'actual-claim.json');assert c['status']=='pushed' and c['operation']=='claim' and c['actor']=='Boss4' and c['local_sync']['status']=='synced'
    assert c['remote_tip']=='5a8e6e6069abd3fcefd8086a69f5a27eb61da8e2' and len(c['ids'])==24 and ids<=set(c['ids']) and foreign.isdisjoint(c['ids'])
    cached=read(E/'local-inputs-original-manifest.json');assert 'pure local' in cached['method'] and {x['id'] for x in cached['rows'] if x['group']=='facility_cs'}==ids|foreign
    cov=read(E/'primary-read-coverage.json');assert len(cov)==3
    for x in primary+support:
        p=S/x['preserved_path'];data=p.read_bytes();assert len(data)==x['size'] and sha(p)==x['sha256'] and len(p.read_text().splitlines())==x['lines']
        assert hashlib.sha1(data).hexdigest()==x['raw_content_sha1'] and hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==x['blob'] and x['local_blob_sha1_verified']
        assert x['actual_read_ranges']==[[1,x['lines']]] and x['actual_read'].startswith('full')
        assert x['owner_actual']['owner']==('Boss4' if x['id'] in ids else 'Boss6')
        if x['id'] in ids:
            assert x['actual_full_read_after_pushed_claim'] and x['unique_units_accounted_for']
            assert [(a['first_line'],a['last_line']) for a in cov if a['id']==x['id']]==[(1,x['lines'])]
        else:assert x['extra_receipt'] is False
    assert sum(x['size'] for x in primary)==9366 and sum(x['lines'] for x in primary)==154
    assert sum(x['size'] for x in support)==10865 and sum(x['lines'] for x in support)==187 and all(x['actual_text_displayed'] for x in cov)
    layout=read(E/'formal-layout.json');assert len(layout)==4 and len({x['id'] for x in layout})==4
    assert sorted(x['kind'] for x in layout)==['counterexample','resource','resource','resource'];links=0
    for x in layout:
        p=S/x['path'];t=p.read_text();assert t.startswith('---\n')
        h={k:json.loads(v) for k,v in (a.split(': ',1) for a in t.split('\n---\n',1)[0][4:].splitlines())}
        assert h['id']==x['id'] and h['kind']==x['kind'] and h['source_ids']==x['primary_ids']
        assert all(h[k] for k in ['type_tag','title','status','summary','source_refs'])
        for target in re.findall(r'\]\(([^)]+)\)',t):
            a=target.split('#',1)[0]
            if not a or '://' in a:continue
            q=(p.parent/a).resolve();rel=q.relative_to(S);assert q.exists() or (R/rel).exists(),(x['path'],target);links+=1
        for old in (R/'archives/customer-attraction/state').rglob('*.md'):
            if old.relative_to(R).as_posix()==x['path']:continue
            assert not re.search(r'^id:\s*["\']?'+re.escape(x['id'])+r'["\']?\s*$',old.read_text().split('\n---\n',1)[0],re.M)
    receipts=read(W/'semantic-receipts.json');assert {x['id'] for x in receipts}==ids
    for x in receipts:
        assert all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and x['disposition']=='integrated'
        assert all(x[k] for k in ['read_note','comparison_note','decision_note']) and x['targets']==[p['path'] for p in layout if x['id'] in p['primary_ids']]
    comps=read(E/'comparison-manifest.json');assert len(comps)==9
    for x in comps:assert sha(S/x['snapshot'])==x['sha256'] and x['actual_full_read'] and not x['new_primary_receipt']
    exe=read(E/'run-exact-selfcheck/execution.json');report=read(E/'run-exact-selfcheck/report.json')
    assert exe['returncode']==0 and exe['new_exact_selfcheck_runs']==1 and exe['original_source_program_entries']==0 and exe['cwd_initially_empty'] and exe['network_calls']==0
    assert exe['script_sha256']==sha(S/E/'check-threshold-and-static-bridge.py') and exe['stdout_sha256']==sha(S/E/'run-exact-selfcheck/stdout.txt') and exe['stderr_sha256']==sha(S/E/'run-exact-selfcheck/stderr.txt')
    assert (S/E/'run-exact-selfcheck/stderr.txt').read_text()=='' and report['status']=='passed'
    a=report['selected_branch_lower_envelope_counterexample'];assert a['L']=={'A':'1','B':'3/2','C':'3/2'} and a['theta']=='3/2' and a['actual_payoffs']==['2','2']
    assert a['complete_strategy_maps_enumerated']==81 and a['complete_strategy_maps_spe']==5 and a['root_outcomes_from_full_policy_enum']==a['root_outcomes_from_threshold_recursion'] and a['half_counterexample'] is False
    a=report['static_nonPNE_three_player_certificate'];assert a['nodes']==13 and a['comparisons_including_stay']==39 and a['nontrivial_alternatives']==26
    assert a['static_player2_deviation_payoff']=='4/3' and a['true_player2_deviation_payoff']=='5/6' and a['half_counterexample'] is False
    assert report['smoothness_extra_budget_scalar_limit']['actual_CAG_SPE_counterexample_claimed'] is False
    scope=read(E/'execution-and-scope.json');assert scope['two_player_branch_payoff_table_entries']==972 and scope['counter_field_qualification'] and scope['original_source_program_entries']==0 and scope['report_every_field_actually_read']
    corrections=read(E/'source-corrections.json');assert len(corrections['items'])==2 and corrections['no_source_or_progress_edits'] and corrections['no_foreign_owner_done']
    assert not corrections['shared_old_page_patch_needed'] and corrections['items'][0]['source_id']=='0abe71e0f3a6d2e380b7'
    source=S/next(x['preserved_path'] for x in primary if x['id']=='0abe71e0f3a6d2e380b7');item=corrections['items'][0]
    assert sha(source)==item['source_sha256'] and source.read_text().splitlines()[item['original_line_number']-1]==item['exact_original_line']
    rel=read(W/'relations.json')['relations'];assert len(rel)==12 and all(x['common_premises'] and x['evidence'] and x['gap'] and x['phase3_graph_written'] is False for x in rel)
    nxt=read(W/'next-candidates.json')['candidates'];assert len(nxt)==5 and (ids|foreign).isdisjoint({x['id'] for x in nxt})
    assert all(not x['local_progress_observed'].get('owner') and x['not_claimed_by_this_package'] and x['known_actual_claims_and_Boss6_sources_excluded'] for x in nxt)
    log=read(E/'reading-log.json');assert log['running_sessions']=={} and not log['network_or_clean_show_or_lazy_fetch']
    for p in S.rglob('*.json'):json.loads(p.read_text())
    paths={p.relative_to(S).as_posix() for p in S.rglob('*') if p.is_file()}|{M.as_posix(),V.as_posix()}
    if manifest:
        m=read(M);assert m['ready'] is True and set(m['copy_paths'])==paths and len(m['copy_paths'])==len(paths) and set(m['files'])==paths-{M.as_posix()}
        for path,a in m['files'].items():assert sha(S/path)==a['sha256'] and (S/path).stat().st_size==a['bytes'],path
    return {'status':'all structural and byte checks passed','actual_claim_sources':24,'primary_sources':3,'primary_full_actual_bytes':9366,'primary_full_actual_lines':154,'primary_actual_display_ranges':3,'Boss6_comparison_only_sources':3,'Boss6_comparison_actual_bytes':10865,'Boss6_comparison_actual_lines':187,'Boss6_new_receipts':0,'formal_pages':4,'formal_lines':sum(x['lines'] for x in layout),'formal_links_checked':links,'semantic_receipts':3,'formal_comparisons':9,'formal_comparison_actual_lines':sum(x['lines'] for x in comps),'relations_evidence':12,'new_exact_selfcheck_runs':1,'original_source_program_entries':0,'source_corrections':2,'old_shared_patch_targets':0,'network_clean_show_lazy_fetch_calls':0,'exact_copy_files':len(paths),'verification_limit':'Record/hash checks and finite selfchecks do not certify universal half, external independence or novelty.'}
if __name__=='__main__':
    prepare='--prepare-validation' in sys.argv;r=validate(not prepare);t=json.dumps(r,ensure_ascii=False,indent=2)+'\n'
    if prepare:(S/V).write_text(t)
    else:assert (S/V).read_text()==t
    print(json.dumps({'mode':'prepare-only-not-READY' if prepare else 'final-manifest-verified',**r},ensure_ascii=False))
