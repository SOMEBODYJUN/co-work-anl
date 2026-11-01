"""Nonmathematical package checks; does not import or execute frozen programs."""
from pathlib import Path
import ast, hashlib, json, re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
BODY=ROOT/'archives/customer-attraction/state/程序/历史依赖策略锥的搜索程序--程序.md'
RECEIPT=ROOT/'cleanup/workspaces/Boss7/receipts-round10/984ad082aeaf3857d562.json'
manifest=json.loads((HERE/'source-manifest.json').read_text())
raw=(HERE/manifest['preserved_path']).read_bytes()
assert len(raw)==manifest['source']['size']==11589
assert hashlib.sha256(raw).hexdigest()==manifest['source']['sha256']
receipt=json.loads(RECEIPT.read_text())
assert receipt['id']==manifest['source']['id']=='984ad082aeaf3857d562'
assert receipt['disposition']=='integrated'
assert all((ROOT/p).is_file() for p in receipt['targets'])
for p in HERE.rglob('*.py'): ast.parse(p.read_text(),filename=str(p))
for p in HERE.rglob('*.json'): json.loads(p.read_text())
links=[]
for p in [BODY,HERE/'README.md']:
    for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
        if '://' in link: continue
        dest=(p.parent/link.split('#',1)[0]).resolve()
        if dest.name=='self-check.json': continue
        assert dest.exists(),(str(p),link)
        links.append({'from':str(p.relative_to(ROOT)),'target':str(dest.relative_to(ROOT))})
report=json.loads((HERE/'small-contract-report.json').read_text())
assert report['original_main_calls']==0 and report['total_solver_calls']==2
assert sum(c['matrix_coordinates_compared'] for c in report['cases'])==294
assert sum(c['exact_all_history_including_self_comparisons'] for c in report['cases'])==78
assert all(c['candidate_full_policy_roundtrip'] for c in report['cases'])
assert report['cases'][1]['same_count_groups_with_different_actions']==1
comp=json.loads((HERE/'comparison-manifest.json').read_text())
for item in comp['related_full_reads']:
    data=(ROOT/item['path']).read_bytes()
    assert len(data)==item['bytes']
    assert hashlib.sha256(data).hexdigest()==item['sha256']
files=[]
for p in sorted([BODY,RECEIPT,*HERE.rglob('*')]):
    if not p.is_file() or p.name=='self-check.json':continue
    assert '__pycache__' not in p.parts
    files.append({'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
out={'status':'pass','scope':'package integrity and links only; no additional mathematical program invocation','previous_package_attempts':[{'status':'failed','reason':'repository root used parents[3] instead of parents[4]; fixed before this final check','mathematical_calls':0}],'source_bytes_sha_verified':True,'comparison_snapshots_still_match':8,'targets_exist':len(receipt['targets']),'links':links,'files':files}
(HERE/'self-check.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'pass','files':len(files),'links':len(links),'mathematical_reruns':0},ensure_ascii=False))
