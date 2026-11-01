#!/usr/bin/env python3
"""Static package identity check. Never imports or executes the audited program."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re

def identity(p):
    b = p.read_bytes()
    return {'path': str(p), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    args = ap.parse_args()
    repo = args.repo.resolve()
    rel = Path('archives/customer-attraction/tools/evidence/diagonal-menu-independent-audit')
    package = repo / rel
    body = repo / 'archives/customer-attraction/state/程序/同索引末回复必要行的有理审计程序--程序.md'
    out = package / 'self-check.json'
    manifest = json.loads((package / 'source-manifest.json').read_text())
    checked_sources = []
    for item in manifest['sources']:
        p = repo / item['preserved_path']
        b = p.read_bytes()
        assert len(b) == item['size']
        assert hashlib.sha256(b).hexdigest() == item['sha256']
        assert hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest() == item['blob']
        checked_sources.append(identity(p))
    review = json.loads((package / 'review-record.json').read_text())
    checked_comparisons = []
    for item in review['comparison_assets']:
        p = repo / item['path']
        got = identity(p)
        assert got['bytes'] == item['bytes'] and got['sha256'] == item['sha256']
        checked_comparisons.append(got)
    frozen = (package / 'original/audit_diagonal_menu.json').read_bytes()
    assert (package / 'replay/audit_diagonal_menu.json').read_bytes() == frozen
    assert (package / 'replay/stdout.txt').read_bytes() == frozen
    assert (package / 'replay/stderr.txt').read_bytes() == b''
    report = json.loads(frozen)
    assert list(report) == ['scope','node','comparison','lhs_sum','rhs_sum','slack_sum','passes_necessary_inequality']
    assert report['passes_necessary_inequality'] is False
    event = json.loads((package / 'replay/execution.json').read_text())
    assert event['exit_code'] == 0 and event['output_equals_frozen_bytes'] and event['stdout_equals_frozen_bytes']
    assert event['before'] == event['after']
    assert event['runtime_before'] == event['runtime_after']
    assert event['execution_scope']['original_main_processes_launched'] == 1
    assert event['execution_scope']['lp_solver_calls'] == 0
    assert event['execution_scope']['new_independent_38_term_implementations'] == 0
    independent = json.loads((repo / review['independent_stored_result']).read_text())
    old = independent['later_L2_vs_L1']
    assert report['slack_sum'] == old['value']
    assert len(old['all38_summands']) == 38 and old['negative'] is True
    assert [v['atom'] for v in old['all38_summands']] == list(range(38))
    input_source = next(s for s in manifest['sources'] if s['id'] == '667dc37261628075aedc')
    old_point = json.loads((repo / input_source['preserved_path']).read_text())
    assert len(old_point) == 12 and len(old_point['point']) == 65 and len(old_point['atom_masses']) == 38
    assert all(len(a['bits']) == 10 and len(a['AB_hist']) == 8 and len(a['AE_hist']) == 8 and
               len(a['second_hist']) == 16 and len(a['menus_lh']) == 3 for a in old_point['atom_masses'])
    receipt_results = []
    for source_id in ['9c091035a7d908e9877f','09c28210901715b44312']:
        p = repo / 'cleanup/workspaces/Boss7/receipts-round21' / (source_id + '.json')
        r = json.loads(p.read_text())
        assert r['id'] == source_id and r['disposition'] == 'integrated'
        assert r['full_file_reviewed'] and r['related_material_checked'] and r['unique_content_accounted_for']
        for target in r['targets']:
            q = repo / target
            assert q.exists() or q == out
        receipt_results.append(identity(p))
    links = []
    for p in [body, package / 'README.md']:
        text = p.read_text()
        assert not any(ord(c) < 32 and c not in '\n\t' for c in text)
        for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
            if '://' in link or link.startswith('#'):
                continue
            q = (p.parent / link.split('#', 1)[0]).resolve()
            assert q.exists() or q == out, (p, link)
            links.append({'from':str(p.relative_to(repo)), 'to':str(q.relative_to(repo))})
    own = []
    ast_files = []
    json_files = []
    for p in sorted(package.rglob('*')):
        if not p.is_file() or p == out:
            continue
        own.append(identity(p))
        if p.suffix == '.py':
            ast.parse(p.read_text(), filename=str(p)); ast_files.append(str(p.relative_to(repo)))
        if p.suffix == '.json':
            json.loads(p.read_text()); json_files.append(str(p.relative_to(repo)))
    result = {
        'status':'PASS',
        'scope':'static file/hash/schema/byte identity/link check only; no coefficient recomputation',
        'body':identity(body), 'sources':checked_sources, 'comparison_assets':checked_comparisons,
        'own_files_except_this_output':own, 'receipts':receipt_results,
        'links':links, 'python_ast_files':ast_files, 'json_files':json_files,
        'original_report_byte_identity':True,
        'stored_independent_slack_string_equal':True,
        'source_schema_sizes':{'top_fields':12,'point':65,'atom_masses':38,'report_fields':7},
        'new_original_runs':0,'new_row_evaluations':0,'new_lp_calls':0,'new_spe_checks':0,
        'self_output_excluded_from_hashes':True
    }
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':'PASS','sources':len(checked_sources),'comparison_assets':len(checked_comparisons),
                      'own_files':len(own),'links':len(links),'receipts':len(receipt_results)},ensure_ascii=False))

if __name__ == '__main__':
    main()
