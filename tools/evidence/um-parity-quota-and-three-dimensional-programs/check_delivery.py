#!/usr/bin/env python3
"""Record and hash checks only; never executes any mathematical entry."""
from pathlib import Path
import difflib
import hashlib
import json
import re
import sys

ST=Path(__file__).resolve().parents[3];REPO=ST.parents[1]/'boss4-research'
E=Path('tools/evidence/um-parity-quota-and-three-dimensional-programs')
W=Path('cleanup/workspaces/Boss4/r3-um-parity-quota-and-three-dimensional-programs')
M=W/'copy-files.json';V=E/'validation.json'
def read(p):return json.loads((ST/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def validate(manifest=True):
    s=read(E/'source-manifest.json');ids={a['id'] for a in s}
    assert ids=={'58a0cf8f417facbe1024','8af37296657f6ee6656d','11edfbeb430cb529a9a7','a68bbc33808220d4814e','4f13d4de5870674ce284'}
    claim=read(E/'actual-claim.json')
    assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['operation']=='claim'
    assert ids<=set(claim['ids']) and claim['local_sync']['status']=='synced'
    assert claim['remote_tip']=='372a7d401e044cd87f4457e55b6ae7e79704565a'
    cov=read(E/'primary-read-coverage.json')
    for a in s:
        p=ST/a['preserved_path'];assert sha(p)==a['sha256'] and p.stat().st_size==a['size']
        assert len(p.read_text().splitlines())==a['lines'] and a['actual_full_read_after_pushed_claim']
        assert a['preparation_not_substituted_for_primary']
        ranges=sorted((b['first_line'],b['last_line']) for b in cov if b['id']==a['id'])
        assert ranges[0][0]==1 and ranges[-1][1]==a['lines']
        assert all(x[1]+1==y[0] for x,y in zip(ranges,ranges[1:]))
        assert all(b['actual_text_displayed'] for b in cov if b['id']==a['id'])
    ver=read(E/'version-and-scope-checks.json');dep=ver['prior_ready_dependency'];prior=Path(dep['external_root'])
    assert sha(prior/dep['manifest_path'])==dep['manifest_sha256']
    assert sha(prior/dep['required_formal_target'])==dep['required_formal_sha256']
    layout=read(E/'formal-layout.json');assert len(layout)==5 and len({a['id'] for a in layout})==5
    assert sum(a['type_tag']=='资源' for a in layout)==4
    links=0
    for a in layout:
        p=ST/a['path'];text=p.read_text();assert text.startswith('---\n') and '\n---\n' in text[4:]
        head={k:json.loads(v) for k,v in (line.split(': ',1) for line in text.split('\n---\n',1)[0][4:].splitlines())}
        assert head['id']==a['id'] and head['type_tag']==a['type_tag']
        assert head['kind']==('resource' if a['type_tag']=='资源' else 'review')
        assert all(head[k] for k in ('title','status','summary','source_refs'))
        for target in re.findall(r'\]\(([^)]+)\)',text):
            target=target.split('#',1)[0]
            if not target or '://' in target:continue
            q=(p.parent/target).resolve();rel=q.relative_to(ST)
            allowed_prior=(rel.as_posix()==dep['required_formal_target'] and (prior/rel).exists())
            assert q.exists() or (REPO/rel).exists() or allowed_prior,(a['path'],target)
            links+=1
        for old in (REPO/'archives/unrelated-machines/state').rglob('*.md'):
            if old.relative_to(REPO).as_posix()==a['path']:continue
            header=old.read_text().split('\n---\n',1)[0]
            assert not re.search(r'^id:\s*["\']?'+re.escape(a['id'])+r'["\']?\s*$',header,re.M)
    receipts=read(W/'semantic-receipts.json');assert {a['id'] for a in receipts}==ids
    for a in receipts:
        assert all(a[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
        assert a['disposition']=='integrated' and all(a[k] for k in ('read_note','comparison_note','decision_note'))
        assert a['targets']==[b['path'] for b in layout if a['id'] in b['primary_ids']]
    support=read(E/'supporting-source-manifest.json');assert len(support)==6
    assert {a['id'] for a in support}.isdisjoint(ids)
    for a in support:
        p=ST/a['preserved_path'];assert sha(p)==a['sha256'] and p.stat().st_size==a['size']
        assert len(p.read_text().splitlines())==a['lines'] and a['actual_full_read']
        assert a['read_ranges']==[[1,a['lines']]] and not a['new_primary_receipt']
    comps=read(E/'comparison-manifest.json');assert len(comps)==5
    for a in comps:
        assert sha(ST/a['snapshot'])==a['sha256'] and a['actual_full_read']
        assert a['read_ranges']==[[1,a['lines']]] and not a['new_primary_receipt']
    runscope=read(E/'execution-and-scope.json');assert runscope['new_original_entry_runs_total']==4
    assert runscope['new_parity_entry_runs']==0 and runscope['prior_same_SHA_parity_entry_runs_reused']==1
    for a in runscope['new_original_entries']:
        assert a['source_id']!='58a0cf8f417facbe1024' and a['entry_runs_this_batch']==1 and a['returncode']==0
        assert a['cwd_initially_empty'] and a['input_files']==[] and a['project_module_imports']==[]
        folder=ST/E/'runs'/a['source_id']
        assert sha(folder/'stdout.txt')==a['stdout_sha256'] and sha(folder/'stderr.txt')==a['stderr_sha256']
        assert (folder/'stderr.txt').read_text()==''
        orig=next(b for b in s if b['id']==a['source_id'])
        assert a['source_sha256']==orig['sha256']
    reuse=read(E/'prior-parity-run/reuse.json');assert reuse['current_new_entry_runs']==0 and reuse['prior_isolated_entry_runs_reused']==1
    parity=next(a for a in s if a['id']=='58a0cf8f417facbe1024')
    assert reuse['same_source_sha256']==parity['sha256'] and reuse['not_new_current_execution']
    assert sha(Path(reuse['prior_external_root'])/reuse['prior_manifest_path'])==reuse['prior_manifest_sha256']
    for a in reuse['prior_raw_files_copied']:assert sha(ST/a['path'])==a['sha256']
    old=read(E/'prior-parity-run/report.json')
    assert old['archived_entry_sha256']==parity['sha256'] and old['archived_entry_runs']==1 and old['original_returncode']==0
    assert (ST/E/'prior-parity-run/stderr.txt').read_text()==''
    diag=read(E/'run-diagnostics/report.json');assert diag['diagnostic_runs']==1 and diag['original_entry_runs_in_this_diagnostic']==0
    assert diag['original_definition_only_loads']==4 and diag['diagnostic_sha256']==sha(ST/E/'diagnose-models-and-counts.py')
    bad=diag['three_dimensional_original_oracle_defect']
    assert bad['original_brute_b']=='1/3' and bad['independent_typed_tree_b']==bad['original_closed_form']=='1/2'
    assert bad['analytic_identity_refuted'] is False and bad['original_full_entry_failed'] is False
    different=diag['multi_label_versus_single_neighborhood']
    assert different['multi_label_bundle_b']=='1/2' and different['collapsed_single_A_per_choice_b']=='1'
    assert diag['single_layer_free_q_boundary']['nu_K']==2
    counts=diag['actual_loop_counts']
    assert counts['bundle_exhaustive_q1_K_instances']==32 and counts['single_exhaustive_cases']==4788
    assert counts['three_exhaustive_instance_K_comparisons']==1290 and counts['three_q3_sample_K_comparisons']==2408
    assert counts['quota_pair_shift_low_t_cases']==4375 and counts['quota_tournament_cases']==3
    er=E/'errata-quota-model-and-oracle';err=read(er/'errata-manifest.json')
    assert err['target_files']==2 and err['exact_replacements']==7
    assert sum(a['replacement_count'] for a in err['targets'])==7
    for a in err['targets']:
        prefix=a['key'];before=(ST/er/(prefix+'-before.md')).read_text()
        after=(ST/er/(prefix+'-proposed.md')).read_text();current=before
        assert sha(ST/er/(prefix+'-before.md'))==a['before_sha256']
        assert sha(ST/er/(prefix+'-proposed.md'))==a['proposed_sha256']
        for change in a['replacements']:
            assert current.count(change['exact_before'])==1
            assert before[:before.index(change['exact_before'])].count('\n')+1==change['original_start_line']
            current=current.replace(change['exact_before'],change['exact_after'])
        assert current==after
        patch=''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='a/'+a['target_path'],tofile='b/'+a['target_path']))
        assert patch==(ST/er/(prefix+'.patch')).read_text()
    add=read(E/'errata-evidence-line-addendum-v2.json')
    assert add['frozen_errata_manifest_sha256']==sha(ST/er/'errata-manifest.json')
    assert add['exact_source_ranges']==[[77,82]] and not add['math_or_replacement_change']
    assert 'options.append' in (ST/E/'original/4f13d4de5870674ce284.py').read_text().splitlines()[78]
    assert 'zip(' in (ST/E/'original/4f13d4de5870674ce284.py').read_text().splitlines()[81]
    rel=read(W/'relations.json')['relations'];assert len(rel)==11
    assert all(a['common_premises'] and a['evidence'] and a['gap'] and not a['phase3_graph_written'] for a in rel)
    nxt=read(W/'next-candidates.json')['candidates'];assert len(nxt)==5
    assert all(not a['local_progress_observed'].get('owner') and a['not_claimed_by_this_package'] for a in nxt)
    for p in ST.rglob('*.json'):json.loads(p.read_text())
    paths={p.relative_to(ST).as_posix() for p in ST.rglob('*') if p.is_file()}|{M.as_posix(),V.as_posix()}
    if manifest:
        m=read(M);assert m['ready'] is True and m['external_root']==str(ST)
        assert set(m['copy_paths'])==paths and len(m['copy_paths'])==len(paths)
        assert set(m['files'])==paths-{M.as_posix()}
        for path,a in m['files'].items():
            p=ST/path;assert sha(p)==a['sha256'] and p.stat().st_size==a['bytes'],path
    return {'status':'all structural and byte checks passed','primary_sources':5,'primary_bytes':sum(a['size'] for a in s),
      'primary_lines':sum(a['lines'] for a in s),'contiguous_actual_read_blocks':len(cov),'formal_pages':5,
      'formal_lines':sum(len((ST/a['path']).read_text().splitlines()) for a in layout),'formal_local_links_checked':links,
      'supporting_sources':6,'support_actual_full_lines':sum(a['lines'] for a in support),'formal_comparisons':5,
      'comparison_actual_full_lines':sum(a['lines'] for a in comps),'receipts':5,'relations':11,'exact_copy_files':len(paths),
      'new_original_entry_runs_recorded':4,'prior_same_SHA_entry_runs_reused':1,'new_independent_diagnostic_runs_recorded':1,
      'new_diagnostic_original_entry_runs':0,'new_errata_target_pages':2,'new_errata_replacements':7,
      'verification_limit':'hash/record checks and finite counterexamples do not prove general mathematics, source hardness or historical independence'}

if __name__=='__main__':
    prepare='--prepare-validation' in sys.argv;result=validate(manifest=not prepare)
    encoded=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if prepare:(ST/V).write_text(encoded)
    else:assert (ST/V).read_text()==encoded
    print(json.dumps({'mode':'prepare-only-not-READY' if prepare else 'final-manifest-verified',**result},ensure_ascii=False))
