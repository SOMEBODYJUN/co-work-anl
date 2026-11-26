#!/usr/bin/env python3
"""Freeze complete note evidence or bind three already-written final reviews.

This tool generates no findings, observations, candidate decisions or identities.
The three actual reports must already name and review the frozen version.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT / '.agents/skills/math-notes-evidence-audit/scripts'))
from audit import content_snapshot, expected_scope, file_inventory, load_json, safe_path, sha256_file


def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def current(project):
    mp,lp = project/'manifest.json',project/'ledger.json'
    manifest,ledger = load_json(mp),load_json(lp)
    return mp,lp,manifest,ledger,content_snapshot(mp,lp,manifest,ledger)


def freeze(project):
    mp,lp,manifest,ledger,snapshot = current(project)
    if ledger['final_rounds']:
        raise ValueError('a final chain already exists; archive and genuinely restart if content changed')
    precheck = load_json(project/'audit-prefinal-report.json')
    if (precheck['snapshot_sha256'] != snapshot or precheck['unresolved_count'] != 0 or
        any(not error.startswith('FINAL_THREE_ROUNDS:') for error in precheck['structural_errors'])):
        raise ValueError('latest original-evidence audit must have zero unresolved records and only the missing-final-round gate')
    state = {'note_id':ledger['review_policy']['note_id'],
             'snapshot_sha256':snapshot,'scope':expected_scope(manifest,ledger),
             'document_hashes':{name:sha256_file(project/name) for name in
                                ['source-transcript.md','study-notes.md','source-target-map.json']},
             'file_digests':{key:sha256_file(path) for key,path in
                              sorted(file_inventory(mp,lp,manifest,ledger).items())},
             'review_policy':ledger['review_policy'],
             'instruction':'Each registered reviewer independently rereads the original images and reviews the whole frozen content. No review conclusion is supplied here.'}
    write(project/'audit/final-freeze.json',state)
    print(json.dumps({'snapshot_sha256':snapshot,'scope_counts':{k:len(v) for k,v in state['scope'].items()},
                      'document_hashes':state['document_hashes']},ensure_ascii=False,indent=2))


def bind(project,report_paths):
    mp,lp,manifest,ledger,snapshot = current(project)
    if ledger['final_rounds']:
        raise ValueError('do not overwrite or reseal an existing final review chain')
    frozen = load_json(project/'audit/final-freeze.json')
    if frozen['snapshot_sha256'] != snapshot:
        raise ValueError('content changed after freeze; actual reviews must restart')
    if len(report_paths) != 3:
        raise ValueError('exactly three actual independent reports are required')
    scope = expected_scope(manifest,ledger)
    current_hashes = {name:sha256_file(project/name) for name in frozen['document_hashes']}
    participants = set(ledger['review_policy']['reviewer_ids'])
    reviewers,sessions = set(),set()
    records = []
    for number,relative in enumerate(report_paths,1):
        path = safe_path(project,relative)
        report = load_json(path)
        reviewer,session = report['reviewer_id'],report['session_id']
        if reviewer not in participants or reviewer in reviewers or session in sessions:
            raise ValueError('reports must come from the three different actual registered agents')
        reviewers.add(reviewer);sessions.add(session)
        if report['snapshot_sha256'] != snapshot or report['findings']:
            raise ValueError('an actual review is stale or still has findings')
        for phase in ['document_hashes_start','document_hashes_end']:
            if any(report[phase].get(k) != v for k,v in current_hashes.items()):
                raise ValueError('the actual final report is not bound to the current documents')
        for key,ids in scope.items():
            actual = report['scope'][key]
            if len(actual)!=len(set(actual)) or set(actual)!=set(ids):
                raise ValueError('an actual report did not review the complete scope: '+key)
        blind = report['blind_reading']
        if sha256_file(safe_path(project,blind['path'])) != blind['sha256']:
            raise ValueError('independent source-reread file does not match its declared hash')
        records.append({'id':f'{frozen["note_id"]}-FINAL-{number:02d}','round':number,
                        'reviewer_id':reviewer,'session_id':session,'snapshot_sha256':snapshot,
                        'previous_round_sha256':None,'scope':report['scope'],
                        'findings':report['findings'],'evidence_ids':report['evidence_ids'],
                        'page_notes':report['page_notes'],'notes':report['notes'],
                        'blind_reading':blind,'report':{'path':relative,'sha256':sha256_file(path)},
                        'record_sha256':None})
    if reviewers != participants:
        raise ValueError('all three actual members must complete their final reviews')
    hashes = []
    for record in records:
        ledger = load_json(lp)
        ledger['final_rounds'].append(record)
        write(lp,ledger)
        done = subprocess.run([sys.executable,str(ROOT/'tools/campaign_audit.py'),'seal-round',
                               '--manifest',str(mp),'--ledger',str(lp),'--round-id',record['id']],
                              capture_output=True,text=True)
        if done.returncode:
            raise RuntimeError(done.stderr)
        hashes.append(done.stdout.strip())
    print(json.dumps({'snapshot_sha256':snapshot,'actual_reviewers':sorted(reviewers),
                      'sealed_round_hashes':hashes},ensure_ascii=False,indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['freeze','bind'])
    parser.add_argument('project',type=Path)
    parser.add_argument('--reports',nargs=3)
    args = parser.parse_args()
    if args.command == 'freeze':
        freeze(args.project.resolve())
    else:
        bind(args.project.resolve(),args.reports or [])
