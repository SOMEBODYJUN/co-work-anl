"""Freeze the completed symbolic interface without writing any parent file."""
from hashlib import sha256
from pathlib import Path
import ast
import gzip
import json

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
REPO = BASE.parents[2]


def sha(path):
    return sha256(path.read_bytes()).hexdigest()


def load(path):
    if path.suffix == '.gz':
        with gzip.open(path, 'rt') as f:
            return json.load(f)
    return json.loads(path.read_text())


def main():
    direct = load(HERE/'direct_interface_exact.json.gz')
    extended = load(HERE/'extended_interface_exact.json.gz')
    dv = load(HERE/'direct_verification.json')
    ev = load(HERE/'extended_verification.json')
    av = load(HERE/'append_api_verification.json')
    assert dv['status'] == 'INDEPENDENT_EXACT_SHARED_X_DIRECT_INTERFACE_PASS'
    assert ev['status'] == 'INDEPENDENT_EXACT_EXTENDED_SHARED_X_INTERFACE_PASS'
    assert av['status'] == 'EXACT_APPEND_NAMESPACE_AUDIT_PASS'
    for item in direct['sources'] + dv['sources']:
        assert sha(BASE/item['path']) == item['sha256']
    for name, expected in ev['sources'].items():
        assert sha(HERE/name) == expected
    assert len(direct['rows']) == 42 and len(extended['principal_rows']) == 236
    assert len(extended['eta_columns']) == 1216 and len(extended['eta_equalities']) == 38
    # Verify the frozen parent's six declared runtime inputs against its own
    # prior freeze, without opening or interpreting any discarded point.
    parent = BASE/'common_x_joint_lp/final'
    parent_freeze = load(parent/'freeze_manifest.json')
    parent_receipt = []
    for item in parent_freeze['six_runtime_inputs']:
        path = REPO/item['path']
        assert path.is_file() and sha(path) == item['sha256']
        assert path.stat().st_size == item['bytes']
        parent_receipt.append(dict(path=item['path'], sha256=item['sha256'], bytes=item['bytes'], unchanged=True))
    assert parent_freeze['shape'] == [23676, 21021]
    assert parent_freeze['nonzeros'] == 3313758
    # This package uses only exact symbolic arithmetic and standard-library I/O.
    allowed = {'collections', 'fractions', 'hashlib', 'itertools', 'pathlib',
               'gzip', 'json', 'time', 'ast'}
    imports = {}
    for path in sorted(HERE.glob('*.py')):
        found = set()
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.Import):
                found.update(alias.name.split('.')[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                found.add(node.module.split('.')[0])
        assert found <= allowed, (path.name, found-allowed)
        imports[path.name] = sorted(found)
    source_paths = [
        BASE/'root_x_joint_contract.md', BASE/'root_x_joint_contract/own_blocks.json',
        BASE/'root_x_joint_contract/verify_kernel.py', BASE/'root_sorting_20910.md',
        BASE/'root_sorting_20910/model.py', BASE/'root_sorting_20910/symbolic_matrix_exact.json.gz',
        BASE/'root_marginal_closure/model.py', BASE/'terminal_response_cycles.md',
        BASE/'terminal_response_cycles/max_b_symbolic_lift.json', BASE/'actual_pair_20910.md',
        REPO/'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md',
        REPO/'archives/customer-attraction/state/引理/跨族末两人菜单的共同锚点与运输界--引理.md',
    ]
    artifacts = [p for p in HERE.iterdir() if p.is_file() and p.name != 'freeze_manifest.json']
    artifacts.append(BASE/'root_x_shared_queries.md')
    result = dict(
        status='FROZEN_SHARED_X_ROOT_QUERY_INTERFACE_COMPLETE_NO_POINT_DIAGNOSTIC',
        completed_scope=dict(direct_principal_rows=42, full_principal_rows=236,
                             root_PAIR=41, actual_RC_unordered=185, actual_RC_ordered=360,
                             shared_eta=1216, eta_mass_equalities=38,
                             conditional_min=12860, conditional_sorting=2940,
                             full_added_inequalities=38932),
        files=[dict(path=str(p.relative_to(BASE)), sha256=sha(p), bytes=p.stat().st_size)
               for p in sorted(artifacts)],
        sources=[dict(path=str(p.relative_to(REPO)), sha256=sha(p)) for p in source_paths],
        frozen23676_runtime_inputs=parent_receipt,
        frozen23676_matrix_unchanged=True,
        standard_library_imports=imports,
        optimizer_calls=0, discarded_cb45_values_evaluated=0, point_diagnostic_executed=False,
        remaining_obligations=['evaluate only a subsequently assigned exact point',
                               'global old-hidden-state X compatibility beyond 210 local own blocks',
                               'common cross-query transports and full ordered-history strategy realization'],
        write_scope='Only root_x_shared_queries/ and root_x_shared_queries.md; no Git, RUN, registry or credentials.',
    )
    (HERE/'freeze_manifest.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(dict(status=result['status'], files=len(result['files']),
                          source_files=len(result['sources']), parent_runtime_inputs_verified=len(parent_receipt),
                          optimizer_calls=0), ensure_ascii=False))


if __name__ == '__main__':
    main()
