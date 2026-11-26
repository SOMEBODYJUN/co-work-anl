"""Apply adjudicated metadata findings from three real current CA07 reviews.

The unchanged prose is not reauthored. No acceptance decision is generated;
the same three reviewers must confirm the actual resulting delta.
"""
from pathlib import Path
import hashlib
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools'))
from build_note_ledger import build
from catalog_note_evidence import catalog
from final_note_reviews import current

P = ROOT / 'work/notes-f86b97e0dd5e406a/notes/CA07/project'
A = P / 'audit/current-review-5-merge'


def load(p):
    return json.loads(p.read_text(encoding='utf-8'))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write(p, obj):
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    assert not (A / 'applied-result.json').exists(), 'immutable one-time merge'
    assert current(P)[-1] == '840ef895e825e4e5abb554db179747ec727623518e73f9b7eca7c954ed3111ef'
    plan, ledger = load(P / 'content-plan.json'), load(P / 'ledger.json')
    hashes = {n: sha(P / n) for n in ('source-transcript.md', 'study-notes.md', 'source-target-map.json')}
    report_shas = {
        'visual': '54c9e3fb8f0d4d59ab7cd110e23056fcaa02404f3e9be513f89dd6bd81cf2e1b',
        'math': 'a5d32a9b9c42db5bde20a5f17a6122fc2906a4f972072855f69bc201188a1ba4',
        'adversarial': '26f23d7558a2f3c8bb62da1e7af42085b8a15ab2e9ed5d36a883a40b4841b993',
    }
    required = {a: {x['id'] for x in ledger[b]} for a,b in
                [('source_unit_ids','source_units'), ('target_unit_ids','target_units'),
                 ('recovery_ids','recoveries'), ('issue_ids','issues')]}
    reviews, files = [], []
    for role, digest in report_shas.items():
        folder = P / f'proposals/ca07_{role}/post-final-current-review-5'
        f = folder / 'second-pass-report.json'
        assert sha(f) == digest
        d = load(f)
        assert d['reviewer_id'] == f'/root/ca07_{role}'
        assert d['document_hashes_start'] == d['document_hashes_end'] == hashes
        for k, ids in required.items():
            assert set(d['reviewed_scope'][k]) == ids
        assert len(d['recovery_reviews']) == 58 and len(d['issue_reviews']) == 58
        assert len(d['pages']) == 8 and len(d['regions']) == 48
        reviews.append({'reviewer_id': d['reviewer_id'], 'path': str(f.relative_to(P)),
                        'sha256': digest, 'findings': d['findings'],
                        'read_by_boss': True,
                        'boss_read_scope': '完整叙述、全部恢复理由、发现、当前实开图观察及较历史变化的页区观察；结构与哈希另作机械核验。'})
        files.extend(str(x.relative_to(P)) for x in sorted(folder.iterdir())
                     if x.is_file() and x.suffix in {'.json','.jsonl','.md'})
    nav = P / 'proposals/ca07_math/post-final-current-review-5/navigation-addendum.json'
    assert sha(nav) == 'e511b74ce95bd068846a55dd97f99ad3992ead412b0dfd7785cfcad27cade71f'
    expected_nav = {
        'CA07-I005': ['CA07-TRANSCRIPTION-V-001'],
        'CA07-I019': ['CA07-TRANSCRIPTION-037', 'CA07-STUDY-016'],
        'CA07-I032': ['CA07-TRANSCRIPTION-060'],
        'CA07-I037': ['CA07-TRANSCRIPTION-068'],
        'CA07-I039': ['CA07-TRANSCRIPTION-072'],
    }
    assert {x['issue_id']: set(x['proposed_related_ids_additions']) for x in load(nav)['issue_target_reviews']} == {k:set(v) for k,v in expected_nav.items()}
    # Independently validate referenced actual image bytes; this is integrity
    # validation, not a claim that this program performs visual interpretation.
    integrity = []
    for role in ['visual','adversarial']:
        folder = P / f'proposals/ca07_{role}/post-final-current-review-5'
        if role == 'visual':
            rows = [json.loads(s) for s in (folder / 'viewed-images.jsonl').read_text().splitlines()]
        else:
            d = load(folder / 'viewed-images.json')
            rows = d['current_opened_native_800'] + d['historically_opened_same_sha_native_800'] + d['historically_opened_same_sha_pages_and_regions_400']
        for row in rows:
            path = row.get('path', row.get('image_path'))
            digest = row.get('sha256', row.get('image_sha256'))
            assert path and digest and sha(P/path) == digest, (role,path)
        integrity.append({'reviewer':role,'image_hashes_verified':len(rows)})
    A.mkdir(parents=True, exist_ok=True)
    for name in ['content-plan.json','ledger.json','source-transcript.md','study-notes.md','source-target-map.json','audit-prefinal-report.json']:
        shutil.copy2(P / name, A / ('before-' + name))
    residual = ROOT / 'work/notes-f86b97e0dd5e406a/recovery-campaign/ca07-current5-residual-check.json'
    shutil.copy2(residual, A / 'boss-original-residual-check.json')
    write(A/'independent-frozen-receipts.json', {
        'candidate_snapshot_sha256':'840ef895e825e4e5abb554db179747ec727623518e73f9b7eca7c954ed3111ef',
        'actual_reviews': reviews, 'image_integrity_checks': integrity,
        'math_navigation_addendum': {'path':str(nav.relative_to(P)), 'sha256':sha(nav),'read_by_boss':True},
        'all_reports_frozen_before_formal_mutation':True,
    })
    old = '首维与M下标为高竖加单右肩；同式×后的n是低圆拱，邻u_k有独立上下两叉；下一行M下也同单肩。'
    new = '首维与M下标为高竖加单右肩；同式×后的n是低圆拱，邻u_k有独立上下两叉；下文P003-U10中取C*式开头的M下标也呈同一单肩形。'
    write(A/'boss-decisions.json', {
        'boss':'BossNotes-2ff3215d6446', 'input_document_hashes':hashes,
        'decisions':[{'record_id':'CA07-R019','field':'return_to_image.observation','before':old,'after':new,
                      'basis':'三人独立完整复核均指出该定位；Boss本轮已实际看P3整页及U06/U10，原始图读记录在boss-original-residual-check.json。'}]
        + [{'record_id':k,'field':'related_ids','add':v,
            'basis':'问题文字明确点名、现正文落点和双向来源映射已实核。Visual实图报告、Math逐目标导航补录及Boss原检查一致。'} for k,v in expected_nav.items()],
        'prose_or_content_edge_changes':False,
        'formal_acceptance_generated':False,
        'remaining_gate':'相同三位实际reviewer核新差异并与自己刚完成的完整复核合并确认，然后建立新终审链。',
    })
    files += ['audit/current-review-5-merge/independent-frozen-receipts.json',
              'audit/current-review-5-merge/boss-decisions.json',
              'audit/current-review-5-merge/boss-original-residual-check.json',
              'audit/current-review-5-merge/math-read-receipt.json']
    indexed = catalog(P, {'text_files':files, 'crop_indexes':[]})
    existing = {x['path'] for x in plan['evidence_artifacts']}
    plan['evidence_artifacts'].extend(x for x in indexed['evidence_artifacts'] if x['path'] not in existing)
    refs = {x['path']:'artifact:'+x['id'] for x in plan['evidence_artifacts']}
    evidence = [refs[x['path']] for x in reviews] + [refs[str(nav.relative_to(P))], refs['audit/current-review-5-merge/boss-decisions.json']]
    rec = next(x for x in plan['recoveries'] if x['id']=='CA07-R019')
    assert rec['return_to_image']['observation'] == old
    rec['return_to_image']['observation'] = new
    rec['return_to_image']['evidence_ids'] = sorted(set(rec['return_to_image']['evidence_ids'] + evidence))
    rec['evidence_ids'] = sorted(set(rec['evidence_ids'] + evidence))
    for issue in plan['issues']:
        if issue['id'] in expected_nav:
            addition = expected_nav[issue['id']]
            assert not set(addition) & set(issue['related_ids'])
            issue['related_ids'] = sorted(set(issue['related_ids'] + addition))
            issue['evidence_ids'] = sorted(set(issue['evidence_ids'] + evidence))
    assert [x['pass'] for x in plan['observations']] == [1]
    write(P/'content-plan.json', plan)
    result = build(P)
    assert hashes == {n:sha(P/n) for n in hashes}
    assert not (P/'audit/final-freeze.json').exists()
    mapping = load(P/'source-target-map.json')
    assert sum(len(x['source_ids']) for x in mapping['target_to_sources']) == 756
    result.update({'document_hashes':hashes,'document_and_mapping_bytes_unchanged':True,
                   'navigation_links_added':6,'recovery_observations_changed':1,
                   'snapshot_sha256':current(P)[-1],
                   'ledger_sha256':sha(P/'ledger.json'),'plan_sha256':sha(P/'content-plan.json'),
                   'formal_acceptance_generated':False})
    write(A/'applied-result.json',result)
    # Stale prefinal failure remains in the archive; run the next active check
    # once the actual current-version nonauthor acceptance has been bound.
    (P/'audit-prefinal-report.json').unlink()
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
