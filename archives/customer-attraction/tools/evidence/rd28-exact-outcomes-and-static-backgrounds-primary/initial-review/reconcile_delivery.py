#!/usr/bin/env python3
"""Static delivery reconciliation; never imports or executes a mathematical engine."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import re
from itertools import product


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--repo',required=True,type=Path)
    args=ap.parse_args();package=Path(__file__).resolve().parent
    stage=next(parent for parent in package.parents if parent.name=='deliverables')
    manifest=json.loads((package/'manifest.json').read_text());receipts=json.loads((package/'receipts.json').read_text())
    assert manifest['primary_count']==len(manifest['sources'])==len(receipts)==11
    assert manifest['primary_bytes']==sum(row['size'] for row in manifest['sources'])==136521
    assert {row['id'] for row in manifest['sources']}=={row['id'] for row in receipts}
    original_checks=[]
    for row in manifest['sources']:
        path=package/row['package_path']
        assert path.stat().st_size==row['size'] and sha(path)==row['sha256']
        assert len(row['sources'])==2 and all(len(s['commit'])==40 and s['path']==row['path'] for s in row['sources'])
        original_checks.append({'id':row['id'],'size':row['size'],'sha256':row['sha256']})
    for row in receipts:
        assert row['disposition']=='integrated'
        assert all(row[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
        assert all(row[k] for k in ('read_note','comparison_note','decision_note','targets'))
        assert all((stage/target).is_file() for target in row['targets'])
    run=package/'new-fixed-audit-001';event=json.loads((run/'execution-record.json').read_text())
    assert event['exit_code']==0 and event['new_fixed_audit_process_calls']==1
    assert event['stdout_bytes']==(run/'stdout.txt').stat().st_size==5339
    assert event['stderr_bytes']==0 and (run/'stderr.txt').read_bytes()==b''
    assert event['stdout_sha256']==sha(run/'stdout.txt') and event['stderr_sha256']==sha(run/'stderr.txt')
    assert event['script_sha256']==sha(package/'audit_fixed_records.py')
    assert all(event[k]==0 for k in ('original_CLI_calls','original_80_self_test_calls','project_solver_or_verifier_calls','LP_calls','random_search_calls','mature_all_big_seed_rechecks'))
    summary=json.loads((run/'data/summary.json').read_text())
    assert json.loads((run/'stdout.txt').read_text())==summary and summary['all_checks_passed'] is True
    original=json.loads((package/'original/notes/global_ne_boundary.json').read_text())
    fixed=json.loads((run/'data/global-boundary-fixed.json').read_text())
    assert fixed['source_literal_policy'] is True
    literal={tuple(r['history']):r['action'] for r in original['certificate']['actions']}
    layers=[''.join(str(literal[h]) for h in product(range(5),repeat=d)) for d in range(5)]
    assert layers==fixed['action_layers_depth_lex']
    assert len(fixed['all_static_counts'])==126 and len(fixed['all_static_PNE'])==1
    assert sorted(map(tuple,fixed['all_spe_counts']))==sorted(map(tuple,original['all_spe_counts']))
    assert fixed['minimum_spe_welfare']==original['minimum_spe_welfare']==54
    assert fixed['minimum_ne_welfare']==original['minimum_ne_welfare']==56
    old=json.loads((package/'original/experiments/cex_last_half_probe.json').read_text())
    all_reports=[fixed]
    for i,row in enumerate(old['records']):
        data=json.loads((run/f'data/last-record-{i:02d}-new-policy.json').read_text())
        assert data['source_literal_policy'] is False
        assert data['actual_path']==row['path'] and data['weights']==row['weights']
        assert data['individual']==row['individual'] and data['aggregate']==row['aggregate']
        assert data['record_index']==i and data['trial']==row['trial']
        all_reports.append(data)
    assert len(all_reports)==9 and len(old['records'])==8
    for i,row in enumerate(all_reports):
        p=5 if i==0 else 7
        assert [len(layer) for layer in row['action_layers_depth_lex']]==[p**d for d in range(5)]
        assert len(row['node_payload_ids_depth_lex'])==row['histories']
        assert all(len(values)==p for values in row['payloads_scaled'])
        assert all(0<=idx<len(row['payloads_scaled']) for idx in row['node_payload_ids_depth_lex'])
        assert row['comparisons_including_self']==row['histories']*p
        assert row['strict']+row['ties']==row['nonself_comparisons']==row['histories']*(p-1)
    comparisons=json.loads((package/'comparison-record.json').read_text())
    for row in comparisons['direct_formal_comparisons']:
        path=args.repo/row['path']
        assert path.stat().st_size==row['size'] and sha(path)==row['sha256']
    formal=sorted((stage/'archives/customer-attraction/state').rglob('*.md'))
    assert len(formal)==4
    links=[]
    for page in formal+[package/'README.md']:
        text=page.read_text()
        if page in formal:
            assert text.startswith('---\nid: ') and '\nsource_refs:\n' in text
            assert re.search(r'source:[0-9a-f]{40}:research/',text)
        for link in re.findall(r'\]\(([^)]+)\)',text):
            if re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:',link) or link.startswith('#'):continue
            resolved=(page.parent/link.split('#',1)[0]).resolve()
            if resolved.is_file():kind='stage'
            else:
                rel=resolved.relative_to(stage);assert (args.repo/rel).is_file(),(str(page),link)
                kind='inherited-repository'
            links.append({'page':str(page.relative_to(stage)),'link':link,'resolved':kind})
    result={'checked_at_utc':datetime.now(timezone.utc).isoformat(),'identity':'Boss3',
            'scope':'static source hashes, receipt targets, original/new policy provenance and output shape, stored event and report transcription, links and mature comparison hashes; zero mathematical re-execution',
            'primary_checks':original_checks,'receipts':11,'formal_pages':4,
            'fixed_policy_data_files':9,'inherited_original_policy':1,'newly_constructed_policy_files':8,
            'formal_comparison_hashes':len(comparisons['direct_formal_comparisons']),
            'links':links,'mathematical_reexecutions_in_this_check':0,'original_CLI_calls_in_this_check':0,
            'all_checks_passed':True}
    (package/'self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'ok':True,'primary_sources':11,'receipts':11,'formal_pages':4,'policy_data':9,
                      'links':len(links),'mature_hashes':len(comparisons['direct_formal_comparisons']),
                      'mathematical_reexecutions':0},ensure_ascii=False))


if __name__=='__main__':main()
