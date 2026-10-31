#!/usr/bin/env python3
"""Structural byte/record checks only; no mathematical program is executed."""
from pathlib import Path
import json,hashlib,difflib,re,sys
S=Path(__file__).resolve().parents[3];R=S.parents[1]/'boss4-research'
E=Path('tools/evidence/um-occupation-and-menu-primary');W=Path('cleanup/workspaces/Boss4/r3-um-occupation-and-menu-primary');M=W/'copy-files.json';V=E/'validation.json'
def read(p):return json.loads((S/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def validate(manifest=True):
    sources=read(E/'source-manifest.json');ids={x['id'] for x in sources}
    assert ids=={'1d9b334ebced677c1709','766b5a5b121a0ebb3751','6981dd956e13b85d220f','46554c947efcae1aa3e7','555810a28cb65428aed4'}
    claim=read(E/'actual-claim.json');assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['operation']=='claim' and claim['local_sync']['status']=='synced'
    assert claim['remote_tip']=='9bff88d715e258bf152edf97073591b1652307e2' and len(claim['ids'])==25 and ids<=set(claim['ids'])
    owner=read(E/'owner-verification.json');assert set(owner['primary_actual_intersection'])==ids and owner['capture_ids_count']==25
    assert {x['id'] for x in owner['initial_owner_records']}==ids
    for x in owner['initial_owner_records']:
        assert x['owner']=='Boss4' and x['disposition']=='in-progress' and x['request_id']=='cfe5382a75514231b8a7b18d6e0589e3'
        assert x['source_sha256']==next(s['sha256'] for s in sources if s['id']==x['id'])
    cov=read(E/'primary-read-coverage.json')
    for x in sources:
        p=S/x['preserved_path'];assert sha(p)==x['sha256'] and p.stat().st_size==x['size'] and len(p.read_text().splitlines())==x['lines']
        assert x['actual_full_read_after_pushed_claim'] and x['preparation_not_substituted_for_primary'] and x['unique_units_accounted_for']
        ranges=sorted((a['first_line'],a['last_line']) for a in cov if a['id']==x['id'])
        assert ranges[0][0]==1 and ranges[-1][1]==x['lines'] and all(a[1]+1==b[0] for a,b in zip(ranges,ranges[1:]))
    assert sum(x['size'] for x in sources)==49464 and sum(x['lines'] for x in sources)==1111 and len(cov)==7 and all(x['actual_text_displayed'] for x in cov)
    layout=read(E/'formal-layout.json');assert len(layout)==5 and len({x['id'] for x in layout})==5
    links=0
    for x in layout:
        p=S/x['path'];t=p.read_text();assert t.startswith('---\n')
        h={k:json.loads(v) for k,v in (a.split(': ',1) for a in t.split('\n---\n',1)[0][4:].splitlines())}
        assert h['id']==x['id'] and h['kind']=='resource' and h['type_tag']=='资源' and h['source_ids']==x['primary_ids']
        assert all(h[k] for k in ['title','status','summary','source_refs'])
        for a in re.findall(r'\]\(([^)]+)\)',t):
            a=a.split('#',1)[0]
            if not a or '://' in a:continue
            q=(p.parent/a).resolve();rel=q.relative_to(S);assert q.exists() or (R/rel).exists(),(x['path'],a);links+=1
        for old in (R/'archives/unrelated-machines/state').rglob('*.md'):
            if old.relative_to(R).as_posix()==x['path']:continue
            assert not re.search(r'^id:\s*["\']?'+re.escape(x['id'])+r'["\']?\s*$',old.read_text().split('\n---\n',1)[0],re.M)
    receipts=read(W/'semantic-receipts.json');assert {x['id'] for x in receipts}==ids
    for x in receipts:
        assert all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and x['disposition']=='integrated'
        assert all(x[k] for k in ['read_note','comparison_note','decision_note'])
        assert x['targets']==[p['path'] for p in layout if x['id'] in p['primary_ids']]
    support=read(E/'support-manifest.json');assert len(support)==1 and support[0]['id']=='c8cdbf5ff2de274caf1b'
    x=support[0];p=S/x['snapshot'];assert sha(p)==x['inventory']['sha256'] and p.stat().st_size==9982 and x['lines']==130 and x['actual_read_ranges']==[[1,130]] and x['actual_full_read'] and not x['extra_receipt']
    comp=read(E/'comparison-manifest.json');assert len(comp)==9
    for x in comp:assert sha(S/x['snapshot'])==x['sha256'] and x['actual_read'].startswith('full') and not x['new_primary'] and not x['receipt']
    ignored=read(E/'export-selection-note.json');assert ignored['id']=='681999ce023678a10c97' and ignored['not_primary'] and ignored['not_support_claimed_read']
    assert not (S/E/'support/681999ce023678a10c97.md').exists()
    exe=read(E/'execution-and-scope.json');assert exe['original_main_entries']==4 and exe['original_library_main_entries']==0 and exe['new_library_api_probe_runs']==1
    assert exe['all_reports_every_field_actually_read'] and {x['source_id'] for x in exe['entries']}==ids
    for x in exe['entries']:
        folder=S/E/'runs'/x['source_id'];library=x['source_id']=='46554c947efcae1aa3e7'
        assert x['original_main_entries']==(0 if library else 1) and x['api_probe_runs']==(1 if library else 0)
        assert x['returncode']==0 and x['cwd_initially_empty'] and x['inputs_unchanged_after_run']
        assert sha(folder/'stdout.txt')==x['stdout_sha256'] and sha(folder/'stderr.txt')==x['stderr_sha256'] and (folder/'stderr.txt').read_text()==''
        for a in x['input_aliases']:assert sha(folder/'input-tree'/a['relative_path'])==a['sha256']
    menu=read(E/'runs/1d9b334ebced677c1709/report.json');face=read(E/'runs/766b5a5b121a0ebb3751/report.json');edge=read(E/'runs/6981dd956e13b85d220f/report.json');core=read(E/'runs/46554c947efcae1aa3e7/report.json');cycle=read(E/'runs/555810a28cb65428aed4/report.json')
    assert sum(x['feasible'] for x in menu['enumeration'])==3528 and menu['counts']['feasible_cases']==3536 and menu['counts']['boundary_fixtures']==8 and menu['counts']['enumerated_candidates']==5696
    assert face['transversal_presentations']==304 and face['exposed_faces_with_multiplicity']==20760 and face['violations']==0
    assert len(edge['cases'])==15 and sum(x['all_occupancy_subsets_checked'] for x in edge['cases'])==162 and sum(x['labelled_edge_orientations_checked'] for x in edge['cases'])==1035
    assert core['original_library_main_entries']==0 and core['new_api_probe_runs']==1 and [x['non_singleton_homes'] for x in core['cases']]==[2,4]
    assert sum(x['legal_assignments'] for x in cycle['runs'])==25600 and len(cycle['runs'])==3
    er=E/'errata-counts-and-dynamic-opt';err=read(er/'errata-manifest.json');assert err['target_files']==3 and err['exact_replacements']==3 and err['new_extra_program_runs_for_errata']==0
    for x in err['targets']:
        bp=S/er/(x['key']+'-before.md');ap=S/er/(x['key']+'-proposed.md');before=bp.read_text();after=ap.read_text();current=before
        assert sha(bp)==x['before_sha256'] and sha(ap)==x['proposed_sha256']
        for a in x['replacements']:
            assert current.count(a['exact_before'])==1 and before[:before.index(a['exact_before'])].count('\n')+1==a['before_lines'][0]
            current=current.replace(a['exact_before'],a['exact_after'])
        assert current==after and not (S/x['target_path']).exists()
        assert ''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='a/'+x['target_path'],tofile='b/'+x['target_path']))==(S/er/(x['key']+'.patch')).read_text()
    rel=read(W/'relations.json')['relations'];assert len(rel)==14 and all(x['common_premises'] and x['evidence'] and x['gap'] and x['phase3_graph_written'] is False for x in rel)
    nxt=read(W/'next-candidates.json')['candidates'];assert len(nxt)==5 and ids.isdisjoint({x['id'] for x in nxt}) and all(not x['local_progress_observed'].get('owner') and x['not_claimed_by_this_package'] and x['known_actual_pushed_claims_excluded'] for x in nxt)
    log=read(E/'reading-log.json');assert log['running_sessions']=={} and log['reports_every_field_actually_read'] and log['actual_claim_file_is_unmodified_full25']
    for p in S.rglob('*.json'):json.loads(p.read_text())
    paths={p.relative_to(S).as_posix() for p in S.rglob('*') if p.is_file()}|{M.as_posix(),V.as_posix()}
    if manifest:
        m=read(M);assert m['ready'] is True and set(m['copy_paths'])==paths and len(m['copy_paths'])==len(paths) and set(m['files'])==paths-{M.as_posix()}
        for path,a in m['files'].items():assert sha(S/path)==a['sha256'] and (S/path).stat().st_size==a['bytes'],path
    return {'status':'all structural and byte checks passed','full_actual_claim_ids':25,'primary_subset_sources':5,'primary_bytes':49464,'primary_full_actual_lines':1111,'actual_display_ranges':7,'formal_pages':5,'formal_lines':sum(x['lines'] for x in layout),'formal_links_checked':links,'receipts':5,'support_sources':1,'support_full_actual_lines':130,'formal_comparisons':9,'comparison_full_actual_lines':sum(x['lines'] for x in comp),'relations_evidence':14,'new_original_main_entries':4,'library_original_main_entries':0,'new_library_api_probes':1,'errata_target_pages':3,'errata_exact_replacements':3,'new_errata_runs':0,'exact_copy_files':len(paths),'verification_limit':'Records/hashes and finite reports do not prove general mathematics, historical independence, external review or novelty.'}
if __name__=='__main__':
    prepare='--prepare-validation' in sys.argv;r=validate(not prepare);text=json.dumps(r,ensure_ascii=False,indent=2)+'\n'
    if prepare:(S/V).write_text(text)
    else:assert (S/V).read_text()==text
    print(json.dumps({'mode':'prepare-only-not-READY' if prepare else 'final-manifest-verified',**r},ensure_ascii=False))
