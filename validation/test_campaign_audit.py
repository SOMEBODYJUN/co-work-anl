"""Synthetic-only regressions for the explicitly requested fixed-trio protocol."""
from pathlib import Path
import json
import sys
import tempfile
import unittest

import fitz
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from campaign_audit import CampaignAuditor, standard
from selftest import make_fixture, reseal


class FixedTrioTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='campaign-audit-test-', dir=ROOT.parent)
        self.manifest_path, self.ledger_path = make_fixture(Path(self.temp.name))
        self.project = self.ledger_path.parent
        self.manifest = standard.load_json(self.manifest_path)
        self.ledger = standard.load_json(self.ledger_path)
        self.ids = ['synthetic-trio-visual', 'synthetic-trio-math', 'synthetic-trio-audit']
        participants = {
            'note_id': 'SYNTHETIC', 'boss_id': 'synthetic-author',
            'subagents': [{'id': value} for value in self.ids],
            'model': 'gpt-6.2-sol', 'reasoning_effort': 'max',
            'authorization': 'Synthetic explicit fixed-trio authorization for test coverage only.',
            'independence_scope': 'Synthetic returning participants, not fresh-reviewer evidence.',
        }
        self.auth = self.project / 'synthetic-authorization.json'
        self.auth.write_text(json.dumps(participants) + '\n')
        self.ledger['artifacts'].append({'id': 'trio-authorization', 'path': self.auth.name,
            'sha256': standard.sha256_file(self.auth), 'kind': 'evidence', 'format': 'text'})
        self.ledger['review_policy'] = {'mode': 'user_requested_fixed_trio', 'note_id': 'SYNTHETIC',
            'boss_id': 'synthetic-author', 'authorization_artifact_id': 'trio-authorization',
            'reviewer_ids': self.ids}
        for check in self.ledger['page_checks'] + self.ledger['region_checks']:
            check['reviewer_id'] = self.ids[0 if check['pass'] == 1 else 2]
            check['session_id'] = check['reviewer_id']
        for recovery in self.ledger['recoveries']:
            recovery['reviewer_id'] = self.ids[2]
            recovery['session_id'] = self.ids[2]
        self.ledger['authors'].append(self.ids[0])
        for record, participant in zip(self.ledger['final_rounds'], self.ids):
            record['reviewer_id'] = participant
            record['session_id'] = participant

    def tearDown(self):
        self.temp.cleanup()

    def report(self):
        reseal(self.manifest_path, self.ledger_path, self.ledger)
        return CampaignAuditor(self.manifest_path, self.ledger_path).run()

    def assert_blocked(self, report, code):
        self.assertFalse(report['audit_pass'], report)
        self.assertTrue(any(e.startswith(code + ':') for e in report['structural_errors']), report)

    def test_fixed_trio_reports_actual_repeated_participation(self):
        report = self.report()
        self.assertTrue(report['audit_pass'], report)
        self.assertTrue(report['content_resolved'], report)
        self.assertFalse(report['fresh_final_reviewers_claimed'])
        self.assertEqual(report['review_protocol'], 'user_requested_fixed_trio')
        self.assertFalse(report['visual_reading_proven'])

    def test_original_fresh_reviewer_policy_is_unchanged(self):
        del self.ledger['review_policy']
        reseal(self.manifest_path, self.ledger_path, self.ledger)
        report = standard.Auditor(self.manifest_path, self.ledger_path).run()
        self.assert_blocked(report, 'ROUND_REVIEWER')

    def test_same_agent_cannot_fill_two_final_rounds(self):
        self.ledger['final_rounds'][2]['reviewer_id'] = self.ids[0]
        self.assert_blocked(self.report(), 'ROUND_REVIEWER')

    def test_unregistered_final_agent_rejected(self):
        self.ledger['final_rounds'][2]['reviewer_id'] = 'synthetic-unregistered'
        self.assert_blocked(self.report(), 'ROUND_REVIEWER')

    def test_authorization_cannot_register_different_trio(self):
        record = json.loads(self.auth.read_text())
        record['subagents'][2]['id'] = 'synthetic-different'
        self.auth.write_text(json.dumps(record))
        self.ledger['artifacts'][-1]['sha256'] = standard.sha256_file(self.auth)
        self.assert_blocked(self.report(), 'TRIO_AUTHORIZATION')

    def test_second_pass_still_requires_a_different_nonauthor(self):
        for check in self.ledger['region_checks']:
            if check['pass'] == 2:
                check['reviewer_id'] = self.ids[0]
        self.assert_blocked(self.report(), 'AUTHOR_SECOND_REVIEW')

    def test_an_open_issue_cannot_be_certified(self):
        self.ledger['issues'].append({'id': 'open-synthetic', 'status': 'open',
            'description': 'Synthetic unresolved reading must keep the gate open.',
            'related_ids': ['s01'], 'evidence_ids': ['image:p0001'], 'resolution': ''})
        report = self.report()
        self.assertTrue(report['audit_pass'], report)
        self.assertFalse(report['content_resolved'])
        self.assertEqual(report['unresolved_count'], 1)

    def test_incomplete_scope_still_fails(self):
        self.report()
        ledger = standard.load_json(self.ledger_path)
        ledger['final_rounds'][-1]['scope']['region_ids'].pop()
        ledger['final_rounds'][-1]['record_sha256'] = standard.round_hash(ledger['final_rounds'][-1])
        self.ledger_path.write_text(json.dumps(ledger))
        self.assert_blocked(CampaignAuditor(self.manifest_path, self.ledger_path).run(), 'ROUND_SCOPE')

    def test_updated_body_hash_cannot_rebind_old_review(self):
        self.report()
        ledger = standard.load_json(self.ledger_path)
        body = self.project / 'study.md'
        body.write_text(body.read_text().replace('infer', 'deduce'))
        next(a for a in ledger['artifacts'] if a['id'] == 'study')['sha256'] = standard.sha256_file(body)
        for unit in ledger['target_units']:
            if unit['artifact_id'] == 'study':
                unit['text_sha256'] = standard.text_hash(body, unit['start_line'], unit['end_line'])
        self.ledger_path.write_text(json.dumps(ledger))
        self.assert_blocked(CampaignAuditor(self.manifest_path, self.ledger_path).run(), 'ROUND_SNAPSHOT')

    def test_high_resolution_crop_is_rerendered_and_pixel_verified(self):
        path = self.project / 'synthetic-800.png'
        box = [5, 5, 55, 25]
        with fitz.open(self.project / 'source.pdf') as doc:
            doc[0].get_pixmap(dpi=800, clip=fitz.Rect(*box), colorspace=fitz.csRGB, alpha=False).save(path)
        artifact = {'id': 'synthetic-800', 'path': path.name, 'sha256': standard.sha256_file(path),
            'kind': 'evidence', 'format': 'image',
            'source_crop': {'page_id': 'p0001', 'bbox_px': box, 'dpi': 800}}
        self.ledger['artifacts'].append(artifact)
        self.assertTrue(self.report()['audit_pass'])
        with Image.open(path) as image:
            changed = image.convert('RGB')
        changed.putpixel((10, 10), (1, 2, 3))
        changed.save(path)
        artifact['sha256'] = standard.sha256_file(path)
        self.assert_blocked(self.report(), 'ARTIFACT_INVALID')

    def test_expanded_pdf_viewport_is_reproducible_and_cannot_hide_pixel_edits(self):
        path = self.project / 'synthetic-outside-media.png'
        with fitz.open(self.project / 'source.pdf') as doc:
            box = list(doc[0].mediabox)
            box[0] -= 10
            doc[0].set_mediabox(fitz.Rect(box))
            clip = [0, 0, 50, 25]
            doc[0].get_pixmap(dpi=800, clip=fitz.Rect(clip),
                             colorspace=fitz.csRGB, alpha=False).save(path)
        artifact = {'id': 'synthetic-viewport', 'path': path.name,
            'sha256': standard.sha256_file(path), 'kind': 'evidence', 'format': 'image',
            'pdf_viewport': {'page_id': 'p0001', 'mediabox_pdf_pt': box,
                             'clip_pdf_pt': clip, 'dpi': 800}}
        self.ledger['artifacts'].append(artifact)
        self.assertTrue(self.report()['audit_pass'])
        with Image.open(path) as image:
            changed = image.convert('RGB')
        changed.putpixel((10, 10), (1, 2, 3))
        changed.save(path)
        artifact['sha256'] = standard.sha256_file(path)
        self.assert_blocked(self.report(), 'ARTIFACT_INVALID')


if __name__ == '__main__':
    unittest.main(verbosity=2)
