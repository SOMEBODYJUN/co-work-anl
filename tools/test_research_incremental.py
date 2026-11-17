"""Research backflow cannot overwrite a registry advanced since its review."""
import json
from pathlib import Path
import tempfile
import unittest

import research_runtime as runtime


class BackflowGuardTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(dir=Path.cwd())
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.registry = {'schema': 2, 'objects': [], 'materials': [], 'edge_files': [],
                         'registration_batches': [], 'baseline': {'historical': 'unchanged'}}
        runtime._write_json(self.root / runtime.REGISTRY, self.registry)

    def candidate(self, base=None):
        current = self.root / runtime.REGISTRY
        candidate = dict(self.registry, backflow_guard={'registry': runtime.REGISTRY,
                            'base_sha256': runtime.digest(current.read_bytes()) if base is None else base})
        runtime._write_json(self.root / 'candidate.json', candidate)
        return candidate

    def test_registry_advanced_after_candidate_does_not_lose_peer_data(self):
        self.candidate()
        newer = dict(self.registry, peer_increment='Preserve this independently published result')
        runtime._write_json(self.root / runtime.REGISTRY, newer)
        before = (self.root / runtime.REGISTRY).read_bytes()
        with self.assertRaisesRegex(ValueError, 'Backflow base changed'):
            runtime.register(self.root, 'candidate.json')
        self.assertEqual((self.root / runtime.REGISTRY).read_bytes(), before)

    def test_guard_is_not_a_second_canonical_fact_store(self):
        self.candidate()
        runtime.register(self.root, 'candidate.json')
        self.assertEqual(json.loads((self.root / runtime.REGISTRY).read_text()), self.registry)

    def test_candidate_for_one_registry_cannot_be_installed_in_another(self):
        self.candidate()
        runtime._write_json(self.root / 'alternate.json', self.registry)
        with self.assertRaisesRegex(ValueError, 'exact canonical registry path'):
            runtime.register(self.root, 'candidate.json', 'alternate.json')

    def test_empty_project_can_register_once_and_reject_repeated_old_base(self):
        (self.root / runtime.REGISTRY).unlink()
        candidate = dict(self.registry, backflow_guard={'registry': runtime.REGISTRY, 'base_sha256': None})
        runtime._write_json(self.root / 'candidate.json', candidate)
        runtime.register(self.root, 'candidate.json')
        with self.assertRaisesRegex(ValueError, 'Backflow base changed'):
            runtime.register(self.root, 'candidate.json')


class DraftEndpointTests(unittest.TestCase):
    def test_new_edge_can_be_bound_and_checked_before_review_without_registering_objects(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as temporary:
            root = Path(temporary)
            body = root / 'proof.md'
            body.write_text('# A\nThe premise.\n# B\nThe exact consequence and joint argument.\n')
            reference = {'path': 'proof.md', 'sha256': runtime.digest(body.read_bytes())}
            objects = [{
                'object_id': oid, 'version': 1, 'title': oid, 'kind': 'lemma', 'truth_status': 'proved',
                'statement': 'Precise ' + oid, 'model': 'same model', 'quantifiers': 'every instance',
                'assumptions': [], 'scope': 'full stated domain', 'objections': 'Declared reviewed scope',
                'body': dict(reference, section=oid), 'evidence': [], 'sources': ['local exact argument']
            } for oid in ('A', 'B')]
            batch = {'schema': 2, 'objects': objects, 'edge_files': [],
                     'materials': [dict(reference, disposition='objects', object_ids=['A', 'B'],
                                        reason='Two explicit mathematical sections in one body')]}
            runtime._write_json(root / 'batch.json', batch)
            edge = {'edge_id': 'new-edge', 'kind': 'implies', 'status': 'accepted',
                    'source_ids': ['A'], 'target_ids': ['B'], 'premises_mode': 'all',
                    'conditions': 'Same original instance', 'explanation': 'The complete stated argument',
                    'roles': {'A': 'full premise', 'B': 'consequence'}, 'scope': 'full domain',
                    'evidence': [reference], 'relation_mode': 'unconditional',
                    'whole_result': 'A gives the whole B', 'reviewed_by': 'independent reader',
                    'review_note': 'Exact statement and argument checked'}
            _, merged = runtime.edge_context(root, batch_file='batch.json')
            edge.update(runtime.edge_bindings(root, edge, merged))
            runtime._write_json(root / 'edge.json', edge)
            outcome = runtime.check_edge(root, 'edge.json', batch_file='batch.json')
            self.assertEqual(outcome['draft_batch'], 'batch.json')
            self.assertFalse(outcome['canonical_registry_modified'])
            self.assertFalse((root / runtime.REGISTRY).exists())
            with self.assertRaises(FileNotFoundError):
                runtime.check_edge(root, 'edge.json')


if __name__ == '__main__':
    unittest.main()
