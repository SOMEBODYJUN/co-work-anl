"""Regression checks for collecting published incremental object versions."""
import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

import map_tasks
import registration
import research_runtime as runtime


class RegistrationVersionHistoryTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(dir=Path.cwd())
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.body = self.write('archives/demo/state/theorem.md', '# Claim\nA precise claim.\n')
        self.proof = self.write('archives/demo/state/proof.md', '# Proof\nAdditional proof.\n')
        self.git('init', '-q')
        self.git('add', '.')
        self.git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'Proof bytes')
        self.baseline = self.write('research/registration/baseline.json', {
            'schema': 1, 'scope': 'partial', 'coverage_note': 'Two exact proof inputs',
            'commit': self.git('rev-parse', 'HEAD').strip(), 'materials': [self.body, self.proof]})
        self.old = dict(object_id='CLAIM-A', version=1, title='Claim A', kind='theorem',
                        truth_status='proved', model='Finite sets', statement='A precise claim',
                        quantifiers='Every finite set', assumptions=[], scope='Finite sets',
                        objections='Mature proof reused', body=self.body, evidence=[], sources=[])
        self.new = dict(self.old, version=2, evidence=[self.proof])
        self.home = 'research/operations/test-registration'
        self.ctx = dict(phase='registration', run='test-registration', home=self.home, config={}, local=True)
        # Put the newer version first in lexical task order.
        self.update = self.task('a-update', [self.new], [self.material(self.body, 'objects'), self.material(self.proof, 'attachment')])
        self.base = self.task('z-base', [self.old], [self.material(self.body, 'objects')])
        self.dependent = self.task('b-dependent', [], [self.material(self.proof, 'attachment')])
        self.registry = self.write(runtime.REGISTRY, {
            'schema': 2, 'baseline': self.baseline, 'objects': [self.old],
            'materials': [self.material(self.body, 'objects')], 'edge_files': [],
            'registration_batches': [{'batch_id': 'z-base', 'record': self.base['receipt']['batch_file']}]})

    def git(self, *args):
        return subprocess.run(['git', *args], cwd=self.root, check=True, capture_output=True, text=True).stdout

    def write(self, name, value):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value if isinstance(value, str) else json.dumps(value), encoding='utf-8')
        return {'path': name, 'sha256': runtime.digest(path.read_bytes())}

    def material(self, ref, disposition):
        return dict(ref, disposition=disposition, object_ids=['CLAIM-A'], reason='Exact mathematical owner')

    def task(self, name, objects, materials):
        batch = self.write('research/registration/batches/' + name + '.json', {
            'schema': 2, 'objects': objects, 'materials': materials, 'edge_files': []})
        row = {'definition': {'task_id': name, 'stage': 'registration', 'baseline': self.baseline,
                             'goal': 'Register exact evidence',
                             'materials': [{k: r[k] for k in ('path', 'sha256')} for r in materials],
                             'write_paths': [batch['path']]},
               'state': 'done', 'owner': 'Boss1',
               'receipt': {'batch_file': batch, 'assets': [batch]}}
        self.write(self.home + '/tasks/' + name + '.json', row)
        return row

    def test_collect_history_then_incrementally_compose(self):
        result = map_tasks.collect(self.root, 'registration', ctx=self.ctx, baseline_ref=self.baseline)
        manifest = self.write('research/registration/manifest.json', dict(
            baseline=self.baseline, batches=result['batches'], mode='incremental', base_registry=self.registry))
        registration.compose(self.root, manifest['path'], 'research/registration/proposed.json')
        data, objects = runtime.load(self.root, 'research/registration/proposed.json')
        self.assertEqual(objects['CLAIM-A'], self.new)
        self.assertEqual(len(data['registration_batches']), 3)
        self.assertEqual(len(data['materials']), 2)

    def test_atomic_completion_still_rejects_two_versions(self):
        deliveries = [(row['definition'], row['receipt']) for row in (self.base, self.update)]
        with self.assertRaisesRegex(ValueError, 'Conflicting mathematical owner'):
            map_tasks._prefetch_done(self.root, deliveries, 'registration')

    def test_same_version_different_content_is_rejected(self):
        conflicting = dict(self.old, statement='A different claim under the same version')
        self.task('c-conflict', [conflicting], [self.material(self.body, 'objects')])
        with self.assertRaisesRegex(ValueError, 'Conflicting mathematical owner'):
            map_tasks.collect(self.root, 'registration', ctx=self.ctx)

    def test_historical_records_are_not_skipped(self):
        corrupted = copy.deepcopy(self.old)
        corrupted['body']['sha256'] = '0' * 64
        self.task('z-base', [corrupted], [self.material(self.body, 'objects')])
        with self.assertRaises(ValueError):
            map_tasks.collect(self.root, 'registration', ctx=self.ctx)


if __name__ == '__main__':
    unittest.main()
