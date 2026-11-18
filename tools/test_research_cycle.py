"""Re-run the complete lightweight research file cycle through root work.py.

This isolated integration fixture uses elementary integer inequalities, synthetic
agent/reviewer IDs, and a local bare Git remote. It launches no Work model and
does not certify independent mathematical review or any novel result. Unlike the
smaller function tests, every research/checkpoint operation below is a CLI call.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SOURCE = Path(__file__).resolve().parents[1]
BRANCH = 'research-cycle-fixture'
RUN = 'cycle-fixture'
HOME = 'research/runs/' + RUN
WORK = 'research/workspaces/' + RUN
REGISTRY = 'research/registry.json'


def digest(value):
    return hashlib.sha256(value).hexdigest()


def pin(value):
    return digest(json.dumps(value, ensure_ascii=False, sort_keys=True,
                             separators=(',', ':')).encode())


class ResearchCycleCLITests(unittest.TestCase):
    def setUp(self):
        # Never copy the live registry, journals, Git configuration or credentials.
        self.tmp = tempfile.TemporaryDirectory(prefix='research-cycle-', dir=SOURCE.parent)
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base / 'author'
        self.root.mkdir()
        self.remote = self.base / 'remote.git'
        self.env = dict(os.environ, GIT_TERMINAL_PROMPT='0', PYTHONDONTWRITEBYTECODE='1',
                        GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1')
        for key in list(self.env):
            if (key.startswith(('GIT_CONFIG_KEY_', 'GIT_CONFIG_VALUE_', 'WCG_'))
                    or key in {'GIT_DIR', 'GIT_WORK_TREE', 'GIT_COMMON_DIR', 'GIT_INDEX_FILE',
                               'GIT_OBJECT_DIRECTORY', 'GIT_ALTERNATE_OBJECT_DIRECTORIES',
                               'GIT_CONFIG_COUNT', 'GIT_ASKPASS', 'SSH_ASKPASS'}):
                self.env.pop(key)
        shutil.copy2(SOURCE / 'work.py', self.root / 'work.py')
        (self.root / 'tools').mkdir()
        for source in (SOURCE / 'tools').glob('*.py'):
            if not source.name.startswith('test_'):
                shutil.copy2(source, self.root / 'tools' / source.name)
        shutil.copytree(SOURCE / 'tools/vendor', self.root / 'tools/vendor',
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        self.write('.gitignore', '__pycache__/\n*.pyc\n')
        self.write('archives/fixture/README.md', '# Fixture archive\n')
        self.write('prompts/research-runtime.md', '# Fixture launch instructions\n')
        self.write('archives/fixture/workspaces/Boss2/README.md', '# Fixture workspace\n')
        self.write('archives/fixture/workspaces/Boss2/workspace.json',
                   {'schema': 1, 'save': 'fixture', 'actor': 'Boss2', 'instance': '1' * 32})
        self.git('init', '-q', '-b', BRANCH)
        self.bind_clone()
        self.problem = self.write(WORK + '/problem.md',
                                  '# Engineering fixture, not a research claim\n\n'
                                  'For every integer n, prove n + 4 >= n in the usual order.\n'
                                  'Intermediate facts are n + 1 >= n and n + 2 >= n.\n')
        self.definition = self.write(WORK + '/definitions.md',
                                     '# Model\n\nThe domain is the integers with their usual order. '
                                     'Addition preserves the order and the domain is closed under addition.\n')
        self.obstacle = self.write(WORK + '/allowed-obstacle.md',
                                   '# Allowed initial warning\n\nA finite check alone does not prove a universally quantified integer inequality.\n')
        self.spec = WORK + '/spec.json'
        self.write(self.spec, {'problem_id': 'integer-order-fixture', 'problem': self.problem,
                               'definitions': [self.definition], 'obstacles': [self.obstacle],
                               'seed_ids': ['fixture-A']})
        self.objects = {'fixture-A': self.object('fixture-A', 1)}
        self.write(REGISTRY, {'schema': 2, 'objects': list(self.objects.values()),
                              'materials': [self.material(self.objects['fixture-A'])],
                              'edge_files': [], 'fixture_metadata': {'preserve': True}})
        self.git('add', '.')
        self.git('commit', '-qm', 'Minimal isolated CLI fixture')
        self.git('init', '--bare', '-q', str(self.remote))
        self.git('remote', 'add', 'origin', str(self.remote))
        self.git('push', '-qu', 'origin', BRANCH)
        self.initial = self.cli('research', 'studio', 'init', RUN, '--spec', self.spec,
                                '--expect-branch', BRANCH, '--expect-remote', str(self.remote))
        self.run = self.read(HOME + '/run.json')

    def command(self, command, *, cwd=None):
        result = subprocess.run(command, cwd=cwd or self.root, env=self.env,
                                capture_output=True, text=True, timeout=90)
        self.assertEqual(result.returncode, 0,
                         'Command failed: ' + ' '.join(map(str, command)) + '\n'
                         + result.stdout[-5000:] + '\n' + result.stderr[-5000:])
        return result.stdout.strip()

    def git(self, *args, cwd=None):
        return self.command(['git', *args], cwd=cwd)

    def bind_clone(self):
        # Local transport needs no credentials; SSH mode avoids token discovery.
        for key, value in {'user.name': 'Research Cycle Fixture',
                           'user.email': 'fixture@example.invalid', 'wcg.actor': 'Boss2',
                           'wcg.role': 'boss', 'wcg.branch': BRANCH,
                           'wcg.save': 'fixture', 'wcg.auth': 'ssh'}.items():
            self.git('config', '--local', key, value)

    def cli(self, *args):
        output = self.command([sys.executable, str(self.root / 'work.py'),
                               '--repo', str(self.root), *args])
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            self.fail('Expected one JSON CLI result:\n' + output[-5000:])

    def write(self, name, value):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value if isinstance(value, str) else
                        json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        return self.ref(name)

    def ref(self, name):
        return {'path': name, 'sha256': digest((self.root / name).read_bytes())}

    def read(self, name):
        return json.loads((self.root / name).read_text(encoding='utf-8'))

    def record(self, name, value):
        return self.write(WORK + '/main/' + name + '.json', value)['path']

    def object(self, oid, increment):
        proof = ('Since 1 >= 0, translation of the integer order gives n + 1 >= n. '
                 if increment == 1 else
                 'The previous universally quantified inequality gives n + '
                 + str(increment // 2) + ' >= n. Apply it also to the integer n + '
                 + str(increment // 2) + ', obtaining n + ' + str(increment)
                 + ' >= n + ' + str(increment // 2) + '. Transitivity gives n + '
                 + str(increment) + ' >= n. ')
        body = self.write('archives/fixture/state/命题/' + oid + '--命题.md',
                          '# ' + oid + '\n\nEngineering fixture; no novel mathematics.\n\n'
                          'For every integer n, n + ' + str(increment) + ' >= n.\n\n'
                          + proof + 'All variables range over the integers.\n')
        return {'object_id': oid, 'version': 1, 'title': oid, 'kind': 'lemma',
                'truth_status': 'proved', 'model': 'integers with usual order',
                'statement': 'n + ' + str(increment) + ' >= n',
                'quantifiers': 'for every integer n', 'assumptions': [],
                'scope': 'all integers', 'objections': 'Engineering fixture only',
                'body': body, 'evidence': [], 'sources': ['elementary integer order']}

    @staticmethod
    def material(obj):
        return {**obj['body'], 'disposition': 'objects', 'object_ids': [obj['object_id']],
                'reason': 'Exact fixture statement and complete elementary argument'}

    def save_line(self, line, text, *, session='fixture-session-1', agent=None,
                  feedback=None, ack=False, read_refs=None):
        journal = self.write(WORK + '/' + line + '/journal.md', text)
        args = ['research', 'studio', 'line', RUN, '--line', line,
                '--note', journal['path'], '--next', 'Continue the exact saved fixture obligation',
                '--agent-id', agent or 'fixture-no-model-' + line, '--session-tag', session,
                '--model', 'fixture-no-model', '--reasoning-effort', 'fixture', '--fork-turns', 'none']
        if feedback:
            args += ['--feedback', feedback]
        if ack:
            args += ['--ack-feedback']
        if read_refs is not None:
            ledger = self.write(WORK + '/' + line + '/reads.json',
                                {'reads': read_refs, 'note': 'Synthetic fixture inputs, not a Work read assertion'})
            args += ['--read-ledger', ledger['path']]
        return self.cli(*args), journal

    def adopt(self, number, source, target, edge, edge_path, *,
              session='fixture-session-1', agent=None):
        # Read the newly registered support through the user-facing CLI first.
        shown = self.cli('research', 'show', target, '--body')
        self.assertIn('body_text', shown)
        context = self.cli('research', 'context', target, '--edge', edge['edge_id'])
        support = context['support_options'][target][0]
        self.assertEqual(support['all_premises'], [source])
        frontier = self.cli('research', 'frontier', target, '--edge', edge['edge_id'],
                            '--expect-branch', BRANCH)
        self.assertIn(edge['edge_id'], json.dumps(frontier))
        self.write(WORK + '/informed-a/consumed-round-' + str(number) + '.json',
                   {'context': context, 'frontier': frontier})
        proof = self.write(WORK + '/informed-a/application-argument-' + str(number) + '.md',
                           '# Round ' + str(number) + ' consumes the previous new edge\n\n'
                           'Put k = ' + str(2 ** (number - 1)) + '. For any integer n, '
                           + source + ' gives n + k >= n. Since n + k is also an integer, '
                           'the same universal source gives n + 2k >= n + k. '
                           'Transitivity gives n + 2k >= n, exactly ' + target + '.\n'
                           'This is a synthetic engineering fixture, with no Work agent.\n')
        saved, _ = self.save_line('informed-a', '# Application saved\n\nSee ' + proof['path'] + '.\n',
                                     session=session, agent=agent,
                                     read_refs=[self.objects[source]['body'],
                                                self.objects[target]['body'], self.ref(edge_path)])
        record = {'application_id': 'fixture-application-' + str(number), 'line': 'informed-a',
                  'problem_spec_pin': self.run['spec_pin'], 'edge_id': edge['edge_id'],
                  'edge_declaration_pin': pin(edge), 'direction': 'forward',
                  'object_pins': {oid: pin(self.objects[oid]) for oid in (source, target)},
                  'source_to_target_mapping': 'Use arbitrary integer n and its translated integer instance',
                  'applicability': {'model': 'usual integer order',
                                    'quantifiers': 'the source is universal, hence both n and its shift apply',
                                    'scope': 'all integers'},
                  'premise_bindings': [{'source_id': source, 'source_pin': pin(self.objects[source]),
                                        'local_statement': self.objects[source]['statement'],
                                        'applicability': 'The universal statement applies to both needed integers',
                                        'state': 'established-here', 'proof_ref': proof}],
                  'bridge_obligation': {'state': 'global-whole-argument-applies',
                                        'statement': 'Transitivity joins the two shifted inequalities',
                                        'proof_ref': proof},
                  'conditions_text': edge['conditions'],
                  'condition_discharge': [{'condition': edge['conditions'],
                                           'argument': 'An integer plus the fixed integer increment is an integer',
                                           'state': 'established', 'proof_ref': proof}],
                  'result_scope': 'whole', 'actual_result': self.objects[target]['statement'],
                  'remaining': 'No debt for this elementary fixture lemma; no new research claim',
                  'evidence_refs': [proof], 'depends_on_applications': [],
                  'inherited_unpaid_obligation_ids': [], 'discharged_obligations': [],
                  'unpaid_obligation_ids': []}
        adopted = self.cli('research', 'studio', 'adopt', RUN,
                           '--record-file', self.record('application-' + str(number), record))
        return adopted, saved

    def backflow(self, number, source, target, increment, application=None):
        obj = self.object(target, increment)
        self.objects[target] = obj
        batch = self.write(WORK + '/main/batch-' + str(number) + '.json',
                           {'schema': 2, 'objects': [obj], 'materials': [self.material(obj)], 'edge_files': []})
        edge_path = 'map/edges/fixture/round-' + str(number) + '.json'
        edge = {'edge_id': 'fixture-edge-' + str(number), 'kind': 'implies', 'status': 'accepted',
                'source_ids': [source], 'target_ids': [target], 'premises_mode': 'all',
                'conditions': 'The shifted variable is an integer in the same usual order.',
                'scope': 'all integers', 'explanation': 'Apply the source at n and at n plus half the target increment, then use transitivity.',
                'roles': {source: 'universal translated inequality', target: 'twice the increment'},
                'evidence': [obj['body']], 'relation_mode': 'unconditional',
                'whole_result': obj['statement'] + ' for every integer n',
                'reviewed_by': 'synthetic-fixture-reviewer-no-model',
                'review_note': 'Fixture declaration only; no Work reviewer was launched'}
        self.write(edge_path, edge)
        self.cli('research', 'edge-bind', edge_path, '--batch-file', batch['path'], '--write')
        self.cli('research', 'edge-check', edge_path, '--batch-file', batch['path'])
        edge, edge_ref = self.read(edge_path), self.ref(edge_path)
        _, note = self.save_line('main', '# Fixture synthesis round ' + str(number)
                                 + '\n\n' + (self.root / obj['body']['path']).read_text(encoding='utf-8'))
        aid, fid, rid = ('fixture-result-' + str(number), 'fixture-freeze-' + str(number),
                         'fixture-review-' + str(number))
        artifact = {'artifact_id': aid, 'line': 'main', 'state': 'established', 'kind': 'lemma',
                    'statement': obj['statement'] + ' for every integer n; engineering fixture only',
                    'note_ref': note, 'authors': ['fixture-no-model-main'], 'evidence_refs': [],
                    'applications': ([{key: application[key] for key in ('application_id', 'revision_pin')}]
                                     if application else []),
                    'unpaid_obligation_ids': [], 'publication_refs': [obj['body'], batch, edge_ref]}
        self.cli('research', 'studio', 'artifact', RUN,
                 '--record-file', self.record('artifact-' + str(number), artifact))
        freeze = self.cli('research', 'studio', 'freeze', RUN, '--artifact', aid, '--freeze-id', fid)
        frozen = self.read(freeze['path'])
        self.assertTrue({self.problem['path'], self.definition['path'], self.obstacle['path'],
                         self.spec, HOME + '/packet-obstacle.json', HOME + '/packet-full.json'}
                        <= {ref['path'] for ref in frozen['content_refs']})
        report = self.write(WORK + '/informed-b/review-' + str(number) + '.md',
                            '# Synthetic review record\n\nEngineering fixture only. No Work reviewer or independent proof check was run.\n')
        review = {'review_id': rid, 'freeze_id': fid, 'freeze_revision_pin': freeze['revision_pin'],
                  'reviewer_agent_id': 'synthetic-fixture-reviewer-no-model', 'independent': True,
                  'scope': 'Simulated exact-version metadata for this engineering fixture',
                  'verdict': 'approve', 'evidence_level': 'internal-independent', 'report_ref': report,
                  'reviewed_content_refs': frozen['content_refs']}
        self.cli('research', 'studio', 'review', RUN,
                 '--record-file', self.record('review-' + str(number), review))
        plan = {'plan_id': 'fixture-backflow-' + str(number), 'freeze_id': fid, 'review_id': rid,
                'claim_scope': 'local-result', 'scope_argument': 'Publish only this elementary fixture lemma',
                'registration_batch_ref': batch, 'object_ids': [target], 'edge_refs': [edge_ref]}
        before = (self.root / REGISTRY).read_bytes()
        promoted = self.cli('research', 'studio', 'promote', RUN,
                            '--record-file', self.record('backflow-' + str(number), plan))
        self.assertEqual((self.root / REGISTRY).read_bytes(), before)
        candidate = self.read(promoted['candidate_registry_ref']['path'])
        self.assertTrue(candidate['fixture_metadata']['preserve'])
        self.cli('research', 'register', '--record-file', promoted['candidate_registry_ref']['path'])
        self.cli('research', 'edge-check', edge_path)
        checked = self.cli('research', 'check')
        self.assertEqual(checked['edges'], number)
        built = self.cli('research', 'build')
        self.assertIn('map/graph-v2.json', built['projections'])
        self.assertEqual(len(self.read(REGISTRY)['objects']), number + 1)
        return edge, edge_path, freeze, promoted

    def publish(self, freezes, plans):
        paths = ['research', 'archives/fixture', 'map']
        flags = [item for plan in plans for item in ('--review-plan', plan['path'])]
        pushed = self.cli('checkpoint', *paths, *flags, '-m', 'Save exact synthetic fixture increment')
        self.assertEqual(pushed['status'], 'pushed')
        self.assertEqual(pushed['review_checked_head'], pushed['pushed_head'])
        self.assertEqual(set(pushed['reviewed_plans']), {plan['path'] for plan in plans})
        self.assert_reviewed_bytes(pushed['pushed_head'], freezes)
        self.assertEqual(self.git('ls-remote', 'origin', 'refs/heads/' + BRANCH).split()[0],
                         pushed['pushed_head'])
        return pushed

    def assert_reviewed_bytes(self, revision, freezes):
        for frozen_ref in freezes:
            for ref in self.read(frozen_ref['path'])['content_refs']:
                raw = subprocess.check_output(['git', 'show', revision + ':' + ref['path']],
                                              cwd=self.root, env=self.env)
                self.assertEqual(digest(raw), ref['sha256'], ref['path'])

    def test_two_backflows_reconsumption_and_fresh_clone_recovery(self):
        self.assertEqual(self.initial['agents_launched'], 0)
        first_events = {}
        for line in ('main', 'independent', 'informed-a', 'informed-b'):
            event, _ = self.save_line(line, '# ' + line + '\n\nInitial synthetic fixture obligation.\n',
                                      read_refs=[self.problem] if line == 'independent' else None)
            first_events[line] = event['event_id']
        feedback, _ = self.save_line('informed-a', '# Partial fixture work\nThe shift must stay in the integer domain.\n',
                                     feedback='Explain why the translated variable remains an integer')
        self.assertEqual(feedback['continuation_of'], first_events['informed-a'])
        pending = self.cli('research', 'resume', RUN)
        self.assertIn('informed-a', pending['pending_feedback'])
        acked, _ = self.save_line('informed-a', '# Feedback answer\nThe sum of two integers is an integer.\n', ack=True)
        self.assertEqual(acked['continuation_of'], feedback['event_id'])
        self.assertNotIn('informed-a', self.cli('research', 'resume', RUN)['pending_feedback'])
        generic_save = self.cli('research', 'save', RUN, '--solver', 'independent', '--profile', 'obstacle',
                                '--note', WORK + '/independent/journal.md',
                                '--next', 'Continue from the same isolated original-input fixture')
        independent = self.read(HOME + '/run.json')['solvers']['independent']
        self.assertEqual(generic_save['continuation_of'], first_events['independent'])
        self.assertEqual(independent['session_tag'], 'fixture-session-1')
        self.assertIn('read_ledger', independent)
        ordinary = self.cli('checkpoint', 'research', '-m', 'Save ongoing fixture journals')
        self.assertEqual(ordinary['status'], 'pushed')
        self.assertEqual(ordinary.get('reviewed_plans'), [])

        edge1, path1, freeze1, plan1 = self.backflow(1, 'fixture-A', 'fixture-B', 2)
        first_push = self.publish([freeze1], [plan1])
        recovered = self.cli('research', 'resume', RUN)
        self.assertTrue(recovered['version_changes']['registry_changed'])
        self.assertIn(edge1['edge_id'], {row['edge_id'] for row in recovered['version_changes']['new_incident_edges']})

        # Round 2 genuinely records an application of the edge produced in round 1.
        application1, consumed1 = self.adopt(1, 'fixture-A', 'fixture-B', edge1, path1)
        edge2, path2, freeze2, plan2 = self.backflow(2, 'fixture-B', 'fixture-C', 4, application1)
        frozen2 = self.read(freeze2['path'])
        self.assertIn(path1, {ref['path'] for ref in frozen2['content_refs']})
        self.assertIn(application1['path'], {ref['path'] for ref in frozen2['content_refs']})
        self.save_line('informed-b', '# Pending saved fixture challenge\nCheck both translated integer instances.\n',
                       feedback='State explicitly how the same universal source pays both translated instances')
        second_push = self.publish([freeze1, freeze2], [plan1, plan2])
        self.assertNotEqual(first_push['pushed_head'], second_push['pushed_head'])

        # A blank-conversation startup must restore only the remote's committed bytes.
        clone = self.base / 'recovered'
        launcher = self.base / 'work.py'
        shutil.copy2(SOURCE / 'work.py', launcher)
        startup = json.loads(self.command([sys.executable, str(launcher), '--repo', str(clone),
            'start', '--actor', 'Boss2', '--save', 'fixture', '--remote', str(self.remote),
            '--branch', BRANCH, '--auth', 'ssh', '--resume'], cwd=self.base))
        self.assertEqual(startup['remote_tip'], second_push['pushed_head'])
        self.assertFalse(startup['workspace']['created'])
        self.root = clone
        resumed = self.cli('research', 'resume', RUN)
        self.assertEqual(resumed['recovery_warnings'], [])
        self.assertEqual(resumed['run']['spec_pin'], self.run['spec_pin'])
        self.assertEqual(resumed['event_history']['independent'][0]['event_id'], generic_save['event_id'])
        self.assertEqual(resumed['event_history']['independent'][-1]['event_id'], first_events['independent'])
        self.assertIn('informed-b', resumed['pending_feedback'])
        self.assertGreaterEqual(len(resumed['event_history']['informed-a']), 4)
        status = self.cli('research', 'studio', 'status', RUN, '--session-tag', 'fixture-session-2')
        self.assertEqual(status['agents_launched'], 0)
        self.assertEqual(status['application_version_issues'], [])
        self.assertEqual(status['frozen_version_issues'], [])
        self.assertFalse(status['lines']['informed-a']['session_match'])
        self.assertEqual(status['lines']['informed-a']['platform_liveness'], 'not-verified')
        self.assertEqual(self.git('rev-parse', 'HEAD'), second_push['pushed_head'])
        self.assert_reviewed_bytes(second_push['pushed_head'], [freeze1, freeze2])
        self.save_line('informed-b', '# Saved feedback answered\nUniversal quantification permits each integer substitution, '
                       'and transitivity combines the two exact inequalities.\n',
                       session='fixture-session-2', agent='fixture-restored-review-no-model', ack=True)

        # Resume the saved obligation with a new synthetic ID, then consume edge 2.
        continued, _ = self.save_line('informed-a', '# Restored fixture\nContinue from the committed round-2 inputs.\n',
                                      session='fixture-session-2', agent='fixture-replacement-no-model')
        self.assertEqual(continued['continuation_of'], consumed1['event_id'])
        app2, _ = self.adopt(2, 'fixture-B', 'fixture-C', edge2, path2,
                             session='fixture-session-2', agent='fixture-replacement-no-model')
        self.assertEqual(self.read(app2['path'])['edge_id'], edge2['edge_id'])
        continued_push = self.cli('checkpoint', 'research', '-m', 'Save restored fixture continuation')
        self.assertEqual(continued_push['status'], 'pushed')
        self.assertEqual(continued_push.get('reviewed_plans'), [])
        self.assert_reviewed_bytes(continued_push['pushed_head'], [freeze1, freeze2])
        final = self.cli('research', 'studio', 'status', RUN, '--session-tag', 'fixture-session-2')
        self.assertEqual(len(final['studio']['applications']), 2)
        self.assertEqual(len(final['studio']['backflow_plans']), 2)
        self.assertEqual(final['recovery']['pending_feedback'], {})
        self.assertEqual(self.git('status', '--porcelain'), '')


if __name__ == '__main__':
    unittest.main()
