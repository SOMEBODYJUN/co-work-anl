"""Cross-cutting engine checks; fixtures are synthetic engineering data."""
import argparse
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from cncrisis import engine


class EngineFlows(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--workspace', default=self.root)
        engine.register_cli(self.parser.add_subparsers(required=True))
        self.call('init')

    def tearDown(self):
        self.tmp.cleanup()

    def call(self, *argv):
        a = self.parser.parse_args(list(argv))
        return a.func(a)

    def write(self, name, value):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(value), encoding='utf-8')
        return str(p)

    def source(self, sid='F1', text='Synthetic fixture value 1', kind='fact', **extra):
        row = {'id': sid, 'kind': kind, 'url': 'https://example.org/release',
               'source_family': 'fixture-origin', 'published_at': '2020-01-01',
               'observation_period': '2020Q1', 'text': text, **extra}
        if self.call('status')['nodes'] and 'targets' not in row:
            state = json.loads((self.root / 'research_state.json').read_text())
            row['targets'] = list(state['nodes'])
        return self.call('ingest', '--file', self.write('incoming.json', row))

    def graph(self, nodes, edges=None):
        return self.call('graph-put', '--file', self.write('graph.json', {'nodes': nodes, 'edges': edges or []}))

    def phases(self):
        mode = self.call('status')['mode']
        for sid in engine.FIRST_STAGES if mode == 'first' else engine.UPDATE_STAGES:
            p = self.root / 'steps' / (sid + '.md')
            p.parent.mkdir(exist_ok=True)
            p.write_text('Synthetic engineering fixture: ' + sid)
            self.call('stage', '--id', sid, '--files', str(p.relative_to(self.root)), '--note', 'Executed fixture phase')

    def release(self):
        self.phases()
        self.write('formal/report.json', {'judgment': 'Synthetic fixture conclusion, not an economic finding'})
        self.call('review', '--verdict', 'pass', '--files', 'formal/report.json', '--note', 'Fixture review', '--reviewer', 'audit-agent')
        return self.call('release', '--files', 'formal/report.json', '--judgment', 'Synthetic fixture conclusion')

    def change(self, pid, target, statement, new_statement, revision=1, **extra):
        row = {'id': pid, 'target': target, 'base_revision': revision,
               'action': 'replace', 'old_statement': statement, 'new_statement': new_statement,
               'new_evidence': ['F1'], 'reason': 'Fixture source changed and now warrants this judgment', **extra}
        self.call('proposal', '--file', self.write('proposal.json', row))
        self.call('proposal-review', '--id', pid, '--verdict', 'pass', '--reviewer', 'audit-agent', '--note', 'Independently inspected fixture delta')
        return self.call('apply', '--id', pid)

    def test_reposts_and_search_reuse_keep_event_lineage(self):
        self.source(event_id='event-a')
        res = self.source('REPOST', source_family='repost-site', url='https://another.org/story?utm_source=x')
        self.assertEqual(res['records'][0]['status'], 'duplicate')
        self.assertEqual(res['evidence_record_count'], 1)
        self.assertEqual(engine.canonical_url('https://example.org/release/?b=2&utm_source=x&a=1#top'), 'https://example.org/release?a=1&b=2')
        self.call('search-log', '--file', self.write('search.json', {'query': '  POLICY  release ', 'topic': 'fiscal', 'period': '2020', 'results': []}))
        res = self.call('search-plan', '--query', 'policy release', '--topic', 'fiscal', '--period', '2020')
        self.assertEqual(res['decision'], 'reuse')
        self.assertEqual(self.call('search-plan', '--query', 'policy release', '--topic', 'fiscal', '--period', '2021')['decision'], 'search')

    def test_statistics_period_kind_and_publication_counts_survive_dedup(self):
        self.source('JAN', text='Same published value', observation_period='2020-01', published_at='2020-02-01')
        res = self.source('FEB', text='Same published value', observation_period='2020-02', published_at='2020-03-01')
        self.assertEqual(res['evidence_record_count'], 2)
        self.assertEqual(res['publication_count'], 2)
        res = self.source('ANOTHER_METRIC', text='Different metric from same publication', observation_period='2020-02', published_at='2020-03-01')
        self.assertEqual(res['evidence_record_count'], 3)
        self.assertEqual(res['publication_count'], 2)
        res = self.source('OPINION', text='Same published value', kind='opinion', observation_period='2020-02', published_at='2020-03-01')
        self.assertEqual(res['evidence_record_count'], 4)
        self.source('COPY', text='Same published value', observation_period='2020-02', published_at='2020-03-01')
        res = self.source('COPY', text='Same published value', observation_period='2020-02', published_at='2020-03-01')
        self.assertEqual(res['records'][0]['status'], 'unchanged')

    def test_proposal_review_and_new_counterevidence_cannot_be_bypassed(self):
        self.source()
        self.graph([{'id': 'J1', 'statement': 'Old fixture judgment', 'evidence': ['F1']}])
        p = {'id': 'P1', 'target': 'J1', 'base_revision': 1, 'action': 'retain',
             'old_statement': 'Old fixture judgment', 'new_statement': 'Old fixture judgment',
             'new_evidence': ['F1'], 'reason': 'The fixture argument was independently examined'}
        self.call('proposal', '--file', self.write('p.json', p))
        with self.assertRaisesRegex(engine.EngineError, 'accepted review'):
            self.call('apply', '--id', 'P1')
        self.call('proposal-review', '--id', 'P1', '--verdict', 'pass', '--reviewer', 'audit-agent', '--note', 'Initial fixture review')
        self.source('NEW', 'New opposing fixture observation', targets=['J1'])
        with self.assertRaisesRegex(engine.EngineError, 'accepted review'):
            self.call('apply', '--id', 'P1')
        self.call('proposal-review', '--id', 'P1', '--verdict', 'reject', '--reviewer', 'audit-agent', '--note', 'The newly admitted evidence defeats this proposal')
        state = json.loads((self.root / 'research_state.json').read_text())
        self.assertEqual(state['proposals']['P1']['status'], 'rejected')
        incoming = {'id': 'NO_TARGET', 'kind': 'opinion', 'url': 'fixture://commentator',
                    'source_family': 'commentator', 'published_at': '2020-02-01', 'text': 'A different interpretation'}
        with self.assertRaisesRegex(engine.EngineError, 'explicit targets'):
            self.call('ingest', '--file', self.write('missing_target.json', incoming))

    def test_all_premises_cycles_and_opinions(self):
        self.source()
        self.source('V1', 'A commentator expects distress', kind='opinion')
        edges = [{'id': 'H1', 'tails': ['F1', 'C2'], 'head': 'C1', 'conditions': [],
                  'counterevidence': [], 'mechanism': 'Joint synthetic premises', 'falsifier': 'Fixture fails', 'lag': 'One fixture step'},
                 {'id': 'H2', 'tails': ['C1'], 'head': 'C2', 'conditions': [],
                  'counterevidence': [], 'mechanism': 'Circular fixture', 'falsifier': 'Independent observation', 'lag': 'One step'}]
        res = self.graph([{'id': 'C1', 'kind': 'judgment', 'statement': 'Cycle one'},
                          {'id': 'C2', 'kind': 'judgment', 'statement': 'Cycle two'},
                          {'id': 'BADFACT', 'kind': 'fact', 'statement': 'Opinion treated as fact', 'evidence': ['V1']}], edges)
        self.assertEqual(set(res['unresolved']), {'C1', 'C2', 'BADFACT'})
        self.assertEqual(res['edges']['H1']['missing'], ['C2'])

    def test_source_change_invalidates_transitive_conclusions(self):
        self.source()
        self.graph([{'id': 'J1', 'kind': 'judgment', 'statement': 'First', 'evidence': ['F1']},
                    {'id': 'J2', 'kind': 'judgment', 'statement': 'Second', 'evidence': ['J1']}])
        res = self.source(text='Synthetic fixture value 2')
        self.assertEqual(res['needs_review'], ['J1', 'J2'])
        self.change('P1', 'J1', 'First', 'First revised')
        self.assertEqual(self.call('graph-status')['unresolved'], ['J2'])
        self.change('P2', 'J2', 'Second', 'Second revised', new_evidence=['J1'])
        self.assertEqual(self.call('graph-status')['unresolved'], [])

    def test_proposal_revision_cas_and_reversal_memory(self):
        self.source()
        self.graph([{'id': 'J1', 'statement': 'A', 'evidence': ['F1']}])
        p = {'id': 'P-stale', 'target': 'J1', 'base_revision': 1, 'action': 'replace',
             'old_statement': 'A', 'new_statement': 'C', 'new_evidence': ['F1'], 'reason': 'Different fixture route'}
        self.call('proposal', '--file', self.write('p.json', p))
        self.change('P1', 'J1', 'A', 'B')
        with self.assertRaisesRegex(engine.EngineError, 'Target changed'):
            self.call('apply', '--id', 'P-stale')
        with self.assertRaisesRegex(engine.EngineError, 'reversal'):
            self.change('P2', 'J1', 'B', 'A', revision=2)
        self.change('P3', 'J1', 'B', 'A', revision=2, responds_to=['P1'])
        state = json.loads((self.root / 'research_state.json').read_text())
        self.assertEqual(state['nodes']['J1']['revision'], 3)
        self.assertEqual(state['proposals']['P1']['new_statement'], 'B')

    def test_review_rejection_and_changed_artifacts_block_release(self):
        self.source()
        self.release()
        self.call('review', '--verdict', 'reject', '--note', 'Found a material fixture error')
        with self.assertRaisesRegex(engine.EngineError, 'accepted current'):
            self.call('release', '--files', 'formal/report.json', '--judgment', 'Fixture judgment')
        self.call('review', '--verdict', 'pass', '--files', 'formal/report.json', '--note', 'Rechecked')
        (self.root / 'formal/report.json').write_text('Changed after review')
        with self.assertRaisesRegex(engine.EngineError, 'changed after'):
            self.call('release', '--files', 'formal/report.json', '--judgment', 'Fixture judgment')

    def test_raw_source_bytes_and_unregistered_formal_file_block_release(self):
        self.source()
        self.release()
        self.write('formal/unregistered.json', {'important': 'unreviewed output'})
        with self.assertRaisesRegex(engine.EngineError, 'Unregistered'):
            self.call('release', '--files', 'formal/report.json', '--judgment', 'Fixture judgment')
        (self.root / 'formal/unregistered.json').unlink()
        state = json.loads((self.root / 'research_state.json').read_text())
        (self.root / state['sources']['F1']['blob']).write_text('tampered raw text')
        with self.assertRaisesRegex(engine.EngineError, 'Raw source bytes changed'):
            self.call('release', '--files', 'formal/report.json', '--judgment', 'Fixture judgment')

    def test_stage_file_change_and_sequence_are_enforced(self):
        self.write('scope.md', {'scope': 'fixture'})
        with self.assertRaisesRegex(engine.EngineError, 'earlier stages'):
            self.call('stage', '--id', engine.FIRST_STAGES[1], '--files', 'scope.md', '--note', 'Too early')
        self.phases()
        (self.root / 'steps/s07_property.md').write_text('Changed stage output')
        status = self.call('status')
        self.assertEqual(len(status['completed_stages']), 6)
        self.assertIn('s20_release', status['remaining_stages'])

    def test_first_and_incremental_cycle_preserves_search_graph_and_history(self):
        self.source()
        self.graph([{'id': 'J1', 'statement': 'Synthetic engineering judgment A', 'evidence': ['F1']}])
        first = self.release()
        self.assertEqual(first['cycle'], 1)
        self.call('init', '--mode', 'update')
        self.assertEqual(self.call('status')['nodes'], 1)
        self.source(text='Synthetic engineering value changed')
        self.change('P-update', 'J1', 'Synthetic engineering judgment A', 'Synthetic engineering judgment B')
        second = self.release()
        self.assertEqual(second['cycle'], 2)
        state = json.loads((self.root / 'research_state.json').read_text())
        self.assertTrue(any(x['event'] == 'begin_update' and x['prior_release']['cycle'] == 1 for x in state['history']))
        self.assertEqual(len(state['sources']['F1']['versions']), 1)

    def test_update_cannot_adopt_a_stale_release_as_its_baseline(self):
        self.source()
        self.release()
        (self.root / 'formal/report.json').write_text('Modified after release without new review')
        with self.assertRaisesRegex(engine.EngineError, 'Repair the current cycle before update'):
            self.call('init', '--mode', 'update')
        state = json.loads((self.root / 'research_state.json').read_text())
        self.assertEqual(state['mode'], 'first')
        self.assertEqual(state['cycle'], 1)

    def test_path_escape_and_writer_lock(self):
        self.write('p.json', {})
        with self.assertRaisesRegex(engine.EngineError, 'inside workspace'):
            self.call('stage', '--id', engine.FIRST_STAGES[0], '--files', '../outside.md', '--note', 'Invalid path')
        (self.root / '.engine.lock').write_text('another writer')
        with self.assertRaisesRegex(engine.EngineError, 'locked'):
            self.call('status')
        (self.root / '.engine.lock').unlink()


if __name__ == '__main__':
    unittest.main()
