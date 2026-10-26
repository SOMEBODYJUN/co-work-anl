"""Curated, pinned, read-only source package for the six-provider problem."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import argparse
import ast
import hashlib
import json
import re
import subprocess
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'customer_attraction/model.py').exists())
BASE = '6da46a68073073e9038cd538fd01019a0f112ede'
A = 'research/workspaces/customer-attraction/'
NEW = A + 'R-a8ee6fdb155c47da95540775b4a6a2db/'
ZERO = A + 'R-23ab27f8efb44f1faca2699d45886250/general_n/'
D1 = A + 'R-d1fe1e0c444e40d68b6813bf88db8fba/'
C4 = A + 'R-c4f1ef099fad483c9f81283b61eb0b53/'
PREV = A + 'R-964def22ed03479582e83410444f2ea2/parent/'
SEVEN = A + 'R-07e871289a6b4c1fb07244c97eb4aac8/'
CURRENT = 'research/current/customer_attraction/'
FIVE = 'customer_attraction/proofs/half5_exact_v1/'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=HERE / 'Q-CAG-HALF-6.zip')
    args = parser.parse_args()
    names = git('ls-tree', '-r', '--name-only', BASE).decode().splitlines()
    tracked = set(names)
    groups = {
        'model_known_results_general_tools': [CURRENT + n + '.md' for n in (
            'model', 'three_player_sharp', 'four_player_bound', 'five_player_half',
            'two_remaining_tax', 'four_remaining_profit_bound', 'tail_profit_lift',
            'priced_hidden_reply_projection', 'same_source_reply_requery',
            'fractional_cover_path_budget', 'oblivious_security', 'strategy_cone',
            'exact_solver', 'optimal_first_action_branch_gap', 'general_half_proof')],
        'five_complete_proof': [n for n in names if n.startswith(FIVE)],
        'five_review': ['research/reviews/customer_attraction/five_player_half_' + x + '.md'
                        for x in ('import', 'local', 'global')],
        'six_joint_witness': [NEW + 'closure/' + x for x in (
            'README.md', 'joint_atoms_exact.json', 'root_extension_exact.json',
            'verify_joint_atoms.py', 'root_extension.py')]
            + [NEW + 'attack/closure_independent_review.md'],
        'six_suffix_envelope': [NEW + 'parent/' + x for x in (
            'suffix_envelope_boundary.md', 'suffix_envelope_input.json',
            'verify_suffix_envelope.py', 'suffix_envelope_exact.json')]
            + [NEW + 'direct/' + x for x in (
                'suffix_envelope_independent_review.md',
                'audit_suffix_envelope_independent.py',
                'suffix_envelope_independent_audit.json')],
        'zero_regret_complete_SPE': [ZERO + x for x in (
            'zero_regret_promotion_reset.md', 'promotion_reset_boundary.md',
            'verify_zero_regret_promotion.py', 'zero_regret_promotion_exact.json',
            'independent_zero_source.py', 'independent_zero_source_exact.json')],
        'other_general_boundaries_candidates': [
            'research/customer_attraction/FAILED_ROUTES.md',
            D1 + 'six_difficulty/README.md',
            C4 + 'parent/potential_copy_candidate.md',
            NEW + 'potential/exclusion_safety_margin.md'],
        'finite_exact_game_tools': ['customer_attraction/' + x for x in (
            '__init__.py', 'model.py', 'exact.py', 'certificate.py', 'priced_hidden_reply.py')],
    }
    selected = set().union(*map(set, groups.values()))
    assert selected <= tracked, sorted(selected - tracked)

    # Resolve unique repository-local Python modules used by the actual replay
    # entry points. This is source inclusion, not proof of dynamic completeness.
    dependency_entries = {NEW + 'closure/verify_joint_atoms.py',
                          NEW + 'closure/root_extension.py'}
    modules = {}
    for name in names:
        if name.endswith('.py') and name.startswith(A):
            modules.setdefault(Path(name).stem, []).append(name)
    parsed, todo, dependencies = set(), list(dependency_entries), set()
    while todo:
        name = todo.pop()
        if name in parsed:
            continue
        parsed.add(name)
        syntax = ast.parse(git('show', BASE + ':' + name).decode())
        imports = []
        for node in ast.walk(syntax):
            if isinstance(node, ast.Import):
                imports.extend(alias.name.split('.')[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.append(node.module.split('.')[0])
        for module in imports:
            candidates = modules.get(module, [])
            if len(candidates) == 1 and candidates[0] not in parsed:
                dependencies.add(candidates[0])
                todo.append(candidates[0])
    # This file is loaded via importlib and is not an ordinary import.
    dependencies.add(D1 + 'six_maxroot/discover.py')
    data_dependencies = {
        C4 + 'six_astra/attractive_nested_exact.json',
        SEVEN + 'general_from_half5/six_copy_free_results.json',
        D1 + 'parent/joint_system.json',
        D1 + 'parent/strong_pair_projection.json',
        D1 + 'query_closure/iterate_same_menu.json',
        D1 + 'general_payment/compact_cuts.json',
        PREV + 'fourth_indexed_projection.json',
    }
    for n in ('exact_cuts.json', 'exact_cuts_threecopy.json', 'exact_cut_directional.json'):
        data_dependencies.add(D1 + 'six_maxroot/' + n)
    for n in ('AB_projected_row.json', 'AB_projected_row_joint.json'):
        data_dependencies.add(D1 + 'six_lift/' + n)
    optional = D1 + 'general_payment/target_joint.json'
    if optional in tracked:
        data_dependencies.add(optional)
    dependencies |= data_dependencies
    assert dependencies <= tracked, sorted(dependencies - tracked)
    groups['minimal_original_replay_dependencies'] = sorted(dependencies - selected)
    selected |= dependencies

    payload = {}
    source_meta = {}
    secret = re.compile(rb'(?:github_pat_|gh[pousr]_)[A-Za-z0-9_]{12,}')
    for name in sorted(selected):
        content = git('show', BASE + ':' + name)
        assert not secret.search(content), 'Credential pattern found; contents suppressed'
        payload['source/' + name] = content
        source_meta['source/' + name] = {'source_path': name,
            'git_blob': git('rev-parse', BASE + ':' + name).decode().strip()}
    payload['source/work.py'] = (
        '"""Read-only bundle root marker; no repository operations or authentication."""\n'
        'if __name__ == "__main__":\n'
        '    raise SystemExit("This is only a directory marker for bundled verifiers.")\n'
    ).encode()
    for name in ('00_TASK_ZH.md', '01_MATERIALS_ZH.md', '02_REPRODUCTION_ZH.md',
                 'verify_manifest.py', 'run_checks.py'):
        payload[name] = (HERE / name).read_bytes()
    payload['requirements.txt'] = b'numpy\nscipy\n'
    selection = {
        'source_commit': BASE,
        'repository': 'https://github.com/SOMEBODYJUN/co-work-anl',
        'target': 'Exactly six providers, arbitrary finite customers/common catalogue, every full-history pure SPE: 2W>=OPT6',
        'target_status': 'OPEN',
        'groups': {k: sorted(v) for k, v in groups.items()},
        'selection_scope': 'Curated mathematical originals and dependencies of the named replay entry points; not all useful assets or all repository links',
        'excluded': ['credentials', 'Git metadata/history', 'communication logs',
                     'role instructions', 'unrelated projects', 'bulk scans',
                     'superseded five-only task packets', 'redundant pricing rounds'],
        'source_work_py': 'Nonfunctional root marker generated for this package; not the repository work.py',
        'review_scope': 'Original mathematical review identities retained; new wrappers do not constitute an independent proof implementation',
    }
    payload['SELECTION.json'] = (json.dumps(selection, ensure_ascii=False, indent=2) + '\n').encode()
    if (HERE / 'VALIDATION.json').exists():
        payload['VALIDATION.json'] = (HERE / 'VALIDATION.json').read_bytes()
    manifest = []
    for name, content in sorted(payload.items()):
        path = PurePosixPath(name)
        assert not path.is_absolute() and '..' not in path.parts
        assert not secret.search(content), 'Credential pattern found; contents suppressed'
        manifest.append({'path': name, 'size_bytes': len(content),
                         'sha256': hashlib.sha256(content).hexdigest(),
                         **source_meta.get(name, {})})
    payload['MANIFEST.json'] = (json.dumps({'schema': 'curated-half6-v1',
        'source_commit': BASE, 'files': manifest}, ensure_ascii=False, indent=2) + '\n').encode()
    stamp = datetime.fromisoformat(git('show', '-s', '--format=%cI', BASE).decode().strip())
    stamp = stamp.astimezone(timezone.utc).timetuple()[:6]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.output, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, content in sorted(payload.items()):
            info = zipfile.ZipInfo('Q-CAG-HALF-6/' + name, stamp)
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(args.output) as archive:
        assert archive.testzip() is None
        assert len(archive.namelist()) == len(set(archive.namelist())) == len(payload)
        for row in manifest:
            content = archive.read('Q-CAG-HALF-6/' + row['path'])
            assert hashlib.sha256(content).hexdigest() == row['sha256']
    report = {'status': 'BUILT_AND_BYTE_VERIFIED', 'source_commit': BASE,
              'source_files': len(selected), 'total_files': len(payload),
              'uncompressed_bytes': sum(map(len, payload.values())),
              'zip_bytes': args.output.stat().st_size,
              'zip_sha256': hashlib.sha256(args.output.read_bytes()).hexdigest(),
              'credential_pattern_scan': 'PASS', 'zip_crc_and_sha256': 'PASS',
              'has_portable_replay_report': 'VALIDATION.json' in payload}
    (HERE / 'BUILD_REPORT.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
