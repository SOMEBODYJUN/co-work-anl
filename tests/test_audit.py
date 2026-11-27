"""Independent regressions for failures reproduced through the public CLI."""
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class AuditCLI(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.workspace = Path(self.tmp.name)
        self.call('init')

    def tearDown(self):
        self.tmp.cleanup()

    def call(self, *args, ok=True):
        p = subprocess.run([sys.executable, str(ROOT / 'crisis.py'), '--workspace', str(self.workspace), *args],
                           capture_output=True, text=True)
        if ok:
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            return json.loads(p.stdout)
        self.assertNotEqual(p.returncode, 0, p.stdout + p.stderr)
        return p

    def write(self, path, value):
        p = self.workspace / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')
        return str(p)

    def source(self, sid='OBS', **changes):
        row = {'id': sid, 'kind': 'fact', 'url': 'https://example.org/table',
               'source_family': 'synthetic-original', 'published_at': '2026-02-01',
               'observation_period': '2026-01', 'text': 'Output = 100', 'input_kind': 'synthetic_test'}
        row.update(changes)
        return row

    def complete_phases(self):
        from cncrisis.engine import FIRST_STAGES
        for phase in FIRST_STAGES:
            name = 'research/' + phase + '.md'
            p = self.workspace / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text('Engineering fixture: ' + phase + '.\n', encoding='utf-8')
            self.call('stage', '--id', phase, '--files', name, '--note', 'Engineering test artifact saved')
        report = self.workspace / 'formal' / 'engineering.md'
        report.parent.mkdir(exist_ok=True)
        report.write_text('Engineering fixture: released files match the independently reviewed snapshot.\n')
        self.call('review', '--verdict', 'pass', '--files', 'formal/engineering.md',
                  '--reviewer', 'audit-fixture', '--author', 'author-fixture', '--note', 'Fixture review')

    def release(self, ok=True):
        return self.call('release', '--files', 'formal/engineering.md', '--judgment',
                         'Engineering fixture: all submitted artifacts are current.', ok=ok)

    def test_identical_values_in_different_months_remain_distinct(self):
        records = [self.source('JAN'), self.source('FEB', url='https://example.org/feb',
                   observation_period='2026-02', published_at='2026-03-01')]
        result = self.call('ingest', '--file', self.write('input.json', records))
        self.assertEqual(result['evidence_record_count'], 2)

    def test_fact_and_opinion_same_words_do_not_alias(self):
        result = self.call('ingest', '--file', self.write('input.json', [
            self.source('OBS'), self.source('VIEW', kind='opinion', url='https://example.org/opinion')]))
        self.assertEqual(result['evidence_record_count'], 2)

    def test_same_repost_can_be_reingested_idempotently(self):
        records = [self.source('ORIGINAL'), self.source('REPOST', url='https://example.org/repost')]
        path = self.write('input.json', records)
        first = self.call('ingest', '--file', path)
        second = self.call('ingest', '--file', path)
        self.assertEqual(first['evidence_record_count'], 1)
        self.assertEqual(second['evidence_record_count'], 1)

    def test_blank_artifact_cannot_complete_phase(self):
        (self.workspace / 'blank.md').write_text(' \n\t')
        self.call('stage', '--id', 's01_scope', '--files', 'blank.md', '--note', 'Empty artifact', ok=False)

    def test_search_reuse_respects_period_and_expiry(self):
        data = {'query': 'household debt', 'topic': 'income', 'period': '2026-01', 'results': [],
                'executed_at': (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()}
        self.call('search-log', '--file', self.write('query.json', data))
        result = self.call('search-plan', '--query', ' HOUSEHOLD   DEBT ', '--topic', 'income', '--period', '2026-01')
        self.assertEqual(result['decision'], 'reuse')
        result = self.call('search-plan', '--query', 'household debt', '--topic', 'income', '--period', '2026-02')
        self.assertEqual(result['decision'], 'search')
        result = self.call('search-plan', '--query', 'household debt', '--topic', 'income', '--period', '2026-01', '--freshness-days', '0.1')
        self.assertEqual(result['decision'], 'search')

    def test_opinion_and_unanchored_cycle_cannot_support_facts(self):
        self.call('ingest', '--file', self.write('input.json', self.source('VIEW', kind='opinion')))
        edge = lambda sid, tail, head: {'id': sid, 'tails': [tail], 'head': head, 'conditions': [],
             'mechanism': 'Engineering cycle only', 'counterevidence': [], 'falsifier': 'External observation', 'lag': 'one month'}
        graph = {'nodes': [
            {'id': 'BADFACT', 'kind': 'fact', 'statement': 'A viewpoint is not a factual observation', 'evidence': ['VIEW']},
            {'id': 'CYCLE_A', 'statement': 'A needs external grounding'},
            {'id': 'CYCLE_B', 'statement': 'B needs external grounding'}],
            'edges': [edge('EDGE_A', 'CYCLE_A', 'CYCLE_B'), edge('EDGE_B', 'CYCLE_B', 'CYCLE_A')]}
        result = self.call('graph-put', '--file', self.write('graph.json', graph))
        self.assertEqual(set(result['unresolved']), {'BADFACT', 'CYCLE_A', 'CYCLE_B'})

    def test_all_premises_are_required(self):
        self.call('ingest', '--file', self.write('input.json', self.source()))
        graph = {'nodes': [{'id': 'READY', 'statement': 'Observed premise', 'evidence': ['OBS']},
                           {'id': 'MISSING', 'statement': 'Unpaid premise'},
                           {'id': 'RESULT', 'statement': 'Needs both premises'}],
                 'edges': [{'id': 'ALL_EDGE', 'tails': ['READY', 'MISSING'], 'head': 'RESULT',
                            'conditions': [], 'mechanism': 'Both conditions needed', 'counterevidence': [],
                            'falsifier': 'One premise absent', 'lag': 'one month'}]}
        result = self.call('graph-put', '--file', self.write('graph.json', graph))
        self.assertFalse(result['nodes']['RESULT']['grounded'])
        self.assertFalse(result['edges']['ALL_EDGE']['all_premises_met'])

    def test_reject_revokes_prior_pass(self):
        self.complete_phases()
        self.call('review', '--verdict', 'reject', '--reviewer', 'audit-fixture', '--note', 'Reopened material issue')
        self.release(ok=False)

    def test_post_review_artifact_change_blocks_release(self):
        self.complete_phases()
        (self.workspace / 'formal/engineering.md').write_text('Changed after review')
        self.release(ok=False)

    def test_unregistered_formal_output_blocks_release(self):
        self.complete_phases()
        (self.workspace / 'formal/unreviewed.md').write_text('New unreviewed output')
        self.release(ok=False)

    def test_raw_source_tampering_blocks_release(self):
        self.call('ingest', '--file', self.write('input.json', self.source()))
        self.complete_phases()
        blobs = list((self.workspace / 'source_blobs').glob('*.bin'))
        self.assertEqual(len(blobs), 1)
        blobs[0].write_bytes(b'changed without source ingestion')
        self.release(ok=False)


if __name__ == '__main__':
    unittest.main()
