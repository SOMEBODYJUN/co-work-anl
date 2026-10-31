#!/usr/bin/env python3
"""Structural records/bytes only. Does not execute mathematical programs."""
from pathlib import Path
import json,hashlib,re,sys,difflib
ST=Path(__file__).resolve().parents[3]
REPO=ST.parents[1]/'boss4-research'
E=Path('tools/evidence/um-home-unit-transit-and-envelope-primary')
W=Path('cleanup/workspaces/Boss4/r3-um-home-unit-transit-and-envelope-primary')
M=W/'copy-files.json';V=E/'validation.json'
def read(p):return json.loads((ST/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def validate(manifest=True):
    sources=read(E/'source-manifest.json');ids={s['id'] for s in sources}
    assert ids=={'e8b6428338f9c956317c','594190c19816e3b1e99a','e8706876e0c1b5dcebd9','3c16720b6c276a5997e1','10ce30330f34e96a1a00'}
    claim=read(E/'actual-claim.json')
    assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['operation']=='claim'
    assert ids==set(claim['ids']) and claim['local_sync']['status']=='synced'
    assert claim['remote_tip']=='b72e8fe0a4f37eeb6a0e5f9a6f43026b7b3fee53'
    coverage=read(E/'primary-read-coverage.json')
    for s in sources:
        p=ST/s['preserved_path'];assert sha(p)==s['sha256'] and p.stat().st_size==s['size']
        assert len(p.read_text().splitlines())==s['lines'] and s['actual_full_read_after_pushed_claim'] and s['preparation_not_substituted_for_primary']
        assert len(s['unique_units_accounted_for'])>=4
        ranges=sorted((c['first_line'],c['last_line']) for c in coverage if c['id']==s['id'])
        assert ranges[0][0]==1 and ranges[-1][1]==s['lines']
        assert all(x[1]+1==y[0] for x,y in zip(ranges,ranges[1:]))
        assert all(c['actual_text_displayed'] for c in coverage if c['id']==s['id'])
    assert sum(s['size'] for s in sources)==57058 and sum(s['lines'] for s in sources)==1405
    layout=read(E/'formal-layout.json');assert len(layout)==5 and len({x['id'] for x in layout})==5
    assert sorted(x['kind'] for x in layout)==['algorithm','resource','resource','resource','theorem']
    links=0
    for x in layout:
        p=ST/x['path'];text=p.read_text();assert text.startswith('---\n')
        h={k:json.loads(v) for k,v in (a.split(': ',1) for a in text.split('\n---\n',1)[0][4:].splitlines())}
        assert all(h[k] for k in ['id','kind','type_tag','title','status','summary','source_refs'])
        assert h['id']==x['id'] and h['source_ids']==x['primary_ids']
        for target in re.findall(r'\]\(([^)]+)\)',text):
            target=target.split('#',1)[0]
            if not target or '://' in target:continue
            q=(p.parent/target).resolve();rel=q.relative_to(ST)
            assert q.exists() or (REPO/rel).exists(),(x['path'],target)
            links+=1
        for old in (REPO/'archives/unrelated-machines/state').rglob('*.md'):
            if old.relative_to(REPO).as_posix()==x['path']:continue
            assert not re.search(r'^id:\s*["\']?'+re.escape(x['id'])+r'["\']?\s*$',old.read_text().split('\n---\n',1)[0],re.M)
    receipts=read(W/'semantic-receipts.json');assert {x['id'] for x in receipts}==ids
    for x in receipts:
        assert all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
        assert all(x[k] for k in ['read_note','comparison_note','decision_note']) and x['disposition']=='integrated'
        assert x['targets']==[a['path'] for a in layout if x['id'] in a['primary_ids']]
    support=read(E/'support-manifest.json');assert len(support)==5 and len({x['id'] for x in support})==5
    assert ids.isdisjoint({x['id'] for x in support})
    for x in support:
        p=ST/x['snapshot'];assert sha(p)==x['inventory']['sha256'] and p.stat().st_size==x['inventory']['size']
        assert not x['extra_receipt'] and len(p.read_text().splitlines())==x['lines']
    byid={x['id']:x for x in support}
    assert byid['eef751243f82cd1689d6']['actual_read_ranges']==[[1,111]]
    assert byid['ab79c520ba1a75adf3ef']['actual_read_ranges']==[[1,104]]
    for sid in ['d0a31d464c835feda704','cd5e59034198845a9ec2','e0965328b2194975c31c']:
        ranges=byid[sid]['actual_read_ranges'];assert ranges[0][0]==1 and ranges[-1][1]==byid[sid]['lines']
    comps=read(E/'comparison-manifest.json');assert len(comps)==4
    for x in comps:assert sha(ST/x['snapshot'])==x['sha256'] and not x['primary'] and not x['extra_receipt'] and x['actual_read'].startswith('full')
    runscope=read(E/'execution-and-scope.json');assert runscope['new_original_entry_runs_total']==5 and runscope['runtime_dependency_main_runs']==0
    assert runscope['all_reports_every_field_actually_read'] and runscope['independent_transit_explicitly_imports_reviewed']
    assert {x['source_id'] for x in runscope['original_entries']}==ids
    for x in runscope['original_entries']:
        assert x['entry_runs']==1 and x['returncode']==0 and x['cwd_initially_empty'] and x['inputs_unchanged_after_run']
        folder=ST/E/'runs'/x['source_id']
        assert sha(folder/'stdout.txt')==x['stdout_sha256'] and sha(folder/'stderr.txt')==x['stderr_sha256']
        assert (folder/'stderr.txt').read_text()==''
        for a in x['input_aliases']:
            p=folder/'inputs'/Path(a['path']).name;assert sha(p)==a['sha256']
        json.loads((folder/'report.json').read_text())
    new=read(E/'runs/e8706876e0c1b5dcebd9/report.json');ind=read(E/'runs/3c16720b6c276a5997e1/report.json')
    assert new['all_ordered_DAG_cases']==9496 and new['full_support_K_cases']==28488
    assert ind['exact_oracle_cases']==9496 and ind['fixed_support_cases']==5350
    diag=read(E/'errata-diagnostic/report.json');ex=read(E/'errata-diagnostic/execution.json')
    assert diag['status']=='passed' and diag['diagnostic_runs']==1 and diag['original_entry_runs']==0 and diag['definition_only_imports']==1
    assert ex['returncode']==0 and ex['script_sha256']==sha(ST/E/'check-home-load-errata.py')
    assert (ST/E/'errata-diagnostic/stderr.txt').read_text()==''
    assert diag['cases'][0]['actual_loads']==['1','1','0'] and diag['cases'][1]['actual_loads']==['1','3/2','1']
    er=E/'errata-home-token';err=read(er/'errata-manifest.json')
    before=(ST/er/'before.md').read_text();after=(ST/er/'proposed.md').read_text();current=before
    assert sha(ST/er/'before.md')==err['before_sha256'] and sha(ST/er/'proposed.md')==err['proposed_sha256']
    assert err['replacement_count']==2 and err['logical_issues']==3
    for x in err['replacements']:
        assert current.count(x['before_exact'])==1
        assert before[:before.index(x['before_exact'])].count('\n')+1==x['before_lines'][0]
        current=current.replace(x['before_exact'],x['after_exact'])
    assert current==after
    assert ''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='a/'+err['target'],tofile='b/'+err['target']))==(ST/er/'proposed.patch').read_text()
    assert not (ST/err['target']).exists(),'shared old page may not be included as overwrite target'
    rel=read(W/'relations.json')['relations'];assert len(rel)==12
    assert all(x['common_premises'] and x['evidence'] and x['gap'] and x['phase3_graph_written'] is False for x in rel)
    nxt=read(W/'next-candidates.json')['candidates'];assert len(nxt)==5
    assert all(not x['local_progress_observed'].get('owner') and x['not_claimed_by_this_package'] for x in nxt)
    log=read(E/'reading-log.json');assert log['running_exec_sessions']=={} and len(log['completed_original_entries'])==5
    for p in ST.rglob('*.json'):json.loads(p.read_text())
    paths={p.relative_to(ST).as_posix() for p in ST.rglob('*') if p.is_file()}|{M.as_posix(),V.as_posix()}
    if manifest:
        m=read(M);assert m['ready'] is True and m['external_root']==str(ST) and set(m['copy_paths'])==paths
        assert len(m['copy_paths'])==len(paths) and set(m['files'])==paths-{M.as_posix()}
        for path,a in m['files'].items():
            p=ST/path;assert sha(p)==a['sha256'] and p.stat().st_size==a['bytes'],path
    fullsupport=sum(x['lines'] for x in support if x['id'] not in ['eef751243f82cd1689d6','ab79c520ba1a75adf3ef'])
    return {'status':'all structural and byte checks passed','primary_sources':5,'primary_bytes':57058,'primary_full_actual_lines':1405,'contiguous_actual_display_ranges':len(coverage),'formal_pages':5,'formal_lines':sum(x['lines'] for x in layout),'formal_links_checked':links,'receipts':5,'support_sources':5,'support_full_actual_lines':fullsupport,'support_selected_actual_lines':215,'formal_comparisons':4,'formal_comparison_actual_lines':sum(x['lines'] for x in comps),'relations_evidence':12,'new_original_entry_runs':5,'old_dependency_main_runs':0,'new_diagnostic_runs':1,'diagnostic_original_main_entries':0,'errata_target_pages':1,'errata_replacements':2,'errata_logical_issues':3,'exact_copy_files':len(paths),'verification_limit':'Records/bytes and finite witnesses do not certify general mathematics, authorship, external review or global novelty.'}
if __name__=='__main__':
    prepare='--prepare-validation' in sys.argv;result=validate(not prepare);encoded=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if prepare:(ST/V).write_text(encoded)
    else:assert (ST/V).read_text()==encoded
    print(json.dumps({'mode':'prepare-only-not-READY' if prepare else 'final-manifest-verified',**result},ensure_ascii=False))
