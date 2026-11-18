"""Meaningful negative boundaries and a real registry/edge backflow cycle."""
import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

import research_frontier as frontier
import research_runtime as runtime
import research_studio as studio


class StudioTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=Path.cwd())
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.git('init', '-q', '-b', 'research-test')
        self.git('config', 'user.name', 'Test')
        self.git('config', 'user.email', 'test@example.invalid')
        self.git('config', 'wcg.actor', 'Boss2')
        self.git('commit', '-qm', 'initial', '--allow-empty')
        self.git('remote', 'add', 'origin', 'https://example.invalid/research.git')
        self.problem = self.write('problem.md', '# Original problem\nFor every x in the full model.\n')
        self.spec = {'problem_id': 'exact-target', 'problem': self.problem,
                     'definitions': [], 'obstacles': [], 'seed_ids': []}
        self.write('spec.json', self.spec)
        self.initialized = studio.init(self.root, 'run', 'spec.json', expect_branch='research-test')
        self.home = 'research/runs/run'
        self.work = 'research/workspaces/run'
        self.note = self.write(self.work + '/main/journal.md', '# Derivation\nA full mathematical argument.\n')
        studio.line(self.root, 'run', 'main', self.note['path'], 'Prove the remaining bridge', 'actual-main', 'session-one')
        self.run = self.read(self.home + '/run.json')

    def git(self, *args):
        return subprocess.run(['git', *args], cwd=self.root, check=True,
                              capture_output=True, text=True).stdout.strip()

    def write(self, name, value):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value if isinstance(value, str) else json.dumps(value, ensure_ascii=False), encoding='utf-8')
        return {'path': name, 'sha256': runtime.digest(path.read_bytes())}

    def read(self, name):
        return json.loads((self.root / name).read_text(encoding='utf-8'))

    def record(self, value, name='record'):
        return self.write(self.work + '/main/' + name + '.json', value)['path']

    def obj(self, oid, truth='proved'):
        body = self.write('archives/example/state/命题/' + oid + '--命题.md', '# ' + oid + '\nPrecise statement and complete argument.\n')
        return {'object_id': oid, 'version': 1, 'title': oid, 'kind': 'lemma',
                'truth_status': truth, 'model': 'same exact model', 'statement': oid + '(x)',
                'quantifiers': 'for every x', 'assumptions': [], 'scope': 'full domain',
                'objections': 'No additional objection declared', 'body': body,
                'evidence': [], 'sources': ['actual local derivation']}

    def material(self, obj):
        return {**obj['body'], 'disposition': 'objects', 'object_ids': [obj['object_id']],
                'reason': 'This body contains this exact statement and proof'}

    def graph(self, *, partial=False, reverse=False):
        self.objects = {obj['object_id']: obj for obj in [self.obj('A'), self.obj('B', 'open'), self.obj('C', 'open')]}
        self.edge = {'edge_id': 'joint', 'kind': 'equivalent_to' if reverse else 'implies',
                     'status': 'accepted', 'premises_mode': 'all',
                     'source_ids': ['A', 'B'], 'target_ids': ['C'],
                     'conditions': 'The same x is used throughout.', 'scope': 'same exact model',
                     'explanation': 'The joint argument uses A and B on the same x.',
                     'roles': {'A': 'first premise', 'B': 'joint premise', 'C': 'conclusion'},
                     'evidence': [self.note], 'relation_mode': 'conditional',
                     'reviewed_by': 'actual prior author', 'review_note': 'Declared exact conditional argument'}
        if partial:
            self.edge['contribution'] = {'result': 'A local step toward C', 'remaining': 'The global C argument remains unpaid'}
        else:
            self.edge['whole_result'] = 'A and B imply C under the same x'
        self.edge.update(runtime.edge_bindings(self.root, self.edge, self.objects))
        self.edge_ref = self.write('map/edges/joint.json', self.edge)
        registry = {'schema': 2, 'objects': list(self.objects.values()),
                    'materials': [self.material(obj) for obj in self.objects.values()],
                    'edge_files': [self.edge_ref['path']], 'historical_field': {'preserve': True}}
        self.write(runtime.REGISTRY, registry)
        return registry

    def application(self, aid='app', *, open_b=True, reverse=False, partial=False):
        premises = ['C'] if reverse else ['A', 'B']
        bindings = []
        for oid in premises:
            row = {'source_id': oid, 'source_pin': runtime.pin(self.objects[oid]),
                   'local_statement': oid + '(the same x)', 'applicability': 'Exact shared instance and quantifiers',
                   'state': 'established-here', 'proof_ref': self.note}
            if oid == 'B' and open_b:
                row.pop('proof_ref')
                row.update(state='open-obligation', obligation_id='B-required')
            bindings.append(row)
        result = {'application_id': aid, 'line': 'main', 'problem_spec_pin': self.run['spec_pin'],
                  'edge_id': 'joint', 'edge_declaration_pin': runtime.pin(self.edge),
                  'direction': 'reverse' if reverse else 'forward',
                  'object_pins': {oid: runtime.pin(obj) for oid, obj in self.objects.items()},
                  'source_to_target_mapping': 'Use the same x, full model and quantifier order',
                  'premise_bindings': bindings,
                  'bridge_obligation': {'state': 'global-whole-argument-applies',
                                        'statement': 'ALL instantiated premises jointly give the local conclusion', 'proof_ref': self.note},
                  'conditions_text': self.edge['conditions'],
                  'condition_discharge': [{'condition': self.edge['conditions'], 'argument': 'All instances are identical',
                                           'state': 'established', 'proof_ref': self.note}],
                  'applicability': {'model': 'same exact model', 'quantifiers': 'same x throughout', 'scope': 'full domain'},
                  'depends_on_applications': [], 'inherited_unpaid_obligation_ids': [],
                  'discharged_obligations': [], 'unpaid_obligation_ids': ['B-required'] if open_b and not reverse else [],
                  'actual_result': 'The exact instantiated C, conditional on B when unpaid',
                  'remaining': 'B remains required' if open_b else 'No local hypothesis debt remains',
                  'result_scope': 'contribution' if partial else 'whole', 'evidence_refs': [self.note]}
        if partial:
            result['target_remaining'] = {'statement': self.edge['contribution']['remaining'], 'obligation_id': 'C-global-remaining'}
        return result

    def adopt(self, record):
        return studio.adopt(self.root, 'run', self.record(record, record['application_id']))

    def artifact(self, *, state='established', applications=None, publication_refs=None, debts=None, aid='result'):
        record = {'artifact_id': aid, 'line': 'main', 'kind': 'lemma',
                  'statement': 'The exact reusable local result', 'state': state,
                  'note_ref': self.note, 'authors': ['actual-main'],
                  'unpaid_obligation_ids': debts or [], 'evidence_refs': [],
                  'publication_refs': publication_refs or [], 'applications': applications or []}
        result = studio.artifact(self.root, 'run', self.record(record, 'artifact-' + aid))
        return record, result

    def review(self, fid, *, reviewer='independent-reviewer', verdict='approve', rid='review', resolves=None):
        index = self.read(self.home + '/studio.json')
        frozen = self.read(index['freezes'][fid]['path'])
        report = self.write(self.work + '/informed-b/' + rid + '.md', '# Independent challenge\nExact proof steps and conditions were examined.\n')
        record = {'review_id': rid, 'freeze_id': fid,
                  'freeze_revision_pin': index['freezes'][fid]['revision_pin'],
                  'reviewer_agent_id': reviewer, 'independent': True,
                  'scope': 'All frozen statements, new bridges, evidence and exact publication metadata',
                  'verdict': verdict, 'report_ref': report,
                  'reviewed_content_refs': frozen['content_refs'], 'evidence_level': 'internal-independent'}
        if resolves:
            record.update(resolves_review_ids=resolves, resolution_argument='The exact objection is addressed in the frozen proof and this report')
        return studio.review(self.root, 'run', self.record(record, rid))

    def backflow(self, *, applications=None, state='established', edge_evidence=None):
        objects = [self.obj('X', 'conditional' if state == 'conditional' else 'open' if state == 'open' else 'proved'), self.obj('Y')]
        if state in {'conditional', 'open'}:
            objects = objects[:1]
        batch = {'schema': 2, 'objects': objects, 'materials': [self.material(obj) for obj in objects], 'edge_files': []}
        batch_ref = self.write(self.work + '/main/registration-batch.json', batch)
        refs = [obj['body'] for obj in objects] + [batch_ref]
        edges = []
        if len(objects) == 2:
            by_id = {obj['object_id']: obj for obj in objects}
            edge = {'edge_id': 'new-support', 'kind': 'implies', 'status': 'accepted',
                    'source_ids': ['X'], 'target_ids': ['Y'], 'premises_mode': 'all',
                    'conditions': 'Same exact full-domain model', 'scope': 'full domain',
                    'explanation': 'X gives the complete Y statement',
                    'roles': {'X': 'full sufficient input', 'Y': 'whole conclusion'},
                    'evidence': edge_evidence or [objects[0]['body']], 'relation_mode': 'unconditional',
                    'whole_result': 'X implies the whole Y', 'reviewed_by': 'independent-reviewer',
                    'review_note': 'Examined the complete full-domain argument'}
            edge.update(runtime.edge_bindings(self.root, edge, by_id))
            edges = [self.write('map/edges/new-support.json', edge)]
            refs.extend(edges)
        self.artifact(state=state, applications=applications, publication_refs=refs)
        frozen = studio.freeze(self.root, 'run', 'result', 'frozen')
        self.review('frozen')
        return {'plan_id': 'publish', 'freeze_id': 'frozen', 'review_id': 'review',
                'claim_scope': 'local-result', 'scope_argument': 'This is the precise reviewed reusable statement',
                'registration_batch_ref': batch_ref, 'object_ids': [obj['object_id'] for obj in objects], 'edge_refs': edges}

    def test_init_launches_nothing_and_main_plus_three_keep_separate_packets(self):
        self.assertEqual(self.initialized['agents_launched'], 0)
        self.assertEqual(self.initialized['subagent_count'], 3)
        self.assertEqual(set(studio.LINES), {row['solver_id'] for row in self.initialized['solver_roster']})
        obstacle = self.read(self.home + '/packet-obstacle.json')
        self.assertNotIn('context', obstacle)
        self.assertEqual(obstacle['target'], '# Original problem\nFor every x in the full model.\n')
        for slot in studio.LINES:
            self.assertTrue((self.root / self.work / slot / 'journal.md').is_file())
        with self.assertRaisesRegex(ValueError, 'Existing RUN'):
            (self.root / self.home / 'studio.json').unlink()
            studio.init(self.root, 'run', 'spec.json', expect_branch='research-test')

    def test_same_event_chain_preserves_feedback_and_marks_cross_session_recovery(self):
        first = self.run['solvers']['main']['latest_event']
        saved = studio.line(self.root, 'run', 'main', self.note['path'], 'Answer exact missing step',
                            'actual-main', 'session-one', feedback='The last implication needs proof')
        self.assertEqual(saved['continuation_of'], first)
        result = studio.status(self.root, 'run', 'new-session')
        self.assertFalse(result['lines']['main']['session_match'])
        self.assertEqual(result['lines']['main']['platform_liveness'], 'not-verified')
        self.assertIn('main', result['recovery']['pending_feedback'])
        self.assertEqual(self.read(self.home + '/studio.json')['artifacts'], {})

    def test_restart_distinguishes_committed_journal_from_new_note_bytes(self):
        committed = self.write(self.note['path'], 'A prior journal saved before this restart.\n')
        self.git('add', committed['path'])
        self.git('commit', '-qm', 'Prior journal')
        restarted = studio.line(self.root, 'run', 'main', committed['path'],
                                'Resume the existing derivation', 'actual-main', 'session-two')
        self.assertEqual(restarted['note_change'], 'same-as-committed-source')
        repeated = studio.line(self.root, 'run', 'main', committed['path'],
                               'Record feedback without editing the note', 'actual-main', 'session-two')
        self.assertEqual(repeated['note_change'], 'same-as-previous-event')
        updated = self.write(committed['path'], 'A derivation with an additional step.\n')
        advance = studio.line(self.root, 'run', 'main', updated['path'],
                              'Check the new step', 'actual-main', 'session-two')
        self.assertEqual(advance['note_change'], 'different-note-bytes')
        status = studio.status(self.root, 'run', 'session-two')
        self.assertEqual(status['lines']['main']['note_change'], advance['note_change'])

    def test_scoped_studio_rejects_another_archive_and_cannot_be_rebound(self):
        scope = 'archives/customer-attraction/subarchives/six-providers'
        self.write('archives/customer-attraction/README.md', '# Parent\n')
        self.write(scope + '/README.md', '# Child\n')
        self.git('config', 'wcg.save', 'customer-attraction')
        self.git('config', 'wcg.subarchive', 'six-providers')
        spec = {**self.spec, 'collaboration_scope': 'archives/unrelated-machines'}
        self.write('scoped.json', spec)
        with self.assertRaisesRegex(ValueError, 'RUN archive mismatch'):
            studio.init(self.root, 'scoped', 'scoped.json', expect_branch='research-test')
        self.assertFalse((self.root / 'research/runs/scoped').exists())
        spec['collaboration_scope'] = scope
        self.write('scoped.json', spec)
        result = studio.init(self.root, 'scoped', 'scoped.json', expect_branch='research-test')
        self.assertEqual(result['archive_scope'], scope)
        self.assertEqual(studio.status(self.root, 'scoped')['studio']['archive_scope'], scope)
        self.git('config', '--unset', 'wcg.subarchive')
        with self.assertRaisesRegex(ValueError, 'clone bound to this studio archive'):
            studio.status(self.root, 'scoped')

    def test_reviewed_backflow_rejects_a_body_in_a_different_archive(self):
        record = self.backflow()
        index = self.read(self.home + '/studio.json')
        index['archive_scope'] = 'archives/target'
        self.write(self.home + '/studio.json', index)
        self.write('archives/target/README.md', '# Target archive\n')
        self.git('config', 'wcg.save', 'target')
        with self.assertRaisesRegex(ValueError, 'Register the RUN result under archives/target/state/'):
            studio.promote(self.root, 'run', self.record(record, 'backflow'))

    def test_four_lines_resume_same_problem_and_save_preserves_agent_session_and_reads(self):
        events = {}
        for slot in studio.LINES:
            ledger = self.write(self.work + '/' + slot + '/reads.json',
                                {'reads': [self.problem], 'note': 'Read the unchanged original question'})
            with mock.patch.object(runtime, '_write_json', wraps=runtime._write_json) as writes:
                saved = studio.line(self.root, 'run', slot, self.work + '/' + slot + '/journal.md',
                                    'Continue this exact mathematical line', 'agent-' + slot, 'session-one',
                                    model='actual-model', reasoning_effort='ultra', fork_turns='none',
                                    read_ledger=ledger['path'], feedback='Pay the precise missing step')
            event_writes = [call for call in writes.call_args_list if '/events/' in str(call.args[0])]
            self.assertEqual(len(event_writes), 1, 'A saved immutable event must be written once')
            original = self.read(self.home + '/events/' + saved['event_id'] + '.json')
            continued = runtime.update_run(self.root, 'run', slot, studio.LINES[slot],
                                           self.work + '/' + slot + '/journal.md', 'Answer the pending feedback',
                                           'working', agent_id='agent-' + slot)
            events[slot] = self.read(self.home + '/events/' + continued['event_id'] + '.json')
            self.assertEqual(events[slot]['continuation_of'], saved['event_id'])
            self.assertEqual(events[slot]['session_tag'], 'session-one')
            self.assertEqual(events[slot]['read_ledger'], original['read_ledger'])
            self.assertEqual(self.read(self.home + '/events/' + saved['event_id'] + '.json'), original)
        recovered = studio.status(self.root, 'run', 'session-one')
        self.assertEqual(set(recovered['lines']), set(studio.LINES))
        self.assertTrue(all(line['session_match'] for line in recovered['lines'].values()))
        self.assertEqual(set(recovered['recovery']['pending_feedback']), set(studio.LINES))
        self.assertEqual(set(recovered['recovery']['packet_bindings']), {'full', 'obstacle'})
        replacement = runtime.update_run(self.root, 'run', 'informed-a', 'full',
                                         self.work + '/informed-a/journal.md', 'Recover the same original line',
                                         'working', agent_id='fresh-replacement')
        replaced = self.read(self.home + '/events/' + replacement['event_id'] + '.json')
        self.assertNotIn('session_tag', replaced)
        self.assertNotIn('read_ledger', replaced)
        self.assertEqual(replaced['continuation_of'], events['informed-a']['event_id'])
        self.assertTrue(replaced['feedback_pending'])

    def test_foreign_boss_branch_remote_and_path_writes_are_rejected(self):
        with self.assertRaises(ValueError):
            studio.line(self.root, 'run', 'main', self.work + '/informed-a/journal.md', 'Continue', 'main', 'one')
        with self.assertRaises(ValueError):
            studio.artifact(self.root, 'run', '../escape.json')
        self.git('config', 'wcg.actor', 'Boss3')
        with self.assertRaisesRegex(ValueError, 'another Boss'):
            studio.status(self.root, 'run')
        self.git('config', 'wcg.actor', 'Boss2')
        self.git('checkout', '-qb', 'other-branch')
        with self.assertRaisesRegex(ValueError, 'Expected branch'):
            studio.status(self.root, 'run')
        self.git('checkout', '-q', 'research-test')
        self.git('remote', 'set-url', 'origin', 'https://example.invalid/other.git')
        with self.assertRaisesRegex(ValueError, 'origin changed'):
            studio.status(self.root, 'run')

    def test_independent_read_ledger_rejects_informed_material_and_snapshots_actual_reads(self):
        foreign = self.write(self.work + '/informed-a/result.md', 'An informed result')
        ledger = self.write(self.work + '/independent/reads.json', {'reads': [foreign], 'note': 'Read exact source'})
        kwargs = {'model': 'actual-model', 'reasoning_effort': 'ultra', 'fork_turns': 'none', 'read_ledger': ledger['path']}
        with self.assertRaisesRegex(ValueError, 'Independent input'):
            studio.line(self.root, 'run', 'independent', self.work + '/independent/journal.md', 'Continue', 'actual-independent', 'session-one', **kwargs)
        self.write(ledger['path'], {'reads': [self.problem], 'note': 'Read the full original problem'})
        result = studio.line(self.root, 'run', 'independent', self.work + '/independent/journal.md', 'Prove the original target', 'actual-independent', 'session-one', **kwargs)
        event = self.read(self.home + '/events/' + result['event_id'] + '.json')
        self.write(ledger['path'], {'reads': [foreign], 'note': 'Later changed'})
        self.assertEqual(json.loads(runtime.ref_bytes(self.root, event['read_ledger']))['reads'], [self.problem])

    def test_all_premises_need_payment_reading_is_not_payment_and_reverse_keeps_all(self):
        self.graph()
        application = self.application()
        application['premise_bindings'].pop()
        with self.assertRaisesRegex(ValueError, 'Every ALL'):
            self.adopt(application)
        application = self.application()
        application['unpaid_obligation_ids'] = []
        with self.assertRaisesRegex(ValueError, 'omit or invent'):
            self.adopt(application)
        result = self.adopt(self.application())
        self.assertEqual(result['unpaid_obligation_ids'], ['B-required'])
        self.graph(reverse=True)
        reverse = self.application('reverse', reverse=True, open_b=False)
        reverse['premise_bindings'] = []
        with self.assertRaisesRegex(ValueError, 'Every ALL'):
            self.adopt(reverse)

    def test_legacy_edge_without_declared_result_scope_cannot_be_adopted_as_whole(self):
        self.graph()
        self.edge.pop('whole_result')
        self.edge.update(runtime.edge_bindings(self.root, self.edge, self.objects))
        self.write(self.edge_ref['path'], self.edge)
        report = frontier.frontier_report(runtime.context(self.root, ['C']))
        self.assertIn('whole-result-scope-requires-review', report['routes'][0]['structural_blockers'])
        with self.assertRaisesRegex(ValueError, 'whole_result'):
            self.adopt(self.application(open_b=False))

    def test_upstream_debt_must_be_inherited_and_only_explicit_proof_can_remove_it(self):
        self.graph()
        upstream = self.adopt(self.application('upstream'))
        child = self.application('child', open_b=False)
        child['depends_on_applications'] = [{'application_id': 'upstream', 'revision_pin': upstream['revision_pin']}]
        with self.assertRaisesRegex(ValueError, 'Inherited upstream debt'):
            self.adopt(child)
        child['inherited_unpaid_obligation_ids'] = ['B-required']
        child['unpaid_obligation_ids'] = ['B-required']
        result = self.adopt(child)
        self.assertEqual(result['unpaid_obligation_ids'], ['B-required'])
        child['discharged_obligations'] = [{'obligation_id': 'B-required', 'proof_ref': self.note}]
        child['unpaid_obligation_ids'] = []
        self.assertEqual(self.adopt(child)['unpaid_obligation_ids'], [])

    def test_open_condition_and_bridge_debts_survive_downstream_adoption(self):
        self.graph()
        upstream = self.application('upstream', open_b=False)
        upstream['bridge_obligation'].update(state='gap', obligation_id='joint-bridge')
        upstream['bridge_obligation'].pop('proof_ref')
        upstream['condition_discharge'][0].update(state='open', obligation_id='same-instance')
        upstream['condition_discharge'][0].pop('proof_ref')
        upstream['unpaid_obligation_ids'] = ['joint-bridge', 'same-instance']
        result = self.adopt(upstream)
        child = self.application('child', open_b=False)
        child['depends_on_applications'] = [{'application_id': 'upstream', 'revision_pin': result['revision_pin']}]
        child['inherited_unpaid_obligation_ids'] = ['joint-bridge']
        child['unpaid_obligation_ids'] = ['joint-bridge']
        with self.assertRaisesRegex(ValueError, 'Inherited upstream debt'):
            self.adopt(child)
        child['inherited_unpaid_obligation_ids'] = ['joint-bridge', 'same-instance']
        child['unpaid_obligation_ids'] = ['joint-bridge', 'same-instance']
        self.assertEqual(self.adopt(child)['unpaid_obligation_ids'], ['joint-bridge', 'same-instance'])

    def test_conditional_dependency_cycle_cannot_pay_itself(self):
        self.graph()
        a = self.adopt(self.application('a'))
        b = self.application('b')
        b.update(depends_on_applications=[{'application_id': 'a', 'revision_pin': a['revision_pin']}],
                 inherited_unpaid_obligation_ids=['B-required'])
        b = self.adopt(b)
        a2 = self.application('a')
        a2.update(depends_on_applications=[{'application_id': 'b', 'revision_pin': b['revision_pin']}],
                  inherited_unpaid_obligation_ids=['B-required'])
        with self.assertRaisesRegex(ValueError, 'cycle'):
            self.adopt(a2)

    def test_freeze_includes_application_and_new_bridge_proof_bytes(self):
        self.graph()
        proof = self.write(self.work + '/main/new-bridge.md', '# New synthesis\nActual complete synthesis argument.\n')
        global_proof = self.write('archives/example/state/命题/global-edge-proof.md',
                                  '# Prior relation\nFull independent global relation argument.\n')
        self.edge['evidence'] = [global_proof]
        self.edge.update(runtime.edge_bindings(self.root, self.edge, self.objects))
        self.write(self.edge_ref['path'], self.edge)
        app = self.application(open_b=False)
        app['bridge_obligation']['proof_ref'] = proof
        app = self.adopt(app)
        self.artifact(applications=[{'application_id': 'app', 'revision_pin': app['revision_pin']}])
        frozen = studio.freeze(self.root, 'run', 'result')
        record = self.read(frozen['path'])
        self.assertIn(proof, record['content_refs'])
        self.assertIn(global_proof, record['content_refs'])
        self.assertIn({key: app[key] for key in ('path', 'sha256')}, record['content_refs'])

    def test_status_detects_changed_adoption_even_before_any_freeze(self):
        self.graph()
        self.adopt(self.application())
        self.edge['review_note'] = 'A newly corrected relation argument'
        self.edge.update(runtime.edge_bindings(self.root, self.edge, self.objects))
        self.write(self.edge_ref['path'], self.edge)
        recovered = studio.status(self.root, 'run', 'session-one')
        self.assertEqual(recovered['application_version_issues'][0]['application_id'], 'app')
        self.assertIn('Stale application edge', recovered['application_version_issues'][0]['error'])
        self.assertEqual(recovered['frozen_version_issues'], [])

    def test_old_review_does_not_cover_changed_artifact_or_mutable_publication(self):
        plan = self.backflow()
        old = self.read(self.home + '/studio.json')
        self.write(self.note['path'], '# Derivation\nRevised proof with changed conditions.\n')
        self.note = {'path': self.note['path'], 'sha256': runtime.digest((self.root / self.note['path']).read_bytes())}
        self.artifact()
        with self.assertRaisesRegex(ValueError, 'new revision'):
            studio.promote(self.root, 'run', self.record(plan, 'publish'))
        self.assertEqual(self.read(self.home + '/studio.json')['freezes'], old['freezes'])

    def test_original_problem_bytes_are_frozen_and_old_review_rejects_replaced_input(self):
        plan = self.backflow()
        frozen = self.read(self.read(self.home + '/studio.json')['freezes']['frozen']['path'])
        self.assertIn(self.problem, frozen['content_refs'])
        self.write(self.problem['path'], '# A different original problem\nChanged quantifiers and domain.\n')
        with self.assertRaisesRegex(ValueError, 'Stale content binding'):
            studio.promote(self.root, 'run', self.record(plan, 'publish'))

    def test_publication_declarations_automatically_freeze_all_named_evidence(self):
        proof = self.write(self.work + '/main/edge-proof.md', '# Relation proof\nComplete argument for the new edge.\n')
        plan = self.backflow(edge_evidence=[proof])
        frozen = self.read(self.read(self.home + '/studio.json')['freezes']['frozen']['path'])
        self.assertIn(proof, frozen['content_refs'])
        self.write(proof['path'], '# Relation proof\nAn unreviewed stronger argument.\n')
        with self.assertRaisesRegex(ValueError, 'Stale content binding'):
            studio.promote(self.root, 'run', self.record(plan, 'publish'))

    def test_legacy_freeze_missing_new_edge_evidence_cannot_backflow(self):
        proof = self.write(self.work + '/main/edge-proof.md', 'Actual new edge proof')
        plan = self.backflow(edge_evidence=[proof])
        index = self.read(self.home + '/studio.json')
        frozen = self.read(index['freezes']['frozen']['path'])
        frozen['content_refs'].remove(proof)
        index['freezes']['frozen'] = studio._store(self.root, 'run', 'freezes', 'frozen', frozen)
        studio._save_index(self.root, 'run', index)
        self.review('frozen', rid='legacy-review')
        plan['review_id'] = 'legacy-review'
        with self.assertRaisesRegex(ValueError, 'New edge evidence'):
            studio.promote(self.root, 'run', self.record(plan, 'publish'))

    def test_review_by_author_and_unresolved_later_objection_block_backflow(self):
        plan = self.backflow()
        with self.assertRaisesRegex(ValueError, 'nonauthor'):
            self.review('frozen', reviewer='actual-main', rid='self-review')
        self.review('frozen', verdict='changes-required', rid='objection')
        with self.assertRaisesRegex(ValueError, 'Unresolved'):
            studio.promote(self.root, 'run', self.record(plan, 'publish'))
        self.review('frozen', rid='resolved', resolves=['objection'])
        plan['review_id'] = 'resolved'
        self.assertEqual(studio.promote(self.root, 'run', self.record(plan, 'publish'))['status'], 'backflow-plan-ready-local-not-published')

    def test_backflow_builds_complete_candidate_then_existing_register_and_context_use_new_edge(self):
        self.graph()
        old_registry = (self.root / runtime.REGISTRY).read_bytes()
        plan = self.backflow()
        result = studio.promote(self.root, 'run', self.record(plan, 'publish'))
        self.assertEqual((self.root / runtime.REGISTRY).read_bytes(), old_registry)
        candidate = self.read(result['candidate_registry_ref']['path'])
        self.assertEqual(candidate['historical_field'], {'preserve': True})
        self.assertEqual({obj['object_id'] for obj in candidate['objects']}, {'A', 'B', 'C', 'X', 'Y'})
        runtime.register(self.root, result['candidate_registry_ref']['path'])
        checked = runtime.check(self.root)
        self.assertEqual(checked['edges'], 2)
        runtime.build(self.root)
        context = runtime.context(self.root, ['Y'], edge_ids=['new-support'])
        self.assertEqual(context['support_options']['Y'][0]['all_premises'], ['X'])
        fresh = frontier.frontier_report(context)
        self.assertTrue(fresh['routes'][0]['structurally_eligible'])
        body = next(obj['body'] for obj in candidate['objects'] if obj['object_id'] == 'X')
        self.write(body['path'], '# X\nChanged proof bytes after registration.\n')
        stale = frontier.frontier_report(runtime.context(self.root, ['Y'], edge_ids=['new-support']))
        self.assertFalse(stale['routes'][0]['structurally_eligible'])
        self.assertIn('bindings-require-refresh', stale['routes'][0]['structural_blockers'])
        self.assertNotIn('backflow_guard', self.read(runtime.REGISTRY))

    def test_promoted_candidate_cannot_erase_a_later_registration(self):
        self.graph()
        plan = self.backflow()
        result = studio.promote(self.root, 'run', self.record(plan, 'publish'))
        peer = self.read(runtime.REGISTRY)
        extra = self.obj('PEER')
        peer['objects'].append(extra)
        peer['materials'].append(self.material(extra))
        self.write(runtime.REGISTRY, peer)
        peer_bytes = (self.root / runtime.REGISTRY).read_bytes()
        with self.assertRaisesRegex(ValueError, 'Backflow base changed'):
            runtime.register(self.root, result['candidate_registry_ref']['path'])
        self.assertEqual((self.root / runtime.REGISTRY).read_bytes(), peer_bytes)
        refreshed = studio.promote(self.root, 'run', self.record(plan, 'publish'))
        runtime.register(self.root, refreshed['candidate_registry_ref']['path'])
        self.assertIn('PEER', {obj['object_id'] for obj in self.read(runtime.REGISTRY)['objects']})

    def test_changed_batch_or_edge_after_review_is_rejected(self):
        plan = self.backflow()
        batch = self.read(plan['registration_batch_ref']['path'])
        batch['objects'][0]['statement'] = 'A stronger unreviewed statement'
        plan['registration_batch_ref'] = self.write(plan['registration_batch_ref']['path'], batch)
        with self.assertRaisesRegex(ValueError, 'Stale content binding|reviewed frozen bytes'):
            studio.promote(self.root, 'run', self.record(plan, 'publish'))

    def test_candidate_cannot_overwrite_line_journal(self):
        plan = self.backflow()
        plan['candidate_registry_path'] = self.work + '/informed-a/journal.md'
        before = (self.root / plan['candidate_registry_path']).read_bytes()
        with self.assertRaisesRegex(ValueError, 'dedicated backflow'):
            studio.promote(self.root, 'run', self.record(plan, 'publish'))
        self.assertEqual((self.root / plan['candidate_registry_path']).read_bytes(), before)

    def test_local_contribution_can_publish_locally_and_whole_needs_reviewed_target_discharge(self):
        self.graph(partial=True)
        app = self.adopt(self.application(open_b=False, partial=True))
        plan = self.backflow(applications=[{'application_id': 'app', 'revision_pin': app['revision_pin']}])
        self.assertEqual(studio.promote(self.root, 'run', self.record(plan, 'local-publish'))['status'], 'backflow-plan-ready-local-not-published')
        plan['claim_scope'] = 'whole-target'
        with self.assertRaisesRegex(ValueError, 'target remaining'):
            studio.promote(self.root, 'run', self.record(plan, 'whole-publish'))
        plan['target_discharges'] = [{'obligation_id': 'C-global-remaining', 'argument': 'The frozen complete synthesis pays this precise remaining step',
                                     'proof_ref': self.read(self.read(self.home + '/studio.json')['freezes']['frozen']['path'])['content_refs'][0]}]
        self.assertEqual(studio.promote(self.root, 'run', self.record(plan, 'whole-publish'))['status'], 'backflow-plan-ready-local-not-published')

    def test_whole_downstream_application_preserves_upstream_contribution_remaining(self):
        registry = self.graph(partial=True)
        upstream = self.adopt(self.application('partial', open_b=False, partial=True))
        edge = copy.deepcopy(self.edge)
        edge.update(edge_id='downstream-whole', whole_result='ALL premises give the exact whole local conclusion')
        edge.pop('contribution')
        edge.update(runtime.edge_bindings(self.root, edge, self.objects))
        ref = self.write('map/edges/downstream-whole.json', edge)
        registry['edge_files'].append(ref['path'])
        self.write(runtime.REGISTRY, registry)
        child = self.application('child', open_b=False)
        child.update(edge_id=edge['edge_id'], edge_declaration_pin=runtime.pin(edge),
                     depends_on_applications=[{'application_id': 'partial', 'revision_pin': upstream['revision_pin']}])
        result = self.adopt(child)
        self.assertEqual(result['unpaid_obligation_ids'], [])
        self.assertEqual(result['target_remaining'], {'C-global-remaining': self.edge['contribution']['remaining']})
        plan = self.backflow(applications=[{'application_id': 'child', 'revision_pin': result['revision_pin']}])
        studio.promote(self.root, 'run', self.record(plan, 'local'))
        plan['claim_scope'] = 'whole-target'
        with self.assertRaisesRegex(ValueError, 'target remaining'):
            studio.promote(self.root, 'run', self.record(plan, 'whole'))

    def test_open_mathematical_obligation_can_backflow_without_claiming_target_complete(self):
        plan = self.backflow(state='open')
        result = studio.promote(self.root, 'run', self.record(plan, 'publish'))
        self.assertEqual(self.read(result['candidate_registry_ref']['path'])['objects'][0]['truth_status'], 'open')
        plan['claim_scope'] = 'whole-target'
        with self.assertRaisesRegex(ValueError, 'Whole-target'):
            studio.promote(self.root, 'run', self.record(plan, 'whole'))


if __name__ == '__main__':
    unittest.main()
