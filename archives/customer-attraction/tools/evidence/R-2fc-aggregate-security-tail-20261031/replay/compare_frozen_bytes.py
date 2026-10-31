#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ORIGINAL=ROOT/'original'
REPO=ROOT.parents[4]  # .../co-work-anl
# verify this anchor to keep target paths explicit
if not (REPO/'.git').is_dir():
    raise SystemExit(f'not repo: {REPO}')
items={
 '6c9d817c586d116a7ef2_dr_groups_repeats.json':('dr_groups_repeats.json','3408fb3ea0e84b1549351ffdc7a9ec9d5a76508f'),
 '615b20e056941847ca2d_dr_groups_simple_query.json':('dr_groups_simple_query.json','e06e74c5b7236601e009f49b54dea888b1458edc'),
 '29bbc735344948028c8b_dr_groups_simple_query_diag.json':('dr_groups_simple_query_diag.json','a194bbbdcdf9104d7f2209beec3f6e19a9d768e0'),
 'e66595d9da26cedb6334_dr_groups_third.json':('dr_groups_third.json','ca6a368851c2e62a2f23f840fc9c23ed6f48617b'),
 '4b98a2950c56d94cfbf5_dr_n3k3.json':('dr_n3k3.json','9b04e82083c212f3ca10c5dfe82a4eb316c9c351'),
 '8cda73aa604b09b9b171_dr_n3k4.json':('dr_n3k4.json','53940ee79aaa3ed8ab1eeac082b23d3eb42499cd'),
}
commits=('68fad804ec5946cb296f77dc5b336308a66abf12','aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c')
pathbase='research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/'
env={k:v for k,v in os.environ.items() if k.lower() not in {'http_proxy','https_proxy','all_proxy','no_proxy'}}
errors=[]
for name,(source,blob) in items.items():
    archived=(ORIGINAL/name).read_bytes()
    print(f'{name}: archived_sha256={hashlib.sha256(archived).hexdigest()} archived_bytes={len(archived)}')
    for commit in commits:
        r=subprocess.run(['git','-C',str(REPO),'show',f'{commit}:{pathbase}{source}'],env=env,capture_output=True)
        if r.returncode:
            errors.append(f'{name} {commit[:8]} git-show rc={r.returncode}: {r.stderr.decode(errors="replace").strip()}')
            print(f'  {commit[:8]} rc={r.returncode}')
            continue
        got=hashlib.sha256(r.stdout).hexdigest(); same=(r.stdout==archived)
        print(f'  {commit[:8]} blob_bytes={len(r.stdout)} sha256={got} archived_byte_equal={same} expected_blob={blob} blob_equal={hashlib.sha1(b"blob "+str(len(r.stdout)).encode()+bytes([0])+r.stdout).hexdigest()==blob}')
        if not same: errors.append(f'{name} {commit[:8]} differs from archived')
print(f'checked {len(items)} sources x {len(commits)} commits; errors={len(errors)}')
if errors:
    for e in errors: print('ERROR',e)
    raise SystemExit(1)
