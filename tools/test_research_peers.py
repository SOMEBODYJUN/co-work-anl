"""Same-target discovery and actual worker metadata, independent of display IDs."""
import json
from pathlib import Path
import tempfile
import unittest

import research_runtime as runtime


class ResearchPeerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=Path.cwd())
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.problem = self.write('problem.md', '# Target\nEvery finite instance.\n')
        self.definition = self.write('definition.md', '# Model\nFull ordered histories.\n')

    def write(self, name, value):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value if isinstance(value, str) else json.dumps(value), encoding='utf-8')
        return {'path': name, 'sha256': runtime.digest(path.read_bytes())}

    def init(self, name, problem_id, definitions=None, mode='open', scope=None):
        spec = {'problem_id': problem_id, 'problem': self.problem,
                'definitions': definitions if definitions is not None else [self.definition],
                'obstacles': [], 'seed_ids': []}
        if scope is not None:
            spec['collaboration_scope'] = scope
        self.write(name + '.json', spec)
        return runtime.init_run(self.root, name, name + '.json', mode=mode)

    def test_same_saved_sources_match_despite_different_problem_ids_and_changed_spec(self):
        self.init('one', 'display-one')
        self.init('two', 'display-two')
        result = runtime.peers(self.root, 'one')
        self.assertEqual({x['run_id'] for x in result['peer_runs']}, {'one', 'two'})
        self.assertEqual(result['shared_workspace'], runtime.peers(self.root, 'two')['shared_workspace'])
        # The original input, not an edited present-day spec, defines the run.
        self.write('two.json', {'problem': 'changed'})
        self.assertEqual(result['input_fingerprint'], runtime.peers(self.root, 'two')['input_fingerprint'])

    def test_archive_and_nested_subarchive_route_is_the_same_at_init_peers_and_resume(self):
        scopes = ['archives/game', 'archives/game/subarchives/child',
                  'archives/game/subarchives/child/subarchives/grandchild']
        for index, scope in enumerate(scopes):
            with self.subTest(scope=scope):
                self.problem = self.write(scope + '/problem.md', '# Target\nEvery finite instance.\n')
                initialized = self.init('run-' + str(index), 'target')['collaboration']
                discovered = runtime.peers(self.root, 'run-' + str(index))
                restored = runtime.resume(self.root, 'run-' + str(index))['collaboration']
                expected = scope + '/collaboration/P-' + discovered['input_fingerprint'][:24] + '/README.md'
                self.assertEqual(discovered['status'], 'ready')
                self.assertEqual(discovered['collaboration_scope'], scope)
                self.assertEqual(initialized['shared_entry'], expected)
                self.assertEqual(discovered['shared_entry'], expected)
                self.assertEqual(restored['shared_entry'], expected)
                self.assertFalse((self.root / expected).exists())

    def test_workspace_scope_is_saved_in_packet_and_does_not_change_fingerprint(self):
        self.problem = self.write('research/workspaces/one/problem.md', '# Target\nEvery finite instance.\n')
        self.init('one', 'target', scope='archives/game/subarchives/child')
        packet_path = self.root / 'research/runs/one/packet-full.json'
        original_packet = packet_path.read_bytes()
        packet = json.loads(original_packet)
        self.assertEqual(packet['collaboration_scope'], 'archives/game/subarchives/child')
        result = runtime.peers(self.root, 'one')
        self.assertEqual(result['input_fingerprint'], runtime.pin(result['inputs']))
        edited = json.loads((self.root / 'one.json').read_text())
        edited['collaboration_scope'] = 'archives/other'
        self.write('one.json', edited)
        self.assertEqual(runtime.resume(self.root, 'one')['collaboration']['shared_entry'], result['shared_entry'])
        self.assertEqual(packet_path.read_bytes(), original_packet)

    def test_archived_problem_cannot_override_its_deepest_canonical_scope(self):
        canonical = 'archives/game/subarchives/child/subarchives/grandchild'
        self.problem = self.write(canonical + '/problem.md', '# Target\nEvery finite instance.\n')
        for index, scope in enumerate(['archives/game', 'archives/game/subarchives/child', 'archives/other']):
            with self.subTest(scope=scope), self.assertRaisesRegex(ValueError, 'conflicts with the problem archive'):
                self.init('wrong-' + str(index), 'target', scope=scope)
        result = self.init('canonical', 'target', scope=canonical)['collaboration']
        self.assertEqual(result['collaboration_scope'], canonical)
        self.assertEqual(result['status'], 'ready')
        self.assertEqual(result['scope_conflicts'], [])
        self.problem = self.write('archives/game/problem.md', '# Parent target\n')
        with self.assertRaisesRegex(ValueError, 'conflicts with the problem archive'):
            self.init('wrong-child', 'target', scope='archives/game/subarchives/child')

    def test_workspace_scope_conflicts_are_explicit_without_changing_packets_or_fingerprint(self):
        self.problem = self.write('research/workspaces/shared/problem.md', '# Target\nEvery finite instance.\n')
        self.init('one', 'target', scope='archives/game')
        self.init('two', 'target', scope='archives/game/subarchives/child')
        self.init('unknown', 'target')
        packets = [self.root / 'research/runs' / name / 'packet-full.json' for name in ('one', 'two', 'unknown')]
        original = [path.read_bytes() for path in packets]
        first = runtime.peers(self.root, 'one')
        second = runtime.resume(self.root, 'two')['collaboration']
        self.assertEqual(first['input_fingerprint'], second['input_fingerprint'])
        self.assertEqual(first['status'], 'scope-conflict')
        self.assertEqual(second['status'], 'scope-conflict')
        self.assertNotEqual(first['shared_entry'], second['shared_entry'])
        self.assertEqual({row['run_id'] for row in first['scope_conflicts']}, {'one', 'two'})
        self.assertEqual({row['shared_entry'] for row in first['scope_conflicts']},
                         {first['shared_entry'], second['shared_entry']})
        self.assertIn('agree one current board', first['instruction'])
        self.assertEqual(first['legacy_shared_entry'], second['legacy_shared_entry'])
        unknown = runtime.peers(self.root, 'unknown')
        self.assertEqual(unknown['status'], 'scope-required')
        self.assertIsNone(unknown['shared_entry'])
        self.assertEqual(unknown['scope_conflicts'], first['scope_conflicts'])
        self.assertEqual([path.read_bytes() for path in packets], original)

    def test_unknown_scope_continues_without_root_board_or_definition_guessing(self):
        self.problem = self.write('research/workspaces/one/problem.md', '# Target\nEvery finite instance.\n')
        self.definition = self.write('archives/other/subarchives/unrelated/definition.md', '# Model\n')
        result = self.init('one', 'target')['collaboration']
        self.assertEqual(result['status'], 'scope-required')
        self.assertIsNone(result['collaboration_scope'])
        self.assertIsNone(result['shared_entry'])
        self.assertIsNone(result['shared_workspace'])
        self.assertFalse(result['shared_entry_exists'])
        self.assertTrue(result['legacy_shared_entry'].startswith('research/collaboration/P-'))
        self.assertEqual(runtime.resume(self.root, 'one')['collaboration']['status'], 'scope-required')

    def test_legacy_packet_scope_comes_from_saved_problem_not_live_spec(self):
        scope = 'archives/game/subarchives/child'
        self.problem = self.write(scope + '/problem.md', '# Target\nEvery finite instance.\n')
        self.init('one', 'target')
        packet_path = self.root / 'research/runs/one/packet-full.json'
        packet = json.loads(packet_path.read_text())
        packet.pop('input_refs')
        self.write(packet_path.relative_to(self.root).as_posix(), packet)
        run_path = runtime.run_path(self.root, 'one')
        run = json.loads(run_path.read_text())
        # Reproduce the pre-input_refs packet format, with its original pin.
        run['packet_pins']['full'] = runtime.pin(packet)
        self.write(run_path.relative_to(self.root).as_posix(), run)
        before = packet_path.read_bytes()
        result = runtime.peers(self.root, 'one')
        self.assertEqual(result['collaboration_scope'], scope)
        self.assertEqual(packet_path.read_bytes(), before)

    def test_same_path_target_revisions_have_their_own_board_and_are_not_exact_peers(self):
        self.problem = self.write('archives/game/problem.md', '# Target\nOriginal formulation.\n# Variant\nOther formulation.\n')
        self.init('old', 'target')
        old = runtime.peers(self.root, 'old')
        self.problem = dict(self.problem, section='Target')
        self.init('section', 'target')
        self.problem = self.write('archives/game/problem.md', '# Target\nCorrected formulation.\n')
        self.init('revision', 'target')
        revised = runtime.peers(self.root, 'revision')
        self.assertEqual([x['run_id'] for x in revised['peer_runs']], ['revision'])
        rows = {row['run_id']: row for row in revised['same_target_revisions']}
        self.assertEqual(set(rows), {'old', 'section'})
        self.assertEqual(rows['old']['shared_entry'], old['shared_entry'])
        self.assertEqual(rows['old']['legacy_shared_entry'], old['legacy_shared_entry'])
        self.assertNotEqual(rows['old']['shared_entry'], revised['shared_entry'])
        self.assertIn('check their mathematical relationship', rows['old']['instruction'])
        old_now = runtime.peers(self.root, 'old')
        self.assertEqual(old_now['input_fingerprint'], old['input_fingerprint'])
        self.assertEqual({x['run_id'] for x in old_now['same_target_revisions']}, {'revision', 'section'})

    def test_scope_rejects_non_archive_and_unsafe_paths(self):
        for index, scope in enumerate(['research/collaboration', 'archives/game/state',
                                       '../archives/game', '/archives/game']):
            with self.subTest(scope=scope), self.assertRaises(ValueError):
                self.init('invalid-' + str(index), 'target', scope=scope)

    def test_definition_order_ignored_but_section_and_definition_changes_are_separate(self):
        another = self.write('another.md', '# Other\nA definition.\n')
        self.init('one', 'same-label', [self.definition, another])
        self.init('two', 'other-label', [another, self.definition])
        self.init('three', 'same-label', [self.definition])
        self.init('four', 'same-label', [dict(self.definition, section='Model'), another])
        result = runtime.peers(self.root, 'one')
        self.assertEqual({x['run_id'] for x in result['peer_runs']}, {'one', 'two'})
        self.assertEqual({x['run_id'] for x in result['same_target_different_definitions']}, {'three', 'four'})

    def test_unrelated_or_corrupt_peer_cannot_block_saved_target(self):
        self.init('one', 'target')
        self.problem = self.write('other-target.md', '# Different target\n')
        self.init('two', 'target')
        self.init('broken', 'broken')
        self.write('research/runs/broken/packet-full.json', {'edited': True})
        result = runtime.peers(self.root, 'one')
        self.assertEqual([x['run_id'] for x in result['peer_runs']], ['one'])
        self.assertEqual(len(result['discovery_warnings']), 1)

    def test_open_defaults_and_real_launch_metadata_survive_save_and_feedback(self):
        result = self.init('one', 'target')
        self.assertEqual(result['agents_launched'], 0)
        packet = json.loads((self.root / 'research/runs/one/packet-full.json').read_text())
        self.assertEqual({k: packet['launch'][k] for k in runtime.WORKER_LAUNCH}, runtime.WORKER_LAUNCH)
        self.write('note.md', '# New inequality\nExact proof and next step.\n')
        runtime.update_run(self.root, 'one', 'lemma', 'full', 'note.md', 'Pay remaining term', 'working',
                           agent_id='/root/lemma', model='chosen-model', reasoning_effort='ultra', fork_turns='none')
        runtime.update_run(self.root, 'one', 'lemma', 'full', 'note.md', 'Check premise', 'needs-feedback',
                           feedback='Resolve the shared-history assumption')
        saved = json.loads(runtime.run_path(self.root, 'one').read_text())
        self.assertEqual(saved['solvers']['lemma']['launch']['model'], 'chosen-model')
        self.assertTrue(saved['solvers']['lemma']['feedback_pending'])
        resumed = runtime.resume(self.root, 'one')
        self.assertTrue(resumed['collaboration'])
        self.assertEqual(resumed['pending_feedback']['lemma'], 'Resolve the shared-history assumption')
        # A replacement agent's model must not be invented from the old worker.
        runtime.update_run(self.root, 'one', 'lemma', 'full', 'note.md', 'Continue', 'working', agent_id='/root/replacement')
        saved = json.loads(runtime.run_path(self.root, 'one').read_text())
        self.assertNotIn('launch', saved['solvers']['lemma'])

    def test_peer_discovery_failure_does_not_block_recoverable_notes(self):
        self.init('one', 'target')
        self.write('note.md', '# Established part\nStill recover this proof.\n')
        runtime.update_run(self.root, 'one', 'lemma', 'full', 'note.md', 'Continue', 'working', agent_id='/root/lemma')
        path = self.root / 'research/runs/one/packet-full.json'
        packet = json.loads(path.read_text())
        packet['task'] = 'Changed after publication'
        self.write(path.relative_to(self.root).as_posix(), packet)
        result = runtime.resume(self.root, 'one')
        self.assertEqual(result['collaboration']['status'], 'input-recovery-required')
        self.assertEqual(result['event_history']['lemma'][0]['note_binding']['status'], 'current')
        self.assertTrue(result['recovery_warnings'])

    def test_comparison_packets_keep_their_original_inputs_and_no_peer_injection(self):
        self.init('open', 'target')
        initialized = self.init('comparison', 'target', mode='comparison')
        self.assertIsNone(initialized['collaboration'])
        self.assertEqual(initialized['solver_count'], 3)
        packet_paths = [self.root / 'research/runs/comparison' / ('packet-' + profile + '.json')
                        for profile in ('obstacle', 'full')]
        packet_bytes = [path.read_bytes() for path in packet_paths]
        resumed = runtime.resume(self.root, 'comparison')
        self.assertIsNone(resumed['collaboration'])
        self.assertEqual(set(resumed['packet_bindings']), {'obstacle', 'full'})
        self.assertTrue(all(v['status'] == 'current' for v in resumed['packet_bindings'].values()))
        self.assertFalse(resumed['recovery_warnings'])
        self.assertEqual([path.read_bytes() for path in packet_paths], packet_bytes)


if __name__ == '__main__':
    unittest.main()
