"""Registration completion precedes graph construction and never rewrites input."""
import copy
import json
import unittest
import test_research_runtime as fixtures
import registration
import research_runtime as runtime


class RegistrationTests(unittest.TestCase):
    setUp = fixtures.ResearchRuntimeTests.setUp
    write = fixtures.ResearchRuntimeTests.write
    write_json = fixtures.ResearchRuntimeTests.write_json
    git = fixtures.ResearchRuntimeTests.git
    ref = fixtures.ResearchRuntimeTests.ref
    bind = fixtures.ResearchRuntimeTests.bind

    def test_registration_final_does_not_need_a_graph_or_edges(self):
        (self.root / 'map/coverage.json').unlink()
        (self.root / 'map/edges/AB-C.json').unlink()
        report = registration.check(self.root, final=True)
        self.assertFalse(report['graph_required'])
        with self.assertRaises(FileNotFoundError): runtime.check(self.root, final=True)

    def test_freeze_requires_all_current_formal_paths_for_repository_scope(self):
        self.write('archives/demo/state/new.md', '# New independent claim\n')
        self.write_json('research/inputs.json', {'scope': 'repository', 'coverage_note': 'Reviewed output list', 'materials': [self.ref(self.body)]})
        with self.assertRaisesRegex(ValueError, 'omits'): registration.freeze(self.root, 'research/inputs.json', 'research/new-baseline.json')

    def test_frozen_input_is_immutable_and_source_bytes_are_untouched(self):
        original = (self.root / self.body).read_bytes()
        inputs = {'scope': 'repository', 'coverage_note': 'Actual reviewed stage-2 output', 'materials': [self.ref(self.body)]}
        self.write_json('research/inputs.json', inputs)
        registration.freeze(self.root, 'research/inputs.json', 'research/new-baseline.json')
        self.assertEqual(registration.freeze(self.root, 'research/inputs.json', 'research/new-baseline.json')['status'], 'already-frozen')
        inputs['coverage_note'] = 'Another selection'; self.write_json('research/inputs.json', inputs)
        with self.assertRaisesRegex(ValueError, 'overwriting'): registration.freeze(self.root, 'research/inputs.json', 'research/new-baseline.json')
        self.assertEqual((self.root / self.body).read_bytes(), original)

    def manifest(self, records):
        batches = []
        for index, record in enumerate(records):
            name = 'research/registration/batches/b%d.json' % index
            self.write_json(name, record)
            batches.append({'batch_id': 'b%d' % index, 'record': self.ref(name)})
        self.write_json('research/registration/batches.json', {'baseline': self.data['baseline'], 'batches': batches})
        return 'research/registration/batches.json'

    def test_batch_composition_retains_one_page_many_objects(self):
        shard = dict(copy.deepcopy(self.data), edge_files=[])
        result = registration.compose(self.root, self.manifest([shard]), 'research/candidate.json')
        self.assertEqual(result['objects'], 3)
        self.assertEqual(registration.check(self.root, 'research/candidate.json', final=True)['materials'], 1)
        self.assertEqual(runtime.load(self.root)[0], self.data)

    def test_conflicting_object_id_is_not_silently_merged(self):
        one = dict(copy.deepcopy(self.data), edge_files=[])
        two = copy.deepcopy(one); two['objects'][0]['statement'] = 'Different quantifier or claim'
        with self.assertRaisesRegex(ValueError, 'Conflicting object'):
            registration.compose(self.root, self.manifest([one, two]), 'research/candidate.json')

    def test_missing_material_and_pending_disposition_block_completion(self):
        empty = dict(self.data, objects=[], materials=[])
        self.write_json('research/empty.json', empty)
        with self.assertRaisesRegex(ValueError, 'incomplete'): registration.check(self.root, 'research/empty.json', final=True)
        self.data['materials'][0]['disposition'] = 'needs-decision'; self.write_json(runtime.REGISTRY, self.data)
        with self.assertRaisesRegex(ValueError, 'pending'): registration.check(self.root, final=True)

    def test_new_ids_are_unique_and_do_not_change_existing_ids(self):
        generated = registration.new_ids(20)['object_ids']
        self.assertEqual(len(set(generated)), 20)
        self.assertTrue(all(i.startswith('M-') for i in generated))
        self.assertEqual([o['object_id'] for o in runtime.load(self.root)[0]['objects']], ['A', 'B', 'C'])

    def test_new_formal_output_after_freeze_requires_explicit_reconciliation(self):
        self.write('archives/demo/state/later.md', '# Later stage-2 output\n')
        with self.assertRaisesRegex(ValueError, 'new formal paths'): registration.check(self.root, final=True)


if __name__ == '__main__': unittest.main()
