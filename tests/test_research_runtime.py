"""Cross-layer contracts, not mathematical theorem certification."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import research_runtime as research
import map_tasks


class ResearchRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=ROOT / 'tests', prefix='research-fixture-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.git('init', '--quiet', '--initial-branch=main')
        self.git('config', 'user.name', 'Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.body = 'archives/demo/subarchives/child/state/notes.md'
        self.write(self.body, '# Model\nIntegers a,b,c.\n\n# A\na>0\n\n```python\n# Fake heading\n```\n\n# B\nb>0\n\n# C\na+b>0\n')
        self.write('research/target.md', '# Problem\nShow a+b>0 for positive integers.\n')
        self.write('research/definitions.md', '# Definitions\na and b are positive integers.\n')
        self.write('research/obstacles.md', '# Obstacle\nA one-premise claim does not suffice.\n')
        objects = []
        for oid in ['A', 'B', 'C']:
            objects.append({'object_id': oid, 'version': 1, 'title': oid, 'kind': 'lemma',
                            'truth_status': 'proved', 'model': 'positive integers', 'statement': oid + ' exact statement',
                            'quantifiers': 'for every a,b in the positive integers', 'assumptions': ['a,b>0'],
                            'scope': 'integer fixture only', 'objections': 'No known objection in this elementary fixture',
                            'body': self.ref(self.body, oid), 'evidence': [], 'sources': [], 'keywords': ['positive']})
        self.data = {'schema': 2, 'objects': objects, 'materials': [dict(self.ref(self.body), disposition='objects', object_ids=['A', 'B', 'C'], reason='Three independently stated claims in one page')], 'edge_files': ['map/edges/AB-C.json']}
        self.edge = {'edge_id': 'AB-C', 'source_ids': ['A', 'B'], 'target_ids': ['C'], 'premises_mode': 'all',
                     'kind': 'implies', 'status': 'accepted', 'relation_mode': 'unconditional', 'conditions': 'a,b>0',
                     'explanation': 'The sum of two positive integers is positive', 'scope': 'the stated integer domain',
                     'roles': {'A': 'positivity of a', 'B': 'positivity of b', 'C': 'positivity of the sum'},
                     'evidence': [self.ref(self.body, 'C')], 'reviewed_by': 'Fixture', 'review_note': 'Direct elementary proof, fixture only'}
        self.bind()
        self.spec = {'problem_id': 'positive-sum', 'problem': self.ref('research/target.md'),
                     'definitions': [self.ref('research/definitions.md')], 'obstacles': [self.ref('research/obstacles.md')], 'seed_ids': ['C']}
        self.write_json('research/spec.json', self.spec)
        self.git('add', '.'); self.git('commit', '--quiet', '-m', 'Fixture')

    def write(self, name, content):
        path = self.root / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(content)

    def write_json(self, name, data): self.write(name, json.dumps(data, ensure_ascii=False, indent=2) + '\n')

    def git(self, *args):
        p = subprocess.run(['git', *args], cwd=self.root, capture_output=True, text=True, timeout=45)
        self.assertEqual(p.returncode, 0, p.stderr); return p.stdout.strip()

    def ref(self, name, section=None):
        result = {'path': name, 'sha256': research.digest((self.root / name).read_bytes())}
        if section: result['section'] = section
        return result

    def bind(self):
        objs = {o['object_id']: o for o in self.data['objects']}
        bindings = research.edge_bindings(self.root, self.edge, objs)
        self.edge.update({k: v for k, v in bindings.items() if k != 'note'})
        self.write_json('map/edges/AB-C.json', self.edge)
        self.write_json(research.REGISTRY, self.data)

    def test_joint_premises_are_not_split_by_retrieval(self):
        ctx = research.context(self.root, ['A'], hops=1)
        self.assertEqual({o['object_id'] for o in ctx['objects']}, {'A', 'B', 'C'})
        self.assertEqual(len(ctx['edges']), 1)
        self.assertEqual(ctx['edges'][0]['source_ids'], ['A', 'B'])

    def test_one_page_can_hold_multiple_objects_without_rewriting(self):
        _, objects = research.load(self.root)
        self.assertEqual(len(objects), 3)
        self.assertIn('a>0', research.read_ref(self.root, objects['A']['body']))
        self.assertNotIn('b>0', research.read_ref(self.root, objects['A']['body']))

    def test_code_headings_do_not_end_sections(self):
        text = research.section((self.root / self.body).read_text(), 'A')
        self.assertIn('# Fake heading', text)
        with self.assertRaisesRegex(ValueError, 'missing'): research.section(text, 'Fake heading')

    def test_changed_relation_explanation_requires_new_review(self):
        self.edge['explanation'] = 'Different argument'
        self.write_json('map/edges/AB-C.json', self.edge)
        with self.assertRaisesRegex(ValueError, 'Stale'): research.check(self.root)

    def test_changed_object_metadata_invalidates_relation(self):
        self.data['objects'][0]['quantifiers'] = 'there exists a'
        self.write_json(research.REGISTRY, self.data)
        with self.assertRaisesRegex(ValueError, 'endpoint_pins'): research.check(self.root)

    def test_changed_body_is_not_silently_reaccepted(self):
        self.write(self.body, 'Different mathematics')
        with self.assertRaisesRegex(ValueError, 'Stale content'): research.check(self.root)

    def test_conditional_or_finite_premise_cannot_become_unconditional(self):
        self.data['objects'][0]['truth_status'] = 'finite'; self.bind()
        with self.assertRaisesRegex(ValueError, 'conditional relation'): research.check(self.root)
        self.edge['relation_mode'] = 'conditional'; self.bind()
        self.assertEqual(research.check(self.root)['edges'], 1)

    def test_context_edge_cannot_act_as_proof(self):
        self.edge['kind'] = 'motivates'; self.bind()
        with self.assertRaisesRegex(ValueError, 'Contextual'): research.check(self.root)

    def test_obstacle_packet_has_no_graph_or_existing_claims(self):
        value = research.packet(self.root, self.spec, 'obstacle')
        self.assertNotIn('context', value); self.assertNotIn('retrieval', value)
        self.assertNotIn('A exact statement', json.dumps(value))
        self.assertEqual(value['launch']['fork_turns'], 'none')
        self.assertIn('context', research.packet(self.root, self.spec, 'full'))

    def test_feedback_continues_original_solver_and_survives_reload(self):
        research.init_run(self.root, 'r1', 'research/spec.json')
        self.write('research/workspaces/r1/s1.md', '# Partial\nPositive sum argument.\n')
        first = research.update_run(self.root, 'r1', 's1', 'full', 'research/workspaces/r1/s1.md', 'Check the zero boundary', 'candidate', agent_id='live-agent-1')
        second = research.update_run(self.root, 'r1', 's1', 'full', 'research/workspaces/r1/s1.md', 'Answer this precise domain question', 'needs-feedback', feedback='Is zero actually allowed?')
        state = research.resume(self.root, 'r1')['run']['solvers']['s1']
        self.assertEqual(second['continuation_of'], first['event_id'])
        self.assertEqual(state['agent_id'], 'live-agent-1'); self.assertEqual(state['feedback'], 'Is zero actually allowed?')
        with self.assertRaises(ValueError): research.init_run(self.root, 'r1', 'research/spec.json')

    def test_problem_change_cannot_resume_as_same_problem(self):
        research.init_run(self.root, 'r1', 'research/spec.json')
        self.spec['problem_id'] = 'another-problem'; self.write_json('research/spec.json', self.spec)
        with self.assertRaisesRegex(ValueError, 'reframe'): research.resume(self.root, 'r1')

    def test_missing_coverage_blocks_final_graph(self):
        self.write('archives/demo/state/extra.md', '# New claim\n')
        with self.assertRaisesRegex(ValueError, 'coverage incomplete'): research.check(self.root, final=True)
        self.assertEqual(research.check(self.root)['unregistered_materials'], 1)

    def test_no_evidence_snapshots_enter_inventory(self):
        self.write('archives/demo/tools/evidence/original/archives/fake/state/fake.md', '# Old copy\n')
        self.assertEqual(len(research.inventory(self.root)), 1)

    def test_three_projection_levels_and_boundary_objects(self):
        result = research.build(self.root, final=True)
        self.assertEqual(len(result['projections']), 3)
        self.assertTrue((self.root / 'archives/demo/map/graph-v2.json').is_file())

    def test_registration_changes_need_new_object_version(self):
        self.data['objects'][0]['statement'] = 'A different statement'
        self.edge['status'] = 'proposed'; self.bind()
        # Restore the previous canonical declaration before importing a candidate.
        self.git('checkout', '--', research.REGISTRY)
        self.write_json('research/proposed-registry.json', self.data)
        with self.assertRaisesRegex(ValueError, 'new version'): research.register(self.root, 'research/proposed-registry.json')

    def definition(self, task_id='t1'):
        return {'task_id': task_id, 'stage': '3A', 'registry': research.REGISTRY,
                'input_pins': {o['object_id']: research.pin(o) for o in self.data['objects']},
                'object_ids': ['A', 'B', 'C'], 'write_paths': ['map/edges', 'map/receipts/t1.json'], 'goal': 'Compare the sum proof'}

    def test_map_scope_conflict_and_exact_coverage(self):
        old = {'definition': self.definition(), 'state': 'available', 'owner': None}
        claimed = map_tasks.transition(self.root, old, [], 'Boss32', 'claim', 'r1')
        other = copy.deepcopy(claimed); other['definition']['task_id'] = 'other'
        with self.assertRaisesRegex(ValueError, 'Overlapping'):
            map_tasks.transition(self.root, old, [other], 'Boss33', 'claim', 'r2')
        with self.assertRaisesRegex(ValueError, 'Every input'):
            map_tasks.transition(self.root, claimed, [], 'Boss32', 'done', 'r2', receipt={'coverage': {}})

    def test_map_done_requires_outputs_in_published_snapshot(self):
        old = {'definition': self.definition(), 'state': 'claimed', 'owner': 'Boss32'}
        coverage = {i: {'state': 'linked', 'reason': 'AB-C comparison', 'comparison_scope': 'A B C'} for i in ['A', 'B', 'C']}
        with self.assertRaises(FileNotFoundError):
            map_tasks.transition(self.root, old, [], 'Boss32', 'done', 'r2', receipt={'coverage': coverage, 'assets': [{'path': 'map/receipts/t1.json', 'sha256': 'a'*64}]})

    def test_root_work_cli_dispatch_is_read_only(self):
        shutil.copy2(ROOT / 'work.py', self.root / 'work.py')
        shutil.copytree(ROOT / 'tools', self.root / 'tools', ignore=shutil.ignore_patterns('evidence', '__pycache__'))
        p = subprocess.run([sys.executable, str(self.root / 'work.py'), '--repo', str(self.root), 'research', 'context', 'A', '--hops', '1'], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(len(json.loads(p.stdout)['edges']), 1)


if __name__ == '__main__': unittest.main()
