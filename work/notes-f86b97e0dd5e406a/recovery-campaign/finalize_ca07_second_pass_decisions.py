#!/usr/bin/env python3
"""Serialize the Boss's read and adjudication of frozen CA07 appendices.

The decisions below were made after actual independent records and original
images were read. This script only copies those records, hashes files and
assembles the explicitly chosen evidence. It performs no review or completion.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[3]
P = ROOT / 'work/notes-f86b97e0dd5e406a/notes/CA07/project'
OUT = P / 'audit/second-pass-merge'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    pinned = {
        'math': '8d22d6f5d1e9b0ab34e05a152d30a0368925a571f86e2527bc45c2a8f1146263',
        'visual': 'c6c16dd04ab4671e2821f89b701d873511cacebed3dc5fdc62a2dcf9aed20f34',
        'adversarial': 'b80de5221e2a34d1270b52ff1ecb55d9d3baaaf9f9c5e72f499c29735719e9c6',
    }
    errata_dir = P / 'proposals/ca07_visual/post-second-pass-errata'
    assert (errata_dir / 'erratum.json').is_file()
    assert (errata_dir / 'reconciled-source-observations.json').is_file()
    reports, records = {}, []
    for role, expected in pinned.items():
        directory = P / f'proposals/ca07_{role}/post-second-pass-1'
        report = directory / 'literal-recovery.json'
        assert sha(report) == expected, role
        reports[role] = read(report)
        assert len(reports[role]['groups']) == 8
        files = {str(path.relative_to(P)): sha(path)
                 for path in sorted(directory.rglob('*')) if path.is_file()}
        if role == 'visual':
            files.update({str(path.relative_to(P)): sha(path)
                          for path in sorted(errata_dir.rglob('*')) if path.is_file()})
        records.append({'reviewer_id': '/root/ca07_' + role, 'files': files,
            'boss_read_scope': 'All eight structured groups, candidates, forward/backward tests, placements, mappings and observation errata; narrative files are frozen supporting records. Image viewing is recorded separately and is not inferred from hashing.'})
    save(OUT / 'independent-post-receipts.json', {
        'boss_id': 'BossNotes-2ff3215d6446', 'note_id': 'CA07',
        'boss_read_all_independent_records': True,
        'meaning': 'Three actual targeted-recovery appendices were read. These are not a new full second pass and do not accept the revised content.',
        'records': records,
    })

    decisions = read(OUT / 'boss-decisions-draft.json')
    decisions['status'] = 'authored after all three independent records'
    decisions['source_observation_record'] = str((errata_dir / 'reconciled-source-observations.json').relative_to(P))
    decisions['independent_records'] = [f'proposals/ca07_{role}/post-second-pass-1/literal-recovery.json'
                                        for role in pinned]
    replacements = {
        'proposals/ca07_math/second-pass-1/p5-limited-dimension-1200.png':
            'audit/boss-recovery-5/p5-finite-before-k-1200.png',
        'proposals/ca07_math/second-pass-1/p5-limited-generation-comparison-1200.png':
            'audit/boss-recovery-5/p5-finite-comparison-1200.png',
    }

    def group_paths(group):
        return [replacements.get(path, path) for path in group.get('images', group.get('evidence_paths', []))]

    target_changes = {
        5: ['S030', 'S031'], 7: ['T010', 'S030', 'TV-006', 'S031'],
        10: ['T020', 'S011', 'TV-008', 'S012'], 12: ['T022', 'S011'],
        27: ['TV-014'], 29: ['TV-015', 'S026', 'TV-016'], 32: ['S024'],
        33: ['T063', 'S035', 'TV-017', 'S036'], 37: ['T067', 'T069', 'S037', 'TV-018'],
        39: ['TV-019', 'S038'], 43: ['T080', 'S040'], 44: ['T086', 'S042'],
        46: ['T088', 'S040', 'TV-023'], 47: ['T017', 'S009', 'TV-007', 'S010'],
        48: ['T018', 'S009'], 53: ['TV-010'], 54: ['T018', 'S009', 'S012'],
    }

    def target_id(short):
        return ('CA07-TRANSCRIPTION-' if short.startswith('T') else 'CA07-STUDY-') + short[1:]

    for decision in decisions['recoveries']:
        rid = decision['recovery_id']
        evidence = set(decision['evidence_paths'])
        for role, report in reports.items():
            for group in report['groups']:
                if rid in group['recovery_ids']:
                    evidence.add(f'proposals/ca07_{role}/post-second-pass-1/literal-recovery.json')
                    evidence.update(group_paths(group))
                    if role == 'visual':
                        decision['additional_candidates'] = [{
                            'id': f'visual-post-g{group["number"]}-{candidate["id"]}',
                            'text': candidate['text'],
                            'evidence_paths': [f'proposals/ca07_{role}/post-second-pass-1/literal-recovery.json'] + group_paths(group),
                        } for candidate in group['candidates']]
        decision['evidence_paths'] = sorted(evidence)
        decision['related_target_ids'] = [target_id(x) for x in target_changes.get(int(rid[-3:]), [])]
        if rid == 'CA07-R033':
            decision['selected_text'] += '括内分别记较高斜点和另一枚细针点，不将它们合成一处；闭括外小点另计。'
            decision['return_to_image']['observation'] += 'Boss重开U10原生800图，确认括内的较高斜点、横波、另一细针点、短柱与B形各占其位。'
        if rid == 'CA07-R007':
            decision['correction'] += ' T-V006的平方解释也采用同一条件性恢复。'
    for label in decisions['source_labels']:
        if label['source_id'] == 'CA07-P005-U10':
            label['label'] = 'eg.V是有限后另独立上折下竖双回字团（维的上下文恢复），再k；后括内高斜点、横波、另一细针点、短柱与B形缩记，闭括外下方另小点'

    new = decisions['new_recovery']
    new['observation'] = '原生800图和三人各自从原PDF渲染的1200定向图均记录第一个限字左上白区的极淡针点；Boss也重开数学员的1200图核实。该点与限的冠部及左竖分离，保持孤墨，不赋新的字符值。'
    new['problem'] = '第二遍发现P7U10第一个限字左上极淡针点在旧正文中遗漏；三人独立比较孤墨与字内部件等候选后，修订稿就地保留该点及其用途限制，等待当前内容的完整第二遍接受。'
    new_evidence = set(new['evidence_paths'])
    for role, report in reports.items():
        group = report['groups'][6]
        new_evidence.update(group_paths(group))
    new['evidence_paths'] = sorted(new_evidence)
    decisions['boss_image_return'] = {
        'records': ['audit/boss-recovery-5/readonly-observations-4.json',
                    'audit/boss-recovery-5/readonly-observations-5.json',
                    'audit/second-pass-merge/boss-region-recheck.json'],
        'limit': 'Only actual Boss views are claimed; all other independent crop observations remain attributed to their real authors.',
    }
    save(OUT / 'boss-decisions.json', decisions)

    text_files = set()
    for role in pinned:
        for phase in ['second-pass-1', 'post-second-pass-1']:
            directory = P / f'proposals/ca07_{role}/{phase}'
            text_files.update(str(path.relative_to(P)) for path in directory.rglob('*')
                              if path.is_file() and path.suffix in {'.json', '.jsonl', '.md'})
    for directory in [P / 'audit/boss-recovery-5', errata_dir]:
        text_files.update(str(path.relative_to(P)) for path in directory.rglob('*')
                          if path.is_file() and path.suffix in {'.json', '.jsonl', '.md'})
    text_files.update('audit/second-pass-merge/' + name for name in [
        'boss-decisions.json', 'independent-post-receipts.json', 'boss-region-recheck.json', 'evidence-inputs.json'])
    indexes = [
        'audit/boss-recovery-5/crop-index.json',
        'audit/boss-recovery-5/crop-index-additional.json',
        'audit/boss-recovery-5/heading-comparison-index.json',
        'audit/boss-recovery-5/math-renderer-comparison-index.json',
        'proposals/ca07_adversarial/second-pass-1/extra-crops-index.json',
    ] + [f'proposals/ca07_{role}/post-second-pass-1/crop-index.json' for role in pinned]
    save(OUT / 'evidence-inputs.json', {'text_files': sorted(text_files), 'crop_indexes': indexes})
    print(json.dumps({'records': len(records), 'revisions': len(decisions['recoveries']),
        'new_recoveries': 1, 'text_files': len(text_files), 'crop_indexes': len(indexes)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
