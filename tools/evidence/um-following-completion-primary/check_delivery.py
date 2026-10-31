#!/usr/bin/env python3
"""Structural record/hash checks, never executes any mathematical entry."""
from pathlib import Path
import json,hashlib,re,sys,difflib
S=Path(__file__).resolve().parents[3];R=S.parents[1]/'boss4-research'
E=Path('tools/evidence/um-following-completion-primary');W=Path('cleanup/workspaces/Boss4/r3-um-following-completion-primary')
M=W/'copy-files.json';V=E/'validation.json'
def read(p):return json.loads((S/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def validate(manifest=True):
    sources=read(E/'source-manifest.json');ids={s['id'] for s in sources}
    assert ids=={'17bd2d415c11d5953378','7e9a28847d18f65c3e1a','9ca39b22ace6bb8649be','e206d008d16b3d8734bf','eec3fb2bff408d1f3a48'}
    c=read(E/'actual-claim.json');assert c['status']=='pushed' and c['actor']=='Boss4' and c['operation']=='claim'
    assert c['local_sync']['status']=='synced' and set(c['ids'])==ids and c['remote_tip']=='04312516fb9129c893537083d13b4e5a21162937'
    cov=read(E/'primary-read-coverage.json')
    for x in sources:
        p=S/x['preserved_path'];assert sha(p)==x['sha256'] and p.stat().st_size==x['size'] and len(p.read_text().splitlines())==x['lines']
        assert x['actual_full_read_after_pushed_claim'] and x['preparation_not_substituted_for_primary'] and x['unique_units_accounted_for']
        ranges=sorted((a['first_line'],a['last_line']) for a in cov if a['id']==x['id'])
        assert ranges[0][0]==1 and ranges[-1][1]==x['lines'] and all(a[1]+1==b[0] for a,b in zip(ranges,ranges[1:]))
    assert sum(x['size'] for x in sources)==59278 and sum(x['lines'] for x in sources)==1404 and len(cov)==7
    assert all(x['actual_text_displayed'] for x in cov)
    layout=read(E/'formal-layout.json');assert len(layout)==4 and len({x['id'] for x in layout})==4
    links=0
    for x in layout:
        p=S/x['path'];t=p.read_text();assert t.startswith('---\n')
        h={k:json.loads(v) for k,v in (a.split(': ',1) for a in t.split('\n---\n',1)[0][4:].splitlines())}
        assert h['id']==x['id'] and h['kind']=='resource' and h['type_tag']=='资源' and h['source_ids']==x['primary_ids']
        assert all(h[k] for k in ['title','summary','status','source_refs'])
        for a in re.findall(r'\]\(([^)]+)\)',t):
            a=a.split('#',1)[0]
            if not a or '://' in a:continue
            q=(p.parent/a).resolve();rel=q.relative_to(S);assert q.exists() or (R/rel).exists(),(x['path'],a);links+=1
        for old in (R/'archives/unrelated-machines/state').rglob('*.md'):
            if old.relative_to(R).as_posix()==x['path']:continue
            assert not re.search(r'^id:\s*["\']?'+re.escape(x['id'])+r'["\']?\s*$',old.read_text().split('\n---\n',1)[0],re.M)
    receipts=read(W/'semantic-receipts.json');assert {x['id'] for x in receipts}==ids
    for x in receipts:
        assert all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
        assert all(x[k] for k in ['read_note','comparison_note','decision_note']) and x['disposition']=='integrated'
        assert x['targets']==[p['path'] for p in layout if x['id'] in p['primary_ids']]
    support=read(E/'support-manifest.json');assert len(support)==4 and ids.isdisjoint({x['id'] for x in support})
    for x in support:
        p=S/x['snapshot'];assert sha(p)==x['inventory']['sha256'] and p.stat().st_size==x['inventory']['size'] and len(p.read_text().splitlines())==x['lines']
        assert x['extra_receipt'] is False
    ss={x['id']:x for x in support};assert ss['8c90fcce237d7988a7a5']['actual_read_ranges']==[[1,107],[246,322]]
    assert ss['7d8533e6d4a2dfeb379d']['prior_full_read_reused'] is True and ss['7d8533e6d4a2dfeb379d']['actual_read_ranges']==[[1,156]]
    comp=read(E/'comparison-manifest.json');assert len(comp)==7
    for x in comp:assert sha(S/x['snapshot'])==x['sha256'] and x['actual_read'].startswith('full') and not x['new_primary'] and not x['receipt']
    exe=read(E/'execution-and-scope.json');assert exe['new_original_entry_runs']==5 and exe['dependency_old_bridge_main_runs']==0 and exe['extra_diagnostic_runs']==0
    assert exe['all_reports_every_field_actually_read'] and exe['normative_bridge_records_full_fields_read']==35
    for x in exe['entries']:
        folder=S/E/'runs'/x['source_id'];assert x['entry_runs']==1 and x['returncode']==0 and x['cwd_initially_empty'] and x['inputs_unchanged_after_run']
        assert sha(folder/'stdout.txt')==x['stdout_sha256'] and sha(folder/'stderr.txt')==x['stderr_sha256'] and (folder/'stderr.txt').read_text()==''
        for a in x['input_aliases']:assert sha(folder/'input-tree'/a['relative_path'])==a['sha256']
    norm=read(E/'runs/7e9a28847d18f65c3e1a/report.json');ind=read(E/'runs/9ca39b22ace6bb8649be/report.json');star=read(E/'runs/eec3fb2bff408d1f3a48/report.json');long=read(E/'runs/e206d008d16b3d8734bf/report.json');mat=read(E/'runs/17bd2d415c11d5953378/report.json')
    assert norm['exhaustive_bundle_instances']==4056 and norm['color_runs']==11832 and norm['strict_improving_moves']==12186
    assert len(norm['token_bridge']['records'])==35 and norm['token_bridge']['below_two_decoded']==16 and norm['token_bridge']['alpha_zero_cases']==19
    assert ind['cases']==2800 and len(ind['benchmarks'])==40 and ind['resource_parent_assignments']==88586
    assert star['star_gap_k2_independent_full_enumeration']['assignments_checked']==82944 and star['nested_contraction_audit']['fully_lifted_schedules']==89712
    assert sum(x['independent_oracle']['orientations'] for x in long['instances'] if 'independent_oracle' in x)==541184
    assert mat['parameter_cases']==16 and mat['fundamental_circuit_cases']==2674 and mat['explicit_circuit_witness_checks']==109351
    er=E/'errata-finite-scope';err=read(er/'errata-manifest.json');assert err['target_files']==2 and err['exact_replacements']==3 and err['new_extra_diagnostic_runs']==0
    for x in err['targets']:
        before=(S/er/(x['key']+'-before.md')).read_text();after=(S/er/(x['key']+'-proposed.md')).read_text();current=before
        assert sha(S/er/(x['key']+'-before.md'))==x['before_sha256'] and sha(S/er/(x['key']+'-proposed.md'))==x['proposed_sha256']
        for a in x['replacements']:
            assert current.count(a['exact_before'])==1 and before[:before.index(a['exact_before'])].count('\n')+1==a['before_lines'][0]
            current=current.replace(a['exact_before'],a['exact_after'])
        assert current==after and not (S/x['target_path']).exists()
        assert ''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='a/'+x['target_path'],tofile='b/'+x['target_path']))==(S/er/(x['key']+'.patch')).read_text()
    rel=read(W/'relations.json')['relations'];assert len(rel)==13 and all(x['common_premises'] and x['evidence'] and x['gap'] and x['phase3_graph_written'] is False for x in rel)
    obs=read(E/'local-progress-observation.json');assert {x['id'] for x in obs['initial_primary_owner_verification']}==ids
    assert all(x['owner']=='Boss4' and x['request_id']=='8663e010a41e41a699fc6a28436c64e9' for x in obs['initial_primary_owner_verification']) and obs['no_local_absence_reinterpreted_as_available']
    nxt=read(W/'next-candidates.json')['candidates'];assert len(nxt)==5 and ids.isdisjoint({x['id'] for x in nxt})
    assert all(not x['local_progress_observed'].get('owner') and x['not_claimed_by_this_package'] and x['known_pushed_claims_checked_and_excluded'] for x in nxt)
    log=read(E/'reading-log.json');assert log['entry_runs_completed']==5 and log['running_sessions']=={} and log['report_full_fields_read']
    for p in S.rglob('*.json'):json.loads(p.read_text())
    paths={p.relative_to(S).as_posix() for p in S.rglob('*') if p.is_file()}|{M.as_posix(),V.as_posix()}
    if manifest:
        m=read(M);assert m['ready'] is True and set(m['copy_paths'])==paths and len(m['copy_paths'])==len(paths) and set(m['files'])==paths-{M.as_posix()}
        for p,a in m['files'].items():assert sha(S/p)==a['sha256'] and (S/p).stat().st_size==a['bytes'],p
    return {'status':'all structural and byte checks passed','primary_sources':5,'primary_bytes':59278,'primary_full_actual_lines':1404,'actual_display_ranges':7,'formal_pages':4,'formal_lines':sum(x['lines'] for x in layout),'formal_links_checked':links,'receipts':5,'support_sources':4,'support_current_full_read_lines':303,'support_prior_sameSHA_full_read_lines_reused':156,'support_current_selected_read_lines':184,'formal_comparisons':7,'comparison_full_actual_lines':sum(x['lines'] for x in comp),'relations_evidence':13,'new_original_main_entries':5,'old_dependency_main_entries':0,'extra_diagnostics':0,'errata_target_pages':2,'errata_replacements':3,'local_progress_discrepancy_preserved_and_Root_notified':True,'exact_copy_files':len(paths),'verification_limit':'Record/hash checks and finite reports do not prove general mathematics, historical independence, external review or novelty.'}
if __name__=='__main__':
    prepare='--prepare-validation' in sys.argv;r=validate(not prepare);text=json.dumps(r,ensure_ascii=False,indent=2)+'\n'
    if prepare:(S/V).write_text(text)
    else:assert (S/V).read_text()==text
    print(json.dumps({'mode':'prepare-only-not-READY' if prepare else 'final-manifest-verified',**r},ensure_ascii=False))
