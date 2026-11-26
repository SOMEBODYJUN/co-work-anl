#!/usr/bin/env python3
"""Bind an actual, current, nonauthor review to an authored note plan.

This does not perform a review. The report must already contain the reviewer's
observations, explicit recovery acceptances, full inventory and current hashes.
It refuses findings, stale files, a partial scope or an author as reviewer.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys

from build_note_ledger import build


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    parser.add_argument('--report', required=True)
    parser.add_argument('--narrative', required=True)
    args = parser.parse_args()
    project = args.project.resolve()
    plan_path = project / 'content-plan.json'
    plan, ledger, manifest = (load(project / n) for n in
                              ['content-plan.json','ledger.json','manifest.json'])
    def contained(relative):
        path = (project / relative).resolve()
        if not path.is_relative_to(project) or not path.is_file():
            raise ValueError('review evidence must be a real file inside this project')
        return path
    report_path, narrative_path = contained(args.report), contained(args.narrative)
    report = load(report_path)
    reviewer, session = report['reviewer_id'], report['session_id']
    if reviewer in plan['authors'] or session in plan['authors']:
        raise ValueError('second pass must be performed by the nonauthor reviewer')
    if reviewer not in plan['review_policy']['reviewer_ids']:
        raise ValueError('reviewer is not an actual registered member of this note trio')
    if report['findings']:
        raise ValueError('the actual second-pass report still has findings')
    files = ['source-transcript.md','study-notes.md','source-target-map.json']
    current = {name:sha(project / name) for name in files}
    for phase in ['document_hashes_start','document_hashes_end']:
        if any(report[phase].get(name) != value for name,value in current.items()):
            raise ValueError(f'{phase} is not the current three-file content version')
    required = {'source_unit_ids':[x['id'] for x in ledger['source_units']],
                'target_unit_ids':[x['id'] for x in ledger['target_units']],
                'recovery_ids':[x['id'] for x in ledger['recoveries']],
                'issue_ids':[x['id'] for x in ledger['issues']]}
    for key, ids in required.items():
        reviewed = report['reviewed_scope'][key]
        if len(reviewed) != len(set(reviewed)) or set(reviewed) != set(ids):
            raise ValueError(f'actual second-pass scope is incomplete: {key}')
    accepted = report['accepted_recovery_ids']
    if len(accepted) != len(set(accepted)) or set(accepted) != set(required['recovery_ids']):
        raise ValueError('every proposed recovery needs an explicit actual acceptance')
    expected_pages = {p['id'] for p in manifest['pages']}
    expected_regions = {r['id'] for p in manifest['pages'] for r in p['regions']}
    for field, key, expected in [('pages','page_id',expected_pages),
                                 ('regions','region_id',expected_regions)]:
        observations = report[field]
        if len(observations) != len(expected) or {x[key] for x in observations} != expected:
            raise ValueError('actual page/region observations are incomplete')
        if any(x['assessment'] == 'unresolved' or len(x['observation'].strip()) < 8
               for x in observations):
            raise ValueError('page/region observations remain incomplete or unresolved')
    def register(path, proposed_id):
        relative = str(path.relative_to(project))
        for item in plan['evidence_artifacts']:
            if item['path'] == relative:
                return item['id']
        if any(item['id'] == proposed_id for item in plan['evidence_artifacts']):
            raise ValueError('review evidence ID collision')
        plan['evidence_artifacts'].append({'id':proposed_id,'path':relative,
                                          'kind':'evidence','format':'text'})
        return proposed_id
    report_id = register(report_path,'accepted-second-pass-report')
    narrative_id = register(narrative_path,'accepted-second-pass-narrative')
    evidence = ['artifact:'+report_id,'artifact:'+narrative_id]
    if any(item['pass'] == 2 for item in plan['observations']):
        raise ValueError('pass 2 already exists; do not silently replace a prior review')
    plan['observations'].append({'pass':2,'reviewer_id':reviewer,'session_id':session,
                                'path':args.report,'artifact_id':report_id})
    selected = {}
    for recovery in plan['recoveries']:
        recovery['status'] = 'resolved'
        recovery['reviewer_id'], recovery['session_id'] = reviewer, session
        recovery['evidence_ids'] = sorted(set(recovery['evidence_ids'] + evidence))
        for key in ['forward_validation','backward_validation','return_to_image']:
            recovery[key]['evidence_ids'] = sorted(set(recovery[key]['evidence_ids'] + evidence))
        chosen = next(c['text'] for c in recovery['candidates']
                      if c['id'] == recovery['selected_candidate_id'])
        selected[recovery['id']] = chosen
    for issue in plan['issues']:
        linked = [i for i in issue['related_ids'] if i in selected]
        if not linked:
            raise ValueError('an issue lacks an explicitly accepted recovery')
        issue['status'] = 'resolved'
        issue['evidence_ids'] = sorted(set(issue['evidence_ids'] + evidence))
        issue['resolution'] = (f'非作者 {reviewer} 在两份当前正文及完整映射上实查接受：' +
                               '；'.join(selected[i] for i in linked) +
                               '。置信度、备选和恢复范围见所绑定的独立报告。')
    for source in plan['sources']:
        source['status'] = 'resolved'
    for key in ['transcription_blocks','study_blocks']:
        for block in plan[key]:
            block['status'] = 'resolved'
    plan_path.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    result = build(project)
    if current != {name:sha(project / name) for name in files}:
        raise RuntimeError('binding a review unexpectedly changed reviewed content')
    print(json.dumps({**result,'actual_reviewer':reviewer,'document_hashes_unchanged':True},
                     ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
