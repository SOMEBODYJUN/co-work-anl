"""Static source/record/link checks only; no imports or mathematical replays."""
from pathlib import Path
import ast,hashlib,json,re
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4]
BODY=ROOT/'archives/customer-attraction/state/程序/同源回复再查询的分离程序--程序.md'
RECEIPT=ROOT/'cleanup/workspaces/Boss7/receipts-round12/fc07ebb90129de65f3b8.json'
manifest=json.loads((HERE/'source-manifest.json').read_text())
for item in manifest['sources']:
    data=(HERE/item['preserved_path']).read_bytes();source=item['source']
    assert len(data)==source['size'] and hashlib.sha256(data).hexdigest()==source['sha256']
comp=json.loads((HERE/'comparison-manifest.json').read_text())
for item in comp['formal_and_raw_comparisons']:
    data=(ROOT/item['path']).read_bytes()
    assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256']
receipt=json.loads(RECEIPT.read_text())
assert receipt['id']=='fc07ebb90129de65f3b8' and receipt['disposition']=='integrated'
assert all((ROOT/p).is_file() for p in receipt['targets'])
for p in HERE.rglob('*.py'):ast.parse(p.read_text(),filename=str(p))
for p in HERE.rglob('*.json'):json.loads(p.read_text())
links=[]
for p in (BODY,HERE/'README.md'):
    for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
        if '://' in link:continue
        target=(p.parent/link.split('#',1)[0]).resolve()
        if target.name=='self-check.json':continue
        assert target.exists(),(str(p),link)
        links.append({'from':str(p.relative_to(ROOT)),'target':str(target.relative_to(ROOT))})
event=json.loads((HERE/'replay/execution.json').read_text())
assert event['exit_code']==0 and event['original_main_calls']==1 and not event['all_queries']
assert event['dependency_main_calls']==0 and event['before']==event['after']
assert len((HERE/'replay/stdout.txt').read_bytes())==event['stdout_bytes']==300
assert (HERE/'replay/stderr.txt').read_bytes()==b''
report=json.loads((HERE/'replay/report.json').read_text())
assert report['LPs']==24 and len(report['selected'])==5
old=json.loads((HERE/'related/early_reply_requery_master_all_queries.json').read_text())
assert old['LPs']==384 and len(old['selected'])==14
assert [r for r in old['selected'] if r['cut']['query']==5]==report['selected']
peer=json.loads((HERE.parent/'local-reply-portfolio-joint-cuts/exact-audit.json').read_text())
key=lambda c:json.dumps(c,sort_keys=True)
peer_records={key(r['cut']):r['exact_slack_on_frozen_5180_point'] for r in peer['all_rows'] if r['family']=='requery'}
assert len(peer_records)==5
assert {key(r['cut']):r['slack'] for r in report['selected']}==peer_records
files=[]
for p in sorted([BODY,RECEIPT,*HERE.rglob('*')]):
    if not p.is_file() or p.name=='self-check.json':continue
    assert '__pycache__' not in p.parts
    data=p.read_bytes();files.append({'path':str(p.relative_to(ROOT)),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
result={'status':'pass','scope':'static source bytes, syntax, record identity and links only; no mathematical imports/entries/LPs',
        'verified_source_records':len(manifest['sources']),'comparison_hashes':len(comp['formal_and_raw_comparisons']),
        'five_default_records_match_historical_query5_and_peer_diagnostics':True,'links':links,'files':files}
(HERE/'self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'pass','files':len(files),'links':len(links),'mathematical_reruns':0},ensure_ascii=False))
