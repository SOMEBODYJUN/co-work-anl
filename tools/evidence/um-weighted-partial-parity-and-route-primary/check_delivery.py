#!/usr/bin/env python3
"""Byte/record validation only; never executes archived or new math code."""
from pathlib import Path
import hashlib
import json
import re
import sys

ST=Path(__file__).resolve().parents[3]
REPO=ST.parents[1]/'boss4-research'
E=Path('tools/evidence/um-weighted-partial-parity-and-route-primary')
W=Path('cleanup/workspaces/Boss4/r3-um-weighted-partial-parity-and-route-primary')
M=W/'copy-files.json';V=E/'validation.json'
def read(p):return json.loads((ST/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def validate(manifest=True):
    source=read(E/'source-manifest.json');ids={a['id'] for a in source}
    assert ids=={'6b11559d50dd8f8fb23c','371e4302c248eaf14f86','ad465f429de1d94fc30a'}
    claim=read(E/'actual-claim.json')
    assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['operation']=='claim'
    assert set(claim['ids'])==ids and claim['local_sync']['status']=='synced'
    assert claim['remote_tip']=='5ba6efa08661893ade1dd40516174169777e6770'
    coverage=read(E/'primary-read-coverage.json')
    for a in source:
        p=ST/a['preserved_path'];assert sha(p)==a['sha256'] and p.stat().st_size==a['size']
        assert len(p.read_text().splitlines())==a['lines'] and a['actual_full_read_after_pushed_claim']
        assert a['preparation_read_not_substituted']
        blocks=sorted((b['first_line'],b['last_line']) for b in coverage if b['id']==a['id'])
        assert blocks[0][0]==1 and blocks[-1][1]==a['lines']
        assert all(x[1]+1==y[0] for x,y in zip(blocks,blocks[1:]))
        assert all(b['actual_text_displayed'] for b in coverage if b['id']==a['id'])
    versions=read(E/'version-and-scope-checks.json')
    dep=versions['previous_ready_dependency'];previous=Path(dep['external_root'])
    assert sha(previous/dep['manifest_path'])==dep['manifest_sha256']
    assert sha(previous/dep['required_formal_target'])==dep['required_formal_sha256']
    layout=read(E/'formal-layout.json');assert len(layout)==3 and len({a['id'] for a in layout})==3
    links=0
    for a in layout:
        p=ST/a['path'];text=p.read_text();assert text.startswith('---\n') and '\n---\n' in text[4:]
        fields={k:json.loads(v) for k,v in (line.split(': ',1) for line in text.split('\n---\n',1)[0][4:].splitlines())}
        assert all(k in fields for k in ('id','kind','type_tag','title','status','summary','source_refs'))
        assert fields['id']==a['id'] and fields['type_tag']==a['type_tag'] and fields['source_refs']
        assert fields['kind']==('resource' if a['type_tag']=='资源' else 'review')
        for target in re.findall(r'\]\(([^)]+)\)',text):
            target=target.split('#',1)[0]
            if not target or '://' in target:continue
            q=(p.parent/target).resolve();rel=q.relative_to(ST)
            allowed_prior=(rel.as_posix()==dep['required_formal_target'] and (previous/rel).exists())
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
    supports=read(E/'supporting-source-manifest.json');assert len(supports)==4
    assert {a['id'] for a in supports}.isdisjoint(ids)
    for a in supports:
        p=ST/a['preserved_path'];assert sha(p)==a['sha256'] and p.stat().st_size==a['size']
        assert len(p.read_text().splitlines())==a['lines'] and a['actual_full_read_this_batch']
        assert a['read_ranges']==[[1,a['lines']]] and not a['new_primary_receipt']
    comparisons=read(E/'comparison-manifest.json');assert len(comparisons)==6
    for a in comparisons:
        assert sha(ST/a['snapshot'])==a['sha256'] and a['read_ranges']==[[1,a['lines']]]
        assert not a['new_primary_receipt']
    report=read(E/'run-parity-and-certificates/report.json')
    assert report['wrapper_runs']==report['archived_entry_runs']==1
    assert report['archived_entry_sha256']==sha(ST/E/'support/parity_block_check.py')
    assert report['wrapper_sha256']==sha(ST/E/'reproduce-and-check.py')
    assert report['original_returncode']==0 and report['original_entry_imports_no_project_modules']
    assert (ST/E/'run-parity-and-certificates/stderr.txt').read_text()==''
    stdout=(ST/E/'run-parity-and-certificates/stdout.txt').read_text().splitlines();assert len(stdout)==6
    assert report['constants']['coverage_bound']=='2500154630232929/3750000000000000'
    assert report['constants']['margin_over_two_thirds']=='154630232929/3750000000000000'
    fixtures=report['complete_ordinary_UM_certificates'];assert len(fixtures)==8
    assert sum(a['parity']=='even' for a in fixtures)==6 and sum(a['parity']=='odd' for a in fixtures)==2
    assert max(a['jobs'] for a in fixtures)==777 and max(a['finite_entries'] for a in fixtures)==5529
    assert all(a['all_jobs_once_original_legal_end'] and a['one_X_token_per_choice_vertex'] and not a['proves_OPT_by_enumeration'] for a in fixtures)
    execution=read(E/'execution-note.json');assert execution['runs']=={'wrapper':1,'original_child_entry':1}
    relations=read(W/'relations.json')['relations'];assert len(relations)==10
    assert all(a['common_premises'] and a['evidence'] and a['gap'] and not a['phase3_graph_written'] for a in relations)
    nexts=read(W/'next-candidates.json')['candidates'];assert len(nexts)==5
    assert all(not a['local_progress_observed'].get('owner') and a['not_claimed_by_this_package'] for a in nexts)
    assert '58a0cf8f417facbe1024' not in ids
    for p in ST.rglob('*.json'):json.loads(p.read_text())
    paths={p.relative_to(ST).as_posix() for p in ST.rglob('*') if p.is_file()}|{M.as_posix(),V.as_posix()}
    if manifest:
        m=read(M);assert m['ready'] is True and m['external_root']==str(ST)
        assert set(m['copy_paths'])==paths and len(m['copy_paths'])==len(paths)
        assert set(m['files'])==paths-{M.as_posix()}
        for path,a in m['files'].items():
            p=ST/path;assert sha(p)==a['sha256'] and p.stat().st_size==a['bytes'],path
    return {'status':'all structural and byte checks passed','primary_sources':3,'primary_bytes':sum(a['size'] for a in source),
       'primary_lines':sum(a['lines'] for a in source),'contiguous_read_blocks':len(coverage),'formal_pages':3,
       'formal_lines':sum(len((ST/a['path']).read_text().splitlines()) for a in layout),'formal_local_links_checked':links,
       'supporting_sources':4,'support_full_actual_lines':sum(a['lines'] for a in supports),
       'formal_comparisons':6,'formal_comparison_actual_lines':sum(a['lines'] for a in comparisons),
       'receipts':3,'relations':10,'exact_copy_files':len(paths),'wrapper_runs_recorded':1,'archived_entry_runs_recorded':1,
       'new_actual_certificate_fixtures':8,'parity_source_identity_clarifications':2,
       'verification_limit':'structural/byte checks and fixed-fixture evidence do not prove general mathematics, source hardness or historical independence'}

if __name__=='__main__':
    prepare='--prepare-validation' in sys.argv;result=validate(manifest=not prepare)
    encoded=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if prepare:(ST/V).write_text(encoded)
    else:assert (ST/V).read_text()==encoded
    print(json.dumps({'mode':'prepare-only-not-READY' if prepare else 'final-manifest-verified',**result},ensure_ascii=False))
