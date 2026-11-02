#!/usr/bin/env python3
"""Prepare original audit bytes in a fresh runtime; execute no mathematics.

The one generated model.py is a declared comment-only root-lookup marker.
Neither original audit imports it. No author recovery dependencies are stubbed.
"""
from pathlib import Path
from argparse import ArgumentParser
import hashlib
import json

HERE=Path(__file__).resolve().parent
WORKSPACE='research/workspaces/customer-attraction/R-ae18a85a07214b22b7b9d614c34779e0'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def locate_repo(explicit, manifest):
    if explicit:
        return Path(explicit).resolve()
    candidates=[p for p in HERE.parents if all((p/d['archive_path']).is_file() for d in manifest['reused_dependencies'])]
    if not candidates:
        raise SystemExit('Cannot find reused original inputs; supply --repo REPOSITORY_ROOT.')
    return candidates[0]

def main():
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('--runtime',required=True)
    parser.add_argument('--repo',help='Repository root containing reused original evidence; usually auto-detected.')
    args=parser.parse_args()
    manifest=json.loads((HERE/'manifest.json').read_text())
    repo=locate_repo(args.repo,manifest)
    runtime=Path(args.runtime).resolve()
    if runtime.exists() and (not runtime.is_dir() or any(runtime.iterdir())):
        raise SystemExit('Runtime must not exist or must be empty.')
    runtime.mkdir(parents=True,exist_ok=True)
    copied=[]
    # Preserve all ten original primary bytes, including the non-runnable joint route.
    for item in manifest['sources']:
        data=(HERE/item['package_path']).read_bytes()
        assert sha(data)==item['sha256'] and len(data)==item['size'], item['id']
        dest=runtime/item['path']
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(data)
        copied.append(dict(path=item['path'],sha256=sha(data),bytes=len(data),role='primary-original'))
    for item in manifest['reused_dependencies']:
        data=(repo/item['archive_path']).read_bytes()
        assert sha(data)==item['sha256'] and len(data)==item['size'], item['archive_path']
        dest=runtime/item['frozen_path']
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(data)
        copied.append(dict(path=item['frozen_path'],sha256=sha(data),bytes=len(data),role='reused-original-input'))
    marker=manifest['routing_marker']
    dest=runtime/marker['path']
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(marker['contents'])
    record=dict(action='prepare-only; no audit imports or scientific entrypoint calls',
        copied_originals=copied,declared_nonexecuted_routing_marker=marker,
        runnable_original_audits=[WORKSPACE+'/dual/separate_shared_root_audit.py',WORKSPACE+'/countersearch/audit_shared_root_math.py'],
        author_recovery_prepared=False,
        scientific_entrypoint_calls=0)
    (runtime/'preparation-record.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(dict(original_files=len(copied),scientific_entrypoint_calls=0,runtime=str(runtime)),indent=2))

if __name__=='__main__':
    main()
