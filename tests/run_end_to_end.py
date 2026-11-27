#!/usr/bin/env python3
"""Actual CLI, Git, clone, and replay rehearsal using a synthetic household.

No result in this script is a forecast for China or a real household. The actor
names are fixture identities exercising the interface, not simulated LLM calls.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
FIRST = 's01_scope s02_inventory s03_acquisition s04_vintages s05_methods s06_viewpoints s07_property s08_fiscal s09_households s10_banks s11_external s12_history s13_graph s14_models s15_adversarial s16_verdict s17_writing s18_calculator s19_audit s20_release'.split()
UPDATE = 'i01_restore i02_delta i03_research i04_proposal i05_review i06_merge i07_replay i08_release'.split()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n' if not isinstance(value, str) else value,
                    encoding='utf-8')


def shell(*args, cwd=None):
    p = subprocess.run([str(x) for x in args], cwd=cwd, capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(' '.join(map(str, args)) + '\n' + p.stdout + p.stderr)
    return p.stdout.strip()


def cash_test(income):
    cash = 12000
    rows = []
    failure = None
    for month in range(1, 121):
        cash += income - 9000 - 1000
        rows.append({'month': month, 'cash': cash})
        if cash < 0:
            failure = month
            break
    return {'input_kind': 'synthetic_engineering_fixture', 'income': income, 'opening_cash': 12000,
            'living_cost': 9000, 'debt_service': 1000, 'first_shortfall_month': failure, 'rows': rows,
            'rule': 'Stop at first cash shortfall; no automatic borrowing or terminal wealth after failure.'}


class Rehearsal:
    def __init__(self, repo):
        self.repo = repo
        self.w = repo / 'work' / 'engineering'
        self.commands = 0
        self.blocks = []

    def cli(self, *args, rejected=False):
        self.commands += 1
        p = subprocess.run([sys.executable, str(self.repo / 'work.py'), '--workspace', str(self.w), *map(str, args)],
                           capture_output=True, text=True)
        if rejected:
            if not p.returncode:
                raise AssertionError('Expected rejection: ' + repr(args) + '\n' + p.stdout)
            self.blocks.append({'command': list(map(str, args)), 'error': p.stderr.strip()})
            return None
        if p.returncode:
            raise RuntimeError(repr(args) + '\n' + p.stdout + p.stderr)
        return json.loads(p.stdout)

    def input(self, name, value):
        path = self.w / 'research' / name
        save(path, value)
        return path

    def phase(self, phase, note):
        path = 'research/phases/' + phase + '.md'
        save(self.w / path, '# Synthetic engineering rehearsal\n\n' + note + '\n')
        return self.cli('stage', '--id', phase, '--files', path, '--note', note)

    def review(self):
        names = sorted(str(p.relative_to(self.w)) for p in (self.w / 'formal').rglob('*') if p.is_file())
        return self.cli('review', '--verdict', 'pass', '--files', *names, '--reviewer', 'fixture-reviewer',
                        '--author', 'fixture-author', '--note', 'Engineering inputs, calculations and versions reconciled')

    def release(self, judgment):
        names = sorted(str(p.relative_to(self.w)) for p in (self.w / 'formal').rglob('*') if p.is_file())
        return self.cli('release', '--files', *names, '--judgment', judgment)

    def inspect_proposal(self, pid, verdict='pass'):
        return self.cli('proposal-review', '--id', pid, '--verdict', verdict,
                        '--reviewer', 'fixture-reviewer', '--note', 'Independent fixture calculation and prior reasoning compared')


def main(output):
    with tempfile.TemporaryDirectory(prefix='cncrisis-e2e-') as temp:
        base = Path(temp)
        repo = base / 'source'
        repo.mkdir()
        for filename in ['crisis.py', 'work.py']:
            shutil.copy2(ROOT / filename, repo / filename)
        shutil.copytree(ROOT / 'cncrisis', repo / 'cncrisis', ignore=shutil.ignore_patterns('__pycache__'))
        shell('git', 'init', '-q', '-b', 'work/cn-crisis', repo)
        shell('git', 'config', 'user.name', 'Engineering Fixture', cwd=repo)
        shell('git', 'config', 'user.email', 'fixture@example.invalid', cwd=repo)
        r = Rehearsal(repo)
        r.cli('init')
        source = lambda sid, text: {'id': sid, 'kind': 'fact', 'url': 'https://example.invalid/' + sid,
            'source_family': 'synthetic-fixture', 'published_at': '2026-11-01', 'observation_period': 'test-month-1',
            'text': text, 'event_id': 'SYNTHETIC-CASHFLOW', 'input_kind': 'synthetic_engineering_fixture'}
        records = [source('INCOME', 'Synthetic monthly income CNY 8000'),
                   source('COST', 'Synthetic monthly living and contractual costs CNY 10000'),
                   source('START', 'Synthetic opening liquid cash CNY 12000')]
        intake = r.input('sources.json', records)
        r.cli('ingest', '--file', intake)
        query = {'query': 'synthetic household cashflow', 'topic': 'engineering', 'period': 'test-month-1',
                 'results': [], 'status': 'zero_results', 'input_kind': 'synthetic_engineering_fixture'}
        r.cli('search-log', '--file', r.input('search.json', query))
        cached = r.cli('search-plan', '--query', query['query'], '--topic', 'engineering', '--period', 'test-month-1')
        assert cached['decision'] == 'reuse'
        assert r.cli('search-plan', '--query', query['query'], '--topic', 'engineering', '--period', 'test-month-2')['decision'] == 'search'
        first_result = cash_test(8000)
        assert first_result['first_shortfall_month'] == 7
        first_statement = '合成测试家庭在给定收入8000元、月支出10000元、现金12000元下，第7月出现现金缺口。'
        edge = {'id': 'FLOW', 'tails': ['INCOME', 'COST', 'START'], 'head': 'CASH_VERDICT', 'mode': 'ALL',
                'conditions': ['Synthetic fixed monthly amounts; no additional financing'],
                'mechanism': 'Cash decreases by CNY 2000 per month; month seven first falls below zero.',
                'counterevidence': [], 'falsifier': 'A change in actual income, cash, expenditure or financing terms', 'lag': 'monthly'}
        graph = {'nodes': [{'id': 'CASH_VERDICT', 'kind': 'judgment', 'statement': first_statement,
                            'evidence': ['INCOME', 'COST', 'START']}], 'edges': [edge]}
        assert not r.cli('graph-put', '--file', r.input('graph.json', graph))['unresolved']
        params = {'input_kind': 'synthetic_engineering_fixture', 'income': 8000}
        save(r.w / 'research/parameters.json', params)
        replay = '''import json,sys\nfrom pathlib import Path\np=json.loads(Path(sys.argv[1]).read_text());cash=12000;rows=[];failure=None\nfor month in range(1,121):\n cash+=p['income']-9000-1000;rows.append({'month':month,'cash':cash})\n if cash<0: failure=month;break\nr={'input_kind':'synthetic_engineering_fixture','income':p['income'],'opening_cash':12000,'living_cost':9000,'debt_service':1000,'first_shortfall_month':failure,'rows':rows,'rule':'Stop at first cash shortfall; no automatic borrowing or terminal wealth after failure.'}\nPath(sys.argv[2]).write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\\n')\n'''
        save(r.w / 'research/replay.py', replay)
        save(r.w / 'formal/results.json', first_result)
        save(r.w / 'formal/report.md', '# 合成工程演练\n\n' + first_statement + '\n\n此文件仅验证工程，不是中国危机报告。\n')
        save(r.w / 'formal/calculator.html', '''<!doctype html><meta charset="utf-8"><title>合成现金流演练</title><h1>合成工程测试</h1><label>月收入<input id="income" type="number" value="8000"></label><button onclick="run()">重算</button><p id="result"></p><script>function run(){let cash=12000,month=0;while(cash>=0&&month<120){month++;cash+=Number(document.getElementById('income').value)-10000;}document.getElementById('result').textContent=cash<0?'第'+month+'月出现现金缺口':'120个月无缺口';}run();</script>''')
        phase_notes = [
            'Scope is a controlled cashflow and recovery exercise; no macro forecast.',
            'Three synthetic observations, one family and one event; originals retained.',
            'Intake and zero-result search memory stored; next period refreshes.',
            'CNY monthly flows and initial stock kept separate.',
            'Monthly cash identity and deterministic replay selected.',
            'Analyst interpretation separated from synthetic observations.',
            'No property asset is assumed in the fixture.',
            'No fiscal relief is included in the fixture.',
            'Income 8000, living 9000, debt service 1000, opening cash 12000.',
            'No automatic borrowing is introduced when liquid cash fails.',
            'No external-policy or investment gains are assumed.',
            'No historical economic case is inferred from a synthetic fixture.',
            'ALL edge requires all three stock/flow inputs; source IDs remain shared.',
            'Independent arithmetic identifies first shortfall in month seven.',
            'No post-failure terminal wealth is reported; omitted income is not invented.',
            first_statement,
            'A concrete engineering report states the result and its exact inputs.',
            'The small offline fixture calculator recomputes monthly cash from its income input.',
            'Version, arithmetic and raw-blob integrity checked for the engineering fixture.',
            'All engineering artifacts retained for a fresh-clone replay.'
        ]
        for phase, note in zip(FIRST, phase_notes):
            r.phase(phase, note)
        r.review()
        r.cli('review', '--verdict', 'reject', '--reviewer', 'fixture-reviewer', '--note', 'Test revocation of prior pass')
        r.cli('release', '--files', 'formal/report.md', '--judgment', first_statement, rejected=True)
        r.review()
        original_report = (r.w / 'formal/report.md').read_text()
        save(r.w / 'formal/report.md', original_report + '\nChanged after review.\n')
        r.cli('release', '--files', 'formal/report.md', '--judgment', first_statement, rejected=True)
        save(r.w / 'formal/report.md', original_report)
        r.review()
        first_release = r.release(first_statement)
        r.cli('checkpoint', '--paths', 'crisis.py', 'work.py', 'cncrisis', 'work/engineering', '--message', 'Complete synthetic first-cycle rehearsal')
        clone = base / 'recovered'
        shell('git', 'clone', '--quiet', '--no-hardlinks', repo, clone)
        restored = Rehearsal(clone)
        assert restored.cli('status')['release']['current']
        replay_path = clone / 'work/engineering/research/replay.py'
        shell(sys.executable, replay_path, restored.w / 'research/parameters.json', base / 'first-replayed.json')
        assert json.loads((base / 'first-replayed.json').read_text()) == first_result
        restored.cli('init', '--mode', 'update')
        restored.phase(UPDATE[0], 'Recovered prior release, accepted mechanisms and earlier search scope from an independent clone.')
        new_income = {**records[0], 'text': 'Synthetic revised monthly income CNY 9000', 'targets': ['CASH_VERDICT'], 'vintage': 'revised'}
        changed = restored.cli('ingest', '--file', restored.input('updated_income.json', new_income))
        assert 'CASH_VERDICT' in changed['needs_review']
        stale = restored.cli('graph-status')
        assert stale['nodes']['CASH_VERDICT']['status'] == 'needs_review'
        assert stale['edges']['FLOW']['status'] == 'needs_review'
        restored.phase(UPDATE[1], 'Only synthetic income changes; three old source IDs and cached query remain available.')
        second_result = cash_test(9000)
        assert second_result['first_shortfall_month'] == 13
        restored.phase(UPDATE[2], 'Independent monthly arithmetic changes the first shortfall from month seven to month thirteen.')
        new_statement = '合成测试收入修订至9000元后，其他条件相同，第13月出现现金缺口。'
        wrong = {'id': 'P_BAD', 'target': 'CASH_VERDICT', 'author': 'fixture-author', 'base_revision': 1,
                 'action': 'replace', 'old_statement': first_statement, 'new_statement': 'Synthetic cash lasts forever.',
                 'new_method': 'Intentionally wrong alternative for rejection test', 'reason': 'Fixture to exercise explicit rejection history'}
        restored.cli('proposal', '--file', restored.input('rejected_proposal.json', wrong))
        restored.inspect_proposal('P_BAD', 'reject')
        edge2 = {**edge, 'mechanism': 'Cash decreases by CNY 1000 per month; month thirteen first falls below zero.'}
        ep = {'id': 'P_EDGE', 'target': 'FLOW', 'author': 'fixture-author', 'base_revision': 1, 'action': 'replace',
              'old_statement': edge['mechanism'], 'replacement': edge2, 'new_evidence': ['INCOME'],
              'reason': 'Revised input changes the mechanism magnitude and timing.'}
        restored.cli('proposal', '--file', restored.input('edge_proposal.json', ep))
        restored.phase(UPDATE[3], 'Mechanism proposal binds edge revision one and the revised income observation.')
        restored.inspect_proposal('P_EDGE')
        restored.phase(UPDATE[4], 'The edge revision has an accepted independent fixture review.')
        restored.cli('apply', '--id', 'P_EDGE')
        assert restored.cli('graph-status')['nodes']['CASH_VERDICT']['status'] == 'needs_review'
        edits = []
        for name, text in [
            ('research/parameters.json', json.dumps({**params, 'income': 9000}, ensure_ascii=False, indent=2) + '\n'),
            ('formal/results.json', json.dumps(second_result, ensure_ascii=False, indent=2) + '\n'),
            ('formal/report.md', '# 合成工程演练\n\n' + new_statement + '\n\n此文件仅验证工程，不是中国危机报告。\n')]:
            edits.append({'path': name, 'base_sha256': hashlib.sha256((restored.w / name).read_bytes()).hexdigest(), 'text': text})
        cp = {'id': 'P_CLAIM', 'target': 'CASH_VERDICT', 'author': 'fixture-author', 'base_revision': 1,
              'action': 'replace', 'old_statement': first_statement, 'new_statement': new_statement,
              'new_evidence': ['INCOME'], 'reason': 'Income rises by 1000; monthly deficit halves; independent replay matches.', 'files': edits}
        restored.cli('proposal', '--file', restored.input('claim_proposal.json', cp))
        restored.cli('apply', '--id', 'P_CLAIM', rejected=True)
        restored.phase(UPDATE[3], 'Second serial proposal replaces the claim and exact report, parameters and result bytes.')
        restored.inspect_proposal('P_CLAIM')
        restored.phase(UPDATE[4], 'Claim review follows the already-merged edge; old rejection is preserved.')
        restored.cli('apply', '--id', 'P_CLAIM')
        restored.phase(UPDATE[5], 'Serial apply replaces statement, parameters, report and result atomically against their base hashes.')
        reversal = {**cp, 'id': 'P_REVERSE', 'base_revision': 2, 'old_statement': new_statement,
                    'new_statement': first_statement, 'new_method': 'Attempted return to an older statement', 'files': []}
        restored.cli('proposal', '--file', restored.input('unanswered_reversal.json', reversal), rejected=True)
        shell(sys.executable, replay_path, restored.w / 'research/parameters.json', base / 'updated-replayed.json')
        assert json.loads((base / 'updated-replayed.json').read_text()) == second_result
        restored.phase(UPDATE[6], 'The cloned replay script independently reproduces first shortfall month thirteen from updated parameters.')
        restored.phase(UPDATE[7], 'Updated mechanism, claim, parameters and deliverables frozen with complete prior reasons.')
        restored.review()
        second_release = restored.release(new_statement)
        shell('git', 'config', 'user.name', 'Engineering Fixture', cwd=clone)
        shell('git', 'config', 'user.email', 'fixture@example.invalid', cwd=clone)
        restored.cli('checkpoint', '--paths', 'work/engineering', '--message', 'Complete synthetic incremental rehearsal')
        final_clone = base / 'final-recovered'
        shell('git', 'clone', '--quiet', '--no-hardlinks', clone, final_clone)
        final = Rehearsal(final_clone)
        assert final.cli('status')['release']['current']
        shell(sys.executable, final.w / 'research/replay.py', final.w / 'research/parameters.json', base / 'final-replayed.json')
        assert json.loads((base / 'final-replayed.json').read_text()) == second_result
        state = json.loads((final.w / 'research_state.json').read_text())
        assert state['proposals']['P_BAD']['status'] == 'rejected'
        assert state['proposals']['P_EDGE']['status'] == 'applied'
        assert state['proposals']['P_CLAIM']['status'] == 'applied'
        summary = {'status': 'passed', 'input_kind': 'synthetic_engineering_fixture',
                   'first_cycle_stages': len(FIRST), 'update_cycle_stages': len(UPDATE),
                   'cli_commands': r.commands + restored.commands + final.commands,
                   'fresh_clones': 2, 'initial_shortfall_month': first_result['first_shortfall_month'],
                   'updated_shortfall_month': second_result['first_shortfall_month'],
                   'search_reuse_and_scope_refresh': True, 'old_rejection_preserved': True,
                   'unreviewed_apply_blocked': True, 'unanswered_reversal_blocked': True,
                   'edge_and_claim_separately_reviewed': True, 'offline_replay_identical': True,
                   'first_release_snapshot': first_release['review_snapshot'],
                   'update_release_snapshot': second_release['review_snapshot'],
                   'blocked_cases': r.blocks + restored.blocks}
        if output:
            save(Path(output), summary)
        print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--output', default=str(ROOT / 'tests/live/end_to_end.json'))
    main(p.parse_args().output)
