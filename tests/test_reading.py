"""Critical provenance and report-priority regressions; fixtures are synthetic."""
import argparse
import json
from pathlib import Path
import tempfile
import unittest

from cncrisis import engine, reading, runtime


class ReadingTests(unittest.TestCase):
    def test_metadata_is_not_article_body(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, '不是正文'):
                reading.text_blocks(b'{"posts":[{"title":"Only metadata"}]}',
                                    'application/json', Path(directory))

    def test_article_container_excludes_navigation_and_keeps_paragraphs(self):
        html = b'<html><nav>not the argument</nav><article><p>A real argument about economic choices.</p><p>A distinct supporting observation.</p></article></html>'
        with tempfile.TemporaryDirectory() as directory:
            _, _, rows = reading.text_blocks(html, 'text/html', Path(directory))
        self.assertEqual([r['id'] for r in rows], ['p0001', 'p0002'])
        self.assertNotIn('not the argument', str(rows))

    def test_nonexistent_paragraph_and_changed_packet_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = {'question': 'Synthetic test', 'articles': [
                {'id': 'A1', 'paragraphs': [{'id': 'p0001', 'text': 'Synthetic original.'}]}]}
            (root / 'documents.json').write_text(json.dumps(docs))
            (root / 'packet.json').write_text(json.dumps({
                'documents_sha256': reading.sha((root / 'documents.json').read_bytes())}))
            result = json.loads(json.dumps(reading.SCHEMA))
            result['claims'][0]['evidence'][0]['paragraph_ids'] = ['p9999']
            (root / 'result.json').write_text(json.dumps(result))
            checked = reading.validate(root, root / 'result.json')
            self.assertFalse(checked['ok'])
            self.assertIn('p9999', str(checked['issues']))
            (root / 'documents.json').write_text(json.dumps(docs) + '\n')
            self.assertIn('正文已变', str(reading.validate(root, root / 'result.json')['issues']))

    def test_feedback_cannot_use_its_conclusion_as_same_time_premise(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = {'question': 'Synthetic test', 'articles': [
                {'id': 'A1', 'paragraphs': [{'id': 'p0001', 'text': 'Synthetic original.'}]}]}
            (root / 'documents.json').write_text(json.dumps(docs))
            digest = reading.sha((root / 'documents.json').read_bytes())
            (root / 'packet.json').write_text(json.dumps({'documents_sha256': digest}))
            result = json.loads(json.dumps(reading.SCHEMA))
            result['input_documents_sha256'] = digest
            result['mechanisms'][0]['head'] = result['mechanisms'][0]['premises'][0]
            (root / 'result.json').write_text(json.dumps(result))
            issues = reading.validate(root, root / 'result.json')['issues']
            self.assertIn('不能用结论证明自己', str(issues))


class ReportPriorityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.args = argparse.Namespace(workspace=self.root, actor='fixture', profile='report-first')
        runtime.start(self.args)

    def tearDown(self):
        self.tmp.cleanup()

    def stage(self, key):
        file = self.root / (key + '.txt')
        file.write_text('Synthetic provenance fixture: ' + key)
        return engine.stage(argparse.Namespace(workspace=self.root, id=key,
                            files=[file.name], note='Synthetic fixture'))

    def test_report_has_editorial_and_no_calculator_gate(self):
        with engine.Store(self.root) as store:
            store.require()
            self.assertIn('s18_editorial', store.stages())
            self.assertNotIn('s18_calculator', store.stages())
        self.assertNotIn('formal/calculator.html', runtime.REPORT_DELIVERABLES)
        self.assertNotIn('offline_ui', runtime.REPORT_CHECKS)
        self.assertNotIn('household_engine', runtime.REPORT_CHECKS)
        (self.root / 'formal').mkdir()
        (self.root / 'formal/calculator.html').write_text('Unfinished legacy calculator fixture')
        with engine.Store(self.root) as store:
            store.require()
            self.assertEqual(store.untracked_formal(set()), [])

    def test_independent_method_work_survives_unrelated_stage_registration(self):
        self.stage('s01_scope')
        self.stage('s05_methods')  # no need to wait for acquisition
        self.stage('s02_inventory')
        with engine.Store(self.root) as store:
            store.require()
            self.assertIn('s05_methods', store.valid_stages()[0])
        (self.root / 's02_inventory.txt').write_text('Changed inventory fixture')
        with engine.Store(self.root) as store:
            store.require()
            valid, changed = store.valid_stages()
            self.assertIn('s05_methods', valid)
            self.assertIn('s02_inventory', changed)

    def test_rejection_preserves_scope_without_authorising_release(self):
        self.stage('s01_scope')
        result = engine.review(argparse.Namespace(workspace=self.root, verdict='reject',
            files=[], reviewer='independent-fixture', author='fixture', note='Synthetic unresolved point'))
        self.assertIn('s01_scope.txt', result['files'])
        self.assertEqual(result['author'], 'fixture')
        self.assertEqual(result['verdict'], 'reject')
        self.assertFalse(runtime.progress(self.args)['complete'])

    def test_revised_dependency_stays_stale_after_parent_resubmission(self):
        self.stage('s01_scope')
        self.stage('s02_inventory')
        self.stage('s05_methods')
        (self.root / 's02_inventory.txt').write_text('A genuinely revised source inventory')
        engine.stage(argparse.Namespace(workspace=self.root, id='s02_inventory',
            files=['s02_inventory.txt'], note='Changed source coverage'))
        self.stage('s03_acquisition')
        self.stage('s02_inventory')  # a changed upstream receipt
        with engine.Store(self.root) as store:
            store.require()
            valid, changed = store.valid_stages()
            self.assertIn('s05_methods', valid)
            self.assertNotIn('s03_acquisition', valid)
            self.assertIn('dependency was revised', changed['s03_acquisition'])


if __name__ == '__main__':
    unittest.main()
