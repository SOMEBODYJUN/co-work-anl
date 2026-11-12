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

    def init(self, name, problem_id, definitions=None, mode='open'):
        spec = {'problem_id': problem_id, 'problem': self.problem,
                'definitions': definitions if definitions is not None else [self.definition],
                'obstacles': [], 'seed_ids': []}
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
        resumed = runtime.resume(self.root, 'comparison')
        self.assertIsNone(resumed['collaboration'])
        self.assertEqual(set(resumed['packet_bindings']), {'obstacle', 'full'})
        self.assertTrue(all(v['status'] == 'current' for v in resumed['packet_bindings'].values()))
        self.assertFalse(resumed['recovery_warnings'])


if __name__ == '__main__':
    unittest.main()
