#!/usr/bin/env python3
"""Pin already-read, independently frozen records before the CA07 edit.

The required final adversarial digest must come from that actual reviewer.
This file only records evidence ownership and Boss-authored merge choices.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import json

ROOT = Path(__file__).resolve().parents[3]
P = ROOT / 'work/notes-f86b97e0dd5e406a/notes/CA07/project'
OUT = P / 'audit/second-pass-2-merge'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--adversarial-report-sha', required=True)
    parser.add_argument('--boss-read-frozen-reports', action='store_true', required=True)
    args = parser.parse_args()
    expected = {
        'math':'2e71ef0496af8f6d583cfd09d00d8f605921f0666c2dc65e6d3b98e6060aa977',
        'visual':'23359df57dc063f0e0a124efb06fb84608edad493cd3dba3003b165b354d0575',
        'adversarial':args.adversarial_report_sha,
    }
    additional = {
        'math':['second-pass-2-edge-addendum'],
        'visual':['second-pass-2-observation-errata'],
        'adversarial':[],
    }
    expected_aux = {
        'proposals/ca07_math/second-pass-2-edge-addendum/edge-check.json':'aa800e54b6dc5334e077159b0d29d403fe78ec309d510321866d0bdbed54826d',
        'proposals/ca07_visual/second-pass-2-observation-errata/erratum.json':'7babfce21f6a1cfc119c3609e87bd05e6c049c5d7c13501f2178d62f0489ab96',
        'proposals/ca07_visual/second-pass-2-observation-errata/reconciled-source-observations.json':'442251e292633075a8f4fae2610abaf03fb44d78e41ae31da5e63286f0d1dba2',
    }
    for path, digest in expected_aux.items():
        assert sha(P / path) == digest, path
    draft = load(OUT / 'boss-decisions-draft.json')
    assert draft['status'] == 'draft awaiting all three independent frozen records'
    for path, digest in draft['document_hashes_before'].items():
        assert sha(P / path) == digest, path
    records, text_files, crop_indexes = [], [], []
    for role, digest in expected.items():
        directory = P / f'proposals/ca07_{role}/second-pass-2'
        report_path = directory / 'second-pass-report.json'
        assert sha(report_path) == digest, role
        report = load(report_path)
        assert report['reviewer_id'] == report['session_id'] == f'/root/ca07_{role}'
        assert report['document_hashes_start'] == report['document_hashes_end'] == draft['document_hashes_before']
        assert report['findings'], 'these records document findings; they are not acceptance records'
        directories = [directory] + [directory.parent / name for name in additional[role]]
        files = {}
        for folder in directories:
            for path in sorted(folder.rglob('*')):
                if not path.is_file() or path.suffix not in ('.json','.md','.jsonl','.png'):
                    continue
                relative = str(path.relative_to(P))
                files[relative] = sha(path)
                if path.suffix != '.png':
                    text_files.append(relative)
                if path.name == 'crop-index.json':
                    crop_indexes.append(relative)
        records.append({'reviewer_id':report['reviewer_id'],'files':files,
            'main_report_sha256':digest,'finding_count':len(report['findings']),
            'scope_counts':{k:len(v) for k,v in report['reviewed_scope'].items()},
            'boss_read_scope':'all findings, candidates and directional tests, all recovery judgments, page/region records, and declared source/target checks',
            'status':'frozen actual independent review with findings; never bound as a pass'})
    receipt = {'boss_id':'BossNotes-2ff3215d6446','note_id':'CA07',
        'boss_read_all_independent_records':True,'document_hashes_before':draft['document_hashes_before'],
        'records':records,
        'reconciliation_notes':[
            'Math full report original R008 first-operator intersection wording is superseded only by the separately frozen actual 1200 dpi erratum.',
            'Math R051 original acceptance is superseded for direct-premise provenance by its separately frozen edge addendum.',
            'Visual active source observations use the separately frozen five-field erratum; unchanged observations explicitly retain their real second-pass-2 viewing provenance.',
            'The three complete reviews contain findings. None is used to set content_resolved or to supply final reviews.']}
    save(OUT / 'independent-frozen-receipts.json', receipt)
    decisions = copy.deepcopy(draft)
    decisions['status'] = 'authored after all three independent records'
    decisions['source_observation_record'] = 'proposals/ca07_visual/second-pass-2-observation-errata/reconciled-source-observations.json'
    decisions['independent_frozen_receipt'] = 'audit/second-pass-2-merge/independent-frozen-receipts.json'
    decisions['cross_report_resolution'] = [
        'Use conservative literal-shape annotation with an explicitly separate mathematical interpretation; no unresolved glyph is described as perfectly legible.',
        'R008: preserve only two source-supported operator locations; label first separated strokes, middle two marks, conditional exponent and terminal n/0 shape.',
        'R012/R018: qualify each distinct middle-mark sequence at its own physical location.',
        'R034/R035: qualify set delimiters and both open operator letters, preserve the isolated bracket point, and distinguish the image algebra from the polynomial ring.',
        'R058: preserve the leftward source shape; use the later membership relation to recover the scalar domain, not an invented ring homomorphism.',
        'Add each direct semantic edge at the target that uses it. Keep R051 minimal direct validation sources U22/U23/U25/U26 while S007 separately links the full definition.']
    save(OUT / 'boss-decisions.json', decisions)
    root6 = P / 'audit/boss-recovery-6'
    text_files += [str(path.relative_to(P)) for path in sorted(root6.glob('*.json'))]
    crop_indexes.append('audit/boss-recovery-6/crop-index.json')
    text_files += ['audit/second-pass-merge/boss-postmerge-inspection.json',
                   'audit/second-pass-2-merge/independent-frozen-receipts.json',
                   'audit/second-pass-2-merge/boss-decisions.json']
    save(OUT / 'evidence-inputs.json', {'text_files':sorted(set(text_files)),
        'crop_indexes':sorted(set(crop_indexes))})
    print(json.dumps({'frozen_reviewers':[r['reviewer_id'] for r in records],
        'finding_counts':[r['finding_count'] for r in records],
        'target_edits':len(decisions['target_edits']),
        'amended_recoveries':len(decisions['recoveries']),
        'new_recoveries':len(decisions['new_recoveries']),
        'text_evidence_inputs':len(set(text_files)),'crop_indexes':len(set(crop_indexes)),
        'formal_content_edited':False},ensure_ascii=False))


if __name__ == '__main__':
    main()
