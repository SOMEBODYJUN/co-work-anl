"""Restore a frozen runtime for the fourteen-row auditor without executing it."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repository', required=True, type=Path)
    parser.add_argument('--runtime', required=True, type=Path)
    args = parser.parse_args()
    root = args.repository.resolve()
    runtime = args.runtime.resolve()
    assert runtime != root and root not in runtime.parents, 'Use an isolated tree outside the result repository'
    evidence = root / 'archives/customer-attraction/tools/evidence'
    pack = evidence / 'combined-branch-master-program'
    available = json.loads((pack / 'rerun/available-frozen-files-manifest.json').read_bytes())
    preserved = {v['id']: root / v['stored_path']
                 for v in json.loads((pack / 'source-manifest.json').read_bytes())['frozen_sources']}
    preserved.update({
        '358135a42d98d3ff5129': evidence / 'continuous-old-query-cuts-program/related/all_reply_query_cuts_exact.json',
        'dcb82d5dd75f34db2ecf': evidence / 'split-basic-graph-program/related/split_basic_exact.json',
        '53a6dd749f079ac1abc9': evidence / 'cross-source-graph-program/related/audit_cross_source_basic.py',
    })
    author = {'id': '53a6dd749f079ac1abc9',
              'path': 'research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_3/audit_cross_source_basic.py',
              'size': 3019,
              'sha256': '5113ef5d4f46b5d2c40b6fc9dcb3c1788fa4d3ea6677bf89a462560d4a53275b'}
    records = available + [author]
    for record in records:
        source = preserved[record['id']]
        assert source.stat().st_size == record['size'] and sha(source) == record['sha256']
        target = runtime / record['path']
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            assert target.read_bytes() == source.read_bytes(), target
        else:
            shutil.copyfile(source, target)
    marker = runtime / 'work.py'
    if not marker.exists():
        shutil.copyfile(root / 'work.py', marker)
    for record in records:
        assert sha(runtime / record['path']) == record['sha256']
    print(json.dumps({'status': 'PASS', 'restored_or_verified_frozen_files': len(records),
                      'runtime': str(runtime), 'source_programs_executed': 0,
                      'root_marker': 'work.py only used for directory discovery; not imported or executed'}, indent=2))


if __name__ == '__main__':
    main()
