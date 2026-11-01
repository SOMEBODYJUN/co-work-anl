#!/usr/bin/env python3
"""Static delivery verification only; never run source or mathematical audits."""
import ast
import hashlib
import json
import re
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
BODY = ROOT / 'archives/customer-attraction/state/程序/六人七主题固定完整策略的福利比线性规划程序--程序.md'
RECEIPT = ROOT / 'cleanup/workspaces/Boss7/receipts-round16/1ee3fd3da1dc3b243cc8.json'
R = HERE / 'replay'


def read(path):
    return json.loads(path.read_text())


def verify(path, item):
    raw = path.read_bytes()
    assert len(raw) == item.get('bytes', item.get('size')), str(path)
    assert hashlib.sha256(raw).hexdigest() == item['sha256'], str(path)


def main():
    own = read(HERE / 'artifact-manifest.json')['files']
    for item in own:
        verify(ROOT / item['path'], item)
    source = read(HERE / 'source-manifest.json')['sources']
    for item in source:
        verify(HERE / item['preserved_path'], item['source'])
    compared = read(HERE / 'comparison-manifest.json')['files']
    shared = read(HERE / 'shared-audit-binding.json')['files']
    for item in compared + shared:
        verify(ROOT / item['path'], item)
    assert (HERE / 'original/spe_dp.py').read_bytes() == (HERE.parent / 'r70-spe-dp-program/original/spe_dp.py').read_bytes()
    json_paths = sorted(p for p in HERE.rglob('*.json') if p.name != 'self-check.json')
    for path in json_paths:
        read(path)
    python_paths = sorted(HERE.rglob('*.py'))
    for path in python_paths:
        ast.parse(path.read_text(), filename=str(path))
    links = []
    for document in [BODY, HERE / 'README.md']:
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', document.read_text()):
            target = target.strip('<>').split('#', 1)[0]
            if not target or re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:', target):
                continue
            assert (document.parent / target).resolve().exists(), (str(document), target)
            links.append({'document': str(document.relative_to(ROOT)), 'target': target})
    event = read(R / 'execution.json')
    assert event['inputs_before'] == event['inputs_after']
    for item in event['inputs_before']:
        name = Path(item['path']).name
        folder = 'related' if name == 'random_best.json' else 'original'
        verify(HERE / folder / name, item)
    for name, item in event['files'].items():
        verify(R / name, item)
    assert event['counts'] == {'original_main': 1, 'solve': 1, 'strategy_constraints': 1, 'matrix': 1, 'optimize': 1, 'linprog': 7}
    assert event['helper_replacements'] == event['additional_solve_or_LP_calls'] == event['original_verify_result_calls'] == 0
    process = read(R / 'process-capture.json')
    assert process['returncode'] == 0
    for name, item in process['output_files'].items():
        verify(R / ('stderr.txt' if '.stderr.' in name else 'stdout.txt'), item)
    assert (R / 'stderr.txt').stat().st_size == 0
    assert (R / 'lp_best.json').read_bytes() == (HERE / 'related/lp_best.json').read_bytes()
    assert read(R / 'lp_best.json') == read(R / 'optimize-return.json')
    dp = read(R / 'dp-return.json')
    assert dp == read(HERE / 'related/random_best.json')['result']
    strategy = read(R / 'complete-strategy.json')
    assert strategy['node_count'] == len(strategy['entries']) == 19608
    assert len({tuple(x['history']) for x in strategy['entries']}) == 19608
    keys = read(R / 'constraint-keys.json')['keys']
    matrix = read(R / 'ic-matrix.json')
    assert len(keys) == 3048 and matrix['shape'] == [3048, 127]
    assert len(matrix['data']) == len(matrix['indices']) == 198672
    assert len(matrix['indptr']) == 3049 and matrix['indptr'][-1] == 198672
    # Append the captured seven binary coverage rows to the captured CSR;
    # this checks actual-call serialization, not any new LP or payoff computation.
    augmented = {key: list(value) for key, value in matrix.items()}
    augmented['shape'] = [3055, 127]
    for omit in range(7):
        for mask in range(1, 128):
            if mask & (127 - (1 << omit)):
                augmented['data'].append(1.0)
                augmented['indices'].append(mask - 1)
        augmented['indptr'].append(len(augmented['data']))
    csr_sha = hashlib.sha256(json.dumps(augmented, separators=(',', ':'), sort_keys=True).encode()).hexdigest()
    calls = read(R / 'seven-lp-results.json')['calls']
    assert [x['omit'] for x in calls] == list(range(7))
    for call in calls:
        assert call['A_ub_shape'] == [3055, 127]
        assert call['A_ub_nnz'] == len(augmented['data'])
        assert call['A_ub_csr_sha256'] == csr_sha
        assert call['b_ub'] == [0.0] * 3048 + [1.0] * 7
        assert call['bounds'] == [0, None] and call['method'] == 'highs'
        assert call['result']['success'] is True and call['result']['status'] == 0
        assert len(call['result']['ineqlin']['marginals']) == 3055
    audit = read(HERE / 'exact-cone-audit.json')
    assert audit['status'] == 'PASS'
    for name, item in audit['inputs'].items():
        verify(R / name, item)
    assert audit['ordered_nodes'] == 19608 and audit['matrix_coefficients_checked'] == 387096
    assert audit['scope']['original_imports'] == audit['scope']['DP'] == audit['scope']['LP'] == 0
    expected = ['6/11', '3/5', '6/11', '3/5', '3/5', '3/5', '3/5']
    assert [d['exact_dual_bound'] for d in audit['duals']] == expected
    body = BODY.read_text()
    active = set()
    for d in audit['duals']:
        assert d['status'] == 'PASS' and d['minimum_residual'] == '0'
        assert len(d['column_residuals']) == 127
        assert d['negative_residual_columns'] == d['positive_inequality_multiplier_rows'] == []
        pairs = '；'.join(f'{t["row"]}:{-F(t["value"])}' for t in d['nonzero_inequality_multipliers'])
        assert f'| {d["omit"]} | {d["exact_dual_bound"]} | {pairs} |' in body
        active.update(t['row'] for t in d['nonzero_inequality_multipliers'])
    assert len(active) == 21 and all(i < 3048 for i in active)
    for i in active:
        a, q, b, r = keys[i]
        row = f'| {i} | {a} | ({",".join(map(str,q))}) | {b} | ({",".join(map(str,r))}) |'
        assert row in body
    point = read(HERE.parent / 'r70-six1-best-data/point-audit.json')
    assert point['status'] == 'PASS'
    assert point['original_solver_runs'] == point['optimizer_calls'] == 0
    assert point['points']['lp_integer']['ratio'] == '6/11'
    assert point['points']['lp_integer']['comparisons'] == 137256
    verify(R / 'complete-strategy.json', point['input_bindings'][2])
    receipt = read(RECEIPT)
    assert receipt['id'] == '1ee3fd3da1dc3b243cc8' and receipt['disposition'] == 'integrated'
    for key in ['full_file_reviewed', 'related_material_checked', 'unique_content_accounted_for']:
        assert receipt[key] is True
    for target in receipt['targets']:
        assert (ROOT / target).exists(), target
    report = {'status': 'PASS', 'scope': 'static fingerprints, structure, CSR capture binding, table transcriptions, links and receipt; no source or math-audit execution',
              'own_fingerprints': len(own), 'original_bindings': len(source), 'comparison_bindings': len(compared),
              'shared_audit_bindings': len(shared), 'JSON_syntax_files': len(json_paths), 'Python_AST_files': len(python_paths),
              'local_links': len(links), 'receipt_targets': len(receipt['targets']), 'body_IC_table_rows': 21, 'body_dual_table_rows': 7,
              'original_call_CSR_fingerprints': 7, 'old_new_lp_bytes_equal': True, 'links': links}
    (HERE / 'self-check.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'links'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
