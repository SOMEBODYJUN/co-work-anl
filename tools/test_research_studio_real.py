"""Exercise adoption against this repository's actual SUMmin edge semantics.

These are structural regression fixtures, not new mathematical research or
independent proof reviews. The temporary project is removed after each test.
"""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

import research_frontier as frontier
import research_runtime as runtime
import research_studio as studio


EQUIVALENCE = 'boss3-uniform-summin-full-budget-equivalence-3313f41b4a46c9dc'
CONTRIBUTION = 'boss5-all-spe-summin-budget-7383c8bf44f753cc'


class RealSUMminTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = Path(__file__).resolve().parents[1]
        path = cls.source / runtime.REGISTRY
        if not path.is_file():
            raise unittest.SkipTest('An exported empty project has no source-project mathematics')
        data = json.loads(path.read_text())
        cls.selected = {}
        for name in data['edge_files']:
            edge = json.loads((cls.source / name).read_text())
            if edge['edge_id'] in {EQUIVALENCE, CONTRIBUTION}:
                cls.selected[edge['edge_id']] = (name, edge)
        if len(cls.selected) != 2:
            raise unittest.SkipTest('This project does not contain the two SUMmin regression endpoints')
        cls.catalog = {obj['object_id']: obj for obj in data['objects']}

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(dir=Path.cwd())
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        subprocess.run(['git', 'init', '-q', '-b', 'research'], cwd=self.root, check=True)
        subprocess.run(['git', 'config', 'wcg.actor', 'Boss2'], cwd=self.root, check=True)
        subprocess.run(['git', '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
                        'commit', '--allow-empty', '-qm', 'Structural fixture only'], cwd=self.root, check=True)
        endpoints = {oid for _, edge in self.selected.values()
                     for oid in edge['source_ids'] + edge['target_ids']}
        refs = [ref for _, edge in self.selected.values() for ref in edge['evidence']]
        refs += [ref for oid in endpoints for ref in [self.catalog[oid]['body'], *self.catalog[oid]['evidence']]]
        names = {ref['path'] for ref in refs} | {name for name, _ in self.selected.values()}
        for name in names:
            destination = self.root / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(self.source / name, destination)
        materials = {}
        for oid in endpoints:
            obj = self.catalog[oid]
            for ref in [obj['body'], *obj['evidence']]:
                row = materials.setdefault(ref['path'], {'path': ref['path'], 'sha256': ref['sha256'],
                                  'disposition': 'attachment', 'object_ids': [], 'reason': 'Selected actual regression evidence'})
                if oid not in row['object_ids']:
                    row['object_ids'].append(oid)
                if ref == obj['body']:
                    row['disposition'] = 'objects'
        data = {'schema': 2, 'objects': [self.catalog[oid] for oid in sorted(endpoints)],
                'materials': list(materials.values()), 'edge_files': [name for name, _ in self.selected.values()]}
        runtime._write_json(self.root / runtime.REGISTRY, data)
        target = self.catalog[self.selected[EQUIVALENCE][1]['target_ids'][0]]['body']
        spec = {'problem_id': 'structural-consumption-fixture', 'problem': target,
                'definitions': [], 'obstacles': [], 'seed_ids': []}
        runtime._write_json(self.root / 'spec.json', spec)
        studio.init(self.root, 'fixture', 'spec.json', expect_branch='research')
        self.spec_pin = runtime.pin(spec)

    def application(self, eid):
        _, edge = self.selected[eid]
        proof = edge['evidence'][0]
        partial = 'contribution' in edge
        debt = [] if partial else ['uniform-budget-unproved']
        record = {'application_id': 'consume-' + ('family' if partial else 'equivalence'),
                  'line': 'informed-a', 'problem_spec_pin': self.spec_pin, 'edge_id': eid,
                  'edge_declaration_pin': runtime.pin(edge), 'direction': 'forward',
                  'object_pins': {oid: runtime.pin(self.catalog[oid])
                                  for oid in edge['source_ids'] + edge['target_ids']},
                  'premise_bindings': [],
                  'source_to_target_mapping': 'The same original model, complete ordered history, sigma, actual prefix and independent p; fixture mirrors the exact edge scope.',
                  'actual_result': edge.get('whole_result', edge.get('contribution', {}).get('result')),
                  'remaining': edge.get('contribution', {}).get('remaining', 'The universal budget premise remains unproved.'),
                  'evidence_refs': edge['evidence'], 'conditions_text': edge['conditions'],
                  'bridge_obligation': {'state': 'global-whole-argument-applies',
                                        'statement': edge['explanation'], 'proof_ref': proof},
                  'condition_discharge': [{'condition': edge['conditions'], 'argument': 'Exact original relation scope is retained in this structural fixture.',
                                           'state': 'established', 'proof_ref': proof}],
                  'applicability': {'model': 'Original unit-customer CA model',
                                    'quantifiers': 'Exactly the selected edge quantifiers', 'scope': edge['scope']},
                  'result_scope': 'contribution' if partial else 'whole',
                  'depends_on_applications': [], 'inherited_unpaid_obligation_ids': [],
                  'discharged_obligations': [], 'unpaid_obligation_ids': debt}
        for oid in edge['source_ids']:
            binding = {'source_id': oid, 'source_pin': runtime.pin(self.catalog[oid]),
                       'local_statement': self.catalog[oid]['statement'],
                       'applicability': 'Same original source and the exact conditions of this edge.'}
            if partial:
                binding.update(state='established-here', proof_ref=self.catalog[oid]['body'])
            else:
                binding.update(state='open-obligation', obligation_id=debt[0])
            record['premise_bindings'].append(binding)
        if partial:
            record['target_remaining'] = {'statement': edge['contribution']['remaining'],
                                          'obligation_id': 'general-input-budget'}
        return record

    def adopt(self, record):
        name = 'research/workspaces/fixture/informed-a/application.json'
        runtime._write_json(self.root / name, record)
        return studio.adopt(self.root, 'fixture', name)

    def test_real_open_equivalence_preserves_the_unproved_budget(self):
        result = self.adopt(self.application(EQUIVALENCE))
        self.assertIn('uniform-budget-unproved', result['unpaid_obligation_ids'])
        self.assertEqual(result['status'], 'application-recorded-not-a-proof')

    def test_real_open_equivalence_frontier_has_no_self_funded_base(self):
        edge = self.selected[EQUIVALENCE][1]
        endpoints = set(edge['source_ids'] + edge['target_ids'])
        context = runtime.context(self.root, edge['target_ids'], edge_ids=[EQUIVALENCE])
        report = frontier.frontier_report(context)
        self.assertFalse(endpoints.intersection(report['declared_bases']))
        self.assertFalse(endpoints.intersection(report['structural_assuming_conditions_closure']))
        cycle = next(row for row in report['cyclic_dependency_components']
                     if endpoints <= set(row['object_ids']))
        self.assertFalse(cycle['self_payment_allowed'])
        self.assertTrue(endpoints <= set(cycle['unresolved_object_ids']))

    def test_real_two_source_contribution_keeps_scope_and_refuses_missing_premise(self):
        record = self.application(CONTRIBUTION)
        outcome = self.adopt(record)
        self.assertEqual(outcome['result_scope'], 'contribution')
        missing = copy.deepcopy(record)
        missing['premise_bindings'].pop()
        with self.assertRaisesRegex(ValueError, 'Every ALL premise'):
            self.adopt(missing)
        enlarged = copy.deepcopy(record)
        enlarged['result_scope'] = 'whole'
        with self.assertRaisesRegex(ValueError, 'partial contribution'):
            self.adopt(enlarged)


if __name__ == '__main__':
    unittest.main()
